## ADDED Requirements

### Requirement: Graduación correcta de la Fase 5
El sistema de backend MUST validar la maestría de los 13 niveles de práctica de la Fase 5 y, tras la aprobación, actualizar la fase actual del alumno a la Fase 6 (orden 6) en la base de datos.

#### Scenario: Graduación de Fase 5 exitosa
- **WHEN** un alumno con los 13 niveles dominados realiza la petición de graduación `POST /api/fase5/graduate`
- **THEN** el sistema actualiza su `fase_actual_id` al ID de la Fase 6 y retorna un mensaje de éxito indicando el avance, y se ha ajustado el mensaje de error para que no mencione "Fase 2" ni "desafíos".
