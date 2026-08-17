"""
Auditoría genérica de una fase contra el Postgres local.
Usa SQL crudo (evita validación de Enum al leer). Reutilizable: python _audit_fase.py <fase_id>

Chequea los arquetipos del método razonamiento_profundo:
  - tipo_error con valores fuera de TipoErrorEnum (bug de frontera seed->lectura)
  - lectura ORM de Alternativa (¿crashea por enum inválido?)
  - estructura_padre_id en práctica (¿progreso posible?)
  - respuestas degeneradas (respuesta impresa en el enunciado)
  - respuestas no enteras en preguntas numéricas
  - distractores duplicados / doble-correcta / respuesta ausente de las opciones
  - variedad de enunciados por sección
  - variantes espejo por familia
  - respuestas de texto guardadas como RESPUESTA_NUMERICA
"""
import asyncio
import re
import sys
import unicodedata

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from sqlalchemy import text
from app.db.session import engine, AsyncSessionLocal
from app.models.enums import TipoErrorEnum

VALID_TIPO_ERROR = {e.value for e in TipoErrorEnum} | {e.name for e in TipoErrorEnum}


def is_numeric(s):
    if s is None:
        return False
    s = str(s).strip().replace(",", ".")
    try:
        float(s)
        return True
    except ValueError:
        return False


def norm_text(s):
    # quita números y espacios múltiples para medir variedad estructural
    s = s or ""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"\d+([.,]\d+)?", "#", s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


