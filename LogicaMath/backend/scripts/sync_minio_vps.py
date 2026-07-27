#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Sincronización de Imágenes a MinIO de la VPS
======================================================
Este script lee las imágenes del MinIO local y las sube de forma asíncrona
al bucket correspondiente de la VPS (Desarrollo o Producción) según el flag provisto.
"""

import asyncio
import os
import sys
import argparse
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

# Configurar path de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Cargar configuración local de S3
from app.config import settings

def load_env_credentials(env_name: str):
    """Carga credenciales específicas del archivo .env correspondiente."""
    if env_name == "local":
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        env_path = os.path.join(base_dir, "Datos_localhost", ".env.local")
        if not os.path.exists(env_path):
            env_path = os.path.join("Datos_localhost", ".env.local")
    else:
        # Intentar leer desde las copias mapeadas en /app/data
        env_path = f"/app/data/env_{env_name}"
        
        if not os.path.exists(env_path):
            env_path = f"data/env_{env_name}"
            
        if not os.path.exists(env_path):
            env_dir = "Datos_Desarrollo" if env_name == "dev" else "Datos_Producion"
            env_path = os.path.join("..", env_dir, ".env")
            
        if not os.path.exists(env_path):
            env_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "Datos_Desarrollo" if env_name == "dev" else "Datos_Producion", ".env")

        if not os.path.exists(env_path):
            # Intentar ruta relativa directa si se ejecuta desde la raíz de la app
            env_dir = "Datos_Desarrollo" if env_name == "dev" else "Datos_Producion"
            env_path = os.path.join(env_dir, ".env")

    if not os.path.exists(env_path):
        raise FileNotFoundError(f"No se pudo encontrar el archivo env en: {env_path}")
        
    creds = {}
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                key, val = line.strip().split("=", 1)
                creds[key.strip()] = val.strip()
    return creds

async def sync_images(
    env_name: str,
    batch_size: int = 3,
    fase5_only: bool = False,
    fase_id=None,
):
    print("=" * 90)
    print(f"SINCRONIZANDO IMÁGENES HACIA VPS - ENTORNO: {env_name.upper()}")
    if fase5_only:
        print("   (MODO legacy: Solo figuras de Fase 5)")
    if fase_id is not None:
        print(f"   (MODO: Solo figuras referenciadas por fase_id={fase_id})")
        if fase_id in (5, 6):
            print("   [!] Fases 5–6 usan SVG inline (bd_minio §1.3); normalmente no hay graphics/.")
    print("=" * 90)

    # 1. Cargar credenciales del destino
    try:
        remote_creds = load_env_credentials(env_name)
    except Exception as e:
        print(f"❌ Error al cargar credenciales del entorno {env_name}: {e}")
        return

    # Extraer variables remotas (sin fallbacks hardcodeados de secretos — bd_minio §2)
    remote_access_key = remote_creds.get("S3_ACCESS_KEY")
    remote_secret_key = remote_creds.get("S3_SECRET_KEY")
    remote_bucket = remote_creds.get("S3_BUCKET_NAME")
    remote_endpoint = (
        remote_creds.get("S3_ENDPOINT_URL")
        or remote_creds.get("S3_ENDPOINT")
        or remote_creds.get("S3_PUBLIC_URL")
    )

    if not all([remote_access_key, remote_secret_key, remote_bucket, remote_endpoint]):
        raise RuntimeError(
            "Faltan S3_ACCESS_KEY / S3_SECRET_KEY / S3_BUCKET_NAME / "
            "(S3_ENDPOINT_URL|S3_ENDPOINT|S3_PUBLIC_URL) en el .env del destino. "
            "No se usan credenciales hardcodeadas."
        )

    print(f"Destino:")
    print(f" - Endpoint: {remote_endpoint}")
    print(f" - Bucket:   {remote_bucket}")
    print(f" - Key ID:   {remote_access_key[:6]}...")

    # 2. Inicializar clientes de S3 (Local y Remoto)
    try:
        local_creds = load_env_credentials("local")
    except Exception as e:
        print(f"[!] Error al cargar credenciales del entorno local: {e}")
        return

    local_access_key = local_creds.get("S3_ACCESS_KEY")
    local_secret_key = local_creds.get("S3_SECRET_KEY")
    local_bucket = local_creds.get("S3_BUCKET_NAME", "logicakids")

    # Si corre en docker backend, el endpoint interno es http://minio:9000
    in_docker = os.environ.get("DATABASE_URL") is not None
    local_endpoint = "http://minio:9000" if in_docker else "http://localhost:9100"
    
    local_s3 = boto3.client(
        's3',
        endpoint_url=local_endpoint,
        aws_access_key_id=local_access_key,
        aws_secret_access_key=local_secret_key,
        config=Config(s3={'addressing_style': 'path'})
    )

    remote_s3 = boto3.client(
        's3',
        endpoint_url=remote_endpoint,
        aws_access_key_id=remote_access_key,
        aws_secret_access_key=remote_secret_key,
        config=Config(s3={'addressing_style': 'path'}, signature_version='s3v4')
    )

    # 3. Listar objetos en el bucket local bajo el prefijo 'graphics/'
    print("\n[+] Listando objetos del bucket local...")
    try:
        paginator = local_s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=local_bucket, Prefix='graphics/')
        
        local_keys = []
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    local_keys.append(obj['Key'])
    except Exception as e:
        print(f"[!] Error al listar objetos locales: {e}")
        return

    filter_fase = 5 if fase5_only else fase_id
    if filter_fase is not None:
        import psycopg2
        print(f"   [+] Mapeando filenames de graphics/ para fase_id={filter_fase}...")
        try:
            local_db_url = local_creds["DATABASE_URL"].replace("+asyncpg", "")
            local_db_url = local_db_url.replace("@postgres:5432/", "@localhost:5433/")

            conn = psycopg2.connect(local_db_url)
            filenames = set()
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT datos_numericos FROM preguntas WHERE fase_id = %s AND datos_numericos IS NOT NULL;",
                    (filter_fase,),
                )
                for row in cur.fetchall():
                    datos = row[0]
                    if isinstance(datos, str):
                        import json
                        try:
                            datos = json.loads(datos)
                        except Exception:
                            continue
                    if isinstance(datos, dict) and "url" in datos:
                        url = datos["url"] or ""
                        if "graphics/" in url:
                            filenames.add(url.split("graphics/")[-1].split("?")[0])
                        else:
                            filenames.add(url.split("/")[-1])
            conn.close()
            print(f"       Mapeados {len(filenames)} filenames en DB.")
            local_keys = [k for k in local_keys if k.split("/")[-1] in filenames]
        except Exception as db_err:
            print(f"   [!] Falló filtro por fase en DB local: {db_err}. Se sincronizarán todas.")

    total_files = len(local_keys)
    print(f"Total de imágenes locales encontradas: {total_files}")
    if total_files == 0:
        print("No hay imágenes locales para sincronizar.")
        return

    # 4. Sincronizar en lotes (batches) asíncronos para velocidad
    sem = asyncio.Semaphore(batch_size)
    success_count = 0
    fail_count = 0

    async def sync_single_file(key: str):
        nonlocal success_count, fail_count
        async with sem:
            max_attempts = 3
            for attempt in range(1, max_attempts + 1):
                try:
                    # Descargar objeto local a memoria
                    local_obj = await asyncio.to_thread(
                        local_s3.get_object,
                        Bucket=local_bucket,
                        Key=key
                    )
                    file_data = local_obj['Body'].read()
                    content_type = local_obj.get('ContentType', 'image/png')

                    # Subir al MinIO remoto de la VPS
                    await asyncio.to_thread(
                        remote_s3.put_object,
                        Bucket=remote_bucket,
                        Key=key,
                        Body=file_data,
                        ContentType=content_type
                    )
                    success_count += 1
                    break
                except Exception as e:
                    if attempt == max_attempts:
                        print(f"   [!] Falló sincronización de key '{key}' (Intento {attempt}/{max_attempts}): {e}")
                        fail_count += 1
                    else:
                        # Breve pausa antes de reintentar
                        await asyncio.sleep(attempt * 1.5)

    print(f"\n[+] Iniciando subida de {total_files} archivos a la VPS en lotes de {batch_size} (con auto-retry)...")
    
    tasks = [sync_single_file(key) for key in local_keys]
    
    # Correr todas las tareas e imprimir avance cada 200 archivos
    for chunk_start in range(0, len(tasks), 200):
        chunk = tasks[chunk_start:chunk_start+200]
        await asyncio.gather(*chunk)
        print(f"   Progreso: {min(chunk_start + 200, total_files)}/{total_files} procesados...")

    print("\n" + "=" * 90)
    print("RESUMEN DE SINCRONIZACIÓN DE IMÁGENES:")
    print(f" - Entorno Destino:                     {env_name.upper()}")
    print(f" - Archivos exitosamente sincronizados: {success_count}")
    print(f" - Archivos fallidos:                  {fail_count}")
    print("=" * 90)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sincroniza imágenes locales de MinIO (graphics/) con la VPS.")
    parser.add_argument("--env", choices=["dev", "prod"], required=True, help="Entorno de la VPS (dev o prod)")
    parser.add_argument(
        "--fase5-only",
        action="store_true",
        help="(Legacy) Solo figuras referenciadas por fase_id=5",
    )
    parser.add_argument(
        "--fase",
        type=int,
        default=None,
        help="Solo figuras referenciadas por preguntas de este fase_id",
    )
    args = parser.parse_args()

    asyncio.run(sync_images(args.env, fase5_only=args.fase5_only, fase_id=args.fase))
