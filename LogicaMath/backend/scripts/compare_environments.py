#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Comparación de Entornos (Local, Desarrollo y Producción)
==================================================================
Este script analiza y compara:
1. Las preguntas y alternativas de la Base de Datos.
2. Los archivos/figuras de MinIO bajo el prefijo 'graphics/'.

Requiere que los túneles SSH de la base de datos de Desarrollo y Producción
estén activos si se ejecuta desde una máquina local.
"""

import os
import sys
import argparse
import psycopg2
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from urllib.parse import urlparse

def load_env_file(filepath: str) -> dict:
    """Lee un archivo .env y retorna un diccionario con sus claves y valores."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No se encontró el archivo .env en: {filepath}")
    
    env_data = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                env_data[key.strip()] = val.strip()
    return env_data

def rewrite_db_url(db_url: str, override_host: str = None, override_port: int = None) -> str:
    """Convierte una URL asyncpg en una URL compatible con psycopg2 y permite sobrescribir host y puerto."""
    # Pre-procesar para codificar '#' en la sección de usuario/contraseña
    if "://" in db_url:
        scheme, rest = db_url.split("://", 1)
        if "@" in rest:
            auth, host_path = rest.split("@", 1)
            auth = auth.replace("#", "%23")
            db_url = f"{scheme}://{auth}@{host_path}"

    # Quitar el prefijo +asyncpg
    url = db_url.replace("+asyncpg", "")
    
    if not override_host and not override_port:
        return url
        
    parsed = urlparse(url)
    scheme = parsed.scheme
    netloc = parsed.netloc
    path = parsed.path
    
    # Extraer usuario y contraseña si existen
    auth = ""
    host_port = netloc
    if "@" in netloc:
        auth, host_port = netloc.split("@", 1)
        auth += "@"
        
    host = host_port
    port = ""
    if ":" in host_port:
        host, port = host_port.split(":", 1)
        
    new_host = override_host if override_host else host
    new_port = str(override_port) if override_port else port
    
    new_netloc = auth + new_host
    if new_port:
        new_netloc += ":" + new_port
        
    return f"{scheme}://{new_netloc}{path}"

def get_db_questions(db_url: str, env_name: str) -> dict:
    """Conecta a la base de datos y obtiene el conteo e información de las preguntas."""
    print(f"[+] Conectando a Base de Datos de {env_name.upper()}...")
    questions = {}
    alternatives_count = {}
    
    try:
        conn = psycopg2.connect(db_url)
        with conn.cursor() as cur:
            # Primero consultar conteo de alternativas por pregunta
            cur.execute("SELECT pregunta_id, COUNT(*) FROM alternativas GROUP BY pregunta_id;")
            for row in cur.fetchall():
                alternatives_count[row[0]] = row[1]
                
            # Consultar preguntas
            cur.execute("""
                SELECT id, fase_id, seccion, enunciado, respuesta_correcta 
                FROM preguntas 
                ORDER BY id;
            """)
            for row in cur.fetchall():
                q_id, fase_id, seccion, enunciado, respuesta = row
                questions[q_id] = {
                    "id": q_id,
                    "fase_id": fase_id,
                    "seccion": seccion,
                    "enunciado": enunciado.strip() if enunciado else "",
                    "respuesta_correcta": respuesta.strip() if respuesta else "",
                    "num_alternativas": alternatives_count.get(q_id, 0)
                }
        conn.close()
        print(f"    ✅ Conexión exitosa a {env_name.upper()}. Total preguntas: {len(questions)}")
    except Exception as e:
        print(f"    ❌ Error al conectar o consultar la base de datos de {env_name.upper()}: {e}")
        return None
        
    return questions

