"""
Banco curado de preguntas REALES del examen CMRJ / Colégio Pedro II, por fase.

Origen: `Pedro II/04_Banco_Transcribido` (transcripción de las fotos del examen),
traducidas al español y verificadas. Se inyectan en el desafío final de cada
fase temática con `seed_banco_cmrj()` (ver seed maestro), como ANCLAS reales del
nivel del examen, junto al contenido generado. Las figuras usan los
visualizadores paramétricos de la app (tipo_visual) para no revelar la respuesta
ni depender de archivos externos.

Formato por pregunta: enunciado (ES), correcta, distractores[3], explicacion,
tema, dificultad(1-3), tipo_visual opcional + payload.
"""

# Mapea cada fase temática a la sección de desafío donde inyectar (se resuelve
# dinámicamente en el seeder si no existe).
BANCO_CMRJ = {
    # ── FASE 5: Fracciones, Porcentajes y Proporciones ──────────────────────
    5: [
        {"tema": "Fracción de una figura", "enunciado": "En un círculo dividido en 8 partes iguales hay 3 partes sombreadas. ¿Qué fracción representa la parte sombreada?",
         "correcta": "3/8", "distractores": ["5/8", "3/5", "8/3"],
         "explicacion": "3 partes sombreadas de 8 partes iguales en total = 3/8.",
         "dificultad": 1, "tipo_visual": "pizza", "cortes": 8, "sombreados": [0, 1, 2]},
        {"tema": "Suma de fracciones (distinto denominador)", "enunciado": "Calcula 1/2 + 1/3 reduciendo al mínimo común múltiplo.",
         "correcta": "5/6", "distractores": ["2/5", "1/6", "2/6"],
         "explicacion": "MCM(2,3)=6. 1/2 = 3/6 y 1/3 = 2/6; 3/6 + 2/6 = 5/6.", "dificultad": 2},
        {"tema": "Fracción impropia a mixto", "enunciado": "Transforma la fracción impropia 9/4 en número mixto.",
         "correcta": "2 1/4", "distractores": ["1 5/4", "2 3/4", "4 1/2"],
         "explicacion": "9 ÷ 4 = 2 con resto 1, entonces 9/4 = 2 enteros y 1/4.", "dificultad": 2},
        {"tema": "Aumento porcentual", "enunciado": "El salario de Roberval era R$ 950. Recibió un aumento del 30%. ¿Cuál es su nuevo salario?",
         "correcta": "R$ 1235", "distractores": ["R$ 1250", "R$ 285", "R$ 980"],
         "explicacion": "30% de 950 = 285; nuevo salario = 950 + 285 = 1235.", "dificultad": 2},
        {"tema": "Fracción del resto (multi-paso)", "enunciado": "Un mayorista tenía 2600 sacas de arroz. Vendió 4/13; del resto vendió 1/3; del nuevo resto vendió 3/10. ¿Cuántas sacas le sobraron?",
         "correcta": "840", "distractores": ["800", "1200", "600"],
         "explicacion": "4/13 de 2600 = 800 (quedan 1800); 1/3 de 1800 = 600 (quedan 1200); 3/10 de 1200 = 360 (quedan 840).", "dificultad": 3},
    ],
    # ── FASE 6: Geometría Espacial, Volumen y Magnitudes ────────────────────
    6: [
        {"tema": "Poliedros vs cuerpos redondos", "enunciado": "¿Cuál de estos NO es un poliedro (tiene superficie curva)?",
         "correcta": "El cilindro", "distractores": ["El cubo", "La pirámide", "El prisma triangular"],
         "explicacion": "El cilindro es un cuerpo redondo (superficie curva). El cubo, la pirámide y los prismas son poliedros (caras planas).", "dificultad": 1},
        {"tema": "Relación de Euler", "enunciado": "Un poliedro tiene 8 vértices y 12 aristas. Según Euler (V + C = A + 2), ¿cuántas caras tiene?",
         "correcta": "6", "distractores": ["4", "8", "5"],
         "explicacion": "C = A + 2 − V = 12 + 2 − 8 = 6 caras.", "dificultad": 3},
        {"tema": "Volumen y capacidad", "enunciado": "¿Cuántos litros de agua caben en un depósito cúbico de 1 metro de arista?",
         "correcta": "1000", "distractores": ["100", "10000", "1"],
         "explicacion": "1 m³ = 1000 dm³ y 1 dm³ = 1 litro, entonces caben 1000 litros.", "dificultad": 2},
        {"tema": "Balanza en equilibrio", "enunciado": "Una balanza está en equilibrio con 3 sandías iguales de un lado y 1 sandía más una pesa de 4 kg del otro. ¿Cuánto pesa cada sandía?",
         "correcta": "2 kg", "distractores": ["4 kg", "6 kg", "1 kg"],
         "explicacion": "3 sandías = 1 sandía + 4 kg → 2 sandías = 4 kg → cada sandía pesa 2 kg.", "dificultad": 3},
        {"tema": "Área de una corona circular", "enunciado": "Una piscina circular de radio 3 m tiene alrededor una vereda de 1 m de ancho. ¿Cuál es el área de la vereda? (π = 3,14)",
         "correcta": "21,98 m²", "distractores": ["28,26 m²", "50,24 m²", "12,56 m²"],
         "explicacion": "Círculo grande 3,14×4²=50,24; piscina 3,14×3²=28,26; vereda = 50,24 − 28,26 = 21,98 m².", "dificultad": 3},
        {"tema": "Área total de una planta", "enunciado": "Un apartamento tiene: sala 24 m², cuarto 1 15 m², cuarto 2 12 m², cocina 9 m² y baño 4 m². ¿Cuál es el área total?",
         "correcta": "64 m²", "distractores": ["60 m²", "66 m²", "54 m²"],
         "explicacion": "24 + 15 + 12 + 9 + 4 = 64 m².", "dificultad": 2},
    ],
    # ── FASE 7: Coordenadas, Rutas y Tiempo ─────────────────────────────────
    7: [
        {"tema": "Tiempo (sistema sexagesimal)", "enunciado": "Una escuela tiene 5 clases de 50 minutos cada una y un recreo de 20 minutos. ¿Cuánto tiempo permanece el alumno en la escuela?",
         "correcta": "4h 30min", "distractores": ["5h", "4h", "3h 50min"],
         "explicacion": "5 × 50 + 20 = 270 minutos = 4 horas y 30 minutos.", "dificultad": 2},
        {"tema": "Perímetro", "enunciado": "Una mesa de ping-pong mide 274 cm de largo y 152 cm de ancho. ¿Cuál es su perímetro?",
         "correcta": "852 cm", "distractores": ["426 cm", "800 cm", "904 cm"],
         "explicacion": "Perímetro = 2 × (274 + 152) = 2 × 426 = 852 cm.", "dificultad": 2},
    ],
    # ── FASE 8: Lógica, Combinatoria y Probabilidad ─────────────────────────
    8: [
        {"tema": "Gráfico de sectores (%)", "enunciado": "En una ciudad de 10 000 habitantes, el 49% tiene sangre tipo O. ¿Cuántas personas son tipo O?",
         "correcta": "4900", "distractores": ["4090", "5100", "490"],
         "explicacion": "49% de 10 000 = 0,49 × 10 000 = 4900 personas.", "dificultad": 2},
        {"tema": "Conteo de posibilidades", "enunciado": "Al lanzar dos dados de 6 caras, ¿de cuántas maneras distintas la suma de los puntos puede ser 5?",
         "correcta": "4", "distractores": ["3", "5", "2"],
         "explicacion": "Las combinaciones son (1,4), (2,3), (3,2) y (4,1): 4 maneras.", "dificultad": 2},
        {"tema": "Divisibilidad", "enunciado": "En el número 4A47B, ¿qué cifras A y B lo hacen divisible a la vez por 2, 5, 9 y 10?",
         "correcta": "A=3, B=0", "distractores": ["A=0, B=0", "A=3, B=5", "A=6, B=0"],
         "explicacion": "Para ÷2, 5 y 10, B=0. Para ÷9, 4+A+4+7+0=15+A múltiplo de 9 → A=3.", "dificultad": 3},
        {"tema": "MDC (algoritmo de Euclides)", "enunciado": "¿Cuál es el máximo común divisor (MDC) de 1200 y 540?",
         "correcta": "60", "distractores": ["120", "30", "90"],
         "explicacion": "1200 = 2×540 + 120; 540 = 4×120 + 60; 120 = 2×60. El último resto no nulo es 60.", "dificultad": 3},
    ],
    # ── FASE 4: Decimales y Conversiones ────────────────────────────────────
    4: [
        {"tema": "Porcentaje de una cantidad", "enunciado": "¿Cuánto es el 40% de 48 metros?",
         "correcta": "19,2 m", "distractores": ["4,8 m", "24 m", "12 m"],
         "explicacion": "40% de 48 = 0,40 × 48 = 19,2 metros.", "dificultad": 2},
        {"tema": "Decimal a fracción irreducible", "enunciado": "Escribe 0,76 como fracción irreducible.",
         "correcta": "19/25", "distractores": ["76/100", "38/50", "19/20"],
         "explicacion": "0,76 = 76/100; dividiendo entre 4: 19/25.", "dificultad": 3},
    ],
}


