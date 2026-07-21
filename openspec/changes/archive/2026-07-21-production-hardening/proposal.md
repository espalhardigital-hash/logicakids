## Why
El proyecto corre localmente y permite validar flujos principales, pero antes de publicar una version de produccion requiere una capa explicita de hardening. La auditoria detecto riesgos que son tolerables en local pero inaceptables en produccion, como la vulnerabilidad a XSS, la gestion insegura de sesiones en `localStorage`, la exposicion de APIs administrativas con configuracion de infraestructura, y deficiencias en procesos de build y calidad.

## What Changes
- **Sanitizacion de HTML:** Reemplazo de `dangerouslySetInnerHTML` por un helper centralizado que sanitiza el contenido dinamico mediante una allowlist estricta.
- **Autenticacion con Cookies:** Migracion de tokens JWT a cookies `HttpOnly`, `SameSite`, y `Secure` para produccion, manteniendo modo legacy solo local bajo bandera.
- **Restriccion de Endpoints:** Restriccion total del endpoint `/admin/system-config` en produccion.
- **Manejo de Schema y Logging:** Desactivacion de `Base.metadata.create_all` y dependencia exclusiva en Alembic. Desactivacion de `echo=True` de SQLAlchemy por defecto. CORS restrictivo.
- **Quality Gates:** Implementacion de `tsc --noEmit` previo a `vite build` y separacion clara de runners (Vitest vs Playwright).
- **Entorno e Infraestructura:** Unificacion de la API URL, presupuestos base para bundles y limpieza de Git de artefactos de prueba generados.

## Capabilities

### New Capabilities
- `secure-html-rendering`: Sanitizacion centralizada de HTML dinamico mediante allowlist.
- `secure-production-auth`: Implementacion de sesiones con cookies seguras para produccion.
- `production-infrastructure-security`: Hardening del backend incluyendo migraciones, logs, endpoint admin config y CORS.
- `production-quality-gates`: Validacion estricta de typecheck en build de frontend y convenciones consolidadas de testing (Vitest/Playwright).

### Modified Capabilities

## Impact
- **Frontend principal:** Servicios de auth/API, rendering HTML en teoria/preguntas, scripts de build, configuracion de Vitest/Playwright, `.gitignore`.
- **Backend:** Auth router (login/register), CORS middlewares, configuracion de base de datos e inicializacion, admin system-config router.
- **Operacion:** Definicion clara de variables de entorno para Portainer y desarrollo local.
