#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sincronización segura de preguntas (+ MinIO graphics/) local → VPS.

Alineado con RULES AGENTES/bd_minio.md:
  - Política por defecto: insert-new (no sobrescribe existentes)
  - upsert opcional (no reescribe alternativas si hay intentos)
  - Reescritura de datos_numericos.url al dominio/bucket destino
  - FK a users inexistentes → NULL
  - Huérfanas: solo dentro del alcance; preserva si hay progreso
  - --dry-run (pre-vuelo) sin escrituras
  - --no-minio / auto-skip para Fases 5–6 (SVG inline)
  - Confirmación humana requerida salvo --yes (y nunca en dry-run)

Ejemplos:
  # Pre-vuelo solo Fase 5 hacia dev (sin MinIO)
  python scripts/sync_db_and_minio_prod.py --env dev --fase 5 --dry-run

  # Insertar solo nuevas en prod (requiere confirmación)
  python scripts/sync_db_and_minio_prod.py --env prod --policy insert-new

  # Upsert de una sección con confirmación explícita
  python scripts/sync_db_and_minio_prod.py --env dev --policy upsert --fase 3 --seccion 1 --yes
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from typing import Any, Optional

# Asegura import de sync_helpers al ejecutar como script
_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

import boto3
import psycopg2
from botocore.config import Config

from sync_helpers import (
    DEFAULT_TUNNEL_PORTS,
    SVG_INLINE_FASES,
    build_scope_where,
    load_env_file,
    null_missing_user_fks,
    parse_id_list,
    repo_root_from_scripts,
    resolve_env_path,
    rewrite_datos_numericos_url,
    rewrite_db_url,
    serialize_jsonb,
    should_skip_minio,
)

# ---------------------------------------------------------------------------
# MinIO (solo prefijo graphics/)
# ---------------------------------------------------------------------------

