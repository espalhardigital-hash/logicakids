# Análisis de Integración: Fracciones y Porcentajes en Áreas No Homogéneas (Fase 4)

Este documento sirve como especificación de requerimientos técnicos y pedagógicos para la incorporación de desafíos de fracciones y porcentajes sobre polígonos interactivos de áreas no homogéneas en la **Fase 4** de la aplicación.

---

## 1. Justificación Pedagógica

Los ejercicios tradicionales de fracciones se basan en particiones homogéneas (por ejemplo, un círculo dividido en 4 sectores circulares idénticos). Esto permite al alumno resolver los problemas de manera mecánica contando partes pintadas sobre el total de partes.

La incorporación de **figuras con áreas no homogéneas** (asimétricas) aporta las siguientes ventajas:
* **Comprensión Conceptual Profunda**: Obliga al alumno a analizar el peso o área relativa de cada sector, en lugar de realizar un conteo visual simple.
* **Equivalencia Práctica**: Fomenta el entendimiento intuitivo de que diferentes porciones combinadas pueden sumar un mismo valor total (por ejemplo, que colorear \(\frac{1}{2}\) equivale a colorear \(\frac{1}{5} + \frac{1}{5} + \frac{1}{10}\)).
* **Resolución Multicamino**: Ofrece varias soluciones correctas para una misma pregunta, estimulando el pensamiento matemático flexible y creativo.

---

## 2. Nuevos Conceptos Pedagógicos y Visuales Detectados

A partir del análisis de las variaciones del triángulo asimétrico complejo, se incorporan dos conceptos de alto valor pedagógico a la especificación:

### A. Asimetría Lateral Controlada (Fragmentado vs. Consolidado)
En la figura del triángulo, el lado izquierdo y el lado derecho no están divididos de la misma manera:
* El **lado izquierdo** está altamente fragmentado (dividido en 4 sub-piezas pequeñas de \(\frac{1}{8}\) cada una).
* El **lado derecho** está consolidado (dividido en 2 sub-piezas de \(\frac{1}{8}\) y 1 pieza grande de \(\frac{1}{4}\) en la esquina inferior).
* **Valor Pedagógico**: Este desequilibrio visual controlado ayuda al alumno a entender que un mismo espacio o área puede presentarse en una sola pieza compacta o fragmentado en partes más pequeñas. Le entrena para "descomponer y componer" áreas mentalmente.

### B. Fracciones No Simplificadas como Reto Adicional
El sistema puede alternar enunciados que piden colorear fracciones simplificadas y no simplificadas sobre el mismo objeto:
* Por ejemplo, preguntar **"Colorea 2/4 del triángulo"** en lugar de "Colorea 1/2".
* **Valor Pedagógico**: Introduce un desafío de doble capa. El estudiante debe realizar primero una simplificación matemática mental (\(\frac{2}{4} = \frac{1}{2}\)) y posteriormente encontrar la combinación de áreas físicas que sumen esa mitad.

### C. Línea de Simetría Central como Guía Implícita
La inclusión de una línea vertical (mediana/altura) que divide longitudinalmente al triángulo facilita una referencia visual de "mitades":
* El alumno sabe visualmente que todo lo que esté a la izquierda de la línea representa exactamente la mitad (\(\frac{1}{2}\) o \(\frac{2}{4}\)), y todo lo que esté a la derecha representa la otra mitad, a pesar de que las formas internas sean asimétricas en cada lado.

---

## 3. Ubicación en la Estructura de la Fase 4

Este concepto se integrará en dos partes clave de la Fase 4:

1. **Módulo 1 (La Fracción Visual) - Nivel 3 (Áreas y Asimetrías)**:
   * **Propósito**: Evaluar la habilidad del alumno para identificar y sombrear fracciones sobre áreas asimétricas.
   * **Contexto**: Amplía y materializa el concepto del Nivel 3 (cuya teoría actual ya advierte sobre la diferencia de áreas pero carecía de un componente de coloreado asimétrico dinámico).
2. **Módulo 3 (Porcentajes Rápidos)**:
   * **Propósito**: Utilizar las mismas figuras vectoriales para pedir sombreados basados en porcentajes (por ejemplo, "Colorea el 50% de la figura").
   * **Contexto**: Refuerza la relación de equivalencia entre fracciones y porcentajes de manera visual.

