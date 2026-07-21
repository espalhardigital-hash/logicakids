## 1. Backend Question Generation (seed.py)

- [x] 1.1 Implement `_deduplicate_alts` helper to ensure unique distractors that don't match the correct answer
- [x] 1.2 Integrate `_deduplicate_alts` into `seed_practica_pool` and `seed_preguntas_desafios` before appending to DB models
- [x] 1.3 Refactor `_gen_fase5_pool` Module 1 (Perímetro) to handle `lvl_id` 1, 2, and 3 distinctly with varied templates
- [x] 1.4 Refactor `_gen_fase5_pool` Module 2 (Área) to handle `lvl_id` 1, 2, and 3 distinctly with varied templates
- [x] 1.5 Refactor `_gen_fase5_pool` Module 3 (Figuras compuestas) to handle `lvl_id` 1, 2, and 3 distinctly with varied templates
- [x] 1.6 Expand `_gen_fase5_pool` M3-N4 (Simetría) to include more shapes (círculo, rombo, etc.)
- [x] 1.7 Expand `_gen_fase5_pool` M4-N2 (Diagonal) and M4-N3 (Superficie) to include varied phrasing and parameters
- [x] 1.8 Fix minor textual bugs in `seed.py` (e.g. "En el plano de arriba" -> "En la figura")

## 2. Theory Visuals (theory_examples.py)

- [x] 2.1 Update M2-N3 theory SVGs to render geometric grids instead of text-only descriptions
- [x] 2.2 Update M4-N1 theory SVGs to render map scale graphics instead of text-only equations
- [x] 2.3 Update M4-N3 theory SVGs to render surface area equivalents visually

## 3. Frontend Semantic Fixes

- [x] 3.1 Fix graduation message in `Fase5GameScreen.tsx` ("Fase 3" -> "Fase 6")
- [x] 3.2 Fix phase name references in `Fase5GameScreen.tsx` ("Desarrollo Numérico" -> "Geometría Plana y Medidas")
- [x] 3.3 Update file header comments in `Fase5Service.ts` and `Fase5Types.ts` to reflect the correct phase name
