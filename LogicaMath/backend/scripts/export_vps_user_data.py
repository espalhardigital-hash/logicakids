#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI para migrar datos de usuarios, puntajes y niveles aprobados desde una VPS hacia Local.

Alineado con el plan de migración por desactivación de VPS:
- Entornos VPS soportados: prod (puerto túnel 5435 por defecto) o dev (puerto túnel 5434).
- Base Local: puerto DB 5433 por defecto (o .env.local).
- Tablas migradas (VPS -> Local):
  1. users (Usuarios y admins)
  2. alumnos (Perfiles pedagógicos)
  3. progreso_maestria (Niveles Aprobados y progreso por bloque)
  4. pool_asignado_alumno (Preguntas asignadas)
  5. intentos (Puntajes y respuestas analíticas)
  6. intento_preguntas & intento_pasos (Fase 2 multi-paso)
  7. simulado_sessions (Sesiones de simulacros)
  8. ux_feedbacks (Feedbacks reportados)
- Pre-vuelo (--dry-run) que reporta totales sin escribir.
- Garantía de integridad de FK (inserta o alerta si faltan preguntas referenciadas).
- Reseteo automático de secuencias PostgreSQL (setval) tras la importación.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

# Asegurar import de sync_helpers desde el mismo directorio
_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, _SCRIPTS_DIR)

import psycopg2
from psycopg2.extras import RealDictCursor

from sync_helpers import (
    DEFAULT_TUNNEL_PORTS,
    load_env_file,
    resolve_env_path,
    rewrite_db_url,
)

# Lista ordenada por jerarquía de claves foráneas
TARGET_TABLES = [
    "users",
    "alumnos",
    "progreso_maestria",
    "pool_asignado_alumno",
    "intentos",
    "intento_preguntas",
    "intento_pasos",
    "simulado_sessions",
    "ux_feedbacks",
]

# Tablas con secuencia SERIAL en PostgreSQL que requieren setval()
SEQUENCE_TABLES = [
    "alumnos",
    "progreso_maestria",
    "pool_asignado_alumno",
    "intentos",
    "intento_preguntas",
    "intento_pasos",
    "ux_feedbacks",
]


def connect_db(env_name: str, port_override: Optional[int] = None) -> psycopg2.extensions.connection:
    """Crea una conexión psycopg2 a la base de datos indicada."""
    env_path = resolve_env_path(env_name)
    env_data = load_env_file(env_path)

    raw_url = env_data.get("DATABASE_URL")
    if not raw_url:
        raise ValueError(f"No se encontró DATABASE_URL en {env_path}")

    port = port_override or DEFAULT_TUNNEL_PORTS.get(env_name, 5433)
    db_url = rewrite_db_url(raw_url, override_host="localhost", override_port=port)

    conn = psycopg2.connect(db_url)
    return conn


def get_table_counts(conn: psycopg2.extensions.connection) -> Dict[str, int]:
    """Obtiene el conteo de filas de cada tabla objetivo."""
    counts = {}
    with conn.cursor() as cur:
        for table in TARGET_TABLES:
            try:
                cur.execute(f'SELECT COUNT(*) FROM "{table}";')
                counts[table] = cur.fetchone()[0]
            except Exception:
                conn.rollback()
                counts[table] = 0

        # Conteo específico de Niveles Aprobados
        try:
            cur.execute("SELECT COUNT(*) FROM progreso_maestria WHERE estado = 'APROBADO';")
            counts["niveles_aprobados"] = cur.fetchone()[0]
        except Exception:
            conn.rollback()
            counts["niveles_aprobados"] = 0

    return counts


def check_missing_question_fks(
    vps_conn: psycopg2.extensions.connection,
    local_conn: psycopg2.extensions.connection,
) -> Tuple[List[int], List[int]]:
    """
    Verifica si existen pregunta_ids o alternativa_ids en los intentos/pools de la VPS
    que no existan en la base de datos local.
    """
    vps_p_ids = set()
    with vps_conn.cursor() as cur:
        cur.execute("SELECT DISTINCT pregunta_id FROM intentos WHERE pregunta_id IS NOT NULL;")
        vps_p_ids.update(r[0] for r in cur.fetchall())
        cur.execute("SELECT DISTINCT pregunta_id FROM pool_asignado_alumno WHERE pregunta_id IS NOT NULL;")
        vps_p_ids.update(r[0] for r in cur.fetchall())

    local_p_ids = set()
    with local_conn.cursor() as cur:
        cur.execute("SELECT id FROM preguntas;")
        local_p_ids.update(r[0] for r in cur.fetchall())

    missing_p_ids = list(vps_p_ids - local_p_ids)

    # Verificar alternativas
    vps_a_ids = set()
    with vps_conn.cursor() as cur:
        cur.execute("SELECT DISTINCT alternativa_id FROM intentos WHERE alternativa_id IS NOT NULL;")
        vps_a_ids.update(r[0] for r in cur.fetchall())

    local_a_ids = set()
    with local_conn.cursor() as cur:
        cur.execute("SELECT id FROM alternativas;")
        local_a_ids.update(r[0] for r in cur.fetchall())

    missing_a_ids = list(vps_a_ids - local_a_ids)

    return missing_p_ids, missing_a_ids


