## Context

El sistema cuenta con un Modo Evaluador en el panel de administración que permite a los evaluadores depurar el flujo de los juegos (por ejemplo, omitiendo preguntas). Sin embargo, carece de un canal estructurado dentro de la misma aplicación para reportar fallos de interfaz de usuario. Actualmente, la comunicación de bugs de UI/UX depende de capturas de pantalla manuales y descripciones en texto que a menudo carecen del contexto preciso de la fase, módulo, pregunta o selector de código donde reside el problema visual.

## Goals / Non-Goals

**Goals:**
- Proveer un mecanismo intuitivo de "apuntar y hacer clic" para dejar anotaciones sobre elementos visuales de la pantalla.
- Capturar automáticamente el contexto exacto (Fase, Módulo, Nivel, Pregunta, Selector CSS y estado React).
- Guardar las anotaciones en la base de datos PostgreSQL de desarrollo/pruebas.
- Mostrar una vista de administración dentro de la app para ver el listado de feedbacks.
- Facilitar la resolución por parte del desarrollador o de la IA de Antigravity mediante correlación directa con el código fuente.

**Non-Goals:**
- No se pretende que esta herramienta se exponga al usuario final (estudiantes o profesores), sólo a evaluadores/QA autorizados.
- No se automatizará la edición directa de código en caliente en el navegador (la resolución se hace a nivel de código fuente en local).

## Decisions

### 1. Inyección de Overlay Global en el Frontend
- **Decisión**: Envolver el contenedor principal del juego en un componente React `<UXFeedbackOverlay>`.
- **Razón**: Evita modificar cada pantalla de Fase de manera individual. El overlay intercepta eventos de clic globales en fase de captura (`onClickCapture`) si el modo "Inspector de Feedback" está activo, deteniendo la propagación hacia el juego de forma segura.
- **Alternativas**: Modificar cada uno de los archivos `FaseXGameScreen.tsx`. Esto aumentaría el acoplamiento y el riesgo de introducir regresiones de juego en producción.

### 2. Algoritmo de Selector CSS Semántico
- **Decisión**: Implementar una función recursiva de navegación DOM ascendente que genere un selector CSS omitiendo IDs automáticos del renderizado y priorizando clases específicas del dominio (ej. `.f4-pizza-visualizer`).
- **Razón**: Permite a herramientas de desarrollo como Ripgrep mapear rápidamente el selector al código fuente React, ya que los estilos específicos del juego suelen usar estas clases.
- **Alternativas**: XPath completo o coordenadas absolutas de pantalla. XPath es frágil frente a pequeños cambios de estructura y las coordenadas dependen de la resolución y el tamaño de la pantalla.

### 3. Almacenamiento Relacional y Almacenamiento S3 (MinIO)
- **Decisión**: Almacenar los metadatos (Fase, Módulo, Selector, JSON del Estado) en una tabla PostgreSQL estructurada mediante SQLAlchemy. Opcionalmente, usar `html2canvas` para renderizar el área de juego y subir la imagen a MinIO (S3 local).
- **Razón**: PostgreSQL garantiza el orden de la cola de mejorías para el administrador, y el almacenamiento en MinIO mantiene las imágenes seguras y centralizadas.
- **Alternativas**: Escribir un archivo JSON en disco local en el backend. Esto fallaría en entornos distribuidos o de pruebas multiusuario en el VPS.

## Risks / Trade-offs

- **[Riesgo] Interferencia con eventos táctiles y dinámicos**: El bloqueo de eventos al inspeccionar puede interferir con elementos de animación dinámicos (Framer Motion).
  - *Mitigación*: El Modo Inspector tendrá un interruptor visual prominente para "Activar/Desactivar" el escáner. Al desactivarlo, los listeners del DOM se desconectan por completo, permitiendo el juego natural.
- **[Riesgo] Desactualización de Selectores**: Cambios futuros en el árbol de componentes pueden hacer que el selector CSS guardado en la BD apunte a elementos inexistentes en el código.
  - *Mitigación*: Se capturará también el ID de la Pregunta y la Fase. Aunque el selector cambie, la ubicación lógica del problema (Fase 4, Módulo 1, Pregunta 2) permanece inalterada y sirve como referencia principal de localización.
