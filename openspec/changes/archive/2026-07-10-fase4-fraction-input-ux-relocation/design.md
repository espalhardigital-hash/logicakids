## Context

En la pantalla de juego de la Fase 4 (`Fase4GameScreen.tsx`), la caja de respuestas (ya sea fracción con dos inputs y línea horizontal, o número entero con input simple) se renderiza en la columna de la derecha, arriba del teclado numérico. Esto obliga a los niños a desviar su mirada hacia la derecha, alejándose de la pizza u objeto visual y del enunciado de la pregunta (a la izquierda). El usuario solicita mover esta caja de respuesta al final de la tarjeta de la izquierda (debajo del enunciado), de forma que se mantenga el foco lector y visual unificado en una sola tarjeta.
Además, los botones "CONFIRMAR" de toda la Fase 4 son de dimensiones excesivamente grandes, lo cual satura la interfaz. Se solicita disminuir su tamaño de forma sistemática en todas las preguntas de la Fase 4.

## Goals / Non-Goals

**Goals:**
- Mover el JSX condicional de inputs en `Fase4GameScreen.tsx` de la columna derecha a la columna izquierda (tarjeta visual).
- Ajustar estilos CSS en `Fase4Styles.css` para optimizar el espaciado e integrar estéticamente las cajas de inputs en el flujo vertical de la columna izquierda.
- Disminuir el tamaño de todos los botones de "CONFIRMAR" (interactivo, de formas/visuales y de opción múltiple) a un estándar de tipografía `text-xl`, padding `py-4 px-6`, bordes `rounded-2xl` y ancho máximo `max-w-[280px]` (o `w-full` en contenedores específicos).
- Adaptar correspondientemente el indicador de check circular (`w-8 h-8` y `text-base` interna).
- Garantizar un diseño responsivo excelente tanto en pantallas de escritorio como móviles.

**Non-Goals:**
- Cambiar la lógica de validación de respuestas.
- Alterar la posición de otros elementos como el mapa de fases o los modales de teoría.

## Decisions

### Decision 1: Reubicación de inputs en el árbol de componentes React
- **Alternativa A**: Mantener inputs a la derecha pero flotantes. (Rechazada: No soluciona el problema de fragmentación del foco visual).
- **Alternativa B**: Extraer el bloque condicional de inputs manuales (`showFractionInput`) y colocarlo dentro del `motion.div` de `Visual representations card` en `Fase4GameScreen.tsx`, justo debajo del elemento `<p className="text-lg font-bold text-center mt-6 text-slate-200" ... />`. (Seleccionada: Cumple directamente el requerimiento de UX).

### Decision 2: Reducción de dimensiones del botón CONFIRMAR
- **Alternativa A**: Modificar clases CSS globales. (Rechazada: Puede alterar componentes de otras fases).
- **Alternativa B**: Modificar las clases inline y de Tailwind directamente en los tres botones de confirmación dentro de `Fase4GameScreen.tsx` (modos interactivos, de formas y opción múltiple), optimizando su tipografía a `text-xl`, flex gap a `gap-4`, paddings a `py-4 px-6` (en interactivo y opción múltiple) / `py-4 px-6` (en formas), y bordes a `rounded-2xl`. (Seleccionada: Rápida y aislada a Fase 4).

### Decision 3: Reducción del tamaño de fuente en el input simple cuando está en la tarjeta
- **Alternativa A**: Mantener tamaño de texto de `2xl` y padding `p-5` en el input simple. (Rechazada: Ocupa demasiado espacio vertical en la tarjeta izquierda).
- **Alternativa B**: Reducir el padding a `p-4` y el tamaño de texto de `text-2xl` a `text-xl` para el input simple en la columna izquierda, con un `max-w-[200px]` para asegurar compacidad. (Seleccionada: Mantiene la consistencia con la caja de fracciones compacta).

## Risks / Trade-offs

- **[Riesgo]**: En pantallas muy pequeñas, al estar el visualizador, el enunciado y el input dentro de la misma tarjeta, esta podría crecer demasiado verticalmente.
  - **Mitigación**: El contenedor izquierdo tiene paddings adecuados y usa clases fluidas de Tailwind en móvil. Al apilarse en una sola columna en móvil, el input quedará ubicado perfectamente entre el enunciado de la pregunta y el teclado numérico inferior, lo cual es de hecho el flujo móvil ideal.
