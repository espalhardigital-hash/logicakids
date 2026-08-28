"""Auditoría publicable de la Fase 5 sobre la base local activa.

Falla con código distinto de cero ante cualquier defecto. Comprueba el banco
completo, alternativas, retroalimentación, teoría, configuración y contratos
UX que no pueden observarse solo con una fórmula correcta.
"""

from __future__ import annotations

import asyncio
import json
import re
import sys
from collections import Counter
from pathlib import Path

from sqlalchemy import text

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db.session import AsyncSessionLocal


EXPECTED_SECTIONS = {
    **{module * 100 + level: 65 for module in range(1, 5) for level in range(1, 4)},
    **{
        module * 1000 + challenge: (65 if (module, challenge) == (1, 12) else 39)
        for module in range(1, 5)
        for challenge in (11, 12, 13)
    },
    99099: 156,
}
EXPECTED_TOTAL = sum(EXPECTED_SECTIONS.values())

FORBIDDEN_TEXT = (
    re.compile(r"¿Cuánto es (?:las|los)\b", re.IGNORECASE),
    re.compile(r"(?:regala|dona)[^?!.]*estudiantes", re.IGNORECASE),
    re.compile(r"(?:gasta|gastó|gastado)[^?!.]*caramelos", re.IGNORECASE),
    re.compile(r"\b(?:pregunta|ítem) espejo\b", re.IGNORECASE),
    re.compile(r"\{[A-Za-z_][A-Za-z0-9_]*\}"),
    re.compile(r"\b(?:undefined|nan|null)\b|\[object Object\]", re.IGNORECASE),
)