def list_minio_objects(endpoint: str, access_key: str, secret_key: str, bucket: str, env_name: str) -> set:
    """Lista todos los objetos bajo el prefijo 'graphics/' en el bucket de MinIO especificado."""
    print(f"[+] Conectando a MinIO de {env_name.upper()} ({endpoint}, bucket: {bucket})...")
    keys = set()
    try:
        s3 = boto3.client(
            's3',
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=Config(s3={'addressing_style': 'path'})
        )
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket, Prefix='graphics/')
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    keys.add(obj['Key'])
                    
        print(f"    ✅ Conexión exitosa a MinIO de {env_name.upper()}. Total figuras: {len(keys)}")
    except Exception as e:
        print(f"    ❌ Error al conectar o listar objetos en MinIO de {env_name.upper()}: {e}")
        return None
        
    return keys

def compare_db_data(local_q: dict, remote_q: dict, env_name: str):
    """Compara las preguntas locales con un entorno remoto."""
    print(f"\n=== COMPARACIÓN DE BASE DE DATOS: LOCAL vs {env_name.upper()} ===")
    
    if not local_q:
        print("❌ No hay datos locales para comparar.")
        return
    if not remote_q:
        print(f"⚠️ No se pudo realizar la comparación con {env_name.upper()} debido a fallos de conexión.")
        return

    local_ids = set(local_q.keys())
    remote_ids = set(remote_q.keys())
    
    # 1. Preguntas que están en local pero faltan en el remoto
    missing_in_remote = local_ids - remote_ids
    # 2. Preguntas que están en el remoto pero no en local
    extra_in_remote = remote_ids - local_ids
    
    # 3. Preguntas con diferencias de contenido
    common_ids = local_ids & remote_ids
    content_differences = []
    
    for q_id in common_ids:
        l_item = local_q[q_id]
        r_item = remote_q[q_id]
        
        diffs = []
        if l_item["fase_id"] != r_item["fase_id"]:
            diffs.append(f"Fase ({l_item['fase_id']} vs {r_item['fase_id']})")
        if l_item["seccion"] != r_item["seccion"]:
            diffs.append(f"Sección ({l_item['seccion']} vs {r_item['seccion']})")
        if l_item["enunciado"] != r_item["enunciado"]:
            diffs.append("Enunciado diferente")
        if l_item["respuesta_correcta"] != r_item["respuesta_correcta"]:
            diffs.append(f"Respuesta ({l_item['respuesta_correcta']} vs {r_item['respuesta_correcta']})")
        if l_item["num_alternativas"] != r_item["num_alternativas"]:
            diffs.append(f"Alternativas ({l_item['num_alternativas']} vs {r_item['num_alternativas']})")
            
        if diffs:
            content_differences.append((q_id, diffs))
            
    # Mostrar resultados
    print(f"Resumen de diferencias:")
    print(f" - Preguntas idénticas en ID y estructura: {len(common_ids) - len(content_differences)}/{len(local_ids)}")
    print(f" - Preguntas locales faltantes en {env_name.upper()} (por ID): {len(missing_in_remote)}")
    print(f" - Preguntas extra en {env_name.upper()} (no están en local): {len(extra_in_remote)}")
    print(f" - Preguntas con diferencias de contenido/estructura: {len(content_differences)}")
    
    if missing_in_remote:
        print(f"\n⚠️ IDs de preguntas locales faltantes en {env_name.upper()} (primeros 15):")
        print(f"   {list(missing_in_remote)[:15]}")
        
    if extra_in_remote:
        print(f"\n⚠️ IDs de preguntas extra en {env_name.upper()} (primeros 15):")
        print(f"   {list(extra_in_remote)[:15]}")
        
    if content_differences:
        print(f"\n⚠️ Preguntas con discrepancias detectadas (primeros 10):")
        for q_id, diffs in content_differences[:10]:
            l_val = local_q[q_id]
            print(f"   • ID {q_id} [Fase {l_val['fase_id']}, Sec {l_val['seccion']}]: {', '.join(diffs)}")

