## Context

Actualmente, el aprendizaje de **Fracción de Cantidad (Módulo 2)** y **Porcentajes Rápidos (Módulo 3)** en la Fase 4 de LogicaMath utiliza metáforas genéricas y una teoría basada en explicaciones de texto con imágenes SVG estáticas limitadas. Las imágenes provistas (con el visualizador de barra segmentada y ecuación de fracción interactiva) demuestran que el estudiante asimila mejor cuando él mismo ensambla la fracción y ve el efecto en un contexto visual. 

## Goals / Non-Goals

**Goals:**
- Implementar un visualizador de ecuaciones interactivo (`FractionPercentageVisualizer`) en el frontend donde el niño seleccione el numerador y denominador correctos (o los asigne) para observar la porción del total iluminada.
- Integrar este componente interactivo en la sección de **Teoría** de la Fase 4 para el **Módulo 2 (Nivel 1 y 2)** y el **Módulo 3 (Nivel 1)** reemplazando gráficos estáticos.
- Integrar este componente en las **Preguntas** de la Fase 4:
  - En Módulo 2 para calcular `m/n de Total`.
  - En Módulo 3 para calcular porcentajes (20%, 40%, 50%, 60%, 75%, etc.) mediante su fracción equivalente.

**Non-Goals:**
- No se crearán niveles nuevos. Se mejorarán las mecánicas y los componentes de los niveles y teorías ya existentes.
- No se usarán animaciones complejas 3D ni drag and drop (DND) problemático; se priorizará un diseño responsivo de "click-to-select" (clic en número, clic en caja) por simplicidad y robustez, o el uso de inputs numéricos nativos amigables.

## Decisions

1. **Componente Visualizador Compartido:**
   - *Decisión*: Crear `FractionPercentageVisualizer` como un nuevo componente React que sirva tanto para fracciones puras como para porcentajes. Agregaremos el `tipo_visual: 'fraction_percentage'` en `Fase4Types.ts`.
   - *Razón*: La lógica subyacente (armar un numerador y denominador para aplicar a un total y graficar la porción en una barra) es idéntica en Fracciones de Cantidad (M2) y Porcentajes Equivalentes (M3).
2. **Mecánica de Selección (Click-to-Select):**
   - *Decisión*: Implementar una interfaz tipo banco de números o ruleta táctil interactiva. El usuario selecciona el numerador y denominador visualmente antes de resolver el total.
   - *Razón*: Asegura accesibilidad en tabletas sin necesidad de arrastrar elementos en pantallas táctiles.
3. **Inyección Híbrida en Backend:**
   - *Decisión*: Modificaremos `fase4/theory_examples.py` y `fase4/seed.py` (Módulos 2 y 3) para devolver `tipo_visual: 'fraction_percentage'`.
   - *Razón*: Se reutiliza un único desarrollo de interfaz para revolucionar visualmente dos módulos enteros de la Fase 4.

## Risks / Trade-offs

- **[Risk]** Sobrecargar la memoria cognitiva de los estudiantes con demasiados pasos interactivos por pregunta.
  - *Mitigación*: Se calibrarán los niveles; en preguntas iniciales o de teoría, la fracción puede estar pre-armada o tener asistencia muy clara.
