import asyncio
import random
import base64
from sqlalchemy import select, and_, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal

from app.models.sql_models import (
    Fase, Pregunta, Alternativa, ConfiguracionProgreso,
    StatusEnum, OperacionEnum, TipoPreguntaEnum, TipoErrorEnum,
    Intento, PoolAsignadoAlumno
)
from app.fase2.models import NivelTeoria, IntentoPregunta, IntentoPaso

FASE9_ID = 8

# --- DICCIONARIOS DE CONTEXTO FASE 8 ---
NOMBRES = ["Samuel", "Camila", "Julieta", "Emilio", "Valentina", "Nicolás", "Mateo", "Isabella", "Lucas", "Martina"]
ROPA_1 = ["camisas", "poleras", "chaquetas", "polerones"]
ROPA_2 = ["pantalones", "faldas", "shorts", "jeans"]
ROPA_3 = ["zapatos", "zapatillas", "gorras", "bufandas"]
CONTENEDORES = ["caja", "bolsa", "urna", "sombrero", "cofre", "mochila"]
FRUTAS_1 = ["manzanas", "naranjas", "peras", "duraznos"]
FRUTAS_2 = ["plátanos", "uvas", "frutillas", "ciruelas"]

async def clear_fase8_data(session: AsyncSession):
    print("Purging existing Fase 8 data...")
    result = await session.execute(select(Pregunta.id).where(Pregunta.fase_id == FASE9_ID))
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
        
    await session.execute(delete(Intento).where(Intento.fase_id == FASE9_ID))
    await session.execute(delete(PoolAsignadoAlumno).where(PoolAsignadoAlumno.fase_id == FASE9_ID))
    await session.execute(delete(Pregunta).where(Pregunta.fase_id == FASE9_ID))
    await session.execute(delete(ConfiguracionProgreso).where(ConfiguracionProgreso.fase_id == FASE9_ID))
    await session.execute(delete(NivelTeoria).where(NivelTeoria.fase_id == FASE9_ID))
    await session.commit()
    print("Fase 8 data purged.")

async def seed_teoria_niveles_fase8(session: AsyncSession):
    print("Sembrando guión de textos para Fase 8...")
    from app.fase9.content_fase8 import niveles_teoria_fase8
    
    for data in niveles_teoria_fase8:
        nt = NivelTeoria(fase_id=FASE9_ID, **data)
        session.add(nt)
    await session.commit()

