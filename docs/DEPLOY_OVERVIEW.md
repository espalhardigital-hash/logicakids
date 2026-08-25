# Overview de despliegue (sin secretos)

Documento **versionable**. El runbook con hosts, IPs y stacks concretos vive en **`DEPLOY.md`** en la raíz del monorepo (gitignored).

## Arquitectura

```text
PostgreSQL  ←  Backend (FastAPI)  ←  Frontend (React/Vite)
MinIO/S3    ←
         Traefik (TLS / rutas)
```

- **Código de la app:** `LogicaMath/` (backend + frontend).
- **Compose / env por entorno:** carpetas `Datos_localhost`, `Datos_Desarrollo`, `Datos_Producion` (gitignored).
- **Proxy:** Traefik en redes Docker compartidas (`traefik_proxy`, `internal_services` — nombres según tu VPS).

## Repositorio y ramas

| Concepto | Valor actual del workspace |
|----------|----------------------------|
| Remoto | `https://github.com/espalhardigital-hash/logicakids.git` |
| Rama activa / estable | rama **`producion`** (`origin/HEAD`) |
| Rama `desarrollo` | **Congelada** — no recibe commits; todo va a `producion` |
| ⚠️ | No uses `main` salvo que el remoto lo reintroduzca |

**Nota:** `desarrollo` está congelada y va detrás de `producion`. No asumir paridad. Si algún día se reactiva, primero sincronizar:

```bash
git fetch origin
git log --oneline origin/desarrollo..origin/producion
git log --oneline origin/producion..origin/desarrollo
```

## Flujo Git → VPS (resumen)

1. Probar en local.
2. Commit + push a la rama adecuada (`desarrollo` o `producion`) — **solo si el usuario lo pide** (agentes).
3. En la VPS: `git pull` del clone del monorepo.
4. Copiar/sincronizar el árbol de compose al stack de Portainer (rsync o UI).
5. Reconstruir con nombre de proyecto explícito:

```bash
sudo docker compose -p <nombre_proyecto> up -d --build backend frontend
```

Evita proyectos Docker duplicados por el nombre de carpeta.

## Operación local vigente

La verificación de Fases 5 y 6 se realiza exclusivamente con el compose local:

```powershell
docker compose -f D:\Antigravity\APP_Logica_Matematicas_kids\Datos_localhost\docker-compose.local.yml up -d --build
```

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- PostgreSQL: `localhost:5433`

Después de modificar un seeder, reconstruir el backend y resembrar solo la fase afectada. El procedimiento y las cautelas para Fases 5 y 6 están en [`ESTADO_IMPLEMENTACION_FASES_5_6.md`](./ESTADO_IMPLEMENTACION_FASES_5_6.md).

## Variables de entorno (nombres, no valores)

| Variable | Uso |
|----------|-----|
| `DATABASE_URL` | PostgreSQL (`postgresql+asyncpg://…`) |
| `SECRET_KEY` | JWT |
| `S3_*` / MinIO | Access, secret, bucket, endpoint / public URL |
| `VITE_API_URL` | URL pública del API (build del frontend) |
| `ALLOWED_ORIGINS` | CORS |
| `NOMBRE_APP` / `DOMINIO` | Traefik / identidad del stack |

Valores reales: solo en `.env` de cada entorno (nunca en Git).

## Datos vs código

| Objetivo | Guía |
|----------|------|
| Desplegar **código** | Este overview + `DEPLOY.md` local |
| Sincronizar **preguntas / figuras** | [`RULES AGENTES/bd_minio.md`](../RULES%20AGENTES/bd_minio.md) |
| Migración SQL one-shot 2026-07 | Archivada en `docs/historico/` — **no usar** |

## Túneles DB (convención de puertos)

Confirmables con el operador; no son secretos:

| Puerto host | Uso típico |
|-------------|------------|
| 5433 | Postgres local |
| 5434 | Túnel → DB desarrollo VPS |
| 5435 | Túnel → DB producción VPS |

```bash
ssh -L <PUERTO_LOCAL>:localhost:<PUERTO_DB_REMOTO> <USER>@<VPS_HOST> -N
```

## Checklist pre-producción

- [ ] Cambios probados en local / dev
- [ ] Rama correcta (`producion` para estable)
- [ ] Secretos solo en env/Portainer
- [ ] Sync de preguntas con pre-vuelo (`--dry-run`) si hay cambios de banco
- [ ] No borrar users / progreso / avatares
- [ ] `docker compose -p <proyecto>` explícito en VPS