async def seed_banco_cmrj(session):
    """Inyecta las preguntas reales del CMRJ en el desafío final de cada fase.
    Idempotente: borra las inyecciones previas (estructura_padre_id 'cmrj_*')."""
    import random as _r
    from sqlalchemy import select, delete, func
    from app.models.sql_models import (
        Pregunta, Alternativa, StatusEnum, OperacionEnum, TipoPreguntaEnum,
    )

    total = 0
    for fase_id, preguntas in BANCO_CMRJ.items():
        sec = (await session.execute(
            select(func.max(Pregunta.seccion)).where(
                Pregunta.fase_id == fase_id, Pregunta.seccion >= 1000
            )
        )).scalar()
        if sec is None:
            sec = (await session.execute(
                select(func.max(Pregunta.seccion)).where(Pregunta.fase_id == fase_id)
            )).scalar() or 99099

        prev = (await session.execute(
            select(Pregunta.id).where(
                Pregunta.fase_id == fase_id,
                Pregunta.estructura_padre_id.like("cmrj_%"),
            )
        )).scalars().all()
        if prev:
            await session.execute(delete(Alternativa).where(Alternativa.pregunta_id.in_(prev)))
            await session.execute(delete(Pregunta).where(Pregunta.id.in_(prev)))

        for idx, q in enumerate(preguntas):
            datos = {"origen": "cmrj", "tema": q["tema"],
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
    print(f"[banco_cmrj] {total} preguntas reales del CMRJ inyectadas en las fases.")
    return total
