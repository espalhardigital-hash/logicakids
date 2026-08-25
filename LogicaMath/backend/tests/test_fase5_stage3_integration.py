"""
Test de verificación para la Etapa 3: Desbloqueo de pool y topología canónica.
Verifica que los 12 bloques de práctica y 12 de desafío estén definidos y accesibles en la topología.
"""

import pytest
from app.fase5.topology import (
    MODULE_IDS, PRACTICE_LEVEL_IDS, CHALLENGE_LEVEL_IDS, PLAYABLE_BLOCKS, get_block
)
from app.fase5.router import NIVELES_META, MODULOS_META


def test_topology_has_25_blocks():
    """Valida que la topología tenga exactamente 12 de práctica, 12 de desafío y 1 mixto = 25 bloques."""
    assert len(MODULE_IDS) == 4
    assert len(PRACTICE_LEVEL_IDS) == 3
    assert len(CHALLENGE_LEVEL_IDS) == 3
    assert len(PLAYABLE_BLOCKS) == 25


def test_niveles_meta_matches_canonical_topology():
    """Valida que NIVELES_META tenga 12 pares (m, n) y no contenga el nivel 3,4 huérfano."""
    assert len(NIVELES_META) == 12
    assert (3, 4) not in NIVELES_META
    for m in (1, 2, 3, 4):
        for n in (1, 2, 3):
            assert (m, n) in NIVELES_META


def test_get_block_raises_valueerror_for_noncanonical():
    """Valida que get_block rechace pares fuera de la topología como (3, 4)."""
    with pytest.raises(ValueError, match="inválido"):
        get_block(3, 4)

    # Bloques válidos
    assert get_block(1, 1).section == 101
    assert get_block(4, 3).section == 403
    assert get_block(1, 11).section == 1011
    assert get_block(99, 99).section == 99099
