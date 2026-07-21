## 1. Backend: Autenticación y Secretos

- [x] 1.1 Reemplazar pass silencioso por logs explícitos en el bloque try-except del rollback en `backend/app/routers/auth_users.py`.
- [x] 1.2 Importar `settings` de `app.core.config` en `apply_teacher_feedback.py` y sustituir uso de `os.environ.get("GOOGLE_API_KEY")`.
- [x] 1.3 Importar `settings` en `audit_question_images.py` y sustituir uso de `os.environ.get("GOOGLE_API_KEY")`.

## 2. Frontend: Timeouts y WebSockets

- [x] 2.1 Agregar `clearTimeout(retryTimerRef.current)` antes del inicio del timer en manejadores `onerror`, `onclose` o catch dentro de `useWebSocket.ts`.
- [x] 2.2 Reemplazar la función global `fetch` por la importación y uso de `fetchWithTimeout` en `Fase2Service.ts`.
- [x] 2.3 Repetir reemplazo de timeout para Fases 3 a 9 iterando masivamente sobre los directorios correspondientes.
