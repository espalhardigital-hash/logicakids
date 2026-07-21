## Why

El equipo de control de calidad (QA) y los revisores pedagógicos de LógicaKids necesitan una forma directa y precisa de reportar problemas visuales, errores de UX o sugerencias de copy en las pantallas de los módulos sin tener que redactar descripciones largas sobre la ubicación del elemento (Fase, Módulo, Nivel, Pregunta, etc.). Este cambio introduce un inspector de feedback visual contextual que automatiza la captura de metadatos del juego y permite al desarrollador (o a la IA Antigravity) localizar con precisión milimétrica el componente de código fuente que requiere modificaciones.

## What Changes

- **Inspector de Feedback Visual en Caliente**: Nueva herramienta dentro del Modo Evaluador que permite hacer clic en cualquier elemento DOM del juego para abrir un formulario de comentarios flotante.
- **Captura Automática de Contexto**: Registro automático de Fase, Módulo ID, Nivel ID, Pregunta ID, Paso actual, selector CSS único, viewport del dispositivo y estado de la aplicación.
- **Persistencia de Anotaciones**: Creación de una tabla PostgreSQL `ux_feedback` y API endpoints en FastAPI para guardar y consultar comentarios.
- **Administrador de Mejorías**: Vista tipo bandeja de entrada en el Panel de Administración de LógicaKids para visualizar y filtrar los reportes UX de los revisores.

## Capabilities

### New Capabilities
- `feedback-ux-evaluador`: Sistema de anotaciones y comentarios contextuales de UX en caliente para el modo evaluador y panel de control administrativo.

### Modified Capabilities
*Ninguno*

## Impact

- **Frontend (React)**: Incorporación de una capa global `<UXFeedbackOverlay>` en las pantallas del juego, interceptación de clics en modo inspector.
- **Backend (FastAPI)**: Nuevos modelos SQLAlchemy, esquemas Pydantic y endpoints routers bajo `/api/evaluador`.
- **Base de Datos (PostgreSQL)**: Nueva tabla `ux_feedback` generada mediante migraciones de Alembic.
