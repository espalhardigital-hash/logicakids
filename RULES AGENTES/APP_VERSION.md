# Información de Versión y Fuentes de Datos — LogicaKids Pro

Control de versiones, nombres de la aplicación y **de dónde** salen los datos que ven las interfaces.  
Documento genérico: **sin rutas absolutas de un PC** y **sin secretos**.

## 1. Identificación de la aplicación

### Nombre

| Capa | Dónde | Valor típico / variable |
|------|--------|-------------------------|
| Desarrollo VPS | `Datos_Desarrollo/.env` → `NOMBRE_APP` | p.ej. `pruebas` |
| Producción VPS | `Datos_Producion/.env` → `NOMBRE_APP` | p.ej. `matematicas_Kids` |
| Frontend | `LogicaMath/frontend/package.json` → `"name"` | `logicakids-pro` |
| Backend | `LogicaMath/backend/app/main.py` → `FastAPI(title=…)` | `LogicaKids Pro API` |

### Versión

| Componente | Dónde se define | Notas |
|------------|-----------------|--------|
| Backend / API | `FastAPI(…, version=…)` en `main.py` | Suite documentada como `3.0.0` (verificar en código) |
| Frontend | `LogicaMath/frontend/package.json` → `"version"` | Puede diferir del marketing de la suite |

---

## 2. Orígenes de datos para interfaces

### A. PostgreSQL

- Progreso / maestría: `configuracion_progreso`, `progreso_maestria`, pools, etc.
- Banco de preguntas: tablas `preguntas` + `alternativas` (vía API).
- Intentos / historial: `intentos`, `intento_preguntas`, …
- Auth / perfiles: `users`, `alumnos` (**no** se sincronizan con la skill de preguntas).

Nombres exactos de tablas: ver modelos en `LogicaMath/backend/app/models/` y skill [`bd_minio.md`](./bd_minio.md).

### B. MinIO / S3

| Prefijo / uso | ¿Qué es? | Sync con `bd_minio`? |
|---------------|----------|----------------------|
| `graphics/<uuid>.<ext>` | Figuras de preguntas | **Sí** (único ámbito de la skill) |
| objetos en la **raíz** del bucket | Avatares / perfil | **Nunca** |
| `screenshots/` | UX feedback | **Nunca** |

- URL pública y bucket: variables `S3_PUBLIC_URL` / `S3_BUCKET_NAME` (por entorno).
- Backend: `LogicaMath/backend/app/core/storage.py`
- Frontend avatares: `LogicaMath/frontend/services/storageService.ts`

**Fases 5 y 6:** figuras en **SVG inline** dentro de `enunciado` → no dependen de `graphics/` (ver `bd_minio.md` §1.3).

### C. Metadatos estáticos del frontend

- `LogicaMath/frontend/components/fase_generic/faseMetadata.ts` (teoría / muestras UI).
- No sustituye el banco en PostgreSQL para el juego real.

### D. API URL y Traefik

| Variable | Rol |
|----------|-----|
| `VITE_API_URL` | Base del API en el build del frontend |
| `DOMINIO` / `NOMBRE_APP` | Enrutado Traefik + certificados |

Valores por entorno solo en `.env` (gitignored).

---

## 3. Repositorio y ramas

| Campo | Valor (workspace) |
|-------|-------------------|
| Remoto | `https://github.com/espalhardigital-hash/logicakids.git` |
| Desarrollo | rama `desarrollo` |
| Producción | rama **`producion`** (`origin/HEAD`) — no `main` |
| App | `LogicaMath/` |
| Sync de preguntas | [`bd_minio.md`](./bd_minio.md) |
| Deploy overview (Git) | [`docs/DEPLOY_OVERVIEW.md`](../docs/DEPLOY_OVERVIEW.md) |
| Deploy detalle (local) | `DEPLOY.md` en la raíz (gitignored) |
| Histórico migración SQL | `docs/historico/` — no usar |

### Exclusiones relevantes (`.gitignore`)

- `Datos_Desarrollo/`, `Datos_Producion/`, `Datos_localhost/`
- `.env*`
- `DEPLOY.md`, `INSTRUCCIONES_MIGRACION_VPS.md`, `docs/historico/INSTRUCCIONES_MIGRACION_VPS*.md`
- `openspec/`, `.agent/`, `*.sql`, `Pedro II/`

---

## 4. Índice general de docs

Ver [`docs/README.md`](../docs/README.md).
