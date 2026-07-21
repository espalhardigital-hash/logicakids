# Capability: gameplay-fase4-multiple-opcion

## Purpose
TBD (To Be Determined)

## Requirements

### Requirement: Explicit confirmation for multiple choice options
The system SHALL require the user to explicitly click a confirmation button after selecting a multiple choice alternative in Phase 4, matching the UI pattern from Phase 2.

#### Scenario: User selects an option
- **WHEN** user clicks on a multiple choice alternative
- **THEN** the alternative is visually highlighted as selected
- **AND** the answer is NOT yet submitted
- **AND** the confirmation button becomes enabled

#### Scenario: User submits an answer
- **WHEN** user has an alternative selected and clicks the "Confirmar" button
- **THEN** the answer is submitted to the backend
- **AND** the feedback is shown

#### Scenario: Post-feedback continuation (Challenge Mode - Incorrect)
- **WHEN** the answer is incorrect in challenge mode
- **THEN** the confirmation button transforms into "Continuar →"
- **AND** the system automatically advances to the next question after 1.5 seconds

#### Scenario: Post-feedback continuation (Normal Mode - Incorrect)
- **WHEN** the answer is incorrect in normal mode
- **THEN** the confirmation button transforms into "Intentar de nuevo ↺"

### Requirement: Reinicio de intentos y errores al iniciar sesión
El sistema backend SHALL recibir un parámetro `reload: bool` al cargar la siguiente pregunta. Si `reload` es verdadero, el backend SHALL purgar el pool asignado y los intentos de la sesión anterior del alumno, estableciendo `aciertos_acumulados` y `intentos_totales` en `0`.

#### Scenario: Reiniciar desafío de Fase 4
- **WHEN** el alumno inicia un desafío de la Fase 4 y el frontend realiza la llamada inicial con `reload=true`
- **THEN** el sistema reinicia el progreso de maestría a 0% y elimina los intentos pasados para evitar heredar errores.
