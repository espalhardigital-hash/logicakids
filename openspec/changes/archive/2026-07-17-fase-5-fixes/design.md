## Context

Phase 5's question generator currently shares the exact same logic and template for multiple levels within a module, largely ignoring the `lvl_id` parameter. Distractors are generated via rigid formulas (e.g., `a*b`, `a+b`, `ans+4`), which naturally causes collisions and duplicate values in certain edge cases (e.g. `(a-2)(b-2)=8` for perimeter, or `a=b` for area). Theory examples lack distinct visual figures, using text-only SVG charts instead of meaningful geometry.

## Goals / Non-Goals

**Goals:**
- Completely eliminate duplicated alternative answers in Phase 5 generated questions.
- Introduce level-specific (N1, N2, N3) differentiation for M1, M2, and M3 question logic.
- Prevent identical text string fatigue by ensuring at least 3 distinct semantic templates per question type.
- Ensure that SVGs used in `theory_examples.py` for M2-N3, M4-N1, M4-N3 actually render geometric visuals.

**Non-Goals:**
- Refactoring the frontend logic for rendering questions (the rendering system works fine, the issue is data).
- Modifying the core gameplay mechanisms of Phase 5.
- Expanding the number of levels or modules.

## Decisions

- **Deduplication Mechanism:** We will implement a `_deduplicate_alts(alts, correct, rng)` helper inside `seed.py`. This helper will take the formulaically generated distractors, check for duplicates against a `Set()`, and if a duplicate (or overlap with `correct`) is found, it will iteratively mutate the value (e.g. `ans + rng.choice([2,3,5,-2,-3])`) until a unique, positive number is achieved. This ensures that the primary distractors (which target specific pedagogical misconceptions) are preserved when valid, but safely replaced when they cause collisions.
- **Level Differentiation in `_gen_fase5_pool`:** The central routing `if mod_id == X:` logic will be split into sub-branches `if lvl_id == 1:`, `elif lvl_id == 2:`, etc. Each branch will utilize a different subset of templates and mathematical parameters reflecting the difficulty of that level.

## Risks / Trade-offs

- **Risk: Breaking DB Schema via Seed:** The seed drops and recreates Phase 5. If we introduce bugs in the data structure, the seed will fail.
  - *Mitigation:* Ensure we maintain the exact data schema expected by `Pregunta` and `Alternativa` models. Run a simulated validation of the seed locally.
- **Risk: Graphic URL Caching:** The generator currently caches generated SVG URLs based on `a` and `b` values. Differentiating logic might require caching by template or level as well.
  - *Mitigation:* Adjust cache keys to include `lvl_id` or template identifier if the underlying geometry requirements change per level.
