#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Sincronización Segura a Producción (VPS)
==================================================
Este script realiza las siguientes acciones de forma automática:
1. Sincroniza todas las imágenes del bucket local de MinIO bajo 'graphics/'
   hacia el bucket de producción en la VPS.
2. Compara y sincroniza las tablas 'preguntas' y 'alternativas':
   - Modifica las existentes con la versión local actual.
   - Inserta las nuevas locales.
   - Elimina las preguntas de la VPS que ya no están en local, SIEMPRE Y CUANDO
     no tengan intentos de alumnos ni estén en pools de asignación activos.
   - Deja intactas las tablas de alumnos, usuarios y progresos/intentos.

REQUISITO:
Tener abierto el túnel SSH para la base de datos de producción en el puerto 5435:
ssh -L 5435:localhost:5432 rominejo@35.222.6.7 -N
"""

import os
import sys
import json
import asyncio
import argparse
import psycopg2
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from urllib.parse import urlparse

# Cargar configuración del .env
def load_env_file(filepath: str) -> dict:
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
    # Quitar asyncpg
    url = db_url.replace("+asyncpg", "")
    
    # Pre-procesar para codificar '#' en la sección de auth
    if "://" in url:
        scheme, rest = url.split("://", 1)
        if "@" in rest:
            auth, host_path = rest.split("@", 1)
            auth = auth.replace("#", "%23")
            url = f"{scheme}://{auth}@{host_path}"

    if not override_host and not override_port:
        return url
        
    parsed = urlparse(url)
    scheme = parsed.scheme
    netloc = parsed.netloc
    path = parsed.path
    
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

# =====================================================================
# SINCRONIZACIÓN DE IMÁGENES EN MINIO
# =====================================================================
async def sync_minio_images(local_env: dict, prod_env: dict):
    print("\n" + "="*80)
    print("[+] INICIANDO SINCRONIZACIÓN DE IMÁGENES (MINIO)")
    print("="*80)

    # Credenciales Locales
    local_access = local_env.get("S3_ACCESS_KEY", "logicakids_minio_admin")
    local_secret = local_env.get("S3_SECRET_KEY", "LogicaKids2026#MinIO")
    local_bucket = local_env.get("S3_BUCKET_NAME", "logicakids")
    local_endpoint = "http://localhost:9100"  # Endpoint desde el host

    # Credenciales VPS Producción
    prod_access = prod_env.get("S3_ACCESS_KEY")
    prod_secret = prod_env.get("S3_SECRET_KEY")
    prod_bucket = prod_env.get("S3_BUCKET_NAME", "logicakids-producion")
    prod_endpoint = "https://files.espalhar.shop"

    print(f"[*] Origen:  Local MinIO ({local_endpoint}, bucket: '{local_bucket}')")
    print(f"[*] Destino: VPS MinIO ({prod_endpoint}, bucket: '{prod_bucket}')")

    # Inicializar clientes
    try:
        local_s3 = boto3.client(
            's3',
            endpoint_url=local_endpoint,
            aws_access_key_id=local_access,
            aws_secret_access_key=local_secret,
            config=Config(s3={'addressing_style': 'path'})
        )
        prod_s3 = boto3.client(
            's3',
            endpoint_url=prod_endpoint,
            aws_access_key_id=prod_access,
            aws_secret_access_key=prod_secret,
            config=Config(s3={'addressing_style': 'path'}, signature_version='s3v4')
        )
    except Exception as e:
        print(f"❌ Error al inicializar clientes de MinIO: {e}")
        return

    # Listar objetos locales
    print("[*] Listando archivos del bucket local bajo el prefijo 'graphics/'...")
    try:
        paginator = local_s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=local_bucket, Prefix='graphics/')
        local_keys = []
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    local_keys.append(obj['Key'])
    except Exception as e:
        print(f"❌ Error al listar objetos del MinIO local: {e}")
        return

    total_files = len(local_keys)
    print(f"✅ Se encontraron {total_files} figuras locales para sincronizar.")
    if total_files == 0:
        return

    # Sincronizar en lotes asíncronos
    sem = asyncio.Semaphore(5)
    success_count = 0
    fail_count = 0

    async def sync_file(key: str):
        nonlocal success_count, fail_count
        async with sem:
            try:
                # Descargar local
                obj = await asyncio.to_thread(local_s3.get_object, Bucket=local_bucket, Key=key)
                file_data = obj['Body'].read()
                content_type = obj.get('ContentType', 'image/png')

                # Subir a la VPS
                await asyncio.to_thread(
                    prod_s3.put_object,
                    Bucket=prod_bucket,
                    Key=key,
                    Body=file_data,
                    ContentType=content_type
                )
                success_count += 1
            except Exception as ex:
                print(f"   [!] Error al sincronizar '{key}': {ex}")
                fail_count += 1

    tasks = [sync_file(k) for k in local_keys]
    
    # Procesar y mostrar progreso
    for start_idx in range(0, len(tasks), 100):
        chunk = tasks[start_idx:start_idx+100]
        await asyncio.gather(*chunk)
        print(f"   Progreso de subida: {min(start_idx + 100, total_files)}/{total_files} procesados...")

    print(f"✅ Sincronización de figuras completa. Exitosos: {success_count}, Fallidos: {fail_count}")

# =====================================================================
# SINCRONIZACIÓN DE BASE DE DATOS
# =====================================================================
def sync_database(local_db_url: str, prod_db_url: str):
    print("\n" + "="*80)
    print("[+] INICIANDO SINCRONIZACIÓN DE BASE DE DATOS (PREGUNTAS Y ALTERNATIVAS)")
    print("="*80)

    try:
        local_conn = psycopg2.connect(local_db_url)
        prod_conn = psycopg2.connect(prod_db_url)
        print("✅ Conexiones a bases de datos establecidas con éxito.")
    except Exception as e:
        print(f"❌ Error al conectar a las bases de datos: {e}")
        return

    try:
        # 1. Obtener datos locales
        print("[*] Leyendo preguntas y alternativas locales...")
        local_questions = {}
        with local_conn.cursor() as cur:
            cur.execute("""
                SELECT id, fase_id, seccion, sub_nivel, estructura_padre_id, operacion, tipo_pregunta,
                       enunciado, respuesta_correcta, datos_numericos, payload_tokenizado, 
                       explicacion_paso_a_paso, requiere_subrayado, palabras_clave, errores_previstos,
                       creado_por, modificado_por, estado, revisado_admin, revisado_por, fecha_revision
                FROM preguntas;
            """)
            columns = [desc[0] for desc in cur.description]
            for row in cur.fetchall():
                q_data = dict(zip(columns, row))
                local_questions[q_data['id']] = q_data

            # Leer alternativas locales
            cur.execute("SELECT id, pregunta_id, texto, es_correcta, orden, tipo_error, feedback_error FROM alternativas;")
            local_alternatives = {}
            for row in cur.fetchall():
                alt = {
                    "id": row[0],
                    "pregunta_id": row[1],
                    "texto": row[2],
                    "es_correcta": row[3],
                    "orden": row[4],
                    "tipo_error": row[5],
                    "feedback_error": row[6]
                }
                if alt["pregunta_id"] not in local_alternatives:
                    local_alternatives[alt["pregunta_id"]] = []
                local_alternatives[alt["pregunta_id"]].append(alt)

        print(f"   Local: {len(local_questions)} preguntas cargadas.")

        # 2. Obtener preguntas de la VPS
        prod_question_ids = set()
        with prod_conn.cursor() as cur:
            cur.execute("SELECT id FROM preguntas;")
            for row in cur.fetchall():
                prod_question_ids.add(row[0])
        print(f"   VPS Producción: {len(prod_question_ids)} preguntas existentes.")

        # 3. Detectar preguntas huérfanas en la VPS (existen en VPS pero ya no en local)
        orphans = prod_question_ids - set(local_questions.keys())
        deleted_count = 0
        preserved_count = 0

        if orphans:
            print(f"[*] Se detectaron {len(orphans)} preguntas en la VPS que ya no están localmente.")
            print("[*] Evaluando si es seguro eliminarlas sin romper el progreso de los alumnos...")
            
            with prod_conn.cursor() as cur:
                for q_id in orphans:
                    # Verificar FKs en progreso, intentos e intento_preguntas
                    cur.execute("""
                        SELECT EXISTS (
                            SELECT 1 FROM pool_asignado_alumno WHERE pregunta_id = %s
                            UNION ALL
                            SELECT 1 FROM intentos WHERE pregunta_id = %s
                            UNION ALL
                            SELECT 1 FROM intento_preguntas WHERE pregunta_id = %s
                        );
                    """, (q_id, q_id, q_id))
                    has_progress = cur.fetchone()[0]
                    
                    if not has_progress:
                        # Es seguro eliminarla (las alternativas se borran en cascada si está la FK configurada,
                        # pero para asegurar las borramos a mano primero)
                        cur.execute("DELETE FROM alternativas WHERE pregunta_id = %s;", (q_id,))
                        cur.execute("DELETE FROM preguntas WHERE id = %s;", (q_id,))
                        deleted_count += 1
                    else:
                        # Tiene registros asociados de alumnos, se preserva intacta para no alterar puntajes
                        preserved_count += 1
            print(f"   🗑️ Preguntas huérfanas eliminadas de forma segura: {deleted_count}")
            print(f"   🔒 Preguntas huérfanas preservadas por tener progreso/intentos de alumnos: {preserved_count}")

        # 4. Insertar o actualizar preguntas locales en la VPS
        print("[*] Sincronizando preguntas locales hacia la VPS...")
        upserted_count = 0
        inserted_count = 0

        with prod_conn.cursor() as cur:
            for q_id, q in local_questions.items():
                # Serializar campos JSONB
                datos_numericos = json.dumps(q['datos_numericos']) if q['datos_numericos'] else None
                payload_tokenizado = json.dumps(q['payload_tokenizado']) if q['payload_tokenizado'] else None
                explicacion_paso_a_paso = json.dumps(q['explicacion_paso_a_paso']) if q['explicacion_paso_a_paso'] else None
                palabras_clave = json.dumps(q['palabras_clave']) if q['palabras_clave'] else None
                errores_previstos = json.dumps(q['errores_previstos']) if q['errores_previstos'] else None

                if q_id in prod_question_ids:
                    # UPDATE de pregunta existente
                    cur.execute("""
                        UPDATE preguntas
                        SET fase_id = %s, seccion = %s, sub_nivel = %s, estructura_padre_id = %s, 
                            operacion = %s, tipo_pregunta = %s, enunciado = %s, respuesta_correcta = %s, 
                            datos_numericos = %s, payload_tokenizado = %s, explicacion_paso_a_paso = %s, 
                            requiere_subrayado = %s, palabras_clave = %s, errores_previstos = %s, 
                            creado_por = %s, modificado_por = %s, estado = %s, revisado_admin = %s, 
                            revisado_por = %s, fecha_revision = %s, ultima_modificacion = NOW()
                        WHERE id = %s;
                    """, (
                        q['fase_id'], q['seccion'], q['sub_nivel'], q['estructura_padre_id'],
                        q['operacion'], q['tipo_pregunta'], q['enunciado'], q['respuesta_correcta'],
                        datos_numericos, payload_tokenizado, explicacion_paso_a_paso,
                        q['requiere_subrayado'], palabras_clave, errores_previstos,
                        q['creado_por'], q['modificado_por'], q['estado'], q['revisado_admin'],
                        q['revisado_por'], q['fecha_revision'], q_id
                    ))
                    upserted_count += 1
                else:
                    # INSERT de nueva pregunta
                    cur.execute("""
                        INSERT INTO preguntas (
                            id, fase_id, seccion, sub_nivel, estructura_padre_id, operacion, tipo_pregunta,
                            enunciado, respuesta_correcta, datos_numericos, payload_tokenizado, 
                            explicacion_paso_a_paso, requiere_subrayado, palabras_clave, errores_previstos,
                            creado_por, modificado_por, estado, revisado_admin, revisado_por, fecha_revision,
                            fecha_creacion, ultima_modificacion
                        ) VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW()
                        );
                    """, (
                        q_id, q['fase_id'], q['seccion'], q['sub_nivel'], q['estructura_padre_id'],
                        q['operacion'], q['tipo_pregunta'], q['enunciado'], q['respuesta_correcta'],
                        datos_numericos, payload_tokenizado, explicacion_paso_a_paso,
                        q['requiere_subrayado'], palabras_clave, errores_previstos,
                        q['creado_por'], q['modificado_por'], q['estado'], q['revisado_admin'],
                        q['revisado_por'], q['fecha_revision']
                    ))
                    inserted_count += 1

                # Borrar alternativas previas de esta pregunta en la VPS e insertar las vigentes locales
                cur.execute("DELETE FROM alternativas WHERE pregunta_id = %s;", (q_id,))
                
                alts = local_alternatives.get(q_id, [])
                for alt in alts:
                    cur.execute("""
                        INSERT INTO alternativas (pregunta_id, texto, es_correcta, orden, tipo_error, feedback_error, fecha_creacion, ultima_modificacion)
                        VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW());
                    """, (q_id, alt['texto'], alt['es_correcta'], alt['orden'], alt['tipo_error'], alt['feedback_error']))

            # Confirmar transacción
            prod_conn.commit()
            print(f"   🔄 Preguntas actualizadas en la VPS: {upserted_count}")
            print(f"   ✨ Nuevas preguntas insertadas en la VPS: {inserted_count}")

    except Exception as e:
        prod_conn.rollback()
        print(f"❌ Ocurrió un error durante la transacción de la Base de Datos. Se realizó Rollback: {e}")
    finally:
        local_conn.close()
        prod_conn.close()
        print("✅ Conexiones a las bases de datos cerradas de forma segura.")

# =====================================================================
# EJECUCIÓN PRINCIPAL
# =====================================================================
def main():
    # Rutas absolutas a los archivos .env
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    local_env_path = os.path.join(base_dir, "Datos_localhost", ".env.local")
    prod_env_path = os.path.join(base_dir, "Datos_Producion", ".env")

    print("[*] Cargando archivos de configuración .env...")
    try:
        local_env = load_env_file(local_env_path)
        prod_env = load_env_file(prod_env_path)
        print("✅ Configuraciones cargadas correctamente.")
    except Exception as e:
        print(f"❌ Error al cargar los archivos .env: {e}")
        sys.exit(1)

    # 1. Ejecutar sincronización de imágenes en MinIO (asíncrono)
    asyncio.run(sync_minio_images(local_env, prod_env))

    # 2. Ejecutar sincronización de Base de Datos
    local_db_url = rewrite_db_url(local_env.get("DATABASE_URL"), override_host="localhost", override_port=5433)
    prod_db_url = rewrite_db_url(prod_env.get("DATABASE_URL"), override_host="localhost", override_port=5435)
    
    sync_database(local_db_url, prod_db_url)

    print("\n" + "="*80)
    print("PROCESO DE SINCRONIZACIÓN A PRODUCCIÓN FINALIZADO EXITOSAMENTE")
    print("="*80)

if __name__ == "__main__":
    main()
