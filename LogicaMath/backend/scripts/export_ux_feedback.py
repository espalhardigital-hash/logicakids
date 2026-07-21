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
                    "fecha_creacion": f.fecha_creacion.isoformat() if f.fecha_creacion else None
                })

            # Determinar ruta de salida tolerante a entornos Docker
            output_file = None
            try:
                docs_dir = Path(backend_path).parent / "docs"
                # Intentar crear e interactuar con el directorio
                os.makedirs(docs_dir, exist_ok=True)
                test_file = docs_dir / ".write_test"
                test_file.touch()
                test_file.unlink()
                output_file = docs_dir / "ux_correcciones_pendientes.json"
            except Exception:
                # Fallback al directorio data/ del backend en Docker
                data_dir = Path(backend_path) / "data"
                os.makedirs(data_dir, exist_ok=True)
                output_file = data_dir / "ux_correcciones_pendientes.json"
            
            with open(output_file, "w", encoding="utf-8") as json_file:
                json.dump(output_list, json_file, ensure_ascii=False, indent=2)

            print(f"✅ Se exportaron exitosamente {len(output_list)} mejorías UX pendientes.")
            print(f"📁 Archivo generado en: {output_file.resolve()}")
            print("=============================================================")
            
        await engine.dispose()
    except Exception as e:
        print(f"❌ Error durante el proceso de exportación: {e}")

if __name__ == "__main__":
    asyncio.run(export_pending_feedbacks())
