# Documentación del monorepo — LogicaKids / LogicaMath

Índice de **fuentes de verdad** por tema. Si dos docs chocan, gana la fila de esta tabla (y, para agentes, `RULES AGENTES/deep_analise_pro.md`).

## Fuentes de verdad

| Tema | Documento canónico | Notas |
|------|-------------------|--------|
| Comportamiento de agentes | [`RULES AGENTES/deep_analise_pro.md`](../RULES%20AGENTES/deep_analise_pro.md) | Entrada: [`AGENTS.md`](../AGENTS.md) |
| Sync preguntas + MinIO (local → VPS) | [`RULES AGENTES/bd_minio.md`](../RULES%20AGENTES/bd_minio.md) | Scripts: `LogicaMath/backend/scripts/sync_*` |
| Despliegue de **código** (Docker / Portainer) | [`DEPLOY.md`](../DEPLOY.md) (local, gitignored) + overview versionable abajo | No confundir con sync de datos |
| Overview de deploy (sin secretos) | [`docs/DEPLOY_OVERVIEW.md`](./DEPLOY_OVERVIEW.md) | Seguro para Git |
| Onboarding app / stack | [`LogicaMath/README.md`](../LogicaMath/README.md) | Enlace correcto a `../DEPLOY.md` |
| Versión y fuentes de datos UI | [`RULES AGENTES/APP_VERSION.md`](../RULES%20AGENTES/APP_VERSION.md) | |
| Permisos de herramientas del agente | [`RULES AGENTES/gemini.md`](../RULES%20AGENTES/gemini.md) | No sustituye el manual unificado |
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
