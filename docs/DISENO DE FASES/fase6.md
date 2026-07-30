# Especificación de Interfaz de Usuario: Fase 6 — Geometría Plana, Espacial y Medidas Físicas

Esta especificación detalla la arquitectura pedagógica, reglas de diseño visual y modelos interactivos para la **Fase 6 de LogicaKids Pro**, enfocada en dominar el espacio bidimensional y tridimensional: perímetros, áreas en malla cuadrillada, figuras compuestas (Tangram), cubos unitarios, volumen y magnitudes físicas.

---

## 1. Propósito Pedagógico

* **Objetivo General**: Dominar la conservación de la superficie, el cálculo de perímetros, la descomposición de polígonos complejos, el conteo de cubos unitarios en 3D (estética Voxel/Minecraft) y la lectura de magnitudes físicas (monto, masa, temperatura).

### 1.1. Estructura Completa de Módulos y Niveles

| Módulo | Nivel 1: Descubrimiento | Nivel 2: Consolidación | Nivel 3: Fluidez / Avanzado | Nivel 4: Especialización |
| :--- | :--- | :--- | :--- | :--- |
| **1. Reconocimiento 3D y Perímetros** | **1.1 Conteo directo**: Conteo directo sobre bordes de cuadrículas cuadradas simples. | **1.2 Cálculo analítico**: Perímetros sumando magnitudes de polígonos irregulares. | **1.3 Moldes 3D**: Identificación de poliedros y planificaciones desplegadas. | — |
| **2. Área en Malha y Patrones** | **2.1 Conteo analítico**: Conteo de unidades confinadas en cuadrículas densas. | **2.2 Fusión de sectores**: Fusión de sectores triangulares (mitades = enteros). | **2.3 Sucesiones 3D**: Patrones de crecimiento espacial en capas. | — |
| **3. Cubos Unitarios y Volumen** | **3.1 Concepto de volumen**: Conteo de cubos unitarios en prismas compactos (`u³`). | **3.2 Bloques ocultos**: Detección de bloques ocultos por perspectivas isométricas. | **3.3 Volumen y líquidos**: Relación entre volumen cúbico y capacidad (`1 dm³ = 1 L`). | — |
| **4. Figuras Compuestas y Medidas** | **4.1 Descomposición y Tangram**: Descomposición de polígonos y conservación del área. | **4.2 Áreas sombreadas**: Cálculo por resta geométrica (Área Mayor - Área Menor). | **4.3 Simetría y Medidas**: Ejes de simetría, balanzas y termómetros. | — |

---

## 2. Pautas de Diseño de la Interfaz Visual

### 2.1. El Tablero de Rejilla y Renderizador SVG Inline
* **Visualizador**: Rejilla neón dinámica renderizada en línea mediante SVG (`bd_minio §1.3`).
* **Interactividad**: Permite iluminar bordes para perímetros y rellenar cuadraditos para áreas.

### 2.2. Visualizador Isométrico 3D (Voxel / Minecraft)
* **Visualizador**: Escena isométrica de bloques 3D con sombras direccionales.
* **Interactividad**: Rotación en 360° y corte por capas horizontales para contar cubos ocultos.

---

## 3. Control de Cambios y Alineación

* **Actualización 2026-07-27:** Asignada la **Fase 6** oficialmente a **Geometría Plana, Espacial y Medidas Físicas**, consolidando perímetros, mallas, Tangram y cubos unitarios 3D.