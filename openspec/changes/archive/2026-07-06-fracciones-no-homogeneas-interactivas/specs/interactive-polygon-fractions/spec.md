## ADDED Requirements

### Requirement: Renderizado SVG interactivo de polígonos no homogéneos
El sistema DEBE renderizar figuras geométricas SVG con sectores de áreas no homogéneas que el alumno puede colorear haciendo clic. Cada sector se dibuja como un elemento `<polygon>` con coordenadas normalizadas en un `viewBox` de 100x100. Los sectores sin seleccionar DEBEN mostrarse en gris oscuro y los seleccionados en el color de acento del módulo activo.

#### Scenario: Renderizado inicial de la figura
- **WHEN** se carga una pregunta con `tipo_visual: "non_homogeneous_polygon"` en `datos_numericos`
- **THEN** el sistema DEBE renderizar un SVG con todos los sectores definidos en `datos_numericos.sectors`, cada uno como un `<polygon>` con fondo gris oscuro, bordes blancos (`stroke="#ffffff"`) y cursor pointer

#### Scenario: Colorear un sector al hacer clic
- **WHEN** el alumno hace clic en un sector no coloreado
- **THEN** el sector DEBE cambiar su relleno al color de acento del módulo (ej: `#A855F7` para Módulo 1) con una transición suave de 200ms

#### Scenario: Deseleccionar un sector al hacer clic nuevamente
- **WHEN** el alumno hace clic en un sector ya coloreado
- **THEN** el sector DEBE volver a su color gris oscuro original con una transición suave de 200ms

#### Scenario: Botón "Reiniciar" limpia la selección
- **WHEN** el alumno presiona el botón "Reiniciar"
- **THEN** todos los sectores DEBEN volver a su estado gris oscuro y la lista de seleccionados DEBE vaciarse

---

### Requirement: Validación por suma de pesos decimales
El backend DEBE validar las respuestas de preguntas `non_homogeneous_polygon` sumando los valores `weight` de los sectores seleccionados y comparando contra el `target_value` con una tolerancia de `0.001`.

#### Scenario: Respuesta correcta cuando la suma coincide con el target
- **WHEN** el alumno envía los IDs de sectores `[1, 5, 6]` cuya suma de pesos es `0.125 + 0.125 + 0.25 = 0.5`
- **AND** el `target_value` de la pregunta es `0.5`
- **THEN** el sistema DEBE marcar la respuesta como correcta (`es_correcta: true`)

#### Scenario: Respuesta incorrecta cuando la suma no coincide
- **WHEN** el alumno envía los IDs de sectores `[1, 2]` cuya suma de pesos es `0.125 + 0.125 = 0.25`
- **AND** el `target_value` de la pregunta es `0.5`
- **THEN** el sistema DEBE marcar la respuesta como incorrecta (`es_correcta: false`)

#### Scenario: Tolerancia de punto flotante
- **WHEN** la suma calculada es `0.33333333` y el `target_value` es `0.333`
- **THEN** el sistema DEBE considerar la respuesta como correcta porque `abs(0.33333333 - 0.333) < 0.001`

---

### Requirement: Variación dinámica de preguntas sobre un mismo asset
El sistema DEBE soportar múltiples preguntas que comparten la misma definición geométrica de `sectors` pero con diferentes valores de `target_value` y `target_fraction_text`.

#### Scenario: Misma figura con diferente fracción objetivo
- **WHEN** se generan preguntas semilla para una grilla de rectángulos con 6 sectores
- **THEN** se DEBEN crear al menos 3 variantes: una para `target_value: 0.333` (1/3), otra para `target_value: 0.667` (2/3), y otra para `target_value: 0.167` (1/6)

#### Scenario: Enunciados con fracciones no simplificadas
- **WHEN** se genera una variante con `target_fraction_text: "2/4"`
- **THEN** el enunciado DEBE mostrar "Colorea 2/4 del triángulo" y el `target_value` DEBE ser `0.5`

---

### Requirement: Preguntas semilla para Módulo 1 Nivel 3
El seed DEBE generar preguntas interactivas de coloreado asimétrico para el Módulo 1 Nivel 3, reemplazando las preguntas actuales de tipo Sí/No.

