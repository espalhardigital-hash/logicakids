# state-capture Specification

## Purpose
TBD - created by archiving change mejoras-buzon-ux-qa. Update Purpose after archive.
## Requirements
### Requirement: Application State Capture
El sistema MUST inyectar y persistir las variables y propiedades fundamentales del estado reactivo de la aplicación (ej. puntaje, variables dependientes del contexto, inputs ingresados) en el objeto `app_state` del reporte de retroalimentación.

#### Scenario: Submitting feedback with contextual state
- **WHEN** un reporte de UX es despachado al servidor
- **THEN** el payload `app_state` incluye las claves del estado reactivo activo en el momento del reporte, las cuales se mostrarán en la vista del Administrador

