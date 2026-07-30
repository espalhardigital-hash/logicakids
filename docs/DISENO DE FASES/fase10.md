# 🧩 FASE 10: LÓGICA COMPLEJA, RAZONAMIENTO ABSTRACTO Y BALANZAS

**Propósito:** Desarrollar el razonamiento lógico-deductivo avanzado, la deducción de equivalencias implícitas en balanzas, las relaciones de parentesco, secuencias abstractas y la resolución de acertijos matriciales sin depender exclusivamente del cálculo aritmético.

---

## 1. Propósito Pedagógico

* **Objetivo General**: Entrenar la deducción formal y el pensamiento algebraico abstracto en niños, desarrollando habilidades para resolver acertijos de balanzas en equilibrio, patrones visuales complejos, verdad/mentira y deducción de relaciones.

### 1.1. Estructura de Módulos y Niveles

| Módulo | Nivel 1: Descubrimiento | Nivel 2: Consolidación | Nivel 3: Fluidez (Integración) |
| :--- | :--- | :--- | :--- |
| **1. Acertijos de Balanzas y Pesos** | **1.1 Balanzas de Platillos**: Deducción de equivalencias simples entre formas geométricas. | **1.2 Sistemas de Balanzas Cruzadas**: Sustitución de variables entre 2 o más balanzas. | **1.3 Peso Faltante**: Determinación del objeto necesario para equilibrar una balanza final. |
| **2. Secuencias Abstractas y Patrones** | **2.1 Matrices de Figuras 3x3**: Rotación, traslación y cambio de forma en grillas. | **2.2 Patrones de Cuentas y Colores**: Deducción del elemento en la posición N (operatoria modular). | **2.3 Secuencias Numéricas Complejas**: Sucesiones dobles e intercaladas. |
| **3. Deducción Lógica y Verdad/Mentira** | **3.1 Declaraciones Contradictorias**: Detección del único culpable o mentiroso en un grupo. | **3.2 Parentescos y Árboles Familiares**: Ordenamiento de lazos familiares ("El padre del hijo de mi hermano..."). | **3.3 Ordenamiento de Posiciones**: Deducción de puestos en carreras o filas según pistas fragmentadas. |
| **4. Rompecabezas Topológicos y Redes** | **4.1 Grafos y Recorridos**: Trazado de figuras de un solo trazo (Eulerian paths). | **4.2 Cubos Desplegados Avanzados**: Identificación del cubo correcto entre alternativas giradas. | **4.3 Laberintos de Coordenadas Lógicas**: Navegación condicionada por reglas formales. |

---

## 2. Pautas de Diseño de la Interfaz Visual

### 2.1. El Simulador de Balanzas Interactivas (`balance-scale`)
* **Visualizador**: Dos platillos vectoriales neón apoyados en un eje central balanceado.
* **Interactividad**: Los niños pueden arrastrar figuras (círculos, triángulos, estrellas) hacia los platillos para simular el peso y observar cómo bascula el platillo en tiempo real.

### 2.2. La Matriz de Deducción 3x3 (`matrix-puzzle`)
* **Visualizador**: Rejilla de 9 celdas con 8 figuras y una celda con signo de interrogación `?`.
* **Interactividad**: Opciones visuales con botones de rotación para previsualizar la figura seleccionada antes de confirmar.

---

## 3. Modelo TJS y Evaluación

* **Desafío 1 (Estándar):** Preguntas de deducción lógica directa con opciones múltiples.
* **Desafío 2 (Avanzado):** Sistemas de balanzas complejas con 3 variables.
* **Desafío Final (Maestría):** Resolución por texto/entrada directa de acertijos complejos con criterio de aprobación del **90%**.
