## ADDED Requirements

### Requirement: Registro de comentarios en el simulador
El sistema SHALL permitir al docente escribir comentarios sobre las preguntas y teorías que visualiza en el simulador mediante una caja de texto.

#### Scenario: Comentario guardado con éxito
- **WHEN** el docente escribe un comentario en el cuadro de retroalimentación y presiona el botón "Enviar Comentario"
- **THEN** el sistema envía una petición HTTP POST al backend y notifica con un mensaje de éxito

### Requirement: Persistencia local de comentarios
El backend del sistema SHALL almacenar los comentarios de revisión recibidos en el archivo JSON local `backend/data/feedback_docente.json` conservando los datos de la fase, sección, pregunta, contenido y fecha.

#### Scenario: Anexar comentario a JSON local
- **WHEN** el backend recibe una petición HTTP POST válida con el comentario del docente
- **THEN** el backend abre el archivo `backend/data/feedback_docente.json`, anexa el nuevo registro con un UUID único y marca la bandera `procesado` en falso

### Requirement: Procesamiento asistido de feedback
El sistema SHALL contar con un script de listado de diagnóstico `backend/scripts/apply_teacher_feedback.py` que permita al Agente Antigravity (IA) leer los comentarios sin procesar de forma fácil para luego aplicar los cambios solicitados de forma manual/interactiva en la base de datos de preguntas.

#### Scenario: Agente LLM procesa feedback y corrige base de datos
- **WHEN** el desarrollador o agente ejecuta el script de diagnóstico y detecta un comentario didáctico no procesado
- **THEN** el Agente Antigravity interpreta la sugerencia, aplica el cambio en PostgreSQL mediante herramientas de IDE y marca el registro como procesado en el JSON local
