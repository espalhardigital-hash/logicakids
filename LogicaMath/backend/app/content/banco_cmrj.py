"""
Banco curado de preguntas REALES del examen CMRJ / Colégio Pedro II.

Origen: fotos del examen (`Pedro II/`), banco transcrito y análisis
`coelgiomilitar.md`. Traducidas al español y **verificadas** (respuesta
recalculada). Cada pregunta lleva `modulo` (a qué módulo de la fase pertenece) y
`nivel`:
  - "simulacro"  → dificultad real del examen (se inyecta como "Desafío
                    Simulacro" en el desafío final del módulo, 1-2 por módulo).
  - "familiariza"→ mismo tema/estructura pero MÁS FÁCIL, para que el alumno se
                    familiarice antes (se inyecta en la práctica del módulo).

`seed_banco_cmrj()` (cableado en el seed maestro) reparte cada pregunta a su
sección. Idempotente. Las figuras usan visualizadores paramétricos (no revelan).
"""

# BANCO_CMRJ[fase_id] = lista de preguntas. Campos:
#   modulo, nivel, tema, enunciado, correcta, distractores[3], explicacion,
#   dificultad(1-3), [tipo_visual, cortes, sombreados, total, val_a, val_b]
BANCO_CMRJ = {
    # ═══════════ FASE 4 · Decimales y Conversiones ═══════════
    4: [
        {"modulo": 1, "nivel": "familiariza", "tema": "Suma de decimales", "enunciado": "En una tienda, Ana pagó R$ 3,50 por un cuaderno y R$ 2,75 por un lápiz. ¿Cuánto pagó en total?",
         "correcta": "R$ 6,25", "distractores": ["R$ 6,15", "R$ 5,25", "R$ 6,35"], "explicacion": "Alinea las comas: 3,50 + 2,75 = 6,25.", "dificultad": 1},
        {"modulo": 1, "nivel": "simulacro", "tema": "Suma multi-unidad", "enunciado": "Mariana recorrió tramos de 8000 cm, luego 220 m y luego 0,15 km. ¿Cuántos metros recorrió en total?",
         "correcta": "450 m", "distractores": ["228,15 m", "8220,15 m", "1050 m"], "explicacion": "8000 cm = 80 m; 0,15 km = 150 m; 80 + 220 + 150 = 450 m.", "dificultad": 3},
        {"modulo": 4, "nivel": "familiariza", "tema": "Conversión simple", "enunciado": "¿Cuántos centímetros hay en 2,5 metros?",
         "correcta": "250 cm", "distractores": ["25 cm", "2500 cm", "205 cm"], "explicacion": "1 m = 100 cm, entonces 2,5 × 100 = 250 cm.", "dificultad": 1},
        {"modulo": 4, "nivel": "simulacro", "tema": "Conversión y suma", "enunciado": "Un cable mide 1,2 m; otro 85 cm; otro 400 mm. ¿Cuál es la longitud total en metros?",
         "correcta": "2,45 m", "distractores": ["2,05 m", "486,2 m", "3,25 m"], "explicacion": "85 cm = 0,85 m; 400 mm = 0,4 m; 1,2 + 0,85 + 0,4 = 2,45 m.", "dificultad": 3},
        {"modulo": 3, "nivel": "simulacro", "tema": "Decimal a fracción irreducible", "enunciado": "Escribe 0,76 como fracción irreducible.",
         "correcta": "19/25", "distractores": ["76/100", "38/50", "19/20"], "explicacion": "0,76 = 76/100; dividiendo entre 4: 19/25.", "dificultad": 3},
    ],
    # ═══════════ FASE 5 · Fracciones, Porcentajes y Proporciones ═══════════
    5: [
        {"modulo": 1, "nivel": "familiariza", "tema": "Leer una fracción", "enunciado": "En un círculo dividido en 8 partes iguales hay 3 sombreadas. ¿Qué fracción representa la parte sombreada?",
         "correcta": "3/8", "distractores": ["5/8", "3/5", "8/3"], "explicacion": "3 partes de 8 = 3/8.", "dificultad": 1, "tipo_visual": "pizza", "cortes": 8, "sombreados": [0, 1, 2]},
        {"modulo": 1, "nivel": "familiariza", "tema": "Suma de fracciones", "enunciado": "Calcula 1/2 + 1/3 reduciendo al mínimo común múltiplo.",
         "correcta": "5/6", "distractores": ["2/5", "1/6", "2/6"], "explicacion": "MCM(2,3)=6; 3/6 + 2/6 = 5/6.", "dificultad": 2},
        {"modulo": 2, "nivel": "familiariza", "tema": "Fracción de una cantidad", "enunciado": "En un concurso se inscribieron 7200 candidatos y aprobaron 5/12. ¿Cuántos aprobaron?",
         "correcta": "3000", "distractores": ["600", "4200", "2400"], "explicacion": "7200 ÷ 12 = 600; 600 × 5 = 3000.", "dificultad": 2},
        {"modulo": 2, "nivel": "simulacro", "tema": "Fracción del resto (multi-paso)", "enunciado": "Un mayorista tenía 2600 sacas de arroz. Vendió 4/13; del resto vendió 1/3; del nuevo resto vendió 3/10. ¿Cuántas sacas le sobraron?",
         "correcta": "840", "distractores": ["800", "1200", "600"], "explicacion": "4/13 de 2600 = 800 (quedan 1800); 1/3 de 1800 = 600 (quedan 1200); 3/10 de 1200 = 360 (quedan 840).", "dificultad": 3},
        {"modulo": 2, "nivel": "simulacro", "tema": "Problema inverso del salario", "enunciado": "Gasté 1/5 de mi salario en comida y 2/3 de lo que sobró en otros gastos. Me quedaron R$ 160. ¿Cuál era mi salario?",
         "correcta": "R$ 600", "distractores": ["R$ 800", "R$ 480", "R$ 720"], "explicacion": "Tras comida queda 4/5; otros gastos 2/3 de 4/5 = 8/15; sobra 4/15 = 160 → salario 160 × 15/4 = 600.", "dificultad": 3},
        {"modulo": 3, "nivel": "familiariza", "tema": "Porcentaje simple", "enunciado": "¿Cuánto es el 25% de 80?",
         "correcta": "20", "distractores": ["25", "40", "16"], "explicacion": "25% = una cuarta parte; 80 ÷ 4 = 20.", "dificultad": 1},
        {"modulo": 3, "nivel": "simulacro", "tema": "Aumento porcentual", "enunciado": "El salario de Roberval era R$ 950. Recibió un aumento del 30%. ¿Cuál es su nuevo salario?",
         "correcta": "R$ 1235", "distractores": ["R$ 1250", "R$ 285", "R$ 980"], "explicacion": "30% de 950 = 285; 950 + 285 = 1235.", "dificultad": 3},
        {"modulo": 4, "nivel": "simulacro", "tema": "Cadena de fracciones", "enunciado": "Calcula 4/7 de 3/4 de 14/9 de 21.",
         "correcta": "14", "distractores": ["12", "21", "7"], "explicacion": "4/7 × 3/4 = 3/7; × 14/9 = 2/3; × 21 = 14.", "dificultad": 3},
    ],
    # ═══════════ FASE 6 · Geometría Espacial, Volumen y Magnitudes ═══════════
    6: [
        {"modulo": 1, "nivel": "familiariza", "tema": "Poliedros vs cuerpos redondos", "enunciado": "¿Cuál de estos NO es un poliedro (tiene superficie curva)?",
         "correcta": "El cilindro", "distractores": ["El cubo", "La pirámide", "El prisma triangular"], "explicacion": "El cilindro es un cuerpo redondo; el cubo, la pirámide y los prismas tienen caras planas.", "dificultad": 1},
        {"modulo": 1, "nivel": "simulacro", "tema": "Relación de Euler", "enunciado": "Un poliedro tiene 8 vértices y 12 aristas. Según Euler (V + C = A + 2), ¿cuántas caras tiene?",
         "correcta": "6", "distractores": ["4", "8", "5"], "explicacion": "C = A + 2 − V = 12 + 2 − 8 = 6.", "dificultad": 3},
        {"modulo": 3, "nivel": "familiariza", "tema": "Perímetro de rectángulo", "enunciado": "Una mesa mide 274 cm de largo y 152 cm de ancho. ¿Cuál es su perímetro?",
         "correcta": "852 cm", "distractores": ["426 cm", "800 cm", "904 cm"], "explicacion": "2 × (274 + 152) = 852 cm.", "dificultad": 2},
        {"modulo": 3, "nivel": "simulacro", "tema": "Área de una corona circular", "enunciado": "Una piscina circular de radio 3 m tiene alrededor una vereda de 1 m de ancho. ¿Cuál es el área de la vereda? (π = 3,14)",
         "correcta": "21,98 m²", "distractores": ["28,26 m²", "50,24 m²", "12,56 m²"], "explicacion": "Círculo grande 3,14×4²=50,24; piscina 3,14×3²=28,26; vereda = 21,98 m².", "dificultad": 3},
        {"modulo": 4, "nivel": "familiariza", "tema": "Volumen y capacidad", "enunciado": "¿Cuántos litros de agua caben en un depósito cúbico de 1 metro de arista?",
         "correcta": "1000", "distractores": ["100", "10000", "1"], "explicacion": "1 m³ = 1000 dm³ = 1000 litros.", "dificultad": 2},
        {"modulo": 4, "nivel": "simulacro", "tema": "Balanza en equilibrio", "enunciado": "Una balanza está en equilibrio con 3 sandías iguales de un lado y 1 sandía más una pesa de 4 kg del otro. ¿Cuánto pesa cada sandía?",
         "correcta": "2 kg", "distractores": ["4 kg", "6 kg", "1 kg"], "explicacion": "3 sandías = 1 sandía + 4 kg → 2 sandías = 4 kg → 2 kg cada una.", "dificultad": 3},
    ],
    # ═══════════ FASE 7 · Coordenadas, Rutas y Tiempo ═══════════
    7: [
        {"modulo": 3, "nivel": "familiariza", "tema": "Suma de tiempos", "enunciado": "Una clase dura 50 minutos y el recreo 20 minutos. ¿Cuánto suman en total?",
         "correcta": "1h 10min", "distractores": ["1h 20min", "1h", "1h 30min"], "explicacion": "50 + 20 = 70 minutos = 1 hora y 10 minutos.", "dificultad": 1},
        {"modulo": 3, "nivel": "simulacro", "tema": "Tiempo total (sexagesimal)", "enunciado": "Una escuela tiene 5 clases de 50 minutos cada una y un recreo de 20 minutos. ¿Cuánto tiempo permanece el alumno en la escuela?",
         "correcta": "4h 30min", "distractores": ["5h", "4h", "3h 50min"], "explicacion": "5 × 50 + 20 = 270 minutos = 4 horas y 30 minutos.", "dificultad": 3},
    ],
    # ═══════════ FASE 8 · Lógica, Combinatoria y Probabilidad ═══════════
    8: [
        {"modulo": 3, "nivel": "familiariza", "tema": "Porcentaje sobre población", "enunciado": "En una ciudad de 10 000 habitantes, el 49% tiene sangre tipo O. ¿Cuántas personas son tipo O?",
         "correcta": "4900", "distractores": ["4090", "5100", "490"], "explicacion": "49% de 10 000 = 4900.", "dificultad": 2},
        {"modulo": 3, "nivel": "simulacro", "tema": "Conteo de posibilidades", "enunciado": "Al lanzar dos dados de 6 caras, ¿de cuántas maneras distintas la suma de los puntos puede ser 5?",
         "correcta": "4", "distractores": ["3", "5", "2"], "explicacion": "(1,4), (2,3), (3,2) y (4,1): 4 maneras.", "dificultad": 3},
        {"modulo": 1, "nivel": "simulacro", "tema": "Divisibilidad", "enunciado": "En el número 4A47B, ¿qué cifras A y B lo hacen divisible a la vez por 2, 5, 9 y 10?",
         "correcta": "A=3, B=0", "distractores": ["A=0, B=0", "A=3, B=5", "A=6, B=0"], "explicacion": "Para ÷2, 5 y 10, B=0. Para ÷9, 15+A múltiplo de 9 → A=3.", "dificultad": 3},
        {"modulo": 1, "nivel": "simulacro", "tema": "MDC (Euclides)", "enunciado": "¿Cuál es el máximo común divisor (MDC) de 1200 y 540?",
         "correcta": "60", "distractores": ["120", "30", "90"], "explicacion": "1200=2×540+120; 540=4×120+60; 120=2×60 → MDC 60.", "dificultad": 3},
    ],
}


