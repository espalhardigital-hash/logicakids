## Why

La Fase 4 (Módulo 1: La Fracción Visual, Nivel 3: Áreas y Asimetrías) actualmente solo presenta preguntas de tipo Sí/No ("¿Las secciones son iguales?") y carece de ejercicios interactivos donde el alumno coloree áreas asimétricas para representar fracciones. Esto limita la comprensión profunda del concepto de fracción como proporción de área. Además, el Módulo 3 (Porcentajes Rápidos) puede reutilizar el mismo motor visual para reforzar la equivalencia fracción-porcentaje, multiplicando el contenido pedagógico sin duplicar código.

## What Changes

- **Nuevo componente visual interactivo** (`Fase4NonHomogeneousPolygon.tsx`): Renderiza figuras SVG con sectores de áreas no homogéneas (rectángulos, triángulos) que el alumno puede colorear haciendo clic para sumar la fracción o porcentaje solicitado.
- **Nuevo tipo visual en el backend** (`non_homogeneous_polygon`): Extensión del campo `datos_numericos` en las preguntas para almacenar coordenadas SVG de polígonos con pesos decimales, permitiendo validación por suma de pesos.
- **Nuevas preguntas semilla para Módulo 1 Nivel 3**: Reemplazo de las preguntas actuales de tipo Sí/No por preguntas interactivas de coloreado asimétrico con variación dinámica (misma figura, distinta fracción objetivo). Se incorporan fracciones no simplificadas como reto adicional (ej: "Colorea 2/4" en vez de "Colorea 1/2").
- **Extensión de preguntas para Módulo 3**: Reutilización de las mismas figuras vectoriales con enunciados de porcentaje ("Colorea el 50% de la figura").
- **Nueva lógica de validación en el router**: Rama de validación en `/responder` que suma los pesos de los sectores seleccionados y los compara contra el `target_value` con tolerancia flotante.
- **Modal de feedback "¿Por qué?"**: Vista de simplificación visual comparativa que muestra la figura original coloreada junto a una versión consolidada donde las líneas internas se desvanecen para evidenciar la equivalencia.
- **Todos los textos, botones y explicaciones en español**.

## Capabilities

### New Capabilities
- `interactive-polygon-fractions`: Motor de renderizado SVG interactivo para figuras geométricas con áreas no homogéneas (rectángulos, triángulos), validación por suma de pesos, variación dinámica de preguntas sobre un mismo asset, y feedback visual de simplificación ("¿Por qué?").

### Modified Capabilities
- `gameplay-fase4-multiple-opcion`: Extensión del `Fase4GameScreen.tsx` para soportar el nuevo `tipo_visual` `non_homogeneous_polygon` junto a los tipos existentes (`pizza`, `thermometer`, `beaker`, `pie`, `shapes`).

## Impact

- **Backend** (`app/fase4/router.py`): Nueva rama de validación en el endpoint `/responder` para el tipo `non_homogeneous_polygon` (suma de pesos vs. `target_value`).
- **Backend** (`app/fase4/seed.py`): Nuevas preguntas semilla para Módulo 1 Nivel 3 (reemplazo de preguntas Sí/No) y extensión opcional para Módulo 3 con enunciados de porcentaje.
- **Frontend** (`components/fase4/Fase4GameScreen.tsx`): Integración del nuevo componente visual en el flujo de renderizado condicional por `tipo_visual`.
- **Frontend** (`components/fase4/Fase4NonHomogeneousPolygon.tsx`): Nuevo componente React.
- **Frontend** (`components/fase4/Fase4Types.ts`): Extensión del tipo `datos_numericos` para incluir `sectors`, `target_value`, `target_fraction_text` y `viewBox`.
- **Base de datos**: No requiere migración de esquema; se utiliza el campo JSON existente `datos_numericos` en la tabla `preguntas`.
