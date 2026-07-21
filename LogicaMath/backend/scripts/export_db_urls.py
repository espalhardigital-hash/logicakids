import json
import asyncio
import os
import sys

# Configurar path de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import AsyncSessionLocal
from app.models.sql_models import Pregunta
from sqlalchemy import select

async def run():
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(Pregunta.id, Pregunta.datos_numericos))
        rows = res.all()
        
        # Mapeo id -> datos_numericos
        data = {}
        for r in rows:
            q_id = r[0]
            datos = r[1]
            if datos:
                # Modificar URL de desarrollo/producción VPS de forma dinámica en base al bucket
                data[q_id] = datos
                
        output_path = "data/preguntas_urls.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"✅ JSON exportado con {len(data)} registros en {output_path}")

if __name__ == "__main__":
    asyncio.run(run())
