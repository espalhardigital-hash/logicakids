## 1. Alineación y Correcciones de Lógica

- [x] 1.1 Modificar `phaseMaps.ts` en el frontend para alinear las secciones de Fases 5 a 8 con el formato del backend (`modulo_id * 100 + nivel_id`).
- [x] 1.2 Corregir el endpoint de graduación de Fase 5 en `backend/app/fase5/router.py` para actualizar a Fase 6 (orden 6) y validar 13 niveles de práctica en vez de 26 mixtos.
- [x] 1.3 Ocultar la contraseña de base de datos en `SystemTab.tsx` usando un input tipo `password` con control de ojo para revelarla.
- [x] 1.4 Garantizar la presencia de `progreso_sre.json` en el servidor de reportes local para resolver el HTTP 404 de SreTab.

## 2. Modularización y Refactorización del Administrador

- [x] 2.1 Separar `PedagogyTab.tsx` en subcomponentes funcionales: `PedagogyTabContainer`, `ProgressConfigTable`, `ConfigFormModal` y `PhaseFlowDesigner`.
- [x] 2.2 Separar `ContentTab.tsx` en subcomponentes funcionales: `ContentTabContainer`, `TheoryEditor`, `QuestionTable` y `QuestionFormModal`.
- [x] 2.3 Integrar y verificar la consistencia del estilo premium glassmorphic del panel tras la modularización.

## 3. Simulador Pedagógico e Interacción Docente

- [x] 3.1 Implementar `StudentViewSimulator.tsx` con un `StudentMockProvider` para revisar teoría, preguntas guiadas y juego de prueba libre sin colisiones de estado.
- [x] 3.2 Incorporar contenedores con `aspect-ratio` fijo y `ResizeObserver` reactivo en los canvas del simulador para evitar distorsiones de figuras 2D/3D.
- [x] 3.3 Modificar componentes de frontend para aceptar un prop `isSimulationMode={true}` que permita el Skip y bypass de endpoints HTTP reales.

## 4. Sistema de Comentarios del Docente (Feedback)

- [x] 4.1 Crear el componente `TeacherCommentBox.tsx` dentro del simulador para permitir al docente registrar notas de revisión.
- [x] 4.2 Crear el endpoint `POST /api/admin/feedback` en `backend/app/routers/feedback.py` para persistir los comentarios en `backend/data/feedback_docente.json`.
- [x] 4.3 Registrar el nuevo router de feedback en el punto de entrada principal `backend/app/main.py`.
- [x] 4.4 Desarrollar el script de listado diagnóstico `backend/scripts/apply_teacher_feedback.py` que permita al Agente Antigravity leer el JSON y aplicar cambios asistidos en la DB.

## 5. Auditoría y Autocuración de Imágenes (Fases 3-8)

- [x] 5.1 Implementar el script de diagnóstico `backend/scripts/audit_question_images.py` para escanear la DB y reportar imágenes faltantes en consola.
- [x] 5.2 Incorporar en el Agente Antigravity el rol de verificación de existencia y generación procedimental (relojes, planos cartesianos, cuadrículas, termómetros, bloques 3D) asistida.
- [x] 5.3 Desarrollar herramientas de renderización vectorial offline usando Pillow (círculos/barras de fracciones, dados y urnas con esferas) para uso del Agente interactivo.
