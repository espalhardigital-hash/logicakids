"""
Auditoría Profunda de Terreno CH-1: Fundación de Datos (Intercambio y Saneamiento)
según deep_analise_pro.md (§18 DoD, §19 Informes de terreno)
"""

import asyncio
import sys
import os
import re

async def audit():
    print("=== AUDITORÍA PROFUNDA Y CERTIFICACIÓN DE TERRENO CH-1 ===")
    from app.db.session import AsyncSessionLocal
    from sqlalchemy import text

    base_dir = r"/app/app"

    # 1. Auditoría de Código y Constantes (Backend)
    print("\n--- 1. Verificación de Constantes de Backend ---")
    files_to_check = [
        (os.path.join(base_dir, "fase5", "seed.py"), "FASE_DECIMALES_ID = 4"),
        (os.path.join(base_dir, "fase5", "router.py"), "FASE_DECIMALES_ID = 4"),
        (os.path.join(base_dir, "fase5", "analyze_database.py"), "FASE_DECIMALES_ID = 4"),
    ]
    for filepath, expected in files_to_check:
        assert os.path.exists(filepath), f"FAIL: {filepath} no existe"
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()
        assert expected in code, f"FAIL: {expected} no encontrado en {filepath}"
        assert "FASE5_ID = 5" not in code, f"FAIL: FASE5_ID = 5 aún presente en {filepath}"
        print(f"[OK] {os.path.basename(filepath)}: Constante FASE_DECIMALES_ID = 4 verificada.")

    # 2. Auditoría de Base de Datos
    print("\n--- 2. Verificación de Base de Datos Local ---")
    async with AsyncSessionLocal() as session:
        # A. Sanidad de IDs de Fase (swap 4 <-> 5)
        res_fases = await session.execute(text("SELECT id, nombre FROM fases WHERE id IN (4, 5) ORDER BY id;"))
        fases_dict = dict(res_fases.fetchall())
        assert fases_dict.get(4) == "Operatoria Decimal y Conversiones", f"FAIL: fase_id 4 es {fases_dict.get(4)}"
        assert fases_dict.get(5) == "Fracciones, Porcentajes y Proporciones", f"FAIL: fase_id 5 es {fases_dict.get(5)}"
        print("[OK] Sanidad de BD: fase_id 4 = Operatoria Decimal y Conversiones, fase_id 5 = Fracciones, Porcentajes y Proporciones.")

        # B. Integridad de Fases 1 a 3 (Intactas)
        res_f13 = await session.execute(text("SELECT fase_id, COUNT(*) FROM preguntas WHERE fase_id IN (1, 2, 3) GROUP BY fase_id ORDER BY fase_id;"))
        f13_counts = dict(res_f13.fetchall())
        assert f13_counts[1] == 400, f"FAIL: fase_id 1 cambió a {f13_counts.get(1)}"
        assert f13_counts[2] == 8470, f"FAIL: fase_id 2 cambió a {f13_counts.get(2)}"
        assert f13_counts[3] == 9600, f"FAIL: fase_id 3 cambió a {f13_counts.get(3)}"
        print(f"[OK] Integridad de Fases 1-3: F1={f13_counts[1]}, F2={f13_counts[2]}, F3={f13_counts[3]} (intactas).")

        # C. Barrido de fase_id 4 (Decimales POST-swap)
        res_f4 = await session.execute(text("SELECT COUNT(*) FROM preguntas WHERE fase_id = 4;"))
        count_f4 = res_f4.scalar()
        assert count_f4 == 0, f"FAIL: fase_id 4 tiene {count_f4} preguntas residuo"
        print("[OK] Saneamiento: fase_id 4 (Decimales POST-swap) vaciada completamente (0 preguntas residuo).")

        # D. Módulos aparcados (Geometría Plana f6 y Espacial f7)
        res_p6 = await session.execute(text("SELECT COUNT(*) FROM preguntas WHERE fase_id = 6 AND seccion = 90;"))
        res_p7 = await session.execute(text("SELECT COUNT(*) FROM preguntas WHERE fase_id = 7 AND seccion = 90;"))
        count_p6 = res_p6.scalar()
        count_p7 = res_p7.scalar()
        assert count_p6 == 480, f"FAIL: Superficie aparcada en f6 es {count_p6}"
        assert count_p7 == 1440, f"FAIL: Capacidad aparcada en f7 es {count_p7}"
        print(f"[OK] Módulos Aparcados: Superficie en fase_id 6 ({count_p6} preg), Capacidad en fase_id 7 ({count_p7} preg).")

        # E. Reseteo de Progreso en fase_id >= 4
        res_prog = await session.execute(text("SELECT COUNT(*) FROM intentos WHERE fase_id >= 4;"))
        count_prog = res_prog.scalar()
        assert count_prog == 0, f"FAIL: Intentos en fase_id >= 4 es {count_prog}"
        print("[OK] Progreso de Alumnos: Reseteado para fase_id >= 4 (0 intentos).")

    print("\n=== AUDITORIA PROFUNDA CH-1 CERTIFICADA CON EXITO -- 0 FALLOS ===")

if __name__ == "__main__":
    asyncio.run(audit())
