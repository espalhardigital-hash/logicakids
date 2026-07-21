## Context

La aplicacion esta en fase local/desarrollo. Los builds de Vite pasan, pero el frontend principal no ejecuta typecheck en el build y los tests mezclan Vitest con Playwright. En backend, el arranque combina migraciones Alembic con `Base.metadata.create_all`, SQLAlchemy emite SQL con `echo=True`, y el panel admin tiene un endpoint capaz de leer/escribir `.env`.
El mayor riesgo de seguridad viene de renderizar HTML dinamico desde base de datos o estado capturado sin una allowlist. Ese riesgo se amplifica porque la sesion JWT se guarda en `localStorage`.

## Goals / Non-Goals

**Goals:**
- Reducir riesgo XSS mediante sanitizacion centralizada y reemplazo progresivo de HTML inseguro.
- Preparar sesiones seguras para produccion con cookies `HttpOnly` y `SameSite`.
- Evitar exposicion accidental de configuracion sensible en produccion.
- Hacer que el schema de produccion dependa de Alembic, no de `create_all`.
- Asegurar que el build de produccion falle ante errores TypeScript.
- Separar claramente unit/component tests de E2E tests.
- Unificar variables de entorno para frontend principal y admin.
- Reducir ruido de artefactos generados en Git.
- Crear una base medible para optimizacion de bundles.

**Non-Goals:**
- Reescribir toda la autenticacion en una sola iteracion si rompe compatibilidad local.
- Eliminar toda la posibilidad de HTML enriquecido; se permitira una allowlist controlada.
- Optimizar todos los bundles en la primera etapa; se priorizara seguridad y release gates.

## Decisions

### Decision 1: Sanitizacion centralizada
Se introducira un helper unico para transformar texto/markdown permitido a HTML seguro. El helper debera escapar atributos, validar URLs (`http`, `https`, rutas relativas permitidas) y sanitizar el resultado con una allowlist estricta. Todo `dangerouslySetInnerHTML` debera consumir este helper o justificar su excepcion.

### Decision 2: Auth de produccion con cookies
El backend seguira retornando token durante una fase de compatibilidad local, pero en produccion debera setear una cookie `HttpOnly`, `Secure`, `SameSite=Lax` o `Strict`. El frontend debera soportar `credentials: "include"` para endpoints autenticados. El almacenamiento en `localStorage` quedara como modo legacy/dev, controlado por variable de entorno.

### Decision 3: Endpoint de sistema solo local/dev
`/admin/system-config` se mantendra solo si `ENABLE_SYSTEM_CONFIG_ENDPOINT=true` y el entorno no es produccion. En produccion debera responder 404 o 403 sin incluir `DATABASE_URL`. Las credenciales y conexiones se gestionaran via Portainer/env vars.

### Decision 4: Alembic como autoridad de schema
En produccion no se ejecutara `Base.metadata.create_all`. El arranque ejecutara Alembic de forma controlada o fallara si las migraciones no pueden aplicarse. `create_all` podra quedar como fallback local explicito, nunca implicito en produccion.

### Decision 5: Quality gates separados
El frontend principal cambiara `build` a `tsc --noEmit && vite build`. Vitest incluira solo `*.test.ts` y `*.test.tsx`; Playwright seguira usando `*.spec.ts` dentro de `tests/`. El admin mantendra `tsc -b && vite build` y se limpiaran reglas lint por etapas.

### Decision 6: Convencion unica de API URL
Se usara una sola variable para el frontend principal. La opcion propuesta es `VITE_API_URL` como base sin sufijo obligatorio `/api`, porque el backend ya soporta rutas con y sin prefijo via middleware. La documentacion debera aclarar ejemplos para local y produccion.

### Decision 7: Bundle budgets progresivos
Primero se mediran chunks y se documentaran presupuestos. Luego se separaran dependencias pesadas como Fabric/Three/visualizadores y pantallas admin mediante imports dinamicos reales, evitando imports estaticos que anulan code splitting.

## Risks / Trade-offs

- **Risk:** Migrar a cookies puede romper llamadas existentes si no se activa `credentials: "include"`.
  - **Mitigation:** Implementar modo compatibilidad y tests de login/me.
- **Risk:** Sanitizar HTML puede remover estilos o SVGs didacticos existentes.
  - **Mitigation:** Empezar con allowlist explicita para tags pedagogicos necesarios y pruebas visuales de teoria/preguntas.
- **Risk:** Activar typecheck en build puede bloquear despliegues por deuda acumulada.
  - **Mitigation:** Corregir errores por categoria y no activar gate CI hasta que `tsc --noEmit` pase localmente.
