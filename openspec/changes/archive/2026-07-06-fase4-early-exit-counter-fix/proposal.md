## Why

En el Desafío de la Fase 4, el contador de errores del encabezado de la interfaz muestra un número inconsistente de errores acumulados históricos (`61/2`) en lugar de los errores reales cometidos en la sesión del desafío actual. Esto ocurre porque el backend de la Fase 4 no resetea `intentos_totales` a `0` ni purga la tabla `intentos` al gatillar el early exit, a diferencia de la Fase 2 que se toma como patrón y referencia absoluta de diseño.

## What Changes

- **Backend (fase4/router.py):**
  - Actualizar `responder_pregunta` para que, al dispararse el early exit, se limpie `progreso.intentos_totales = 0` y se eliminen de forma explícita los intentos del alumno de esa sección (en las tablas `intento` y `intento_pregunta`), alineándolo con el comportamiento estándar de la Fase 2.
  - Actualizar `get_pregunta` para que limpie `intentos_totales` al inicializar un pool de desafío desde cero.

## Capabilities

### New Capabilities
- Ninguna.

### Modified Capabilities
- Ninguna.

## Impact

- **Backend:** Modificaciones de lógica de reset en `LogicaMath/backend/app/fase4/router.py`.
- **Base de Datos:** Eliminación selectiva de intentos acumulados huérfanos al reiniciar un desafío por expulsión.
