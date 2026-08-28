"""Contratos de publicación para la Fase 8.

La fase trabaja con secuencias, combinatoria y probabilidad. Cada ítem debe
ser resoluble, tener una sola clave y llevar una visual que no revele la clave.
"""

import base64
import random

import pytest

from app.fase9.seed_fase8 import _gen_fase8_pool


@pytest.mark.asyncio
@pytest.mark.parametrize("modulo,nivel", [(m, n) for m in (1, 2, 3) for n in (1, 2, 3, 11, 12, 13)])
async def test_fase8_generated_items_are_complete_unique_and_non_mirror(modulo, nivel):
    for seed in range(20):
        item = await _gen_fase8_pool(random.Random(80_000 + modulo * 1_000 + nivel * 100 + seed), modulo, nivel)
        assert item["enunciado"].strip()
        assert item["respuesta_correcta"].strip()
        assert item["expl"].strip()
        assert item["respuesta_correcta"] in item["alts"]
        assert len(item["alts"]) == len(set(item["alts"]))
        assert sum(alt == item["respuesta_correcta"] for alt in item["alts"]) == 1

        visual = item["metadata_visual"]
        assert visual["requiere_imagen"] is True
        svg = base64.b64decode(visual["svg_base64"].split(",", 1)[-1]).decode("utf-8")
        assert "<svg" in svg.lower()
        # La respuesta no puede aparecer como una etiqueta textual completa en
        # la gráfica; los datos mostrados solo apoyan el razonamiento.
        assert f">{item['respuesta_correcta']}<" not in svg


def test_fase8_seed_declares_all_variations_as_originals():
    """Evita que una futura re-siembra reactive el bucle espejo."""
    from pathlib import Path

    source = Path(__file__).parents[1] / "app" / "fase9" / "seed_fase8.py"
    text = source.read_text(encoding="utf-8")
    assert 'payload["es_espejo"] = False' in text
    assert 'payload["es_espejo"] = True' not in text
