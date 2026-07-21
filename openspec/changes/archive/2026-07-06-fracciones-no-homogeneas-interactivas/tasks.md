## 1. Tipos y Modelo de Datos (Frontend)

- [x] 1.1 Extender la interfaz `Fase4Pregunta` en `Fase4Types.ts` para incluir los nuevos campos de `datos_numericos`: `sectors` (array de `{id, weight, points, label}`), `target_value` (number), `target_fraction_text` (string) y `viewBox` (string)
- [x] 1.2 Crear la interfaz `NonHomogeneousSector` con los campos `id: number`, `weight: number`, `points: string`, `label?: string`

### ✅ Verificación del Grupo 1
- [x] 1.V1 Compilar el frontend (`npm run build` o `npx tsc --noEmit`) y verificar que no hay errores de tipos TypeScript
- [x] 1.V2 Verificar que las interfaces existentes (`Fase4Pregunta`, `Fase4AnswerPayload`, etc.) no fueron rotas: ejecutar `npx tsc --noEmit` sin errores

---

## 2. Componente Visual SVG (Frontend)

- [x] 2.1 Crear el componente `Fase4NonHomogeneousPolygon.tsx` en `components/fase4/` con las props: `sectors`, `viewBox`, `selectedIds`, `onToggleSector`, `accentColor`, `targetFractionText`
- [x] 2.2 Implementar el renderizado SVG con `<polygon>` para cada sector, usando `viewBox` normalizado y bordes blancos (`stroke="#ffffff"`, `strokeWidth={1.5}`)
- [x] 2.3 Implementar la lógica de toggle (clic para colorear/descolorear) con estado local `selectedIds` y transiciones CSS suaves (`transition-all duration-200`)
- [x] 2.4 Implementar efecto hover (opacidad reducida suave) y cursor pointer en los sectores
- [x] 2.5 Implementar el indicador de progreso visual: barra o pill que muestre la suma actual de pesos seleccionados vs. `target_value` (ej: "2/6 seleccionado → objetivo: 1/2")
- [x] 2.6 Implementar el botón "Reiniciar" que vacía la selección de sectores

### ✅ Verificación del Grupo 2
- [x] 2.V1 Compilar el frontend sin errores de TypeScript (`npx tsc --noEmit`)
- [x] 2.V2 Crear un archivo de prueba temporal (`scratch/test_polygon.tsx` o storybook) que renderice el componente con datos hardcoded de un rectángulo de 3 sectores (mitad + dos cuartos) y verificar visualmente en el navegador que: (a) los polígonos se dibujan correctamente, (b) el clic cambia el color a púrpura, (c) el segundo clic deselecciona, (d) el hover muestra efecto de opacidad, (e) el botón "Reiniciar" limpia todo
- [x] 2.V3 Probar con datos hardcoded de un triángulo de 6 sectores (medianas) y verificar que los polígonos triangulares se renderizan sin solapamientos ni huecos visuales

---

## 3. Integración en la Pantalla de Juego (Frontend)

- [x] 3.1 Agregar la rama condicional `tipo_visual === 'non_homogeneous_polygon'` en `Fase4GameScreen.tsx` (sección de renderizado visual, ~línea 1494) para renderizar `Fase4NonHomogeneousPolygon` en lugar de los visualizadores existentes
- [x] 3.2 Conectar el estado de sectores seleccionados al flujo de envío de respuesta: al presionar "CONFIRMAR", construir `respuesta_dada` como string de IDs separados por coma (ej: `"1,3,5"`)
- [x] 3.3 Asegurar que el enunciado se muestre debajo de la figura SVG en español con el formato existente (`dangerouslySetInnerHTML`)
- [x] 3.4 Verificar que los botones de acción muestren texto en español: "CONFIRMAR", "Continuar →", "Intentar de nuevo ↺"

