## Context

El proyecto requiere que todas las fases pedagógicas de la plataforma mantengan una consistencia visual y de comportamiento estructurada alrededor de la **Fase 2**, que sirve como la fase patrón.

Se han detectado dos incoherencias de diseño fundamentales en la Fase 4:
1. **Apoyo Gráfico Inconsistente:** En las preguntas de "Fracción de Cantidad" (Fase 4, Módulo 2, Nivel 3) que tratan sobre colecciones discretas de objetos (figuritas, cartas, tazos, etc.), el frontend renderiza un vaso graduado (*beaker*) con líquido morado para representar la fracción del complemento. Este elemento visual es confuso e inadecuado, ya que el agua de un vaso no es la manera idónea de representar colecciones discretas de figuritas o cartas.
2. **Mensaje e Interfaz de Bucle Espejo Fuera de Patrón:** En la Fase 4, al activarse el Bucle Espejo, se muestra un banner inline morado encima del tablero del juego. En la Fase 2, la activación del Bucle Espejo lanza un modal de pantalla completa (`Fase2MirrorModal`) que cambia el modo de interacción a un entorno enfocado de "¡SEGUNDA OPORTUNIDAD!" para repasar el concepto.

## Goals / Non-Goals

**Goals:**
- Modificar el apoyo visual en la Fase 4 (Módulo 2, Nivel 3) para ocultar o reemplazar la representación de vaso graduado (*beaker*) en problemas de colecciones de objetos discretos, optando por una visualización en cuadrícula de elementos, pizzas, barras o simplemente deshabilitar la imagen si no es coherente con el enunciado.
- Estandarizar la interfaz de alerta del Bucle Espejo en la Fase 4 (y revisar Fase 3 u otras fases posteriores si aplica) implementando un componente `Fase4MirrorModal` (y equivalentes) que herede el patrón modal de pantalla completa establecido en la Fase 2 (`Fase2MirrorModal`).
- Garantizar que el flujo de rescate y espejo en el frontend llame a los endpoints correctos en cada fase.

**Non-Goals:**
- Reescribir la lógica de validación o cálculo del Bucle Espejo en el backend.
- Cambiar la estructura matemática de las preguntas o alterar los parámetros de la semilla del backend.

## Decisions

### Decisión 1: Eliminar/Reemplazar el vaso graduado (beaker) para colecciones discretas
* **Opción A (Recomendada):** Ocultar el componente `BeakerVisualizer` o similar en el frontend cuando el contexto de la pregunta de la Fase 4 sea de tipo discreto (por ejemplo, si la variable `tipo_visual` es "beaker" pero la colección es "figuritas", "tazos", "cartas", "monedas de oro", "manzanas"). Es mejor no mostrar apoyo visual confuso que desvíe la atención del alumno. Si se mantiene apoyo gráfico, debe ser en forma de cuadrícula de objetos discretos o barra segmentada.
* **Alternativa Considerada:** Implementar un visualizador de cuadrícula de iconos en SVG. Sin embargo, para evitar sobrecargar el frontend en la Fase 4 y alinearlo con la simplicidad de la Fase 2, se optará por no mostrar una imagen de apoyo inconsistente, limitando el visualizador a preguntas de volumen o áreas.

### Decisión 2: Implementar un `MirrorModal` de pantalla completa en la Fase 4 y unificar criterios
* **Opción A (Recomendada):** Crear un componente `Fase4MirrorModal.tsx` con el mismo diseño visual de la Fase 2. Cuando el backend devuelva `es_espejo: true`, en lugar de renderizar la alerta inline, se activará el estado `showMirrorModal` que abrirá este modal superpuesto de pantalla completa con su propio flujo interactivo.
* **Alternativa Considerada:** Mantener el banner inline actual pero cambiarle el texto. Rechazada porque el usuario solicita explícitamente que la alerta y la interfaz sigan el patrón estándar de la Fase 2.

## Risks / Trade-offs

* **[Riesgo] Estilos CSS no unificados:** Al portar el componente `MirrorModal` a otras fases, se pueden arrastrar dependencias de CSS específicas de la Fase 2 (`Fase2Styles.css`).
  * *Mitigación:* Se creará un estilo común o se adaptará el CSS de cada modal en su respectivo archivo de estilos de fase (ej. `Fase4Styles.css`).
* **[Riesgo] Inconsistencias en Fase 3:** Aunque el reporte se centra en la Fase 4 y fases posteriores, la Fase 3 también tiene menciones a "Bucle Espejo Activado" en el frontend.
  * *Mitigación:* Se auditará la Fase 3 como parte de las tareas para verificar si el Bucle Espejo allí también rompe el patrón de la Fase 2 y unificarlo si es necesario.
