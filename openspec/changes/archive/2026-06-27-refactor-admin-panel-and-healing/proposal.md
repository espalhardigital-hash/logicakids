## Why

El panel de administrador actual de LogicaKids sufre de archivos de componentes gigantescos y difíciles de mantener (`PedagogyTab.tsx` y `ContentTab.tsx`), un error de carga de preguntas en Fases 5+ por desalineación de IDs de sección y la desactualización del servidor de reportes SRE. Además, se requiere que el docente pueda simular el flujo completo del alumno (teoría, preguntas guiadas y prueba libre), omitir respuestas durante las pruebas para no bloquear las auditorías y dejar comentarios didácticos en un JSON local que la LLM consumirá para auto-corregir enunciados. Adicionalmente, se detectan imágenes de enunciados rotas u omitidas en las Fases 3 a 8 que deben ser auditadas y autocuradas mediante generación procedimental o IA.

## What Changes

- **Refactorización del Panel**: Modularización de `PedagogyTab` y `ContentTab` en subcomponentes más pequeños y limpios.
- **Enmascarado de Credenciales**: Ocultación de contraseñas de base de datos en `SystemTab.tsx`.
- **Ajuste de IDs de Sección**: Alinear las secciones de las Fases 5 a 8 en el frontend (`modulo_id * 100 + nivel_id`).
- **Simulador de Flujo Pedagógico**: Inclusión de pestañas para simular teoría, paso a paso y prueba libre idénticas al alumno.
- **Botón Omitir (Skip)**: Capacidad para que el administrador avance preguntas sin responder.
- **Caja de Comentarios**: Formulario en el simulador para ingresar comentarios que se guardan en `docs/feedback_docente.json`.
- **Pipeline de Autocuración**: Script de backend que escanea Fases 3-8, detecta fallos visuales y genera los assets.
- **Corrección de Graduación**: Solución al error de graduación de Fase 5 que redirige a Fase 3 en lugar de Fase 6.

## Capabilities

### New Capabilities
- `feedback-docente`: Endpoint y archivo local para registrar y procesar retroalimentación pedagógica del docente.

### Modified Capabilities
- `refactor-admin-panel`: Refactorización modular, simulación del flujo estudiantil, botón omitir y pipeline de autocuración de imágenes.
- `bug-fase5-graduation`: Corrección de la lógica de graduación de Fase 5 para dirigir al usuario a la Fase 6 en el backend.

## Impact

- **Frontend**: Componentes de administración en `frontend/src/components/admin/`, rutas de fases y simulación.
- **Backend**: API de retroalimentación en `backend/app/routers/`, scripts de auditoría en `backend/scripts/` y modelos en `backend/app/models/`.
- **Storage**: Carga de assets a MinIO local en el bucket `logicakids`.
