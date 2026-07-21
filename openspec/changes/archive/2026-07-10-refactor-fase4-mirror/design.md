## Context
La Fase 4 maneja la interfaz de fracciones interactivas. El Bucle Espejo (modal de reintento) actual omite toda la renderización gráfica e impide la entrada de respuestas fraccionarias por falta de botones adecuados. Esto viola el principio fundamental de consistencia del Tomo 3 de la Guía UX de LogicaKids Pro.

## Goals / Non-Goals

**Goals:**
- Desacoplar el renderizado interactivo de la pantalla principal en un componente reutilizable.
- Soportar preguntas tipo `pizza`, `beaker`, `thermometer`, `bar_chart`, etc. en el Mirror Modal.
- Habilitar el teclado completo (`CustomKeyboard`) y entradas fraccionarias en el Modal Espejo.

**Non-Goals:**
- Modificar el sistema de evaluación del backend.
- Cambiar la lógica de Fase 2 o Fase 3.
- Modificar la forma en que se estructuran los tipos de la fase 4 (`Fase4Pregunta`).

## Decisions

1. **`Fase4VisualizerEngine`**: Se decidió extraer la lógica de renderizado hacia un nuevo componente puro en lugar de duplicar el código gigante del switch condicional.
   - *Rationale*: Previene bugs de inconsistencia si se añaden más visualizadores en el futuro (ej. balanza de porcentajes).
2. **Reemplazo por `<CustomKeyboard>`**: Se desechará el JSX hardcodeado.
   - *Rationale*: Fase 2 ya posee un componente global para teclados. Re-usarlo minimiza la deuda técnica.
3. **`activeInputField` en Espejo**: Imitar el estado de `Fase4GameScreen` de numerador y denominador.
   - *Rationale*: Evita que los usuarios de pantallas táctiles intenten insertar barras (/) desde el teclado nativo, respetando el bloqueo de distracciones del sistema.

## Risks / Trade-offs

- **[Risk]** Pérdida del estilo visual del modal actual.
  - **Mitigation:** El motor visualizador se montará en la mitad de la columna flex, manteniendo el diseño responsivo sin desbordar el contenedor modal.
- **[Risk]** Manejo de inputs del teclado afectando a ambos inputs.
  - **Mitigation:** Se implementará el selector condicional `activeInputField` ('num' o 'den') para rutear el evento del `CustomKeyboard` al field correcto, igual que en el juego principal.
