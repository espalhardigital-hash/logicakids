## Context

Phase 4 of the application currently handles `multiple_opcion` questions by submitting the answer immediately upon alternative click. If the answer is incorrect during a challenge, the alternatives are disabled and feedback is shown, but no explicit button is present to continue or retry. 
In Phase 2, a robust pattern exists:
1. Clicking an alternative selects it (`selectedAltId`).
2. A separate "Confirmar" button submits the answer.
3. Upon feedback, the button text changes to "Continuar" (if correct or in challenge) or "Intentar de nuevo" (if incorrect in normal mode).

## Goals / Non-Goals

**Goals:**
- Align Phase 4's `multiple_opcion` component with Phase 2's design pattern.
- Implement a `selectedAltId` state for option selection.
- Implement an explicit submit/continue button for `multiple_opcion`.
- Ensure auto-advance behavior works correctly (1.5s after incorrect answer in challenge).

**Non-Goals:**
- Do not modify non-multiple-choice UI elements in Phase 4 (e.g. fractional inputs, diagrams).
- Do not change backend logic.

## Decisions

**State Management for Selection**
Introduce `const [selectedAltId, setSelectedAltId] = useState<number | null>(null);` in `Fase4GameScreen.tsx`. Update the rendering of alternatives to highlight the selected one and set this state on click.

**Confirmation Button**
Instead of `handleAltSelect(alt.texto)` calling `handleSubmit`, it will set `selectedAltId`. A dedicated "Confirmar" button will call `handleSubmit`. In `handleSubmit`, we will determine the text from the selected alternative ID.

**Feedback Continuation**
When `feedback.visible` is true, the Confirmar button becomes "Continuar" or "Intentar de nuevo" and is enabled. When clicked, it will call `handleFeedbackClose()`.

## Risks / Trade-offs

- *Risk*: `handleSubmit` currently infers `finalAnswer` from multiple places. We need to ensure that when `selectedAltId` is set, `handleSubmit` finds the correct `alt.texto` for submission.
  *Mitigation*: We will add a check in `handleSubmit` to find `pregunta.alternativas.find(a => a.id === selectedAltId)?.texto` if `selectedAltId` is not null.
