## Why

El modal de "Segunda Oportunidad" (Bucle Espejo) en la Fase 4 de Fracción de Cantidad presenta scroll vertical debido a textos redundantes y un layout excesivamente grande. Esto impide que toda la información visual del modal se mantenga en una sola pantalla, rompiendo los criterios pedagógicos y de diseño del proyecto.

Además, el teclado virtual del modal espejo difiere en distribución y comportamiento del diseño estándar simétrico de grilla 3x4 definido en la Fase 2 (que sirve como modelo de consistencia UX para todas las fases), y existen errores de género gramatical en las preguntas generadas en el backend (ej. "¿Cuántos cartas le QUEDAN...").

## What Changes

- **Ocultamiento de la pregunta anterior fallida:** El enunciado completo de la pregunta anterior que causó la equivocación desaparecerá del bloque de repaso superior del modal.
- **Rediseño compacto del Repaso:** Rediseñar la sección de repaso de la respuesta anterior para que ocupe una barra horizontal delgada y minimalista que no requiera scroll.
- **Teclado Simétrico 3x4 Estándar (Fase 2):** Implementar en el modal de la Fase 4 el teclado simétrico de 3x4 (`[.] [0] [Borrar]` y botón Confirmar abajo) idéntico al de la Fase 2, pero con estilos locales `.f4-` y con la tecla de punto decimal `.` deshabilitada visual y funcionalmente (ya que en la Fase 4 las respuestas son cantidades enteras).
- **Estilos CSS Locales y Autónomos:** Definir todos los estilos de layout y teclado del modal en `Fase4Styles.css` utilizando el prefijo `.f4-` para evitar depender de que los estilos de la Fase 2 estén cargados en memoria.
- **Corrección de Género en el Backend:** Adaptar dinámicamente el artículo interrogativo ("¿Cuántos/as") y la preposición ("de los/las") según el género de la colección en el generador de enunciados (`LogicaMath/backend/app/fase4/seed.py`).

## Capabilities

### New Capabilities
- Ninguna.

### Modified Capabilities
- `phase-design-consistency`: Se modifica el requisito de comportamiento del Bucle Espejo para establecer que toda la información se debe mantener en una sola pantalla sin scroll, eliminando el texto del enunciado de la pregunta anterior en la sección de repaso y optimizando el espaciado vertical, además de obligar a que el teclado del modal espejo mantenga la grilla simétrica de 3x4 con botón de confirmación de ancho completo inferior unificado.

## Impact

- **Frontend:** Modificación de `Fase4MirrorModal.tsx` y `Fase4Styles.css` para aplicar el teclado simétrico 3x4 portado con estilos `.f4-` y el layout compacto horizontal de repaso sin scroll.
- **Backend:** Modificación de `seed.py` de la Fase 4 para corregir la gramática de los enunciados del Módulo 2.
- **Base de Datos:** Se requiere volver a sembrar (seed) las preguntas de la Fase 4 en el entorno local para actualizar los enunciados corregidos en la tabla `preguntas`.