def _svg_to_base64(svg_str: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(svg_str.encode('utf-8')).decode('utf-8')

# ── Generadores de SVGs Especializados para Fase 8 ──────────────────────────

def _generate_svg_seq_arithmetic(start: int, step: int, is_plus: bool = True) -> str:
    svg = '<svg viewBox="0 0 500 130" xmlns="http://www.w3.org/2000/svg" style="background:#0f172a; border-radius:10px; border:2px solid #10B981;">'
    svg += '<text x="250" y="22" font-size="12" font-family="Arial" font-weight="bold" fill="#38BDF8" text-anchor="middle">Secuencia Aritmética</text>'
    for i in range(5):
        val = (start + step * i) if is_plus else (start - step * i)
        txt = "?" if i == 4 else str(val)
        color = "#EF4444" if i == 4 else "#10B981"
        svg += f'<rect x="{20 + i*95}" y="38" width="65" height="55" rx="10" fill="{color}22" stroke="{color}" stroke-width="2.5"/>'
        svg += f'<text x="{52 + i*95}" y="74" font-size="22" font-family="Arial" font-weight="bold" fill="#F8FAFC" text-anchor="middle">{txt}</text>'
        if i < 4:
            sign = "+" if is_plus else "-"
            svg += f'<path d="M {87 + i*95} 65 Q {97 + i*95} 40 {113 + i*95} 65" fill="none" stroke="#F59E0B" stroke-width="2" stroke-dasharray="3 3"/>'
            svg += f'<text x="{100 + i*95}" y="42" font-size="11" font-family="Arial" font-weight="bold" fill="#F59E0B" text-anchor="middle">{sign}{step}</text>'
    svg += '</svg>'
    return _svg_to_base64(svg)

def _generate_svg_seq_geometric(start: int, factor: int) -> str:
    svg = '<svg viewBox="0 0 500 130" xmlns="http://www.w3.org/2000/svg" style="background:#0f172a; border-radius:10px; border:2px solid #10B981;">'
    svg += '<text x="250" y="22" font-size="12" font-family="Arial" font-weight="bold" fill="#38BDF8" text-anchor="middle">Progresión Geométrica (Multiplicación)</text>'
    for i in range(4):
        val = start * (factor ** i)
        txt = "?" if i == 3 else str(val)
        color = "#EF4444" if i == 3 else "#8B5CF6"
        svg += f'<rect x="{30 + i*115}" y="38" width="75" height="55" rx="10" fill="{color}22" stroke="{color}" stroke-width="2.5"/>'
        svg += f'<text x="{67 + i*115}" y="74" font-size="20" font-family="Arial" font-weight="bold" fill="#F8FAFC" text-anchor="middle">{txt}</text>'
        if i < 3:
            svg += f'<path d="M {107 + i*115} 65 Q {125 + i*115} 40 {143 + i*115} 65" fill="none" stroke="#F59E0B" stroke-width="2" stroke-dasharray="3 3"/>'
            svg += f'<text x="{125 + i*115}" y="42" font-size="11" font-family="Arial" font-weight="bold" fill="#F59E0B" text-anchor="middle">×{factor}</text>'
    svg += '</svg>'
    return _svg_to_base64(svg)

def _generate_svg_seq_interpolation(vals: list, missing_idx: int) -> str:
    svg = '<svg viewBox="0 0 500 130" xmlns="http://www.w3.org/2000/svg" style="background:#0f172a; border-radius:10px; border:2px solid #10B981;">'
    svg += '<text x="250" y="22" font-size="12" font-family="Arial" font-weight="bold" fill="#38BDF8" text-anchor="middle">Interpolación (Término Oculto)</text>'
    n = len(vals)
    spacing = 460 // n
    for i in range(n):
        txt = "?" if i == missing_idx else str(vals[i])
        color = "#EF4444" if i == missing_idx else "#10B981"
        x_pos = 20 + i * spacing
        svg += f'<rect x="{x_pos}" y="38" width="60" height="55" rx="10" fill="{color}22" stroke="{color}" stroke-width="2.5"/>'
        svg += f'<text x="{x_pos + 30}" y="74" font-size="20" font-family="Arial" font-weight="bold" fill="#F8FAFC" text-anchor="middle">{txt}</text>'
    svg += '</svg>'
    return _svg_to_base64(svg)

def _generate_svg_tree_diagram(op1: int, op2: int) -> str:
    svg = '<svg viewBox="0 0 320 180" xmlns="http://www.w3.org/2000/svg" style="background:#0f172a; border-radius:10px; border:2px solid #8B5CF6;">'
    svg += '<text x="160" y="22" font-size="12" font-family="Arial" font-weight="bold" fill="#8B5CF6" text-anchor="middle">Diagrama de Árbol (Ramas de Opciones)</text>'
    svg += '<circle cx="30" cy="90" r="10" fill="#8B5CF6"/>'
    
    for i in range(op1):
        y1 = 45 + i * (90 / max(1, op1 - 1)) if op1 > 1 else 90
        svg += f'<line x1="40" y1="90" x2="110" y2="{y1}" stroke="#A78BFA" stroke-width="2"/>'
        svg += f'<rect x="110" y="{y1-12}" width="35" height="24" rx="5" fill="#8B5CF6" stroke="#C4B5FD"/>'
        svg += f'<text x="127" y="{y1+4}" font-size="10" font-family="Arial" font-weight="bold" fill="#FFF" text-anchor="middle">A{i+1}</text>'
        
        for j in range(op2):
            y2 = y1 - 15 + j * (30 / max(1, op2 - 1)) if op2 > 1 else y1
            svg += f'<line x1="145" y1="{y1}" x2="230" y2="{y2}" stroke="#6D28D9" stroke-width="1.5" stroke-dasharray="2 2"/>'
            svg += f'<circle cx="240" cy="{y2}" r="8" fill="#10B981"/>'
            svg += f'<text x="240" y="{y2+3}" font-size="9" font-family="Arial" font-weight="bold" fill="#FFF" text-anchor="middle">B{j+1}</text>'
            
    svg += f'<text x="160" y="168" font-size="11" font-family="Arial" font-weight="bold" fill="#F8FAFC" text-anchor="middle">Total de Combinaciones = {op1} × {op2} = {op1*op2}</text>'
    svg += '</svg>'
    return _svg_to_base64(svg)

def _generate_svg_multiplicative_groups(op1: int, op2: int, op3: int = None) -> str:
    svg = '<svg viewBox="0 0 320 140" xmlns="http://www.w3.org/2000/svg" style="background:#0f172a; border-radius:10px; border:2px solid #8B5CF6;">'
    svg += '<text x="160" y="22" font-size="12" font-family="Arial" font-weight="bold" fill="#8B5CF6" text-anchor="middle">Principio Multiplicativo</text>'
    
    if op3:
        total = op1 * op2 * op3
        txt_formula = f"{op1} × {op2} × {op3} = {total}"
    else:
        total = op1 * op2
        txt_formula = f"{op1} × {op2} = {total}"
        
    svg += f'<rect x="30" y="40" width="70" height="40" rx="8" fill="#1e293b" stroke="#3b82f6" stroke-width="2"/>'
    svg += f'<text x="65" y="65" font-size="14" font-family="Arial" font-weight="bold" fill="#3b82f6" text-anchor="middle">{op1} Opciones</text>'

    svg += f'<text x="120" y="66" font-size="18" font-family="Arial" font-weight="bold" fill="#F59E0B" text-anchor="middle">×</text>'

    svg += f'<rect x="140" y="40" width="70" height="40" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="2"/>'
    svg += f'<text x="175" y="65" font-size="14" font-family="Arial" font-weight="bold" fill="#10b981" text-anchor="middle">{op2} Opciones</text>'

    if op3:
        svg += f'<text x="230" y="66" font-size="18" font-family="Arial" font-weight="bold" fill="#F59E0B" text-anchor="middle">×</text>'
        svg += f'<rect x="245" y="40" width="60" height="40" rx="8" fill="#1e293b" stroke="#ec4899" stroke-width="2"/>'
        svg += f'<text x="275" y="65" font-size="13" font-family="Arial" font-weight="bold" fill="#ec4899" text-anchor="middle">{op3} Opt.</text>'

    svg += f'<text x="160" y="115" font-size="13" font-family="Arial" font-weight="bold" fill="#F8FAFC" text-anchor="middle">Combinaciones Totales: {txt_formula}</text>'
    svg += '</svg>'
    return _svg_to_base64(svg)

def _generate_svg_mcd_groups(num1: int, num2: int, mcd_val: int) -> str:
    svg = '<svg viewBox="0 0 320 140" xmlns="http://www.w3.org/2000/svg" style="background:#0f172a; border-radius:10px; border:2px solid #8B5CF6;">'
    svg += '<text x="160" y="22" font-size="12" font-family="Arial" font-weight="bold" fill="#8B5CF6" text-anchor="middle">Empaquetado Exacto — Máximo Común Divisor</text>'
    
    svg += f'<rect x="25" y="40" width="125" height="45" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>'
    svg += f'<text x="87" y="58" font-size="11" font-family="Arial" font-weight="bold" fill="#38bdf8" text-anchor="middle">Grupo A: {num1} unidades</text>'
    svg += f'<text x="87" y="74" font-size="10" font-family="Arial" fill="#94a3b8" text-anchor="middle">({num1//mcd_val} por canasta)</text>'

    svg += f'<rect x="170" y="40" width="125" height="45" rx="8" fill="#1e293b" stroke="#f59e0b" stroke-width="1.5"/>'
    svg += f'<text x="232" y="58" font-size="11" font-family="Arial" font-weight="bold" fill="#f59e0b" text-anchor="middle">Grupo B: {num2} unidades</text>'
    svg += f'<text x="232" y="74" font-size="10" font-family="Arial" fill="#94a3b8" text-anchor="middle">({num2//mcd_val} por canasta)</text>'

    svg += f'<text x="160" y="118" font-size="12" font-weight="bold" font-family="Arial" fill="#10b981" text-anchor="middle">MCD({num1}, {num2}) = {mcd_val} Canastas Máximas</text>'
    svg += '</svg>'
    return _svg_to_base64(svg)

def _generate_svg_urn_balls(rojas: int, azules: int) -> str:
    total = rojas + azules
    svg = '<svg viewBox="0 0 280 170" xmlns="http://www.w3.org/2000/svg" style="background:#0f172a; border-radius:10px; border:2px solid #F59E0B;">'
    svg += '<text x="140" y="20" font-size="12" font-family="Arial" font-weight="bold" fill="#F59E0B" text-anchor="middle">Urna de Probabilidad (Regla de Laplace)</text>'
    
    # Jar Shape
    svg += '<path d="M 80 40 L 80 125 A 30 15 0 0 0 200 125 L 200 40" fill="#1e293b" stroke="#64748b" stroke-width="3"/>'
    svg += '<ellipse cx="140" cy="40" rx="60" ry="12" fill="#0f172a" stroke="#64748b" stroke-width="3"/>'
    
    # Esferas rojas
    for i in range(rojas):
        cx = 105 + (i % 3) * 28
        cy = 110 - (i // 3) * 24
        svg += f'<circle cx="{cx}" cy="{cy}" r="10" fill="#ef4444" stroke="#f8fafc" stroke-width="1.5"/>'
    
    # Esferas azules
    for i in range(azules):
        cx = 120 + (i % 3) * 28
        cy = 75 - (i // 3) * 24
        svg += f'<circle cx="{cx}" cy="{cy}" r="10" fill="#3b82f6" stroke="#f8fafc" stroke-width="1.5"/>'
        
    svg += f'<text x="140" y="155" font-size="11" font-family="Arial" font-weight="bold" fill="#f8fafc" text-anchor="middle">Rojas: {rojas} | Azules: {azules} | Total: {total}</text>'
    svg += '</svg>'
    return _svg_to_base64(svg)

def _generate_svg_probability_duel(favA: int, totA: int, favB: int, totB: int) -> str:
    svg = '<svg viewBox="0 0 300 140" xmlns="http://www.w3.org/2000/svg" style="background:#0f172a; border-radius:10px; border:2px solid #F59E0B;">'
    svg += '<text x="150" y="22" font-size="12" font-family="Arial" font-weight="bold" fill="#F59E0B" text-anchor="middle">Duelo de Probabilidades</text>'
    
    svg += f'<rect x="25" y="40" width="110" height="55" rx="8" fill="#1e293b" stroke="#38bdf8" stroke-width="2"/>'
    svg += f'<text x="80" y="60" font-size="11" font-family="Arial" font-weight="bold" fill="#38bdf8" text-anchor="middle">Opción A</text>'
    svg += f'<text x="80" y="80" font-size="14" font-family="Arial" font-weight="bold" fill="#f8fafc" text-anchor="middle">{favA}/{totA}</text>'

    svg += f'<text x="150" y="72" font-size="16" font-family="Arial" font-weight="bold" fill="#f59e0b" text-anchor="middle">VS</text>'

    svg += f'<rect x="165" y="40" width="110" height="55" rx="8" fill="#1e293b" stroke="#10b981" stroke-width="2"/>'
    svg += f'<text x="220" y="60" font-size="11" font-family="Arial" font-weight="bold" fill="#10b981" text-anchor="middle">Opción B</text>'
    svg += f'<text x="220" y="80" font-size="14" font-family="Arial" font-weight="bold" fill="#f8fafc" text-anchor="middle">{favB}/{totB}</text>'

    svg += f'<text x="150" y="122" font-size="11" font-family="Arial" font-style="italic" fill="#94a3b8" text-anchor="middle">Compara las fracciones para elegir al ganador</text>'
    svg += '</svg>'
    return _svg_to_base64(svg)

# ── Generador del Pool Diferenciado por Modulo y Nivel ──────────────────────

def _dedupe_and_pad(alts: list, rng: random.Random, pad_fn) -> list:
    """Devuelve exactamente 4 alternativas string DISTINTAS. `pad_fn` genera un
    candidato nuevo en el mismo formato temático (fracción, número) cuando
    faltan opciones tras deduplicar — evita el bug de opciones repetidas
    (p.ej. "rojas/total" == "azules/total" cuando rojas==azules).
    """
    out = list(dict.fromkeys(alts))  # dedupe preservando orden
    attempts = 0
    while len(out) < 4 and attempts < 50:
        candidate = pad_fn()
        if candidate not in out:
            out.append(candidate)
        attempts += 1
    return out


async def _gen_fase8_pool(rng: random.Random, mod_id: int, lvl_id: int) -> dict:
    nombre = rng.choice(NOMBRES)
    errores_previstos = {}

    if mod_id == 1:
        if lvl_id in (1, 11):
            start = rng.randint(2, 12)
            step = rng.randint(2, 6)
            is_plus = rng.choice([True, False])
            
            if is_plus:
                ans = start + step * 4
                seq_str = f"{start}, {start+step}, {start+step*2}, {start+step*3}, ___"
                expl_str = f"El patrón es sumar {step} a cada número."
                ans_str = str(ans)
                alts = [ans_str, str(ans + step), str(ans - 1), str(start + step * 3)]
                errores_previstos[str(ans + step)] = "Te saltaste un término. Calculaste el número siguiente."
            else:
                start = start + step * 5
                ans = start - step * 4
                seq_str = f"{start}, {start-step}, {start-step*2}, {start-step*3}, ___"
                expl_str = f"El patrón es restar {step} a cada número."
                ans_str = str(ans)
                alts = [ans_str, str(ans - step), str(ans + 1), str(start - step * 3)]
                errores_previstos[str(ans - step)] = "Restaste un paso de más."

            alts = _dedupe_and_pad(alts, rng, lambda: str(rng.randint(2, 50)))
            rng.shuffle(alts)

            enunciado = f"{nombre} analiza la siguiente secuencia: {seq_str}. ¿Qué número falta en el espacio en blanco?"
            svg_data = _generate_svg_seq_arithmetic(start if is_plus else (start - step*4), step, is_plus)

            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "expl": expl_str,
                "alts": alts,
                "metadata_visual": {"requiere_imagen": True, "svg_base64": svg_data},
                "errores_previstos": errores_previstos
            }

        elif lvl_id in (2, 12):
            start = rng.randint(1, 4)
            factor = rng.choice([2, 3, 5])
            ans = start * (factor ** 3)
            ans_str = str(ans)
            seq_str = f"{start}, {start*factor}, {start*(factor**2)}, ___"
            
            enunciado = f"{nombre} descubre una secuencia multiplicativa: {seq_str}. ¿Cuál es el término siguiente?"
            alts = [ans_str, str(start*(factor**2) + factor), str(ans * factor), str(ans - 1)]
            alts = _dedupe_and_pad(alts, rng, lambda: str(rng.randint(2, 200)))
            rng.shuffle(alts)
            
            errores_previstos[str(start*(factor**2) + factor)] = f"Sumaste {factor} en vez de multiplicar por {factor}."
            svg_data = _generate_svg_seq_geometric(start, factor)

            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "expl": f"El patrón es multiplicar por {factor}. {start*(factor**2)} × {factor} = {ans}.",
                "alts": alts,
                "metadata_visual": {"requiere_imagen": True, "svg_base64": svg_data},
                "errores_previstos": errores_previstos
            }

        else:
            # Interpolación (número oculto en el medio)
            start = rng.randint(5, 20)
            step = rng.randint(3, 7)
            vals = [start, start + step, start + step*2, start + step*3, start + step*4]
            missing_idx = 2
            ans_str = str(vals[missing_idx])
            
            display_seq = f"{vals[0]}, {vals[1]}, ___, {vals[3]}, {vals[4]}"
            enunciado = f"{nombre} encuentra una secuencia con un número oculto en el medio: {display_seq}. ¿Qué número debe ir en la casilla vacía?"
            
            alts = [ans_str, str(vals[1] + 1), str(vals[3] - 1), str(vals[1] + step*2)]
            alts = _dedupe_and_pad(alts, rng, lambda: str(rng.randint(5, 60)))
            rng.shuffle(alts)
            
            errores_previstos[str(vals[1] + step*2)] = "Sumaste dos veces la regla de un solo paso."
            svg_data = _generate_svg_seq_interpolation(vals, missing_idx)

            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "expl": f"Midiendo la diferencia entre {vals[3]} y {vals[4]}, la regla es +{step}. Luego {vals[1]} + {step} = {ans_str}.",
                "alts": alts,
                "metadata_visual": {"requiere_imagen": True, "svg_base64": svg_data},
                "errores_previstos": errores_previstos
            }

    elif mod_id == 2:
        if lvl_id in (1, 11):
            op1 = rng.randint(2, 4)
            op2 = rng.randint(2, 4)
            ans = op1 * op2
            ans_str = str(ans)
            
            enunciado = f"{nombre} arma un diagrama de árbol con {op1} tipos de helados y {op2} coberturas. ¿Cuántas combinaciones únicas se forman en total?"
            alts = [ans_str, str(op1 + op2), str(ans + 2), str(ans - 1)]
            alts = _dedupe_and_pad(alts, rng, lambda: str(rng.randint(2, 20)))
            rng.shuffle(alts)
            
            errores_previstos[str(op1 + op2)] = "Sumaste las opciones. En un árbol debes multiplicar las ramas."
            svg_data = _generate_svg_tree_diagram(op1, op2)

            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "expl": f"En el diagrama de árbol multiplicamos las ramas: {op1} × {op2} = {ans}.",
                "alts": alts,
                "metadata_visual": {"requiere_imagen": True, "svg_base64": svg_data},
                "errores_previstos": errores_previstos
            }

        elif lvl_id in (2, 12):
            op1 = rng.randint(3, 5)
            op2 = rng.randint(2, 4)
            op3 = rng.choice([2, 3])
            ans = op1 * op2 * op3
            ans_str = str(ans)
            
            ropa1 = rng.choice(ROPA_1)
            ropa2 = rng.choice(ROPA_2)
            ropa3 = rng.choice(ROPA_3)
            
            enunciado = f"{nombre} tiene {op1} {ropa1}, {op2} {ropa2} y {op3} par(es) de {ropa3}. Aplicando el Principio Multiplicativo, ¿cuántos atuendos completos puede formar?"
            alts = [ans_str, str(op1 + op2 + op3), str(op1 * op2), str(ans + 2)]
            alts = _dedupe_and_pad(alts, rng, lambda: str(rng.randint(5, 50)))
            rng.shuffle(alts)
            
            errores_previstos[str(op1 + op2 + op3)] = "Sumaste las categorías en vez de multiplicarlas."
            errores_previstos[str(op1 * op2)] = "Olvidaste multiplicar por la tercera opción de vestimenta."
            svg_data = _generate_svg_multiplicative_groups(op1, op2, op3)

            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "expl": f"Multiplicamos las 3 categorías: {op1} × {op2} × {op3} = {ans} combinaciones.",
                "alts": alts,
                "metadata_visual": {"requiere_imagen": True, "svg_base64": svg_data},
                "errores_previstos": errores_previstos
            }

        else:
            # Empaquetado Exacto (MCD)
            mcd_val = rng.choice([2, 3, 4, 5, 6])
            mult1 = rng.randint(2, 4)
            mult2 = rng.randint(3, 5)
            if mult1 == mult2:
                mult2 += 1
                
            num1 = mcd_val * mult1
            num2 = mcd_val * mult2
            ans_str = str(mcd_val)
            
            f1 = rng.choice(FRUTAS_1)
            f2 = rng.choice(FRUTAS_2)
            
            enunciado = f"{nombre} quiere armar canastas idénticas con {num1} {f1} y {num2} {f2} sin que sobre nada. ¿Cuál es la cantidad MÁXIMA de canastas que puede armar (MCD)?"
            alts = [ans_str, str(num1 + num2), str(min(num1, num2)), str(mcd_val * 2)]
            alts = _dedupe_and_pad(alts, rng, lambda: str(rng.randint(1, 15)))
            rng.shuffle(alts)
            
            errores_previstos[str(num1 + num2)] = "Sumaste el total de frutas en lugar de buscar el divisor común máximo."
            svg_data = _generate_svg_mcd_groups(num1, num2, mcd_val)

            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "expl": f"El Máximo Común Divisor entre {num1} y {num2} es {mcd_val}. Se pueden armar {mcd_val} canastas exactas.",
                "alts": alts,
                "metadata_visual": {"requiere_imagen": True, "svg_base64": svg_data},
                "errores_previstos": errores_previstos
            }

    else:
        if lvl_id in (1, 11):
            # Eventos Seguro, Posible, Imposible. Antes: 3 escenarios con números fijos
            # (6 canicas, 5 dulces, dado) → solo cambiaba el nombre. Ahora se aleatorizan
            # objeto, cantidades y contenedor (los colores se mantienen rojo/azul para
            # coincidir con la imagen de la urna).
            tipo_ev = rng.choice(["Seguro", "Imposible", "Posible", "Posible"])
            objs = [("canicas", "canica"), ("pelotas", "pelota"), ("fichas", "ficha"),
                    ("bolitas", "bolita"), ("esferas", "esfera"), ("cuentas", "cuenta")]
            obj_pl, obj_sg = rng.choice(objs)
            contenedor = rng.choice(CONTENEDORES)
            n1 = rng.randint(3, 9)
            if tipo_ev == "Seguro":
                enunciado = f"En un(a) {contenedor}, {nombre} tiene {n1} {obj_pl} y TODAS son rojas. Saca una sin mirar. ¿Qué tipo de evento es sacar una {obj_sg} ROJA?"
                ans_str = "Seguro"
                errores_previstos["Posible"] = f"Como todas son rojas, sacar una roja es 100% Seguro."
                balls = (n1, 0)
            elif tipo_ev == "Imposible":
                enunciado = f"En un(a) {contenedor}, {nombre} tiene {n1} {obj_pl}, todas rojas. Saca una sin mirar. ¿Qué tipo de evento es sacar una {obj_sg} AZUL?"
                ans_str = "Imposible"
                errores_previstos["Posible"] = f"No hay ninguna {obj_sg} azul, así que sacar una azul es Imposible."
                balls = (n1, 0)
            else:
                n2 = rng.randint(2, 6)
                color_preg = rng.choice(["ROJA", "AZUL"])
                enunciado = f"En un(a) {contenedor}, {nombre} tiene {n1} {obj_pl} rojas y {n2} {obj_pl} azules. Saca una sin mirar. ¿Qué tipo de evento es sacar una {obj_sg} {color_preg}?"
                ans_str = "Posible"
                errores_previstos["Seguro"] = "No es Seguro: también hay otras del otro color, así que solo es Posible."
                errores_previstos["Imposible"] = "Sí existen de ese color, así que no es Imposible: es Posible."
                balls = (n1, n2)

            alts = ["Seguro", "Posible", "Imposible"]
            svg_data = _generate_svg_urn_balls(balls[0], balls[1])

            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "expl": f"Es un evento {ans_str} según los casos favorables que existen en el/la {contenedor}.",
                "alts": alts,
                "metadata_visual": {"requiere_imagen": True, "svg_base64": svg_data},
                "errores_previstos": errores_previstos
            }

        elif lvl_id in (2, 12):
            rojas = rng.randint(2, 5)
            azules = rng.randint(2, 5)
            total = rojas + azules
            ans_str = f"{rojas}/{total}"
            contenedor = rng.choice(CONTENEDORES)
            
            enunciado = f"En un(a) {contenedor}, {nombre} guardó {rojas} esferas rojas y {azules} esferas azules. ¿Cuál es la probabilidad (Regla de Laplace) de sacar al azar una esfera ROJA?"
            alts = [ans_str, f"{azules}/{total}", f"{rojas}/{azules}", f"1/{total}"]
            # Cuando rojas==azules, "azules/total" coincide con la respuesta correcta
            # (confirmado en BD: preguntas con "3/6, 3/6" repetido) — el relleno
            # deduplicado se encarga de sustituirlo por otra fracción distinta.
            alts = _dedupe_and_pad(alts, rng, lambda: f"{rng.randint(1, total - 1)}/{total}")
            rng.shuffle(alts)
            
            errores_previstos[f"{azules}/{total}"] = "Calculaste la probabilidad de las azules en lugar de las rojas."
            errores_previstos[f"{rojas}/{azules}"] = "Dividiste rojas entre azules en vez de rojas entre el TOTAL."
            svg_data = _generate_svg_urn_balls(rojas, azules)

            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "expl": f"Casos favorables (rojas) = {rojas}. Casos totales = {rojas} + {azules} = {total}. Probabilidad = {ans_str}.",
                "alts": alts,
                "metadata_visual": {"requiere_imagen": True, "svg_base64": svg_data},
                "errores_previstos": errores_previstos
            }

        else:
            # Duelo de Probabilidades
            # Antes favA/totA/favB/totB eran constantes fijas (3/5 vs 1/5), así que
            # las 30 preguntas de esta sección (práctica + desafíos) eran literalmente
            # idénticas palabra por palabra. Se aleatorizan ambas fracciones y se
            # compara por multiplicación cruzada (evita errores de coma flotante),
            # descartando empates para que siempre haya una respuesta única.
            totA = rng.choice([4, 5, 6, 8, 10])
            totB = rng.choice([4, 5, 6, 8, 10])
            favA = rng.randint(1, totA - 1)
            favB = rng.randint(1, totB - 1)
            tries = 0
            while favA * totB == favB * totA and tries < 20:
                favB = rng.randint(1, totB - 1)
                tries += 1
            ans_str = "A" if favA * totB > favB * totA else "B"
            perdedor = "B" if ans_str == "A" else "A"

            enunciado = f"La Opción A tiene una probabilidad de {favA}/{totA} de ganar un premio, mientras que la Opción B tiene {favB}/{totB}. ¿Cuál opción ofrece MAYOR probabilidad de ganar? (A o B)"
            alts = ["A", "B"]
            errores_previstos[perdedor] = f"{favB}/{totB} no es mayor que {favA}/{totA}." if ans_str == "A" else f"{favA}/{totA} no es mayor que {favB}/{totB}."
            svg_data = _generate_svg_probability_duel(favA, totA, favB, totB)

            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "expl": f"Comparamos {favA}/{totA} y {favB}/{totB} multiplicando en cruz: {favA}×{totB}={favA*totB} vs {favB}×{totA}={favB*totA}. La Opción {ans_str} es superior.",
                "alts": alts,
                "metadata_visual": {"requiere_imagen": True, "svg_base64": svg_data},
                "errores_previstos": errores_previstos
            }

