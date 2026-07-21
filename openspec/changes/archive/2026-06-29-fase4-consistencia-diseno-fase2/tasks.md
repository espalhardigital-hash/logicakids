## 1. Ajuste de Apoyo Visual en la Fase 4

- [x] 1.1 Modificar `Fase4GameScreen.tsx` para detectar cuándo una pregunta es sobre colecciones discretas u objetos (figuritas, cartas, tazos, etc.).
- [x] 1.2 **Test de Verificación 1.1:** Ejecutar simulaciones del flujo o añadir logs de verificación en consola para comprobar que la lógica de detección de colecciones discretas clasifica correctamente las preguntas de la Fase 4 Módulo 2.
- [x] 1.3 Ocultar o condicionar el renderizado del visualizador de vaso graduado (`BeakerVisualizer` / *beaker*) en `Fase4GameScreen.tsx` para preguntas de colecciones discretas.
- [x] 1.4 **Test de Verificación 1.3:** Comprobar visualmente mediante el simulador de estudiantes que el vaso graduado ya no se muestra al cargar preguntas de colecciones discretas, pero sí sigue apareciendo en preguntas continuas (de volumen/líquidos).

## 2. Unificación del Bucle Espejo en la Fase 4

- [x] 2.1 Crear el componente `Fase4MirrorModal.tsx` en `LogicaMath/frontend/components/fase4/` adaptando la estructura, estilos, textos y animaciones de `Fase2MirrorModal.tsx`.
- [x] 2.2 **Test de Verificación 2.1:** Compilar el frontend localmente y validar que el componente `Fase4MirrorModal` no contenga errores de sintaxis, tipos o de importaciones.
- [x] 2.3 Reemplazar la alerta inline de Bucle Espejo en `Fase4GameScreen.tsx` por la renderización del modal superpuesto de pantalla completa `Fase4MirrorModal.tsx`.
- [x] 2.4 **Test de Verificación 2.3:** Comprobar mediante renderizado de prueba que al activarse el Bucle Espejo se lance el modal superpuesto en pantalla completa y bloquee correctamente la interacción con el tablero principal de fondo.
- [x] 2.5 Conectar los estados `showMirrorModal`, `mirrorPregunta` y los datos de la última respuesta fallida en `Fase4GameScreen.tsx` para emular el flujo de rescate de la Fase 2.
- [x] 2.6 **Test de Verificación 2.5:** Realizar un ciclo de error completo en la Fase 4 para verificar que la activación del Bucle Espejo carga la pregunta espejo en el modal, muestra la respuesta fallida anterior y permite responder o continuar tras el acierto.

## 3. Auditoría y Corrección en Fases Posteriores

- [x] 3.1 Auditar la Fase 3 (`Fase3GameScreen.tsx`) para asegurar consistencia del Bucle Espejo y verificar si utiliza algún apoyo visual de vaso graduado de forma inconsistente.
- [x] 3.2 **Test de Verificación 3.1:** Documentar hallazgos de la Fase 3 y, si es necesario, aplicar y probar los mismos ajustes de modal de espejo e imágenes.
- [x] 3.3 Inspeccionar `Fase5GameScreen.tsx`, `Fase6GameScreen.tsx`, `Fase7GameScreen.tsx` y `Fase8GameScreen.tsx` para asegurar que implementan correctamente el patrón de Bucle Espejo de pantalla completa.
- [x] 3.4 **Test de Verificación 3.3:** Simular errores consecutivos en cada una de las fases 5, 6, 7 y 8 para corroborar visualmente que el modal de espejo se activa según el patrón de la Fase 2.
- [x] 3.5 Revisar visualizadores en las fases 5 a 8 y corroborar que no se muestren gráficos de tipo "beaker" o barras en contextos no coherentes.
- [x] 3.6 **Test de Verificación 3.5:** Ejecutar pruebas de regresión visual en el panel de administración / simulador para validar que todas las fases (3 a 8) mantengan consistencia visual y de flujo.
