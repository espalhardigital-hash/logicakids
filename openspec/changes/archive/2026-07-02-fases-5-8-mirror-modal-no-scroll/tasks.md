## 1. Fase 5: Ajuste de Modal y Estilos

- [x] 1.1 Modificar `LogicaMath/frontend/components/fase5/Fase5MirrorModal.tsx` para eliminar la visualización del enunciado largo de la pregunta anterior fallida (`lastQuestionEnunciado`).
- [x] 1.2 Rediseñar la sección de repaso de la Fase 5 como una franja flex horizontal minimalista que ocupe el mínimo espacio de pantalla.
- [x] 1.3 Ajustar `Fase5Styles.css` para bloquear la aparición de scroll mediante `overflow: hidden !important` y limitar la altura a `max-height: 96vh` en las clases `.f5-feedback-overlay` y `.f5-mirror-modal-card`.

## 2. Fase 6: Ajuste de Modal y Estilos

- [x] 2.1 Modificar `LogicaMath/frontend/components/fase6/Fase6MirrorModal.tsx` para eliminar la visualización del enunciado largo de la pregunta anterior fallida.
- [x] 2.2 Rediseñar la sección de repaso de la Fase 6 como una franja flex horizontal minimalista que ocupe el mínimo espacio de pantalla.
- [x] 2.3 Ajustar `Fase6Styles.css` para bloquear la aparición de scroll mediante `overflow: hidden !important` y limitar la altura a `max-height: 96vh` en las clases `.f6-feedback-overlay` and `.f6-mirror-modal-card`.

## 3. Fase 7: Ajuste de Modal y Estilos

- [x] 3.1 Modificar `LogicaMath/frontend/components/fase7/Fase7MirrorModal.tsx` para eliminar la visualización del enunciado largo de la pregunta anterior fallida.
- [x] 3.2 Rediseñar la sección de repaso de la Fase 7 como una franja flex horizontal minimalista que ocupe el mínimo espacio de pantalla.
- [x] 3.3 Ajustar `Fase7Styles.css` para bloquear la aparición de scroll mediante `overflow: hidden !important` y limitar la altura a `max-height: 96vh` en las clases `.f7-feedback-overlay` and `.f7-mirror-modal-card`.

## 4. Fase 8 y 9: Ajuste de Modal y Estilos

- [x] 4.1 Modificar `LogicaMath/frontend/components/fase8/Fase8MirrorModal.tsx` y `LogicaMath/frontend/components/fase9/Fase9MirrorModal.tsx` para eliminar la visualización del enunciado largo de la pregunta anterior fallida.
- [x] 4.2 Rediseñar la sección de repaso de las Fases 8 y 9 como una franja flex horizontal minimalista que ocupe el mínimo espacio de pantalla.
- [x] 4.3 Ajustar `Fase8Styles.css` y `Fase9Styles.css` para bloquear la aparición de scroll mediante `overflow: hidden !important` y limitar la altura a `max-height: 96vh` en las clases `.f8-feedback-overlay` and `.f8-mirror-modal-card`.

## 5. Verificación y Pruebas locales

- [x] 5.1 Levantar el entorno de desarrollo local con Docker Compose de cero (limpiando volúmenes de datos antiguos con `down -v` y compilando con `SEED_DB=true`).
- [x] 5.2 Comprobar y verificar la persistencia de las preguntas con la concordancia de género corregida en la base de datos local.
- [x] 5.3 Ejecutar la suite de pruebas unitarias y visuales de Playwright en local (`npx playwright test`) y verificar el paso exitoso de los tests de las Fases 2, 7, 8 y 9.
- [x] 5.4 Comprobar de forma manual el correcto comportamiento sin scroll de las ventanas de segunda oportunidad (espejo) al cometer errores en las Fases 5, 6, 7 y 8.
- [x] 5.5 Realizar un re-deploy local de estabilidad tras pruebas positivas.

## 6. Sincronización en GitHub y Despliegue en VPS

- [x] 6.1 Hacer commit de todos los cambios de las Fases 4 a 9 en la rama local `desarrollo` y subir a `origin/desarrollo` en GitHub.
- [x] 6.2 Hacer checkout a la rama `main` (producción), fusionar `desarrollo` en `main` y subir a `origin/main` en GitHub.
- [x] 6.3 Conectarse vía SSH a la VPS (`35.222.6.7`) y en la carpeta base `/home/rominejo/logicakids` actualizar el repositorio en la rama `desarrollo`.
- [x] 6.4 Sincronizar y actualizar los archivos del stack de desarrollo (Stack 28) en la VPS y reconstruir/reiniciar contenedores.
- [x] 6.5 Sincronizar y actualizar los archivos del stack de producción (Stack 29) en la VPS y reconstruir/reiniciar contenedores.
- [x] 6.6 Ejecutar de forma manual el seed de la Fase 4 en el contenedor de backend de desarrollo del VPS (`sudo docker exec logicakids-desarollo-backend-1 python -m app.fase4.seed`).
- [x] 6.7 Ejecutar de forma manual el seed de la Fase 4 en el contenedor de backend de producción del VPS (`sudo docker exec matematicas-producion-backend-1 python -m app.fase4.seed`).
- [x] 6.8 Auditar logs de ambos contenedores backend en la VPS para certificar que el despliegue es estable y libre de errores.
