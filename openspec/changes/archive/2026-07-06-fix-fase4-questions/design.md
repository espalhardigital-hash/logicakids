## Context

La Fase 4 de LogicaKids enseña fracciones, porcentajes, promedios y razones a niños. Las preguntas se generan algorítmicamente en `LogicaMath/backend/app/fase4/seed.py` usando generadores determinísticos con semilla (`random.Random(seed)`). Actualmente el sistema produce:

- **Práctica Libre**: 4 módulos × (3-4 niveles) × 15 familias × 4 variantes = **780 preguntas** de práctica.
- **Desafíos**: 4 módulos × 3 desafíos × 30 preguntas = **360 preguntas** de desafío.

El problema es que la diversidad percibida es muy baja. Los diccionarios de contexto son pequeños (8 nombres, 5 objetos, 4 bebidas), las variantes "espejo" no alteran los valores numéricos, y los rangos de cálculo son estrechos. Además, algunas preguntas dependen visualmente de componentes interactivos (`pizza`, `beaker`, `pie`) que no siempre se renderizan.

Archivo principal afectado: [seed.py](file:///d:/Antigravity/APP_Logica_Matematicas_kids/LogicaMath/backend/app/fase4/seed.py)

## Goals / Non-Goals

**Goals:**
- Aumentar significativamente la diversidad percibida de preguntas sin cambiar la arquitectura del generador.
- Hacer que las 4 variantes de cada familia produzcan problemas matemáticamente distintos.
- Agregar enunciados de texto autoexplicativos como fallback para preguntas interactivas.
- Ampliar los rangos numéricos manteniendo cálculos apropiados para niños de 8-12 años.
- Mantener la determinismo de las semillas (`random.Random(seed)`) para reproducibilidad.

**Non-Goals:**
- No se cambiará la arquitectura del generador (familias × variantes con semilla determinística).
- No se modificará el esquema de base de datos ni los modelos SQLAlchemy.
- No se modificará el Frontend ni el router de la Fase 4.
- No se cambiará la estructura de módulos/niveles/desafíos (4 módulos, 13 niveles de práctica, 12 desafíos).
- No se abordarán bugs de renderizado del Frontend en esta iteración.

## Decisions

### D1: Expandir diccionarios in-place vs. archivo externo JSON

**Decisión**: Expandir los diccionarios directamente en `seed.py` como listas Python.

**Alternativa considerada**: Mover los diccionarios a un archivo JSON externo (`data/fase4_vocabulario.json`).

**Razón**: El archivo `seed.py` es autocontenido y se ejecuta como script independiente. Agregar una dependencia de archivo externo complicaría el seed sin beneficio real, ya que estos diccionarios solo se usan aquí. Además, mantener todo en un archivo facilita la revisión y el debug.

### D2: Variantes espejo — alterar semilla vs. alterar parámetros

**Decisión**: Alterar la semilla RNG de cada variante para que produzca valores numéricos diferentes, además de aplicar transformaciones lógicas específicas por módulo (invertir fracción, cambiar operación complementaria, escalar totales).

**Alternativa considerada**: Solo cambiar la semilla sin transformaciones lógicas adicionales.

**Razón**: Cambiar solo la semilla produce variaciones, pero puede generar dos preguntas con los mismos valores por coincidencia. Aplicar transformaciones adicionales (ej: si la variante original pide "qué fracción hay pintada", la variante espejo pide "qué fracción NO está pintada") garantiza diversidad pedagógica además de numérica.

### D3: Rangos numéricos — conservadores vs. amplios

**Decisión**: Ampliación moderada. Denominadores `[2, 3, 4, 5, 6, 8, 10, 12]`, multiplicadores `[2..12]`, totales que permitan divisiones exactas hasta ~120.

**Alternativa considerada**: Ampliación agresiva (denominadores hasta 20, totales hasta 500).

**Razón**: Los alumnos objetivo tienen 8-12 años. Denominadores mayores a 12 o totales mayores a ~120 generan cálculos mentales que exceden la capacidad de la mayoría. Mantener divisibilidad exacta (sin decimales) es obligatorio.

### D4: Fallback textual para preguntas interactivas

**Decisión**: Agregar un texto descriptivo complementario al enunciado interactivo que explique la tarea sin depender del gráfico. El campo `enunciado` incluirá el contexto completo.

**Alternativa considerada**: Crear un campo nuevo `enunciado_fallback`.

**Razón**: Agregar un campo nuevo requiere migración de esquema. Es más simple y robusto hacer que el enunciado existente sea autoexplicativo por sí solo, tratando el componente visual como un complemento enriquecedor y no como un requisito.

## Risks / Trade-offs

- **[Re-seed obligatorio]** → Todo cambio en el generador invalida las preguntas existentes. Se debe ejecutar `clear_fase4_data()` + `run_fase4_seed()` tras cada modificación. **Mitigación**: El sistema ya maneja esto con el script de seed. En desarrollo local no hay impacto en usuarios reales.

- **[Determinismo de semillas]** → Cambiar la fórmula de la semilla altera TODAS las preguntas generadas, no solo las variantes. **Mitigación**: Las semillas de variantes espejo (var > 0) usarán un offset adicional (`seed + var * 7919`) para preservar la compatibilidad de la variante original (var=0).

- **[Complejidad de enunciados]** → Enunciados más largos con fallback textual pueden ser menos legibles para niños. **Mitigación**: El texto fallback será una oración corta y complementaria, no un párrafo extenso.