### ✅ Verificación del Grupo 3
- [x] 3.V1 Compilar el frontend sin errores de TypeScript (`npx tsc --noEmit`)
- [x] 3.V2 Insertar manualmente (vía consola del navegador o mock local) una pregunta de prueba con `tipo_visual: "non_homogeneous_polygon"` y verificar que el `Fase4GameScreen` renderiza correctamente el componente de polígonos en lugar de la pizza o el termómetro
- [x] 3.V3 Verificar que al seleccionar sectores y presionar "CONFIRMAR", el payload enviado al backend contiene `respuesta_dada` con el formato correcto de IDs (ej: `"1,3,5"`) — inspeccionar con DevTools > Network
- [x] 3.V4 Cargar una pregunta existente de tipo `pizza` (Módulo 1 Nivel 1) y verificar que sigue funcionando exactamente igual (prueba de regresión de tipos visuales existentes)

---

## 4. Validación en el Backend

- [x] 4.1 Agregar una rama condicional en el endpoint `/responder` de `router.py` (~línea 700) que detecte `tipo_visual == "non_homogeneous_polygon"` en los `datos_numericos` de la pregunta
- [x] 4.2 Implementar la lógica de parseo: separar `respuesta_dada` por coma, convertir a lista de IDs enteros, buscar los `weight` correspondientes en `datos_numericos.sectors`
- [x] 4.3 Implementar la validación: sumar los pesos, comparar contra `datos_numericos.target_value` con tolerancia `abs(suma - target) < 0.001`
- [x] 4.4 Generar feedback de respuesta correcta en español (ej: "¡Excelente! Has coloreado exactamente 1/2 de la figura.")
- [x] 4.5 Generar feedback de respuesta incorrecta en español (ej: "La fracción coloreada no coincide con 1/2. Intenta seleccionar piezas que sumen la mitad del área total.")

### ✅ Verificación del Grupo 4
- [x] 4.V1 Escribir un test unitario (o script de prueba en `scratch/`) que simule el envío de una respuesta con IDs `"1,3,5"` contra una pregunta mock con sectors de pesos `[0.125, 0.125, 0.25, 0.125, 0.125, 0.125, 0.125]` y `target_value: 0.5`, y verificar que retorna `es_correcta: true`
- [x] 4.x Probar con IDs `"1,2"` (suma = 0.25) contra `target_value: 0.5` y verificar que retorna `es_correcta: false`
- [x] 4.V2 Probar con IDs `"1,2"` (suma = 0.25) contra `target_value: 0.5` y verificar que retorna `es_correcta: false`
- [x] 4.V3 Probar tolerancia flotante: IDs que suman `0.33333` contra `target_value: 0.333` y verificar `es_correcta: true`
- [x] 4.V4 Verificar que una pregunta existente de tipo `respuesta_numerica` (ej: Módulo 2) sigue validándose correctamente con la lógica original (prueba de regresión del endpoint)

---

## 5. Preguntas Semilla - Módulo 1 Nivel 3 (Backend)

- [x] 5.1 Crear funciones generadoras de geometrías base en `seed.py`: `_build_rect_half_quarters()`, `_build_rect_rows_tenths()`, `_build_rect_columns_sixths()` que retornen arrays de sectors con puntos y pesos calculados
- [x] 5.2 Crear funciones generadoras de triángulos: `_build_triangle_medians_6()`, `_build_triangle_midpoints_4()`, `_build_triangle_asymmetric_complex()` que retornen arrays de sectors
- [x] 5.3 Reemplazar la lógica actual del Nivel 3 en `generate_practice_question_fase4()` (bloque `else: # Asimetría`, ~línea 808) para generar preguntas de tipo `non_homogeneous_polygon` usando las funciones generadoras
- [x] 5.4 Implementar la variación dinámica: para cada geometría base, generar variantes con diferentes `target_value` (ej: 1/2, 1/3, 2/3, 1/4, 3/4) y `target_fraction_text` correspondiente
- [x] 5.5 Implementar variantes con fracciones no simplificadas (ej: `target_fraction_text: "2/4"` con `target_value: 0.5`) para familias de variación espejo
- [x] 5.6 Asegurar que todos los enunciados generados estén en español: "Colorea {fracción} de la figura" o "Colorea {fracción} del triángulo"

