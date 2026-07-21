## ADDED Requirements

### Requirement: Sincronización e Integración de Código en Git
El flujo de despliegue SHALL requerir la sincronización del repositorio local hacia GitHub, asegurando la existencia de commits en las ramas `desarrollo` y `main` antes de realizar operaciones en la VPS.

#### Scenario: Sincronización exitosa de ramas
- **WHEN** los cambios están listos y validados localmente
- **THEN** el sistema (o el operador) SHALL ejecutar push a la rama `desarrollo` y luego integrar/mergear en la rama `main` de GitHub.

### Requirement: Actualización de Contenedores y Stacks en VPS
El flujo de despliegue en la VPS SHALL realizarse de forma secuencial, actualizando los archivos de cada stack (desarrollo: Stack 28, producción: Stack 29) y reconstruyendo los contenedores a través de `docker compose` con su respectivo namespace de proyecto (`-p`).

#### Scenario: Despliegue en VPS
- **WHEN** el código en GitHub está actualizado
- **THEN** el operador SHALL actualizar la carpeta base en la VPS mediante `git pull`, sincronizar las carpetas de los stacks y levantar los contenedores con `sudo docker compose -p <project_name> up -d --build`.

### Requirement: Siembra Manual (Seeding) de Preguntas
El operador del despliegue SHALL ejecutar los scripts de siembra de base de datos de las Fases 4 y 5 a 8 directamente en el contenedor del backend de FastAPI de la VPS.

#### Scenario: Ejecución de siembra en VPS
- **WHEN** los contenedores del backend en la VPS están levantados y saludables
- **THEN** el operador SHALL invocar el comando de siembra `python -m app.fase4.seed` y `python -m app.seed` (o los scripts correspondientes de fase) en los contenedores de desarrollo y producción de forma manual.
