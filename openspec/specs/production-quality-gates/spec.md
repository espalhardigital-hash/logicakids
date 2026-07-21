# production-quality-gates Specification

## Requirements

### Requirement: Build de Produccion con Typecheck
El frontend principal SHALL ejecutar TypeScript typecheck antes de generar assets de produccion.

#### Scenario: Error TypeScript antes del build
- **WHEN** `npm run build` se ejecuta en `LogicaMath/frontend` y existen errores de tipos
- **THEN** el comando SHALL fallar antes de publicar assets.

### Requirement: Separacion de Runners de Test
La configuracion de pruebas SHALL impedir que Vitest ejecute specs de Playwright y que Playwright ejecute tests unitarios de Vitest.

#### Scenario: Ejecutar tests unitarios
- **WHEN** se ejecuta Vitest
- **THEN** solo SHALL descubrir archivos `*.test.ts` y `*.test.tsx`.

#### Scenario: Ejecutar tests E2E
- **WHEN** se ejecuta Playwright
- **THEN** solo SHALL descubrir archivos `*.spec.ts` dentro de su directorio configurado.

### Requirement: Convencion Unica de URL de API
El frontend principal SHALL usar una unica variable de entorno documentada para resolver la URL base del backend.

#### Scenario: Desarrollo local
- **WHEN** `VITE_API_URL` no esta configurada
- **THEN** el frontend MAY usar `http://localhost:8000` como fallback local.

#### Scenario: Despliegue en produccion
- **WHEN** la aplicacion se compila para produccion
- **THEN** la URL de API SHALL provenir de la variable documentada y no de valores hardcoded inconsistentes.

### Requirement: Artefactos Generados Fuera de Git
El repositorio SHALL ignorar reportes, resultados de prueba y builds generados por herramientas locales.

#### Scenario: Ejecutar Playwright localmente
- **WHEN** Playwright genera `playwright-report/` o `test-results/`
- **THEN** esos artefactos SHALL permanecer fuera del control de versiones.

### Requirement: Presupuesto Inicial de Bundles
El frontend SHALL registrar y revisar el tamano de chunks de produccion para evitar crecimiento no controlado.

#### Scenario: Chunk supera presupuesto
- **WHEN** un chunk principal supera el presupuesto definido
- **THEN** el equipo SHALL revisar imports estaticos, dependencias pesadas y oportunidades de code splitting antes de aceptar el release.
