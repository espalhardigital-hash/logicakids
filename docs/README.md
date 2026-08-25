# Documentación del monorepo — LogicaKids / LogicaMath

Índice de **fuentes de verdad** por tema. Si dos docs chocan, gana la fila de esta tabla (y, para agentes, `RULES AGENTES/deep_analise_pro.md`).

## Fuentes de verdad

| Tema | Documento canónico | Notas |
|------|-------------------|--------|
| Comportamiento de agentes | [`RULES AGENTES/deep_analise_pro.md`](../RULES%20AGENTES/deep_analise_pro.md) | Entrada: [`AGENTS.md`](../AGENTS.md) |
| Plan de una tarea o fase | Solicitud actual + change OpenSpec/plan aprobado que la tarea identifique | Los planes históricos no se cargan ni se aplican de forma global |
| Sync preguntas + MinIO (local → VPS) | [`RULES AGENTES/bd_minio.md`](../RULES%20AGENTES/bd_minio.md) | Scripts: `LogicaMath/backend/scripts/sync_*` |
| Despliegue de **código** (Docker / Portainer) | [`DEPLOY.md`](../DEPLOY.md) (local, gitignored) + overview versionable abajo | No confundir con sync de datos |
| Overview de deploy (sin secretos) | [`docs/DEPLOY_OVERVIEW.md`](./DEPLOY_OVERVIEW.md) | Seguro para Git |
| Onboarding app / stack | [`LogicaMath/README.md`](../LogicaMath/README.md) | Enlace correcto a `../DEPLOY.md` |
| Versión y fuentes de datos UI | [`RULES AGENTES/APP_VERSION.md`](../RULES%20AGENTES/APP_VERSION.md) | |
| Permisos de herramientas del agente | [`RULES AGENTES/gemini.md`](../RULES%20AGENTES/gemini.md) | No sustituye el manual unificado |
| **Cómo reestructurar una fase (método)** | [`docs/reestructuracionGeneralFases.md`](./reestructuracionGeneralFases.md) | **Normativo.** Orden de planeación por etapas con gates, anti-patrones y reglas de delegación. Leer **antes** de reestructurar cualquier fase |
| **Auditoría y certificación de una fase** | [`docs/PROTOCOLO_AUDITORIA_Y_CERTIFICACION_FASES.md`](./PROTOCOLO_AUDITORIA_Y_CERTIFICACION_FASES.md) | **Normativo.** Evidencia exigida desde generador hasta recorrido real del alumno; leer antes de declarar una fase operable |
| **Criterios de teoría, ejemplos guiados y visuales** | [`docs/Criterios Diseno Fase/5_Criterios_Teoria_Ejemplos_y_Visuales.md`](./Criterios%20Diseno%20Fase/5_Criterios_Teoria_Ejemplos_y_Visuales.md) | **Normativo.** T3 (cero scroll) y T4 (ventana fija), anti-revelación en SVG, coherencia de enunciados |
| **Estado implementado de Fases 5 y 6** | [`docs/ESTADO_IMPLEMENTACION_FASES_5_6.md`](./ESTADO_IMPLEMENTACION_FASES_5_6.md) | **Vigente.** Sustituye preguntas espejo por corrección obligatoria de 10 s y documenta el banco local auditado |
| **Estado implementado de Fase 7** | [`docs/ESTADO_IMPLEMENTACION_FASE7.md`](./ESTADO_IMPLEMENTACION_FASE7.md) | **Vigente.** Corrección obligatoria de 10 s, banco visual auditable y cero scroll vertical |
| Memoria de implementación de Fase 4 | [`implementacionfase4.md`](../implementacionfase4.md) | Qué se construyó y por qué; complementa la auditoría |
| Histórico de reestructuración global 9→11 fases | [`docs/reestructuraciondefases.md`](./reestructuraciondefases.md) | **Ejecución parcial; no normativo.** Fase 4 cerrada; alineación física 7–11 pendiente |
| Auditoría de implementación de Fase 4 | [`auditoriafase4.md`](../auditoriafase4.md) | Evidencia histórica aprobada; no es plan activo |
| Traspaso de cambios OpenSpec pendientes de Fase 4 | [`docs/HANDOFF_CAMBIOS_PENDIENTES_FASE4.md`](./HANDOFF_CAMBIOS_PENDIENTES_FASE4.md) | Orden, prompts, gates de datos/UX y criterios de evidencia para continuar con otro modelo |
| Lista de pendientes detectados durante Fase 4 | [`faltantefase4.md`](../faltantefase4.md) | Checklist histórico supersedido; consultar solo para trazabilidad |
| Herramientas manuales mantenidas del backend | [`LogicaMath/backend/scripts/README.md`](../LogicaMath/backend/scripts/README.md) | Clasifica sincronización, auditoría y pruebas manuales |
| Histórico one-shot migración SQL 2026-07 | [`docs/historico/`](./historico/) | **No usar** en operaciones nuevas |

