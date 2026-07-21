#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Actualización de URLs y Metadatos en la DB de la VPS
=============================================================
Este script lee 'data/preguntas_urls.json', ajusta dinámicamente las URLs locales
al dominio público de la VPS y al bucket correspondiente del entorno, y actualiza
los registros en PostgreSQL usando SQLAlchemy.
"""

import asyncio
import os
import sys
import json
from sqlalchemy import select, update
from sqlalchemy.orm import sessionmaker

# Configurar path de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import engine, AsyncSessionLocal
from app.models.sql_models import Pregunta
from app.config import settings

async def update_urls():
    print("=" * 90)
    print("INICIANDO ACTUALIZACIÓN DIDÁCTICA DE BANCO DE PREGUNTAS EN VPS")
    print("=" * 90)

    # Identificar bucket y dominio del entorno actual
    target_bucket = settings.S3_BUCKET_NAME
    target_domain = "https://files.espalhar.shop"
    
    print(f"Entorno detectado:")
    print(f" - Bucket configurado: {target_bucket}")
    print(f" - Servidor de assets: {target_domain}")

    filepath = "data/preguntas_urls.json"
    if not os.path.exists(filepath):
        print(f"❌ No se encontró el archivo de datos en {filepath}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        urls_data = json.load(f)

    print(f"[+] Cargados {len(urls_data)} registros del dump local.")
    
    async with AsyncSessionLocal() as session:
        count_updated = 0
        
        # Procesar por lotes
        keys = list(urls_data.keys())
        total_keys = len(keys)
        
        print(f"[+] Iniciando actualización de registros en PostgreSQL...")
        
        for idx, q_id_str in enumerate(keys):
            q_id = int(q_id_str)
            local_datos = urls_data[q_id_str]
            
            # Ajustar URL de local a VPS
            url = local_datos.get("url", "")
            if url:
                filename = url.split("graphics/")[-1]
                remoto_url = f"{target_domain}/{target_bucket}/graphics/{filename}"
                local_datos["url"] = remoto_url
            
            from sqlalchemy import text
            # Ejecutar update SQL puro
            await session.execute(
                text("UPDATE preguntas SET datos_numericos = :datos WHERE id = :id"),
                {"datos": json.dumps(local_datos), "id": q_id}
            )
            count_updated += 1
                
            if (idx + 1) % 2000 == 0 or (idx + 1) == total_keys:
                # Hacer commits intermedios para liberar memoria y locks de BD
                await session.commit()
                print(f"   Progreso: {idx + 1}/{total_keys} registros procesados (Actualizados: {count_updated})...")
                
        await session.commit()
        
    print("\n" + "=" * 90)
    print("RESUMEN DE ACTUALIZACIÓN:")
    print(f" - Registros analizados:    {total_keys}")
    print(f" - Registros actualizados:  {count_updated}")
    print("=" * 90)

if __name__ == "__main__":
    asyncio.run(update_urls())