async def seed_banco_cmrj(session):
    """Inyecta el banco CMRJ. Idempotente (borra 'cmrj_*' previos).
    - nivel 'simulacro' → desafío final del módulo (Desafío Simulacro), 1-2/módulo.
    - nivel 'familiariza' → práctica del módulo (nivel 3).
    Cada pregunta = familia de 1 (cuenta para el progreso)."""
    import random as _r
    from sqlalchemy import select, delete, func
    from app.models.sql_models import (
        Pregunta, Alternativa, StatusEnum, OperacionEnum, TipoPreguntaEnum,
    )

    total = 0
    for fase_id, preguntas in BANCO_CMRJ.items():
        prev = (await session.execute(
            select(Pregunta.id).where(
                Pregunta.fase_id == fase_id,
                Pregunta.estructura_padre_id.like("cmrj_%"),
            )
        )).scalars().all()
        if prev:
            await session.execute(delete(Alternativa).where(Alternativa.pregunta_id.in_(prev)))
            await session.execute(delete(Pregunta).where(Pregunta.id.in_(prev)))

        # Secciones válidas existentes de la fase (para no inyectar en huecos).
        secs_fase = set((await session.execute(
            select(Pregunta.seccion).where(Pregunta.fase_id == fase_id).distinct()
        )).scalars().all())

        for idx, q in enumerate(preguntas):
            modulo = q.get("modulo", 1)
            if q.get("nivel") == "simulacro":
                # Desafío final del módulo (mod*1000+13); fallback a cualquier desafío.
                sec = modulo * 1000 + 13
                if sec not in secs_fase:
                    sec = next((s for s in sorted(secs_fase, reverse=True) if s >= 1000), None)
            else:
                # Práctica: nivel 3 del módulo (mod*100+3); fallback a nivel del módulo.
                sec = modulo * 100 + 3
                if sec not in secs_fase:
                    sec = next((s for s in sorted(secs_fase) if s == modulo * 100 + 1), None)
            if sec is None:
                # sin sección compatible: usar la máxima existente
                sec = max(secs_fase) if secs_fase else 99099

            datos = {"origen": "cmrj", "tema": q["tema"], "nivel": q.get("nivel", "simulacro"),
                     "dificultad": q.get("dificultad", 2), "es_espejo": False}
            for k in ("tipo_visual", "cortes", "sombreados", "total", "val_a", "val_b"):
                if k in q:
                    datos[k] = q[k]
            preg = Pregunta(
                fase_id=fase_id, seccion=sec, operacion=OperacionEnum.MIXTA,
                tipo_pregunta=TipoPreguntaEnum.MULTIPLE_OPCION,
                enunciado=q["enunciado"], respuesta_correcta=q["correcta"],
                datos_numericos=datos,
                explicacion_paso_a_paso={"pasos": [{"orden": 1, "texto": q["explicacion"]}]},
                estructura_padre_id=f"cmrj_f{fase_id}_{idx:03d}",
                estado=StatusEnum.ACTIVO,
            )
            session.add(preg)
            await session.flush()
            alts = [q["correcta"]] + list(q["distractores"])
            _r.Random(fase_id * 1000 + idx).shuffle(alts)
            for o, txt in enumerate(alts):
                session.add(Alternativa(
                    pregunta_id=preg.id, texto=txt,
                    es_correcta=(txt == q["correcta"]), orden=o,
                ))
            total += 1
    await session.commit()
    print(f"[banco_cmrj] {total} preguntas reales del CMRJ inyectadas (simulacro + familiarizacion).")
    return total
