import asyncio
import json
import os
import sys
from pathlib import Path

# Agregar directorio backend al sys.path
backend_path = str(Path(__file__).resolve().parent.parent)
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import select
from app.config import settings
from app.models.ux_feedback import UXFeedback
from app.models.enums import FeedbackStatusEnum

async def export_pending_feedbacks():
    print("=============================================================")
    print("🚀 Exportador de Anotaciones UX Pendientes para Antigravity")
    print("=============================================================")

    db_url = settings.DATABASE_URL
    if not db_url:
        print("❌ Error: DATABASE_URL no está configurada.")
        return

    # Usar el protocolo correcto de asyncpg
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://")

    try:
        engine = create_async_engine(db_url)
        
        async with engine.connect() as conn:
            # Consultar feedbacks pendientes y en desarrollo
            query = select(UXFeedback).where(
                UXFeedback.estado.in_([FeedbackStatusEnum.PENDIENTE, FeedbackStatusEnum.EN_DESARROLLO])
            ).order_by(UXFeedback.prioridad, UXFeedback.fecha_creacion.desc())
            
            result = await conn.execute(query)
            feedbacks = result.fetchall()
            
            output_list = []
            for f in feedbacks:
                output_list.append({
                    "id": f.id,
                    "fase": f.fase,
                    "modulo_id": f.modulo_id,
                    "nivel_id": f.nivel_id,
                    "pregunta_id": f.pregunta_id,
                    "paso_actual": f.paso_actual,
                    "dom_selector": f.dom_selector,
                    "viewport": f.viewport,
                    "comentario": f.comentario,
                    "tipo": f.tipo.value if hasattr(f.tipo, 'value') else str(f.tipo),
                    "prioridad": f.prioridad,
                    "estado": f.estado.value if hasattr(f.estado, 'value') else str(f.estado),
                    "screenshot_url": f.screenshot_url,
                    "imagenes": f.imagenes,
                    "fecha_creacion": f.fecha_creacion.isoformat() if f.fecha_creacion else None
                })

            # Determinar ruta de salida tolerante a entornos Docker
            docs_dir = Path(backend_path).parent / "docs"
            output_dir = docs_dir
            try:
                os.makedirs(docs_dir, exist_ok=True)
                test_file = docs_dir / ".write_test"
                test_file.touch()
                test_file.unlink()
            except Exception:
                output_dir = Path(backend_path) / "data"
                os.makedirs(output_dir, exist_ok=True)

            output_file = output_dir / "ux_correcciones_pendientes.json"
            base_feedback_dir = output_dir / "ux_feedback"
            os.makedirs(base_feedback_dir, exist_ok=True)

            from app.core.storage import storage_service

            for f in output_list:
                f_id = f["id"]
                feedback_dir = base_feedback_dir / str(f_id)
                os.makedirs(feedback_dir, exist_ok=True)

                imagenes = f.get("imagenes") or []
                if not imagenes and f.get("screenshot_url"):
                    imagenes = [{"url": f["screenshot_url"], "rol": "actual"}]

                local_images = []
                for img in imagenes:
                    url = img["url"]
                    rol = img["rol"]
                    filename = os.path.basename(url)
                    local_img_path = feedback_dir / f"{rol}.png"
                    
                    try:
                        if storage_service.s3_client:
                            # Run synchronous AWS call in thread if possible, but we are in async, 
                            # we can just run it synchronously here since it's a script
                            import boto3
                            from botocore.exceptions import ClientError
                            key = f"screenshots/{filename}"
                            try:
                                resp = storage_service.s3_client.get_object(Bucket=storage_service.bucket_name, Key=key)
                                content = resp['Body'].read()
                                with open(local_img_path, "wb") as img_file:
                                    img_file.write(content)
                                local_images.append((rol, f"./{rol}.png"))
                            except ClientError as e:
                                print(f"  [!] No se encontro {key} en S3.")
                        else:
                            static_path = Path(backend_path) / "app" / "static" / "screenshots" / filename
                            if static_path.exists():
                                with open(static_path, "rb") as src:
                                    with open(local_img_path, "wb") as dst:
                                        dst.write(src.read())
                                local_images.append((rol, f"./{rol}.png"))
                    except Exception as e:
                        print(f"Error bajando imagen {url}: {e}")

                instruccion = f"# Feedback UX #{f_id}\n\n"
                instruccion += f"**Comentario**: {f['comentario']}\n\n"
                instruccion += f"- Fase: {f['fase']}\n- Módulo: {f['modulo_id']}\n- Nivel: {f['nivel_id']}\n"
                instruccion += f"- Selector DOM: `{f['dom_selector']}`\n\n"
                
                for rol, loc in local_images:
                    instruccion += f"### {rol.capitalize()}\n"
                    instruccion += f"![{rol}]({loc})\n\n"

                with open(feedback_dir / "instruccion.md", "w", encoding="utf-8") as inst_file:
                    inst_file.write(instruccion)

            with open(output_file, "w", encoding="utf-8") as json_file:
                json.dump(output_list, json_file, ensure_ascii=False, indent=2)

            print(f"✅ Se exportaron exitosamente {len(output_list)} mejorías UX pendientes.")
            print(f"📁 Archivo generado en: {output_file.resolve()}")
            print(f"📁 Instrucciones generadas en: {base_feedback_dir.resolve()}")
            print("=============================================================")
            
        await engine.dispose()
    except Exception as e:
        print(f"❌ Error durante el proceso de exportación: {e}")

if __name__ == "__main__":
    asyncio.run(export_pending_feedbacks())
