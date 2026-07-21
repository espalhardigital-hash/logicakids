## Context

El hotfix de la Fase 4 para solucionar el comportamiento de la opción múltiple y el reinicio del contador de errores se ha completado y validado en la rama `desarrollo`. Ahora es necesario propagar estos cambios a la rama de producción (`main`), verificar el estado del repositorio remoto (GitHub) y actualizar los contenedores de desarrollo y producción.

Debido al bloqueo o inaccesibilidad SSH temporal con la VPS, el redespliegue de los contenedores remotos en producción/desarrollo no es factible de forma automática desde este agente (los túneles SSH fallan). Sin embargo, se actualizarán las ramas git correspondientes en GitHub y se re-desplegarán los contenedores locales para realizar las pruebas de lógica de la Fase 4.

## Goals / Non-Goals

**Goals:**
- Asegurar la integridad de las ramas `desarrollo` y `main` en GitHub.
- Re-desplegar los contenedores locales (Postgres, Redis, MinIO, Backend, Frontend) para pruebas.
- Validar mediante pruebas manuales en el entorno local que la Fase 4 sigue la lógica de la Fase 2 (el contador de errores inicia en 0 y aumenta en caso de fallo, limpiándose al reiniciar la sesión).
- Revisar y comprobar los logs del contenedor backend y frontend local para asegurar su correcto inicio y ejecución.

**Non-Goals:**
- Redespliegue físico en la VPS remota mediante comandos directos por la terminal del VPS (SSH está desconectado).

## Decisions

- **Decisión 1**: Realizar la actualización de los contenedores locales mediante docker-compose con reconstrucción (`--build`).
  - *Razón*: Asegura que los últimos cambios en `router.py` y `Fase4GameScreen.tsx` sean incorporados en las imágenes locales.
- **Decisión 2**: Subir los cambios a GitHub en ambas ramas (`desarrollo` y `main`).
  - *Razón*: Mantiene la sincronización de repositorios remotos para futuros despliegues manuales o cuando el VPS vuelva a estar en línea.

## Risks / Trade-offs

- **[Riesgo]** La VPS sigue desconectada tras el push en GitHub.
  - *Mitigación* -> Se documenta en el reporte final para que el usuario pueda hacer el despliegue posterior (ej. por Portainer web o pull manual en el servidor) cuando la conexión se estabilice.