async def sync_minio_images(
    local_env: dict,
    remote_env: dict,
    *,
    dry_run: bool = False,
) -> dict[str, int]:
    """Sube objetos graphics/ faltantes local → remoto. No borra nada."""
    print("\n" + "=" * 80)
    print("[+] SINCRONIZACIÓN DE IMÁGENES (MinIO graphics/)")
    print("=" * 80)

    local_access = local_env.get("S3_ACCESS_KEY")
    local_secret = local_env.get("S3_SECRET_KEY")
    local_bucket = local_env.get("S3_BUCKET_NAME")
    if not all([local_access, local_secret, local_bucket]):
        raise RuntimeError("Faltan S3_ACCESS_KEY / S3_SECRET_KEY / S3_BUCKET_NAME en entorno local.")

    in_docker = os.path.exists("/.dockerenv") or "DATABASE_URL" in os.environ
    if not in_docker:
        local_endpoint = local_env.get("S3_PUBLIC_URL") or "http://localhost:9100"
    else:
        local_endpoint = (
            local_env.get("S3_ENDPOINT_URL")
            or local_env.get("S3_ENDPOINT")
            or "http://localhost:9100"
        )

    remote_access = remote_env.get("S3_ACCESS_KEY")
    remote_secret = remote_env.get("S3_SECRET_KEY")
    remote_bucket = remote_env.get("S3_BUCKET_NAME")
    remote_endpoint = (
        remote_env.get("S3_ENDPOINT_URL")
        or remote_env.get("S3_ENDPOINT")
        or remote_env.get("S3_PUBLIC_URL")
    )
    if not all([remote_access, remote_secret, remote_bucket, remote_endpoint]):
        raise RuntimeError(
            "Faltan credenciales MinIO remotas (S3_ACCESS_KEY, S3_SECRET_KEY, "
            "S3_BUCKET_NAME, S3_ENDPOINT o S3_PUBLIC_URL). No se usan fallbacks hardcodeados."
        )

    print(f"[*] Origen:  {local_endpoint} / {local_bucket}")
    print(f"[*] Destino: {remote_endpoint} / {remote_bucket}")

    local_s3 = boto3.client(
        "s3",
        endpoint_url=local_endpoint,
        aws_access_key_id=local_access,
        aws_secret_access_key=local_secret,
        config=Config(s3={"addressing_style": "path"}),
    )
    remote_s3 = boto3.client(
        "s3",
        endpoint_url=remote_endpoint,
        aws_access_key_id=remote_access,
        aws_secret_access_key=remote_secret,
        config=Config(s3={"addressing_style": "path"}, signature_version="s3v4"),
    )

    paginator = local_s3.get_paginator("list_objects_v2")
    local_keys: list[str] = []
    for page in paginator.paginate(Bucket=local_bucket, Prefix="graphics/"):
        for obj in page.get("Contents") or []:
            local_keys.append(obj["Key"])

    remote_keys: set[str] = set()
    try:
        for page in remote_s3.get_paginator("list_objects_v2").paginate(
            Bucket=remote_bucket, Prefix="graphics/"
        ):
            for obj in page.get("Contents") or []:
                remote_keys.add(obj["Key"])
    except Exception as e:
        print(f"[!] No se pudo listar remoto (se subirán todos): {e}")

    to_upload = [k for k in local_keys if k not in remote_keys]
    print(f"[*] Local graphics/: {len(local_keys)} | Remoto: {len(remote_keys)} | A subir: {len(to_upload)}")

    if dry_run:
        print("[dry-run] No se sube ningún objeto.")
        return {"local": len(local_keys), "remote": len(remote_keys), "would_upload": len(to_upload), "uploaded": 0}

    if not to_upload:
        print("✅ Nada que subir.")
        return {"local": len(local_keys), "remote": len(remote_keys), "would_upload": 0, "uploaded": 0}

    sem = asyncio.Semaphore(5)
    success = 0
    fail = 0

    async def _one(key: str) -> None:
        nonlocal success, fail
        async with sem:
            try:
                obj = await asyncio.to_thread(local_s3.get_object, Bucket=local_bucket, Key=key)
                body = obj["Body"].read()
                ctype = obj.get("ContentType", "image/png")
                await asyncio.to_thread(
                    remote_s3.put_object,
                    Bucket=remote_bucket,
                    Key=key,
                    Body=body,
                    ContentType=ctype,
                )
                success += 1
            except Exception as ex:
                print(f"   [!] Error '{key}': {ex}")
                fail += 1

    tasks = [_one(k) for k in to_upload]
    for i in range(0, len(tasks), 100):
        await asyncio.gather(*tasks[i : i + 100])
        print(f"   Progreso: {min(i + 100, len(tasks))}/{len(tasks)}")

    print(f"✅ MinIO: subidos={success} fallidos={fail}")
    return {
        "local": len(local_keys),
        "remote": len(remote_keys),
        "would_upload": len(to_upload),
        "uploaded": success,
        "failed": fail,
    }


# ---------------------------------------------------------------------------
# Base de datos
# ---------------------------------------------------------------------------

QUESTION_SELECT = """
    SELECT id, fase_id, seccion, sub_nivel, estructura_padre_id, operacion, tipo_pregunta,
           enunciado, respuesta_correcta, datos_numericos, payload_tokenizado,
           explicacion_paso_a_paso, requiere_subrayado, palabras_clave, errores_previstos,
           creado_por, modificado_por, estado, revisado_admin, revisado_por, fecha_revision
    FROM preguntas
    {where}
"""


def _fetch_questions(conn, where_sql: str, params: list[Any]) -> dict[int, dict]:
    with conn.cursor() as cur:
        cur.execute(QUESTION_SELECT.format(where=where_sql), params)
        cols = [d[0] for d in cur.description]
        return {row[0]: dict(zip(cols, row)) for row in cur.fetchall()}


