## ADDED Requirements

### Requirement: Automated Screenshot Capture
El sistema MUST tomar una captura de pantalla automáticamente usando `html2canvas` al interceptar un evento de clic sobre un elemento inspeccionado, suprimiendo la necesidad de captura manual.

#### Scenario: Successful automated capture
- **WHEN** el evaluador hace clic en un elemento del DOM resaltado por el inspector
- **THEN** el sistema invoca `html2canvas` sobre `document.body` y adjunta la imagen resultante al payload de retroalimentación
