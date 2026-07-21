## Why

Se ha identificado una falta de consistencia de diseño visual y pedagógico en la Fase 4 (y potencialmente en fases posteriores) en comparación con la Fase 2, la cual está establecida como el patrón estándar del proyecto. Específicamente, el uso de imágenes de apoyo genéricas (como vasos graduados o "beakers" con porcentajes) no se alinea con el contexto temático de las preguntas (figuritas, cartas, tazos), y los mensajes/alertas de activación del "Bucle Espejo" no siguen la estructura estándar de la Fase 2, afectando la coherencia de la interfaz y el proceso de aprendizaje.

## What Changes

- **Corrección de Apoyo Visual (Fase 4):** Reemplazar las imágenes de vasos graduados (*beakers*) por representaciones consistentes con el contexto del problema (ej. pizzas, barras o diagramas de conjunto) o, en su defecto, no mostrar imágenes que no tengan relación con el contexto de la pregunta.
- **Estandarización del Mensaje del Bucle Espejo (Fase 4):** Modificar el componente y las alertas de activación del Bucle Espejo en el frontend de la Fase 4 para que utilicen el formato estándar de la Fase 2.
- **Auditoría de Consistencia (Fases 5 a 8):** Analizar el código de frontend y backend de las fases 5, 6, 7 y 8 para corregir de manera preventiva cualquier incoherencia en imágenes de apoyo o mensajes del Bucle Espejo.

## Capabilities

### New Capabilities

- `phase-design-consistency`: Reglas y especificaciones para garantizar que el diseño de las preguntas, sus recursos visuales y las alertas del Bucle Espejo sigan el patrón estándar establecido en la Fase 2.

### Modified Capabilities
