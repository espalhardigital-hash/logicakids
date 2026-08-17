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

FASE7_ID = 7

# --- DICCIONARIOS DE CONTEXTO FASE 7 ---
NOMBRES = ["Andrés", "Lucía", "Martín", "Elena", "Tomás", "Julia", "Mateo", "Sofía", "Diego", "Valentina"]
LUGARES = ["parque", "zoológico", "museo", "colegio", "cine", "estadio", "biblioteca", "hospital", "supermercado"]
OBJETOS = ["brújula", "rosa de los vientos", "carta", "pista", "mapa del tesoro", "llave de oro"]

async def clear_fase7_data(session: AsyncSession):
    print("Purging existing Fase 7 data...")
    result = await session.execute(select(Pregunta.id).where(Pregunta.fase_id == FASE7_ID))
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
        
    await session.execute(delete(Intento).where(Intento.fase_id == FASE7_ID))
    await session.execute(delete(PoolAsignadoAlumno).where(PoolAsignadoAlumno.fase_id == FASE7_ID))
    await session.execute(delete(Pregunta).where(Pregunta.fase_id == FASE7_ID))
    await session.execute(delete(ConfiguracionProgreso).where(ConfiguracionProgreso.fase_id == FASE7_ID))
    await session.execute(delete(NivelTeoria).where(NivelTeoria.fase_id == FASE7_ID))
    await session.commit()
    print("Fase 7 data purged.")

async def seed_teoria_niveles_fase7(session: AsyncSession):
    print("Sembrando guión de textos para Fase 7...")
    from app.fase7.content_fase7 import niveles_teoria_fase7
    
    for data in niveles_teoria_fase7:
        nt = NivelTeoria(fase_id=FASE7_ID, **data)
        session.add(nt)
    await session.commit()

