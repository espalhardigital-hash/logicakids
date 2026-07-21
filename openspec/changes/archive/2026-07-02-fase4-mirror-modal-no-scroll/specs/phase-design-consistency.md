## MODIFIED Requirements

### Requirement: Estandarización de Alertas de Bucle Espejo
El componente de alerta visual del Bucle Espejo en la Fase 4 y en cualquier fase posterior del sistema SHALL diseñarse e implementarse de tal manera que toda la información relevante (nueva pregunta espejo, input y teclado) se visualice en una sola pantalla sin habilitar el scroll vertical. 

Para lograr esto:
1. La alerta de Bucle Espejo SHALL ocultar el enunciado completo de la pregunta anterior fallida y SHALL compactar el repaso en una sola franja horizontal minimalista que resuma la respuesta incorrecta enviada por el alumno y la respuesta que era correcta.
2. El teclado virtual en pantalla del modal espejo SHALL mantener el diseño de grilla simétrica 3x4 y el botón "Confirmar" de ancho completo abajo, idéntico al patrón y comportamiento definidos en la Fase 2. Si la fase o módulo actual no requiere decimales (como la Fase 4), la tecla de punto decimal `.` SHALL mostrarse deshabilitada visual y funcionalmente, manteniendo la simetría táctil de la grilla.

#### Scenario: Activación de Bucle Espejo en Fase 4
- **WHEN** un alumno falla en una pregunta en la Fase 4 de Práctica Libre y se activa el Bucle Espejo
- **THEN** la interfaz del modal de segunda oportunidad SHALL ocultar el texto completo de la pregunta anterior fallida, SHALL renderizar la barra compacta de repaso, el enunciado de la nueva pregunta espejo y el teclado numérico de grilla simétrica 3x4 con su botón de confirmar inferior de ancho completo, sin generar scroll vertical.
