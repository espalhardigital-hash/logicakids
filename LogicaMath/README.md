# LogicaKids Pro (Plataforma Educativa Pedro II)

Una plataforma educativa premium basada en el aprendizaje de dominio (mastery-based learning) para dominar las matemáticas de manera gamificada, intuitiva y profesional.

## 🎯 Objetivo y Enfoque Pedagógico

LogicaKids Pro no es solo un juego de cálculo; es un **sistema de tutoría invisible**. A través de un backend pedagógico (fases, preguntas, alternativas, intentos, progreso/maestría, pools, simulados, configuración admin, etc.), la plataforma es capaz de:

- Analizar no solo *si* la respuesta es correcta, sino *por qué* el alumno falló (diagnóstico por tipo de error).
- Entregar retroalimentación específica (feedback guiado y explicaciones paso a paso).
- Desbloquear progresivamente nuevos retos lógicos y operaciones matemáticas según la maestría alcanzada.

## 💎 Diseño Visual

La plataforma cuenta con un diseño de alta gama **Premium Glassmorphism**:

- Fondos oscuros con gradientes sutiles y elementos traslúcidos (`backdrop-blur-xl`).
- Micro-animaciones fluidas utilizando **Framer Motion**.
- Estilizado de alto rendimiento gracias a **Tailwind CSS v4**.

## 🚀 Stack Tecnológico

- **Frontend**: React + TypeScript + Vite + Tailwind CSS v4 + Framer Motion + Lucide React.
- **Backend**: FastAPI (Python) + SQLAlchemy Async + API Router-based.
- **Base de Datos**: PostgreSQL 15 (modelo pedagógico multi-tabla + JWT).
- **Almacenamiento**: S3-Compatible (**MinIO**) — avatares de perfil **y** figuras de preguntas bajo el prefijo `graphics/` (Fases 5–6 usan SVG inline en el enunciado; ver skill de sync).
- **Contenedores**: Docker + Portainer + Traefik.

## 📦 Estructura del monorepo

El código de la app vive en **`LogicaMath/`** (este directorio). En la **raíz del repositorio** están la infra, reglas de agentes y guías operativas:

| Ruta (desde la raíz del repo) | Rol |
|---|---|
| `LogicaMath/` | Backend + frontend de la aplicación |
| `DEPLOY.md` | Despliegue VPS / Portainer / variables de entorno |
| `RULES AGENTES/bd_minio.md` | Sync seguro de preguntas + MinIO (local → VPS) |
| `RULES AGENTES/APP_VERSION.md` | Versión de app y fuentes de datos |
| `RULES AGENTES/deep_analise_pro.md` | Manual canónico de agentes |
| `docs/README.md` | Índice de fuentes de verdad |
| `docs/DEPLOY_OVERVIEW.md` | Deploy sin secretos (versionable en Git) |
| `docs/historico/` | Procedimientos one-shot archivados |

### Repositorio GitHub

- **Remoto actual del workspace:** `https://github.com/espalhardigital-hash/logicakids.git`
- **Rama de producción en uso:** `producion` (también es `origin/HEAD`)
- **Rama de desarrollo:** `desarrollo` (**congelada** — todo va a `producion`)
- Carpeta local del monorepo: `APP_Logica_Matematicas_kids` (el clone en servidor suele llamarse `logicakids`).

> Si el remoto se mueve o se sustituye por otro repositorio, actualiza `git remote`, este README, `DEPLOY.md` y `RULES AGENTES/APP_VERSION.md` en el mismo cambio.

## 🛠️ Instalación y Despliegue

La infraestructura está dockerizada y diseñada para su despliegue en servidores VPS.

👉 **[Guía completa de despliegue (`DEPLOY.md` en la raíz del repo)](../DEPLOY.md)**

> El enlace anterior apunta a **`../DEPLOY.md`** (raíz del monorepo). **No** existe `LogicaMath/DEPLOY.md`.

### Inicio rápido (Docker Compose)

1. Configura tu entorno (desde el directorio de compose que uses: local, desarrollo o producción):

   ```bash
   cp .env.example .env
   # Edita .env con tus credenciales de PostgreSQL, JWT y almacenamiento S3/MinIO.
   ```

2. Levanta los contenedores:

   ```bash
   docker compose up -d --build
   ```

*Nota: la inicialización de esquema es **automática**. El backend crea tablas al iniciar si no existen. El **banco de preguntas** y las figuras se gestionan con seeds y/o la skill de sincronización (no con dumps SQL monolíticos legacy).*

### Sincronizar preguntas a la VPS (desarrollo / producción)

Para subir o alinear el banco de preguntas **sin tocar** usuarios, alumnos ni puntajes:

👉 **[Skill canónica: `RULES AGENTES/bd_minio.md`](../RULES%20AGENTES/bd_minio.md)**

El procedimiento one-shot de julio 2026 (`final_migration.sql` vía Portainer) está **archivado** en:

- Stub: [`../INSTRUCCIONES_MIGRACION_VPS.md`](../INSTRUCCIONES_MIGRACION_VPS.md)
- Histórico: [`../docs/historico/INSTRUCCIONES_MIGRACION_VPS_2026-07.md`](../docs/historico/INSTRUCCIONES_MIGRACION_VPS_2026-07.md)

**No lo uses** para operaciones nuevas.

## 👑 Panel de Administración

La plataforma incluye un panel de control exclusivo para usuarios con rol `ADMIN` (mismo diseño Glassmorphism), orientado a:

- **Gestión de usuarios**: perfiles, avatares y contraseñas.
- **Analíticas**: progresos, tasas de acierto y estadísticas.
- **Control pedagógico**: bancos de preguntas, configuración de avance por bloque, feedback UX y herramientas SRE del admin.

## 🧪 Testing

Validación de conexión y flujos críticos del backend:

```bash
docker compose exec backend python tests/test_db_connection.py
```

Suite frontend / E2E (cuando el stack local esté arriba): ver scripts en `frontend/` (Vitest, Playwright).

## 📌 Control de versiones y origen de datos

Descripción de nombre de app, versiones (Backend `3.0.0` / Frontend según `package.json`) y de dónde se leen datos e imágenes (PostgreSQL, MinIO/S3, metadatos locales):

👉 **[Guía de versión y fuentes de datos (`APP_VERSION.md`)](../RULES%20AGENTES/APP_VERSION.md)**