#### Scenario: Generación de preguntas con rectángulos subdivididos
- **WHEN** se ejecuta el seed para Módulo 1, Nivel 3
- **THEN** se DEBEN generar al menos 6 geometrías base de rectángulos subdivididos (mitad-cuartos, filas-décimos, columnas-sextos, etc.) con múltiples variantes de fracción objetivo por cada una

#### Scenario: Generación de preguntas con triángulos subdivididos
- **WHEN** se ejecuta el seed para Módulo 1, Nivel 3
- **THEN** se DEBEN generar al menos 3 geometrías base de triángulos subdivididos (medianas en 6 partes, puntos medios en 4, asimétrico complejo en 7-8 partes) con múltiples variantes de fracción objetivo

#### Scenario: Todas las preguntas en español
- **WHEN** se genera cualquier pregunta semilla
- **THEN** el enunciado DEBE estar en español (ej: "Colorea 1/2 de la figura") y el feedback DEBE estar en español

---

### Requirement: Reutilización para Módulo 3 con enunciados de porcentaje
Las mismas plantillas geométricas DEBEN poder reutilizarse en el Módulo 3 (Porcentajes Rápidos) con enunciados formulados como porcentaje.

#### Scenario: Pregunta de porcentaje sobre la misma geometría
- **WHEN** se crea una pregunta para Módulo 3 usando la misma geometría de rectángulo subdividido
- **THEN** el enunciado DEBE decir "Colorea el 50% de la figura" en lugar de "Colorea 1/2 de la figura"
- **AND** el `target_value` DEBE ser `0.5`

---

### Requirement: Modal de feedback visual de simplificación
El sistema DEBE mostrar un modal de feedback visual ("¿Por qué?") que explique la equivalencia de las áreas seleccionadas.

#### Scenario: Vista de simplificación con figuras lado a lado
- **WHEN** el alumno responde correctamente y presiona "¿Por qué?"
- **THEN** el modal DEBE mostrar dos figuras SVG lado a lado: la original con los sectores coloreados, y una versión simplificada donde los bordes internos entre sectores adyacentes coloreados se ocultan para mostrar bloques consolidados

#### Scenario: Explicación textual en español
- **WHEN** se muestra el modal de simplificación
- **THEN** DEBE incluir un texto explicativo en español que describa la equivalencia (ej: "Al combinar cada columna en una sola pieza, se ve que 2/3 significa tomar 2 de 3 partes iguales.")

---

### Requirement: Interfaz 100% en español
Todos los elementos de interfaz relacionados con este componente DEBEN estar en español.

#### Scenario: Botones del juego en español
- **WHEN** se muestra la pantalla de juego con una pregunta `non_homogeneous_polygon`
- **THEN** los botones DEBEN mostrar "Comprobar", "¿Por qué?", "Continuar" y "Reiniciar" (nunca "Check", "Why?", "Continue" ni "Start over")

#### Scenario: Enunciados en español
- **WHEN** se genera una pregunta de coloreado
- **THEN** el enunciado DEBE usar el formato "Colorea X/Y de la figura" o "Colorea el Z% de la figura"

---

### Requirement: Conservación de la estética visual de Fase 4
El nuevo componente DEBE integrarse visualmente con el tema oscuro existente de la Fase 4 sin introducir colores ni estilos nuevos.

#### Scenario: Fondos y contenedores consistentes
- **WHEN** se renderiza el componente de polígonos no homogéneos
- **THEN** DEBE usar fondo de tarjeta `bg-slate-900/40` con borde `border-white/5` y esquinas redondeadas `rounded-[2.5rem]`, idéntico al contenedor visual actual de la Fase 4

#### Scenario: Colores de acento por módulo
- **WHEN** se colorea un sector en Módulo 1
- **THEN** el color de relleno DEBE ser el púrpura del Módulo 1 (`#A855F7`)
- **WHEN** se colorea un sector en Módulo 3
- **THEN** el color de relleno DEBE ser el púrpura del Módulo 3 (`#7C3AED`)