def _svg_to_base64(svg_str: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(svg_str.encode('utf-8')).decode('utf-8')

def _generate_svg_compass(direction: str) -> str:
    needle_map = {
        "N": '<polygon points="100,35 93,100 107,100" fill="#ef4444"/><polygon points="100,165 93,100 107,100" fill="#64748b"/>',
        "S": '<polygon points="100,165 93,100 107,100" fill="#ef4444"/><polygon points="100,35 93,100 107,100" fill="#64748b"/>',
        "E": '<polygon points="165,100 100,93 100,107" fill="#ef4444"/><polygon points="35,100 100,93 100,107" fill="#64748b"/>',
        "O": '<polygon points="35,100 100,93 100,107" fill="#ef4444"/><polygon points="165,100 100,93 100,107" fill="#64748b"/>'
    }
    needle_svg = needle_map.get(direction, needle_map["N"])
    
    svg = f"""<svg viewBox="0 0 200 200" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <circle cx="100" cy="100" r="85" fill="#0f172a" stroke="#14B8A6" stroke-width="4"/>
  <circle cx="100" cy="100" r="75" fill="none" stroke="#334155" stroke-dasharray="4 4" stroke-width="1"/>
  <text x="100" y="32" font-family="Arial" font-size="16" font-weight="900" fill="#14B8A6" text-anchor="middle">N</text>
  <text x="100" y="185" font-family="Arial" font-size="16" font-weight="900" fill="#14B8A6" text-anchor="middle">S</text>
  <text x="180" y="106" font-family="Arial" font-size="16" font-weight="900" fill="#14B8A6" text-anchor="middle">E</text>
  <text x="20" y="106" font-family="Arial" font-size="16" font-weight="900" fill="#14B8A6" text-anchor="middle">O</text>
  {needle_svg}
  <circle cx="100" cy="100" r="5" fill="#f8fafc"/>
</svg>"""
    return _svg_to_base64(svg)

def _generate_svg_vector_route(x: int, y: int) -> str:
    """SVG representativo para desplazamientos por calles/vectores (Mod 1 Nivel 2)."""
    svg = f"""<svg viewBox="0 0 220 180" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="220" height="180" rx="10" fill="#0f172a" stroke="#14B8A6" stroke-width="2"/>
  <line x1="30" y1="150" x2="190" y2="150" stroke="#334155" stroke-width="2"/>
  <line x1="30" y1="100" x2="190" y2="100" stroke="#334155" stroke-width="2"/>
  <line x1="30" y1="50" x2="190" y2="50" stroke="#334155" stroke-width="2"/>
  
  <line x1="30" y1="30" x2="30" y2="150" stroke="#334155" stroke-width="2"/>
  <line x1="85" y1="30" x2="85" y2="150" stroke="#334155" stroke-width="2"/>
  <line x1="140" y1="30" x2="140" y2="150" stroke="#334155" stroke-width="2"/>
  <line x1="190" y1="30" x2="190" y2="150" stroke="#334155" stroke-width="2"/>

  <circle cx="30" cy="150" r="6" fill="#38bdf8"/>
  <text x="30" y="170" font-family="Arial" font-size="11" font-weight="bold" fill="#38bdf8" text-anchor="middle">Inicio (0,0)</text>

  <line x1="30" y1="150" x2="140" y2="150" stroke="#14B8A6" stroke-width="3" stroke-dasharray="4 2"/>
  <text x="85" y="142" font-family="Arial" font-size="11" font-weight="bold" fill="#14B8A6" text-anchor="middle">{x} Este</text>

  <line x1="140" y1="150" x2="140" y2="50" stroke="#f59e0b" stroke-width="3" stroke-dasharray="4 2"/>
  <text x="155" y="100" font-family="Arial" font-size="11" font-weight="bold" fill="#f59e0b" text-anchor="start">{y} Norte</text>

  <circle cx="140" cy="50" r="7" fill="#ef4444"/>
  <text x="140" y="38" font-family="Arial" font-size="11" font-weight="bold" fill="#ef4444" text-anchor="middle">Destino</text>
</svg>"""
    return _svg_to_base64(svg)

def _generate_svg_cartesian(x1: int, y1: int, x2: int = None, y2: int = None) -> str:
    grid_lines = []
    for i in range(7):
        cx = 30 + i * 25
        grid_lines.append(f'<line x1="{cx}" y1="20" x2="{cx}" y2="180" stroke="#334155" stroke-width="1"/>')
        grid_lines.append(f'<text x="{cx}" y="195" font-family="Arial" font-size="10" fill="#64748b" text-anchor="middle">{i}</text>')
        
        cy = 180 - i * 25
        grid_lines.append(f'<line x1="30" y1="{cy}" x2="180" y2="{cy}" stroke="#334155" stroke-width="1"/>')
        grid_lines.append(f'<text x="20" y="{cy + 3}" font-family="Arial" font-size="10" fill="#64748b" text-anchor="end">{i}</text>')
        
    grid_lines_str = "\n  ".join(grid_lines)
    
    cx1 = 30 + x1 * 25
    cy1 = 180 - y1 * 25
    
    point_b_svg = ""
    path_line_svg = ""
    if x2 is not None and y2 is not None:
        cx2 = 30 + x2 * 25
        cy2 = 180 - y2 * 25
        point_b_svg = f"""
  <circle cx="{cx2}" cy="{cy2}" r="6" fill="#ef4444" stroke="#f8fafc" stroke-width="1.5"/>
  <text x="{cx2}" y="{cy2 - 10}" font-family="Arial" font-size="10" font-weight="bold" fill="#ef4444" text-anchor="middle">B</text>
"""
        path_line_svg = f"""
  <path d="M {cx1} {cy1} L {cx2} {cy1} L {cx2} {cy2}" fill="none" stroke="#e2e8f0" stroke-width="2" stroke-dasharray="4 4"/>
"""

    svg = f"""<svg viewBox="0 0 210 210" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <rect x="0" y="0" width="210" height="210" rx="8" fill="#0f172a"/>
  {grid_lines_str}
  <line x1="30" y1="180" x2="185" y2="180" stroke="#94a3b8" stroke-width="2"/>
  <line x1="30" y1="20" x2="30" y2="180" stroke="#94a3b8" stroke-width="2"/>
  <text x="195" y="184" font-family="Arial" font-size="11" font-weight="bold" fill="#94a3b8">X</text>
  <text x="27" y="12" font-family="Arial" font-size="11" font-weight="bold" fill="#94a3b8">Y</text>
  {path_line_svg}
  <circle cx="{cx1}" cy="{cy1}" r="6" fill="#0d9488" stroke="#f8fafc" stroke-width="1.5"/>
  <text x="{cx1}" y="{cy1 - 10}" font-family="Arial" font-size="10" font-weight="bold" fill="#0d9488" text-anchor="middle">A</text>
  {point_b_svg}
</svg>"""
    return _svg_to_base64(svg)

def _generate_svg_clock(hours: int, minutes: int) -> str:
    hour_angle = (hours % 12) * 30 + minutes * 0.5
    minute_angle = minutes * 6
    
    svg = f"""<svg viewBox="0 0 200 200" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <circle cx="100" cy="100" r="85" fill="#0f172a" stroke="#0F766E" stroke-width="4"/>
  <circle cx="100" cy="100" r="78" fill="none" stroke="#1e293b" stroke-width="1"/>
  
  <text x="100" y="32" font-family="Arial" font-size="14" font-weight="bold" fill="#94a3b8" text-anchor="middle">12</text>
  <text x="100" y="182" font-family="Arial" font-size="14" font-weight="bold" fill="#94a3b8" text-anchor="middle">6</text>
  <text x="175" y="105" font-family="Arial" font-size="14" font-weight="bold" fill="#94a3b8" text-anchor="middle">3</text>
  <text x="25" y="105" font-family="Arial" font-size="14" font-weight="bold" fill="#94a3b8" text-anchor="middle">9</text>

  <line x1="100" y1="100" x2="100" y2="60" stroke="#f8fafc" stroke-width="4" stroke-linecap="round" transform="rotate({hour_angle} 100 100)"/>
  <line x1="100" y1="100" x2="100" y2="42" stroke="#38bdf8" stroke-width="3" stroke-linecap="round" transform="rotate({minute_angle} 100 100)"/>
  
  <circle cx="100" cy="100" r="5" fill="#f8fafc"/>
</svg>"""
    return _svg_to_base64(svg)

def _generate_svg_time_addition(h1: int, m1: int, h2: int, m2: int, total_h: int, total_m: int) -> str:
    """SVG representativo de la suma de dos intervalos de tiempo (Mod 3 Nivel 3)."""
    svg = f"""<svg viewBox="0 0 280 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <rect x="5" y="5" width="270" height="130" rx="10" fill="#0f172a" stroke="#0F766E" stroke-width="2"/>
  
  <text x="140" y="30" font-family="Arial" font-size="13" font-weight="bold" fill="#38bdf8" text-anchor="middle">Aritmética de Tiempo (Suma)</text>
  
  <rect x="20" y="45" width="110" height="35" rx="6" fill="#1e293b" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="75" y="67" font-family="Arial" font-size="11" font-weight="bold" fill="#f8fafc" text-anchor="middle">Tramo 1: {h1}h {m1}m</text>

  <text x="140" y="68" font-family="Arial" font-size="16" font-weight="bold" fill="#f59e0b" text-anchor="middle">+</text>

  <rect x="150" y="45" width="110" height="35" rx="6" fill="#1e293b" stroke="#3b82f6" stroke-width="1.5"/>
  <text x="205" y="67" font-family="Arial" font-size="11" font-weight="bold" fill="#f8fafc" text-anchor="middle">Tramo 2: {h2}h {m2}m</text>

  <line x1="20" y1="95" x2="260" y2="95" stroke="#334155" stroke-width="1"/>

  <text x="140" y="118" font-family="Arial" font-size="12" font-weight="bold" fill="#10b981" text-anchor="middle">Total = {total_h}h {total_m}m</text>
</svg>"""
    return _svg_to_base64(svg)

def _generate_svg_schedule(line1_name: str, line1_t1: str, line1_t2: str, line2_name: str, line2_t1: str, line2_t2: str) -> str:
    svg = f"""<svg viewBox="0 0 300 150" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <rect x="5" y="5" width="290" height="140" rx="10" fill="#0f172a" stroke="#115E59" stroke-width="2"/>
  
  <rect x="15" y="15" width="80" height="25" rx="4" fill="#1e293b"/>
  <text x="55" y="32" font-family="Arial" font-size="11" font-weight="bold" fill="#14B8A6" text-anchor="middle">Línea</text>
  
  <rect x="105" y="15" width="80" height="25" rx="4" fill="#1e293b"/>
  <text x="145" y="32" font-family="Arial" font-size="11" font-weight="bold" fill="#14B8A6" text-anchor="middle">Salida 1</text>
  
  <rect x="195" y="15" width="80" height="25" rx="4" fill="#1e293b"/>
  <text x="235" y="32" font-family="Arial" font-size="11" font-weight="bold" fill="#14B8A6" text-anchor="middle">Salida 2</text>
  
  <text x="55" y="65" font-family="Arial" font-size="11" fill="#f8fafc" text-anchor="middle">{line1_name}</text>
  <text x="145" y="65" font-family="Arial" font-size="11" fill="#f8fafc" text-anchor="middle">{line1_t1}</text>
  <text x="235" y="65" font-family="Arial" font-size="11" fill="#f8fafc" text-anchor="middle">{line1_t2}</text>
  <line x1="15" y1="80" x2="285" y2="80" stroke="#334155" stroke-width="1"/>
  
  <text x="55" y="105" font-family="Arial" font-size="11" fill="#f8fafc" text-anchor="middle">{line2_name}</text>
  <text x="145" y="105" font-family="Arial" font-size="11" fill="#f8fafc" text-anchor="middle">{line2_t1}</text>
  <text x="235" y="105" font-family="Arial" font-size="11" fill="#f8fafc" text-anchor="middle">{line2_t2}</text>
  <line x1="15" y1="120" x2="285" y2="120" stroke="#334155" stroke-width="1"/>
</svg>"""
    return _svg_to_base64(svg)

def _generate_svg_transit_route(trip1: int, wait: int, trip2: int, total: int) -> str:
    """Diagrama de transbordo (Mod 4 Nivel 2)."""
    svg = f"""<svg viewBox="0 0 300 130" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <rect x="5" y="5" width="290" height="120" rx="10" fill="#0f172a" stroke="#115E59" stroke-width="2"/>
  <text x="150" y="25" font-family="Arial" font-size="12" font-weight="bold" fill="#14B8A6" text-anchor="middle">Calculadora de Transbordo</text>
  
  <circle cx="45" cy="65" r="16" fill="#3b82f6"/>
  <text x="45" y="69" font-family="Arial" font-size="10" font-weight="bold" fill="#fff" text-anchor="middle">Bus A</text>
  <text x="45" y="95" font-family="Arial" font-size="10" fill="#94a3b8" text-anchor="middle">{trip1} min</text>

  <line x1="61" y1="65" x2="114" y2="65" stroke="#64748b" stroke-width="2" stroke-dasharray="3 3"/>

  <circle cx="130" cy="65" r="16" fill="#f59e0b"/>
  <text x="130" y="69" font-family="Arial" font-size="10" font-weight="bold" fill="#fff" text-anchor="middle">Espera</text>
  <text x="130" y="95" font-family="Arial" font-size="10" fill="#94a3b8" text-anchor="middle">{wait} min</text>

  <line x1="146" y1="65" x2="199" y2="65" stroke="#64748b" stroke-width="2" stroke-dasharray="3 3"/>

  <circle cx="215" cy="65" r="16" fill="#10b981"/>
  <text x="215" y="69" font-family="Arial" font-size="10" font-weight="bold" fill="#fff" text-anchor="middle">Bus B</text>
  <text x="215" y="95" font-family="Arial" font-size="10" fill="#94a3b8" text-anchor="middle">{trip2} min</text>

  <text x="150" y="115" font-family="Arial" font-size="11" font-weight="bold" fill="#10b981" text-anchor="middle">Total: {total} min</text>
</svg>"""
    return _svg_to_base64(svg)

def _generate_svg_route_options(tA: int, tB: int, tC: int) -> str:
    """Diagrama de comparativa de opciones de GPS (Mod 4 Nivel 3)."""
    svg = f"""<svg viewBox="0 0 300 140" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <rect x="5" y="5" width="290" height="130" rx="10" fill="#0f172a" stroke="#115E59" stroke-width="2"/>
  <text x="150" y="25" font-family="Arial" font-size="12" font-weight="bold" fill="#14B8A6" text-anchor="middle">Optimizador de Ruta GPS</text>
  
  <rect x="25" y="40" width="70" height="40" rx="6" fill="#1e293b" stroke="#3b82f6" stroke-width="1"/>
  <text x="60" y="58" font-family="Arial" font-size="11" font-weight="bold" fill="#f8fafc" text-anchor="middle">Ruta A</text>
  <text x="60" y="73" font-family="Arial" font-size="10" fill="#94a3b8" text-anchor="middle">{tA} min</text>

  <rect x="115" y="40" width="70" height="40" rx="6" fill="#1e293b" stroke="#10b981" stroke-width="2"/>
  <text x="150" y="58" font-family="Arial" font-size="11" font-weight="bold" fill="#10b981" text-anchor="middle">Ruta B</text>
  <text x="150" y="73" font-family="Arial" font-size="10" fill="#10b981" text-anchor="middle">{tB} min ⭐</text>

  <rect x="205" y="40" width="70" height="40" rx="6" fill="#1e293b" stroke="#ef4444" stroke-width="1"/>
  <text x="240" y="58" font-family="Arial" font-size="11" font-weight="bold" fill="#f8fafc" text-anchor="middle">Ruta C</text>
  <text x="240" y="73" font-family="Arial" font-size="10" fill="#94a3b8" text-anchor="middle">{tC} min</text>

  <text x="150" y="105" font-family="Arial" font-size="10" font-style="italic" fill="#cbd5e1" text-anchor="middle">Selecciona la opción con menor tiempo total</text>
</svg>"""
    return _svg_to_base64(svg)

def _dedupe_and_pad(alts: list, rng: random.Random, pad_fn) -> list:
    """Devuelve exactamente 4 alternativas string DISTINTAS. `pad_fn` genera un
    candidato nuevo en el mismo formato temático (coordenada, hora, número)
    cuando faltan opciones tras deduplicar — evita el bug de opciones repetidas
    (p.ej. un distractor "swap XY" que coincide con la respuesta cuando X==Y).
    """
    out = list(dict.fromkeys(alts))  # dedupe preservando orden
    attempts = 0
    while len(out) < 4 and attempts < 50:
        candidate = pad_fn()
        if candidate not in out:
            out.append(candidate)
        attempts += 1
    return out


async def _gen_fase7_pool(rng: random.Random, mod_id: int, lvl_id: int) -> dict:
    nombre = rng.choice(NOMBRES)
    errores_previstos = {}
    
    if mod_id == 1:
        if lvl_id in (1, 11):
            directions = ["Norte", "Este", "Sur", "Oeste"]
            dir_abbrev = {"Norte": "N", "Este": "E", "Sur": "S", "Oeste": "O"}
            start_idx = rng.randint(0, 3)
            turn_right = rng.choice([True, False])
            turn_deg = rng.choice([90, 180, 270])
            
            steps = turn_deg // 90
            if not turn_right:
                steps = -steps
            end_idx = (start_idx + steps) % 4
            
            start_dir = directions[start_idx]
            end_dir = directions[end_idx]
            
            direction_word = "derecha" if turn_right else "izquierda"
            # Variedad de SITUACIÓN: exploradores, marineros, robots... girando con la brújula.
            personaje = rng.choice([nombre, "el explorador", "la capitana del barco", "el robot",
                                    "la excursionista", "el piloto del dron", "la scout"])
            objeto = rng.choice(OBJETOS)
            plantillas = [
                f"{personaje.capitalize()} mira su {objeto} apuntando al {start_dir} y gira {turn_deg}° hacia la {direction_word}. ¿Hacia qué dirección termina mirando?",
                f"Estás mirando al {start_dir} en el mapa. Si haces un giro de {turn_deg}° hacia la {direction_word}, ¿a qué punto cardinal quedas mirando?",
                f"{personaje.capitalize()} apunta al {start_dir} y rota {turn_deg}° a la {direction_word}. ¿Cuál es su nueva orientación?",
            ]
            enunciado = rng.choice(plantillas)

            ans_str = end_dir
            alts = list(directions)
            
            errores_previstos[start_dir] = "No realizaste ningún giro. Debes cambiar de dirección."
            opposite_idx = (start_idx + 2) % 4
            opposite_dir = directions[opposite_idx]
            if opposite_dir != ans_str:
                errores_previstos[opposite_dir] = f"Esa es la dirección opuesta al {start_dir}."
            
            svg_data = _generate_svg_compass(dir_abbrev[start_dir])
            
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "expl": f"Comenzando en el {start_dir}, al girar {turn_deg} grados a la {direction_word}, terminas apuntando al {end_dir}.",
                "alts": alts,
                "metadata_visual": {"requiere_imagen": True, "svg_base64": svg_data},
                "errores_previstos": errores_previstos
            }
            
        elif lvl_id in (2, 12):
            x = rng.randint(1, 5)
            y = rng.randint(1, 5)
            lugar = rng.choice(LUGARES)
            enunciado = f"{nombre} comienza en el punto (0,0). Camina {x} pasos al Este y luego {y} pasos al Norte para ir al {lugar}. ¿Cuántos pasos caminó en total?"
            ans_str = str(x + y)
            
            alts = [ans_str, str(abs(x - y)), str(x * y), str(x + y + 2)]
            alts = _dedupe_and_pad(alts, rng, lambda: str(rng.randint(2, 15)))
            rng.shuffle(alts)
            
            errores_previstos[str(abs(x - y))] = "Restaste los pasos en lugar de sumarlos para obtener la distancia total."
            errores_previstos[str(x * y)] = "Multiplicaste los pasos en lugar de sumarlos."
            
            svg_data = _generate_svg_vector_route(x, y)
            
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "expl": f"La distancia total recorrida es la suma de los pasos: {x} Este + {y} Norte = {x + y} pasos.",
                "alts": alts,
                "metadata_visual": {"requiere_imagen": True, "svg_base64": svg_data},
                "errores_previstos": errores_previstos
            }
            
        else:
            directions = ["Norte", "Este", "Sur", "Oeste"]
            dir_abbrev = {"Norte": "N", "Este": "E", "Sur": "S", "Oeste": "O"}
            start_dir_idx = rng.randint(0, 3)
            start_dir = directions[start_dir_idx]

            # Nivel avanzado: ambos sentidos de giro y los 3 ángulos, con vocabulario
            # "sentido horario/antihorario" (antes solo 180/270 a la derecha → 8 combos).
            deg = rng.choice([90, 180, 270])
            horario = rng.choice([True, False])
            steps = (deg // 90) if horario else -(deg // 90)
            end_dir_idx = (start_dir_idx + steps) % 4
            end_dir = directions[end_dir_idx]
            sentido = "sentido horario (a la derecha)" if horario else "sentido antihorario (a la izquierda)"

            personaje = rng.choice([nombre, "el capitán", "la exploradora", "el timonel", "la astronauta"])
            plantillas = [
                f"{personaje.capitalize()} mira hacia el {start_dir} y gira {deg}° en {sentido}. ¿Hacia dónde termina mirando?",
                f"Partiendo del {start_dir}, si giras {deg}° en {sentido}, ¿a qué punto cardinal llegas?",
                f"La brújula de {personaje} apunta al {start_dir}. Tras rotar {deg}° en {sentido}, ¿cuál es la nueva dirección?",
            ]
            enunciado = rng.choice(plantillas)
            ans_str = end_dir
            alts = list(directions)
            
            svg_data = _generate_svg_compass(dir_abbrev[start_dir])
            
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "expl": f"Al girar {deg}° en {sentido} desde el {start_dir}, terminas apuntando al {end_dir}.",
                "alts": alts,
                "metadata_visual": {"requiere_imagen": True, "svg_base64": svg_data},
                "errores_previstos": errores_previstos
            }

    elif mod_id == 2:
        if lvl_id in (1, 11):
            x = rng.randint(1, 5)
            y = rng.randint(1, 5)
            objeto = rng.choice(OBJETOS)
            enunciado = f"Un cofre con una {objeto} está en el punto A. Si está en la columna X={x} y fila Y={y}, ¿cuál es su coordenada (X,Y)?"
            ans_str = f"({x},{y})"
            # Distractor "orden invertido" (y,x): si x==y coincide con la respuesta
            # correcta (swap de un punto simétrico no cambia nada) — se rellena con
            # coordenadas cercanas distintas en su lugar.
            alts = [f"({x},{y})", f"({x + 1},{y})", f"({x},{y + 1})"]
            if x != y:
                alts.append(f"({y},{x})")
                errores_previstos[f"({y},{x})"] = "Confundiste el orden. Recuerda que el eje horizontal X va primero y el vertical Y va después: (X, Y)."
            alts = _dedupe_and_pad(alts, rng, lambda: f"({rng.randint(0, 8)},{rng.randint(0, 8)})")
            
            svg_data = _generate_svg_cartesian(x, y)
            
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "expl": f"Eje horizontal X es {x}, eje vertical Y es {y}. Coordenada correcta: ({x},{y}).",
                "alts": alts,
                "metadata_visual": {"requiere_imagen": True, "svg_base64": svg_data},
                "errores_previstos": errores_previstos
            }
        elif lvl_id in (2, 12):
            x = rng.randint(1, 3)
            y = rng.randint(1, 3)
            dx = rng.randint(1, 3)
            dy = rng.randint(1, 3)
            
            _plantillas_coord = [
                f"Estás en el punto A({x},{y}). Te trasladas {dx} unidades a la derecha y {dy} unidades hacia arriba. ¿Cuál es tu nueva coordenada (X,Y)?",
                f"Un robot parte de la casilla ({x},{y}) y avanza {dx} casillas a la derecha y {dy} hacia arriba. ¿En qué coordenada (X,Y) queda?",
                f"En el mapa del tesoro, empiezas en ({x},{y}) y caminas {dx} pasos a la derecha y {dy} pasos hacia arriba. ¿Cuál es la coordenada (X,Y) final?",
                f"Una nave está en ({x},{y}). Se mueve {dx} unidades a la derecha y {dy} unidades hacia arriba. ¿Cuál es su nueva posición (X,Y)?",
            ]
            enunciado = rng.choice(_plantillas_coord)
            new_x = x + dx
            new_y = y + dy
            ans_str = f"({new_x},{new_y})"
            # Distractor "orden invertido" (new_y,new_x): si new_x==new_y coincide
            # con la respuesta correcta — se omite y se rellena con otra coordenada.
            alts = [f"({new_x},{new_y})", f"({x - dx},{y - dy})", f"({x + dx},{y})"]
            if new_x != new_y:
                alts.append(f"({new_y},{new_x})")
            errores_previstos[f"({x - dx},{y - dy})"] = "Restaste en lugar de sumar. Ir a la derecha y arriba aumenta los valores X e Y."
            alts = _dedupe_and_pad(alts, rng, lambda: f"({rng.randint(0, 8)},{rng.randint(0, 8)})")
            
            svg_data = _generate_svg_cartesian(x, y, new_x, new_y)
            
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "expl": f"Sumamos a la X: {x} + {dx} = {new_x}. Sumamos a la Y: {y} + {dy} = {new_y}. Queda ({new_x},{new_y}).",
                "alts": alts,
                "metadata_visual": {"requiere_imagen": True, "svg_base64": svg_data},
                "errores_previstos": errores_previstos
            }
        else:
            x1 = rng.randint(1, 2)
            y1 = rng.randint(1, 2)
            x2 = rng.randint(4, 5)
            y2 = rng.randint(4, 5)
            
            dist_x = abs(x2 - x1)
            dist_y = abs(y2 - y1)
            ans = dist_x + dist_y
            ans_str = str(ans)
            
            lugar = rng.choice(LUGARES)
            enunciado = f"Calcula la distancia Manhattan (suma de pasos horizontales y verticales) entre A({x1},{y1}) y el {lugar} en B({x2},{y2})."
            
            alts = [ans_str, str(ans - 1), str(ans + 1), str(dist_x * dist_y)]
            alts = _dedupe_and_pad(alts, rng, lambda: str(rng.randint(2, 12)))
            rng.shuffle(alts)
            
            svg_data = _generate_svg_cartesian(x1, y1, x2, y2)
            
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "expl": f"Distancia horizontal: |{x2} - {x1}| = {dist_x}. Distancia vertical: |{y2} - {y1}| = {dist_y}. Suma: {dist_x} + {dist_y} = {ans}.",
                "alts": alts,
                "metadata_visual": {"requiere_imagen": True, "svg_base64": svg_data},
                "errores_previstos": errores_previstos
            }
            
    elif mod_id == 3:
        if lvl_id in (1, 11):
            hours = rng.randint(1, 12)
            minutes = rng.choice([0, 15, 30, 45])
            
            if minutes == 0:
                minutes_str = "00"
                minutes_lbl = "12"
            else:
                minutes_str = str(minutes)
                minutes_lbl = str(minutes // 5)
                
            ans_str = f"{hours}:{minutes_str}"
            enunciado = f"Mira el reloj. Si la aguja corta apunta al número {hours} y la larga apunta al número {minutes_lbl}, ¿qué hora marca?"
            
            alt_hours = (hours + 1) if hours < 12 else 1
            alts = [ans_str, f"{hours}:{(minutes+15)%60:02d}", f"{alt_hours}:{minutes_str}", f"{hours}:05"]
            alts = _dedupe_and_pad(alts, rng, lambda: f"{rng.randint(1, 12)}:{rng.choice([10, 20, 40]):02d}")
            rng.shuffle(alts)
            
            svg_data = _generate_svg_clock(hours, minutes)
            
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "expl": f"La aguja corta marca la hora ({hours}) y la larga los minutos ({minutes}m). Son las {ans_str}.",
                "alts": alts,
                "metadata_visual": {"requiere_imagen": True, "svg_base64": svg_data},
                "errores_previstos": errores_previstos
            }
        elif lvl_id in (2, 12):
            # Antes: solo 12h PM → 24h, en punto (:00), 11 combos. Ahora: dos sentidos
            # de conversión, con minutos y contextos reales (tren, película, vuelo...).
            minutes = rng.choice([0, 0, 15, 30, 45])
            mm = f"{minutes:02d}"
            contexto = rng.choice(["el tren sale", "la película empieza", "la alarma suena", "el partido comienza",
                                   "la tienda cierra", "el vuelo despega", "la clase termina", "el concierto arranca"])
            if rng.random() < 0.55:
                # 12h PM → 24h
                hours_12 = rng.randint(1, 11)
                hours_24 = hours_12 + 12
                ans_str = f"{hours_24}:{mm}"
                enunciado = f"En el reloj de 12 horas, {contexto} a las {hours_12}:{mm} PM. ¿Cuál es esa hora en formato de 24 horas?"
                expl = f"A una hora PM se le suman 12: {hours_12} + 12 = {hours_24}. Queda {hours_24}:{mm}."
                alts = [ans_str, f"{hours_12}:{mm}", f"{(hours_12 + 10) % 24}:{mm}", f"{hours_24 + 1}:{mm}"]
                errores_previstos[f"{hours_12}:{mm}"] = "Olvidaste sumar 12 a la hora PM para pasar a 24 horas."
                svg_hour = hours_12
            else:
                # 24h → 12h PM
                hours_24 = rng.randint(13, 23)
                hours_12 = hours_24 - 12
                ans_str = f"{hours_12}:{mm} PM"
                enunciado = f"El horario de 24 horas indica que {contexto} a las {hours_24}:{mm}. ¿Cuál es esa hora en formato de 12 horas (con AM/PM)?"
                expl = f"Como pasa del mediodía, restamos 12: {hours_24} - 12 = {hours_12}. Queda {hours_12}:{mm} PM."
                alts = [ans_str, f"{hours_24}:{mm} PM", f"{hours_12}:{mm} AM", f"{hours_12 + 1}:{mm} PM"]
                errores_previstos[f"{hours_12}:{mm} AM"] = "Después del mediodía es PM, no AM."
                svg_hour = hours_12
            alts = _dedupe_and_pad(alts, rng, lambda: f"{rng.randint(1, 12)}:{rng.choice(['00','15','30','45'])}")

            svg_data = _generate_svg_clock(svg_hour, minutes)

            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "expl": expl,
                "alts": alts,
                "metadata_visual": {"requiere_imagen": True, "svg_base64": svg_data},
                "errores_previstos": errores_previstos
            }
        else:
            hours1 = rng.randint(1, 2)
            mins1 = rng.choice([30, 40, 45, 50])
            hours2 = rng.randint(1, 2)
            mins2 = rng.choice([20, 30, 40, 45])
            
            total_mins = mins1 + mins2
            total_hours = hours1 + hours2 + (total_mins // 60)
            rem_mins = total_mins % 60
            
            ans_str = f"{total_hours}h {rem_mins}m"
            _plantillas_tiempo = [
                f"Un viaje dura {hours1}h {mins1}m y el siguiente tramo dura {hours2}h {mins2}m. ¿Cuánto dura en total? (Formato: Xh Ym)",
                f"Una película dura {hours1}h {mins1}m y luego hay un documental de {hours2}h {mins2}m. ¿Cuánto tiempo suman las dos? (Formato: Xh Ym)",
                f"Marta estudió {hours1}h {mins1}m por la mañana y {hours2}h {mins2}m por la tarde. ¿Cuánto estudió en total? (Formato: Xh Ym)",
                f"Un tren tarda {hours1}h {mins1}m hasta la primera parada y {hours2}h {mins2}m hasta la segunda. ¿Cuál es el tiempo total? (Formato: Xh Ym)",
            ]
            enunciado = rng.choice(_plantillas_tiempo)
            
            wrong_hours = hours1 + hours2
            wrong_mins = mins1 + mins2
            alts = [ans_str, f"{wrong_hours}h {wrong_mins}m", f"{total_hours + 1}h {rem_mins}m", f"{total_hours}h {(rem_mins + 10) % 60}m"]
            alts = _dedupe_and_pad(alts, rng, lambda: f"{rng.randint(2, 5)}h {rng.choice([10, 15, 25])}m")
            rng.shuffle(alts)
            
            errores_previstos[f"{wrong_hours}h {wrong_mins}m"] = "Sumaste minutos directo, pero cada 60m se convierten en 1 hora."
            
            svg_data = _generate_svg_time_addition(hours1, mins1, hours2, mins2, total_hours, rem_mins)
            
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "expl": f"Horas: {hours1}+{hours2}={hours1+hours2}h. Minutos: {mins1}+{mins2}={total_mins}m (1h {rem_mins}m). Total = {total_hours}h {rem_mins}m.",
                "alts": alts,
                "metadata_visual": {"requiere_imagen": True, "svg_base64": svg_data},
                "errores_previstos": errores_previstos
            }
            
    else:
        line1_name = "Línea A"
        line2_name = "Línea B"

        if lvl_id in (1, 11):
            # Antes esta pregunta era 100% estática (horarios fijos "08:15"/"08:45"),
            # repitiéndose idéntica en las 45 filas de práctica+desafío. Se aleatoriza
            # la hora de salida y la frecuencia para dar variedad real.
            start_h = rng.randint(6, 11)
            start_m = rng.choice([0, 5, 10, 15, 20, 30, 40, 45])
            freq = rng.choice([15, 20, 25, 30, 40])
            end_total = start_h * 60 + start_m + freq
            end_h, end_m = divmod(end_total, 60)
            t1_1 = f"{start_h:02d}:{start_m:02d}"
            t1_2 = f"{end_h:02d}:{end_m:02d}"
            t2_1 = f"{start_h:02d}:{(start_m + 5) % 60:02d}"
            t2_2_total = start_h * 60 + (start_m + 5) % 60 + rng.choice([20, 25, 35])
            t2_2_h, t2_2_m = divmod(t2_2_total, 60)
            t2_2 = f"{t2_2_h:02d}:{t2_2_m:02d}"

            _plantillas_freq = [
                f"Según el horario, la Línea A sale a las {t1_1} y luego a las {t1_2}. ¿Cuál es la frecuencia (diferencia en minutos) de la Línea A?",
                f"El primer autobús pasa a las {t1_1} y el siguiente a las {t1_2}. ¿Cada cuántos minutos pasa el autobús?",
                f"Un tren sale a las {t1_1} y el próximo a las {t1_2}. ¿Cuántos minutos hay entre un tren y el siguiente?",
                f"En la estación, un metro llega a las {t1_1} y el siguiente a las {t1_2}. ¿Cuál es el intervalo en minutos?",
            ]
            enunciado = rng.choice(_plantillas_freq)
            ans_str = str(freq)
            alts = [ans_str, str(freq + 15), str(max(5, freq - 15)), str(freq + 30)]
            alts = _dedupe_and_pad(alts, rng, lambda: str(rng.choice([10, 15, 20, 25, 30, 35, 40, 45, 50, 60])))

            errores_previstos[str(max(5, freq - 15))] = f"De las {t1_1} a las {t1_2} transcurren {freq} minutos, no menos."

            svg_data = _generate_svg_schedule(line1_name, t1_1, t1_2, line2_name, t2_1, t2_2)

            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "expl": f"Restamos las horas de salida: {t1_2} - {t1_1} = {freq} minutos.",
                "alts": alts,
                "metadata_visual": {"requiere_imagen": True, "svg_base64": svg_data},
                "errores_previstos": errores_previstos
            }
        elif lvl_id in (2, 12):
            # Rangos ampliados y medios de transporte variados (antes 18 combos fijos).
            trip1 = rng.randint(8, 25)
            wait = rng.choice([5, 8, 10, 12, 15])
            trip2 = rng.randint(10, 30)
            total = trip1 + wait + trip2
            v1, parada, v2 = rng.choice([
                ("bus", "la parada", "metro"), ("metro", "la estación", "tranvía"),
                ("tren", "el andén", "autobús"), ("bus A", "la parada", "bus B"),
                ("colectivo", "la esquina", "subte"), ("ferry", "el muelle", "bus"),
            ])
            enunciado = f"{nombre} viaja {trip1} minutos en {v1}, espera {wait} minutos en {parada} y viaja {trip2} minutos en {v2}. ¿Cuánto tardó su trayecto total en minutos?"
            ans_str = str(total)
            alts = [ans_str, str(trip1 + trip2), str(total + 5), str(total - 5)]
            alts = _dedupe_and_pad(alts, rng, lambda: str(rng.randint(max(1, total - 20), total + 20)))

            errores_previstos[str(trip1 + trip2)] = "No sumaste el tiempo muerto de espera en la parada."
            
            svg_data = _generate_svg_transit_route(trip1, wait, trip2, total)
            
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "expl": f"Sumamos todo: {trip1} + {wait} + {trip2} = {total} minutos.",
                "alts": alts,
                "metadata_visual": {"requiere_imagen": True, "svg_base64": svg_data},
                "errores_previstos": errores_previstos
            }
        else:
            tA = rng.randint(25, 30)
            tB = rng.randint(15, 20)
            tC = rng.randint(35, 40)
            
            enunciado = f"Tienes tres opciones: Opción A tarda {tA} min, Opción B tarda {tB} min, y Opción C tarda {tC} min. ¿Cuál es la opción óptima para llegar más rápido? (A, B o C)"
            ans_str = "B"
            alts = ["A", "B", "C"]
            
            errores_previstos["A"] = f"La opción A ({tA}m) es más lenta que la opción B ({tB}m)."
            errores_previstos["C"] = f"La opción C ({tC}m) es la más lenta de todas."
            
            svg_data = _generate_svg_route_options(tA, tB, tC)
            
            return {
                "enunciado": enunciado,
                "respuesta_correcta": ans_str,
                "expl": f"La opción B es la más rápida ya que tarda {tB} minutos en total.",
                "alts": alts,
                "metadata_visual": {"requiere_imagen": True, "svg_base64": svg_data},
                "errores_previstos": errores_previstos
            }

