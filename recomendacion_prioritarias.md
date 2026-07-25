# Recomendaciones prioritarias — LogicaKids Pro

> **Versión:** 1.0  
> **Fecha:** 2026-07-25  
> **Origen:** Análisis integral del repositorio (rama `producion`)  
> **Audiencia:** Producto, desarrollo, operación y agentes de IA que implementen mejoras  

Este documento detalla **cada recomendación prioritaria** del análisis del proyecto: por qué importa, qué riesgos mitiga, qué implica cambiar, cómo implementarla y cómo verificar el éxito.

---

## Índice

| # | Horizonte | Recomendación |
|---|-----------|---------------|
| [R1](#r1-congelar-el-mapa-canónico-de-ids-de-fase) | Corto plazo | Congelar el mapa canónico de IDs de fase |
| [R2](#r2-completar-hardening-de-producción) | Corto plazo | Completar hardening de producción |
| [R3](#r3-alinear-versionado-de-producto) | Corto plazo | Alinear versionado de producto |
| [R4](#r4-tests-de-contrato-por-fase) | Corto plazo | Tests de contrato por fase |
| [R5](#r5-extraer-un-motor-genérico-de-fase) | Medio plazo | Extraer un motor genérico de fase |
| [R6](#r6-reducir-y-gobernar-el-bundle-frontend) | Medio plazo | Reducir y gobernar el bundle frontend |
| [R7](#r7-auditoría-automática-del-pool-en-ci) | Medio plazo | Auditoría automática del pool en CI |
| [R8](#r8-pipeline-ci-mínima-en-pull-requests) | Medio plazo | Pipeline CI mínima en pull requests |
| [R9](#r9-decidir-el-destino-de-la-fase-10) | Largo plazo | Decidir el destino de la Fase 10 |
| [R10](#r10-observabilidad-operativa-y-pedagógica) | Largo plazo | Observabilidad operativa y pedagógica |
| [R11](#r11-limpieza-de-artefactos-y-política-de-git) | Largo plazo | Limpieza de artefactos y política de Git |
| [R12](#r12-sanitización-total-de-html-pedagógico) | Corto plazo (seguridad) | Sanitización total de HTML pedagógico |
| [R13](#r13-migración-de-auth-a-cookies-httponly-en-producción) | Corto/medio | Migración de auth a cookies HttpOnly |
| [R14](#r14-unificar-nomenclatura-y-ortografía-de-infraestructura) | Medio plazo | Unificar nomenclatura e infraestructura |

---

## Cómo usar este documento

1. **Priorizar por riesgo × esfuerzo**, no solo por orden numérico.
2. Cada recomendación incluye un **plan de implementación por etapas** y **criterios de aceptación**.
3. Cuando una recomendación ya tenga un OpenSpec activo, se referencia explícitamente.
4. No mezclar en un mismo PR: renumeración de fases + refactor de motor + hardening de auth. Son cambios de alto radio de explosión.

### Matriz rápida de priorización

| ID | Impacto | Urgencia | Esfuerzo | Dependencias |
|----|---------|----------|----------|--------------|
| R1 | Crítico | Alta | Medio | Ninguna (bloquea claridad de R5/R9) |
| R2 | Crítico | Alta | Medio-Alto | OpenSpec `prepare-production-hardening` |
| R12 | Crítico | Alta | Medio | Parte de R2 |
| R13 | Crítico | Alta | Alto | Parte de R2 / modo dual cookie+token |
| R3 | Alto | Media | Bajo | Ninguna |
| R4 | Alto | Alta | Medio | R1 ayuda a no testear IDs incorrectos |
| R8 | Alto | Media | Bajo-Medio | R4 parcial, R3 |
| R5 | Alto | Media | Muy alto | R1, R4 |
| R6 | Medio | Media | Medio | R8 para no regresar |
| R7 | Alto | Media | Medio | Scripts existentes de auditoría |
| R11 | Medio | Media | Bajo | Política de equipo |
| R14 | Medio | Baja | Bajo-Medio | Coordinación con Portainer/VPS |
| R9 | Medio | Baja | Variable | R1 |
| R10 | Alto | Baja | Alto | R8, infra de logs/métricas |

---

## R1. Congelar el mapa canónico de IDs de fase

### Problema actual

Existe una **desalineación sistemática** entre:

| Capa | Ejemplo problemático |
|------|----------------------|
| Carpeta backend | `app/fase8/`, `app/fase9/`, `app/fase11/` |
| Prefijo API | `/fase8`, `/fase9` (tags a veces dicen `fase7`/`fase8`) |
| Frontend components | `components/fase8/*Fase7*.tsx`, `components/fase9/*Fase8*.tsx` |
| UI / rutas alumno | “Fase 9” de simulados montada sobre `fase11` |
| Documentación pedagógica | Mapa de Fases 1–9 en `docs/DISENO DE FASES/` |
| Seeds / `fase_id` en DB | Constantes `FASE7_ID`, etc., no siempre alineadas con el nombre de carpeta |

Esto no es cosmético: un seed, un dashboard o un test que use el ID incorrecto **rompe progreso de alumnos** o reescribe el pool de otra fase.

### Implicaciones de no actuar

- Bugs de desbloqueo entre fases (el alumno “aprueba” un módulo que no es).
- Seeds con purge que borran datos de la fase equivocada.
- Agentes de IA y desarrolladores nuevos implementan features en la carpeta incorrecta.
- Tests e2e frágiles y falsos verdes.
- Imposible refactorizar con confianza (R5 depende de R1).

### Implicaciones de actuar

- Puede requerir **renombres de archivos/carpetas** o, en el peor caso, **migración de `fase_id` en producción**.
- Hay que decidir si se corrige el **nombre de carpetas** manteniendo IDs de DB, o se renumeran IDs (mucho más riesgoso).
- Documentación, OpenSpec, `phaseMaps.ts` del admin y Traefik no cambian de dominio, pero sí de convenciones internas.

### Cómo implementarlo

#### Etapa 1 — Inventario (sin tocar código de runtime)

Crear un archivo canónico, por ejemplo:

`docs/MAPA_CANONICO_FASES.md`

Con una tabla fija:

| `fase_id` DB | Nombre pedagógico | Carpeta backend | Prefijo API | Carpeta frontend | Rutas UI | Seed key | Estado |
|-------------:|-------------------|-----------------|------------|------------------|----------|----------|--------|
| 1 | Aritmética básica | `fase1` | `/fase1` | `fase1` | `/welcome`, `/play`… | `fase_1` | Activa |
| 2 | … | `fase2` | `/fase2` | `fase2` | … | `fase_2` | Activa |
| … | … | … | … | … | … | … | … |
| 9 | Simulados Pedro II | `fase11` *(hoy)* | `/fase9` + `/fases/11/simulados` | `fase11` | … | … | Activa |
| 10 | Razonamiento abstracto | `fase10` | `/fase10` | `fase10` | — | — | Reservada |

Regla de oro: **el `fase_id` de PostgreSQL es la fuente de verdad**. Nombres de carpeta son alias.

#### Etapa 2 — Constantes únicas en código

Backend:

```python
# app/core/phases.py  (nuevo)
class PhaseId:
    FASE_1 = 1
    FASE_2 = 2
    # ...
    SIMULADOS = 9   # o 11, según lo que diga la tabla canónica
```

Todos los routers/seeds importan desde ahí. Prohibido hardcodear enteros mágicos en seeds grandes.

Frontend:

```ts
// constants/phases.ts
export const PHASE = {
  ARITHMETIC: 1,
  // ...
  SIMULADOS: 9,
} as const;
```

#### Etapa 3 — Alineación de nombres (sin migrar DB si es posible)

Preferencia de menor riesgo:

1. **No cambiar `fase_id` en producción** si ya hay alumnos con progreso.
2. Renombrar archivos frontend (`Fase7GameScreen` → `Fase8GameScreen` si la carpeta es `fase8`) **solo después** de actualizar imports y rutas.
3. Corregir `tags=` de FastAPI y comentarios engañosos.
4. Si la carpeta `fase11` es realmente la Fase 9 pedagógica, documentarlo como **alias histórico** o renombrar carpeta a `fase9_simulados` con re-exports de compatibilidad.

#### Etapa 4 — Guardas automáticas

- Test que falla si `router.prefix` no coincide con el mapa canónico.
- Script `scripts/verify_phase_map.py` que recorra routers y compare con el mapa.
- Checklist en `guia_creacion_fase.md`: “antes de crear fase N, actualizar el mapa canónico”.

### Criterios de aceptación

- [ ] Existe un único documento de mapa canónico referenciado desde README y `APP_VERSION.md`.
- [ ] Cero discrepancias entre `fase_id` en seeds y prefijos documentados.
- [ ] Un desarrollador nuevo puede responder “¿dónde está la Fase 8?” en menos de 30 segundos.
- [ ] Ningún test e2e navega a una ruta de fase con ID incorrecto.

### Riesgos de implementación

| Riesgo | Mitigación |
|--------|------------|
| Romper imports masivos al renombrar | Renombrar en PR aislado; usar `git mv`; CI typecheck |
| Confundir alumnos en producción | No cambiar labels de UI sin aviso; el ID interno puede diferir del número de marketing si se documenta |
| Migración de DB accidental | Prohibir `UPDATE fases SET id=…` salvo plan con backup y freeze de deploys |

---

## R2. Completar hardening de producción

### Problema actual

El proyecto ya corre en VPS/Portainer y tiene piezas de seguridad, pero el OpenSpec `openspec/changes/prepare-production-hardening/` muestra trabajo **parcialmente pendiente**:

- Sanitización HTML incompleta
- Auth aún orientada a token en `localStorage`
- Endpoints admin sensibles
- Mezcla histórica de `create_all` vs Alembic
- CORS y variables de entorno a endurecer
- Quality gates y budgets de bundle

Varias tareas del checklist OpenSpec ya están hechas (p. ej. `tsc --noEmit && vite build`), otras no.

### Implicaciones de no actuar

- XSS vía teoría/preguntas con HTML pedagógico.
- Robo de sesión por XSS + JWT en `localStorage`.
- Exposición de configuración de infraestructura.
- Drift de schema entre entornos.
- Deploys “que funcionan en local” y fallan o son inseguros en prod.

### Implicaciones de actuar

- Cambios transversales frontend + backend + env de Portainer.
- Posible necesidad de **re-login** de usuarios al migrar a cookies.
- Más fricción en desarrollo local si no se mantiene modo dual (`token` vs `cookie`).
- Tiempo de QA más alto antes del próximo release.

### Cómo implementarlo

Seguir el orden del propio OpenSpec (ya validado conceptualmente):

1. **HTML seguro** (R12)  
2. **Backend/config** (CORS, `create_all`, system-config, SQL echo)  
3. **Auth cookies** (R13)  
4. **Quality gates** (R8 parcial)  
5. **Bundles** (R6)

#### Checklist operativo por entorno

Para **producción** (`ENVIRONMENT=production`):

| Variable / flag | Valor recomendado |
|-----------------|-------------------|
| `ENVIRONMENT` | `production` |
| `SESSION_MODE` | `cookie` |
| `COOKIE_SECURE` | `true` |
| `COOKIE_SAMESITE` | `lax` o `strict` según subdominios |
| `ALLOWED_ORIGINS` | dominios exactos, sin `*` |
| `ENABLE_SECURITY_HEADERS` | `true` |
| `ENABLE_SYSTEM_CONFIG_ENDPOINT` | `false` |
| `SQL_ECHO` | `false` |
| `SKIP_DB_ALTERATIONS` / no-`create_all` | activo (Alembic only) |

Para **local**:

| Variable / flag | Valor recomendado |
|-----------------|-------------------|
| `ENVIRONMENT` | `development` |
| `SESSION_MODE` | `token` (comodidad) o `cookie` con dominio localhost |
| `ALLOWED_ORIGINS` | `http://localhost:5173`, `http://127.0.0.1:5173` |
| `ENABLE_SYSTEM_CONFIG_ENDPOINT` | `true` solo si se necesita debug |

#### Plan de PR sugerido (no un monolitico)

1. PR-A: sanitización HTML + tests XSS  
2. PR-B: flags backend + CORS + system-config  
3. PR-C: cookies auth + frontend `credentials: "include"`  
4. PR-D: docs Portainer + `.env.example` unificado  
5. PR-E: budgets/bundle (puede ir con R6)

### Criterios de aceptación

- [ ] Todas las tareas abiertas de `prepare-production-hardening/tasks.md` cerradas o explicitamente descartadas con motivo.
- [ ] Checklist de deploy en `DEPLOY.md` actualizado (cookies, CORS, migraciones, rollback).
- [ ] Smoke test post-deploy: login, una pregunta de fase, admin analytics, logout.
- [ ] No se exponen secretos ni `DATABASE_URL` por HTTP.

### Referencias internas

- `openspec/changes/prepare-production-hardening/`
- `DEPLOY.md`
- `LogicaMath/backend/app/config.py`
- `LogicaMath/backend/app/main.py`

---

## R3. Alinear versionado de producto

### Problema actual

Hoy coexisten varios “números de versión” que no se hablan entre sí:

| Fuente | Valor observado |
|--------|-----------------|
| FastAPI `version=` en `main.py` | `3.0.0` |
| `package.json` frontend | `0.0.0` |
| Tags/commits humanos | `0.0.2` … `0.0.8` |
| `APP_VERSION.md` | documenta la divergencia |
| Seeds (`SEED_VERSIONS`) | versiones por fase independientes (correcto) |

### Implicaciones de no actuar

- Imposible correlacionar un bug de producción con el código desplegado.
- Soporte y docentes no saben “qué versión ven los alumnos”.
- Releases y changelogs se vuelven anecdóticos.
- Portainer muestra imágenes sin semántica de versión.

### Implicaciones de actuar

- Disciplina de release (aunque sea ligera).
- Posible endpoint `/health` o `/version` que devuelva build info.
- El frontend debe mostrar o loguear la versión en admin/SRE.

### Cómo implementarlo

#### Convención recomendada (SemVer de producto)

```text
MAJOR.MINOR.PATCH

MAJOR  → ruptura de progreso/pedagogía o auth incompatible
MINOR  → nueva fase, feature admin, cambios visibles
PATCH  → fixes, seeds correctivos, seguridad menor
```

Separar **versión de producto** de **versión de seed por fase**:

- Producto: `1.4.2`
- Seed Fase 4: `20260725_v3` (sigue en `SEED_VERSIONS`)

#### Cambios concretos

1. Unificar en un solo lugar de verdad, p. ej. `APP_VERSION.md` + archivo `version.json` o variables de build:

```text
APP_VERSION=1.0.0
GIT_SHA=<sha>
BUILD_DATE=<iso>
```

2. Backend: leer `APP_VERSION` y exponer:

```http
GET /health
→ { "status": "ok", "version": "1.0.0", "git_sha": "9303f33" }
```

3. Frontend: inyectar en build Vite:

```ts
// import.meta.env.VITE_APP_VERSION
```

4. `package.json` → misma versión de producto (no dejar `0.0.0`).
5. Tags git: `v1.0.0` alineados con el deploy en Portainer.
6. Changelog breve en `CHANGELOG.md` (solo releases, no cada commit).

### Criterios de aceptación

- [ ] Backend, frontend y tag git reportan la misma versión de producto en un release.
- [ ] El panel admin/SRE muestra versión y SHA.
- [ ] `APP_VERSION.md` deja de describir divergencias y pasa a describir el esquema.

---

## R4. Tests de contrato por fase

### Problema actual

Cada router de fase (Fase 2–9) ronda **1.100–1.300 líneas** con reglas críticas:

- selección de pregunta del pool  
- validación de respuesta  
- Bucle Espejo / bloque de rescate  
- Early Exit  
- actualización de `ProgresoMaestria`  
- desbloqueo de niveles y espejo visual  

La suite actual cubre piezas valiosas (auth, UX feedback, algunos visualizadores, e2e parciales), pero **no garantiza paridad de reglas entre fases**.

### Implicaciones de no actuar

- Un fix en Fase 5 puede no portarse a Fase 6–8 (drift).
- Regresiones silenciosas en desbloqueo y % de maestría.
- Refactor del motor genérico (R5) se vuelve suicida sin red de seguridad.
- Docentes ven comportamientos distintos “sin razón aparente”.

### Implicaciones de actuar

- Inversión inicial en fixtures y factories de alumno/progreso.
- Tests más lentos si se abusa de e2e; conviene **contrato API** (httpx/async) más que UI.
- Hay que definir qué es “comportamiento canónico” del Documento Rector.

### Cómo implementarlo

#### Capa 1 — Contrato HTTP por fase (prioridad)

Para cada fase activa, un archivo:

`backend/tests/contracts/test_fase{N}_contract.py`

Casos mínimos obligatorios:

| Caso | Qué verifica |
|------|----------------|
| `dashboard_requires_auth` | 401 sin token |
| `dashboard_shape` | claves: módulos, niveles, teoría, progreso |
| `get_question_from_pool` | pregunta pertenece a `fase_id` y nivel pedidos |
| `answer_correct_updates_mastery` | contadores y estado |
| `answer_incorrect_mirror_loop` | payload de espejo / tipo_error |
| `early_exit_triggers` | al N-ésimo error en desafío |
| `unlock_next_level` | solo cuando se cumplen reglas de config |
| `no_mock_on_error` | errores de API no devuelven progreso inventado |

Usar un **alumno de prueba** creado en fixture y rollback/transacción por test.

#### Capa 2 — Matriz de paridad

Tabla parametrizada:

```python
@pytest.mark.parametrize("fase_id,prefix", [
    (2, "/fase2"),
    (3, "/fase3"),
    # ...
])
async def test_dashboard_contract(fase_id, prefix, client, auth_headers):
    ...
```

Así un endpoint que se desvía del contrato falla en CI.

#### Capa 3 — E2E smoke (Playwright)

No re-testear toda la pedagogía en UI. Solo:

1. Login alumno  
2. Entrar a welcome de fase  
3. Responder 1 pregunta de práctica  
4. Ver feedback  
5. Volver al mapa  

Un spec por fase o un spec parametrizado `fases.e2e.spec.ts` (ya existe base).

#### Capa 4 — Datos de seed de test

- Base de datos de CI con seed mínimo (pocas preguntas por nivel), no el pool completo de producción.
- Variable `SEED_MINIMAL=true` o fixtures SQL.

### Criterios de aceptación

- [ ] Al menos Fases 2–8 tienen contrato de dashboard + answer.
- [ ] Early Exit y desbloqueo tienen al menos un test cada uno en una fase TJS y una legacy.
- [ ] PR que rompa la forma del payload de respuesta falla en CI.
- [ ] Tiempo total de tests de contrato < 5–8 minutos en CI.

---

## R5. Extraer un motor genérico de fase

### Problema actual

Los routers `fase2`…`fase9` son **casi clones** con variaciones de:

- IDs y prefijos  
- reglas TJS vs legacy  
- validadores específicos (fracciones, geometría, etc.)  
- payloads de visualizadores  

Esto multiplica bugs y hace que cada mejora pedagógica se implemente N veces.

### Implicaciones de no actuar

- Costo de mantenimiento lineal (o peor) con cada fase nueva.
- Inconsistencias de UX/reglas entre fases “gemelas”.
- Code review imposible de hacer bien (PRs de 1.200 líneas × N).
- Riesgo alto al corregir seguridad o progreso global.

### Implicaciones de actuar

- Refactor de alto impacto: puede romper todas las fases a la vez si se hace mal.
- Requiere R1 (mapa canónico) y R4 (contratos) **antes**.
- Curva de aprendizaje: los devs deben entender el motor + plugins, no N copias.

### Cómo implementarlo (estrategia strangler)

**No** reescribir todo de golpe. Usar patrón *strangler fig*:

#### Etapa 1 — Extraer utilidades puras

Mover a `app/services/phase_engine/`:

- normalización de respuesta  
- cálculo de maestría / porcentaje  
- decisión Early Exit  
- aplicación de errores tolerados TJS  
- sincronización de `unlockedLevels` espejo  

Cada función con tests unitarios aislados.

#### Etapa 2 — Definir interfaz de fase

```python
class PhasePlugin(Protocol):
    fase_id: int
    prefix: str
    seed_key: str

    def validate_answer(self, pregunta, payload) -> AnswerResult: ...
    def build_question_dto(self, pregunta) -> dict: ...
    def visual_hints(self, pregunta) -> dict | None: ...
```

Routers delgados:

```python
router = build_phase_router(Fase4Plugin())
```

#### Etapa 3 — Migrar una fase piloto

Elegir **Fase 6 o 7** (madura, no la más compleja visualmente) o **Fase 5** si el generador ya está bien separado.

Criterio del piloto:

- contratos verdes (R4)  
- paridad byte-a-byte de payloads críticos (o snapshot JSON)  
- feature flag `USE_PHASE_ENGINE_F5=true`

#### Etapa 4 — Migrar el resto

Orden sugerido: 6 → 7 → 8 → 5 → 4 (4 es la más rica en UI) → 3 → 2 → 1 (1 tiene más legado).

Simulados (Fase 9/11) **no entran** al mismo motor de práctica: es otro flujo (examen). Pueden compartir solo auth, progreso y clínicas de error.

#### Etapa 5 — Frontend genérico

Ya existe `fase_generic/`. Extenderlo para que más fases lo usen y dejen solo:

- visualizadores específicos  
- theory modals especiales  
- servicios de API delgados  

### Criterios de aceptación

- [ ] Al menos 3 fases de práctica corren sobre el motor compartido.
- [ ] Diferencia de LOC de router por fase baja drásticamente (objetivo: < 200 líneas de wiring).
- [ ] Un cambio de Early Exit se hace en un solo archivo y afecta a todas las fases migradas.
- [ ] Contratos R4 siguen verdes.

### Anti-patrones a evitar

- “Framework” demasiado abstracto antes de 2 fases migradas.
- Meter validación de fracciones y de geometría en el core genérico (van en plugins).
- Duplicar el motor en frontend y backend: la autoridad sigue en servidor.

---

## R6. Reducir y gobernar el bundle frontend

### Problema actual

Dependencias pesadas en gameplay/admin:

- `three`  
- `fabric`  
- `recharts`  
- `framer-motion`  
- visualizadores de fracciones/porcentajes/geometría  

El code splitting con `React.lazy` ya existe en `App.tsx`, pero imports estáticos dentro de módulos pueden **anular** el beneficio. El OpenSpec de hardening ya prevé baseline y budgets.

### Implicaciones de no actuar

- Tiempo de carga alto en redes escolares / móviles.
- Peor LCP y frustración en tablets del colegio.
- Cada nueva fase “cara” degrada a todas si se importa en el entrypoint.

### Implicaciones de actuar

- Refactors de imports y a veces de arquitectura de componentes.
- Más archivos de chunk; hay que vigilar waterfall de requests.
- Posible demora percibida al **entrar** a una fase (lazy) a cambio de mapa/login más rápido.

### Cómo implementarlo

#### 1. Baseline

```bash
cd LogicaMath/frontend
npm run build
# inspeccionar dist/assets y tamaños
```

Registrar en `docs/perf/bundle-baseline.md`:

| Chunk | Tamaño gzip | Quién lo carga |
|-------|-------------|----------------|
| index | … | todos |
| fase4 | … | ruta fase 4 |
| admin | … | solo ADMIN |
| three-vendor | … | visualizadores 3D |

#### 2. Reglas de import

- Prohibido importar `three` / `fabric` desde `App.tsx`, `LoginScreen`, `PhaseMapScreen`.
- Visualizadores: `const Viz = lazy(() => import('./FractionVisualizer'))`.
- Admin: ya es ruta separada; asegurar que no entre en el grafo del alumno.

#### 3. Vendor chunks en Vite

Configurar `manualChunks` para aislar:

- `react-vendor`  
- `charts` (recharts)  
- `canvas` (fabric)  
- `three`

#### 4. Budget

Ejemplo inicial (ajustar tras baseline real):

| Métrica | Budget |
|---------|--------|
| Entry JS inicial (gzip) | < 250 KB |
| Chunk de una fase (gzip) | < 300 KB |
| Admin (gzip) | < 400 KB |

Fallar CI si se supera un umbral configurable (R8).

#### 5. Runtime

- Prefetch de la siguiente fase solo cuando el alumno está en su welcome.
- Comprimir assets en Nginx (`gzip`/`brotli` ya típico en la imagen frontend).

### Criterios de aceptación

- [ ] Baseline documentado y comparado en cada release.
- [ ] Login + mapa no descargan Three/Fabric.
- [ ] Budget de entry no se viola sin aprobación explícita en PR.

---

## R7. Auditoría automática del pool en CI

### Problema actual

El Documento Rector exige:

- pool precargado  
- sin duplicados  
- respuesta matemáticamente coherente con el enunciado  
- purge limpio al reseedar  

Ya existen scripts (`audit_fases_5_6_7.py`, `audit_question_images.py`, etc.), pero su ejecución parece **manual/operativa**, no una compuerta de merge/deploy.

### Implicaciones de no actuar

- Preguntas con respuesta incorrecta llegan a alumnos.
- Imágenes rotas en MinIO (404 pedagógico).
- Duplicados reducen variedad real del pool.
- Seeds grandes se vuelven “caja negra”.

### Implicaciones de actuar

- CI más lenta o job separado nocturno.
- Falsos positivos si el auditor no entiende tipos de pregunta (fracciones, texto libre).
- Necesita DB de CI o validación offline sobre dumps/JSON de seed.

### Cómo implementarlo

#### Auditor mínimo unificado

`backend/scripts/audit_pool.py --fase N` que verifique:

1. **Unicidad** de `enunciado` (normalizado) por `(fase_id, seccion, sub_nivel)`.  
2. **Presencia** de `respuesta_correcta` no vacía.  
3. **Coherencia** según `tipo_pregunta`:
   - numérica: parseable  
   - múltiple opción: exactamente una alternativa marcada correcta en DB  
4. **Referencias de imagen**: URLs/MinIO existen o keys presentes.  
5. **Conteo mínimo** por nivel según `configuracion_progreso.cantidad_requerida` (o umbral de seed).  
6. **JSONB** de `explicacion_paso_a_paso` y `errores_previstos` con schema básico.

Exit code ≠ 0 si hay hallazgos críticos.

#### Integración

| Momento | Acción |
|---------|--------|
| PR que toca `seed.py` de una fase | Job CI corre auditor de esa fase |
| Nightly | Auditor de todas las fases activas |
| Pre-deploy producción | Job obligatorio + reporte artifact |

#### Reportes

Salida JSON + markdown:

```text
resultados/audit_fase4.json
resultados/audit_fase4.md
```

Reutilizar carpeta `resultados/` ya usada por SRE.

### Criterios de aceptación

- [ ] Un seed con respuesta incorrecta inventada a propósito falla el auditor.
- [ ] Duplicados exactos de enunciado fallan el auditor.
- [ ] Documentado en `DEPLOY.md` como paso pre-producción.
- [ ] No requiere MinIO real para checks puramente lógicos (imágenes pueden ser warning vs error).

---

## R8. Pipeline CI mínima en pull requests

### Problema actual

Hay scripts de test y quality gates locales, pero sin una **compuerta uniforme de PR** el merge a `producion` depende de disciplina humana. Eso es frágil en un repo con agentes y varios contribuidores.

### Implicaciones de no actuar

- TypeScript roto llega a build de Portainer.
- Regresiones de auth/fases solo se detectan en runtime.
- Hardening (R2) se revierte sin que nadie lo note.

### Implicaciones de actuar

- Minutos de espera por PR.
- Hay que mantener la CI verde (costo cultural positivo).
- Secrets de CI (DB de test, etc.) hay que configurarlos una vez.

### Cómo implementarlo

#### Pipeline mínima recomendada (GitHub Actions)

```yaml
# .github/workflows/pr-checks.yml
jobs:
  frontend:
    - npm ci
    - npx tsc --noEmit
    - npm test          # vitest unit only
    - npm run build
  backend:
    - pip install -r requirements.txt
    - pytest tests/ -q
    # opcional: contracts si hay postgres service
  # opcional nightly:
  #   playwright + audit_pool
```

#### Separación correcta de runners

Ya prevista en hardening:

- Vitest: `*.test.ts(x)`  
- Playwright: `*.spec.ts`  
- No mezclar en el mismo comando de PR si e2e es lento: e2e en `main`/nightly o label `run-e2e`.

#### Gates por criticidad de path

| Paths tocados | Jobs obligatorios |
|---------------|-------------------|
| `frontend/**` | tsc + vitest + build |
| `backend/app/fase*/**` | pytest + contract de esa fase + audit seed si hay seed |
| `backend/app/auth*` / `routers/auth*` | tests auth |
| `docker-compose*` / Dockerfiles | build images (opcional) |

#### Protección de rama

En GitHub:

- `producion` y `main` (si existe) con **required checks**.  
- Prohibir push directo si el equipo es >1 persona.

### Criterios de aceptación

- [ ] Todo PR ejecuta al menos typecheck frontend + tests unitarios backend/frontend.
- [ ] Build de frontend forma parte del check (no solo tsc).
- [ ] Documentado en README: “cómo correr lo mismo que CI en local”.

---

## R9. Decidir el destino de la Fase 10

### Problema actual

`app/fase10/router.py` solo expone un stub:

```text
status: reserved
nombre: Razonamiento Abstracto y Visual
```

El frontend tiene carpeta `fase10` vacía. El mapa pedagógico documentado llega con claridad hasta Fase 9/simulados; la 10 está “reservada” sin diseño interno completo.

### Implicaciones de no actuar

- Ruido en el mapa de producto (“¿está o no está?”).
- Agentes pueden intentar “completar” la fase sin diseño rector.
- El mapa del alumno puede mostrar huecos o locks confusos.

### Implicaciones de actuar

- Si se **implementa**: gran esfuerzo de diseño pedagógico + seed + UI (similar a una fase completa).
- Si se **archiva**: hay que ocultarla del mapa, admin y docs para no prometer contenido.

### Cómo implementarlo

#### Opción A — Archivar (recomendado si no hay diseño aprobado)

1. Mantener endpoint `/fase10/status` pero con `status: "archived"` o eliminarlo del menú alumno.  
2. Excluir `fase_id=10` del `PhaseMapScreen` y del admin tree.  
3. Documentar en mapa canónico (R1): “reservada / fuera de roadmap Qx”.  
4. No aceptar PRs de gameplay de Fase 10 sin tomo de diseño aprobado.

#### Opción B — Activar formalmente

1. Escribir tomo de diseño en `docs/DISENO DE FASES/fase10.md` siguiendo `guia_creacion_fase.md`.  
2. Definir módulos, niveles, TJS, teoría y pool.  
3. Implementar plugin del motor (R5) en lugar de clonar 1.300 líneas.  
4. Seed versionado + contratos R4 + e2e smoke.  
5. Soft-launch solo para admin/evaluador antes de alumnos.

#### Decisión de producto (obligatoria)

Registrar en este doc o en el mapa canónico:

```text
Decisión Fase 10: ARCHIVADA hasta YYYY-MM | o EN DISEÑO | o EN BUILD
Owner: ...
```

### Criterios de aceptación

- [ ] El mapa alumno no promete una fase jugable que no existe.
- [ ] Existe decisión escrita y fecha de revisión.
- [ ] Si se construye, nace sobre motor genérico + contratos, no como clon.

---

## R10. Observabilidad operativa y pedagógica

### Problema actual

Hay piezas de SRE admin, logs print, audit middleware y scripts de comparación de entornos, pero falta un **sistema de observabilidad** unificado:

- métricas de latencia API  
- tasa de errores 5xx  
- fallos de MinIO  
- eventos pedagógicos (early exits, % de abandono por nivel)  
- correlación request-id  

### Implicaciones de no actuar

- Incidentes se diagnostican por SSH y conjetura.
- No se detecta degradación pedagógica (un nivel imposible o roto).
- Hardening y deploys no tienen “antes/después” medible.

### Implicaciones de actuar

- Infra adicional (Prometheus/Grafana, Loki, OpenTelemetry, o al menos logs estructurados).
- Coste de almacenamiento de logs/métricas.
- Hay que cuidar **privacidad** de menores (no loguear respuestas completas ni PII innecesaria).

### Cómo implementarlo

#### Nivel 1 — Logs estructurados (rápido)

- Reemplazar `print` críticos por logger JSON: `timestamp`, `level`, `request_id`, `fase_id`, `path`, `user_role` (no username si se puede evitar).  
- Middleware que propague `X-Request-ID`.

#### Nivel 2 — Health y readiness

```http
GET /health      → proceso vivo
GET /ready       → DB + Redis + (opcional) MinIO ping
```

Traefik/Portainer usan `/ready` para no mandar tráfico a backends a medio arrancar.

#### Nivel 3 — Métricas

Contadores/histogramas:

- `http_request_duration_seconds{path,status}`  
- `phase_answer_total{fase_id,result}`  
- `phase_early_exit_total{fase_id}`  
- `seed_run_total{fase,result}`  
- `minio_errors_total`

Export Prometheus o, si se prefiere simplicidad, endpoint admin ya existente enriquecido + retención.

#### Nivel 4 — Producto pedagógico

Dashboard admin (extender `SreTab` / analytics):

- tasa de acierto por nivel  
- tiempo medio por pregunta  
- early exits por desafío  
- preguntas con más errores del tipo X  

Alertas humanas semanales para docentes/admin, no solo on-call técnico.

### Criterios de aceptación

- [ ] Se puede responder en < 5 minutos: “¿la API está sana?” y “¿MinIO responde?”.  
- [ ] Un deploy deja traza de versión (R3) + error rate antes/después.  
- [ ] No se almacenan datos sensibles de menores en logs de aplicación.

---

## R11. Limpieza de artefactos y política de Git

### Problema actual

El árbol de trabajo incluye o ha incluido:

- `node_modules/` y `dist/`  
- `playwright-report/`, `test-results/`  
- dumps SQL enormes (`backup_fase4_tjs.sql` ~ decenas de MB)  
- backups locales en `Datos_*`  
- documentación operativa sensible (parte ya en `.gitignore`)

Aunque parte esté ignorada, la **política** no siempre es obvia para humanos y agentes.

### Implicaciones de no actuar

- Clones lentos, PRs ruidosos, riesgo de subir secretos o PII.  
- Confusión sobre qué es fuente de verdad vs basura local.  
- Backups de DB dentro del repo de código (anti-patrón).

### Implicaciones de actuar

- Hay que reubicar backups a storage externo (S3/MinIO privado, drive del equipo).  
- Posible reescritura de historia **solo si** ya se subieron binarios grandes (coordinar; no hacer `git filter-repo` a la ligera en `producion`).

### Cómo implementarlo

#### 1. Política escrita (este mismo repo)

Crear `docs/POLITICA_REPOSITORIO.md` (o sección en README):

| Tipo | ¿En Git? | Dónde va |
|------|----------|----------|
| Código fuente | Sí | `LogicaMath/` |
| Specs OpenSpec activas | Según política actual | `openspec/` (hoy parcialmente ignorado) |
| `.env` y secretos | **Nunca** | Portainer / vault local |
| Backups SQL/dump | **Nunca** | bucket privado `backups/` |
| `node_modules`, `dist` | **Nunca** | build local/CI |
| Reportes Playwright | **Nunca** | artifacts de CI |
| PDFs Pedro II | Opcional (licencia/peso) | preferible storage + referencia |

#### 2. `.gitignore` reforzado

Asegurar entradas para:

```gitignore
**/node_modules/
**/dist/
**/playwright-report/
**/test-results/
*.dump
*.sql
!**/migrations/*.sql   # solo si se versionan migraciones SQL pequeñas a propósito
Datos_localhost/
Datos_Desarrollo/
Datos_Producion/
.env
.env.*
```

#### 3. Limpieza puntual

- Mover `backup_fase4_tjs.sql` fuera del working tree de app.  
- Borrar reportes locales generados.  
- Si un binario grande ya está en el remoto: plan de purga coordinado + aviso al equipo.

#### 4. Pre-commit opcional

Hook o CI check que falle si se agregan archivos `> 5 MB` sin label `allow-large-file`.

### Criterios de aceptación

- [ ] Clone fresco < tamaño razonable sin node_modules ni dumps.  
- [ ] Ningún secreto en historial reciente de la rama de deploy.  
- [ ] Política leíble en < 3 minutos por un dev nuevo.

---

## R12. Sanitización total de HTML pedagógico

> Subconjunto crítico de R2, elevado a recomendación propia por riesgo XSS.

### Problema actual

El contenido pedagógico usa HTML intencional (`keyword-highlight`, pasos de teoría, etc.) y se renderiza con `dangerouslySetInnerHTML` en varios componentes. Existe `dompurify` y usos de `sanitizeHtml` en algunos sitios (p. ej. UX overlay), pero **no es universal**.

### Implicaciones de no actuar

- Un admin comprometido o un seed malicioso inyecta script.  
- Con JWT en `localStorage` (hoy), XSS ≈ robo de sesión.  
- Incumplimiento de buenas prácticas para apps escolares.

### Implicaciones de actuar

- Hay que tunear el allowlist de DOMPurify para **no romper** el diseño pedagógico (spans, clases, strong, sub/sup, etc.).  
- Tests visuales/manuales de teoría en varias fases.  
- Posible rechazo de atributos `style=` si se endurece demasiado (coordinar con CSS por clases).

### Cómo implementarlo

1. Helper único:

```ts
// services/sanitizeHtml.ts
import DOMPurify from 'dompurify';

const ALLOWED_TAGS = ['span', 'strong', 'em', 'br', 'p', 'ul', 'ol', 'li', 'sub', 'sup', 'b', 'i'];
const ALLOWED_ATTR = ['class', 'data-keyword'];

export function sanitizeHtml(dirty: string): string {
  return DOMPurify.sanitize(dirty, { ALLOWED_TAGS, ALLOWED_ATTR });
}
```

2. Grep de `dangerouslySetInnerHTML` y envolver **todos** los valores.  
3. Prohibir en code review el uso sin `sanitizeHtml`.  
4. Tests:

```ts
expect(sanitizeHtml('<img src=x onerror=alert(1)>')).not.toContain('onerror');
expect(sanitizeHtml('<span class="keyword-highlight">x</span>')).toContain('keyword-highlight');
```

5. Opcional backend: sanitizar al **guardar** teoría/preguntas en admin (defensa en profundidad).

### Criterios de aceptación

- [ ] Cero `dangerouslySetInnerHTML` sin sanitizar.  
- [ ] Tests XSS unitarios en CI.  
- [ ] Teoría de Fase 4 y 5 se ve igual (clases de highlight intactas).

---

## R13. Migración de auth a cookies HttpOnly en producción

> Subconjunto crítico de R2.

### Problema actual

El frontend usa patrones basados en `localStorage.getItem('auth_token')` en gameplay y otros flujos. El backend ya tiene flags `SESSION_MODE`, `COOKIE_SECURE`, `COOKIE_SAMESITE`, lo que indica **preparación parcial** pero no adopción completa.

### Implicaciones de no actuar

- Cualquier XSS lee el token.  
- Tokens en storage persisten más de lo deseable.  
- Auditores de seguridad escolares lo marcarán como hallazgo alto.

### Implicaciones de actuar

- Todos los `fetch` autenticados necesitan `credentials: "include"`.  
- CORS no puede usar `*` con credenciales.  
- Local dev debe seguir siendo ergonómico (modo token).  
- Apps nativas futuras (si las hubiera) preferirían token; por eso el modo dual.

### Cómo implementarlo

#### Backend

1. Login:
   - valida credenciales  
   - si `SESSION_MODE=cookie`: setea cookie `HttpOnly`, `Secure` (prod), `SameSite`, path `/`  
   - opcional: también devuelve token en dev  
2. Logout: borra cookie.  
3. Dependencia `get_current_user`: lee cookie primero, luego `Authorization: Bearer` si modo híbrido.  
4. CSRF: con `SameSite=Lax/Strict` baja el riesgo; si hay usos cross-site, añadir token CSRF.

#### Frontend

1. `apiHelper`: `credentials: "include"` siempre en prod.  
2. Eliminar lecturas de `auth_token` en rutas de producción; mantener solo si `import.meta.env.DEV && SESSION_MODE===token`.  
3. `/users/me` al boot para hidratar sesión (en lugar de decodificar JWT local).  
4. Modo evaluador admin: no guardar secretos extra en `localStorage` sin necesidad.

#### Rollout

1. Deploy backend con soporte híbrido.  
2. Deploy frontend cookie-aware.  
3. Forzar re-login.  
4. Desactivar emisión de token en body en producción tras N días.

### Criterios de aceptación

- [ ] En prod, DevTools → Application → Local Storage **no** contiene JWT.  
- [ ] Cookie de sesión HttpOnly presente tras login.  
- [ ] Logout invalida la sesión de forma efectiva.  
- [ ] Localhost sigue documentado y usable.

---

## R14. Unificar nomenclatura y ortografía de infraestructura

### Problema actual

Inconsistencias que dificultan operación y automatización:

| Actual | Preferible |
|--------|------------|
| rama / carpeta `producion` | `production` o mantener alias documentado |
| `Datos_Producion` | `Datos_Produccion` / `Datos_Production` |
| `coelgio` / `coelgiomilitar` | `colegio` |
| `instalcion_clonador_voz.md` | `instalacion_...` |
| Dominios y `NOMBRE_APP` distintos por env | OK, pero documentar tabla única |

### Implicaciones de no actuar

- Scripts y docs fallan por typos de path.  
- Onboarding lento.  
- Riesgo de aplicar compose al entorno equivocado.

### Implicaciones de actuar

- Renombrar ramas y carpetas es **doloroso** si Portainer apunta a paths fijos.  
- Mejor **alias + documentación** que renames agresivos en caliente.

### Cómo implementarlo

1. Tabla oficial de entornos en `DEPLOY.md`:

| Entorno | Rama | Compose | Dominio | `NOMBRE_APP` |
|----------|------|---------|---------|--------------|
| Local | *feature* | `Datos_localhost/docker-compose.local.yml` | localhost | — |
| Desarrollo | `desarrollo` | `Datos_Desarrollo/...` | logica.espalhar.shop | pruebas |
| Producción | `producion` *(nombre histórico)* | `Datos_Producion/...` | matematicas.espalhar.shop | matematicas_Kids |

2. No renombrar la rama `producion` sin plan de Portainer/webhooks.  
3. Corregir typos solo en **docs nuevas** y filenames no referenciados por infra.  
4. Para archivos legacy, dejar redirect en la primera línea: `> Renombrado conceptualmente a X; path histórico conservado`.

### Criterios de aceptación

- [ ] Un runbook permite a un operador desplegar sin adivinar el spelling de carpetas.  
- [ ] `APP_VERSION.md` y `DEPLOY.md` usan la misma tabla de entornos.

---

## Plan de ejecución sugerido (roadmap)

### Sprint 1–2 (cimientos de seguridad y claridad)

1. R1 — Mapa canónico (doc + constantes, sin renames masivos aún)  
2. R12 — Sanitización HTML completa  
3. R3 — Versionado unificado + `/health`  
4. R11 — Política git + ignores (rápido)  
5. Cerrar flags backend de R2 (CORS, system-config, create_all)

### Sprint 3–4 (auth y calidad)

6. R13 — Cookies HttpOnly en prod (híbrido)  
7. R4 — Contratos para Fases 2, 4 y 5 (piloto)  
8. R8 — GitHub Actions mínima  
9. R7 — Auditor de pool en CI para seeds tocados  

### Sprint 5–8 (estructura)

10. R5 — Motor genérico, fase piloto migrada  
11. R6 — Bundle budgets  
12. R4 — Extender contratos al resto de fases  
13. R14 — Runbook de nomenclatura  

### Backlog estratégico

14. R9 — Decisión formal Fase 10  
15. R10 — Observabilidad L1→L3  
16. R5 — Migración completa de fases al motor  

---

## Plantilla de seguimiento por recomendación

Copiar por cada ítem en el tablero del equipo:

```markdown
### [ID] Título
- Estado: pending | in_progress | blocked | done
- Owner:
- PR(s):
- Dependencias:
- Riesgo residual:
- Evidencia de aceptación:
- Fecha de cierre:
```

---

## Relación con documentos existentes

| Documento | Relación |
|-----------|----------|
| `docs/Criterios Diseno Fase/1_Documento_Rector_Pedagogico.md` | Fuente de verdad pedagógica; R4/R5/R7 deben respetarlo |
| `openspec/changes/prepare-production-hardening/` | Desglose táctico de R2, R6, R12, R13 |
| `DEPLOY.md` | Debe absorber checklists de R2, R3, R7, R14 |
| `APP_VERSION.md` | Debe evolucionar con R3 y R1 |
| `guia_creacion_fase.md` | Debe exigir mapa canónico (R1) y motor/plugin (R5) |
| `reglas.md` / `gemini.md` | Operativa para agentes; enlazar a este doc como priorización |

---

## Conclusión

Estas recomendaciones no buscan “añadir más features”, sino **hacer que LogicaKids Pro sea operable, seguro y evolutivo** a escala real de alumnos:

1. **Claridad** del mapa de fases (R1, R14, R9)  
2. **Seguridad de producción** (R2, R12, R13)  
3. **Calidad automatizada** (R4, R7, R8)  
4. **Arquitectura sostenible** (R5, R6)  
5. **Operación profesional** (R3, R10, R11)  

El orden crítico de bloqueo es:

```text
R1 (mapa) ──► R4 (contratos) ──► R5 (motor genérico)
 R2/R12/R13 (seguridad) en paralelo desde el día 1
 R8 (CI) tan pronto como haya algo que fallar en rojo
```

Cualquier implementación debería cerrar criterios de aceptación de este documento o actualizarlos con justificación, nunca silenciarlos.

---

*Fin del documento `recomendacion_prioritarias.md`.*
