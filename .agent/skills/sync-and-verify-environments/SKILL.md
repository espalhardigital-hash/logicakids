---
name: sync-and-verify-environments
description: Actualizar el repositorio GitHub, desplegar en Desarrollo y Producción del VPS, y analizar/sincronizar bases de datos y figuras de MinIO entre entornos.
---

# Habilidad: Sincronización y Verificación de Entornos

Esta habilidad provee una guía paso a paso y herramientas automatizadas para sincronizar el código del repositorio GitHub, redesplegar los entornos en la VPS, y validar la integridad y consistencia de los datos (Bases de Datos y figuras de MinIO) entre el entorno Local y los entornos de Desarrollo y Producción en la VPS.

---

## 1. Sincronización del Repositorio GitHub

> [!IMPORTANT]
> **Regla de Oro de Git:**
> - El agente **NUNCA** realizará operaciones que actualicen el repositorio de GitHub (como `git commit` o `git push`) sin que el usuario lo haya solicitado de manera expresa y explícita en la conversación.
> - Al actualizar el repositorio, opera **exclusivamente sobre la rama de desarrollo** (`desarrollo`), a menos que se indique lo contrario de forma explícita.

### Procedimiento de Actualización local y push:
1. Validar el estado local de Git:
   ```powershell
   git status
   ```
2. Crear un commit de manera segura (con confirmación del usuario):
   ```powershell
   git add .
   ```
3. Hacer push a la rama `desarrollo`:
   ```powershell
   git push origin desarrollo
   ```

---

## 2. Actualización de Desarrollo y Producción en la VPS (Despliegue)

> [!NOTE]
> **Flujo Git-First (Recomendado):**
> El despliegue de cambios en la VPS debe realizarse preferentemente actualizando el repositorio de GitHub y posteriormente redesplegando el stack desde la interfaz web de **Portainer**.

### Despliegue por Consola (Si es necesario y bajo aprobación explícita):
1. Conectarse a la VPS:
   ```powershell
   ssh rominejo@35.222.6.7
   ```
2. Para **Desarrollo** (Stack `logicakids-desarollo`):
   ```bash
   cd /var/lib/docker/volumes/portainer_portainer_data/_data/compose/27/LogicaMath
   sudo docker compose -p logicakids_desarrollo pull
   sudo docker compose -p logicakids_desarrollo up -d --build
   ```
3. Para **Producción** (Stack `matematicas-producion`):
   ```bash
   cd /var/lib/docker/volumes/portainer_portainer_data/_data/compose/23
   sudo docker compose -p matematicas-producion pull
   sudo docker compose -p matematicas-producion up -d --build
   ```

---

## 3. Análisis de Base de Datos (Consistencia de Preguntas)

Dado que las bases de datos de desarrollo y producción no están expuestas públicamente, es necesario establecer túneles SSH locales para conectarse.

### Paso 1: Abrir Túneles SSH en la terminal local
Abre dos terminales de PowerShell independientes en tu máquina local y ejecuta:

- **Túnel para Desarrollo (Puerto local 5434):**
  ```powershell
  ssh -L 5434:localhost:5432 rominejo@35.222.6.7 -N
  ```
- **Túnel para Producción (Puerto local 5435):**
  ```powershell
  ssh -L 5435:localhost:5432 rominejo@35.222.6.7 -N
  ```

### Paso 2: Ejecutar el Análisis Comparativo
Con los túneles SSH activos y el contenedor Docker local de Postgres corriendo (puerto `5433`), ejecuta el script de comparación:

```powershell
python LogicaMath/backend/scripts/compare_environments.py --local-db-port 5433 --dev-db-port 5434 --prod-db-port 5435
```

El script analizará si las preguntas (tabla `preguntas`) y las alternativas (tabla `alternativas`) de desarrollo y producción coinciden con las locales.

---

## 4. Análisis y Sincronización de Figuras de MinIO

Los endpoints públicos de MinIO en la VPS están expuestos y no requieren túneles SSH para la comparación de imágenes.

### Paso 1: Ejecutar la comparación de MinIO
Ejecuta el script con el flag `--skip-db` si solo deseas analizar las figuras en MinIO:

```powershell
python LogicaMath/backend/scripts/compare_environments.py --skip-db
```

### Paso 2: Sincronizar figuras faltantes
Si el análisis arroja que faltan figuras locales en desarrollo o producción, utiliza el script de sincronización provisto:

- **Sincronizar hacia Desarrollo:**
  ```powershell
  python LogicaMath/backend/scripts/sync_minio_vps.py --env dev
  ```
- **Sincronizar hacia Producción:**
  ```powershell
  python LogicaMath/backend/scripts/sync_minio_vps.py --env prod
  ```
