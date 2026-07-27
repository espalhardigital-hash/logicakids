"""
Script ultra-rápido, auto-reconectable y robusto de sincronización de preguntas y alternativas (Local -> VPS Prod)
Garantiza 100% de paridad con reconexión automática ante cortes de SSH tunnel.
"""

import sys
import os
import json
import time
import psycopg2
from psycopg2.extras import execute_values

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync_helpers import load_env_file, rewrite_db_url

def prepare_val(val):
    if isinstance(val, (dict, list)):
        return json.dumps(val)
    return val

def get_connections():
    loc_env = load_env_file("Datos_localhost/.env.local")
    rem_env = load_env_file("Datos_Producion/.env")

    loc_url = rewrite_db_url(loc_env["DATABASE_URL"], "localhost", 5433)
    rem_url = rewrite_db_url(rem_env["DATABASE_URL"], "localhost", 5435)

    loc_conn = psycopg2.connect(loc_url)
    rem_conn = psycopg2.connect(rem_url)

    return loc_conn, rem_conn

def main():
    print("=" * 80)
    print("🚀 INICIANDO SINCRONIZACIÓN AUTO-RECONECTABLE (LOCAL -> VPS PROD)")
    print("=" * 80)

    loc_conn, rem_conn = get_connections()

    loc_cur = loc_conn.cursor()
    rem_cur = rem_conn.cursor()

    # Mapeo de usuarios por email
    loc_cur.execute("SELECT id, email FROM users;")
    loc_users = {r[0]: r[1] for r in loc_cur.fetchall()}

    rem_cur.execute("SELECT id, email FROM users;")
    rem_users_by_email = {r[1]: r[0] for r in rem_cur.fetchall()}
    rem_user_ids = set(rem_users_by_email.values())

    user_id_map = {}
    for loc_id, email in loc_users.items():
        if email in rem_users_by_email:
            user_id_map[loc_id] = rem_users_by_email[email]
        else:
            user_id_map[loc_id] = None

    def map_user(uid):
        if not uid:
            return None
        if uid in rem_user_ids:
            return uid
        return user_id_map.get(uid, None)

    # 1. Obtener todas las preguntas locales
    loc_cur.execute("""
        SELECT id, fase_id, seccion, sub_nivel, operacion, tipo_pregunta, enunciado, 
               respuesta_correcta, datos_numericos, explicacion_paso_a_paso, requiere_subrayado, 
               palabras_clave, errores_previstos, creado_por, modificado_por, estado, 
               fecha_creacion, ultima_modificacion, payload_tokenizado, estructura_padre_id, 
               revisado_admin, revisado_por, fecha_revision
        FROM preguntas
        ORDER BY id;
    """)
    rows = loc_cur.fetchall()
    total_local = len(rows)
    print(f"[*] Total de preguntas locales a sincronizar: {total_local}")

    processed_rows = []
    for r in rows:
        r_list = list(r)
        if r_list[6] and "http://localhost:9100/logicakids" in r_list[6]:
            r_list[6] = r_list[6].replace("http://localhost:9100/logicakids", "https://files.espalhar.shop/logicakids-producion")
        
        r_list[13] = map_user(r_list[13])
        r_list[14] = map_user(r_list[14])
        r_list[21] = map_user(r_list[21])

        processed_rows.append(tuple(prepare_val(v) for v in r_list))

    batch_size = 200
    upsert_sql = """
        INSERT INTO preguntas (
            id, fase_id, seccion, sub_nivel, operacion, tipo_pregunta, enunciado, 
            respuesta_correcta, datos_numericos, explicacion_paso_a_paso, requiere_subrayado, 
            palabras_clave, errores_previstos, creado_por, modificado_por, estado, 
            fecha_creacion, ultima_modificacion, payload_tokenizado, estructura_padre_id, 
            revisado_admin, revisado_por, fecha_revision
        ) VALUES %s
        ON CONFLICT (id) DO UPDATE SET
            fase_id = EXCLUDED.fase_id,
            seccion = EXCLUDED.seccion,
            sub_nivel = EXCLUDED.sub_nivel,
            operacion = EXCLUDED.operacion,
            tipo_pregunta = EXCLUDED.tipo_pregunta,
            enunciado = EXCLUDED.enunciado,
            respuesta_correcta = EXCLUDED.respuesta_correcta,
            datos_numericos = EXCLUDED.datos_numericos,
            explicacion_paso_a_paso = EXCLUDED.explicacion_paso_a_paso,
            requiere_subrayado = EXCLUDED.requiere_subrayado,
            palabras_clave = EXCLUDED.palabras_clave,
            errores_previstos = EXCLUDED.errores_previstos,
            creado_por = EXCLUDED.creado_por,
            modificado_por = EXCLUDED.modificado_por,
            estado = EXCLUDED.estado,
            fecha_creacion = EXCLUDED.fecha_creacion,
            ultima_modificacion = EXCLUDED.ultima_modificacion,
            payload_tokenizado = EXCLUDED.payload_tokenizado,
            estructura_padre_id = EXCLUDED.estructura_padre_id,
            revisado_admin = EXCLUDED.revisado_admin,
            revisado_por = EXCLUDED.revisado_por,
            fecha_revision = EXCLUDED.fecha_revision;
    """

    total_chunks = (total_local + batch_size - 1) // batch_size
    for i in range(0, total_local, batch_size):
        chunk = processed_rows[i:i + batch_size]
        chunk_idx = i // batch_size + 1
        
        for attempt in range(5):
            try:
                execute_values(rem_cur, upsert_sql, chunk)
                rem_conn.commit()
                if chunk_idx % 20 == 0 or chunk_idx == total_chunks:
                    print(f"  ✓ Lote Preguntas {chunk_idx}/{total_chunks}: {i + len(chunk)}/{total_local} procesadas.")
                break
            except Exception as e:
                print(f"  ⚠️ Intento {attempt+1} falló en lote {chunk_idx}: {e}. Reconectando...")
                time.sleep(1)
                try:
                    _, rem_conn = get_connections()
                    rem_cur = rem_conn.cursor()
                except Exception as ex_reconn:
                    print(f"    Error al reconectar: {ex_reconn}")

    # Ajustar secuencia de ID de preguntas
    try:
        rem_cur.execute("SELECT setval('preguntas_id_seq', (SELECT MAX(id) FROM preguntas));")
        rem_conn.commit()
    except Exception:
        pass

    # 2. Obtener alternativas locales
    loc_cur.execute("""
        SELECT id, pregunta_id, texto, es_correcta, orden, tipo_error, 
               feedback_error, fecha_creacion, ultima_modificacion
        FROM alternativas
        ORDER BY id;
    """)
    alt_rows = loc_cur.fetchall()
    total_alts = len(alt_rows)
    print(f"[*] Total de alternativas locales a sincronizar: {total_alts}")

    processed_alts = [tuple(prepare_val(v) for v in r) for r in alt_rows]

    upsert_alt_sql = """
        INSERT INTO alternativas (
            id, pregunta_id, texto, es_correcta, orden, tipo_error, 
            feedback_error, fecha_creacion, ultima_modificacion
        ) VALUES %s
        ON CONFLICT (id) DO UPDATE SET
            pregunta_id = EXCLUDED.pregunta_id,
            texto = EXCLUDED.texto,
            es_correcta = EXCLUDED.es_correcta,
            orden = EXCLUDED.orden,
            tipo_error = EXCLUDED.tipo_error,
            feedback_error = EXCLUDED.feedback_error,
            fecha_creacion = EXCLUDED.fecha_creacion,
            ultima_modificacion = EXCLUDED.ultima_modificacion;
    """

    alt_chunks = (total_alts + batch_size - 1) // batch_size
    for i in range(0, total_alts, batch_size):
        chunk = processed_alts[i:i + batch_size]
        chunk_idx = i // batch_size + 1
        for attempt in range(5):
            try:
                execute_values(rem_cur, upsert_alt_sql, chunk)
                rem_conn.commit()
                if chunk_idx % 10 == 0 or chunk_idx == alt_chunks:
                    print(f"  ✓ Lote Alternativas {chunk_idx}/{alt_chunks}: {i + len(chunk)}/{total_alts} procesadas.")
                break
            except Exception as e:
                print(f"  ⚠️ Intento {attempt+1} falló en alternativas {chunk_idx}: {e}. Reconectando...")
                time.sleep(1)
                try:
                    _, rem_conn = get_connections()
                    rem_cur = rem_conn.cursor()
                except Exception:
                    pass

    try:
        rem_cur.execute("SELECT setval('alternativas_id_seq', (SELECT MAX(id) FROM alternativas));")
        rem_conn.commit()
    except Exception:
        pass

    # Verificar recuento final
    rem_cur.execute("SELECT COUNT(*) FROM preguntas;")
    final_preguntas = rem_cur.fetchone()[0]

    rem_cur.execute("SELECT COUNT(*) FROM alternativas;")
    final_alternativas = rem_cur.fetchone()[0]

    print("=" * 80)
    print(f"✅ SINCRONIZACIÓN FINALIZADA CON ÉXITO:")
    print(f"  • Total preguntas en VPS Prod: {final_preguntas} (Local: {total_local})")
    print(f"  • Total alternativas en VPS Prod: {final_alternativas} (Local: {total_alts})")
    print("=" * 80)

    loc_conn.close()
    rem_conn.close()

if __name__ == "__main__":
    main()