def compare_minio_data(local_files: set, remote_files: set, env_name: str):
    """Compara las figuras locales de MinIO con un entorno remoto."""
    print(f"\n=== COMPARACIÓN DE MINIO: LOCAL vs {env_name.upper()} ===")
    
    if local_files is None:
        print("❌ No se pudieron cargar las figuras locales.")
        return
    if remote_files is None:
        print(f"⚠️ No se pudo realizar la comparación con {env_name.upper()} debido a fallos de conexión.")
        return

    # 1. Figuras locales faltantes en remoto
    missing_in_remote = local_files - remote_files
    # 2. Figuras extra en remoto
    extra_in_remote = remote_files - local_files
    # 3. Coincidencias
    matches = local_files & remote_files
    
    print(f"Resumen de figuras:")
    print(f" - Figuras idénticas presentes en ambos: {len(matches)}")
    print(f" - Figuras locales faltantes en {env_name.upper()}: {len(missing_in_remote)}")
    print(f" - Figuras extra en {env_name.upper()} (no están local): {len(extra_in_remote)}")
    
    if missing_in_remote:
        print(f"\n❌ Figuras locales que FALTAN subir a {env_name.upper()} (primeros 15):")
        for f in sorted(list(missing_in_remote))[:15]:
            print(f"   • {f}")
            
    if extra_in_remote:
        print(f"\n⚠️ Figuras extra en {env_name.upper()} que no están en Local (primeros 15):")
        for f in sorted(list(extra_in_remote))[:15]:
            print(f"   • {f}")