def sync_missing_questions_and_alternatives(
    vps_conn: psycopg2.extensions.connection,
    local_conn: psycopg2.extensions.connection,
    missing_p_ids: List[int],
    missing_a_ids: List[int],
) -> None:
    """Copia preguntas y alternativas faltantes desde la VPS hacia Local para preservar integridad de FK."""
    if not missing_p_ids and not missing_a_ids:
        return

    with vps_conn.cursor(cursor_factory=RealDictCursor) as vps_cur, local_conn.cursor() as local_cur:
        if missing_p_ids:
            print(f"  -> Trayendo {len(missing_p_ids)} preguntas faltantes desde la VPS...")
            vps_cur.execute("SELECT * FROM preguntas WHERE id = ANY(%s);", (missing_p_ids,))
            p_rows = vps_cur.fetchall()
            if p_rows:
                cols = list(p_rows[0].keys())
                col_names = ", ".join(f'"{c}"' for c in cols)
                placeholders = ", ".join(["%s"] * len(cols))
                query = f'INSERT INTO "preguntas" ({col_names}) VALUES ({placeholders}) ON CONFLICT (id) DO NOTHING;'
                for row in p_rows:
                    vals = [json.dumps(v) if isinstance(v, (dict, list)) else v for v in row.values()]
                    local_cur.execute(query, vals)

        if missing_a_ids:
            print(f"  -> Trayendo {len(missing_a_ids)} alternativas faltantes desde la VPS...")
            vps_cur.execute("SELECT * FROM alternativas WHERE id = ANY(%s);", (missing_a_ids,))
            a_rows = vps_cur.fetchall()
            if a_rows:
                cols = list(a_rows[0].keys())
                col_names = ", ".join(f'"{c}"' for c in cols)
                placeholders = ", ".join(["%s"] * len(cols))
                query = f'INSERT INTO "alternativas" ({col_names}) VALUES ({placeholders}) ON CONFLICT (id) DO NOTHING;'
                for row in a_rows:
                    vals = [json.dumps(v) if isinstance(v, (dict, list)) else v for v in row.values()]
                    local_cur.execute(query, vals)


def export_table_data(
    vps_conn: psycopg2.extensions.connection,
    local_conn: psycopg2.extensions.connection,
    table_name: str,
) -> int:
    """Migra datos de una tabla específica desde VPS a Local usando UPSERT."""
    with vps_conn.cursor(cursor_factory=RealDictCursor) as vps_cur, local_conn.cursor() as local_cur:
        vps_cur.execute(f'SELECT * FROM "{table_name}";')
        rows = vps_cur.fetchall()

        if not rows:
            return 0

        cols = list(rows[0].keys())
        col_names = ", ".join(f'"{c}"' for c in cols)
        val_placeholders = ", ".join(["%s"] * len(cols))

        # Determinar clave de conflicto según tabla
        if table_name == "progreso_maestria":
            conflict_target = "(alumno_id, fase_id, seccion, operacion)"
        elif table_name == "pool_asignado_alumno":
            conflict_target = "(alumno_id, pregunta_id)"
        elif table_name == "users" and "id" in cols:
            conflict_target = "(id)"
        elif "id" in cols:
            conflict_target = "(id)"
        else:
            conflict_target = None

        if conflict_target:
            update_cols = [f'"{c}" = EXCLUDED."{c}"' for c in cols if c != "id" and c != "fecha_creacion"]
            if update_cols:
                update_stmt = ", ".join(update_cols)
                on_conflict = f"ON CONFLICT {conflict_target} DO UPDATE SET {update_stmt}"
            else:
                on_conflict = f"ON CONFLICT {conflict_target} DO NOTHING"
        else:
            on_conflict = "ON CONFLICT DO NOTHING"

        query = f'INSERT INTO "{table_name}" ({col_names}) VALUES ({val_placeholders}) {on_conflict};'

        inserted_count = 0
        for row in rows:
            vals = []
            for col in cols:
                v = row[col]
                if isinstance(v, (dict, list)):
                    vals.append(json.dumps(v))
                else:
                    vals.append(v)
            local_cur.execute(query, vals)
            inserted_count += 1

        return inserted_count


