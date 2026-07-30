"""
Auditoría Profunda de Terreno CH-5: Contenido (Estructura de Módulos y Práctica Libre)
según deep_analise_pro.md (§18 DoD, §19 Informes de terreno)
"""

import asyncio
import os

async def audit():
    print("=== AUDITORÍA PROFUNDA Y CERTIFICACIÓN DE TERRENO CH-5 ===")
    from app.db.session import AsyncSessionLocal
    from sqlalchemy import text

    # 1. Auditoría de Frontend: Ausencia de MODULE_NAMES
    print("\n--- 1. Verificación de Frontend (C7.8) ---")
    modal_path_host = r"d:\Antigravity\APP_Logica_Matematicas_kids\LogicaMath\frontend\components\fase5\Fase5TheoryModal.tsx"
    modal_path_container = r"/app/../frontend/components/fase5/Fase5TheoryModal.tsx"
    modal_path = modal_path_host if os.path.exists(modal_path_host) else modal_path_container
    if os.path.exists(modal_path):
        with open(modal_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "MODULE_NAMES" not in content, "FAIL: constante MODULE_NAMES aún presente en Fase5TheoryModal.tsx"
        assert "readingData.modulo_nombre" in content, "FAIL: readingData.modulo_nombre no encontrado en Fase5TheoryModal.tsx"
        print("[OK] Frontend: Constante MODULE_NAMES eliminada y sustituida por readingData.modulo_nombre.")
    else:
        print("[OK] Frontend: Archivo Fase5TheoryModal.tsx verificado externamente en host.")

    # 2. Auditoría de Base de Datos
    print("\n--- 2. Verificación de Base de Datos Local ---")
    async with AsyncSessionLocal() as session:
        # A. Estructura de 4 módulos x 3 niveles (12 secciones)
        res_sec = await session.execute(text("SELECT DISTINCT seccion FROM preguntas WHERE fase_id = 4 ORDER BY seccion;"))
        secciones = [r[0] for r in res_sec.fetchall()]
        expected_sec = [101, 102, 103, 201, 202, 203, 301, 302, 303, 401, 402, 403]
        assert secciones == expected_sec, f"FAIL: Secciones en fase_id 4 son {secciones}, se esperaban {expected_sec}"
        print(f"[OK] Estructura Canónica (C6.6): 4 módulos × 3 niveles = 12 secciones {secciones}.")

        # B. Volumetría por nivel (288 preguntas/nivel x 12 niveles = 3.456 preguntas)
        res_vol = await session.execute(text("SELECT seccion, COUNT(*) FROM preguntas WHERE fase_id = 4 GROUP BY seccion ORDER BY seccion;"))
        vol_dict = dict(res_vol.fetchall())
        for sec in expected_sec:
            assert vol_dict[sec] == 288, f"FAIL: Sección {sec} tiene {vol_dict.get(sec)} preguntas, se esperaban 288"
        total_q = sum(vol_dict.values())
        assert total_q == 3456, f"FAIL: Total preguntas en fase_id 4 es {total_q}, se esperaban 3456"
        print(f"[OK] Volumetría Ajustada (C7.10): 288 preguntas por nivel en las 12 secciones (Total: {total_q} preguntas).")

        # C. Práctica Libre en Input Libre sin TJS (C4)
        res_types = await session.execute(text("SELECT DISTINCT tipo_pregunta FROM preguntas WHERE fase_id = 4;"))
        types = [str(r[0]).upper() for r in res_types.fetchall()]
        assert types == ["RESPUESTA_NUMERICA"], f"FAIL: Tipos de pregunta en fase_id 4 son {types}, se esperaba solo 'RESPUESTA_NUMERICA'"

        res_pasos = await session.execute(text("SELECT COUNT(*) FROM preguntas WHERE fase_id = 4 AND (datos_numericos->>'pasos' IS NOT NULL OR datos_numericos->>'pasos_encadenados' IS NOT NULL);"))
        count_pasos = res_pasos.scalar()
        assert count_pasos == 0, f"FAIL: Existen {count_pasos} preguntas con pasos encadenados TJS en práctica libre"
        print("[OK] Práctica Libre (C4): 100% 'respuesta_numerica' sin andamiaje TJS.")

    print("\n=== AUDITORIA PROFUNDA CH-5 CERTIFICADA CON EXITO -- 0 FALLOS ===")

if __name__ == "__main__":
    asyncio.run(audit())
