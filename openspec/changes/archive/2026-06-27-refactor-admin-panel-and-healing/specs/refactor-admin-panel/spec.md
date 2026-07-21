## ADDED Requirements

### Requirement: Modularización del Panel de Administrador
El panel de administración MUST estructurarse de forma modular dividiendo las pestañas `PedagogyTab` y `ContentTab` en subcomponentes funcionales cohesivos sin alterar el estilo visual de glassmorphism original.

#### Scenario: Carga del panel modularizado
- **WHEN** un usuario con rol de administrador abre el panel de administrador
- **THEN** el sistema carga y renderiza las pestañas utilizando los nuevos subcomponentes manteniendo el diseño visual intacto

### Requirement: Corrección de IDs de Sección en Fases 5 a 8
La aplicación frontend MUST mapear las secciones de las Fases 5 a 8 según la fórmula del backend: `modulo_id * 100 + nivel_id` para práctica, y `modulo_id * 1000 + nivel_id` para desafíos.

#### Scenario: Listado de preguntas de Fase 5 exitoso
- **WHEN** el administrador selecciona la Fase 5 en el banco de preguntas
- **THEN** la tabla de contenido realiza la petición HTTP con el ID de sección correcto y despliega las preguntas correspondientes

### Requirement: Simulador de Flujo Pedagógico en Administrador
El panel de administración MUST incluir un simulador de alumno (`StudentViewSimulator.tsx`) que permita previsualizar la teoría, el flujo de preguntas guiadas y el juego de prueba libre del nivel seleccionado. Las vistas MUST estar envueltas en un contexto falso (`StudentMockProvider`) para evitar colisiones con el estado real del usuario administrador.

#### Scenario: Visualización de teoría en simulador
- **WHEN** el docente abre el simulador de una sección específica
- **THEN** el sistema presenta el texto de descubrimiento, los glosarios de la teoría y los ejercicios interactivos tal y como los visualiza el alumno

### Requirement: Avanzar sin Responder en Simulador
El simulador de estudiante para administradores MUST proveer una opción de "Avanzar sin responder" que permita omitir preguntas y continuar el flujo de auditoría didáctica. Los componentes de frontend (ej. `GuidedQuestionView`) MUST aceptar un flag `isSimulationMode={true}` para que intercepten internamente las llamadas HTTP a `/api/faseX/answer` y eviten ensuciar las estadísticas o arrojar errores de permisos (403).

#### Scenario: Docente salta pregunta
- **WHEN** el docente hace clic en el botón "Avanzar sin responder" en el simulador
- **THEN** el sistema simula el acierto o avanza al siguiente elemento de la cola sin requerir respuesta numérica

### Requirement: Enmascarado de DATABASE_URL en SystemTab
La pestaña de Servidor y BD (`SystemTab.tsx`) MUST proteger visualmente el valor de la contraseña en el campo `DATABASE_URL` por defecto y proveer un control para revelar el texto plano.

#### Scenario: Visualización segura de DATABASE_URL
- **WHEN** el administrador navega a la pestaña Servidor y BD
- **THEN** el campo `DATABASE_URL` oculta la contraseña y muestra un botón de ojo para revelarla

### Requirement: Diagnóstico para Autocuración de Imágenes
El script de backend `backend/scripts/audit_question_images.py` MUST revisar la base de datos de preguntas de las fases 3 a 8 y reportar en consola qué enunciados visuales carecen de imagen en MinIO. Este reporte será consumido por el Agente de IA para proceder a su generación.

#### Scenario: Autocuración asistida por Agente
- **WHEN** se ejecuta el script de auditoría y reporta en consola que una pregunta de la Fase 7 no tiene su imagen de reloj analógico
- **THEN** el Agente Antigravity genera la imagen solicitada (procedimental o usando sus herramientas) y actualiza el sistema

### Requirement: Monitoreo SRE sin error 404
El sistema de monitoreo SRE en el panel de administrador MUST cargar el archivo de progreso sin fallas 404 mediante la inicialización y exposición adecuada del archivo `progreso_sre.json`.

#### Scenario: Visualización del dashboard SRE exitosa
- **WHEN** el administrador navega a la pestaña de Monitoreo SRE
- **THEN** el sistema lee el archivo `progreso_sre.json` desde el servidor local y renderiza los gráficos de progreso técnico sin fallas HTTP 404
