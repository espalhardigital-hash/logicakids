## Context

La Fase 4 de la aplicación LogicaKids enseña fracciones y proporciones a través de 4 módulos secuenciales. Actualmente, el **Módulo 1 (La Fracción Visual)** utiliza visualizadores de tipo `pizza` (sectores circulares simétricos) en los niveles 1 y 2, y preguntas de texto Sí/No en el nivel 3 (Áreas y Asimetrías). El **Módulo 3 (Porcentajes Rápidos)** utiliza termómetros y gráficos circulares.

El campo JSON `datos_numericos` de la tabla `preguntas` ya soporta múltiples tipos visuales (`pizza`, `thermometer`, `beaker`, `pie`, `percentage_thermometer`, `percentage_beaker`, `shapes`). El componente `Fase4GameScreen.tsx` renderiza condicionalmente según `tipo_visual`, por lo que la extensión es directa.

La validación de respuestas en `router.py` (`/responder`) compara texto normalizado o alternativa seleccionada. No existe actualmente una rama de validación por suma de pesos decimales.

Toda la interfaz de la Fase 4 utiliza un tema oscuro con fondo `bg-zinc-950` (#09090b), tarjetas `bg-slate-900/40`, bordes `border-white/5`, y colores de acento púrpura por módulo (Módulo 1: `#A855F7`, Módulo 3: `#7C3AED`).

## Goals / Non-Goals

**Goals:**
- Crear un componente SVG interactivo reutilizable que renderice polígonos de áreas no homogéneas (rectángulos subdivididos, triángulos subdivididos) donde el alumno colorea sectores haciendo clic.
- Implementar validación en el backend por suma de pesos decimales (`weight`) de sectores seleccionados vs. `target_value`.
- Generar preguntas semilla para Módulo 1 Nivel 3 que reemplacen las actuales de Sí/No con ejercicios de coloreado interactivo.
- Reutilizar las mismas plantillas geométricas para Módulo 3 con enunciados de porcentaje.
- Implementar un modal de feedback visual de simplificación ("¿Por qué?") que muestre la equivalencia.
- Mantener todos los textos, botones y explicaciones en español.
- Conservar intacta la estética visual (fondos, bordes, colores de acento) de la Fase 4 existente.

**Non-Goals:**
- No se creará un editor de geometrías para administradores. Las figuras se definen estáticamente en el seed.
- No se implementarán figuras circulares con subdivisiones no homogéneas (el `PizzaFractionVisualizer` existente ya cubre círculos simétricos).
- No se modificará el esquema de base de datos (tablas, columnas). Se reutiliza el campo JSON existente `datos_numericos`.
- No se modificará la lógica de progreso, pool de preguntas ni graduación existentes.

## Decisions

### 1. Representación de geometrías como polígonos SVG en `datos_numericos`

**Decisión**: Almacenar las coordenadas de cada sector como cadenas de puntos SVG (`points`) y su peso relativo (`weight`) dentro del campo JSON `datos_numericos`, bajo un nuevo `tipo_visual: "non_homogeneous_polygon"`.

**Alternativas consideradas**:
- **Canvas/Fabric.js** (ya existe `Fase4FabricVisualizer`): Descartado porque requiere inicialización pesada, no es declarativo, y el componente existente es para arrastrar figuras, no para colorear áreas.
- **Imágenes estáticas con mapa de áreas HTML**: Descartado por no escalar a diferentes resoluciones, duplicar almacenamiento y limitar la variación dinámica de preguntas.

**Rationale**: SVG es declarativo, responsivo (via `viewBox`), ligero en memoria, y permite interactividad nativa con eventos `onClick` por polígono. El campo JSON existente absorbe el nuevo esquema sin migración de BD.

### 2. Validación por suma de pesos decimales con tolerancia

**Decisión**: En el endpoint `/responder`, cuando el tipo sea `non_homogeneous_polygon`, el frontend enviará una lista de IDs de sectores seleccionados en `respuesta_dada` (formato: `"1,3,5"`). El backend recuperará los pesos de `datos_numericos.sectors`, sumará los `weight` de los IDs recibidos, y comparará contra `target_value` con tolerancia `abs(suma - target) < 0.001`.

**Alternativas consideradas**:
- **Validar en el frontend y enviar solo correcto/incorrecto**: Descartado porque permite trampas del lado del cliente.
- **Almacenar todas las combinaciones válidas en `respuesta_correcta`**: Descartado porque el número de combinaciones válidas crece exponencialmente con el número de sectores.

**Rationale**: La suma de pesos es O(n) con n = número de sectores (máximo ~10), es determinista y no requiere almacenar combinaciones.

### 3. Variación dinámica de preguntas (mismo asset, distinto target)

**Decisión**: En `seed.py`, una misma definición de `sectors` (geometría base) se reutilizará en múltiples registros de `Pregunta` con diferentes valores de `target_value` y `target_fraction_text`. Ejemplo: la misma grilla de rectángulos genera preguntas para 1/3, 2/3, 1/6, 50%, etc.

**Rationale**: Maximiza la densidad de preguntas sin aumentar la complejidad del código ni el tamaño del seed. El alumno percibe variedad aunque la figura sea la misma.

### 4. Feedback visual de simplificación en modal

**Decisión**: Cuando el alumno responde correctamente y presiona "¿Por qué?", se abrirá un modal (`Fase4MirrorModal.tsx` existente o nueva sección) que muestra dos SVGs lado a lado: la figura original coloreada y una versión simplificada donde los bordes internos de sectores adyacentes coloreados se ocultan (cambiando `stroke` al color de relleno).

**Rationale**: La transformación visual de "fusionar piezas" demuestra intuitivamente la equivalencia fraccionaria sin necesidad de explicaciones textuales complejas.

### 5. Reutilización del flujo de respuesta existente

**Decisión**: No se crea un endpoint nuevo. Se extiende la lógica del endpoint `/responder` existente con una rama condicional que detecta `tipo_visual == "non_homogeneous_polygon"` en los `datos_numericos` de la pregunta.

**Rationale**: Mantiene la API consistente. El frontend solo necesita enviar `respuesta_dada` con el formato de IDs separados por coma.

## Risks / Trade-offs

- **Precisión de punto flotante** → Mitigación: Usar tolerancia de `0.001` en la comparación y definir pesos como fracciones exactas con denominadores potencia de 2 o decimales finitos (0.125, 0.25, 0.5, 0.333).
- **Complejidad de las coordenadas SVG en el seed** → Mitigación: Crear funciones generadoras (`_build_rectangle_grid`, `_build_triangle_split`) que calculen automáticamente los puntos y pesos a partir de parámetros simples (filas, columnas, divisiones).
- **Rendimiento SVG en dispositivos móviles** → Mitigación: Las figuras tendrán máximo 10-12 polígonos, lo cual es trivial para cualquier renderizador SVG moderno.
- **Alumno no entiende que debe hacer clic** → Mitigación: Incluir instrucción visual animada ("Toca las piezas para colorearlas") y efecto hover/pulse en los sectores.
