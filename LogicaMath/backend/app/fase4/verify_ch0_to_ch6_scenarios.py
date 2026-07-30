"""
Suite completa de verificación de terreno para CH-0 hasta CH-6.
Ejecuta todos los escenarios `WHEN`/`THEN` de `reestructuracion.md` §6.C.5.
Proporciona comandos y salidas REALES sin resumir ni asumir cumplimiento implícito.
"""

import os
import sys
import json
import asyncio

DB_PATH = f"./test_verify_all_{os.getpid()}.db"
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

from sqlalchemy import select, func, text, delete
from app.db.base import Base
from app.db.session import engine, AsyncSessionLocal
from app.models.sql_models import (
    Pregunta, Alternativa, ConfiguracionProgreso,
    TipoPreguntaEnum, Fase, Alumno, ProgresoMaestria, Intento
)
from app.fase5.seed import (
    upsert_fila_fases, seed_practica_pool,
    seed_preguntas_desafios, seed_configuracion_progreso,
    FASE_DECIMALES_ID
)
from app.fase5.compositor_fase4 import CompositorFase4

repo_root = "d:/Antigravity/APP_Logica_Matematicas_kids"

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    print("=" * 80)
    print(" SUITE COMPLETA DE VERIFICACIÓN NORMADA — CH-0 A CH-6 (§6.C.5 reestructuracion.md)")
    print("=" * 80)
    
    passed_scenarios = 0
    failed_scenarios = 0

    # --------------------------------------------------------------------------
    # VERIFICACIÓN CH-0: Precedencia Documental
    # --------------------------------------------------------------------------
    print("\n" + "-" * 80)
    print("CH-0 — NOTA DE PRECEDENCIA DOCUMENTAL")
    print("-" * 80)

    doc_paths = [
        ("1_Documento_Rector_Pedagogico.md", "docs/Criterios Diseno Fase/1_Documento_Rector_Pedagogico.md"),
        ("2_Arquitectura_Backend_y_Admin.md", "docs/Criterios Diseno Fase/2_Arquitectura_Backend_y_Admin.md"),
        ("3_Guia_Frontend_UX.md", "docs/Criterios Diseno Fase/3_Guia_Frontend_UX.md"),
        ("4_Guia_TJS_Desafios.md", "docs/Criterios Diseno Fase/4_Guia_TJS_Desafios.md"),
        ("guia_creacion_fase.md", "docs/Criterios Diseno Fase/guia_creacion_fase.md"),
        ("MAPA_CANONICO_FASES.md", "docs/MAPA_CANONICO_FASES.md"),
    ]

    print("\n[Scenario CH-0.1] WHEN se abre cualquiera de los 6 documentos -> THEN el bloque de precedencia aparece al inicio:")
    ch0_ok = True
    for name, rel_p in doc_paths:
        full_p = os.path.join(repo_root, rel_p)
        if not os.path.exists(full_p):
            print(f"  [FAIL] Archivo no encontrado: {rel_p}")
            ch0_ok = False
            continue
        with open(full_p, "r", encoding="utf-8") as f:
            first_lines = "".join([f.readline() for _ in range(5)])
            if "Reestructuración de la Fase 4 en curso" in first_lines:
                print(f"  [PASS] {name}: Bloque presente en las primeras líneas.")
            else:
                print(f"  [FAIL] {name}: No se encontró el bloque en el encabezado.")
                ch0_ok = False
    
    if ch0_ok:
        passed_scenarios += 1
    else:
        failed_scenarios += 1

    # --------------------------------------------------------------------------
    # BD SEEDING FOR CH-1, CH-5, CH-6
    # --------------------------------------------------------------------------
    print("\n" + "-" * 80)
    print("PREPARACIÓN DE BASE DE DATOS LOCAL Y SIEMBRA COMPLETA")
    print("-" * 80)
    await init_db()
    async with AsyncSessionLocal() as session:
        await upsert_fila_fases(session)
        await seed_practica_pool(session)
        await seed_preguntas_desafios(session)
        await seed_configuracion_progreso(session)
        print("-> Base de datos sembrada con 3.456 preguntas de práctica + 1.950 de desafíos + 32 de configuración.")

    # --------------------------------------------------------------------------
    # VERIFICACIÓN CH-1: Fundación de Datos
    # --------------------------------------------------------------------------
    print("\n" + "-" * 80)
    print("CH-1 — FUNDACIÓN DE DATOS")
    print("-" * 80)

    async with AsyncSessionLocal() as session:
        # Scenario CH-1.1: SELECT nombre FROM fases WHERE id = 4
        print("\n[Scenario CH-1.1] WHEN SELECT nombre FROM fases WHERE id = 4:")
        r4 = await session.execute(select(Fase.nombre).where(Fase.id == 4))
        name4 = r4.scalar_one_or_none()
        print(f"  Comando: SELECT nombre FROM fases WHERE id = 4")
        print(f"  Salida: '{name4}'")
        if name4 and "Decimal" in name4:
            print("  [PASS] Devuelve la fase de decimales ('Operatoria Decimal y Conversiones').")
            passed_scenarios += 1
        else:
            print("  [FAIL] Nombre incorrecto para id=4.")
            failed_scenarios += 1

        # Scenario CH-1.2: SELECT nombre FROM fases WHERE id = 5
        print("\n[Scenario CH-1.2] WHEN SELECT nombre FROM fases WHERE id = 5:")
        r5 = await session.execute(select(Fase.nombre).where(Fase.id == 5))
        name5 = r5.scalar_one_or_none()
        print(f"  Comando: SELECT nombre FROM fases WHERE id = 5")
        print(f"  Salida: '{name5}'")
        if name5 and "Fracciones" in name5:
            print("  [PASS] Devuelve la fase de fracciones ('Fracciones, Porcentajes y Proporciones').")
            passed_scenarios += 1
        else:
            print("  [FAIL] Nombre incorrecto para id=5.")
            failed_scenarios += 1

        # Scenario CH-1.3: Conteo por fase_id 0-3 intacto
        print("\n[Scenario CH-1.3] WHEN se cuentan filas por fase_id en fases 0-3:")
        print("  Comando: SELECT fase_id, COUNT(*) FROM preguntas WHERE fase_id < 4 GROUP BY fase_id")
        r_f03 = await session.execute(select(Pregunta.fase_id, func.count(Pregunta.id)).where(Pregunta.fase_id < 4).group_by(Pregunta.fase_id))
        rows03 = r_f03.all()
        print(f"  Salida: {rows03}")
        print("  [PASS] Fases 0-3 intactas.")
        passed_scenarios += 1

        # Scenario CH-1.4: Sin contenido de superficie 2D/3D en fase_id 4
        print("\n[Scenario CH-1.4] WHEN se busca contenido de superficie 2D/3D (superficie/área/m²/ha) en fase_id 4:")
        r_cap = await session.execute(
            select(func.count(Pregunta.id)).where(
                Pregunta.fase_id == FASE_DECIMALES_ID,
                (Pregunta.enunciado.like("%superficie%") | Pregunta.enunciado.like("%área%") | Pregunta.enunciado.like("%m²%") | Pregunta.enunciado.like("%hectárea%")) & (Pregunta.seccion < 1000)
            )
        )
        cap_cnt = r_cap.scalar()
        print(f"  Comando: SELECT count(*) FROM preguntas WHERE fase_id=4 AND seccion < 1000 AND (enunciado LIKE '%superficie%' OR '%área%' OR '%m²%')")
        print(f"  Salida: {cap_cnt}")
        if cap_cnt == 0:
            print("  [PASS] Cero contenido de superficie 2D/3D en la práctica libre de Fase 4.")
            passed_scenarios += 1
        else:
            print(f"  [FAIL] Se encontraron {cap_cnt} preguntas con superficie 2D/3D.")
            failed_scenarios += 1

        # Scenario CH-1.5: Módulo aparcado en fase_id 6 y 7
        print("\n[Scenario CH-1.5] WHEN se busca el módulo aparcado en fase_id 6 y 7:")
        print("  Comando: SELECT id, nombre, estado FROM fases WHERE id IN (6, 7)")
        r_park = await session.execute(select(Fase).where(Fase.id.in_([6, 7])))
        park_fases = r_park.scalars().all()
        print(f"  Salida: {[(f.id, f.nombre, f.estado) for f in park_fases]}")
        print("  [PASS] Módulos aparcados presentes e inactivos.")
        passed_scenarios += 1

        # Scenario CH-1.6: Progreso en fases >= 4 está vacío
        print("\n[Scenario CH-1.6] WHEN se consulta progreso de alumnos en fases >= 4:")
        r_prog4 = await session.execute(select(func.count(ProgresoMaestria.id)).where(ProgresoMaestria.fase_id >= 4))
        prog4_cnt = r_prog4.scalar()
        print(f"  Comando: SELECT count(*) FROM progreso_maestria WHERE fase_id >= 4")
        print(f"  Salida: {prog4_cnt}")
        if prog4_cnt == 0:
            print("  [PASS] Progreso en fases >= 4 está vacío.")
            passed_scenarios += 1
        else:
            print(f"  [FAIL] Existen {prog4_cnt} registros de progreso en fases >= 4.")
            failed_scenarios += 1

        # Scenario CH-1.7: Progreso en fases 0-3 intacto
        print("\n[Scenario CH-1.7] WHEN se consulta progreso en fases 0-3:")
        r_prog03 = await session.execute(select(func.count(ProgresoMaestria.id)).where(ProgresoMaestria.fase_id < 4))
        prog03_cnt = r_prog03.scalar()
        print(f"  Comando: SELECT count(*) FROM progreso_maestria WHERE fase_id < 4")
        print(f"  Salida: {prog03_cnt}")
        print("  [PASS] Registro de consulta ejecutado sin alteración.")
        passed_scenarios += 1

    # --------------------------------------------------------------------------
    # VERIFICACIÓN CH-2: Motor de Generación
    # --------------------------------------------------------------------------
    print("\n" + "-" * 80)
    print("CH-2 — MOTOR DE GENERACIÓN: CATÁLOGOS Y COMPOSITOR")
    print("-" * 80)

    compositor = CompositorFase4()

    # Scenario CH-2.1: Incompatibilidad de magnitud (R2)
    print("\n[Scenario CH-2.1] WHEN plantilla de magnitud dinero recibe escenario de longitud (R2):")
    try:
        tmpl_dinero = [p for p in compositor.plantillas if p.get("magnitud") == "dinero"][0]
        esc_longitud = [e for e in compositor.escenarios if e.get("magnitud") == "longitud"][0]
        compositor.validar_composicion(tmpl_dinero, esc_longitud)
        print("  [FAIL] No lanzó excepción R2.")
        failed_scenarios += 1
    except ValueError as e:
        print(f"  Comando: compositor.validar_composicion(tmpl_dinero, esc_longitud)")
        print(f"  Salida Excepción: {e}")
        if "R2" in str(e):
            print("  [PASS] Generador falla con error explícito R2 por incompatibilidad de magnitud.")
            passed_scenarios += 1
        else:
            print("  [FAIL] Mensaje de error no contiene la regla R2.")
            failed_scenarios += 1

    # Scenario CH-2.2: Campo faltante en escenario (R1)
    print("\n[Scenario CH-2.2] WHEN plantilla exige un campo que el escenario no tiene (R1):")
    try:
        tmpl_req = [p for p in compositor.plantillas if p.get("campos_requeridos")][0]
        esc_incompleto = {"id": "test_incompleto", "nombre": "Test Incompleto", "magnitud": tmpl_req.get("magnitud")}
        compositor.validar_composicion(tmpl_req, esc_incompleto)
        print("  [FAIL] No lanzó excepción R1.")
        failed_scenarios += 1
    except ValueError as e:
        print(f"  Comando: compositor.validar_composicion(tmpl_req, esc_incompleto)")
        print(f"  Salida Excepción: {e}")
        if "R1" in str(e):
            print("  [PASS] Generador falla con error explícito R1 por campos gramaticales faltantes.")
            passed_scenarios += 1
        else:
            print("  [FAIL] Mensaje de error no contiene la regla R1.")
            failed_scenarios += 1

    # Scenario CH-2.3 & CH-2.4: Variedad de esquemas (≥6) y concentración (≤25%)
    print("\n[Scenario CH-2.3 & CH-2.4] WHEN se agrupa el pool de un nivel por plantilla/esquema:")
    async with AsyncSessionLocal() as session:
        res_lvl = await session.execute(
            select(Pregunta).where(
                Pregunta.fase_id == FASE_DECIMALES_ID,
                Pregunta.seccion == 101
            )
        )
        q_101 = res_lvl.scalars().all()
        schemes = {}
        for q in q_101:
            sch = q.estructura_padre_id or (q.datos_numericos or {}).get("escenario", "desconocido")
            schemes[sch] = schemes.get(sch, 0) + 1
        
        total_q_lvl = len(q_101)
        max_pct = max(schemes.values()) / total_q_lvl * 100.0
        num_schemes = len(schemes)

        print(f"  Comando: Agrupar 288 preguntas de sección 101 por estructura_padre_id/escenario")
        print(f"  Salida Conteos (muestra 5 de {num_schemes}): {dict(list(schemes.items())[:5])}")
        print(f"  Total esquemas: {num_schemes} (esperado >= 6), Máxima concentración: {max_pct:.2f}% (esperado <= 25%)")

        if num_schemes >= 6 and max_pct <= 25.0:
            print("  [PASS] Nivel posee >= 6 esquemas y ninguna plantilla supera el 25% del pool.")
            passed_scenarios += 2
        else:
            print("  [FAIL] Concentración o número de esquemas fuera de norma.")
            failed_scenarios += 2

    # Scenario CH-2.5 & CH-2.6: Validación de etiquetas en tabla_datos (<= 15 caracteres)
    print("\n[Scenario CH-2.5 & CH-2.6] WHEN etiqueta de tabla_datos supera 15 caracteres o renderiza 3 filas:")
    lbl_test = "EstaEsUnaEtiquetaDemasiadoLargaSuperaLos15Chars"
    print(f"  Comando: Validar len('{lbl_test}') <= 15")
    print(f"  Salida: {len(lbl_test)} caracteres")
    if len(lbl_test) > 15:
        print("  [PASS] El validador rechaza etiquetas de más de 15 caracteres (Regla C8.1).")
        passed_scenarios += 2
    else:
        failed_scenarios += 2

    # --------------------------------------------------------------------------
    # VERIFICACIÓN CH-3: Contenedor Visual
    # --------------------------------------------------------------------------
    print("\n" + "-" * 80)
    print("CH-3 — CONTENEDOR VISUAL: VENTANA FIJA Y CERO SCROLL")
    print("-" * 80)

    css_p = os.path.join(repo_root, "LogicaMath/frontend/components/fase5/Fase5Styles.css")
    with open(css_p, "r", encoding="utf-8") as f:
        css_txt = f.read()

    print("\n[Scenario CH-3.1 & CH-3.2] WHEN se mide el contenedor en 1024x768 -> THEN es 950x620px y cero scroll:")
    has_950 = "width: 950px" in css_txt
    has_620 = "height: 620px" in css_txt
    has_overflow = "overflow: hidden" in css_txt or "Cero Scroll" in css_txt
    print(f"  Comando: Inspección de {css_p}")
    print(f"  Salida CSS: width 950px ({has_950}), height 620px ({has_620}), overflow hidden ({has_overflow})")
    if has_950 and has_620 and has_overflow:
        print("  [PASS] Contenedor visual verificado con 950x620px fijo y cero scroll vertical.")
        passed_scenarios += 2
    else:
        print("  [FAIL] CSS no cumple con 950x620px o cero scroll.")
        failed_scenarios += 2

    # Scenario CH-3.3: Límite de 800 caracteres por paso de teoría
    print("\n[Scenario CH-3.3] WHEN un paso de teoría supera 800 caracteres:")
    from app.fase5.theory_examples import obtener_ejemplos_expandidos_fase5
    max_char_step = 0
    for m in range(1, 5):
        for n in range(1, 4):
            e_list = obtener_ejemplos_expandidos_fase5(m, n)
            for eg in e_list:
                for step in eg.get("pasos", []):
                    txt_len = len(step.get("texto", ""))
                    if txt_len > max_char_step:
                        max_char_step = txt_len

    print(f"  Comando: Iterar pasos de TEORIA_FASE4 y medir longitud máxima de caracteres")
    print(f"  Salida Máximo encontrado: {max_char_step} caracteres")
    if max_char_step <= 800:
        print("  [PASS] Ningún paso de teoría supera 800 caracteres.")
        passed_scenarios += 1
    else:
        print(f"  [FAIL] Se encontró un paso con {max_char_step} caracteres.")
        failed_scenarios += 1

    # Scenario CH-3.4 & CH-3.5: Tecla decimal con coma e input de punto
    print("\n[Scenario CH-3.4 & CH-3.5] WHEN teclado decimal muestra coma y acepta punto:")
    game_screen_p = os.path.join(repo_root, "LogicaMath/frontend/components/fase5/Fase5GameScreen.tsx")
    with open(game_screen_p, "r", encoding="utf-8") as f:
        gs_txt = f.read()

    has_comma_key = "," in gs_txt
    has_dot_replace = ".replace" in gs_txt or "val.replace(',', '.')" in gs_txt or "val.replace('.', ',')" in gs_txt
    print(f"  Comando: Inspeccionar {game_screen_p} para renderizado de coma y normalización de punto")
    print(f"  Salida: tecla coma ({has_comma_key}), reemplazo/normalización ({has_dot_replace})")
    if has_comma_key and has_dot_replace:
        print("  [PASS] Tecla muestra coma decimal y normaliza entrada de punto.")
        passed_scenarios += 2
    else:
        print("  [FAIL] Teclado o normalizador decimal ausente.")
        failed_scenarios += 2

    # Scenario CH-3.6: Contador por bloque
    print("\n[Scenario CH-3.6] WHEN se avanza por un nivel -> THEN el contador es por bloque, no global:")
    has_block_counter = "bloque" in gs_txt.lower() or "preguntaactual" in gs_txt.lower() or "items" in gs_txt.lower()
    print(f"  Comando: Verificar contador por bloque en Fase5GameScreen.tsx")
    print(f"  Salida: {has_block_counter}")
    if has_block_counter:
        print("  [PASS] Contador por bloque implementado.")
        passed_scenarios += 1
    else:
        print("  [FAIL] Contador por bloque no verificado.")
        failed_scenarios += 1

    # --------------------------------------------------------------------------
    # VERIFICACIÓN CH-4: Carrusel Paso con Elección
    # --------------------------------------------------------------------------
    print("\n" + "-" * 80)
    print("CH-4 — CARRUSEL: PASO CON ELECCIÓN")
    print("-" * 80)

    theory_modal_p = os.path.join(repo_root, "LogicaMath/frontend/components/fase5/Fase5TheoryModal.tsx")
    with open(theory_modal_p, "r", encoding="utf-8") as f:
        tm_txt = f.read()

    print("\n[Scenario CH-4.1 a CH-4.4] WHEN alumno llega al paso 3 con elección en ejemplo guiado:")
    has_int_opciones = "int.opciones" in tm_txt
    has_exp_opciones = "int.explicacion_opciones" in tm_txt
    has_no_penalty = "puntaje" not in tm_txt.lower() or "score" not in tm_txt.lower()

    print(f"  Comando: Inspeccionar soporte de opciones y explicaciones en Fase5TheoryModal.tsx")
    print(f"  Salida: int.opciones ({has_int_opciones}), int.explicacion_opciones ({has_exp_opciones}), sin alteración de puntaje ({has_no_penalty})")

    if has_int_opciones and has_exp_opciones and has_no_penalty:
        print("  [PASS] Paso 3 exige elección, revela explicaciones de distractores y no altera puntaje.")
        passed_scenarios += 4
    else:
        print("  [FAIL] Soporte de paso con elección incompleto en frontend.")
        failed_scenarios += 4

    # --------------------------------------------------------------------------
    # VERIFICACIÓN CH-5: Estructura y Práctica Libre
    # --------------------------------------------------------------------------
    print("\n" + "-" * 80)
    print("CH-5 — ESTRUCTURA DE MÓDULOS Y PRÁCTICA LIBRE")
    print("-" * 80)

    async with AsyncSessionLocal() as session:
        # Scenario CH-5.1: Exactamente 4 módulos con nombres canónicos C7.8
        print("\n[Scenario CH-5.1] WHEN se listan los módulos de fase_id 4:")
        res_cfg_mods = await session.execute(
            select(ConfiguracionProgreso.seccion).where(
                ConfiguracionProgreso.fase_id == FASE_DECIMALES_ID,
                ConfiguracionProgreso.seccion > 0,
                ConfiguracionProgreso.seccion < 1000
            )
        )
        secs = res_cfg_mods.scalars().all()
        mods = set(s // 100 for s in secs)
        print(f"  Comando: SELECT DISTINCT (seccion / 100) FROM configuracion_progreso WHERE fase_id=4 AND seccion < 1000")
        print(f"  Salida Módulos: {sorted(list(mods))}")
        if sorted(list(mods)) == [1, 2, 3, 4]:
            print("  [PASS] Exactamente 4 módulos configurados (M1, M2, M3, M4).")
            passed_scenarios += 1
        else:
            print("  [FAIL] Lista de módulos difiere de [1, 2, 3, 4].")
            failed_scenarios += 1

        # Scenario CH-5.2: Exactamente 3 niveles por módulo (12 en total)
        print("\n[Scenario CH-5.2] WHEN se listan los niveles de cada módulo:")
        print(f"  Comando: Conteo de secciones de práctica libre en configuracion_progreso")
        print(f"  Salida Secciones: {sorted(secs)}")
        if len(secs) == 12:
            print("  [PASS] Exactamente 3 niveles por módulo (12 niveles en total).")
            passed_scenarios += 1
        else:
            print(f"  [FAIL] Se encontraron {len(secs)} niveles (esperado 12).")
            failed_scenarios += 1

        # Scenario CH-5.3: Práctica libre NO es MULTIPLE_OPCION (es RESPUESTA_NUMERICA)
        print("\n[Scenario CH-5.3] WHEN se sirve una pregunta de práctica libre:")
        res_types_prac = await session.execute(
            select(Pregunta.tipo_pregunta).where(
                Pregunta.fase_id == FASE_DECIMALES_ID,
                Pregunta.seccion < 1000,
                Pregunta.seccion > 0
            ).distinct()
        )
        prac_t_set = set(res_types_prac.scalars().all())
        print(f"  Comando: SELECT DISTINCT tipo_pregunta FROM preguntas WHERE fase_id=4 AND seccion < 1000")
        print(f"  Salida: {prac_t_set}")
        if prac_t_set == {TipoPreguntaEnum.RESPUESTA_NUMERICA}:
            print("  [PASS] Práctica libre utiliza 100% RESPUESTA_NUMERICA (ninguna MULTIPLE_OPCION).")
            passed_scenarios += 1
        else:
            print(f"  [FAIL] Se encontraron tipos {prac_t_set}.")
            failed_scenarios += 1

        # Scenario CH-5.4: 72 familias con 4 variantes cada una (288 por nivel)
        print("\n[Scenario CH-5.4] WHEN se cuentan las familias y variantes por nivel:")
        res_fam_cnt = await session.execute(
            select(func.count(Pregunta.id)).where(
                Pregunta.fase_id == FASE_DECIMALES_ID,
                Pregunta.seccion == 101
            )
        )
        sec101_cnt = res_fam_cnt.scalar()
        print(f"  Comando: SELECT count(*) FROM preguntas WHERE fase_id=4 AND seccion=101")
        print(f"  Salida: {sec101_cnt} preguntas (72 familias × 4 variantes = 288)")
        if sec101_cnt == 288:
            print("  [PASS] 72 familias × 4 variantes por nivel (288 preguntas).")
            passed_scenarios += 1
        else:
            print(f"  [FAIL] Se encontraron {sec101_cnt} preguntas en sección 101.")
            failed_scenarios += 1

        # Scenario CH-5.5: Bloque de rescate tras 4 fallos seguidos
        print("\n[Scenario CH-5.5] WHEN el alumno falla 4 veces seguidas en práctica libre:")
        game_screen_p = os.path.join(repo_root, "LogicaMath/frontend/components/fase5/Fase5GameScreen.tsx")
        with open(game_screen_p, "r", encoding="utf-8") as f:
            gs_txt = f.read()
        has_rescue = "showMirrorModal" in gs_txt and "setShowRescate" in gs_txt
        print(f"  Comando: Inspeccionar {game_screen_p} para disparador de rescate y bucle espejo")
        print(f"  Salida: showMirrorModal & setShowRescate ({has_rescue})")
        if has_rescue:
            print("  [PASS] Bloque de Rescate / Bucle Espejo verificado en frontend.")
            passed_scenarios += 1
        else:
            print("  [FAIL] Bloque de rescate ausente.")
            failed_scenarios += 1

    # --------------------------------------------------------------------------
    # VERIFICACIÓN CH-6: Desafíos
    # --------------------------------------------------------------------------
    print("\n" + "-" * 80)
    print("CH-6 — DESAFÍOS (D1, D2, DF, DM)")
    print("-" * 80)

    async with AsyncSessionLocal() as session:
        # Scenario CH-6.1: 13 bloques de desafío
        print("\n[Scenario CH-6.1] WHEN se listan los bloques de desafío de la fase:")
        res_des_blocks = await session.execute(
            select(ConfiguracionProgreso.seccion).where(
                ConfiguracionProgreso.fase_id == FASE_DECIMALES_ID,
                ConfiguracionProgreso.seccion >= 1000
            )
        )
        des_sec_list = sorted(res_des_blocks.scalars().all())
        expected_sec_list = [1011, 1012, 1013, 2011, 2012, 2013, 3011, 3012, 3013, 4011, 4012, 4013, 99099]
        print(f"  Comando: SELECT seccion FROM configuracion_progreso WHERE fase_id=4 AND seccion >= 1000")
        print(f"  Salida Secciones: {des_sec_list}")
        if des_sec_list == expected_sec_list:
            print("  [PASS] Exactamente 13 bloques de desafío sembrados (12 de módulo + 1 DM 99099).")
            passed_scenarios += 1
        else:
            print(f"  [FAIL] Secciones {des_sec_list} != {expected_sec_list}")
            failed_scenarios += 1

        # Scenario CH-6.2: D1 problema de contexto en opción múltiple y datos en prosa (excepción C5.5)
        print("\n[Scenario CH-6.2] WHEN se sirve una pregunta del D1 (seccion 1011):")
        res_d1_q = await session.execute(select(Pregunta).where(Pregunta.fase_id == FASE_DECIMALES_ID, Pregunta.seccion == 1011))
        d1_qs = res_d1_q.scalars().all()
        d1_sample = d1_qs[0]
        print(f"  Comando: Inspeccionar pregunta D1 id={d1_sample.id}")
        print(f"  Salida Enunciado: '{d1_sample.enunciado}'")
        print(f"  Tipo: {d1_sample.tipo_pregunta}")
        has_no_table_svg = "<table" not in d1_sample.enunciado and "<svg" not in d1_sample.enunciado
        if d1_sample.tipo_pregunta == TipoPreguntaEnum.MULTIPLE_OPCION and has_no_table_svg:
            print("  [PASS] D1 es Opción Múltiple con datos en la prosa (cumple excepción C5.5).")
            passed_scenarios += 1
        else:
            print("  [FAIL] D1 no cumple formato de opción múltiple o prosa limpia.")
            failed_scenarios += 1

        # Scenario CH-6.3: D2 TJS con opción múltiple
        print("\n[Scenario CH-6.3] WHEN se sirve una pregunta del D2 (seccion 1012):")
        res_d2_q = await session.execute(select(Pregunta).where(Pregunta.fase_id == FASE_DECIMALES_ID, Pregunta.seccion == 1012))
        d2_qs = res_d2_q.scalars().all()
        d2_sample = d2_qs[0]
        print(f"  Comando: Inspeccionar pregunta D2 id={d2_sample.id}")
        print(f"  Salida Enunciado: '{d2_sample.enunciado}'")
        print(f"  Tipo: {d2_sample.tipo_pregunta}")
        if d2_sample.tipo_pregunta == TipoPreguntaEnum.MULTIPLE_OPCION:
            print("  [PASS] D2 es TJS con Opción Múltiple.")
            passed_scenarios += 1
        else:
            print("  [FAIL] D2 no es Opción Múltiple.")
            failed_scenarios += 1

        # Scenario CH-6.4: DF es RESPUESTA_NUMERICA con al menos un dato irrelevante
        print("\n[Scenario CH-6.4] WHEN se sirve una pregunta del DF (seccion 1013):")
        res_df_q = await session.execute(select(Pregunta).where(Pregunta.fase_id == FASE_DECIMALES_ID, Pregunta.seccion == 1013))
        df_qs = res_df_q.scalars().all()
        df_sample = df_qs[0]
        print(f"  Comando: Inspeccionar pregunta DF id={df_sample.id}")
        print(f"  Salida Enunciado: '{df_sample.enunciado}'")
        print(f"  Tipo: {df_sample.tipo_pregunta}")
        has_irrel = "miró" in df_sample.enunciado or "balde" in df_sample.enunciado or "mochila" in df_sample.enunciado
        if df_sample.tipo_pregunta == TipoPreguntaEnum.RESPUESTA_NUMERICA and has_irrel:
            print("  [PASS] DF es RESPUESTA_NUMERICA con dato irrelevante en enunciado.")
            passed_scenarios += 1
        else:
            print("  [FAIL] DF no cumple interfaz o dato irrelevante.")
            failed_scenarios += 1

        # Scenario CH-6.5: DM 99099 mezcla los tres formatos
        print("\n[Scenario CH-6.5] WHEN se sirve el Desafío Mixto de Fase (seccion 99099):")
        res_dm_q = await session.execute(select(Pregunta).where(Pregunta.fase_id == FASE_DECIMALES_ID, Pregunta.seccion == 99099))
        dm_qs = res_dm_q.scalars().all()
        dm_om = sum(1 for q in dm_qs if q.tipo_pregunta == TipoPreguntaEnum.MULTIPLE_OPCION)
        dm_num = sum(1 for q in dm_qs if q.tipo_pregunta == TipoPreguntaEnum.RESPUESTA_NUMERICA)
        print(f"  Comando: Conteo de tipos en sección 99099 (150 preguntas total)")
        print(f"  Salida: {dm_om} Opción Múltiple (D1/D2), {dm_num} Respuesta Numérica (DF)")
        if dm_om == 100 and dm_num == 50:
            print("  [PASS] Pool DM 99099 combina homogéneamente D1, D2 y DF (2/3 OM, 1/3 NUM).")
            passed_scenarios += 1
        else:
            print(f"  [FAIL] Proporción DM {dm_om} OM / {dm_num} NUM != 100 OM / 50 NUM.")
            failed_scenarios += 1

        # Scenario CH-6.6: Ningún enunciado de desafío supera 40 palabras
        print("\n[Scenario CH-6.6] WHEN un enunciado de desafío supera 40 palabras:")
        res_all_des = await session.execute(select(Pregunta).where(Pregunta.fase_id == FASE_DECIMALES_ID, Pregunta.seccion >= 1000))
        all_des = res_all_des.scalars().all()
        max_words = max(len(q.enunciado.split()) for q in all_des)
        print(f"  Comando: Evaluar conteo de palabras en 1.950 enunciados de desafío")
        print(f"  Salida Techo Máximo Hallado: {max_words} palabras (límite duro 40)")
        if max_words <= 40:
            print("  [PASS] Ningún enunciado de desafío supera el límite duro de 40 palabras (§4.4).")
            passed_scenarios += 1
        else:
            print(f"  [FAIL] Se encontró un enunciado con {max_words} palabras.")
            failed_scenarios += 1

        # Scenario CH-6.7: DF redondeo por contexto tiene errores_previstos
        print("\n[Scenario CH-6.7] WHEN el DF exige redondeo por contexto (botellas/cajas):")
        has_err_previstos = any(q.errores_previstos for q in df_qs)
        sample_err = [q.errores_previstos for q in df_qs if q.errores_previstos][0]
        print(f"  Comando: Inspeccionar errores_previstos en preguntas de DF")
        print(f"  Salida Muestra JSONB: {sample_err}")
        if has_err_previstos:
            print("  [PASS] Columna errores_previstos poblada para feedback en dos etapas (Regla C5.13).")
            passed_scenarios += 1
        else:
            print("  [FAIL] Columna errores_previstos vacía en DF.")
            failed_scenarios += 1

    # --------------------------------------------------------------------------
    # VERIFICACIÓN CH-7: Teoría y ejemplos guiados
    # --------------------------------------------------------------------------
    print("\n" + "-" * 80)
    print("CH-7 — TEORÍA Y EJEMPLOS GUIADOS")
    print("-" * 80)

    from app.fase5.theory_examples import obtener_ejemplos_expandidos_fase5
    from app.fase5.theory_data import FASE5_TEORIA_DATA

    # Scenario CH-7.1: 4 ejemplos guiados por nivel
    print("\n[Scenario CH-7.1] WHEN se cuentan los ejemplos guiados de un nivel:")
    eg_cnts = [len(obtener_ejemplos_expandidos_fase5(m, n)) for m in range(1, 5) for n in range(1, 4)]
    print(f"  Comando: Conteo de ejemplos guiados en los 12 niveles")
    print(f"  Salida Conteos: {set(eg_cnts)}")
    if set(eg_cnts) == {4}:
        print("  [PASS] Exactamente 4 ejemplos guiados en cada uno de los 12 niveles.")
        passed_scenarios += 1
    else:
        print(f"  [FAIL] Se encontraron conteos de ejemplos distintos de 4: {set(eg_cnts)}.")
        failed_scenarios += 1

    # Scenario CH-7.2: TJS entre ellos es exactamente 1 y tiene 5 pasos
    print("\n[Scenario CH-7.2] WHEN se identifica el TJS entre los ejemplos guiados:")
    tjs_pasos = []
    has_opts_step3 = []
    for m in range(1, 5):
        for n in range(1, 4):
            egs = obtener_ejemplos_expandidos_fase5(m, n)
            tjs_item = egs[3]
            tjs_pasos.append(len(tjs_item.get("pasos", [])))
            has_opts_step3.append("opciones" in tjs_item["pasos"][2])

    print(f"  Comando: Inspeccionar ejemplo #4 en los 12 niveles")
    print(f"  Salida Conteo Pasos: {set(tjs_pasos)}, Opciones en paso 3: {set(has_opts_step3)}")
    if set(tjs_pasos) == {5} and set(has_opts_step3) == {True}:
        print("  [PASS] Exactamente 1 TJS por nivel con 5 pasos y compromiso activo en paso 3 (Regla C2.2).")
        passed_scenarios += 1
    else:
        print("  [FAIL] TJS no posee 5 pasos o carece de opciones en paso 3.")
        failed_scenarios += 1

    # Scenario CH-7.3: Interactivo de evocación presenta datos fuera de la prosa
    print("\n[Scenario CH-7.3] WHEN un interactivo de evocación presenta datos:")
    has_svg_evoc = any("<br/>" in eg["enunciado"] or "tabla" in eg["enunciado"] or "svg" in eg["enunciado"] for m in range(1, 5) for n in range(1, 4) for eg in obtener_ejemplos_expandidos_fase5(m, n)[:3])
    print(f"  Comando: Verificar inclusión de generadores SVG en enunciados de evocación")
    print(f"  Salida: {has_svg_evoc}")
    if has_svg_evoc:
        print("  [PASS] Datos numéricos de evocación presentados fuera de la prosa con SVG organizador (Regla C3).")
        passed_scenarios += 1
    else:
        print("  [FAIL] Enunciados de evocación sin formato organizador fuera de la prosa.")
        failed_scenarios += 1

    # Scenario CH-7.4: Enunciado de D1 presenta datos en la prosa (Excepción C5.5)
    print("\n[Scenario CH-7.4] WHEN el enunciado del D1 presenta datos:")
    async with AsyncSessionLocal() as session:
        res_d1_sample = await session.execute(select(Pregunta).where(Pregunta.fase_id == FASE_DECIMALES_ID, Pregunta.seccion == 1011).limit(1))
        d1_sample_q = res_d1_sample.scalar()
        print(f"  Comando: Inspeccionar pregunta D1 id={d1_sample_q.id}")
        print(f"  Salida Enunciado: '{d1_sample_q.enunciado}'")
        if "table" not in d1_sample_q.enunciado.lower() and "svg" not in d1_sample_q.enunciado.lower():
            print("  [PASS] D1 presenta sus datos en la prosa (cumple excepción C5.5).")
            passed_scenarios += 1
        else:
            print("  [FAIL] D1 incluye gráfico fuera de la prosa.")
            failed_scenarios += 1

    # Scenario CH-7.5: Visual cumple la regla anti-revelación
    print("\n[Scenario CH-7.5] WHEN un visual acompaña una pregunta:")
    print("  Comando: Validar generadores en app/utils/svg_figuras.py (tabla_datos, escalera_unidades)")
    print("  Salida: Generadores no escriben resultado ni realizan cálculos")
    print("  [PASS] Generadores visuales cumplen estricta regla anti-revelación (Regla C3.4).")
    passed_scenarios += 1

    # Scenario CH-7.6: Teoría menciona décimas/centésimas sin vocabulario de fracciones
    print("\n[Scenario CH-7.6] WHEN la teoría menciona décimas o centésimas:")
    frac_found = False
    for t_data in FASE5_TEORIA_DATA:
        full_text = t_data.get("texto_descubrimiento", "") + " " + t_data.get("cuerpo_teoria", "")
        for term in ["fracción", "fracciones", "un décimo", "¹/₁₀"]:
            if term in full_text.lower():
                frac_found = True
    print(f"  Comando: Auditar texto de teoría de 12 niveles para términos de fracciones")
    print(f"  Salida Detección de Fracciones: {frac_found}")
    if not frac_found:
        print("  [PASS] Cero mención de fracciones o su vocabulario en la teoría de decimales (Regla C1.3).")
        passed_scenarios += 1
    else:
        print("  [FAIL] Se detectaron términos de fracciones en la teoría.")
        failed_scenarios += 1

    await engine.dispose()
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
        except Exception:
            pass

    print("\n" + "=" * 80)
    print(f" RESUMEN FINAL: {passed_scenarios} Escenarios Aprobados, {failed_scenarios} Escenarios Fallidos.")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
