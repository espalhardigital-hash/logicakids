## Why

El proyecto corre localmente y ya permite validar flujos principales, pero antes de publicar una version de produccion via GitHub + Portainer necesita una capa explicita de hardening. La auditoria detecto riesgos que en local son tolerables, pero en produccion pueden afectar seguridad, despliegue, mantenimiento del schema y calidad de release.

Los puntos mas sensibles son el renderizado de HTML dinamico sin sanitizacion, sesiones JWT guardadas en `localStorage`, endpoints administrativos que exponen configuracion de infraestructura, mezcla de `create_all` con Alembic, variables de entorno inconsistentes y ausencia de typecheck/test gates fiables.

## What

Esta propuesta prepara la aplicacion para una version de produccion mediante mejoras por etapas:

1. Sanitizar todo HTML renderizado en React o eliminar usos innecesarios de `dangerouslySetInnerHTML`.
2. Migrar la autenticacion de produccion hacia cookie `HttpOnly`/`SameSite`, manteniendo compatibilidad local controlada si es necesario.
3. Quitar o limitar `/admin/system-config` detras de una bandera explicita de entorno local/dev.
4. Usar Alembic como fuente unica de schema en produccion, desactivar `Base.metadata.create_all` y poner SQLAlchemy `echo=False` por defecto.
5. Endurecer CORS y convenciones de variables de entorno para despliegue en Portainer.
6. Convertir el build del frontend principal en `tsc --noEmit && vite build`.
7. Separar Vitest y Playwright para evitar que un runner ejecute tests del otro.
8. Ignorar artefactos generados como `playwright-report/` y `test-results/`.
9. Definir presupuesto y estrategia de reduccion de bundles para fases/visualizadores pesados.

## Out of Scope

- No se cambiara la pedagogia, niveles ni contenido matematico.
- No se redisenara visualmente la aplicacion.
- No se ejecutara despliegue en Portainer dentro de esta propuesta; se dejara preparada y verificable.
- No se eliminaran features admin existentes salvo que representen riesgo directo de produccion.

## Impact

- **Frontend principal:** servicios de autenticacion/API, sanitizacion de HTML, scripts de build, configuracion de Vitest/Playwright, `.gitignore`, code splitting.
- **Backend:** auth, CORS, configuracion, arranque, migraciones, endpoint admin de configuracion del sistema.
- **Operacion:** variables de entorno documentadas para local, desarrollo y produccion.
