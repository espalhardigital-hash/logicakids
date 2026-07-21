## Context

El panel de administrador de LogicaKids cuenta con dos pestañas gigantescas (`PedagogyTab` y `ContentTab`) que concentran lógica de consulta, tablas, edición de preguntas y flujos de mapas. Además, el mapeo de secciones para Fases 5 a 8 en el frontend (`phaseMaps.ts`) está desalineado de la lógica del backend (`modulo_id * 100 + nivel_id`), provocando cargas vacías. Por otro lado, la pérdida de conexión local con la VPS (Modo 100% Local activo) requiere que las imágenes e infraestructura de reportes (SRE) se autogestionen de forma local y consistente sin dependencias de red externa. Por último, los docentes requieren evaluar la teoría y preguntas simulando la experiencia del alumno y registrando comentarios locales para posterior procesamiento.

## Goals / Non-Goals

**Goals:**
- **Modularización**: Dividir los componentes masivos del frontend en subcomponentes cohesivos sin alterar el diseño premium glassmorphism.
- **Simulador de Gameplay con Skip**: Reutilizar los componentes de teoría y juego del alumno en el Panel de Administrador, permitiendo omitir respuestas.
- **Canal de Feedback en JSON**: Registrar los comentarios del docente en `backend/data/feedback_docente.json` para facilitar el acceso offline y su posterior procesamiento por el agente.
- **Autocuración de Gráficos (Fases 3-8)**: Implementar el script `backend/scripts/audit_question_images.py` como diagnóstico para que el Agente IA regenere y suba los gráficos faltantes a MinIO de forma local.
- **Correcciones Técnicas**: Resolver el HTTP 404 del monitoreo SRE y enmascarar contraseñas de la DB en `SystemTab`.

**Non-Goals:**
- Modificar el diseño visual de la interfaz de juego.
- Realizar despliegues o commits automáticos a ramas de producción remotas sin aprobación del usuario.

## Decisions

### 1. Extracción y Modularización del Frontend
* **Opción A**: Reescribir completamente el panel en vistas separadas.
* **Opción B (Elegida)**: Dividir `PedagogyTab.tsx` y `ContentTab.tsx` en componentes reutilizables conservando el contenedor común y el estado de carga en la página del panel para preservar la transición suave.
* *Razón*: Mantiene la coherencia del diseño glassmorphic y simplifica la propagación de estados de carga/error.

### 2. Sandbox de Visualización y Aspect-Ratio Fijo
* Para evitar que figuras isométricas (3D) o planos cartesianos se distorsionen en pantallas de docentes, se implementará un `ResizeObserver` reactivo en los canvas que ajustará dinámicamente la proyección de cámara (`camera.aspect`). Los elementos HTML de imágenes usarán `object-fit: contain` con `aspect-ratio: 16/9`.

### 3. Canal de Feedback Físico en JSON
* En vez de añadir complejidad creando tablas relacionales transitorias en Postgres para los comentarios de revisión del docente, se escribirá un archivo JSON plano local (`backend/data/feedback_docente.json`). Esto simplifica el acceso de agentes LLM que corren tareas DevOps o de auditoría offline para aplicar los cambios propuestos por el docente directamente en la base de datos de preguntas. Se prefiere el volumen `backend/data/` ya que `docs/` no está montado en el contenedor backend.

### 4. Entorno de Simulación Aislado (Skip Mode y Mock Provider)
* El simulador debe renderizar vistas de alumnos (`GuidedQuestionView`) en el panel admin. Para evitar colapsos por uso de contextos no inicializados (el admin no es alumno), se empleará un `StudentMockProvider` que aísle el estado reactivo.
* Para la función "Avanzar sin responder" (Skip), los componentes frontend aceptarán el flag `isSimulationMode={true}`. Si está activo, bypassarán las peticiones a `/api/faseX/answer` evitando errores HTTP 403 y estadísticas corruptas.

### 5. Generación de Imágenes (IA y Procedimental)
* Para garantizar el funcionamiento, la auditoría identificará imágenes faltantes. El Agente Antigravity, de forma interactiva, utilizará funciones de dibujo vectorial nativas con Pillow (como círculos de fracciones y dados) y sus herramientas de generación LLM para suplir estos gráficos.

## Risks / Trade-offs

- **[Riesgo]** Desconexión local de MinIO en la carga de imágenes autocuradas.
  - *Mitigación*: El servicio de almacenamiento (`storage_service`) almacena las imágenes localmente en `/static/graphics/` como fallback inmediato si la API de S3 falla.
- **[Riesgo]** Conflicto de IDs de sección en estudiantes de prueba.
  - *Mitigación*: La alineación de IDs en `phaseMaps.ts` garantiza que tanto el administrador como el alumno compartan exactamente las mismas consultas SQL al backend.
