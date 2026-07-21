## Why

La aplicación presentaba deuda técnica importante relacionada con el manejo de timeouts en el frontend (Fases 2-9 usaban fetch nativo sin abortController), carga insegura de variables de entorno mediante `os.environ` y errores silenciados en los accesos asíncronos a base de datos. Estos problemas ponían en riesgo la estabilidad de la aplicación frente a caídas de red y rompían el encapsulamiento de secretos estipulado en la metodología base.

## What Changes

- Reemplazo global de llamadas `fetch()` por `fetchWithTimeout()` en todas las Fases Didácticas.
- Limpieza explícita del temporizador de reconexión WebSocket al recibir múltiples señales `onclose` simultáneas.
- Eliminación de accesos `os.environ.get("GOOGLE_API_KEY")` usando la instancia centralizada `settings`.
- Inserción de logs explícitos si `db.rollback()` falla asíncronamente en el endpoint `/auth/login`.

## Capabilities

### New Capabilities
*(Ninguna nueva funcionalidad; sólo resolución de deuda de confiabilidad)*

### Modified Capabilities
- `api-reliability-and-security`: Se asegura que todo el frontend cumpla con el requerimiento de timeout ya escrito, y que el backend consuma secretos unificados estrictamente.

## Impact

- Frontend: Archivos `Fase2Service.ts` a `Fase9Service.ts`, y `useWebSocket.ts`.
- Backend: Endpoint `routers/auth_users.py`, scripts `apply_teacher_feedback.py` y `audit_question_images.py`.
