# ux-feedback-system Specification

## Purpose
TBD - created by archiving change mejoras-buzon-ux-qa. Update Purpose after archive.
## Requirements
### Requirement: DOM Selector Exactness
El sistema MUST generar un selector DOM (CSS Selector) que sea inequívoco y absoluto (`dom_selector`) para asegurar que una IA pueda encontrar la ubicación exacta en el código, incorporando validaciones de jerarquía directa (`nth-child`) o atributos de prueba (`data-testid`).

#### Scenario: DOM Selector generation
- **WHEN** el usuario interactúa con el modo inspección
- **THEN** el componente produce un selector CSS que resuelve a un único elemento HTML en el árbol DOM, sin falsos positivos por clases compartidas

### Requirement: Absolute MinIO Links
El sistema MUST responder y registrar URLs completas absolutas hacia el bucket MinIO asignado en lugar de rutas relativas de backend.

#### Scenario: Submitting and reading screenshot URL
- **WHEN** se envía una captura de pantalla al servidor (ya sea subida u obtenida auto-capturada)
- **THEN** el servidor devuelve una URL que puede ser navegada y extraída externamente apuntando explícitamente al storage de MinIO, relacionando inequívocamente la evidencia visual con el reporte del buzón.

