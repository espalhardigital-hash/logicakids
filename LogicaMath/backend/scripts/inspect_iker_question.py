"""
Script de Inspección de la pregunta de Iker (Fase 5, Módulo 1, Nivel 11)
"""

import sys
import os
import json
import psycopg2

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync_helpers import load_env_file, rewrite_db_url

def main():
    print("=" * 85)
    print("🔬 INSPECCIONANDO PREGUNTA DE IKER (FASE 5, MÓDULO 1)")
    print("=" * 85)

    loc_env = load_env_file("Datos_localhost/.env.local")
    loc_url = rewrite_db_url(loc_env["DATABASE_URL"], "localhost", 5433)
    loc_conn = psycopg2.connect(loc_url)
    cur = loc_conn.cursor()

    cur.execute("""
        SELECT id, fase_id, seccion, sub_nivel, operacion, tipo_pregunta, 
               enunciado, respuesta_correcta, datos_numericos, payload_tokenizado
        FROM preguntas 
        WHERE fase_id = 5 AND enunciado LIKE '%Iker reúne montos%';
    """)
    rows = cur.fetchall()
    print(f"[*] Preguntas coincidentes: {len(rows)}")

    for r in rows:
        print(f"\nID: {r[0]} | Fase: {r[1]} | Módulo: {r[2]} | Nivel: {r[3]} | Tipo: {r[5]}")
        print(f"Enunciado:\n  {r[6]}")
        print(f"Datos Numéricos:\n  {r[8]}")
        print(f"Payload Tokenizado:\n  {r[9]}")

        cur.execute("SELECT id, texto, es_correcta, orden FROM alternativas WHERE pregunta_id = %s ORDER BY orden;", (r[0],))
        alts = cur.fetchall()
        print("Alternativas:")
        for a in alts:
            print(f"  [{a[0]}] (Correcta: {a[2]}) -> {a[1]}")

    loc_conn.close()

if __name__ == "__main__":
    main()
