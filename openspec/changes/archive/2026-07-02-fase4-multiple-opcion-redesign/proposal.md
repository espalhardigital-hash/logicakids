## Why

The current `multiple_opcion` component in Phase 4 submits the answer immediately upon clicking an alternative, causing issues such as frozen screens when an incorrect answer is given during a challenge. This behavior deviates from the established UI/UX pattern used in Phase 2 (and other phases), where the user first selects an option (highlighting it) and then explicitly clicks a "Confirmar" button. Adopting this pattern provides better feedback handling and consistency across the platform.

## What Changes

- Modify `multiple_opcion` rendering in `Fase4GameScreen.tsx` to use a `selectedAltId` state instead of immediately submitting.
- Introduce a "Confirmar" button specifically for `multiple_opcion` that becomes "Continuar →" or "Intentar de nuevo ↺" based on `feedback.visible`.
- Ensure alternatives are disabled when feedback is visible.
- Ensure auto-advance after 1.5s in challenge mode.

## Capabilities

### New Capabilities
None

### Modified Capabilities
- `gameplay-fase4-multiple-opcion`: Update UI behavior for multiple choice questions to require confirmation after selection.

## Impact

- `LogicaMath/frontend/components/fase4/Fase4GameScreen.tsx` will be modified.
- User experience in Phase 4 multiple-choice questions will become consistent with Phase 2.
