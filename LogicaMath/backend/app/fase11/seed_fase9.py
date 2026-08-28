import asyncio
import random
from sqlalchemy import select, and_, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal

from app.models.sql_models import (
    Fase, Pregunta, Alternativa, ConfiguracionProgreso,
    StatusEnum, OperacionEnum, TipoPreguntaEnum, TipoErrorEnum,
    Intento, PoolAsignadoAlumno
)
from app.fase2.models import NivelTeoria, IntentoPregunta, IntentoPaso
from app.models.simulado_questao import SimuladoQuestao

FASE11_ID = 9


def _cuatro_alternativas(item: dict) -> list[str]:
    """Construye las cuatro opciones visibles: clave única y tres distractores."""
    opciones = [item["correcta"]]
    for distractor in item["distractores"]:
        if distractor not in opciones:
            opciones.append(distractor)
        if len(opciones) == 4:
            return opciones
    raise ValueError(f"Distractores insuficientes para: {item['enunciado'][:80]}")

async def clear_fase9_data(session: AsyncSession):
    print("Purging existing Fase 9 data...")
    result = await session.execute(select(Pregunta.id).where(Pregunta.fase_id == FASE11_ID))
    pregunta_ids_list = result.scalars().all()
    
    if pregunta_ids_list:
        await session.execute(delete(Alternativa).where(Alternativa.pregunta_id.in_(pregunta_ids_list)))
        res_int_q = await session.execute(select(IntentoPregunta.id).where(IntentoPregunta.pregunta_id.in_(pregunta_ids_list)))
        int_q_ids = res_int_q.scalars().all()
        if int_q_ids:
            await session.execute(delete(IntentoPaso).where(IntentoPaso.intento_pregunta_id.in_(int_q_ids)))
            await session.execute(delete(IntentoPregunta).where(IntentoPregunta.id.in_(int_q_ids)))
            
        await session.execute(delete(Intento).where(Intento.pregunta_id.in_(pregunta_ids_list)))
        await session.execute(delete(PoolAsignadoAlumno).where(PoolAsignadoAlumno.pregunta_id.in_(pregunta_ids_list)))
        
    await session.execute(delete(Intento).where(Intento.fase_id == FASE11_ID))
    await session.execute(delete(PoolAsignadoAlumno).where(PoolAsignadoAlumno.fase_id == FASE11_ID))
    await session.execute(delete(Pregunta).where(Pregunta.fase_id == FASE11_ID))
    await session.execute(delete(ConfiguracionProgreso).where(ConfiguracionProgreso.fase_id == FASE11_ID))
    await session.execute(delete(NivelTeoria).where(NivelTeoria.fase_id == FASE11_ID))
    await session.commit()
    print("Fase 9 data purged.")
async def seed_teoria_niveles_fase9(session: AsyncSession):
    print("Sembrando guión de textos para Fase 9...")
    niveles_teoria = []
    
    # Módulo 1 (5 niveles)
    for l in range(1, 6):
        niveles_teoria.append({
            "modulo_id": 1,
            "nivel_id": l,
            "titulo": f"Simulacro {l}",
            "texto_descubrimiento": "Simulacro de adaptación y nivel básico.",
            "diccionario": {},
            "advertencia": "",
            "ejemplos": [],
            "interactivos": []
        })
        
    # Módulo 2 (10 niveles)
    for l in range(1, 11):
        niveles_teoria.append({
            "modulo_id": 2,
            "nivel_id": l,
            "titulo": f"Simulacro {l+5}",
            "texto_descubrimiento": "Simulacro de exigencia real.",
            "diccionario": {},
            "advertencia": "",
            "ejemplos": [],
            "interactivos": []
        })
        
    # Módulo 3 (5 niveles)
    for l in range(1, 6):
        niveles_teoria.append({
            "modulo_id": 3,
            "nivel_id": l,
            "titulo": f"Simulacro Maestro {l+15}",
            "texto_descubrimiento": "Simulacro de alta exigencia.",
            "diccionario": {},
            "advertencia": "",
            "ejemplos": [],
            "interactivos": []
        })

    for data in niveles_teoria:
        nt = NivelTeoria(fase_id=FASE11_ID, **data)
        session.add(nt)
    await session.commit()


