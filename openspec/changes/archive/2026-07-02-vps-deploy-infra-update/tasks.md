## 1. Documentación: Actualización de DEPLOY.md

- [x] 1.1 Modificar `DEPLOY.md` para actualizar la descripción del entorno local de Docker, redes, variables de entorno y el flujo de despliegue real en la VPS.
- [x] 1.2 Incorporar en `DEPLOY.md` la documentación sobre Smart Seeding y Force Seeding para todas las Fases.

## 2. GitHub: Integración y Pushes

- [x] 2.1 Commitear todos los cambios locales pendientes de las Fases 4 a 9 en la rama local `desarrollo`.
- [x] 2.2 Subir la rama local `desarrollo` a `origin/desarrollo` en GitHub.
- [x] 2.3 Cambiar a la rama de producción `main`, fusionar (merge) `desarrollo` en `main` y subir a `origin/main` en GitHub.
- [x] 2.4 Regresar a la rama local `desarrollo`.

## 3. VPS: Despliegue en Desarrollo (Stack 28)

- [x] 3.1 Conectarse vía SSH a la VPS (`35.222.6.7`) y en `/home/rominejo/logicakids` hacer `git pull origin desarrollo`.
- [x] 3.2 Sincronizar el código actualizado con la carpeta del stack de desarrollo de Portainer: `/var/lib/docker/volumes/portainer_portainer_data/_data/compose/28/`
- [x] 3.3 Recompilar y levantar los contenedores de desarrollo en la VPS (`sudo docker compose -p logicakids-desarollo up -d --build backend frontend`).

## 4. VPS: Despliegue en Producción (Stack 29)

- [x] 4.1 En `/home/rominejo/logicakids` en la VPS cambiar a la rama `main` y hacer `git pull origin main`.
- [x] 4.2 Sincronizar el código actualizado con la carpeta del stack de producción de Portainer: `/var/lib/docker/volumes/portainer_portainer_data/_data/compose/29/`
- [x] 4.3 Recompilar y levantar los contenedores de producción en la VPS (`sudo docker compose -p matematicas-producion up -d --build backend frontend`).
- [x] 4.4 En la VPS regresar a la rama `desarrollo` en `/home/rominejo/logicakids`.

## 5. VPS: Ejecución de Siembras (Seeds) Manuales

- [x] 5.1 Correr el seed de la Fase 4 en el contenedor backend de desarrollo del VPS (`sudo docker exec logicakids-desarollo-backend-1 python -m app.fase4.seed`).
- [x] 5.2 Correr el seed de la Fase 4 en el contenedor backend de producción del VPS (`sudo docker exec matematicas-producion-backend-1 python -m app.fase4.seed`).
- [x] 5.3 Correr los seeds de las Fases 5 a 8 en el contenedor backend de desarrollo del VPS utilizando comandos inline de python para importar y ejecutar `run_faseX_seed()`.
- [x] 5.4 Correr los seeds de las Fases 5 a 8 en el contenedor backend de producción del VPS utilizando comandos inline de python para importar y ejecutar `run_faseX_seed()`.

## 6. Auditoría y Cierre

- [x] 6.1 Leer logs en caliente de desarrollo y producción para certificar el arranque sin errores.
- [x] 6.2 Emitir y redactar el documento final de análisis de cambios implementados y logs en la VPS.
