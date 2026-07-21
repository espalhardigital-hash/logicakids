## Context

Esta propuesta de diseño técnico define el enfoque para corregir múltiples hallazgos en la infraestructura de la API, WebSocket, CORS y el renderizado en React identificados durante la auditoría.

## Goals / Non-Goals

**Goals:**
- Asegurar la limpieza y cierre de sockets huérfanos en el backend frente a desconexiones TCP abruptas.
- Habilitar WebSockets dinámicos en producción de forma nativa sin URLs de host estáticas.
- Hacer tolerante a fallos el login de usuarios frente a caídas momentáneas o bloqueos de la base de datos al guardar metadatos.
- Prevenir desmontajes repetitivos de la pantalla de juego `GameScreen` en el frontend, optimizando el rendimiento.
- Centralizar configuraciones de variables de entorno y mejorar el CORS en producción.

**Non-Goals:**
- Cambiar la librería de WebSocket utilizada en el servidor (FastAPI nativo).
- Modificar componentes visuales internos del juego `GameScreen`.

## Decisions

### Decisión 1: Robustez del ciclo de vida del WebSocket
En `backend/app/main.py`, se implementará un bloque `finally:` para garantizar que la desconexión del WebSocket (`manager.disconnect(websocket)`) se ejecute siempre que finalice el ciclo de escucha del socket, capturando tanto desconexiones controladas como errores TCP abruptos de forma segura.

### Decisión 2: Dinamización de la URL de WebSocket
En `frontend/components/useWebSocket.ts`, se calculará la URL del socket dinámicamente:
- Si `VITE_API_URL` está configurado y empieza con `http`, se transformará a `ws`/`wss`.
- En caso contrario, se usará `window.location.host` y `window.location.protocol` para inferir el esquema adecuado. Si está en desarrollo en puerto 3000 de Vite, se enrutará por defecto hacia el puerto 8000 del backend.

### Decisión 3: Try/Except con Rollback para last_login
En `backend/app/routers/auth_users.py`, se envolverá la persistencia de `user.last_login` en un try/except. En caso de fallo de base de datos, se ejecutará `await db.rollback()` para evitar contaminar o bloquear la sesión transaccional de SQLAlchemy, permitiendo que la generación del Token de acceso JWT continúe con éxito.

### Decisión 4: Helper de Fetch con Timeout y AbortController
Se creará un wrapper genérico `fetchWithTimeout` usando `AbortController` en el frontend para forzar la cancelación de peticiones colgadas tras 10 segundos de inactividad, evitando spinners infinitos de carga. Este helper se integrará progresivamente en los servicios principales (como `authService.ts`).

### Decisión 5: Wrapper Component para evitar desmontajes en Route
En `frontend/App.tsx`, se extraerá la lógica IIFE inline de la ruta `/play` a un componente funcional intermedio `PlayRouteWrapper`. React Router podrá comparar las referencias del elemento de forma persistente, eliminando desmontajes y montajes destructivos innecesarios.

### Decisión 6: Centralización de Secretos y CORS
- Modificar `backend/app/auth.py` y `backend/app/services/ai_service.py` para importar y utilizar el singleton `settings` de `app.config`.
- Restringir CORS orígenes en producción configurando de forma segura los dominios correspondientes.

## Risks / Trade-offs

- **[Riesgo]** El fallback de `last_login` oculta errores de base de datos.
  - *Mitigación:* Se agregará un log de advertencia con `logger.warning` o similar para que el administrador pueda auditar problemas de conectividad de la BD sin interrumpir el login del alumno.
