## Why

Actualmente, la Fase 4 es inconsistente con el diseño y la lógica probada de la Fase 2, resultando en comportamientos frustrantes para el usuario final (congelamiento de pantalla al recargar en medio de un bucle espejo, incapacidad de saltar preguntas tras errores reiterados y falta de sincronización en tiempo real con el administrador). Homologar la Fase 4 al esquema funcional exacto de la Fase 2 resolverá estos problemas definitivamente y unificará la arquitectura.

## What Changes

- Modificación del backend (`app/fase4/router.py`) para inyectar explícitamente `es_espejo=True` en la carga de la pregunta y no solo en el submit.
- Implementación del concepto `soporte_avanzado` en el backend para permitir un rescate seguro tras múltiples errores, incluyendo el nuevo endpoint `@router.post("/cerrar-rescate")`.
- Integración en el frontend (`Fase4GameScreen.tsx`) del listener WebSocket `sync_required` que ya usa la Fase 2.
- Adición del `Fase4RescateModal` al frontend para replicar el flujo de "Bypass" ante múltiples errores en el bucle espejo.
- Refactorización de `loadNextQuestion` y `handleSubmit` en el frontend para centralizar la apertura de modales según la data obtenida en la recarga, previniendo cierres inesperados o estados inconsistentes.

## Capabilities

### New Capabilities
- `gameplay-fase4-logica-homologacion`: Homologación de estado profundo y mecanismos de rescate, incluyendo websockets y bucles espejo, para igualar la robustez de Fase 2.

### Modified Capabilities

## Impact

- Frontend: `Fase4GameScreen.tsx`, `Fase4Types.ts`.
- Backend: `app/fase4/router.py`.
- Flujos de experiencia de usuario de la Fase 4 (se sentirán idénticos a los de la Fase 2 en la recuperación de errores).
