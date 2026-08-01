"""Canonical playable topology and progression policy for Phase 4."""

from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Optional


FASE4_ID = 4
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
        1: "suma",
        2: "multiplicacion",
        3: "mixta",
        4: "mixta",
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
    """Return a canonical block or reject a client-invented combination."""
    try:
        return PLAYABLE_BY_PAIR[(module_id, level_id)]
    except KeyError as exc:
        raise ValueError(
            f"Bloque de Fase 4 invalido: modulo {module_id}, nivel {level_id}."
        ) from exc


def get_block_by_section(section: int) -> BlockSpec:
    try:
        return PLAYABLE_BY_SECTION[section]
    except KeyError as exc:
        raise ValueError(f"Seccion de Fase 4 no jugable: {section}.") from exc


def is_approved(progress: object) -> bool:
    if progress is None:
        return False
    state = getattr(progress, "estado", progress)
    state_value = getattr(state, "value", state)
    return str(state_value).lower() == "aprobado"


def all_prerequisites_approved(progress_by_section: Mapping[int, object]) -> bool:
    return all(is_approved(progress_by_section.get(section)) for section in PREREQUISITE_SECTIONS)


def phase_is_complete(progress_by_section: Mapping[int, object]) -> bool:
    """Phase 4 is complete only when the canonical mixed block is approved."""
    return is_approved(progress_by_section.get(MIXED_SECTION))


def is_block_unlocked(
    progress_by_section: Mapping[int, object], module_id: int, level_id: int
) -> bool:
    block = get_block(module_id, level_id)

    if block.kind is BlockKind.MIXED:
        return all_prerequisites_approved(progress_by_section)

    if block.kind is BlockKind.PRACTICE:
        if block.module_id == 1 and block.level_id == 1:
            return True
        if block.level_id > 1:
            previous = get_block(block.module_id, block.level_id - 1)
            return is_approved(progress_by_section.get(previous.section))

        previous_module = block.module_id - 1
        required = (
            get_block(previous_module, level).section
            for level in PRACTICE_LEVEL_IDS + CHALLENGE_LEVEL_IDS
        )
        return all(is_approved(progress_by_section.get(section)) for section in required)

    practice_sections = (
        get_block(block.module_id, level).section for level in PRACTICE_LEVEL_IDS
    )
    if not all(is_approved(progress_by_section.get(section)) for section in practice_sections):
        return False
    if block.level_id == 11:
        return True
    previous = get_block(block.module_id, block.level_id - 1)
    return is_approved(progress_by_section.get(previous.section))


def default_error_tolerance(module_id: int, level_id: int) -> int:
    block = get_block(module_id, level_id)
    if block.kind is BlockKind.MIXED:
        return 3
    if block.kind is not BlockKind.CHALLENGE:
        return 0
    return 1 if level_id == 13 else 2


def configured_error_tolerance(
    module_id: int, level_id: int, configured_value: Optional[int]
) -> int:
    if configured_value is not None:
        return max(1, int(configured_value))
    return default_error_tolerance(module_id, level_id)


def has_reached_error_limit(error_count: int, tolerance: int) -> bool:
    return error_count >= max(1, tolerance)