def main():
    parser = argparse.ArgumentParser(
        description="Analiza y compara bases de datos y figuras de MinIO entre Local, Desarrollo y Producción.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--local-db-port", type=int, default=5433, help="Puerto local de Postgres en el host (defecto: 5433)")
    parser.add_argument("--dev-db-port", type=int, default=5434, help="Puerto local del túnel SSH para Desarrollo (defecto: 5434)")
    parser.add_argument("--prod-db-port", type=int, default=5435, help="Puerto local del túnel SSH para Producción (defecto: 5435)")
    parser.add_argument("--skip-db", action="store_true", help="Ignorar la comparación de bases de datos")
    parser.add_argument("--skip-minio", action="store_true", help="Ignorar la comparación de MinIO")
    args = parser.parse_args()

    print("=" * 90)
    print("INICIANDO ANALISIS COMPARATIVO DE ENTORNOS (LOCAL / DESARROLLO / PRODUCCION)")
    print("=" * 90)

    # 1. Rutas a los archivos .env
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    
    # Rutas típicas en el host
    local_env_path = os.path.join(base_dir, "Datos_localhost", ".env.local")
    dev_env_path = os.path.join(base_dir, "Datos_Desarrollo", ".env")
    prod_env_path = os.path.join(base_dir, "Datos_Producion", ".env")

    # Si estamos dentro de un contenedor Docker, las rutas del VPS montadas están en la raíz /
    if not os.path.exists(dev_env_path) and os.path.exists("/Datos_Desarrollo/.env"):
        dev_env_path = "/Datos_Desarrollo/.env"
    if not os.path.exists(prod_env_path) and os.path.exists("/Datos_Producion/.env"):
        prod_env_path = "/Datos_Producion/.env"

    print("[+] Cargando configuraciones de los entornos...")
    local_env = {}
    try:
        # Cargar local
        if os.path.exists(local_env_path):
            local_env = load_env_file(local_env_path)
        else:
            # Si no existe (ej. dentro del docker), usar variables de entorno del sistema
            print("    ℹ️ Archivo local .env.local no encontrado. Cargando de las variables de entorno del sistema.")
            local_env = {
                "DATABASE_URL": os.environ.get("DATABASE_URL"),
                "S3_ENDPOINT_URL": os.environ.get("S3_ENDPOINT_URL"),
                "S3_PUBLIC_URL": os.environ.get("S3_PUBLIC_URL"),
                "S3_BUCKET_NAME": os.environ.get("S3_BUCKET_NAME"),
                "S3_ACCESS_KEY": os.environ.get("S3_ACCESS_KEY"),
                "S3_SECRET_KEY": os.environ.get("S3_SECRET_KEY"),
            }
            
        dev_env = load_env_file(dev_env_path)
        prod_env = load_env_file(prod_env_path)
        print("    ✅ Configuraciones cargadas correctamente.")
    except Exception as e:
        print(f"    ❌ Error al cargar archivos de configuración: {e}")
        sys.exit(1)

    # Variables de base de datos
    local_questions, dev_questions, prod_questions = None, None, None

    if not args.skip_db:
        # Si corre dentro de Docker, el host para postgres local es 'postgres' en lugar de 'localhost'
        in_docker = os.environ.get("DATABASE_URL") is not None
        local_host = "postgres" if in_docker else "localhost"
        vps_host = "host.docker.internal" if in_docker else "localhost"
        
        local_db_url = rewrite_db_url(local_env.get("DATABASE_URL"), override_host=local_host, override_port=args.local_db_port if local_host == "localhost" else None)
        # Para base de datos de desarrollo y producción en VPS
        dev_db_url = rewrite_db_url(dev_env.get("DATABASE_URL"), override_host=vps_host, override_port=args.dev_db_port)
        prod_db_url = rewrite_db_url(prod_env.get("DATABASE_URL"), override_host=vps_host, override_port=args.prod_db_port)

        print("\n--- ANALISIS DE BASE DE DATOS (PREGUNTAS) ---")
        local_questions = get_db_questions(local_db_url, "local")
        
        if local_questions is None:
            print("❌ No se pudo conectar a la base de datos LOCAL. Abortando análisis de bases de datos.")
        else:
            dev_questions = get_db_questions(dev_db_url, "desarrollo")
            prod_questions = get_db_questions(prod_db_url, "producción")
            
            compare_db_data(local_questions, dev_questions, "desarrollo")
            compare_db_data(local_questions, prod_questions, "producción")

    if not args.skip_minio:
        print("\n--- ANALISIS DE FIGURAS EN STORAGE (MINIO) ---")
        # Si corre en docker backend, el endpoint interno es http://minio:9000
        # Si corre en host, el endpoint es local_env.S3_PUBLIC_URL o http://localhost:9100
        in_docker = os.environ.get("DATABASE_URL") is not None
        local_endpoint = "http://minio:9000" if in_docker else local_env.get("S3_PUBLIC_URL", "http://localhost:9100")
        local_bucket = local_env.get("S3_BUCKET_NAME", "logicakids")
        local_access = local_env.get("S3_ACCESS_KEY")
        local_secret = local_env.get("S3_SECRET_KEY")
        
        # Desarrollo
        dev_endpoint = "https://files.espalhar.shop"
        dev_bucket = dev_env.get("S3_BUCKET_NAME", "logicakids")
        dev_access = dev_env.get("S3_ACCESS_KEY")
        dev_secret = dev_env.get("S3_SECRET_KEY")
        
        # Producción
        prod_endpoint = "https://files.espalhar.shop"
        prod_bucket = prod_env.get("S3_BUCKET_NAME", "logicakids-producion")
        prod_access = prod_env.get("S3_ACCESS_KEY")
        prod_secret = prod_env.get("S3_SECRET_KEY")

        local_files = list_minio_objects(local_endpoint, local_access, local_secret, local_bucket, "local")
        
        if local_files is None:
            print("❌ No se pudo conectar al MinIO LOCAL. Abortando análisis de almacenamiento.")
        else:
            dev_files = list_minio_objects(dev_endpoint, dev_access, dev_secret, dev_bucket, "desarrollo")
            prod_files = list_minio_objects(prod_endpoint, prod_access, prod_secret, prod_bucket, "producción")
            
            compare_minio_data(local_files, dev_files, "desarrollo")
            compare_minio_data(local_files, prod_files, "producción")

    print("\n" + "=" * 90)
    print("ANÁLISIS COMPARATIVO FINALIZADO")
    print("=" * 90)

if __name__ == "__main__":
    main()