async def inject_pedro_ii_history(session: AsyncSession):
    print("Inyectando Banco Histórico Pedro II y preguntas de simulación...")
    
    sections = []
    # Module 1: 5 levels
    for l in range(1, 6):
        sections.append((1, l))
    # Module 2: 10 levels
    for l in range(1, 11):
        sections.append((2, l))
    # Module 3: 5 levels
    for l in range(1, 6):
        sections.append((3, l))
        
    from app.fase11.banco_simulados import BANCO_SIMULADOS
    total_banco = len(BANCO_SIMULADOS)
    preguntas_por_seccion = 10

    for mod_id, lvl_id in sections:
        seccion_id = mod_id * 100 + lvl_id
        # Baraja determinista del banco por sección: cada simulacro recibe
        # `preguntas_por_seccion` preguntas DISTINTAS (sample sin reemplazo) y
        # distintas secciones obtienen subconjuntos/órdenes diferentes. Esto
        # elimina la repetición palabra-por-palabra del stub anterior.
        orden = random.Random(FASE11_ID * 100000 + seccion_id).sample(
            range(total_banco), k=min(preguntas_por_seccion, total_banco)
        )
        for pos, q_idx in enumerate(orden):
            q = BANCO_SIMULADOS[q_idx]
            rng = random.Random(FASE11_ID * 100000 + seccion_id * 100 + pos)
            alts = _cuatro_alternativas(q)
            rng.shuffle(alts)

            payload = {
                "fase9": True,
                "tema": q["tema"],
                "dificultad": q["dificultad"],
                "origen_examen": "Colégio Militar RJ (adaptado)",
            }

            p = Pregunta(
                fase_id=FASE11_ID, seccion=seccion_id, operacion=OperacionEnum.MIXTA,
                tipo_pregunta=TipoPreguntaEnum.MULTIPLE_OPCION, enunciado=q["enunciado"],
                respuesta_correcta=q["correcta"],
                datos_numericos=payload,
                errores_previstos={},
                explicacion_paso_a_paso={"titulo": "Resolución", "pasos": [{"orden": 1, "texto": q["explicacion"]}]},
                estado=StatusEnum.ACTIVO
            )

            for idx_alt, alt in enumerate(alts):
                p.alternativas.append(Alternativa(texto=alt, es_correcta=(alt == q["correcta"]), orden=idx_alt + 1))

            session.add(p)
    await session.commit()


async def seed_simulados_operativos(session: AsyncSession):
    """Genera los 20 simulacros que sirve la API activa de Fase 9.

    No modifica sesiones ni intentos existentes. Si el banco operacional ya
    existe, se conserva íntegro para que las sesiones anteriores sigan siendo
    reproducibles.
    """
    existentes = await session.scalar(select(func.count(SimuladoQuestao.id)))
    if existentes:
        print(f"simulado_questao ya contiene {existentes} preguntas; se conserva.")
        return

    from app.fase11.banco_simulados import BANCO_SIMULADOS
    letras = "ABCD"
    for numero in range(1, 21):
        indices = random.Random(9_900_000 + numero).sample(range(len(BANCO_SIMULADOS)), 10)
        for orden, indice in enumerate(indices, start=1):
            item = BANCO_SIMULADOS[indice]
            alternativas = _cuatro_alternativas(item)
            random.Random(9_910_000 + numero * 100 + orden).shuffle(alternativas)
            correcta = letras[alternativas.index(item["correcta"])]
            dificultad = {1: "facil", 2: "medio", 3: "dificil"}.get(item["dificultad"], "medio")
            session.add(SimuladoQuestao(
                simulacro_numero=numero, ordem_na_prova=orden,
                enunciado=item["enunciado"],
                alternativa_a=alternativas[0], alternativa_b=alternativas[1],
                alternativa_c=alternativas[2], alternativa_d=alternativas[3],
                alternativa_correta=correcta,
                resolucao=[{"paso": 1, "texto": item["explicacion"]}],
                tema=item["tema"], dificuldade=dificultad,
            ))
    await session.commit()
    print("200 preguntas operativas sembradas en simulado_questao (20 simulacros × 10).")

async def run_fase9_seed():
    print("=" * 60)
    print("Iniciando inyección de datos semilla de FASE 9...")
    async with AsyncSessionLocal() as session:
        fase = await session.get(Fase, FASE11_ID)
        if not fase:
            fase = Fase(id=FASE11_ID, nombre="Simulados Colegio Pedro II", descripcion="Fase 9", orden=9, icono="🎓")
            session.add(fase)
            await session.commit()
            
        await clear_fase9_data(session)
        await seed_teoria_niveles_fase9(session)
        await inject_pedro_ii_history(session)
        await seed_simulados_operativos(session)
    print("FASE 9 COMPLETADA.")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_fase9_seed())
