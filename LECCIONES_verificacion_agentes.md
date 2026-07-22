# Lecciones de Verificación para Agentes — Caso Fase 5 (imágenes con cotas)

> Leer ANTES de tocar código de generación de imágenes/gráficos en este repo (`graphics_generator.py`, `svg_helpers.py`, y en general cualquier fix visual). Documenta un incidente real (2026-07-21) donde una sesión de LLM implementó un fix que parecía correcto en el código pero no lo era en la práctica, porque nunca se verificó el resultado.

## Qué pasó

Un evaluador reportó (vía Buzón de Mejorías UX) que las imágenes de preguntas de Fase 5 tenían: etiquetas de medida superpuestas dentro de la figura, texto ilegible/distorsionado, cuadrícula tapada por el relleno, y espacio en blanco excesivo. Una sesión de LLM anterior implementó un fix (agregar `labels=` a `generate_grid_shape_image`), subió la versión de seed, y dio el trabajo por terminado. **El fix no funcionaba** — el bug reportado seguía intacto, y además había un segundo bug (glifo de texto recortado) que ni siquiera se había detectado.

## La causa raíz del fallo: no fue de conocimiento, fue de proceso

El código escrito por la sesión anterior era razonable a primera vista. El problema es que **nadie generó la imagen resultante y la miró** antes de declarar el trabajo hecho. Cinco fallas concretas:

1. **No regeneró ni miró la imagen resultante.** Se agregó `labels=` a `generate_grid_shape_image` y se dio por terminado sin generar un PNG de prueba ni abrirlo. Por eso no se detectó que las cotas caían **dentro** de la figura en vez de afuera.
2. **No verificó la geometría del fix.** Se agregó la llamada a `_draw_dimension_line` asumiendo que "pasarle los vértices" bastaba, sin comprobar matemáticamente hacia qué lado apunta el vector normal para cada borde del polígono.
3. **No buscó el mismo patrón en funciones hermanas.** `generate_clean_shape_image` y `generate_rectilinear_shape_image` comparten `_draw_dimension_line`. El bug de glifo recortado (dígitos como "3" y "8" se veían distorsionados/como espejados) era transversal a las tres funciones — se habría encontrado con una sola prueba de renderizado, sin necesidad de leer código nuevo.
4. **No re-sembró para cerrar el ciclo.** Se subió la versión de `SEED_VERSIONS["fase_5"]` en el código, pero nunca se ejecutó el re-seed ni se consultó la base de datos/MinIO para confirmar que el cambio realmente llegó a un dato consultable por la app.
5. **No cerró el reporte que motivó el trabajo.** No se actualizó el estado en la tabla `ux_feedbacks` ni se refrescó el export (`ux_correcciones_pendientes.json`) — quedó "implementado en el código" pero sin ninguna evidencia de que el problema reportado se hubiera resuelto.

## Regla general (aplica a cualquier fix visual/generativo, no solo a Fase 5)

**Escribir el código que parece correcto no es lo mismo que confirmar que el bug está resuelto.** Un fix sobre una función que genera una imagen, un PDF, un SVG, o cualquier artefacto renderizado **no está terminado hasta que ese artefacto se genera de verdad y se inspecciona** — no basta con que el código compile o que la lógica "se vea bien" leyendo el diff.

## Checklist de "Definition of Done" — no declarar terminado un fix visual sin:

- [ ] **(a) Generar el artefacto real.** Ejecutar la función/endpoint que produce el resultado final (imagen, PDF, render), no solo revisar el código que la generó.
- [ ] **(b) Verlo, no asumirlo.** Abrir el archivo generado con una herramienta de lectura de imágenes (o el navegador si es UI). Si el detalle es fino (texto pequeño, alineación), hacer zoom/crop antes de concluir que "se ve bien".
- [ ] **(c) Probar casos límite.** No verificar un solo valor — probar el rango real de parámetros que usa la app en producción (mínimo, máximo, y al menos un caso intermedio distinto al de la prueba inicial).
- [ ] **(d) Cerrar el ciclo con el dato real.** Si el fix depende de un re-seed, una migración, o un caché, ejecutar ese paso y consultar la base de datos/storage directamente para confirmar que el dato que la app va a servir es el corregido — no el de antes del fix.
- [ ] **(e) Buscar el mismo patrón en el resto del código.** Si el bug vive en una función compartida por varios llamadores, grep de esos llamadores y confirmar (con el mismo método de los puntos a-c) que el fix los corrige a todos, no solo al que motivó el reporte.
- [ ] **(f) Cerrar el reporte que originó el trabajo.** Si hay un sistema de tickets/feedback (como `ux_feedbacks` en este repo), actualizar su estado y dejar una nota técnica de qué se cambió — sin esto, no hay forma de auditar después si el fix realmente respondió al reporte original.

## Cómo se verificó el fix real (referencia de método, no repetir literalmente)

Cuando se re-hizo el trabajo correctamente, el método fue: generar el PNG directamente desde Python dentro del contenedor backend (`docker exec ... python -c "from app.utils.graphics_generator import ...; ...; open(...).write(img_bytes)"`), copiarlo al host con `docker cp`, y leerlo con la herramienta de lectura de imágenes. Cuando el texto se veía sospechoso a tamaño normal, se hizo un crop + upscale con `Image.NEAREST` (sin interpolación, para no confundir un artefacto de resize con un bug real) antes de concluir nada. Esto fue lo que permitió encontrar el bug real de recorte de glifo, que un vistazo superficial a la imagen completa no habría revelado con certeza.
