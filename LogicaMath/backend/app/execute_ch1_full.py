"""
Script Maestro de Ejecución y Verificación de Terreno CH-1: Fundación de Datos (Intercambio 4 ↔ 5 y Saneamiento)
"""

import asyncio
import sys
import os

async def run_ch1():
    print("=== INICIANDO EJECUCIÓN Y PRUEBA DE TERRENO CH-1 ===")
    from app.db.session import AsyncSessionLocal
    from sqlalchemy import text

    async with AsyncSessionLocal() as session:
        try:
            print("\n[PASO 0.1 y 0.3] Verificando respaldo e inventario inicial...")
            res_before = await session.execute(text("SELECT id, nombre FROM fases ORDER BY id;"))
            fases_before = {r[0]: r[1] for r in res_before.fetchall()}
            print(f"Estado inicial de fases: {fases_before}")
            assert fases_before[4] == "Fracciones, Porcentajes y Proporciones", "FAIL: fase_id 4 inicial no es Fracciones"
            assert fases_before[5] == "Operatoria Decimal y Conversiones", "FAIL: fase_id 5 inicial no es Decimales"

            # -------------------------------------------------------------------------
            # PASO 0.2: Reubicar capacidad (-> fase_id 7) y superficie (-> fase_id 6) en Decimales PRE-swap (fase_id 5)
            # -------------------------------------------------------------------------
            print("\n[PASO 0.2] Reubicando capacidad (-> fase_id 7) y superficie (-> fase_id 6) en fase_id 5 (Decimales PRE-swap)...")
            
            # Reubicar preguntas de capacidad (dm³, L, mL)
            res_cap = await session.execute(text("""
                UPDATE preguntas 
                SET fase_id = 7, seccion = 90, sub_nivel = 1, estado = 'inactivo'
                WHERE fase_id = 5 AND (
                    LOWER(enunciado) LIKE '%litro%' OR LOWER(enunciado) LIKE '%mililitro%' OR LOWER(enunciado) LIKE '%dm³%' OR LOWER(enunciado) LIKE '%capacidad%'
                ) RETURNING id;
            """))
            cap_ids = res_cap.fetchall()
            print(f"  Preguntas de capacidad reubicadas a fase_id 7 (Geometría 3D): {len(cap_ids)}")

            # Reubicar preguntas de superficie (m², cm², hectáreas)
            res_sup = await session.execute(text("""
                UPDATE preguntas 
                SET fase_id = 6, seccion = 90, sub_nivel = 1, estado = 'inactivo'
                WHERE fase_id = 6 AND (
                    LOWER(enunciado) LIKE '%m²%' OR LOWER(enunciado) LIKE '%cm²%' OR LOWER(enunciado) LIKE '%hectárea%' OR LOWER(enunciado) LIKE '%superficie%'
                ) RETURNING id;
            """))
            sup_ids = res_sup.fetchall()
            print(f"  Preguntas de superficie reubicadas a fase_id 6 (Geometría Plana): {len(sup_ids)}")

            # -------------------------------------------------------------------------
            # PASO 3.2: Renumeración Atómica id 4 ↔ 5 mediante id temporal 904
            # -------------------------------------------------------------------------
            print("\n[PASO 3.2] Ejecutando renumeración de fase_id 4 ↔ 5 vía id temporal 904...")
            
            tablas_con_fase = [
                "alumnos", "configuracion_progreso", "preguntas", 
                "pool_asignado_alumno", "progreso_maestria", "intentos", 
                "niveles_teoria_pool", "simulado_sessions"
            ]

            # 1. Insertar fila temporal en la tabla padre fases
            await session.execute(text("INSERT INTO fases (id, nombre, descripcion, orden) VALUES (904, 'Temporal Swap', 'Temporal', 904);"))

            # 2. Mover fase_id 4 -> 904 en tablas hijas
            for tbl in tablas_con_fase:
                if tbl == "alumnos":
                    await session.execute(text(f"UPDATE {tbl} SET fase_actual_id = 904 WHERE fase_actual_id = 4;"))
                else:
                    await session.execute(text(f"UPDATE {tbl} SET fase_id = 904 WHERE fase_id = 4;"))

            # 3. Mover fase_id 5 -> 4 en tablas hijas y actualizar padre
            for tbl in tablas_con_fase:
                if tbl == "alumnos":
                    await session.execute(text(f"UPDATE {tbl} SET fase_actual_id = 4 WHERE fase_actual_id = 5;"))
                else:
                    await session.execute(text(f"UPDATE {tbl} SET fase_id = 4 WHERE fase_id = 5;"))
            await session.execute(text("UPDATE fases SET nombre = 'Operatoria Decimal y Conversiones' WHERE id = 4;"))

            # 4. Mover fase_id 904 -> 5 en tablas hijas y actualizar padre
            for tbl in tablas_con_fase:
                if tbl == "alumnos":
                    await session.execute(text(f"UPDATE {tbl} SET fase_actual_id = 5 WHERE fase_actual_id = 904;"))
                else:
                    await session.execute(text(f"UPDATE {tbl} SET fase_id = 5 WHERE fase_id = 904;"))
            await session.execute(text("UPDATE fases SET nombre = 'Fracciones, Porcentajes y Proporciones' WHERE id = 5;"))

            # 5. Borrar la fila temporal 904
            await session.execute(text("DELETE FROM fases WHERE id = 904;"))

            print("  Swap de clave primaria 4 ↔ 5 completado en transacción.")

            # -------------------------------------------------------------------------
            # PASO 3.4: Verificación de Sanidad
            # -------------------------------------------------------------------------
            print("\n[PASO 3.4] Ejecutando verificación de sanidad...")
            res_after = await session.execute(text("SELECT id, nombre FROM fases WHERE id IN (4, 5) ORDER BY id;"))
            fases_after = {r[0]: r[1] for r in res_after.fetchall()}
            print(f"Estado tras swap: {fases_after}")
            assert fases_after[4] == "Operatoria Decimal y Conversiones", "FAIL: fase_id 4 tras swap no es Decimales!"
            assert fases_after[5] == "Fracciones, Porcentajes y Proporciones", "FAIL: fase_id 5 tras swap no es Fracciones!"
            print("[OK] PASO 3.4 SANIDAD EXITOSA: id 4 es Decimales y id 5 es Fracciones.")

            # -------------------------------------------------------------------------
            # PASO 3.6: Resetear progreso (T1) en fase_id 4 (Decimales, POST-swap) en adelante
            # -------------------------------------------------------------------------
            print("\n[PASO 3.6] Reseteando progreso (T1) en fase_id >= 4...")
            await session.execute(text("DELETE FROM intentos WHERE fase_id >= 4;"))
            await session.execute(text("DELETE FROM pool_asignado_alumno WHERE fase_id >= 4;"))
            await session.execute(text("DELETE FROM progreso_maestria WHERE fase_id >= 4;"))
            print("  Progreso de alumnos reseteado para fase_id >= 4.")

            # -------------------------------------------------------------------------
            # PASO 3.8: Barrido real (C9) sobre fase_id 4 (Decimales, POST-swap)
            # -------------------------------------------------------------------------
            print("\n[PASO 3.8] Barrido real (C9) sobre fase_id 4 (Decimales, POST-swap)...")
            
            # Borrar alternativas de preguntas de fase 4
            await session.execute(text("""
                DELETE FROM alternativas 
                WHERE pregunta_id IN (SELECT id FROM preguntas WHERE fase_id = 4);
            """))
            # Borrar preguntas de fase 4
            res_del_p = await session.execute(text("DELETE FROM preguntas WHERE fase_id = 4 RETURNING id;"))
            del_p_count = len(res_del_p.fetchall())
            print(f"  Preguntas de fase_id 4 eliminadas: {del_p_count}")

            # Borrar teoria de fase 4
            await session.execute(text("DELETE FROM niveles_teoria_pool WHERE fase_id = 4;"))

            # -------------------------------------------------------------------------
            # PASO 3.9: Reubicar Escalas de mapas a fase_id 5 (Fracciones/Proporciones POST-swap)
            # -------------------------------------------------------------------------
            print("\n[PASO 3.9] Reubicando 'Escalas de mapas' a fase_id 5 (Fracciones/Proporciones POST-swap)...")
            res_esc = await session.execute(text("""
                UPDATE preguntas 
                SET fase_id = 5, seccion = 90, sub_nivel = 1, estado = 'inactivo'
                WHERE fase_id = 5 AND (
                    LOWER(enunciado) LIKE '%escala%' OR LOWER(enunciado) LIKE '%mapa%'
                ) RETURNING id;
            """))
            esc_count = len(res_esc.fetchall())
            print(f"  Preguntas de escalas marcadas/reubicadas en fase_id 5: {esc_count}")

            await session.commit()
            print("\n=== COMMIT TRANSACCIONAL CH-1 EXITOSO EN TERRENO ===")

        except Exception as e:
            await session.rollback()
            print(f"\n[ERROR EN CH-1] ROLLBACK EJECUTADO: {e}")
            raise e

if __name__ == "__main__":
    asyncio.run(run_ch1())
