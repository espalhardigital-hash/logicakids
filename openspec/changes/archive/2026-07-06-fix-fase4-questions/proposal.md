## Why

El generador de preguntas de la Fase 4 (`seed.py`) produce preguntas que se repiten con altísima frecuencia y algunas aparecen "vacías" en la interfaz. Esto degrada la experiencia del alumno y reduce la eficacia pedagógica. Las causas raíz son: diccionarios de contexto con solo 8 nombres y 5 objetos, variantes "espejo" que replican la pregunta original sin cambiar los números, rangos numéricos demasiado estrechos, y enunciados que dependen de componentes visuales interactivos que el Frontend no siempre renderiza correctamente.

## What Changes

- **Ampliar diccionarios de contexto**: Expandir las listas `NOMBRES`, `OBJETOS_FRACC`, `COLECCIONES`, `BEBIDAS`, `PINTURAS` y `COLORES` de ~8 elementos a ~25+ cada una, incorporando vocabulario infantil diverso y culturalmente variado.
- **Corregir variantes espejo**: Rediseñar la lógica de generación de variantes (`var > 0`) para que cada variante altere los valores numéricos (denominadores, multiplicadores, totales), no solo el prefijo `[ESPEJO]`. Garantizar que las 4 variantes de cada familia produzcan problemas matemáticamente distintos.
- **Ampliar rangos numéricos**: Expandir los conjuntos de denominadores, multiplicadores y totales para crear más permutaciones únicas, manteniendo la dificultad apropiada para niños.
- **Mejorar enunciados de preguntas interactivas**: Asegurar que las preguntas que requieren componentes visuales (`pizza`, `beaker`, `pie`) incluyan un enunciado de texto alternativo autoexplicativo que funcione incluso si el gráfico no se renderiza.
- **Diversificar desafíos Módulo 3**: Actualmente los desafíos del módulo 3 alternan rígidamente entre porcentajes (índices pares) y promedios (índices impares). Incluir también preguntas de gráficos circulares y barras en el pool de desafíos.

## Capabilities

### New Capabilities
- `fase4-question-diversity`: Lógica de diversificación del generador de preguntas de la Fase 4 incluyendo vocabularios extendidos, variantes numéricas reales, rangos ampliados y enunciados con fallback textual.

### Modified Capabilities
- `gameplay-fase4-multiple-opcion`: Los desafíos de múltiple opción se beneficiarán de mayor variedad en sus alternativas y distractores al tener más permutaciones numéricas disponibles.

## Impact

- **Backend**: `LogicaMath/backend/app/fase4/seed.py` — Cambios significativos en diccionarios, función `generate_practice_question_fase4()` y `generate_challenge_question_fase4()`.
- **Base de datos**: Requiere re-seed completo de las preguntas de Fase 4 (`clear_fase4_data` + `run_fase4_seed`). No hay cambios de esquema.
- **Frontend**: No requiere cambios estructurales, pero se beneficiará de enunciados más autoexplicativos que reduzcan la dependencia de componentes visuales.
- **Compatibilidad**: Sin cambios breaking. El progreso de alumnos existentes en Fase 4 se reseteará al hacer re-seed (comportamiento esperado en desarrollo).
