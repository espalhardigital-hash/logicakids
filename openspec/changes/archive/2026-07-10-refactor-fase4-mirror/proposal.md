## Why

La pantalla `Fase4MirrorModal` en la Fase 4 omite renderizar las interfaces gráficas y visuales (como pizzas fraccionarias o vasos medidores), limitándose a mostrar texto y un teclado numérico sin opción de fracción (`/`). Esto bloquea a los alumnos de responder preguntas de fracciones interactivas, rompiendo la experiencia visual ("Mirror Loop") prescrita en la Guía UX y provocando fallos en la completitud de la plataforma.

## What Changes

- Creación de un nuevo motor visual llamado `Fase4VisualizerEngine` que encapsula todos los visualizadores interactivos.
- Sustitución del enorme condicional de `Fase4GameScreen` por la llamada al nuevo engine.
- Refactorización de `Fase4MirrorModal` para renderizar `Fase4VisualizerEngine` usando la misma lógica que la pantalla de juego.
- Reemplazo del teclado hardcodeado en `Fase4MirrorModal` por el componente global `<CustomKeyboard>`.
- Habilitación de inputs duales de fracciones (Numerador/Denominador) en el Modal Espejo al identificar una respuesta con el carácter `/`.

## Capabilities

### New Capabilities
- `fase4-visualizer-engine`: Componente centralizado que gestiona todos los visuales de fracciones y proporciones de manera reactiva e independiente de la pantalla en la que se monte.
- `mirror-modal-fraction-input`: El Mirror Modal ahora soporta fracciones y usa el teclado numérico estándar global.

### Modified Capabilities
- N/A

## Impact

- `LogicaMath/frontend/components/fase4/Fase4GameScreen.tsx`: Se simplificará su método `render`, delegando la capa visual.
- `LogicaMath/frontend/components/fase4/Fase4MirrorModal.tsx`: Se transformará para utilizar visuales dinámicos y un teclado re-utilizable, arreglando bloqueos funcionales.
- `LogicaMath/frontend/components/fase4/Fase4VisualizerEngine.tsx`: Nuevo componente creado en base al código extraído.
