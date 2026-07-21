## ADDED Requirements

### Requirement: Orden determinista del pool asignado para Preguntas Espejo
El endpoint `GET /pregunta` de Fase 4 SHALL recuperar el pool asignado del alumno con un orden determinista (`ORDER BY id ASC`) para garantizar que, tras un fallo en Práctica Libre, la pregunta espejo (variante recién asignada al pool) sea siempre la primera pregunta pendiente devuelta al frontend.

#### Scenario: Alumno falla una pregunta en Práctica Libre
- **GIVEN** el alumno respondió incorrectamente y el backend asignó la variante espejo al pool (actualizó `pregunta_id` del pool_item)
- **WHEN** el frontend solicita la siguiente pregunta vía `GET /pregunta`
- **THEN** el backend devuelve la pregunta espejo (la del pool_item recién actualizado) como primera pendiente, activando el flag `es_espejo: true` en `datos_numericos`
- **AND** el frontend abre el modal `Fase4MirrorModal` con la pregunta de segunda oportunidad

### Requirement: Feedback textual del tutor visible en errores
El endpoint `POST /responder` de Fase 4 SHALL retornar el mensaje de feedback del tutor en un campo reconocido por el schema Pydantic `Fase2ResultadoRespuesta` (alias `Fase4ResultadoRespuesta`), de modo que FastAPI lo serialice correctamente y el frontend lo reciba para mostrarlo al alumno.

#### Scenario: Alumno responde incorrectamente
- **GIVEN** el alumno envía una respuesta incorrecta al endpoint `/responder`
- **WHEN** el backend construye el objeto de respuesta
- **THEN** el campo de feedback textual del tutor (`feedback_error`) contiene el mensaje explicativo (ej: "Vuelve a calcular. ¡Tú puedes!")
- **AND** el frontend lo muestra como texto visible en la UI (no solo animación rojo/temblor)

### Requirement: Endpoint único de cierre de rescate
El router de Fase 4 SHALL definir un único endpoint `POST /cerrar-rescate` que consolide la lógica de cierre del bucle de rescate, evitando la duplicidad de rutas que provoca que FastAPI sobrescriba la primera definición con la segunda.

#### Scenario: Alumno cierra el modal de rescate
- **GIVEN** el alumno está viendo la explicación del rescate tras agotar los espejos
- **WHEN** el alumno cierra el modal de rescate
- **THEN** el endpoint registra un intento de tipo `BYPASS_EXPLICACION`, marca el pool_item como respondido correctamente, recalcula el porcentaje de progreso, y verifica si el bloque o la fase se completaron
- **AND** no existe otro endpoint registrado con el mismo path que pudiera sobrescribir esta lógica
