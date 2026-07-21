## Why

Esta propuesta aborda tres fallos críticos identificados durante la auditoría de código del backend y frontend de la aplicación. Estos problemas comprometen la integridad del almacenamiento S3/MinIO al borrar archivos, rompen la lógica pedagógica al generar parámetros inconsistentes (decimales) para objetos indivisibles y quiebran la visualización de enunciados estructurados en dos pasos en el simulador docente.

## What Changes

- **Resolución de Fuga de Storage (Backend):** Corregir la extracción de la clave (Key) S3/MinIO en `delete_file` para evitar fallos silenciosos al eliminar archivos didácticos organizados en subcarpetas.
- **Validación Robusta de Parámetros Discretos (Frontend):** Corregir la lógica de validación heurística en `validadorContextual.ts` agregando un mecanismo de fallback infalible para asegurar que la cantidad corregida sea siempre divisible por el divisor cuando no se admiten decimales.
- **Segmentación Flexible de Enunciados (Frontend):** Reemplazar el delimitador rígido `.split(". ")` en `validadorContextual.ts` por una expresión regular flexible compatible con saltos de línea (`\n`), puntos sin espacio, o signos de exclamación e interrogación (`!`, `?`).

## Capabilities

### New Capabilities

- `technical-debt-fixes`: Definición de reglas de robustez para la validación contextual de parámetros didácticos, segmentación flexible de enunciados multi-paso y consistencia en el borrado de archivos del almacenamiento S3/MinIO.

### Modified Capabilities

## Impact

- **Backend:** `LogicaMath/backend/app/core/storage.py` (método `delete_file`).
- **Frontend:** `LogicaMath/frontend/services/validadorContextual.ts` (métodos `validarYCorregirParametros` y de segmentación de enunciados).
