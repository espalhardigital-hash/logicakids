## ADDED Requirements

### Requirement: Captura de clic en el elemento visual
El sistema SHALL interceptar el clic sobre cualquier componente visible de la interfaz del juego cuando el Modo Evaluador / Inspector de UX esté activo.

#### Scenario: Clic en elemento visual en modo inspector
- **WHEN** el evaluador tiene activo el modo de inspección UX y hace clic sobre un elemento visual (por ejemplo, una porción de la pizza).
- **THEN** la interfaz de usuario SHALL detener las acciones normales de juego y desplegar un modal flotante posicionado cerca del elemento clicado.

### Requirement: Recopilación automática de metadatos contextuales
El sistema SHALL capturar automáticamente el contexto técnico preciso del juego (fase, módulo, nivel, paso, selector DOM único, tamaño de pantalla y estado de React) en el instante del clic y asociarlo al comentario del evaluador.

#### Scenario: Captura de metadatos al enviar feedback
- **WHEN** el evaluador escribe el comentario en el formulario flotante y hace clic en "Guardar".
- **THEN** el sistema SHALL empaquetar todos los metadatos contextuales recopilados del DOM y del estado del juego, y enviarlos a la API en formato JSON.

### Requirement: Persistencia de Feedback
El sistema SHALL persistir las anotaciones enviadas en una base de datos centralizada con la información de metadatos y estado de resolución.

#### Scenario: Registro exitoso en base de datos
- **WHEN** se envía una petición `POST /api/evaluador/feedback` con los datos de una anotación.
- **THEN** el backend SHALL guardar el registro en la tabla `ux_feedback` con el estado inicial "pendiente" y retornar una respuesta exitosa con código 201.

### Requirement: Visualización y administración de feedbacks
El Panel de Administración del programa SHALL proveer una interfaz para visualizar, filtrar y actualizar el estado de las anotaciones UX.

#### Scenario: Filtrado y actualización de feedbacks en el panel
- **WHEN** el administrador navega a la sección de mejorías de UX en el panel de control.
- **THEN** el sistema SHALL mostrar una lista detallada de anotaciones con opción de filtrar por Fase y Prioridad, permitiendo actualizar el estado a "en_desarrollo" o "resuelto".
