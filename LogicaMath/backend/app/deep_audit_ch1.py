"""
Script de Verificación de Terreno y Auditoría Profunda CH-1 (Fundación de Datos)
"""

import asyncio
import sys

async def audit():
    print("=== AUDITORÍA PROFUNDA DE TERRENO CH-1 ===")
    from app.db.session import AsyncSessionLocal
    from sqlalchemy import text

    async with AsyncSessionLocal() as session:
        # Scenario 1 & 2: Sanidad id 4 = Decimales, id 5 = Fracciones
        res_f = await session.execute(text("SELECT id, nombre FROM fases WHERE id IN (4, 5) ORDER BY id;"))
        fases = {r[0]: r[1] for r in res_f.fetchall()}
        assert fases[4] == "Operatoria Decimal y Conversiones", f"FAIL: fase 4 es {fases[4]}"
        assert fases[5] == "Fracciones, Porcentajes y Proporciones", f"FAIL: fase 5 es {fases[5]}"
        print("[OK] Scenario 1 & 2: Sanidad de IDs (fase_id 4 = Decimales, fase_id 5 = Fracciones) confirmada.")

        # Scenario 3: Integridad de fases 0 a 3 (fases 1, 2 y 3 intactas con 400, 8470 y 9600 preguntas)
        res_f03 = await session.execute(text("SELECT fase_id, COUNT(*) FROM preguntas WHERE fase_id IN (1, 2, 3) GROUP BY fase_id ORDER BY fase_id;"))
        counts_f03 = dict(res_f03.fetchall())
        assert counts_f03[1] == 400, f"FAIL: fase 1 tiene {counts_f03.get(1)} preguntas"
        assert counts_f03[2] == 8470, f"FAIL: fase 2 tiene {counts_f03.get(2)} preguntas"
        assert counts_f03[3] == 9600, f"FAIL: fase 3 tiene {counts_f03.get(3)} preguntas"
        print(f"[OK] Scenario 3: Fases 1, 2 y 3 intactas con sus preguntas ({counts_f03}).")

        # Scenario 4: Saneamiento de contenido viejo en Decimales (fase_id 4 POST-swap)
        res_old = await session.execute(text("SELECT COUNT(*) FROM preguntas WHERE fase_id = 4;"))
        count_f4 = res_old.scalar()
        assert count_f4 == 0, f"FAIL: fase_id 4 aún contiene {count_f4} preguntas viejas"
        print("[OK] Scenario 4: Barrido de contenido viejo en fase_id 4 (Decimales POST-swap) verificado (0 preguntas).")

        # Scenario 5: Módulos aparcados en fase 6 (superficie) y fase 7 (capacidad)
        res_parked6 = await session.execute(text("SELECT COUNT(*) FROM preguntas WHERE fase_id = 6 AND seccion = 90;"))
        res_parked7 = await session.execute(text("SELECT COUNT(*) FROM preguntas WHERE fase_id = 7 AND seccion = 90;"))
        p6 = res_parked6.scalar()
        p7 = res_parked7.scalar()
        assert p6 > 0, "FAIL: Módulo aparcado de superficie en fase 6 no existe"
        assert p7 > 0, "FAIL: Módulo aparcado de capacidad en fase 7 no existe"
        print(f"[OK] Scenario 5: Módulos aparcados inactivos creados en fase 6 ({p6} preg) y fase 7 ({p7} preg).")

        # Scenario 7: Reseteo de progreso en fases >= 4
        res_prog = await session.execute(text("SELECT COUNT(*) FROM intentos WHERE fase_id >= 4;"))
        c_prog = res_prog.scalar()
        assert c_prog == 0, f"FAIL: intentos en fase_id >= 4 no está vacío ({c_prog})"
        print("[OK] Scenario 7: Reseteo de progreso de alumnos para fase_id >= 4 verificado (0 intentos).")

        print("\n=== AUDITORIA PROFUNDA CH-1 COMPLETADA CON EXITO -- 0 FALLOS ===")

if __name__ == "__main__":
    asyncio.run(audit())