def reset_local_sequences(local_conn: psycopg2.extensions.connection) -> None:
    """Resetea las secuencias PostgreSQL (setval) en la base local tras la importación."""
    with local_conn.cursor() as cur:
        for table in SEQUENCE_TABLES:
            try:
                sql = f"""
                SELECT setval(
                    pg_get_serial_sequence('{table}', 'id'),
                    COALESCE((SELECT MAX(id) FROM "{table}"), 1)
                );
                """
                cur.execute(sql)
            except Exception as e:
                local_conn.rollback()
                print(f"  [Aviso] No se pudo resetear secuencia para {table}: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Migrar usuarios, puntajes y niveles aprobados desde la VPS a Local."
    )
    parser.add_argument(
        "--env",
        choices=["prod", "dev"],
        default="prod",
        help="Entorno VPS de origen (default: prod)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Modo pre-vuelo: compara registros sin escribir en Local",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Confirma la escritura en la base local (requerido si no es dry-run)",
    )
    parser.add_argument(
        "--source-port",
        type=int,
        help="Puerto túnel para la VPS (default: 5435 para prod, 5434 para dev)",
    )
    parser.add_argument(
        "--target-port",
        type=int,
        default=5433,
        help="Puerto PostgreSQL local (default: 5433)",
    )

    args = parser.parse_args()

    print("=================================================================")
    print("      MIGRACIÓN DE DATOS DE USUARIO: VPS -> BASE LOCAL          ")
    print("=================================================================")
    print(f"  Entorno Origen: VPS {args.env.upper()}")
    print(f"  Modo: {'DRY-RUN (Pre-vuelo sin escrituras)' if args.dry-run else 'EJECUCIÓN DE IMPORTACIÓN'}")

    if not args.dry-run and not args.yes:
        print("\n❌ [ERROR] Para ejecutar la migración real debe incluir la bandera '--yes'.")
        print("  Ejemplo pre-vuelo: python export_vps_user_data.py --env prod --dry-run")
        print("  Ejemplo migración: python export_vps_user_data.py --env prod --yes")
        sys.exit(2)

    source_port = args.source_port or DEFAULT_TUNNEL_PORTS.get(args.env, 5435)
    try:
        print(f"\n[1/4] Conectando a VPS {args.env.upper()} (localhost:{source_port}) y Local (localhost:{args.target_port})...")

        vps_conn = connect_db(args.env, port_override=source_port)
        local_conn = connect_db("local", port_override=args.target_port)

        print("  ✅ Conexiones a ambas bases de datos establecidas correctamente.")
    except Exception as e:
        print(f"\n❌ [ERROR DE CONEXIÓN] {e}")
        print("  Verifique que el túnel SSH esté activo. Ejemplo:")
        print(f"  ssh -L {source_port}:localhost:5432 rominejo@34.9.51.225 -N")
        sys.exit(1)

    print("\n[2/4] Auditoría Pre-vuelo de Totales (VPS vs Local)...")
    vps_counts = get_table_counts(vps_conn)
    local_counts = get_table_counts(local_conn)

    print("\n  Tabla                  | Filas VPS | Filas Local")
    print("  -----------------------+-----------+------------")
    for t in TARGET_TABLES:
        print(f"  {t:<22} | {vps_counts.get(t, 0):<9} | {local_counts.get(t, 0):<10}")
    print("  -----------------------+-----------+------------")
    print(f"  ⭐ Niveles Aprobados    | {vps_counts.get('niveles_aprobados', 0):<9} | {local_counts.get('niveles_aprobados', 0):<10}")

    print("\n[3/4] Verificando Claves Foráneas de Preguntas e Intentos...")
    missing_p_ids, missing_a_ids = check_missing_question_fks(vps_conn, local_conn)

    if missing_p_ids or missing_a_ids:
        print(f"  ⚠️  Faltan {len(missing_p_ids)} preguntas y {len(missing_a_ids)} alternativas en local.")
        if not args.dry-run:
            sync_missing_questions_and_alternatives(vps_conn, local_conn, missing_p_ids, missing_a_ids)
            local_conn.commit()
    else:
        print("  ✅ Todas las preguntas y alternativas referenciadas por los usuarios existen en Local.")

    if args.dry-run:
        print("\n=================================================================")
        print("  PRE-VUELO COMPLETADO (Cero escrituras en DB local).")
        print("  Para aplicar la migración real ejecuta:")
        print(f"  python {sys.argv[0]} --env {args.env} --yes")
        print("=================================================================")
        vps_conn.close()
        local_conn.close()
        sys.exit(0)

    print("\n[4/4] Ejecutando Importación Transaccional de Tablas (VPS -> Local)...")
    try:
        total_migrated = 0
        for table in TARGET_TABLES:
            count = export_table_data(vps_conn, local_conn, table)
            print(f"  -> [{table}] Migrados / actualizados {count} registros.")
            total_migrated += count

        print("  -> Reseteando secuencias PostgreSQL (setval)...")
        reset_local_sequences(local_conn)

        local_conn.commit()
        print("\n  ✅ ¡MIGRACIÓN COMPLETADA Y CONFIRMADA (COMMIT) EXITOSAMENTE!")

        post_local_counts = get_table_counts(local_conn)
        print("\n  [Totales Finales en Base Local]")
        print(f"  - Usuarios migrados: {post_local_counts.get('users', 0)}")
        print(f"  - Alumnos migrados:  {post_local_counts.get('alumnos', 0)}")
        print(f"  - Niveles Aprobados: {post_local_counts.get('niveles_aprobados', 0)}")
        print(f"  - Intentos (Puntajes): {post_local_counts.get('intentos', 0)}")

    except Exception as e:
        local_conn.rollback()
        print(f"\n❌ [ERROR CRÍTICO EN MIGRACIÓN] Revertido con Rollback: {e}")
        sys.exit(1)
    finally:
        vps_conn.close()
        local_conn.close()


if __name__ == "__main__":
    main()
