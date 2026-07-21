## ADDED Requirements

### Requirement: Websocket Synchronization in Fase 4
The system SHALL force a reload of the current question in Fase 4 when the `sync_required` websocket event is received from the admin panel.

#### Scenario: Admin updates settings
- **WHEN** the admin saves new configuration settings while a student is in Fase 4
- **THEN** the student's screen automatically reloads the question state using `loadNextQuestion(true)`

### Requirement: Explicit Mirror Flag on Load
The backend SHALL explicitly inject `es_espejo=True` into `datos_numericos` when serving a Fase 4 question if it is a mirror variant.

#### Scenario: Student resumes a mirror session
- **WHEN** a student closes the app during a mirror loop and opens it again
- **THEN** the system loads the current question, detects `es_espejo=True`, and immediately shows the Mirror Modal instead of the regular question UI

### Requirement: Advanced Support Rescue
The backend SHALL return `soporte_avanzado=True` when a student fails the final mirror question in Fase 4, and the frontend SHALL display the `Fase4RescateModal`.

#### Scenario: Failing the final mirror question
- **WHEN** a student answers the final mirror question incorrectly
- **THEN** the system shows the rescue modal with the deep explanation, and bypassing the question when closed via the `/cerrar-rescate` endpoint.

### Requirement: Safe Bypass Endpoint
The backend SHALL provide a `/cerrar-rescate` endpoint for Fase 4 to safely mark a blocked question as responded (without adding mastery points) and advance to the next family.

#### Scenario: Student acknowledges the rescue modal
- **WHEN** the student clicks "Entendido, continuar!" on the `Fase4RescateModal`
- **THEN** the system calls `/cerrar-rescate` to bypass the question and loads the next question family
