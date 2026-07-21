#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auditor y Autocurador de Imágenes de Preguntas (Fases 3 a 8)
==========================================================
Este script realiza una auditoría completa de la base de datos de preguntas
para las Fases 3 a 8. Identifica preguntas que requieran un dibujo, figura,
diseño o representación gráfica. Si el asset no existe o está dañado en MinIO,
lo genera de forma automática (procedimental o usando Gemini) y lo asocia.
"""

import asyncio
import os
import sys
import re
import math
import io
import random
import base64
import httpx
from typing import List, Dict, Any, Optional
from PIL import Image, ImageDraw, ImageFont
from sqlalchemy import select, and_, update
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Configurar path de Python para poder importar módulos de la app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import engine, AsyncSessionLocal
from app.models.sql_models import Pregunta, OperacionEnum, TipoPreguntaEnum
from app.core.storage import storage_service
from app.core.config import settings
from app.utils.graphics_generator import (
    generate_clock_image,
    generate_cartesian_plane_image,
    generate_grid_shape_image,
    generate_isometric_cubes_image,
    generate_thermometer_image,
    get_font
)

# Palabras clave heurísticas para detectar necesidad de gráficos
KEYWORDS_IMAGEN = [
    r"figura", r"dibujo", r"diseño", r"gráfico", r"gráfica", r"cuadrícula",
    r"plano", r"reloj", r"termómetro", r"sombreada", r"sombreado", r"fracción",
    r"esfera", r"cubo", r"cilindro", r"cono", r"pirámide", r"rectángulo",
    r"triángulo", r"círculo", r"plano cartesiano", r"coordenada", r"eje",
    r"escala", r"marcada en el reloj", r"siguiente imagen", r"observa",
    r"ilustra", r"urna", r"dado", r"bolas de colores"
]

# =====================================================================
# GENERADORES DE GRÁFICOS ADICIONALES (Fracciones, Urnas, Dados, etc.)
# =====================================================================

def generate_fraction_circle_image(numerador: int, denominador: int) -> bytes:
    """Dibuja una pizza de fracciones dividida en partes iguales."""
    size = 600
    img = Image.new("RGBA", (size, size), (30, 41, 59, 0)) # Fondo transparente
    draw = ImageDraw.Draw(img)
    
    center_x, center_y = size // 2, size // 2
    r = int(size * 0.4)
    
    # 1. Dibujar fondo del círculo
    draw.ellipse([center_x - r, center_y - r, center_x + r, center_y + r], fill=(15, 23, 42, 255), outline=(148, 163, 184, 255), width=6)
    
    # 2. Dibujar porciones rellenas
    angle_step = 360 / denominador
    for i in range(denominador):
        start_angle = i * angle_step - 90
        end_angle = (i + 1) * angle_step - 90
        
        # Color diferenciado para porciones sombreadas
        if i < numerador:
            # Color lila/púrpura educativo
            draw.pieslice([center_x - r + 6, center_y - r + 6, center_x + r - 6, center_y + r - 6], 
                          start_angle, end_angle, fill=(168, 85, 247, 180), outline=(168, 85, 247, 255), width=2)
        else:
            # Porciones vacías
            draw.pieslice([center_x - r + 6, center_y - r + 6, center_x + r - 6, center_y + r - 6], 
                          start_angle, end_angle, fill=(30, 41, 59, 100), outline=(71, 85, 105, 150), width=2)
            
    # Reducir imagen para antialiasing
    img_resized = img.resize((300, 300), Image.Resampling.LANCZOS)
    output = io.BytesIO()
    img_resized.save(output, format="PNG")
    return output.getvalue()


def generate_fraction_bar_image(numerador: int, denominador: int) -> bytes:
    """Dibuja una barra de fracciones dividida en partes iguales."""
    width, height = 800, 200
    img = Image.new("RGBA", (width, height), (30, 41, 59, 0))
    draw = ImageDraw.Draw(img)
    
    margin_x = 40
    margin_y = 40
    bar_w = width - 2 * margin_x
    bar_h = height - 2 * margin_y
    
    cell_w = bar_w / denominador
    
    # 1. Dibujar el marco exterior
    draw.rectangle([margin_x, margin_y, width - margin_x, height - margin_y], fill=(15, 23, 42, 255), outline=(148, 163, 184, 255), width=5)
    
    # 2. Dibujar divisiones y celdas sombreadas
    for i in range(denominador):
        x1 = margin_x + i * cell_w
        x2 = margin_x + (i + 1) * cell_w
        
        # Relleno sombreado
        if i < numerador:
            draw.rectangle([x1 + 3, margin_y + 3, x2 - 3, height - margin_y - 3], fill=(56, 189, 248, 180), outline=(56, 189, 248, 255), width=2)
        else:
            draw.rectangle([x1 + 3, margin_y + 3, x2 - 3, height - margin_y - 3], fill=(30, 41, 59, 100), outline=(71, 85, 105, 150), width=2)
            
    img_resized = img.resize((400, 100), Image.Resampling.LANCZOS)
    output = io.BytesIO()
    img_resized.save(output, format="PNG")
    return output.getvalue()


def generate_urn_balls_image(red: int, blue: int, green: int, yellow: int = 0) -> bytes:
    """Dibuja una urna/frasco transparente que contiene bolas de colores."""
    width, height = 500, 600
    img = Image.new("RGBA", (width, height), (30, 41, 59, 0))
    draw = ImageDraw.Draw(img)
    
    # 1. Dibujar la urna (silueta de frasco redondeado)
    # Cuerpo del frasco
    draw.rectangle([100, 150, 400, 500], fill=(15, 23, 42, 120), outline=(148, 163, 184, 200), width=6)
    # Cuello del frasco
    draw.rectangle([150, 80, 350, 150], fill=(15, 23, 42, 120), outline=(148, 163, 184, 200), width=6)
    # Tapa
    draw.rectangle([130, 50, 370, 80], fill=(56, 189, 248, 255), outline=(255, 255, 255, 255), width=2)
    # Borrar líneas de unión internas
    draw.rectangle([152, 145, 348, 155], fill=(15, 23, 42, 255))
    
    # 2. Dibujar bolas de colores dentro del frasco
    balls = []
    balls.extend([("red", (239, 68, 68, 255)) for _ in range(red)])
    balls.extend([("blue", (56, 189, 248, 255)) for _ in range(blue)])
    balls.extend([("green", (34, 197, 94, 255)) for _ in range(green)])
    balls.extend([("yellow", (234, 179, 8, 255)) for _ in range(yellow)])
    
    # Posiciones aleatorias fijas dentro del cuerpo de la urna (120 < x < 380, 200 < y < 480)
    rng = random.Random(42)
    ball_r = 30
    
    # Intentar posicionarlas sin que se superpongan en exceso
    placed_positions = []
    for color_name, fill_color in balls:
        placed = False
        for _ in range(100): # Intentos
            cx = rng.randint(130 + ball_r, 370 - ball_r)
            cy = rng.randint(200 + ball_r, 470 - ball_r)
            
            # Verificar colisión
            collision = False
            for px, py in placed_positions:
                dist = math.sqrt((cx - px)**2 + (cy - py)**2)
                if dist < ball_r * 1.8:
                    collision = True
                    break
            
            if not collision:
                placed_positions.append((cx, cy))
                # Dibujar bola con brillo 3D
                draw.ellipse([cx - ball_r, cy - ball_r, cx + ball_r, cy + ball_r], fill=fill_color, outline=(255, 255, 255, 255), width=2)
                draw.ellipse([cx - ball_r // 2, cy - ball_r // 2, cx - ball_r // 4, cy - ball_r // 4], fill=(255, 255, 255, 120))
                placed = True
                break
                
        if not placed: # Fallback si hay muchas bolas
            cx = rng.randint(130 + ball_r, 370 - ball_r)
            cy = rng.randint(200 + ball_r, 470 - ball_r)
            draw.ellipse([cx - ball_r, cy - ball_r, cx + ball_r, cy + ball_r], fill=fill_color, outline=(255, 255, 255, 255), width=2)
            placed_positions.append((cx, cy))

    img_resized = img.resize((250, 300), Image.Resampling.LANCZOS)
    output = io.BytesIO()
    img_resized.save(output, format="PNG")
    return output.getvalue()


def generate_dice_image(valor: int) -> bytes:
    """Dibuja la cara de un dado mostrando una cantidad de puntos (1 a 6)."""
    size = 400
    img = Image.new("RGBA", (size, size), (30, 41, 59, 0))
    draw = ImageDraw.Draw(img)
    
    # 1. Dibujar el cuerpo del dado (Cuadrado con esquinas redondeadas)
    body_color = (248, 250, 252, 255) # Blanco premium
    border_color = (15, 23, 42, 255)  # Borde oscuro
    draw.rounded_rectangle([40, 40, 360, 360], radius=50, fill=body_color, outline=border_color, width=12)
    
    # 2. Posiciones de los puntos del dado
    # Centro: (200, 200)
    # Arriba izquierda: (110, 110), Arriba derecha: (290, 110)
    # Medio izquierda: (110, 200), Medio derecha: (290, 200)
    # Abajo izquierda: (110, 290), Abajo derecha: (290, 290)
    dot_r = 25
    dots = {
        1: [(200, 200)],
        2: [(110, 110), (290, 290)],
        3: [(110, 110), (200, 200), (290, 290)],
        4: [(110, 110), (290, 110), (110, 290), (290, 290)],
        5: [(110, 110), (290, 110), (200, 200), (110, 290), (290, 290)],
        6: [(110, 110), (290, 110), (110, 200), (290, 200), (110, 290), (290, 290)]
    }
    
    for cx, cy in dots.get(valor, [(200, 200)]):
        draw.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill=(15, 23, 42, 255))
        
    img_resized = img.resize((200, 200), Image.Resampling.LANCZOS)
    output = io.BytesIO()
    img_resized.save(output, format="PNG")
    return output.getvalue()


# =====================================================================
# PIPELINE DE VERIFICACIÓN Y AUTOGENERACIÓN
# =====================================================================

async def generate_image_via_gemini_imagen(prompt: str) -> Optional[bytes]:
    """Genera una imagen usando la API de Gemini Imagen 3."""
    api_key = settings.GOOGLE_API_KEY
    if not api_key:
        return None
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:generateImages?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "prompt": prompt,
        "numberOfImages": 1,
        "outputMimeType": "image/png",
        "aspectRatio": "16:9",
        "personGeneration": "allow_adult"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=60.0)
            if response.status_code == 200:
                data = response.json()
                img_b64 = data.get("generatedImages", [{}])[0].get("image", {}).get("imageBytes")
                if img_b64:
                    print(f"      [+] Imagen generada exitosamente mediante Gemini Imagen.")
                    return base64.b64decode(img_b64)
            print(f"      [!] Error en Gemini Imagen (Status {response.status_code}): {response.text}")
    except Exception as e:
        print(f"      [!] Excepción al llamar a Gemini Imagen: {e}")
    return None

async def analizar_enunciado_y_generar(enunciado: str, fase_id: int, seccion_id: int, datos_numericos: Dict[str, Any]) -> Optional[bytes]:
    """
    Analiza el enunciado y la sección pedagógica de una pregunta
    para determinar y generar la imagen procedimental adecuada.
    """
    text_clean = enunciado.lower()
    
    # 1. CASO RELOJ (Fase 7 o mención explícita de horas/reloj)
    if "reloj" in text_clean or "hora" in text_clean or "minutos" in text_clean or "termina" in text_clean or "llego" in text_clean:
        # Buscar patrón de horas: HH:MM o H:MM
        match = re.search(r"(\d{1,2}):(\d{2})", enunciado)
        if match:
            h = int(match.group(1))
            m = int(match.group(2))
        else:
            # Fallback a datos numéricos o por defecto
            h = datos_numericos.get("hora", datos_numericos.get("h", 8))
            m = datos_numericos.get("minuto", datos_numericos.get("m", 0))
            
        print(f"   -> Generando Reloj Analógico ({h:02d}:{m:02d})")
        return generate_clock_image(h, m)

    # 2. CASO PLANO CARTESIANO (Fase 7 o coordenadas)
    if "cartesiano" in text_clean or "coordenada" in text_clean or "vector" in text_clean or "eje" in text_clean:
        # Intentar extraer puntos lógicos, ej: A(3, 2) o B(7, 5) o (4, 5)
        matches = re.findall(r"\((\d+)\s*,\s*(\d+)\)", enunciado)
        points = []
        labels = ["A", "B", "C", "D"]
        for idx, (x, y) in enumerate(matches):
            label = labels[idx] if idx < len(labels) else f"P{idx}"
            points.append({"x": int(x), "y": int(y), "label": label})
            
        if not points:
            # Buscar en datos numéricos o asignar un punto por defecto
            px = datos_numericos.get("x", 3)
            py = datos_numericos.get("y", 2)
            points = [{"x": px, "y": py, "label": "P"}]
            
        print(f"   -> Generando Plano Cartesiano con puntos: {points}")
        return generate_cartesian_plane_image(points)

    # 3. CASO CUADRÍCULA / GEOMETRÍA PLANA (Fase 5 - Perímetro / Área)
    if fase_id == 5 or "cuadrícula" in text_clean or "perímetro" in text_clean or "área" in text_clean:
        # Extraer dimensiones a y b
        a = datos_numericos.get("a", datos_numericos.get("base", 4))
        b = datos_numericos.get("b", datos_numericos.get("altura", 3))
        
        # Intentar extraer números directamente del enunciado si no hay
        if not a or not b:
            nums = [int(s) for s in re.findall(r"\b\d+\b", enunciado)]
            if len(nums) >= 2:
                a, b = nums[0], nums[1]
            else:
                a, b = 4, 3
                
        # Asegurar límites razonables
        a = max(2, min(8, a))
        b = max(2, min(8, b))
        
        vertices = [(1, 1), (1 + a, 1), (1 + a, 1 + b), (1, 1 + b)]
        grid_w, grid_h = max(10, a + 3), max(10, b + 3)
        
        is_area = "área" in text_clean or "baldosa" in text_clean or "cubrir" in text_clean
        fill_color = (168, 85, 247, 60) if is_area else (56, 189, 248, 40)
        outline_color = (168, 85, 247, 255) if is_area else (56, 189, 248, 255)
        
        print(f"   -> Generando Cuadrícula geométrica ({a}x{b}) - Tipo: {'Área' if is_area else 'Perímetro'}")
        return generate_grid_shape_image(vertices, grid_size=(grid_w, grid_h), fill_color=fill_color, outline_color=outline_color)

    # 4. CASO VOLUMEN / CUBOS ISOMÉTRICOS (Fase 6)
    if "cubo" in text_clean or "bloque" in text_clean or "volumen" in text_clean or "apila" in text_clean:
        # Intentar extraer largo, ancho y alto
        largo = datos_numericos.get("largo", 3)
        ancho = datos_numericos.get("ancho", 2)
        alto = datos_numericos.get("alto", 2)
        
        cubes = []
        for x in range(largo):
            for y in range(ancho):
                for z in range(alto):
                    cubes.append((x, y, z))
                    
        if not cubes:
            # Cubos estándar por defecto
            cubes = [(0,0,0), (1,0,0), (0,1,0), (0,0,1)]
            
        print(f"   -> Generando Cubos Isométricos ({largo}x{ancho}x{alto})")
        return generate_isometric_cubes_image(cubes)

    # 5. CASO TERMÓMETRO (Fase 6)
    if "termómetro" in text_clean or "temperatura" in text_clean or "grados" in text_clean or "°c" in text_clean:
        # Extraer temperatura del enunciado o datos numéricos
        match = re.search(r"(-?\d+)\s*(?:°c|grados)", enunciado)
        if match:
            temp = float(match.group(1))
        else:
            temp = float(datos_numericos.get("temp", datos_numericos.get("temperatura", 20.0)))
            
        print(f"   -> Generando Termómetro ({temp}°C)")
        return generate_thermometer_image(temp)

    # 6. CASO FRACCIONES (Fase 4 o enunciado de fracciones)
    if "fracción" in text_clean or "partes" in text_clean or "sombreada" in text_clean or "sombreado" in text_clean:
        # Buscar un formato numérico fraccionario como 3/4 o 5/8
        match = re.search(r"(\d+)/(\d+)", enunciado)
        if match:
            num = int(match.group(1))
            den = int(match.group(2))
        else:
            num = datos_numericos.get("numerador", datos_numericos.get("num", 1))
            den = datos_numericos.get("denominador", datos_numericos.get("den", 4))
            
        # Validar consistencia
        if den <= 0:
            den = 4
        num = min(num, den)
        
        # Decidir si barra o círculo
        if "barra" in text_clean or "tira" in text_clean or "rectángulo" in text_clean:
            print(f"   -> Generando Barra de Fracción ({num}/{den})")
            return generate_fraction_bar_image(num, den)
        else:
            print(f"   -> Generando Pizza de Fracción ({num}/{den})")
            return generate_fraction_circle_image(num, den)

    # 7. CASO URNA CON BOLAS (Fase 8 o probabilidad)
    if "urna" in text_clean or "bolas" in text_clean or "esferas" in text_clean or "frasco" in text_clean:
        # Buscar colores y cantidades
        red = int(datos_numericos.get("rojas", datos_numericos.get("red", 3)))
        blue = int(datos_numericos.get("azules", datos_numericos.get("blue", 4)))
        green = int(datos_numericos.get("verdes", datos_numericos.get("green", 2)))
        yellow = int(datos_numericos.get("amarillas", datos_numericos.get("yellow", 0)))
        
        # Escanear texto si no están en datos
        for color, val in [("roja", 3), ("azul", 4), ("verde", 2), ("amarilla", 1)]:
            match = re.search(r"(\d+)\s*" + color, text_clean)
            if match:
                val = int(match.group(1))
                if "roja" in color: red = val
                elif "azul" in color: blue = val
                elif "verde" in color: green = val
                elif "amarilla" in color: yellow = val
                
        # Intentar generar con Gemini Imagen 3
        ai_prompt = f"Ilustración educativa infantil minimalista estilo cartoon 2D vector, fondo oscuro (#1e293b), una urna transparente con {red} bolas rojas, {blue} bolas azules y {green} bolas verdes adentro."
        ai_img = await generate_image_via_gemini_imagen(ai_prompt)
        if ai_img:
            return ai_img

        print(f"   -> Generando Urna de Bolas (Rojo:{red}, Azul:{blue}, Verde:{green}, Amarillo:{yellow})")
        return generate_urn_balls_image(red, blue, green, yellow)

    # 8. CASO DADO (Fase 8 o probabilidad)
    if "dado" in text_clean or "caras" in text_clean:
        match = re.search(r"\b([1-6])\b", enunciado)
        val = int(match.group(1)) if match else datos_numericos.get("valor", datos_numericos.get("dado", 6))
        
        # Intentar generar con Gemini Imagen 3
        ai_prompt = f"Ilustración educativa infantil minimalista estilo cartoon 2D vector, fondo oscuro (#1e293b), un dado blanco de 6 caras mostrando el valor {val} en la cara frontal."
        ai_img = await generate_image_via_gemini_imagen(ai_prompt)
        if ai_img:
            return ai_img

        print(f"   -> Generando Cara de Dado ({val})")
        return generate_dice_image(val)

    # Intentar generar imagen con Gemini Imagen 3
    ai_prompt = f"Ilustración educativa infantil minimalista estilo cartoon 2D vector, fondo oscuro (#1e293b), representación clara de: {enunciado}"
    ai_img = await generate_image_via_gemini_imagen(ai_prompt)
    if ai_img:
        return ai_img

    # Fallback general para preguntas visuales (ej. un dibujo minimalista abstracto de matemáticas)
    print("   -> Generando Ilustración Minimalista Matemática por defecto")
    size = 400
    img = Image.new("RGBA", (size, size), (30, 41, 59, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([50, 50, 350, 350], radius=30, fill=(15, 23, 42, 255), outline=(56, 189, 248, 255), width=6)
    # Dibujar un signo de pregunta brillante
    font = get_font(120)
    draw.text((150, 100), "?", fill=(56, 189, 248, 255), font=font)
    output = io.BytesIO()
    img.save(output, format="PNG")
    return output.getvalue()


async def check_image_exists_in_storage(url: str) -> bool:
    """Verifica si la imagen existe en el storage (MinIO o local)."""
    if not url:
        return False
        
    # Si la URL apunta a S3/MinIO
    if storage_service.s3_client:
        try:
            # Extraer key del bucket
            bucket_name = storage_service.bucket_name
            if bucket_name in url:
                parts = url.split(f"{bucket_name}/")
                key = parts[1] if len(parts) > 1 else url
            else:
                key = url.split("/")[-1]
                
            # Hacer petición HEAD rápida a S3
            await asyncio.to_thread(
                storage_service.s3_client.head_object,
                Bucket=bucket_name,
                Key=key
            )
            return True
        except ClientError:
            return False
        except Exception as e:
            print(f"      [!] Error verificando S3: {e}")
            return False
            
    # Caso fallback local (verificar en disco)
    if "/static/graphics/" in url:
        filename = url.split("/static/graphics/")[-1]
        local_path = os.path.join("app/static/graphics", filename)
        return os.path.exists(local_path)
        
    return False


async def audit_and_heal_database():
    print("=" * 80)
    print("INICIANDO PIPELINE DE AUDITORÍA Y AUTOCURACIÓN DE IMÁGENES (FASES 3 A 8)")
    print("=" * 80)
    
    async with AsyncSessionLocal() as session:
        # Obtener todas las preguntas de las fases 3 a 8
        query = select(Pregunta).where(
            and_(
                Pregunta.fase_id >= 3,
                Pregunta.fase_id <= 8
            )
        ).order_by(Pregunta.fase_id, Pregunta.seccion, Pregunta.id)
        
        result = await session.execute(query)
        preguntas = result.scalars().all()
        
        print(f"Total de preguntas encontradas en Fases 3-8: {len(preguntas)}")
        
        audited_count = 0
        healed_count = 0
        skipped_count = 0
        
        for q in preguntas:
            enunciado = q.enunciado
            fase_id = q.fase_id
            seccion_id = q.seccion
            
            # Asegurar que datos_numericos sea un dict operable
            datos_numericos = q.datos_numericos or {}
            if not isinstance(datos_numericos, dict):
                datos_numericos = {}
                
            # Determinar si la pregunta requiere imagen
            requiere_imagen = False
            
            # Regla 1: Fases eminentemente visuales en ciertos niveles
            if fase_id == 5 and seccion_id in [101, 102, 103, 201, 202, 203]:
                requiere_imagen = True
            elif fase_id == 6 and seccion_id in [101, 102, 103, 201, 202, 203, 401, 402, 403]:
                requiere_imagen = True
            elif fase_id == 7 and seccion_id in [101, 102, 103, 201, 202, 203]:
                requiere_imagen = True
            else:
                # Regla 2: Búsqueda de palabras clave
                for kw in KEYWORDS_IMAGEN:
                    if re.search(r"\b" + kw + r"\b", enunciado.lower()):
                        requiere_imagen = True
                        break
                        
            # Si requiere imagen, verificarla
            if requiere_imagen:
                audited_count += 1
                current_url = datos_numericos.get("url")
                
                # Chequear existencia física del archivo
                exists = await check_image_exists_in_storage(current_url)
                
                if exists:
                    skipped_count += 1
                    continue
                    
                # Si no existe, autocurarla
                print(f"\n[!] Pregunta ID {q.id} (Fase {fase_id}, Sec {seccion_id}) requiere gráfico y falta o está roto.")
                print(f"    Texto: \"{enunciado[:90]}...\"")
                print(f"    URL previa: {current_url}")
                
                # Generar imagen procedimental
                img_bytes = await analizar_enunciado_y_generar(enunciado, fase_id, seccion_id, datos_numericos)
                
                if img_bytes:
                    # Subir a MinIO
                    filename = f"healed_q_{q.id}.png"
                    url = await storage_service.upload_question_graphic(img_bytes, filename)
                    
                    # Actualizar datos de la pregunta
                    datos_numericos["url"] = url
                    datos_numericos["tipo_visual"] = "imagen"
                    
                    # Usar update para forzar la escritura de JSONB en SQLAlchemy
                    await session.execute(
                        update(Pregunta)
                        .where(Pregunta.id == q.id)
                        .values(datos_numericos=datos_numericos)
                    )
                    
                    healed_count += 1
                    print(f"    ✅ Autocurada con éxito. Nueva URL: {url}")
                else:
                    print("    ❌ Falló la generación de la imagen para esta pregunta.")
                    
        await session.commit()
        
    print("\n" + "=" * 80)
    print("RESUMEN DE AUDITORÍA Y AUTOCURACIÓN:")
    print(f" - Preguntas analizadas que requieren gráficos: {audited_count}")
    print(f" - Preguntas con imágenes válidas y omitidas:  {skipped_count}")
    print(f" - Preguntas autocuradas / regeneradas:        {healed_count}")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(audit_and_heal_database())
