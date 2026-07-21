import asyncio
import os
import sys
import re
from sqlalchemy import select, and_
from botocore.exceptions import ClientError

# Configurar path de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import AsyncSessionLocal
from app.models.sql_models import Pregunta
from app.core.storage import storage_service
from app.config import settings

KEYWORDS_IMAGEN = [
    r"figura", r"dibujo", r"diseño", r"gráfico", r"gráfica", r"cuadrícula",
    r"plano", r"reloj", r"termómetro", r"sombreada", r"sombreado", r"fracción",
    r"esfera", r"cubo", r"cilindro", r"cono", r"pirámide", r"rectángulo",
    r"triángulo", r"círculo", r"plano cartesiano", r"coordenada", r"eje",
    r"escala", r"marcada en el reloj", r"siguiente imagen", r"observa",
    r"ilustra", r"urna", r"dado", r"bolas de colores"
]

async def verify_minio_integrity():
    print("=" * 90)
    print("INICIANDO VERIFICACIÓN DE INTEGRIDAD FÍSICA EN MINIO LOCAL")
    print("=" * 90)

    # Mostrar configuración de storage para diagnostico
    print(f"Endpoint configurado: {settings.S3_ENDPOINT_URL}")
    print(f"Bucket configurado:   {storage_service.bucket_name}")
    print("Conectando con base de datos local y MinIO...")

    async with AsyncSessionLocal() as session:
        # Obtener preguntas de Fases 3-8
        query = select(Pregunta).where(
            and_(
                Pregunta.fase_id >= 3,
                Pregunta.fase_id <= 8
            )
        )
        result = await session.execute(query)
        preguntas = result.scalars().all()

        visual_questions = []
        for q in preguntas:
            enunciado = q.enunciado
            fase_id = q.fase_id
            seccion_id = q.seccion
            
            requiere_imagen = False
            if fase_id == 5 and seccion_id in [101, 102, 103, 201, 202, 203]:
                requiere_imagen = True
            elif fase_id == 6 and seccion_id in [101, 102, 103, 201, 202, 203, 401, 402, 403]:
                requiere_imagen = True
            elif fase_id == 7 and seccion_id in [101, 102, 103, 201, 202, 203]:
                requiere_imagen = True
            else:
                for kw in KEYWORDS_IMAGEN:
                    if re.search(r"\b" + kw + r"\b", enunciado.lower()):
                        requiere_imagen = True
                        break
            
            if requiere_imagen:
                visual_questions.append(q)

        print(f"Preguntas visuales detectadas en DB: {len(visual_questions)}")

        exists_count = 0
        missing_count = 0
        error_count = 0
        sample_keys = []

        # Realizar HEAD check en MinIO para cada una
        for idx, q in enumerate(visual_questions):
            datos = q.datos_numericos or {}
            url = datos.get("url", "")

            if not url:
                missing_count += 1
                continue

            # Extraer Key
            bucket_name = storage_service.bucket_name
            if bucket_name in url:
                parts = url.split(f"{bucket_name}/")
                key = parts[1] if len(parts) > 1 else url
            else:
                key = url.split("/")[-1]

            if not key:
                missing_count += 1
                continue

            # Verificar HEAD a S3
            if storage_service.s3_client:
                try:
                    await asyncio.to_thread(
                        storage_service.s3_client.head_object,
                        Bucket=bucket_name,
                        Key=key
                    )
                    exists_count += 1
                    if len(sample_keys) < 5:
                        sample_keys.append(key)
                except ClientError as e:
                    # Si no se encuentra (404)
                    error_code = e.response.get('Error', {}).get('Code', 'Unknown')
                    if error_code == '404':
                        missing_count += 1
                    else:
                        error_count += 1
                except Exception as ex:
                    error_count += 1
            else:
                # Fallback local
                filename = url.split("/static/graphics/")[-1]
                local_path = os.path.join("app/static/graphics", filename)
                if os.path.exists(local_path):
                    exists_count += 1
                else:
                    missing_count += 1

            if (idx + 1) % 500 == 0 or (idx + 1) == len(visual_questions):
                print(f"   Procesadas {idx + 1}/{len(visual_questions)} preguntas...")

        print("\n" + "=" * 90)
        print("RESULTADOS DEL ANÁLISIS DE MINIO:")
        print(f" - Total de imágenes verificadas físicamente: {exists_count + missing_count + error_count}")
        print(f" - ✅ Imágenes intactas y existentes en MinIO: {exists_count}")
        print(f" - ❌ Imágenes faltantes (HTTP 404 / no URL):  {missing_count}")
        print(f" - ⚠️ Errores de conexión u otros:            {error_count}")
        print("-" * 90)
        if sample_keys:
            print("Muestras de objetos verificados con éxito en MinIO:")
            for sk in sample_keys:
                print(f"   • {sk}")
        print("=" * 90)

if __name__ == "__main__":
    asyncio.run(verify_minio_integrity())