def _fetch_alternatives(conn, question_ids: set[int]) -> dict[int, list[dict]]:
    if not question_ids:
        return {}
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, pregunta_id, texto, es_correcta, orden, tipo_error, feedback_error
            FROM alternativas
            WHERE pregunta_id = ANY(%s)
            """,
            (list(question_ids),),
        )
        out: dict[int, list[dict]] = {}
        for row in cur.fetchall():
            alt = {
                "id": row[0],
                "pregunta_id": row[1],
                "texto": row[2],
                "es_correcta": row[3],
                "orden": row[4],
                "tipo_error": row[5],
                "feedback_error": row[6],
            }
            out.setdefault(alt["pregunta_id"], []).append(alt)
        return out


def _existing_user_ids(conn) -> set[int]:
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM users")
        return {row[0] for row in cur.fetchall()}


def _question_has_progress(cur, q_id: int) -> bool:
    cur.execute(
        """
        SELECT EXISTS (
            SELECT 1 FROM pool_asignado_alumno WHERE pregunta_id = %s
            UNION ALL SELECT 1 FROM intentos WHERE pregunta_id = %s
            UNION ALL SELECT 1 FROM intento_preguntas WHERE pregunta_id = %s
        )
        """,
        (q_id, q_id, q_id),
    )
    return bool(cur.fetchone()[0])


def _question_has_intentos(cur, q_id: int) -> bool:
    cur.execute("SELECT EXISTS (SELECT 1 FROM intentos WHERE pregunta_id = %s)", (q_id,))
    return bool(cur.fetchone()[0])


def sync_database(
    local_db_url: str,
    remote_db_url: str,
    *,
    policy: str = "insert-new",
    dry_run: bool = False,
    fase_id: Optional[int] = None,
    seccion: Optional[int] = None,
    operacion: Optional[str] = None,
    ids: Optional[list[int]] = None,
    public_url: str = "",
    remote_bucket: str = "",
    skip_orphan_delete: bool = False,
) -> dict[str, Any]:
    """
    Sincroniza preguntas + alternativas según política.
    policy: insert-new | upsert
    """
    if policy not in ("insert-new", "upsert"):
        raise ValueError("policy debe ser 'insert-new' o 'upsert'")

    print("\n" + "=" * 80)
    print(f"[+] DB SYNC policy={policy} dry_run={dry_run}")
    print("=" * 80)

    where_sql, where_params = build_scope_where(
        fase_id=fase_id, seccion=seccion, operacion=operacion, ids=ids
    )
    scope_desc = where_sql or "(TOTAL)"
    print(f"[*] Alcance: {scope_desc} params={where_params}")

    local_conn = psycopg2.connect(local_db_url)
    remote_conn = psycopg2.connect(remote_db_url)

    report: dict[str, Any] = {
        "policy": policy,
        "dry_run": dry_run,
        "to_insert": 0,
        "to_update": 0,
        "to_skip_existing": 0,
        "orphans_delete": 0,
        "orphans_preserve": 0,
        "alts_rewritten": 0,
        "alts_preserved": 0,
    }

    try:
        local_questions = _fetch_questions(local_conn, where_sql, where_params)
        local_alts = _fetch_alternatives(local_conn, set(local_questions.keys()))
        remote_questions = _fetch_questions(remote_conn, where_sql, where_params)
        remote_ids = set(remote_questions.keys())
        local_ids = set(local_questions.keys())

        print(f"   Local (alcance): {len(local_ids)} | Remoto (alcance): {len(remote_ids)}")

        user_ids = _existing_user_ids(remote_conn)

        to_insert_ids = local_ids - remote_ids
        common_ids = local_ids & remote_ids
        orphan_ids = remote_ids - local_ids

        report["to_insert"] = len(to_insert_ids)
        if policy == "insert-new":
            report["to_skip_existing"] = len(common_ids)
            report["to_update"] = 0
            update_ids: set[int] = set()
        else:
            report["to_update"] = len(common_ids)
            report["to_skip_existing"] = 0
            update_ids = set(common_ids)

        # Pre-vuelo huérfanas (optimizado masivo)
        deletable: list[int] = []
        preservable: list[int] = []
        if orphan_ids and not skip_orphan_delete:
            with remote_conn.cursor() as cur:
                orphan_list = list(orphan_ids)
                cur.execute(
                    """
                    SELECT DISTINCT pregunta_id FROM pool_asignado_alumno WHERE pregunta_id = ANY(%s)
                    UNION
                    SELECT DISTINCT pregunta_id FROM intentos WHERE pregunta_id = ANY(%s)
                    UNION
                    SELECT DISTINCT pregunta_id FROM intento_preguntas WHERE pregunta_id = ANY(%s)
                    """,
                    (orphan_list, orphan_list, orphan_list),
                )
                ids_con_progreso = {row[0] for row in cur.fetchall()}
                for q_id in orphan_ids:
                    if q_id in ids_con_progreso:
                        preservable.append(q_id)
                    else:
                        deletable.append(q_id)
        elif orphan_ids and skip_orphan_delete:
            preservable = list(orphan_ids)

        report["orphans_delete"] = len(deletable)
        report["orphans_preserve"] = len(preservable)

        print("\n--- PRE-VUELO ---")
        print(f"  Insertar (nuevas):     {report['to_insert']}")
        print(f"  Actualizar (upsert):   {report['to_update']}")
        print(f"  Dejar intactas:        {report['to_skip_existing']}")
        print(f"  Huérfanas a borrar:    {report['orphans_delete']}")
        print(f"  Huérfanas preservadas: {report['orphans_preserve']}")

        if dry_run:
            print("[dry-run] Sin escrituras en DB.")
            return report

        with remote_conn.cursor() as cur:
            # A) Borrar huérfanas seguras (optimizado masivo)
            if deletable:
                print(f"[*] Borrando {len(deletable)} preguntas huérfanas y sus alternativas en la VPS...")
                cur.execute("DELETE FROM alternativas WHERE pregunta_id = ANY(%s)", (deletable,))
                cur.execute("DELETE FROM preguntas WHERE id = ANY(%s)", (deletable,))

            # B) Insert / update en lotes para no saturar la conexión SSH
            work_ids = list(to_insert_ids | update_ids)
            total_work = len(work_ids)
            batch_size = 500
            print(f"[*] Iniciando sincronización de {total_work} preguntas en lotes de {batch_size}...")

            for i in range(0, total_work, batch_size):
                batch_chunk = work_ids[i : i + batch_size]
                for q_id in batch_chunk:
                    q = local_questions[q_id]
                    datos = q["datos_numericos"]
                    if public_url and remote_bucket:
                        datos = rewrite_datos_numericos_url(datos, public_url, remote_bucket)

                    creado, modificado, revisado = null_missing_user_fks(
                        q["creado_por"], q["modificado_por"], q["revisado_por"], user_ids
                    )

                    row_vals = (
                        q["fase_id"],
                        q["seccion"],
                        q["sub_nivel"],
                        q["estructura_padre_id"],
                        q["operacion"],
                        q["tipo_pregunta"],
                        q["enunciado"],
                        q["respuesta_correcta"],
                        serialize_jsonb(datos),
                        serialize_jsonb(q["payload_tokenizado"]),
                        serialize_jsonb(q["explicacion_paso_a_paso"]),
                        q["requiere_subrayado"],
                        serialize_jsonb(q["palabras_clave"]),
                        serialize_jsonb(q["errores_previstos"]),
                        creado,
                        modificado,
                        q["estado"],
                        q["revisado_admin"],
                        revisado,
                        q["fecha_revision"],
                    )

                    if q_id in to_insert_ids:
                        cur.execute(
                            """
                            INSERT INTO preguntas (
                                id, fase_id, seccion, sub_nivel, estructura_padre_id, operacion, tipo_pregunta,
                                enunciado, respuesta_correcta, datos_numericos, payload_tokenizado,
                                explicacion_paso_a_paso, requiere_subrayado, palabras_clave, errores_previstos,
                                creado_por, modificado_por, estado, revisado_admin, revisado_por, fecha_revision,
                                fecha_creacion, ultima_modificacion
                            ) VALUES (
                                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                NOW(), NOW()
                            )
                            """,
                            (q_id, *row_vals),
                        )
                        for alt in local_alts.get(q_id, []):
                            cur.execute(
                                """
                                INSERT INTO alternativas (
                                    pregunta_id, texto, es_correcta, orden, tipo_error, feedback_error,
                                    fecha_creacion, ultima_modificacion
                                ) VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
                                """,
                                (
                                    q_id,
                                    alt["texto"],
                                    alt["es_correcta"],
                                    alt["orden"],
                                    alt["tipo_error"],
                                    alt["feedback_error"],
                                ),
                            )
                        report["alts_rewritten"] += len(local_alts.get(q_id, []))
                    else:
                        cur.execute(
                            """
                            UPDATE preguntas SET
                                fase_id = %s, seccion = %s, sub_nivel = %s, estructura_padre_id = %s,
                                operacion = %s, tipo_pregunta = %s, enunciado = %s, respuesta_correcta = %s,
                                datos_numericos = %s, payload_tokenizado = %s, explicacion_paso_a_paso = %s,
                                requiere_subrayado = %s, palabras_clave = %s, errores_previstos = %s,
                                creado_por = %s, modificado_por = %s, estado = %s, revisado_admin = %s,
                                revisado_por = %s, fecha_revision = %s, ultima_modificacion = NOW()
                            WHERE id = %s
                            """,
                            (*row_vals, q_id),
                        )
                        if _question_has_intentos(cur, q_id):
                            report["alts_preserved"] += 1
                        else:
                            cur.execute("DELETE FROM alternativas WHERE pregunta_id = %s", (q_id,))
                            for alt in local_alts.get(q_id, []):
                                cur.execute(
                                    """
                                    INSERT INTO alternativas (
                                        pregunta_id, texto, es_correcta, orden, tipo_error, feedback_error,
                                        fecha_creacion, ultima_modificacion
                                    ) VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
                                    """,
                                    (
                                        q_id,
                                        alt["texto"],
                                        alt["es_correcta"],
                                        alt["orden"],
                                        alt["tipo_error"],
                                        alt["feedback_error"],
                                    ),
                                )
                            report["alts_rewritten"] += 1

                remote_conn.commit()
                print(f"   Progreso DB: {min(i + batch_size, total_work)}/{total_work} preguntas sincronizadas")

            print("✅ Sincronización DB completada con éxito.")
            print(f"   Insertadas: {report['to_insert']} | Actualizadas: {report['to_update']}")
            print(f"   Huérfanas borradas: {report['orphans_delete']} | Preservadas: {report['orphans_preserve']}")
            print(f"   Alts reescritas (preguntas): {report['alts_rewritten']} | Alts preservadas: {report['alts_preserved']}")

    except Exception as e:
        remote_conn.rollback()
        print(f"❌ Error DB — rollback: {e}")
        raise
    finally:
        local_conn.close()
        remote_conn.close()

    return report


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Sync seguro de preguntas (+ MinIO graphics/) local → VPS (bd_minio.md)."
    )
    p.add_argument("--env", choices=["dev", "prod"], required=True, help="Destino VPS")
    p.add_argument(
        "--policy",
        choices=["insert-new", "upsert"],
        default="insert-new",
        help="insert-new (default, seguro) | upsert",
    )
    p.add_argument("--dry-run", action="store_true", help="Pre-vuelo: solo compara, no escribe")
    p.add_argument("--yes", action="store_true", help="Confirma escrituras sin prompt interactivo")
    p.add_argument("--fase", type=int, default=None, help="Filtrar por fase_id")
    p.add_argument("--seccion", type=int, default=None, help="Filtrar por seccion")
    p.add_argument("--operacion", type=str, default=None, help="Filtrar por operacion")
    p.add_argument("--ids", type=str, default=None, help="IDs separados por coma")
    p.add_argument(
        "--no-minio",
        action="store_true",
        help="No sincronizar MinIO (obligatorio de facto para Fases 5–6 SVG)",
    )
    p.add_argument(
        "--skip-orphan-delete",
        action="store_true",
        help="No borrar huérfanas en el destino (solo insert/update)",
    )
    p.add_argument(
        "--local-port",
        type=int,
        default=None,
        help=f"Puerto túnel/local DB (default {DEFAULT_TUNNEL_PORTS['local']})",
    )
    p.add_argument(
        "--remote-port",
        type=int,
        default=None,
        help="Puerto túnel remoto (default 5434 dev / 5435 prod)",
    )
    p.add_argument("--local-env", type=str, default=None, help="Ruta alternativa al .env local")
    p.add_argument("--remote-env", type=str, default=None, help="Ruta alternativa al .env remoto")
    p.add_argument(
        "--db-only",
        action="store_true",
        help="Solo DB (implica no MinIO)",
    )
    p.add_argument(
        "--minio-only",
        action="store_true",
        help="Solo MinIO graphics/ (sin tocar DB)",
    )
    return p


def main(argv: Optional[list[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    root = repo_root_from_scripts()

    try:
        local_env_path = args.local_env or resolve_env_path("local", root)
        remote_env_path = args.remote_env or resolve_env_path(args.env, root)
        local_env = load_env_file(local_env_path)
        remote_env = load_env_file(remote_env_path)
    except Exception as e:
        print(f"❌ Config: {e}")
        return 1

    local_port = args.local_port or DEFAULT_TUNNEL_PORTS["local"]
    remote_port = args.remote_port or DEFAULT_TUNNEL_PORTS[args.env]

    local_db = rewrite_db_url(
        local_env.get("DATABASE_URL", ""), override_host="localhost", override_port=local_port
    )
    remote_db = rewrite_db_url(
        remote_env.get("DATABASE_URL", ""), override_host="localhost", override_port=remote_port
    )
    if not local_env.get("DATABASE_URL") or not remote_env.get("DATABASE_URL"):
        print("❌ Falta DATABASE_URL en local o remoto.")
        return 1

    ids = parse_id_list(args.ids)
    public_url = (
        remote_env.get("S3_PUBLIC_URL")
        or remote_env.get("S3_ENDPOINT_URL")
        or remote_env.get("S3_ENDPOINT")
        or ""
    ).rstrip("/")
    remote_bucket = remote_env.get("S3_BUCKET_NAME", "")

    # Decidir MinIO
    fase_scope: list[int] = []
    if args.fase is not None:
        fase_scope = [args.fase]
    skip_minio = (
        args.db_only
        or should_skip_minio(args.no_minio, fase_scope)
    )
    if args.fase in SVG_INLINE_FASES and not args.no_minio and not args.db_only:
        print(
            f"[*] Fase {args.fase} es SVG-inline (bd_minio §1.3): se omite MinIO automáticamente. "
            "Use sin --fase o force con sync_minio_vps si hubiera graphics/ excepcionales."
        )
        skip_minio = True

    print("=" * 80)
    print("SYNC local → VPS  (skill: RULES AGENTES/bd_minio.md)")
    print(f"  destino={args.env} policy={args.policy} dry_run={args.dry_run}")
    if args.minio_only:
        print("  modo=minio-only")
    elif skip_minio:
        print("  minio=OFF")
    else:
        print("  minio=ON (solo graphics/ faltantes)")
    print(f"  DB ports local={local_port} remote={remote_port}")
    print("=" * 80)

    if not args.dry_run and not args.yes:
        print(
            "\n⚠️  Escritura en destino requiere confirmación.\n"
            "    Re-ejecute con --dry-run primero, luego con --yes para aplicar.\n"
            "    (bd_minio.md: pre-vuelo + confirmación humana)"
        )
        return 2

    # MinIO
    if not skip_minio and not args.db_only:
        try:
            asyncio.run(sync_minio_images(local_env, remote_env, dry_run=args.dry_run))
        except Exception as e:
            print(f"❌ MinIO: {e}")
            if args.minio_only:
                return 1
            print("[!] Continuando con DB (MinIO falló). Revise credenciales/endpoint.")

    if args.minio_only:
        print("\n✅ minio-only finalizado.")
        return 0

    # DB
    try:
        sync_database(
            local_db,
            remote_db,
            policy=args.policy,
            dry_run=args.dry_run,
            fase_id=args.fase,
            seccion=args.seccion,
            operacion=args.operacion,
            ids=ids,
            public_url=public_url,
            remote_bucket=remote_bucket,
            skip_orphan_delete=args.skip_orphan_delete,
        )
    except Exception as e:
        print(f"❌ Falló sync DB: {e}")
        return 1

    print("\n" + "=" * 80)
    print("PROCESO FINALIZADO" + (" (dry-run)" if args.dry_run else ""))
    print("=" * 80)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