async def seed_configuracion_progreso_fase7(session: AsyncSession):
    print("Sembrando configuraciones de progreso Fase 7...")
    sections = [(m, l) for m in range(1, 5) for l in [1, 2, 3, 11, 12, 13]]
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
            fase_id=FASE7_ID,
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

async def seed_practica_pool_fase7(session: AsyncSession):
    print("Sembrando pool de práctica Fase 7 con alta variedad...")
    sections = [(m, l) for m in range(1, 5) for l in [1, 2, 3, 11, 12, 13]]
    
    for mod_id, lvl_id in sections:
        if lvl_id > 10:
            seccion_id = mod_id * 1000 + lvl_id
            num_questions = 25 if lvl_id < 13 else 10
        else:
            seccion_id = mod_id * 100 + lvl_id
            num_questions = 20
            
        for i in range(num_questions):
            # Práctica (lvl 1-3): cada índice es una FAMILIA con 1 original +
            # 2 variantes espejo (mismo estructura_padre_id, flag es_espejo). El
            # Bucle Espejo del router busca hermanos con datos_numericos.es_espejo
            # is True; antes cada pregunta era familia de 1 y el espejo NUNCA
            # disparaba (0 hermanos). Desafíos (lvl>10) no usan espejo (cuentan
            # aciertos), así que quedan como familia nula.
            if lvl_id <= 3:
                fam_id = f"f7_m{mod_id}_l{lvl_id}_q{i:03d}"
                n_variantes = 3
            else:
                fam_id = None
                n_variantes = 1

            for v in range(n_variantes):
                rng = random.Random(FASE7_ID * 100000 + seccion_id * 1000 + i * 37 + v * 911 + 13)
                q_data = await _gen_fase7_pool(rng, mod_id, lvl_id)

                payload = q_data.get("metadata_visual", {})
                payload["fase7"] = True
                if lvl_id <= 3:
                    payload["es_espejo"] = v > 0

                p = Pregunta(
                    fase_id=FASE7_ID, seccion=seccion_id, estructura_padre_id=fam_id,
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

async def run_fase7_seed():
    print("=" * 60)
    print("Iniciando inyección de datos semilla de FASE 7...")
    async with AsyncSessionLocal() as session:
        fase = await session.get(Fase, FASE7_ID)
        if not fase:
            fase = Fase(id=FASE7_ID, nombre="Coordenadas, Rutas y Tiempo", descripcion="Fase 7", orden=7, icono="🧭")
            session.add(fase)
            await session.commit()
            
        await clear_fase7_data(session)
        await seed_teoria_niveles_fase7(session)
        await seed_configuracion_progreso_fase7(session)
        await seed_practica_pool_fase7(session)
    print("FASE 7 COMPLETADA EXITOSAMENTE.")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(run_fase7_seed())
