# Spec: Fase 4 Gameplay UX

## Purpose
Optimización del flujo y distribución visual de inputs de respuesta y botones "Confirmar" en las pantallas de juego de Fase 4.

## Requirements

### Requirement: Caja de inputs de respuesta dentro de la tarjeta visual en Fase 4
El frontend de la Fase 4 SHALL reubicar la caja de entrada de respuestas (tanto el input de fracción `f4-fraction-input-box` como el input de entero simple) desde la columna de la derecha hacia la parte inferior de la tarjeta visual de la columna de la izquierda, colocándose justo debajo del texto del enunciado de la pregunta.

#### Scenario: Visualización del input de fracción en la tarjeta izquierda
- **WHEN** se carga una pregunta que requiere ingreso manual de fracción (por ejemplo, identificación de fracción pintada en pizza) en la Fase 4
- **THEN** la caja con los campos de entrada de numerador y denominador (con los correspondientes "?") se muestra en la parte inferior de la tarjeta izquierda, debajo del enunciado de la pregunta, y la columna de la derecha solo muestra el teclado numérico.

#### Scenario: Visualización del input de número entero simple en la tarjeta izquierda
- **WHEN** se carga una pregunta que requiere ingreso manual de un número entero simple en la Fase 4
- **THEN** la caja con el campo de entrada numérico único se muestra en la parte inferior de la tarjeta izquierda, debajo del enunciado de la pregunta, y la columna de la derecha solo muestra el teclado numérico.

### Requirement: Layout y márgenes balanceados en la tarjeta izquierda
Los estilos de la Fase 4 MUST ajustar márgenes, paddings y flexbox en la tarjeta visual de la izquierda para acomodar el input de respuesta sin que interfiera con los gráficos del visualizador (`Fase4VisualizerEngine`) y asegurando que sea perfectamente legible y responsivo.

#### Scenario: Ajuste de tamaño y márgenes en pantallas medianas y grandes
- **WHEN** la pantalla tiene resolución de escritorio (por ejemplo, viewport 2560x945)
- **THEN** la tarjeta izquierda se organiza en un flex vertical centrado, con un margen de separación superior de `mt-6` para el input de respuesta, manteniendo un min-height de 300px o superior que preocupe suficiente espacio sin desbordamiento.

### Requirement: Botones Confirmar compactos y ergonómicos en la Fase 4
El frontend de la Fase 4 SHALL reducir el tamaño y volumen de todos los botones de "CONFIRMAR" (interactivo, de formas y de opción múltiple) a dimensiones ergonómicas que se integren con la interfaz infantil sin saturar el espacio visual.

#### Scenario: Reducción del botón Confirmar en modo interactivo
- **WHEN** se carga una pregunta de sombreado interactivo en la Fase 4
- **THEN** el botón de Confirmar a la derecha se muestra con un tamaño máximo de `280px` de ancho, padding vertical `py-4 px-6`, texto de `text-xl` y esquinas redondeadas de `2xl` con un icono circular de check compacto (`w-8 h-8`).
