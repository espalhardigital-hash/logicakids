# AGENTS.md — Project agent entrypoint (root stub)

> Agent rule packs live under **`RULES AGENTES/`**.
>
> ## Canonical manual
>
> **→ [`RULES AGENTES/deep_analise_pro.md`](./RULES%20AGENTES/deep_analise_pro.md)**
>
> *Deep Analysis PRO — Unified Agent Operating Manual* (English)

## What you must do

1. Load **`RULES AGENTES/deep_analise_pro.md`** at session start (minimum: **§24 cheat sheet**).
2. Apply its rules for coding, debugging, databases, security, testing, and verification.
3. **Improve before remove** (§3): do not delete working functions until a verified replacement exists.
4. **On contradictions, ask before implementing** (§4).
5. Treat older split docs in `RULES AGENTES/` as historical only (they redirect to the unified manual).

## Related paths

| Path | Role |
|------|------|
| [`RULES AGENTES/deep_analise_pro.md`](./RULES%20AGENTES/deep_analise_pro.md) | **Canonical full manual** |
| [`RULES AGENTES/AGENTS.md`](./RULES%20AGENTES/AGENTS.md) | Folder-local entrypoint |
| [`.agent/AGENTS.md`](./.agent/AGENTS.md) | Antigravity / IDE entrypoint → same manual |
| [`RULES AGENTES/gemini.md`](./RULES%20AGENTES/gemini.md) | Tool permissions & env isolation |
| [`RULES AGENTES/APP_VERSION.md`](./RULES%20AGENTES/APP_VERSION.md) | App version & data sources |
| [`RULES AGENTES/bd_minio.md`](./RULES%20AGENTES/bd_minio.md) | DB / MinIO sync guide |
| [`docs/README.md`](./docs/README.md) | Doc index (single source of truth table) |
| [`docs/DEPLOY_OVERVIEW.md`](./docs/DEPLOY_OVERVIEW.md) | Deploy overview (no secrets; versionable) |

## Superseded rule packs (inside `RULES AGENTES/`)

- `razonamiento_profundo.md`
- `razonamiento_profundo_PRO.md`
- `reglas.md`
- Previous long body of `.agent/AGENTS.md`
