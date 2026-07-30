# Especificación de Interfaz de Usuario: Fase 5 — Operatoria Decimal y Conversiones

Esta especificación detalla la arquitectura pedagógica, reglas de diseño visual, modelo TJS e interfaz de interacción para la **Fase 5 de LogicaKids Pro**, enfocada en dominar la suma, resta, multiplicación y división de números decimales, así como la conversión de unidades métricas lineales y de superficie.

---

## 1. Propósito Pedagógico

* **Objetivo General**: Romper la limitación de los números enteros, dominando la representación decimal, la alineación de comas, la multiplicación/división decimal y las conversiones del sistema métrico decimal.

### 1.1. Estructura Completa de Módulos y Niveles

| Módulo | Nivel 1: Descubrimiento | Nivel 2: Consolidación | Nivel 3: Fluidez / Avanzado |
| :--- | :--- | :--- | :--- |
| **1. Suma y Resta de Decimales** | **1.1 Suma alineando la coma**: Alineación vertical de comas y ceros de relleno. | **1.2 Resta con prestados**: Resta de números decimales con desatado de unidades. | **1.3 Problemas de cambio**: Transacciones monetarias y cálculo de cambio. |
| **2. Multiplicación de Decimales** | **2.1 Multiplicación por 10, 100, 1000**: Desplazamiento directo de la coma decimal a la derecha. | **2.2 Decimal por entero**: Multiplicación de factores decimales por números naturales. | **2.3 Decimal por decimal**: Conteo acumulado de posiciones decimales en el producto. |
| **3. División con Decimales** | **3.1 División por entero**: Generación de decimales en el cociente. | **3.2 División entre decimales**: Eliminación del divisor decimal multiplicando por potencias de 10. | **3.3 Aproximación y redondeo**: Redondeo a décimas y centésimas más cercanas. |
| **4. Conversión de Unidades** | **4.1 Escalera métrica lineal**: Conversión directa entre `mm`, `cm`, `dm`, `m`, `dam`, `hm`, `km`. | **4.2 Escalera de superficie**: Conversión entre `mm²`, `cm²`, `m²` (factores de 100). | **4.3 Masa y capacidad**: Conversiones complejas de `g`, `kg`, `L`, `mL` e integración. |

### 1.2. Estructura de Evaluación y Maestría (Modelo TJS)

* **Desafío 1 (Estándar):** Opción múltiple con evaluación del alineamiento y operaciones con tiempo.
* **Desafío 2 (Avanzado):** Problemas narrativos complejos de cálculo monetario y conversión métrica.
* **Desafío Final (Maestría):** Resolución por respuesta numérica directa con un criterio de aprobación del **90%**.

---

## 2. Pautas de Diseño de la Interfaz Visual

### 2.1. El Alineador de Comas (`decimal-aligner`)
* **Visualizador**: Matriz en columna interactiva con separador vertical brillante para la coma decimal.
* **Interactividad**: Permite arrastrar dígitos y colocar ceros a la derecha de la parte decimal para igualar longitudes antes de operar.

### 2.2. La Escalera Métrica Interactiva
* **Visualizador**: Diagrama en peldaños interactivo que representa el Sistema Métrico Decimal.
* **Interactividad**: Al seleccionar la unidad de origen y destino, la escalera anima los saltos hacia arriba (división `:10`) o hacia abajo (multiplicación `x10`).

---

## 3. Estilo Visual y Feedback

* **Colores Neón por Módulo**:
  - Módulo 1 (Suma y Resta): Esmeralda Neón (`#10B981`)
  - Módulo 2 (Multiplicación): Violeta Neón (`#8B5CF6`)
  - Módulo 3 (División): Ámbar Neón (`#F59E0B`)
  - Módulo 4 (Conversión de Unidades): Rosa Neón (`#EC4899`)
* **Feedback Pedagógico (Bucle Espejo):** Si se detecta el error clásico de desalinear la coma o no sumar decimales correctamente, se activa la secuencia espejo con ayuda visual paso a paso.

---

## 4. Control de Cambios y Alineación

* **Actualización 2026-07-27:** Renombrados y reestructurados los módulos de la Fase 5 a **Operatoria Decimal y Conversiones** (separándola formalmente de Geometría que corresponde a Fase 6).
