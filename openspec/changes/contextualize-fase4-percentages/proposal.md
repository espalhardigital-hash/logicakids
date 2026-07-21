## Why

El aprendizaje de fracciones de cantidad y porcentajes se asimila mucho mejor cuando los niños descubren activamente la relación visual entre las partes y el todo. Actualmente, la teoría de los Módulos 2 (Fracción de Cantidad) y 3 (Porcentajes) usa imágenes estáticas o preguntas directas en texto. Las imágenes analizadas proponen una mecánica interactiva visual poderosa donde el niño completa la fracción equivalente (`[numerador] / [denominador]`) y ve la porción exacta iluminada sobre un total dado. Incorporar esto mejorará drásticamente la asimilación conceptual.

## What

El objetivo es integrar un nuevo visualizador interactivo de Fracción en la Fase 4, impactando específicamente al **Módulo 2 (Fracción de Cantidad)** y **Módulo 3 (Porcentajes)**:
1. **Nuevo Visualizador (`FractionPercentageVisualizer`)**: Un componente donde el usuario visualiza una barra segmentada (representando el total) y debe armar la ecuación de la fracción (`[ ] / [ ] x Total`) seleccionando de un banco de números interactivos.
2. **Mejora de la Teoría**: Reemplazar los recursos estáticos en la teoría de los niveles iniciales de ambos módulos por este widget interactivo, permitiendo al niño explorar visualmente.
3. **Mejora de las Preguntas**: Ampliar las semillas (`seed.py`) de los niveles correspondientes para usar este visualizador contextual:
   - **Módulo 2 (Nivel 1 y 2)**: Usar el visualizador para representar el problema de "Calcula m/n de Y".
   - **Módulo 3 (Nivel 1)**: Usar el visualizador para ayudar a traducir porcentajes (20%, 25%, 40%, 50%, 60%, 75%, 80%) a su equivalente en fracción y resolverlo visualmente.

## Out of Scope

- No se crearán niveles nuevos (Nivel 5 u otros). Todo se integrará en las mecánicas de los niveles existentes de la Fase 4.
- No se implementarán visualizadores 2D complejos (como barras de chocolate o cuadrículas 2D), nos mantendremos con barras 1D limpias y minimalistas enfocadas en la fracción y el cálculo matemático.