### ✅ Verificación del Grupo 5
- [x] 5.V1 Ejecutar el seed en el entorno local Docker (`docker compose ... exec backend python -m app.fase4.seed`) y verificar que no hay errores de ejecución
- [x] 5.V2 Conectarse a la BD local (`psql`) y consultar las preguntas del Módulo 1 Nivel 3 (sección 103): verificar que `datos_numericos` contiene `tipo_visual: "non_homogeneous_polygon"` con `sectors`, `target_value` y `viewBox`
- [x] 5.V3 Verificar que las geometrías base generan al menos 3 variantes de fracción objetivo distintas por familia
- [x] 5.V4 Verificar que al menos una variante usa fracción no simplificada (ej: `target_fraction_text: "2/4"`)
- [x] 5.V5 Verificar que la suma total de `weight` de todos los `sectors` de cada pregunta es exactamente `1.0` (±0.001)

---

## 6. Preguntas Semilla - Módulo 3 Porcentajes (Backend)

- [x] 6.1 Agregar al generador de Módulo 3 (`modulo_id == 3`) una rama para el Nivel 1 que genere preguntas de porcentaje usando las mismas geometrías base del Módulo 1
- [x] 6.2 Formular los enunciados en español con formato de porcentaje: "Colorea el 50% de la figura", "Colorea el 33% de la figura"
- [x] 6.3 Establecer `target_value` como decimal equivalente (50% → 0.5, 33.3% → 0.333, 25% → 0.25)

### ✅ Verificación del Grupo 6
- [x] 6.V1 Ejecutar el seed y verificar que las preguntas de Módulo 3 con `tipo_visual: "non_homogeneous_polygon"` se insertan en la BD sin errores
- [x] 6.V2 Consultar la BD y verificar que los enunciados de Módulo 3 usan formato de porcentaje en español ("Colorea el X% de la figura")
- [x] 6.V3 Verificar que los `target_value` de las preguntas de Módulo 3 coinciden con los equivalentes decimales de los porcentajes del enunciado

---

## 7. Modal de Feedback Visual "¿Por qué?" (Frontend)

- [x] 7.1 Crear la lógica de simplificación visual: dado un array de `selectedIds` y los `sectors`, identificar sectores adyacentes coloreados y calcular qué bordes internos deben ocultarse
- [x] 7.2 Implementar el renderizado de dos figuras SVG lado a lado en el modal: la original con sectores coloreados y la versión consolidada con bordes internos desvanecidos
- [x] 7.3 Agregar texto explicativo en español debajo de las figuras (ej: "Al combinar cada columna en una sola pieza, se ve que 2/3 significa tomar 2 de 3 partes iguales.")
- [x] 7.4 Integrar el botón "¿Por qué?" en el flujo de feedback post-respuesta correcta de `Fase4GameScreen.tsx`

### ✅ Verificación del Grupo 7
- [x] 7.V1 Compilar el frontend sin errores de TypeScript
- [x] 7.V2 En el navegador, responder correctamente una pregunta `non_homogeneous_polygon` y verificar que aparece el botón "¿Por qué?"
- [x] 7.V3 Presionar "¿Por qué?" y verificar que el modal muestra las dos figuras lado a lado (original y simplificada) con el texto explicativo en español
- [x] 7.V4 Verificar que el modal "¿Por qué?" no aparece para preguntas de tipo `pizza` ni `thermometer` (sin regresión)

---

## 8. Verificación Final e Integración Completa

- [x] 8.1 Ejecutar el seed completo (purge + reseed) en entorno local y verificar que todas las preguntas de Fase 4 se generan sin errores
- [x] 8.2 Realizar el flujo completo de juego en el navegador para Módulo 1 Nivel 3: teoría → pregunta interactiva → seleccionar sectores → confirmar → feedback correcto/incorrecto → "¿Por qué?" → continuar
- [x] 8.3 Realizar el flujo completo para Módulo 3 con una pregunta de porcentaje usando polígonos
- [x] 8.4 Probar en dispositivo móvil (o DevTools responsive) que las figuras SVG se escalan correctamente sin deformarse
- [x] 8.5 Verificar que los Módulos 1 (Niveles 1 y 2), Módulo 2, Módulo 3 (niveles existentes) y Módulo 4 siguen funcionando sin cambios (prueba de regresión completa)
- [x] 8.6 Verificar que la barra de progreso del nivel y la graduación de fase no se vieron afectadas