async def run() -> None:
    failures: list[str] = []
    async with AsyncSessionLocal() as session:
        rows = (await session.execute(text("""
            SELECT p.id, p.seccion, p.tipo_pregunta::text AS tipo_pregunta,
                   p.enunciado, p.respuesta_correcta, p.datos_numericos,
                   p.explicacion_paso_a_paso, p.estructura_padre_id,
                   count(a.id) AS option_count,
                   count(a.id) FILTER (WHERE a.es_correcta) AS correct_count,
                   count(DISTINCT a.texto) AS distinct_option_count,
                   count(a.id) FILTER (
                     WHERE NOT a.es_correcta
                       AND (a.feedback_error IS NULL OR btrim(a.feedback_error) = '')
                   ) AS wrong_without_feedback
            FROM preguntas p
            LEFT JOIN alternativas a ON a.pregunta_id = p.id
            WHERE p.fase_id = 5
            GROUP BY p.id
            ORDER BY p.seccion, p.id
        """))).mappings().all()

        section_counts = Counter(int(row["seccion"]) for row in rows)
        if len(rows) != EXPECTED_TOTAL:
            failures.append(f"total de preguntas={len(rows)}; esperado={EXPECTED_TOTAL}")
        if dict(sorted(section_counts.items())) != dict(sorted(EXPECTED_SECTIONS.items())):
            failures.append(f"conteos por sección no coinciden: {dict(sorted(section_counts.items()))}")

        seen_stems: set[tuple[int, str]] = set()
        for row in rows:
            qid = row["id"]
            section = int(row["seccion"])
            stem = (row["enunciado"] or "").strip()
            answer = (row["respuesta_correcta"] or "").strip()
            data = row["datos_numericos"] or {}
            explanation = row["explicacion_paso_a_paso"] or {}

            if not stem or not answer:
                failures.append(f"pregunta {qid}: enunciado o respuesta vacío")
                continue
            if any(pattern.search(stem) for pattern in FORBIDDEN_TEXT):
                failures.append(f"pregunta {qid}: enunciado no publicable: {stem}")
            if re.search(rf"(?<!\d){re.escape(answer)}(?!\d)", stem):
                failures.append(f"pregunta {qid}: la respuesta {answer} aparece copiada en el enunciado")
            signature = (section, re.sub(r"\s+", " ", stem.casefold()))
            if signature in seen_stems:
                failures.append(f"pregunta {qid}: enunciado duplicado dentro de la sección {section}")
            seen_stems.add(signature)

            if row["option_count"] != 4 or row["correct_count"] != 1:
                failures.append(
                    f"pregunta {qid}: opciones={row['option_count']}, correctas={row['correct_count']}"
                )
            if row["distinct_option_count"] != 4:
                failures.append(f"pregunta {qid}: alternativas duplicadas")
            if row["wrong_without_feedback"]:
                failures.append(f"pregunta {qid}: distractor sin retroalimentación")

            if not data.get("requiere_figura") or not data.get("tipo_visual"):
                failures.append(f"pregunta {qid}: contrato visual ausente")
            if any(key in data for key in ("es_espejo", "pregunta_espejo", "mirror")):
                failures.append(f"pregunta {qid}: metadato de pregunta espejo")
            steps = explanation.get("pasos") if isinstance(explanation, dict) else None
            if not steps or not all(str(step.get("texto", "")).strip() for step in steps):
                failures.append(f"pregunta {qid}: explicación paso a paso incompleta")

            template_id = str(data.get("plantilla_id", ""))
            is_equivalence = section in (102, 1012) or (
                section == 99099 and template_id.startswith(("tpl_m1_n2", "tplx_m1_n2", "tplr_m1_n2"))
            )
            if is_equivalence:
                if data.get("tipo_visual") != "equivalence_strip":
                    failures.append(f"pregunta {qid}: equivalencia sin tira comparativa")
                if not str(data.get("objetivo_visual", "")).strip():
                    failures.append(f"pregunta {qid}: equivalencia sin objetivo visual específico")
                if "expresion_visual" in data or "×" in str(data.get("objetivo_visual", "")):
                    failures.append(f"pregunta {qid}: el visual entrega la operación en vez del reto")
                fractions = [data.get("fraccion_izquierda"), data.get("fraccion_derecha")]
                if not all(isinstance(fr, dict) and set(fr) == {"numerador", "denominador"} for fr in fractions):
                    failures.append(f"pregunta {qid}: contrato de fracciones comparadas incompleto")
                else:
                    visible_terms = {
                        str(value) for fraction in fractions for value in fraction.values()
                        if value is not None
                    }
                    if answer in visible_terms:
                        failures.append(f"pregunta {qid}: la figura copia la respuesta {answer}")

        equivalence_skills = (await session.execute(text("""
            SELECT DISTINCT datos_numericos->>'habilidad'
            FROM preguntas
            WHERE fase_id=5
              AND datos_numericos->>'plantilla_id' ~ '^tpl[r|x]?_m1_n2'
        """))).scalars().all()
        required_equivalence_skills = {
            "inferir_factor", "simplificar_inversa", "leer_subdivision",
            "contar_cortes", "detectar_error", "simplificar",
            "comparar_representaciones",
        }
        if not required_equivalence_skills <= set(equivalence_skills):
            failures.append(
                "M1N2 sin variedad cognitiva requerida: "
                f"faltan {sorted(required_equivalence_skills - set(equivalence_skills))}"
            )

        theory_count = (await session.execute(text(
            "SELECT count(*) FROM niveles_teoria_pool WHERE fase_id=5"
        ))).scalar_one()
        config_count = (await session.execute(text(
            "SELECT count(*) FROM configuracion_progreso WHERE fase_id=5"
        ))).scalar_one()
        if theory_count != 12:
            failures.append(f"bloques de teoría={theory_count}; esperado=12")
        if config_count != 26:
            failures.append(f"configuraciones={config_count}; esperado=26")

    root = Path(__file__).resolve().parents[1]
    router = (root / "app" / "fase5" / "router.py").read_text(encoding="utf-8")
    if "pausa_obligatoria_segundos=0 if es_correcta else 10" not in router:
        failures.append("backend: bloqueo de 10 segundos ausente")

    # El contenedor final del backend no monta el árbol del frontend. Cuando
    # ambos árboles están disponibles (ejecución local), se añaden los checks
    # estáticos; en Docker estos contratos quedan cubiertos por Vitest.
    frontend = root.parent / "frontend" / "components" / "fase5"
    if frontend.exists():
        game = (frontend / "Fase5GameScreen.tsx").read_text(encoding="utf-8")
        styles = (frontend / "Fase5Styles.css").read_text(encoding="utf-8")
        feedback = (frontend / "Fase5FeedbackLockModal.tsx").read_text(encoding="utf-8")
        if "Fase5FeedbackLockModal" not in game:
            failures.append("frontend: modal de retroalimentación no conectado")
        if "disabled={!ready || stepPage < totalStepPages - 1}" not in feedback:
            failures.append("frontend: continuar no exige tiempo y lectura completa")
        if not re.search(r"\.f5-screen-wrapper\s*\{[^}]*overflow:\s*hidden", styles, re.DOTALL):
            failures.append("frontend: gameplay no garantiza cero scroll")
        if not re.search(r"\.f5-welcome-screen\s*\{[^}]*overflow-y:\s*auto", styles, re.DOTALL):
            failures.append("frontend: selector de contenidos no permite scroll")

    report = {
        "phase": 5,
        "questions": len(rows),
        "sections": len(EXPECTED_SECTIONS),
        "theory_blocks": 12,
        "configurations": 26,
        "failures": failures,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(run())
