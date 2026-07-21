## 1. Backend: Implementación de Reset Completo en Responder (Fase 4)

- [x] 1.1 Modificar `responder_pregunta` en `LogicaMath/backend/app/fase4/router.py` para establecer `progreso.intentos_totales = 0` al gatillar la expulsión por salida temprana (`early_exit`).
- [x] 1.2 Incorporar en `responder_pregunta` las sentencias de eliminación (`delete`) para borrar los registros asociados en las tablas `intento` e `intento_pregunta` para esa sección.
- [x] 1.3 **[TEST & VERIFICACIÓN]** Ejecutar una auditoría estática de sintaxis y tipado en el archivo modificado `router.py` para asegurar que compila correctamente antes de avanzar.

## 2. Backend: Implementación de Reset Completo en Get Pregunta (Fase 4)

- [x] 2.1 Modificar `get_pregunta` en `LogicaMath/backend/app/fase4/router.py` para asegurar que al inicializarse o sembrarse el pool de preguntas de desafío de cero, se limpie `progreso.intentos_totales = 0`.
- [x] 2.2 **[TEST & VERIFICACIÓN]** Levantar temporalmente el servicio backend de forma local en la terminal y comprobar en los logs de arranque que no existan errores de importación o fallas en el router.

- [x] 3.1 Levantar el entorno Docker local de pruebas de forma limpia (`down -v` y `up --build`).
- [x] 3.2 Forzar en la base de datos local un progreso con 10 intentos y 0 aciertos para un desafío de la Fase 4.
- [x] 3.3 Validar de forma visual en el frontend que el contador de errores se muestre en `0/2` en la primera pregunta y se incremente de forma limpia sesión a sesión.
- [x] 3.4 Simular la expulsión por acumulación de errores y certificar que las tablas de intentos y el contador vuelvan a cero.
- [x] 3.5 **[TEST & VERIFICACIÓN]** Correr un test de humo de Playwright localmente para certificar que el flujo de respuestas y feedback del Tutor de la Fase 4 sigue funcionando sin regresiones.

## 4. Sincronización de Repositorios y Despliegue en VPS

- [x] 4.1 **Actualización de GitHub (Desarrollo):** Realizar commit y push de los cambios locales a la rama `desarrollo` en GitHub (`origin/desarrollo`).
- [x] 4.2 **Actualización de GitHub (Producción):** Cambiar a la rama `main`, fusionar (merge) `desarrollo` en `main` y subir los cambios a la rama `main` en GitHub (`origin/main`).
- [x] 4.3 **Actualización en VPS (Desarrollo):** Conectarse por SSH a la VPS (`35.222.6.7`), actualizar el repositorio en `/home/rominejo/logicakids` en la rama `desarrollo` y sincronizar los archivos hacia la carpeta del Stack 28 (Desarrollo).
- [x] 4.4 **Actualización en VPS (Producción):** Sincronizar el código actualizado de la rama `main` hacia la carpeta del Stack 29 (Producción) en la VPS.
- [x] 4.5 **Despliegue en VPS (Desarrollo):** Reconstruir y levantar los contenedores del Stack 28 utilizando docker compose en la VPS.
- [x] 4.6 **Despliegue en VPS (Producción):** Reconstruir y levantar los contenedores del Stack 29 utilizando docker compose en la VPS.
- [x] 4.7 **[TEST & VERIFICACIÓN]** Auditar en caliente los logs de ejecución del contenedor backend de desarrollo y del contenedor backend de producción en la VPS para certificar que ambos servicios arrancaron sin errores y se encuentran en estado saludable.