async def main(fase_id):
    print(f"\n{'='*70}\n AUDITORÍA FASE {fase_id}\n{'='*70}")
    async with engine.connect() as conn:
        # Conteos por sección
        rows = (await conn.execute(text(
            "SELECT seccion, count(*) FROM preguntas WHERE fase_id=:f GROUP BY seccion ORDER BY seccion"
        ), {"f": fase_id})).all()
        total = sum(r[1] for r in rows)
        print(f"\n[1] Preguntas: {total} en {len(rows)} secciones")
        secs = [r[0] for r in rows]
        print("    secciones:", secs)

        # tipo_error fuera del enum
        te = (await conn.execute(text(
            "SELECT DISTINCT a.tipo_error FROM alternativas a JOIN preguntas p ON a.pregunta_id=p.id "
            "WHERE p.fase_id=:f AND a.tipo_error IS NOT NULL"
        ), {"f": fase_id})).all()
        stored = {r[0] for r in te}
        invalid = sorted(stored - VALID_TIPO_ERROR)
        print(f"\n[2] tipo_error distintos en BD: {sorted(stored)}")
        if invalid:
            cnt = (await conn.execute(text(
                "SELECT count(*) FROM alternativas a JOIN preguntas p ON a.pregunta_id=p.id "
                "WHERE p.fase_id=:f AND a.tipo_error = ANY(:vals)"
            ), {"f": fase_id, "vals": invalid})).scalar()
            print(f"    *** {len(invalid)} valores INVÁLIDOS (no en TipoErrorEnum): {invalid} -> {cnt} alternativas ***")
        else:
            print("    OK: todos válidos")

        # estructura_padre_id en práctica (secciones de 3 dígitos xy1..xy3 => práctica)
        practica = [s for s in secs if s < 1000]  # práctica = 101..403
        if practica:
            nulls = (await conn.execute(text(
                "SELECT count(*) FROM preguntas WHERE fase_id=:f AND seccion = ANY(:s) AND estructura_padre_id IS NULL"
            ), {"f": fase_id, "s": practica})).scalar()
            fams = (await conn.execute(text(
                "SELECT count(DISTINCT estructura_padre_id) FROM preguntas WHERE fase_id=:f AND seccion = ANY(:s)"
            ), {"f": fase_id, "s": practica})).scalar()
            print(f"\n[3] Práctica: {nulls} preguntas con estructura_padre_id NULL; {fams} familias distintas")
            if nulls:
                print("    *** PROGRESO IMPOSIBLE si el router cuenta DISTINCT estructura_padre_id ***")

        # variantes espejo por familia (práctica)
        if practica:
            dist = (await conn.execute(text(
                "SELECT n_var, count(*) FROM (SELECT estructura_padre_id, count(*) n_var FROM preguntas "
                "WHERE fase_id=:f AND seccion = ANY(:s) AND estructura_padre_id IS NOT NULL "
                "GROUP BY estructura_padre_id) t GROUP BY n_var ORDER BY n_var"
            ), {"f": fase_id, "s": practica})).all()
            print(f"\n[4] Distribución variantes por familia (práctica): {[(r[0], r[1]) for r in dist]}")

        # Todas las preguntas con sus datos
        allq = (await conn.execute(text(
            "SELECT id, seccion, tipo_pregunta, enunciado, respuesta_correcta FROM preguntas WHERE fase_id=:f"
        ), {"f": fase_id})).all()

        # respuestas no enteras en preguntas numéricas
        non_int = []
        text_in_num = []
        for q in allq:
            tp = str(q[2])
            if "numerica" in tp.lower() or "numeric" in tp.lower():
                rc = str(q[4]).strip().replace(",", ".")
                if is_numeric(rc):
                    v = float(rc)
                    if abs(v - round(v)) > 1e-9:
                        non_int.append((q[0], q[1], q[4]))
                else:
                    text_in_num.append((q[0], q[1], q[4]))
        print(f"\n[5] Respuestas NO enteras en preguntas numéricas: {len(non_int)}")
        for r in non_int[:8]:
            print("    ", r)
        print(f"[6] Respuestas de TEXTO en preguntas numéricas: {len(text_in_num)}")
        for r in text_in_num[:8]:
            print("    ", r)

        # degeneradas: respuesta numérica aparece como token aislado en enunciado
        degen = []
        for q in allq:
            rc = str(q[4]).strip()
            if is_numeric(rc):
                rc_norm = rc.replace(",", ".")
                # entero: buscar token aislado
                if re.search(r"(?<![\d.,])" + re.escape(rc) + r"(?![\d.,])", q[3] or ""):
                    degen.append((q[0], q[1], rc, (q[3] or "")[:70]))
        print(f"\n[7] Respuestas impresas como token en el enunciado (degeneradas): {len(degen)}")
        for r in degen[:8]:
            print("    ", r)

        # alternativas: duplicados / doble correcta / respuesta ausente
        alts = (await conn.execute(text(
            "SELECT p.id, p.respuesta_correcta, a.texto, a.es_correcta FROM preguntas p "
            "JOIN alternativas a ON a.pregunta_id=p.id WHERE p.fase_id=:f ORDER BY p.id"
        ), {"f": fase_id})).all()
        from collections import defaultdict
        byq = defaultdict(list)
        for pid, rc, txt, ok in alts:
            byq[pid].append((txt, ok, rc))
        dup_opts = 0
        double_correct = 0
        ans_missing = 0
        n_opts_bad = 0
        for pid, lst in byq.items():
            textos = [t for t, _, _ in lst]
            if len(textos) != len(set(textos)):
                dup_opts += 1
            nc = sum(1 for _, ok, _ in lst if ok)
            if nc != 1:
                double_correct += 1
            if lst and len(lst) != 4:
                n_opts_bad += 1
        print(f"\n[8] Preguntas con opciones duplicadas: {dup_opts}")
        print(f"[9] Preguntas con != 1 correcta: {double_correct}")
        print(f"[10] Preguntas con != 4 opciones: {n_opts_bad}")

        # variedad por sección
        print(f"\n[11] Variedad (enunciados estructurales distintos / total) por sección:")
        bysec = defaultdict(list)
        for q in allq:
            bysec[q[1]].append(norm_text(q[3]))
        low = []
        for s in sorted(bysec):
            vals = bysec[s]
            pct = round(100 * len(set(vals)) / len(vals))
            flag = "  <-- BAJA" if pct < 50 else ""
            if pct < 50:
                low.append((s, pct))
            print(f"    sec {s}: {len(set(vals))}/{len(vals)} = {pct}%{flag}")

    # lectura ORM (¿crashea por enum inválido?)
    print(f"\n[12] Lectura ORM de Alternativa (test de enum-read)...")
    try:
        from app.models.pregunta import Alternativa
        from sqlalchemy import select
        async with AsyncSessionLocal() as s:
            q = text("SELECT a.id FROM alternativas a JOIN preguntas p ON a.pregunta_id=p.id WHERE p.fase_id=:f")
            ids = [r[0] for r in (await s.execute(q, {"f": fase_id})).all()]
            objs = (await s.execute(select(Alternativa).where(Alternativa.id.in_(ids)))).scalars().all()
            print(f"    OK: {len(objs)} alternativas cargadas por ORM sin error")
    except Exception as e:
        print(f"    *** CRASH al leer Alternativa por ORM: {type(e).__name__}: {str(e)[:160]}")

    print(f"\n{'='*70}\n")


if __name__ == "__main__":
    asyncio.run(main(int(sys.argv[1])))
