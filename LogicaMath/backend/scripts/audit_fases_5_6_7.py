#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Auditoría Puntual — Fases 5, 6 y 7
============================================
Audita el estado de las preguntas y sus recursos multimedia (MinIO)
para las Fases 5, 6 y 7.
"""

import asyncio
import os
import sys
import re
from typing import Dict, Any

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import select, func, and_
from app.db.session import AsyncSessionLocal
from app.models.sql_models import Pregunta
from app.core.storage import storage_service
from botocore.exceptions import ClientError

KEYWORDS_IMAGEN = [
    r"figura", r"dibujo", r"diseño", r"gráfico", r"gráfica", r"cuadrícula",
    r"plano", r"reloj", r"termómetro", r"sombreada", r"sombreado", r"fracción",
    r"esfera", r"cubo", r"cilindro", r"cono", r"pirámide", r"rectángulo",
    r"triángulo", r"círculo", r"plano cartesiano", r"coordenada", r"eje",
    r"escala", r"marcada en el reloj", r"siguiente imagen", r"observa",
    r"ilustra", r"urna", r"dado", r"bolas de colores"
]

async def check_image_exists(url: str) -> bool:
    if not url:
        return False
    if storage_service.s3_client:
        try:
            bucket_name = storage_service.bucket_name
            if bucket_name in url:
                parts = url.split(f"{bucket_name}/")
                key = parts[1] if len(parts) > 1 else url
            else:
                key = url.split("/")[-1]
            await asyncio.to_thread(
                storage_service.s3_client.head_object,
                Bucket=bucket_name,
                Key=key
            )
            return True
        except ClientError:
            return False
        except Exception:
            return False
    return False

async def run_audit():
    print("=" * 85)
    print("REPORTE DE AUDITORÍA PUNTUAL — FASES 5, 6 Y 7")
    print("=" * 85)

    async with AsyncSessionLocal() as session:
        for fase_id in [5, 6, 7]:
            query = select(Pregunta).where(Pregunta.fase_id == fase_id).order_by(Pregunta.seccion, Pregunta.id)
            result = await session.execute(query)
            preguntas = result.scalars().all()

            total_q = len(preguntas)
            requieren_grafico = 0
            con_url_valida = 0
            sin_url = 0
            secciones_breakdown = {}

            for q in preguntas:
                sec = q.seccion
                if sec not in secciones_breakdown:
                    secciones_breakdown[sec] = {"total": 0, "requieren": 0, "validas": 0}
                secciones_breakdown[sec]["total"] += 1

                datos = q.datos_numericos or {}
                if not isinstance(datos, dict):
                    datos = {}

                # Evaluar regla de imagen
                req = False
                if fase_id == 5 and sec in [101, 102, 103, 201, 202, 203]:
                    req = True
                elif fase_id == 6 and sec in [101, 102, 103, 201, 202, 203, 401, 402, 403]:
                    req = True
                elif fase_id == 7 and sec in [101, 102, 103, 201, 202, 203]:
                    req = True
                else:
                    for kw in KEYWORDS_IMAGEN:
                        if re.search(r"\b" + kw + r"\b", q.enunciado.lower()):
                            req = True
                            break

                if req:
                    requieren_grafico += 1
                    secciones_breakdown[sec]["requieren"] += 1
                    url = datos.get("url")
                    if url:
                        con_url_valida += 1
                        secciones_breakdown[sec]["validas"] += 1
                    else:
                        sin_url += 1

            print(f"\n--- FASE {fase_id} ---")
            print(f" Total preguntas sembradas:               {total_q}")
            print(f" Preguntas que requieren gráfico visual: {requieren_grafico}")
            print(f" Preguntas con URL de figura asignada:   {con_url_valida}")
            print(f" Preguntas sin URL asignada:              {sin_url}")
            print("\n Desglose por Sección:")
            for sec, data in sorted(secciones_breakdown.items()):
                print(f"   • Sección {sec:4d}: {data['total']:4d} preguntas | {data['requieren']:4d} requieren gráfico | {data['validas']:4d} con URL")

    print("\n" + "=" * 85)
    print("FIN DEL REPORTE DE AUDITORÍA")
    print("=" * 85)

if __name__ == "__main__":
    asyncio.run(run_audit())
