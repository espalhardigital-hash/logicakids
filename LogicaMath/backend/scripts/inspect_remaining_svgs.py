import psycopg2
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sync_helpers import load_env_file, rewrite_db_url

loc_env = load_env_file("Datos_localhost/.env.local")
loc_url = rewrite_db_url(loc_env["DATABASE_URL"], "localhost", 5433)
conn = psycopg2.connect(loc_url)
cur = conn.cursor()

cur.execute("""
    SELECT id, fase_id, substring(enunciado from '<svg[^>]*>') 
    FROM preguntas 
    WHERE enunciado LIKE '%<svg%' 
      AND (
        enunciado LIKE '%height:auto%' 
        OR (enunciado LIKE '%width=%320%' AND enunciado NOT LIKE '%height=%102%')
      )
    LIMIT 10;
""")
print(cur.fetchall())
conn.close()
