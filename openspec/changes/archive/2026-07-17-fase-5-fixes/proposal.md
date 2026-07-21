## Why

Phase 5 (Geometría Plana y Medidas) has several critical bugs in its question generation algorithm (`seed.py`). The most severe issues are duplicate answer alternatives (including cases where the correct answer appears as a distractor), a lack of difficulty differentiation across levels, and extremely low variety in generated question templates. These issues severely impact the pedagogical value and user experience of Phase 5.

## What Changes

- **BREAKING**: Modify the `_gen_fase5_pool` function in `seed.py` to differentiate question generation logic by `lvl_id` for Modules 1, 2, and 3.
- Introduce an alternative deduplication mechanism to ensure all generated distractors are unique and do not overlap with the correct answer.
- Expand the variety of question templates to at least 3-4 distinct templates per section to prevent monotony.
- Expand the parameter variety for highly repetitive sections (e.g., M3-N4 Simetría, M4-N2 Diagonal TV, M4-N3 Conversión superficie).
- Correct semantic texts across the frontend and backend (e.g., correct Phase name, fix "Fase 3" graduation message to "Fase 6", change "En el plano de arriba" to "En la figura").
- Replace text-only SVGs in `theory_examples.py` for M2-N3, M4-N1, and M4-N3 with visual geometric representations.

## Capabilities

### New Capabilities
- `fase5-question-generation`: Establishes requirements for difficulty differentiation, template variety, and deduplication of answers in Phase 5 question generation.
- `fase5-theory-visuals`: Ensures theory examples in Phase 5 contain appropriate geometric visual representations rather than text-only SVGs.

### Modified Capabilities

## Impact

- `LogicaMath/backend/app/fase5/seed.py`: Major rewrite of question generation and alternative generation logic.
- `LogicaMath/backend/app/fase5/theory_examples.py`: Updates to SVG generation logic.
- `LogicaMath/frontend/components/fase5/Fase5GameScreen.tsx`: Minor text updates.
- `LogicaMath/frontend/components/fase5/Fase5Service.ts` and `Fase5Types.ts`: Minor comment updates.