## Repositorio Git (estado del workspace)

| Campo | Valor |
|-------|--------|
| Remoto | `https://github.com/espalhardigital-hash/logicakids.git` |
| Rama producción / `origin/HEAD` | **`producion`** (no `main`) |
| Rama desarrollo | `desarrollo` (**congelada** — todo el trabajo activo va en `producion`) |
| App code | `LogicaMath/` |
| Carpeta local del monorepo | `APP_Logica_Matematicas_kids` (en VPS el clone suele llamarse `logicakids`) |

Si el remoto se mueve o se sustituye, actualiza en el **mismo cambio**: `git remote`, este índice, `LogicaMath/README.md`, `DEPLOY.md` / `DEPLOY_OVERVIEW.md` y `APP_VERSION.md`.

## Flujos rápidos

### Subir / alinear preguntas (datos)

1. Leer [`bd_minio.md`](../RULES%20AGENTES/bd_minio.md).
2. Pre-vuelo:

```bash
cd LogicaMath/backend
python scripts/sync_db_and_minio_prod.py --env dev --fase 5 --dry-run
```

3. Aplicar solo tras confirmación:

```bash
python scripts/sync_db_and_minio_prod.py --env dev --fase 5 --policy insert-new --yes
```

Fases **5 y 6** (SVG inline): no requieren MinIO `graphics/` (§1.3 de la skill).

### Desplegar código en VPS

1. Overview: [`DEPLOY_OVERVIEW.md`](./DEPLOY_OVERVIEW.md)
2. Detalle local (IPs, stacks): `DEPLOY.md` en la raíz (no versionado)

`git push` **no** despliega solo: hace falta pull en VPS + sync a Portainer + `docker compose -p …`.

## Qué no versionar

Ver `.gitignore`: `Datos_*`, `.env*`, `DEPLOY.md` sensible, dumps `*.sql`, histórico de migración con nombres de infra, `Pedro II/`, etc.

## Registro de limpieza general — 2026-07-30

Se ejecutó una depuración basada en referencias y pruebas:

- Se restauró `docs/reestructuraciondefases.md` como plan histórico global y se marcó su ejecución como parcial: Fase 4 cerrada, alineación física de Fases 7–11 pendiente.
- `auditoriafase4.md` se conserva como evidencia cerrada y `faltantefase4.md` como checklist histórico supersedido.
- Se retiraron 22 archivos versionados de reglas duplicadas, parches, renumeradores, inspectores, migraciones one-shot y auditorías de changes ya cerrados.
- Se eliminaron bases temporales, caches, builds y reportes reproducibles; Docker ignora ahora esos artefactos.
- Las herramientas manuales vigentes quedaron inventariadas en `LogicaMath/backend/scripts/README.md`.
- Las dos ubicaciones de pruebas backend forman parte de `pytest.ini`.
- No se eliminaron los componentes ni seeders cruzados de Fases 7–11: requieren una migración integral separada.

Verificación del lote:

- Backend local: `45 passed, 2 skipped, 2 xfailed`.
- Frontend: `46 passed`.
- Build frontend de producción: aprobado.
