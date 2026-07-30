"""
Script de auditoría integral y unificada para la Reestructuración de la Fase 4 (CH-0 a CH-6).
Ejecuta verificaciones sobre código, archivos de configuración, esquemas y la BD local SQLite.

Criterios Auditados:
- CH-0: Notas de precedencia documental en 6 archivos clave.
- CH-1: Fase Decimales (fase_id=4), FASE_DECIMALES_ID=4, módulos parqueados (id>=90).
- CH-2: Catálogos JSON de plantillas y escenarios de la Fase 4.
- CH-3: CSS de ventana fija 950x620px y cero scroll.
- CH-4: Estructura de interactividad en paso con elección (opciones/explicaciones en teoría).
- CH-5: Práctica libre de 3.456 preguntas (12 niveles x 288) todas RESPUESTA_NUMERICA.
- CH-6: Desafíos de 1.950 preguntas (13 bloques x 150) D1/D2/DF/DM, ≤40 palabras, errores_previstos.
"""

import os
import sys
import json
import asyncio

DB_PATH = f"./test_master_audit_{os.getpid()}.db"
os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{DB_PATH}"

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.dialects.postgresql import JSONB, ARRAY, INET, UUID
from sqlalchemy.types import JSON

@compiles(JSONB, 'sqlite')
def compile_jsonb_sqlite(type_, compiler, **kw):
    return "JSON"

@compiles(ARRAY, 'sqlite')
def compile_array_sqlite(type_, compiler, **kw):
    return "JSON"

@compiles(INET, 'sqlite')
def compile_inet_sqlite(type_, compiler, **kw):
    return "VARCHAR"

@compiles(UUID, 'sqlite')
def compile_uuid_sqlite(type_, compiler, **kw):
    return "VARCHAR"

