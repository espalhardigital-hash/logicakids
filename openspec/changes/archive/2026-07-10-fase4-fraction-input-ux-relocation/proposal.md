## Why

En la Fase 4 del juego de lógica matemática (La Fracción Visual), la UI presenta dos problemas de ergonomía y experiencia de usuario (UX):
1. El casillero de respuesta (el input de la fracción con el numerador, el denominador y los símbolos "?") se ubica arriba en la columna derecha, obligando a los niños a desviar la atención constantemente de la tarjeta de la pregunta (a la izquierda) hacia la derecha.
2. El botón de "CONFIRMAR" en el área interactiva y el panel de control es desproporcionadamente grande (usa tipografía `text-4xl` o `text-3xl`, paddings verticales de hasta `py-8` y un ancho máximo muy amplio). Esto satura la pantalla, reduce la armonía del diseño y dificulta una interacción cómoda para los niños.

## What Changes

- Reubicar el contenedor de inputs (`f4-fraction-input-box` y la caja de input numérico simple) en `Fase4GameScreen.tsx` de la columna derecha a la columna izquierda (dentro de la tarjeta de representación visual del problema, justo debajo del enunciado de la pregunta).
- Reducir significativamente el tamaño del botón de "CONFIRMAR" en toda la Fase 4:
  - Cambiar el tamaño de tipografía de `text-4xl` / `text-3xl` a `text-xl`.
  - Reducir paddings de `py-8 px-10` o `py-6 px-8` a un formato balanceado de `py-4 px-6`.
  - Reducir el ancho máximo del botón a `max-w-[280px]` (en lugar de `max-w-md`).
  - Rediseñar el indicador circular del check (`w-12 h-12` o `w-10 h-10` a un formato más compacto `w-8 h-8` y tipografía interna `text-base`).
  - Cambiar esquinas redondeadas de `rounded-[2.5rem]` a `rounded-2xl` para consistencia visual.
- Ajustar los estilos correspondientes en `Fase4Styles.css` para optimizar los márgenes de los inputs y del botón confirmar.

## Capabilities

### New Capabilities
<!-- Ninguna nueva capacidad de negocio a nivel conceptual global, sino optimizaciones UX/UI del flujo de juego -->

### Modified Capabilities
- `fase4-gameplay-ux`: Ubicación más natural de los inputs de respuesta manual y reducción/balance de los botones de confirmación en la Fase 4.

## Impact

- `LogicaMath/frontend/components/fase4/Fase4GameScreen.tsx`: Modificación del JSX de React para reordenar las áreas de inputs y reducir las clases de tamaño de los tres botones de Confirmar (interactivo, formas y opción múltiple).
- `LogicaMath/frontend/components/fase4/Fase4Styles.css`: Ajustar paddings y márgenes para acomodar el input en la columna izquierda.
