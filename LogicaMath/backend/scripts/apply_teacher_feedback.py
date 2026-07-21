#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Diagnóstico y Aplicación de Feedback Docente (asistido por IA)
=======================================================================
Este script lee el archivo 'data/feedback_docente.json', lista los comentarios
pendientes del docente y, si está la API de Gemini disponible, sugiere y aplica
las correcciones a los enunciados o marca gráficos para regenerar en la DB.
"""

import asyncio
import os
import sys
import json
import httpx
from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

# Configurar path de Python para importar módulos del backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import engine, AsyncSessionLocal
from app.models.sql_models import Pregunta
from app.core.config import settings

async def call_gemini_to_suggest_correction(enunciado_actual: str, comentario_docente: str) -> Optional[str]:
    """Llama a la API de Gemini para sugerir un enunciado corregido en base al feedback."""
    api_key = settings.GOOGLE_API_KEY
    if not api_key:
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    prompt = (
        f"Actúa como un diseñador curricular de matemáticas para niños. Un docente ha dejado un comentario "
        f"sobre una pregunta de un juego.\n\n"
        f"Enunciado actual de la pregunta:\n\"{enunciado_actual}\"\n\n"
        f"Comentario/Queja del docente:\n\"{comentario_docente}\"\n\n"
        f"Tu tarea es reescribir el enunciado de la pregunta corrigiendo el error señalado por el docente. "
        f"Mantén un lenguaje claro, sencillo y lúdico apto para niños de primaria. "
        f"Responde ÚNICAMENTE con el nuevo enunciado propuesto, sin preámbulos, explicaciones ni comillas externas."
    )

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=20.0)
            if response.status_code == 200:
                data = response.json()
                text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                if text:
                    return text.strip()
    except Exception as e:
        print(f"      [!] Error al consultar Gemini para sugerencia: {e}")
    return None

async def list_and_process_feedback(auto_apply: bool = False):
    filepath = "data/feedback_docente.json"
    if not os.path.exists(filepath):
        print(f"No se encontró el archivo de feedback en {filepath}. No hay comentarios pendientes.")
        return

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            feedbacks = json.load(f)
    except Exception as e:
        print(f"Error al leer el archivo de feedback: {e}")
        return

    if not feedbacks:
        print("El archivo de feedback está vacío. ¡No hay comentarios pendientes!")
        return

    print("=" * 90)
    print(f"SE ENCONTRARON {len(feedbacks)} COMENTARIOS DE RETROALIMENTACIÓN DEL DOCENTE")
    print("=" * 90)

    async with AsyncSessionLocal() as session:
        for idx, fb in enumerate(feedbacks):
            fb_id = fb.get("id")
            fase_id = fb.get("fase_id")
            seccion_id = fb.get("seccion_id")
            pregunta_id = fb.get("pregunta_id")
            tipo = fb.get("tipo")
            comentario = fb.get("comentario")
            username = fb.get("docente_username", "docente")
            timestamp = fb.get("timestamp", "")
            
            print(f"\n[{idx + 1}] Feedback ID: {fb_id}")
            print(f"    Fecha: {timestamp} | Docente: {username}")
            print(f"    Ubicación: Fase {fase_id}, Sección/Nivel {seccion_id} | Tipo: {tipo.upper()}")
            print(f"    Comentario: \"{comentario}\"")

            if pregunta_id:
                # Consultar la pregunta en la DB
                result = await session.execute(
                    select(Pregunta).where(Pregunta.id == pregunta_id)
                )
                pregunta = result.scalar_one_or_none()
                if pregunta:
                    print(f"    Pregunta DB ID: {pregunta.id}")
                    print(f"    Enunciado actual: \"{pregunta.enunciado}\"")
                    
                    # Llamar a IA para sugerir corrección del enunciado
                    sugerencia = await call_gemini_to_suggest_correction(pregunta.enunciado, comentario)
                    if sugerencia:
                        print(f"    ✨ Sugerencia de Corrección por IA:\n       \"{sugerencia}\"")
                        
                        if auto_apply:
                            # Aplicar cambio en DB
                            pregunta.enunciado = sugerencia
                            
                            # Si el comentario menciona imagen, dibujo o reloj, marcamos la URL como vacía
                            # para que el script de autocuración de imágenes la regenere.
                            comentario_lc = comentario.lower()
                            if any(x in comentario_lc for x in ["imagen", "dibujo", "figura", "reloj", "gráfico", "dado", "urna"]):
                                print("    ⚠️ Comentario relacionado con gráficos detectado. Marcando imagen para regeneración...")
                                datos_num = pregunta.datos_numericos or {}
                                if "url" in datos_num:
                                    # Borrar la URL para disparar la autocuración en el siguiente ciclo
                                    datos_num["url"] = ""
                                    pregunta.datos_numericos = datos_num
                            
                            session.add(pregunta)
                            print("    [✓] Corrección sugerida aplicada en la base de datos.")
                    else:
                        print("    [!] No hay sugerencia de corrección disponible (API Key no configurada o fallo de red).")
                else:
                    print(f"    [!] Pregunta ID {pregunta_id} no encontrada en la base de datos.")
            else:
                print("    (Feedback de teoría o interactivo del nivel, no asociado a una pregunta individual)")

            print("-" * 60)
            
        if auto_apply:
            await session.commit()
            print("\n✅ Todos los cambios aplicados han sido guardados en la base de datos.")
            
            # Limpiar o renombrar el JSON de feedback para marcar como procesado
            processed_path = "data/feedback_docente_procesado.json"
            try:
                # Anexar a procesados
                processed_feedbacks = []
                if os.path.exists(processed_path):
                    with open(processed_path, "r", encoding="utf-8") as pf:
                        processed_feedbacks = json.load(pf)
                processed_feedbacks.extend(feedbacks)
                
                with open(processed_path, "w", encoding="utf-8") as pf:
                    json.dump(processed_feedbacks, pf, ensure_ascii=False, indent=2)
                
                # Vaciar el actual
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump([], f)
                print("✅ Comentarios procesados archivados en 'feedback_docente_procesado.json'.")
            except Exception as ex:
                print(f"Error al archivar comentarios procesados: {ex}")

if __name__ == "__main__":
    auto_apply_flag = "--apply" in sys.argv
    asyncio.run(list_and_process_feedback(auto_apply=auto_apply_flag))
