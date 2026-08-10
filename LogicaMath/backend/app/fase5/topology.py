"""Topología jugable canónica y política de progresión para la Fase 5."""

from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Optional


FASE5_ID = 5
PRACTICE_LEVEL_IDS = (1, 2, 3)
CHALLENGE_LEVEL_IDS = (11, 12, 13)
MODULE_IDS = (1, 2, 3, 4)
MIXED_MODULE_ID = 99
MIXED_LEVEL_ID = 99
MIXED_SECTION = 99099


class BlockKind(str, Enum):
    PRACTICE = "practice"
    CHALLENGE = "challenge"
    MIXED = "mixed"


@dataclass(frozen=True)
class BlockSpec:
    module_id: int
    level_id: int
    section: int
    operation: str
    kind: BlockKind


def _operation_for_module(module_id: int) -> str:
    return {
        1: "fraccion_visual",
        2: "fraccion_cantidad",
        3: "porcentajes_promedios",
        4: "razon_mezclas",
    }[module_id]


PRACTICE_BLOCKS = tuple(
    BlockSpec(
        module_id=module_id,
        level_id=level_id,
        section=module_id * 100 + level_id,
        operation=_operation_for_module(module_id),
        kind=BlockKind.PRACTICE,
    )
    for module_id in MODULE_IDS
    for level_id in PRACTICE_LEVEL_IDS
)

CHALLENGE_BLOCKS = tuple(
    BlockSpec(
        module_id=module_id,
        level_id=level_id,
        section=module_id * 1000 + level_id,
        operation="mixta",
        kind=BlockKind.CHALLENGE,
    )
    for module_id in MODULE_IDS
    for level_id in CHALLENGE_LEVEL_IDS
)

MIXED_BLOCK = BlockSpec(
    module_id=MIXED_MODULE_ID,
    level_id=MIXED_LEVEL_ID,
    section=MIXED_SECTION,
    operation="mixta",
    kind=BlockKind.MIXED,
)

PREREQUISITE_BLOCKS = PRACTICE_BLOCKS + CHALLENGE_BLOCKS
PLAYABLE_BLOCKS = PREREQUISITE_BLOCKS + (MIXED_BLOCK,)
PLAYABLE_BY_PAIR = {(block.module_id, block.level_id): block for block in PLAYABLE_BLOCKS}
PLAYABLE_BY_SECTION = {block.section: block for block in PLAYABLE_BLOCKS}
PREREQUISITE_SECTIONS = frozenset(block.section for block in PREREQUISITE_BLOCKS)
PLAYABLE_SECTIONS = frozenset(block.section for block in PLAYABLE_BLOCKS)


def get_block(module_id: int, level_id: int) -> BlockSpec:
    """Retorna un bloque canónico o rechaza combinaciones no válidas."""
    try:
        return PLAYABLE_BY_PAIR[(module_id, level_id)]
    except KeyError as exc:
        raise ValueError(
            f"Bloque de Fase 5 inválido: módulo {module_id}, nivel {level_id}."
        ) from exc


def get_block_by_section(section: int) -> BlockSpec:
    try:
        return PLAYABLE_BY_SECTION[section]
    except KeyError as exc:
        raise ValueError(f"Sección de Fase 5 no jugable: {section}.") from exc


def is_approved(progress: object) -> bool:
    if progress is None:
        return False
    return getattr(progress, "estado", None) == "APROBADO" or getattr(progress, "porcentaje_actual", 0.0) >= 100.0