---

## 4. Catálogo de Geometrías y Subdivisiones Analizadas

### A. Rectángulos con Subdivisiones Horizontales y Verticales
* **Configuración 1 (Mitad y Cuartos)**: Un rectángulo dividido en una sección de \(\frac{1}{2}\) (mitad superior) y dos secciones de \(\frac{1}{4}\) (mitad inferior dividida verticalmente).
* **Configuración 2 (Filas y Décimos)**: Un rectángulo dividido en 5 filas iguales (peso \(\frac{1}{5}\) cada una). Las filas 2 y 4 están divididas por la mitad verticalmente, creando sub-sectores de peso \(\frac{1}{10}\).
* **Configuración 3 (Columnas y Sextos)**: Un rectángulo dividido en 3 columnas iguales (peso \(\frac{1}{3}\) cada una). Las columnas 1 y 2 están divididas por la mitad horizontalmente, creando sub-sectores de peso \(\frac{1}{6}\).

### B. Triángulos Equiláteros/Isósceles
* **Configuración 1 (Subdivisión por Medianas)**: Un triángulo dividido por sus tres medianas en 6 secciones congruentes de peso \(\frac{1}{6}\) cada una.
* **Configuración 2 (Subdivisión por Puntos Medios)**: Un triángulo dividido en 4 triángulos interiores iguales (peso \(\frac{1}{4}\) cada uno).
* **Configuración 3 (Subdivisión Asimétrica Compleja con División Central)**: Un triángulo dividido en:
  * 2 triángulos superiores (peso \(\frac{1}{8}\) cada uno, divididos por una línea central vertical).
  * 2 triángulos en el centro invertido (peso \(\frac{1}{8}\) cada uno, divididos verticalmente).
  * 2 celdas de \(\frac{1}{8}\) en la esquina inferior izquierda.
  * 1 pieza compacta de \(\frac{1}{4}\) (o \(\frac{2}{8}\)) en la esquina inferior derecha.

---

## 5. Requerimientos de Idioma e Interfaz (100% Español)

Para mantener la consistencia con el resto de la aplicación y facilitar el aprendizaje del alumno, todos los textos, instrucciones, botones y explicaciones deben estar estrictamente en **español**:

* **Botones del Juego**:
  * `Check` $\rightarrow$ **"Comprobar"**
  * `Why?` $\rightarrow$ **"¿Por qué?"**
  * `Continue` $\rightarrow$ **"Continuar"**
  * `Start over` $\rightarrow$ **"Reiniciar"** (o "Volver a empezar")
* **Enunciados de Pregunta**:
  * "Color 1/2 of the shape." $\rightarrow$ **"Colorea 1/2 de la figura."**
  * "Color 1/4 of the triangle." $\rightarrow$ **"Colorea 1/4 del triángulo."**
  * "Color 2/4 of the triangle." $\rightarrow$ **"Colorea 2/4 del triángulo."**
  * "Color 25% of the shape." $\rightarrow$ **"Colorea el 25% de la figura."**
* **Explicaciones de Feedback ("¿Por qué?")**:
  * Todas las deducciones matemáticas de equivalencias y descripciones de porciones se redactarán de forma amigable y didáctica en español.

---

## 6. Diseño de la Interfaz y Respeto a la Estética de Fase 4

Se conservará en su totalidad la dirección de arte y los colores del tema oscuro actual de la Fase 4 para evitar inconsistencias en la UX:

* **Colores de Fondo y Contenedores**:
  * Se mantendrá el fondo de la pantalla de juego de Fase 4 (`bg-zinc-950` / `#09090b`) y las tarjetas principales (`bg-zinc-900` / `#18181b` con bordes sutiles `border-zinc-800`).
* **Lienzo Central de Juego (Cambio de Figura)**:
  * Solo se reemplaza el área interactiva central donde antes se renderizaba la pizza o las barras tradicionales.
  * El nuevo visualizador dinámico de polígonos dibujará las figuras usando el mismo estilo de líneas de contorno blancas (`stroke="#ffffff"`) y relleno inicial en gris oscuro para los sectores sin colorear.
  * Al hacer clic en un sector, se sombreará usando el color de acento azul oficial de la Fase 4.

---

## 7. Diseño de la Arquitectura Técnica

