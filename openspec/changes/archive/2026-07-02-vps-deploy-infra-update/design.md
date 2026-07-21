## Context

La documentación actual de despliegue en `DEPLOY.md` no refleja la arquitectura de pruebas local ni describe el flujo real de sincronización por GitHub de los dos entornos virtuales (Desarrollo: Stack 28, y Producción: Stack 29) de Portainer en la VPS. Asimismo, se detectaron problemas de textos o scroll en las Fases 4 y 5 a 8, los cuales requieren forzar la re-siembra de preguntas tanto localmente como en la VPS.

## Goals / Non-Goals

**Goals:**
- Actualizar `DEPLOY.md` con detalles de la arquitectura, configuración local y despliegue real.
- Definir paso a paso la integración de ramas local (`desarrollo` a `main`) y subida a GitHub.
- Detallar la secuencia de SSH, sincronización de Portainer y reconstrucción en la VPS.
- Detallar la ejecución manual de seeds en el backend para actualizar las bases de datos de desarrollo y producción remotas.

**Non-Goals:**
- No se creará nueva infraestructura de base de datos ni nuevos servicios Docker.

## Decisions

### 1. Actualización Exhaustiva de DEPLOY.md
- **Decisión:** Sobrescribir `DEPLOY.md` para incorporar diagramas de arquitectura local vs remota, variables del archivo `.env.local`, redes internas, y la sección de Smart Seeding & Force Seeding.
- **Razonamiento:** Mantiene el manual actualizado para futuros desarrollos y auditorías.

### 2. Sincronización Git en GitHub
- **Decisión:** Fusiones limpias y no-fast-forward de `desarrollo` a `main` antes del despliegue en la VPS para garantizar trazabilidad.
- **Razonamiento:** Coherente con las directrices de `GEMINI.md`.

### 3. Sincronización en VPS y Recompilación
- **Decisión:** Conectarse mediante SSH (`rominejo@35.222.6.7`), hacer pull en la carpeta base y sincronizar los archivos utilizando `rsync` hacia `/var/lib/docker/volumes/portainer_portainer_data/_data/compose/28/` (desarrollo) y `29/` (producción), y recompilar con:
  - Desarrollo: `sudo docker compose -p logicakids-desarollo up -d --build backend frontend`
  - Producción: `sudo docker compose -p matematicas-producion up -d --build backend frontend`
- **Razonamiento:** Portainer almacena los archivos en esas rutas de volumen. Esta sincronización directa actualiza el código del stack de forma rápida y limpia.

###  decision 4. Seeding Directo en Contenedores VPS
- **Decisión:** Para aplicar las semillas de preguntas actualizadas (como la concordancia gramatical en la Fase 4 y las correcciones de scroll en las Fases 5 a 8):
  - Desarrollo:
    ```bash
    sudo docker exec logicakids-desarollo-backend-1 python -m app.fase4.seed
    sudo docker exec logicakids-desarollo-backend-1 python -c "import asyncio; from app.fase5.seed import run_fase5_seed; asyncio.run(run_fase5_seed())"
    sudo docker exec logicakids-desarollo-backend-1 python -c "import asyncio; from app.fase6.seed import run_fase6_seed; asyncio.run(run_fase6_seed())"
    sudo docker exec logicakids-desarollo-backend-1 python -c "import asyncio; from app.fase7.seed import run_fase7_seed; asyncio.run(run_fase7_seed())"
    sudo docker exec logicakids-desarollo-backend-1 python -c "import asyncio; from app.fase8.seed import run_fase8_seed; asyncio.run(run_fase8_seed())"
    ```
  - Producción:
    ```bash
    sudo docker exec matematicas-producion-backend-1 python -m app.fase4.seed
    sudo docker exec matematicas-producion-backend-1 python -c "import asyncio; from app.fase5.seed import run_fase5_seed; asyncio.run(run_fase5_seed())"
    sudo docker exec matematicas-producion-backend-1 python -c "import asyncio; from app.fase6.seed import run_fase6_seed; asyncio.run(run_fase6_seed())"
    sudo docker exec matematicas-producion-backend-1 python -c "import asyncio; from app.fase7.seed import run_fase7_seed; asyncio.run(run_fase7_seed())"
    sudo docker exec matematicas-producion-backend-1 python -c "import asyncio; from app.fase8.seed import run_fase8_seed; asyncio.run(run_fase8_seed())"
    ```
- **Razonamiento:** Ejecutar directamente los scripts de seeding o importar la función `run_faseX_seed()` y ejecutarla por comando inline de python evita tener que reiniciar los contenedores con variables de entorno de forzado, lo cual es mucho más seguro en caliente.

## Risks / Trade-offs

- **[Risk] Interrupción temporal de producción durante la recompilación:** La compilación de Docker puede tomar ~1-2 minutos.
  - **Mitigación:** Se realizará primero el despliegue en Desarrollo para certificar estabilidad antes de proceder a Producción.