async def seed_configuracion_progreso_fase8(session: AsyncSession):
    print("Sembrando configuraciones de progreso Fase 8...")
    sections = [(m, l) for m in range(1, 4) for l in [1, 2, 3, 11, 12, 13]]
    for mod_id, lvl_id in sections:
        if lvl_id > 10:
            seccion_id = mod_id * 1000 + lvl_id
            num_questions = 25 if lvl_id < 13 else 10
            usa_crono = True
            if lvl_id == 11:
                tiempo = 30
            elif lvl_id == 12:
                tiempo = 45
            else:
                tiempo = 60
        else:
            seccion_id = mod_id * 100 + lvl_id
            num_questions = 15
            usa_crono = False
            tiempo = None
            
        config = ConfiguracionProgreso(
            fase_id=FASE9_ID,
            seccion=seccion_id,
            operacion=OperacionEnum.MIXTA,
            cantidad_requerida=num_questions,
            porcentaje_aprobacion=90,
            orden_desbloqueo=lvl_id,
            usa_cronometro=usa_crono,
            tiempo_default_segundos=tiempo
        )
        session.add(config)
    await session.commit()

async def seed_practica_pool_fase8(session: AsyncSession):
    print("Sembrando pool de práctica Fase 8 con alta variedad...")
    sections = [(m, l) for m in range(1, 4) for l in [1, 2, 3, 11, 12, 13]]
    
    for mod_id, lvl_id in sections:
        if lvl_id > 10:
            seccion_id = mod_id * 1000 + lvl_id
            num_questions = 25 if lvl_id < 13 else 10
        else:
            seccion_id = mod_id * 100 + lvl_id
            num_questions = 20
            
        for i in range(num_questions):
            # Práctica (lvl 1-3): cada índice es una FAMILIA con 1 original +
            # 2 variantes espejo (mismo estructura_padre_id, flag es_espejo) para
            # que el Bucle Espejo del router (busca hermanos con es_espejo True)
            # pueda disparar. Antes cada pregunta era familia de 1 y nunca
            # disparaba. Desafíos (lvl>10) cuentan aciertos, sin espejo.
            if lvl_id <= 3:
                fam_id = f"f8_m{mod_id}_l{lvl_id}_q{i:03d}"
                n_variantes = 3
            else:
                fam_id = None
                n_variantes = 1

            seen_enun = set()
            for v in range(n_variantes):
                # dedup: enunciado distinto entre variantes de la familia.
                q_data = None
                for intento in range(12):
                    rng = random.Random(FASE9_ID * 100000 + seccion_id * 1000 + i * 41 + v * 911 + intento * 101 + 17)
                    cand = await _gen_fase8_pool(rng, mod_id, lvl_id)
                    q_data = cand
                    if cand["enunciado"] not in seen_enun:
                        break
                seen_enun.add(q_data["enunciado"])

                payload = q_data.get("metadata_visual", {})
                payload["fase8"] = True
                # SISTEMA ESPEJO ELIMINADO: las variantes (enunciados distintos)
                # quedan como variedad del pool; ninguna se marca es_espejo.
                payload["es_espejo"] = False

                p = Pregunta(
                    fase_id=FASE9_ID, seccion=seccion_id, estructura_padre_id=fam_id,
                    operacion=OperacionEnum.MIXTA,
                    tipo_pregunta=TipoPreguntaEnum.MULTIPLE_OPCION, enunciado=q_data["enunciado"],
                    respuesta_correcta=q_data["respuesta_correcta"],
                    datos_numericos=payload,
                    errores_previstos=q_data.get("errores_previstos", {}),
                    explicacion_paso_a_paso={"titulo": "Resolución", "pasos": [{"orden": 1, "texto": q_data["expl"]}]},
                    estado=StatusEnum.ACTIVO
                )
                for idx, alt in enumerate(q_data["alts"]):
                    is_correct = (alt == q_data["respuesta_correcta"])
                    error_msg = q_data.get("errores_previstos", {}).get(alt, "Esa alternativa es incorrecta. Vuelve a intentarlo.") if not is_correct else None
                    p.alternativas.append(Alternativa(texto=alt, es_correcta=is_correct, orden=idx+1, tipo_error=TipoErrorEnum.CALCULO if not is_correct else None, feedback_error=error_msg))
                session.add(p)
    await session.commit()

async def run_fase8_seed():
    print("=" * 60)
    print("Iniciando inyección de datos semilla de FASE 8...")
    async with AsyncSessionLocal() as session:
        fase = await session.get(Fase, FASE9_ID)
        if not fase:
            fase = Fase(id=FASE9_ID, nombre="Secuencias, Combinatoria y Probabilidad", descripcion="Fase 8", orden=8, icono="🎲")
            session.add(fase)
            await session.commit()
            
        await clear_fase8_data(session)
        await seed_teoria_niveles_fase8(session)
        await seed_configuracion_progreso_fase8(session)
        await seed_practica_pool_fase8(session)
    print("FASE 8 COMPLETADA EXITOSAMENTE.")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_fase8_seed())