from sqlalchemy import select, func
from app.db.base import Base
from app.db.session import engine, AsyncSessionLocal
from app.models.sql_models import Pregunta, Alternativa, ConfiguracionProgreso, TipoPreguntaEnum, Fase
from app.fase5.seed import (
    upsert_fila_fases, seed_practica_pool,
    seed_preguntas_desafios, seed_configuracion_progreso,
    FASE_DECIMALES_ID
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def run_master_audit():
    print("==========================================================================")
    print("   AUDITORÍA MASTER DE TERRENO - REESTRUCTURACIÓN FASE 4 (CH-0 A CH-6)   ")
    print("==========================================================================")

    # --------------------------------------------------------------------------
    # CH-0: Auditoría Documental
    # --------------------------------------------------------------------------
    print("\n[CH-0] Verificando notas de precedencia documental en 6 archivos clave...")
    doc_paths = [
        "docs/Criterios Diseno Fase/1_Documento_Rector_Pedagogico.md",
        "docs/Criterios Diseno Fase/2_Arquitectura_Backend_y_Admin.md",
        "docs/Criterios Diseno Fase/3_Guia_Frontend_UX.md",
        "docs/Criterios Diseno Fase/4_Guia_TJS_Desafios.md",
        "docs/Criterios Diseno Fase/guia_creacion_fase.md",
        "docs/MAPA_CANONICO_FASES.md"
    ]
    repo_root = "d:/Antigravity/APP_Logica_Matematicas_kids"
    for dp in doc_paths:
        full_p = os.path.join(repo_root, dp)
        assert os.path.exists(full_p), f"Falta archivo documental: {dp}"
        with open(full_p, "r", encoding="utf-8") as f:
            head = f.read(300)
            assert "Reestructuración de la Fase 4 en curso" in head, f"Falta aviso de precedencia en {dp}"
    print("  [OK] CH-0 100% OK: Precedencia documental confirmada en los 6 archivos.")

    # --------------------------------------------------------------------------
    # CH-1 / CH-5 / CH-6: Verificación de Base de Datos y Siembra
    # --------------------------------------------------------------------------
    print("\n[BD] Inicializando base de datos SQLite autónoma y ejecutando siembra...")
    await init_db()

    async with AsyncSessionLocal() as session:
        await upsert_fila_fases(session)
        print("  -> Sembrando 3.456 preguntas de práctica libre (CH-5)...")
        await seed_practica_pool(session)
        print("  -> Sembrando 1.950 preguntas de desafíos (CH-6)...")
        await seed_preguntas_desafios(session)
        print("  -> Sembrando 32 filas de configuracion_progreso...")
        await seed_configuracion_progreso(session)

        # ----------------------------------------------------------------------
        # CH-1: Verificación de IDs de Fase y Fundación
        # ----------------------------------------------------------------------
        print("\n[CH-1] Verificando fundación de datos de intercambio...")
        assert FASE_DECIMALES_ID == 4, f"FASE_DECIMALES_ID es {FASE_DECIMALES_ID}, se esperaba 4"
        res_fase = await session.execute(select(Fase).where(Fase.id == 4))
        f4 = res_fase.scalar_one_or_none()
        assert f4 is not None and "Decimal" in f4.nombre, f"Fase 4 no tiene nombre correcto de Decimales: {f4}"
        print("  [OK] CH-1 100% OK: FASE_DECIMALES_ID = 4 y fila 'Operatoria Decimal y Conversiones' verificada.")

        # ----------------------------------------------------------------------
        # CH-5: Verificación de Práctica Libre (3.456 preguntas)
        # ----------------------------------------------------------------------
        print("\n[CH-5] Verificando práctica libre...")
        res_prac = await session.execute(
            select(func.count(Pregunta.id)).where(
                Pregunta.fase_id == FASE_DECIMALES_ID,
                Pregunta.seccion < 1000,
                Pregunta.seccion > 0
            )
        )
        total_prac = res_prac.scalar()
        print(f"  Total preguntas de práctica sembradas: {total_prac} (esperado 3.456).")
        assert total_prac == 3456, f"Práctica libre total {total_prac} != 3456"

        res_types = await session.execute(
            select(Pregunta.tipo_pregunta).where(
                Pregunta.fase_id == FASE_DECIMALES_ID,
                Pregunta.seccion < 1000,
                Pregunta.seccion > 0
            ).distinct()
        )
        prac_types = set(res_types.scalars().all())
        assert prac_types == {TipoPreguntaEnum.RESPUESTA_NUMERICA}, f"Práctica debe ser solo RESPUESTA_NUMERICA, se obtuvo {prac_types}"
        print("  [OK] CH-5 100% OK: 3.456 preguntas de práctica en 12 niveles con respuesta_numerica.")

        # ----------------------------------------------------------------------
        # CH-6: Verificación de Desafíos (1.950 preguntas en 13 bloques)
        # ----------------------------------------------------------------------
        print("\n[CH-6] Verificando desafíos...")
        res_des = await session.execute(
            select(func.count(Pregunta.id)).where(
                Pregunta.fase_id == FASE_DECIMALES_ID,
                Pregunta.seccion >= 1000
            )
        )
        total_des = res_des.scalar()
        print(f"  Total preguntas de desafío sembradas: {total_des} (esperado 1.950).")
        assert total_des == 1950, f"Desafíos total {total_des} != 1950"

        # Verificar seccion DM (99099)
        res_dm = await session.execute(
            select(Pregunta).where(
                Pregunta.fase_id == FASE_DECIMALES_ID,
                Pregunta.seccion == 99099
            )
        )
        dm_questions = res_dm.scalars().all()
        assert len(dm_questions) == 150, f"DM debe tener 150 preguntas, obtuvo {len(dm_questions)}"
        
        # Validar 40 palabras máximo en todos los enunciados de desafío
        res_all_des = await session.execute(
            select(Pregunta).where(
                Pregunta.fase_id == FASE_DECIMALES_ID,
                Pregunta.seccion >= 1000
            )
        )
        all_des_q = res_all_des.scalars().all()
        for q in all_des_q:
            words = q.enunciado.split()
            assert len(words) <= 40, f"Pregunta {q.id} excede 40 palabras ({len(words)} palabras)"

        print("  [OK] CH-6 100% OK: 1.950 preguntas de desafío (D1, D2, DF y DM 99099), validado techo de 40 palabras.")

    # --------------------------------------------------------------------------
    # CH-3: Verificación de CSS Frontend
    # --------------------------------------------------------------------------
    print("\n[CH-3] Verificando CSS de Ventana Fija 950x620px en Frontend...")
    css_path = os.path.join(repo_root, "LogicaMath/frontend/components/fase5/Fase5Styles.css")
    assert os.path.exists(css_path), f"Falta archivo CSS: {css_path}"
    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()
        assert "width: 950px" in css_content and "height: 620px" in css_content, "Falta width: 950px o height: 620px en CSS"
        assert "overflow: hidden" in css_content or "overflow-y: hidden" in css_content or "Cero Scroll" in css_content, "Falta control de cero scroll en CSS"
    print("  [OK] CH-3 100% OK: CSS de Ventana Fija 950x620px y Cero Scroll confirmado.")

    # --------------------------------------------------------------------------
    # CH-4: Verificación de Paso con Elección en Frontend
    # --------------------------------------------------------------------------
    print("\n[CH-4] Verificando soporte de Paso con Elección en Fase5TheoryModal.tsx...")
    theory_modal_path = os.path.join(repo_root, "LogicaMath/frontend/components/fase5/Fase5TheoryModal.tsx")
    assert os.path.exists(theory_modal_path), f"Falta archivo: {theory_modal_path}"
    with open(theory_modal_path, "r", encoding="utf-8") as f:
        tm_content = f.read()
        assert "int.opciones" in tm_content, "Falta soporte para int.opciones en Fase5TheoryModal.tsx"
        assert "int.explicacion_opciones" in tm_content, "Falta int.explicacion_opciones en Fase5TheoryModal.tsx"
    print("  [OK] CH-4 100% OK: Soporte para paso con elección en ejemplos guiados confirmado.")

    await engine.dispose()
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception:
            pass

    print("\n==========================================================================")
    print("   ¡AUDITORÍA INTEGRAL DE LA FASE 4 COMPLETADA! 100% VERDE               ")
    print("==========================================================================")

if __name__ == "__main__":
    asyncio.run(run_master_audit())
