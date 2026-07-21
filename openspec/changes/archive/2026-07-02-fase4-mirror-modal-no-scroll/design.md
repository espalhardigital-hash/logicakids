## Context

El modal espejo (segunda oportunidad) de la Fase 4 renderiza el enunciado largo del problema anterior fallido en el bloque de repaso superior. Esto añade una altura considerable al modal, forzando un scroll vertical no deseado en resoluciones habituales y rompiendo el estándar visual del juego. 

Además, se busca unificar el comportamiento de los teclados virtuales en modales de espejo de todas las fases, tomando como referencia el diseño simétrico de grilla 3x4 y botón inferior de la Fase 2, y corrigiendo errores de género gramatical en las preguntas de colecciones de la Fase 4 en el backend.

## Goals / Non-Goals

**Goals:**
- Asegurar que todo el contenido del modal de segunda oportunidad de la Fase 4 quepa en la pantalla en una sola visualización sin scroll.
- Ocultar la pregunta anterior fallida del repaso y mostrar únicamente la respuesta errónea del alumno y la respuesta esperada en formato horizontal compacto.
- Implementar el diseño de teclado simétrico de 3x4 de la Fase 2 (`[.] [0] [Borrar]` y botón Confirmar abajo) adaptado con estilos locales `.f4-` en el modal de la Fase 4.
- Deshabilitar el botón del punto decimal `.` visual y funcionalmente en el teclado del modal, ya que la Fase 4 opera con números enteros discretos (cartas, monedas, etc.), manteniendo al mismo tiempo la cuadrícula táctil de 3x4 intacta.
- Lograr la autonomía de estilos de la Fase 4 portando los estilos necesarios de `.f2-` a `.f4-` en `Fase4Styles.css`.
- Corregir el género gramatical en las preguntas de colecciones de la Fase 4 en el backend.

**Non-Goals:**
- No se modificará el comportamiento del Bucle Espejo en otras fases (como la Fase 2), a menos que el usuario lo requiera expresamente en otro cambio.
- No se alterará el motor lógico de evaluación del backend ni el Tutor Invisible.

## Decisions

### 1. Eliminación del enunciado de la pregunta anterior y compactación horizontal
- **Decisión:** Remover el bloque `{lastQuestionEnunciado && ...}` de la UI en `Fase4MirrorModal.tsx` y reestructurar el bloque de REPASO restante para que sea una barrita flex horizontal de altura fija mínima (~40-50px).
- **Razonamiento:** El enunciado anterior aporta poco valor pedagógico en esta pantalla rápida de segunda oportunidad y es el elemento principal que consume el espacio vertical. Al removerlo, garantizamos espacio suficiente para la nueva pregunta y el teclado.
- **Alternativas consideradas:** Mantener el enunciado pero colapsarlo en un acordeón interactivo. Se descartó porque añade interacción innecesaria y complejidad en una pantalla para niños.

### 2. Uso del Teclado Simétrico 3x4 con Punto Deshabilitado
- **Decisión:** Implementar directamente en `Fase4MirrorModal.tsx` el teclado numérico virtual del estándar de la Fase 2:
  - Fila final con `[.]` (deshabilitado), `[0]`, `[Borrar]`.
  - Botón "Confirmar" de ancho completo (`w-full`) e independiente colocado debajo de la grilla.
- **Razonamiento:** Sigue la Guía de UX del proyecto y respeta el estándar de la Fase 2. La tecla del punto decimal se mantendrá dentro de la grilla para preservar la consistencia táctil del layout de 3x4, pero se mostrará en baja opacidad (`opacity-25`) y con el comportamiento click desactivado, ya que el dominio numérico de la Fase 4 es de cantidades enteras.
- **Alternativas consideradas:** Usar el `CustomKeyboard` de la pantalla principal de la Fase 4. Se descartó para priorizar la fidelidad al estándar del modal espejo unificado de la Fase 2 y la Guía de UX que exige la disposición de grilla 3x4 con punto y borrar a la derecha, y botón inferior.

### 3. Autonomía de estilos CSS en Fase 4
- **Decisión:** Copiar las reglas de estilos de espejo, de custom input y del teclado virtual (keypad) de la Fase 2, renombrarlas con prefijo `.f4-`, y agregarlas directamente al final de `Fase4Styles.css`, importando este archivo en `Fase4MirrorModal.tsx`.
- **Razonamiento:** Evita el riesgo de interfaz rota si la Fase 2 no se ha cargado previamente en memoria en la Single Page App.
- **Alternativas consideradas:** Importar `Fase2Styles.css` directamente desde `Fase4MirrorModal.tsx`. Se descartó porque viola el principio de independencia y encapsulación por fases, y podría acarrear efectos secundarios o colisiones de estilo no deseadas.

### 4. Lógica de género condicional en Backend (seed.py)
- **Decisión:** Determinar dinámicamente el artículo interrogativo ("¿Cuántos" o "¿Cuántas") y la preposición ("de los" o "de las") al momento de generar la pregunta basándonos en una lista explícita de colecciones femeninas.
- **Razonamiento:** Es la solución más directa y de bajo coste de cómputo para corregir los textos autogenerados.
- **Alternativas consideradas:** Almacenar el género gramatical en un diccionario estructurado de colecciones en base de datos. Se descartó por ser excesivamente complejo para el alcance actual del proyecto.

## Risks / Trade-offs

- **[Risk] Inconsistencia visual menor en Fase 4:** El teclado del juego principal en Fase 4 usa `CustomKeyboard` (opción A) mientras que el modal espejo usará el teclado estándar simétrico 3x4 de la Fase 2 (opción B). 
  - **Mitigación:** Esta diferencia está justificada y es deseada para alinearse con el diseño de Bucle Espejo premium unificado y la Guía de UX. Además, el teclado simétrico de 3x4 del modal se diseñará estéticamente muy limpio y unificado con los colores purpuras de la Fase 4.
- **[Risk] Persistencia de datos de preguntas viejas:** Si no se re-siembra la base de datos local tras aplicar la corrección en `seed.py`, el usuario seguirá viendo las preguntas con errores gramaticales generadas anteriormente.
  - **Mitigación:** Ejecutar un truncado y una nueva siembra de la tabla `preguntas` en el contenedor local de PostgreSQL al realizar la verificación del cambio.
