## Why

El archivo `DEPLOY.md` actual está desfasado y no documenta adecuadamente la infraestructura local autónoma de pruebas y test unitarios basada en Docker Compose. Asimismo, se requiere definir y formalizar el flujo completo de sincronización de repositorios en GitHub, despliegue en VPS (stacks de desarrollo y producción) y la siembra específica manual de preguntas para las Fases 4, 5, 6, 7 y 8.

## What Changes

- **Actualización de DEPLOY.md:** Documentar con precisión la arquitectura de despliegue local (con Docker Compose local) y el flujo de integración/despliegue en la VPS.
- **Sincronización Git y GitHub:** Automatizar en el checklist de tareas la confirmación local, checkout y pushes a las ramas `desarrollo` y `main`.
- **Despliegue VPS (Desarrollo y Producción):** Describir y ejecutar la sincronización del código de los stacks 28 y 29 en la VPS mediante SSH.
- **Siembras (Seeding) de Preguntas en VPS:** Ejecutar los seeds específicos de las Fases 4 y 5 a 8 directamente en los backends de desarrollo y producción de la VPS.
- **Auditoría de Logs e Informe Final:** Auditar los logs de los contenedores en VPS y emitir un documento de análisis de logs e infraestructura final.

## Capabilities

### New Capabilities
- Ninguna.

### Modified Capabilities
- Ninguna.

## Impact

- **Documentación:** Modificación de `DEPLOY.md`.
- **Infraestructura VPS:** SSH en la VPS `35.222.6.7` y reinicio de contenedores Docker de desarrollo (`logicakids-desarollo`) y producción (`matematicas-producion`).
- **Base de Datos VPS:** Ejecución de scripts de siembra en las bases de datos de desarrollo y producción remotas.
