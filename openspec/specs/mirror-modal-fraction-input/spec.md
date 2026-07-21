# Spec: Mirror Modal Fraction Input

## Purpose
Habilitar soporte completo de entrada de fracciones y teclado virtual unificado en el modal de segunda oportunidad (Mirror Modal).

## Requirements

### Requirement: Dual Fraction Input in Mirror Modal
The Mirror Modal SHALL support dual fraction inputs (Numerator / Denominator) when the correct answer contains a forward slash (`/`).

#### Scenario: Shows Fraction Boxes
- **WHEN** the question's `respuesta_correcta` includes a `/`
- **THEN** the UI renders two stacked input fields (`f4-fraction-input-box`) instead of a single field.

### Requirement: Unified Custom Keyboard
The Mirror Modal SHALL utilize the global `CustomKeyboard` component for all numeric input.

#### Scenario: Inputs Fraction Component
- **WHEN** the user interacts with the `CustomKeyboard`
- **THEN** the active input (numerator or denominator) updates correctly without displaying the native device keyboard.