### A. Representación de Datos en Base de Datos (Backend)
Las preguntas usarán un nuevo tipo visual en `preguntas.datos_numericos` llamado **`non_homogeneous_polygon`**. 

El JSON de la pregunta define el valor decimal objetivo (`target_value`), las coordenadas de cada sector (`points`) y el peso relativo de cada parte (`weight` de 0 a 1.0).

**Ejemplo de JSON para el triángulo asimétrico complejo con división central (4.B.3):**
```json
{
  "tipo_visual": "non_homogeneous_polygon",
  "target_value": 0.25,
  "target_fraction_text": "2/4",
  "viewBox": "0 0 100 100",
  "sectors": [
    { "id": 1, "weight": 0.125, "points": "50,0 50,50 25,50", "label": "Sup Izq" },
    { "id": 2, "weight": 0.125, "points": "50,0 50,50 75,50", "label": "Sup Der" },
    { "id": 3, "weight": 0.125, "points": "50,50 50,100 25,50", "label": "Centro Inv Izq" },
    { "id": 4, "weight": 0.125, "points": "50,50 50,100 75,50", "label": "Centro Inv Der" },
    { "id": 5, "weight": 0.125, "points": "25,50 0,100 25,100", "label": "Inf Izq Ext" },
    { "id": 6, "weight": 0.125, "points": "25,50 25,100 50,100", "label": "Inf Izq Int" },
    { "id": 7, "weight": 0.250, "points": "75,50 75,100 100,100", "label": "Inf Der Consolidad" }
  ]
}
```

### B. Validación en el Servidor (Backend)
Al presionar "Comprobar", el frontend envía una lista de los IDs coloreados (ej: `[1, 3]`). 

El backend en el endpoint `/responder` de la Fase 4:
1. Recupera la configuración de `datos_numericos` de la pregunta.
2. Suma los valores de `weight` de los sectores seleccionados por el alumno.
3. Si la suma total coincide con `target_value` (con tolerancia mínima flotante de `0.001`), la respuesta se evalúa como correcta.

### C. Visualizador Interactivo de Polígonos (Frontend)
Se creará el componente React **`Fase4NonHomogeneousPolygon.tsx`** bajo la carpeta `components/fase4/`.

* **Renderizado**: SVG con elementos `<polygon>` usando los puntos normalizados.
* **Interactividad**: Evento `onClick` que realiza un toggle del ID del sector en el estado local de seleccionados.
* **Estilo**:
  * Fondos de celdas vacías en gris oscuro (`fill="#27272a"` o similar).
  * Bordes blancos limpios y nítidos (`stroke="#ffffff"`, `strokeWidth={1.5}`) para definir la geometría.
  * Relleno interactivo en azul eléctrico (`fill="#3b82f6"`) al ser seleccionado.
  * Animaciones de hover suaves (`transition-all duration-200 hover:opacity-80`).

---

## 8. Dinámica de Variación de Preguntas (Eficiencia del Asset)

Para optimizar al máximo el desarrollo y no saturar el banco de datos, se aplicará el principio de **variación dinámica**:
* A partir de un mismo diseño vectorial, se pueden generar múltiples preguntas:
  * "Colorea 1/4 del triángulo" $\rightarrow$ `target_value: 0.25`
  * "Colorea 2/4 del triángulo" $\rightarrow$ `target_value: 0.50`
  * "Colorea 3/4 del triángulo" $\rightarrow$ `target_value: 0.75`
* Esto permite multiplicar la densidad de práctica del alumno sin necesidad de añadir código ni archivos gráficos nuevos.

---

## 9. Simplificación Visual en el Feedback ("¿Por qué?")

El modal explicativo activado por el botón **"¿Por qué?"** proporcionará una demostración intuitiva de la equivalencia. 

Se implementará una **"vista de simplificación"** comparativa:
* El modal mostrará dos figuras lado a lado:
  1. **Figura original**: Con los sectores asimétricos coloreados por el alumno.
  2. **Figura simplificada (consolidada)**: Donde las líneas divisorias internas de los sectores seleccionados adyacentes se desvanecen (cambiando su borde `stroke` al mismo color de relleno azul), transformando visualmente la composición irregular en bloques uniformes (ej: mostrando cómo las piezas se funden para representar exactamente la mitad o una porción representativa).
* Todo el texto explicativo de la transformación y equivalencia se redactará en español.
