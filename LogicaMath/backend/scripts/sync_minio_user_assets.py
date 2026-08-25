#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI para respaldar / sincronizar recursos multimediales de usuarios desde VPS MinIO hacia Local MinIO.

Alineado con RULES AGENTES/bd_minio.md:
- Descarga los objetos pertenecientes a usuarios: avatares y capturas de pantalla de feedback UX (screenshots/).
- Ignores prefijos de preguntas (graphics/) ya que esos se gestionan por sync_minio_vps.py.
- Preserva la estructura física de buckets de MinIO de la VPS en el MinIO local.
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import List, Optional

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from sync_helpers import load_env_file, resolve_env_path


def get_s3_client(env_name: str):
    """Crea un cliente boto3 S3 configurado para el entorno indicado."""
    env_path = resolve_env_path(env_name)
    env_data = load_env_file(env_path)

    endpoint = env_data.get("S3_ENDPOINT")
    access_key = env_data.get("S3_ACCESS_KEY")
    secret_key = env_data.get("S3_SECRET_KEY")
    bucket = env_data.get("S3_BUCKET")

    if not endpoint or not access_key or not secret_key or not bucket:
        raise ValueError(f"Faltan variables S3_* en {env_path}")

    client = boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(signature_version="s3v4"),
        verify=False,
    )

    return client, bucket


def list_user_objects(s3_client, bucket_name: str) -> List[str]:
    """Lista los objetos de usuarios (avatares, screenshots) ignorando la carpeta graphics/."""
    user_keys = []
    paginator = s3_client.get_paginator("list_objects_v2")

    for page in paginator.paginate(Bucket=bucket_name):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            # Excluir figuras pedagógicas de preguntas
            if key.startswith("graphics/"):
                continue
            user_keys.append(key)

    return user_keys


def object_exists(s3_client, bucket_name: str, key: str) -> bool:
    """Verifica si un objeto existe en el bucket."""
    try:
        s3_client.head_object(Bucket=bucket_name, Key=key)
        return True
    except ClientError:
        return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sincronizar avatares y screenshots de usuarios desde VPS MinIO a Local MinIO."
    )
    parser.add_argument(
        "--env",
        choices=["prod", "dev"],
        default="prod",
        help="Entorno VPS origen (default: prod)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Modo pre-vuelo: lista los archivos a transferir sin escribir en Local",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Confirma la copia de objetos a MinIO local",
    )

    args = parser.parse_args()

    print("=================================================================")
    print("      RESPALDO DE RECURSOS MULTIMEDIA (MINIO): VPS -> LOCAL       ")
    print("=================================================================")
    print(f"  Origen VPS: {args.env.upper()}")
    print(f"  Modo: {'DRY-RUN' if args.dry-run else 'EJECUCIÓN REAL'}")

    if not args.dry-run and not args.yes:
        print("\n❌ [ERROR] Debe especificar '--yes' para copiar archivos realmente.")
        sys.exit(2)

    try:
        vps_s3, vps_bucket = get_s3_client(args.env)
        local_s3, local_bucket = get_s3_client("local")
        print("  ✅ Clientes MinIO VPS y Local configurados correctamente.")
    except Exception as e:
        print(f"\n❌ [ERROR] No se pudo conectar a los servicios MinIO: {e}")
        sys.exit(1)

    print("\n[1/2] Listando recursos multimediales de usuarios en VPS...")
    vps_user_keys = list_user_objects(vps_s3, vps_bucket)
    print(f"  Encontrados {len(vps_user_keys)} archivos multimediales de usuarios (avatares/screenshots).")

    missing_local_keys = []
    for key in vps_user_keys:
        if not object_exists(local_s3, local_bucket, key):
            missing_local_keys.append(key)

    print(f"  -> {len(missing_local_keys)} archivos faltan en MinIO Local.")

    if args.dry-run:
        print("\n=================================================================")
        print("  PRE-VUELO MINIO COMPLETADO (0 transferencias realizadas).")
        print("=================================================================")
        sys.exit(0)

    print("\n[2/2] Transfiriendo objetos faltantes de MinIO VPS -> Local...")
    transferred = 0
    for key in missing_local_keys:
        try:
            print(f"  -> Transfiriendo '{key}'...")
            obj = vps_s3.get_object(Bucket=vps_bucket, Key=key)
            body = obj["Body"].read()
            content_type = obj.get("ContentType", "application/octet-stream")

            local_s3.put_object(
                Bucket=local_bucket,
                Key=key,
                Body=body,
                ContentType=content_type,
            )
            transferred += 1
        except Exception as e:
            print(f"  ⚠️ Error al transferir '{key}': {e}")

    print(f"\n  ✅ Respaldo MinIO finalizado. {transferred} objetos transferidos exitosamente.")


if __name__ == "__main__":
    main()
