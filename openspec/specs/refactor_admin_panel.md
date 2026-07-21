# Especificación de Diseño: Refactorización y Mejoras del Panel de Administrador

## 📋 Objetivos
1. **Preservar y Reparar las Pestañas Técnicas**:
   - **Monitoreo SRE (`SreTab.tsx`)**: Se resolvió el error de desconexión del servidor de reportes (HTTP 404) al sembrar y copiar dinámicamente el archivo `progreso_sre.json` al directorio público de resultados.
   - **Servidor y BD (`SystemTab.tsx`)**: Se implementa el enmascarado del input de `DATABASE_URL` para evitar exponer contraseñas en texto plano (BUG-2).
2. **Modularización de Componentes Gigantes**:
   - Extraer subcomponentes funcionales de `PedagogyTab.tsx` (~101 KB) y `ContentTab.tsx` (~90 KB) para mejorar la legibilidad y mantenimiento del código.
3. **Corregir la Discrepancia de IDs de Sección (Fase 5 a Fase 8)**:
   - Modificar `phaseMaps.ts` para alinear las secciones del administrador con las generadas por los seeders y routers del alumno en el backend (`101`, `102` en lugar de `5011`, `5012`).
4. **Simulador de Interfaz de Alumno (`StudentViewSimulator.tsx`)**:
   - Incorporar un modo de previsualización en caliente para que el docente pueda ver el enunciado, teoría y el teclado virtual tal como los visualiza el alumno durante el gameplay.

---

## 🔍 Análisis de Cambios Requeridos

### 1. Corrección de IDs de Sección en `phaseMaps.ts`
En `phaseMaps.ts`, las secciones de las Fases 5, 6, 7 y 8 deben alinearse a la fórmula del backend:
`seccion = modulo_id * 100 + nivel_id` (Práctica) y `seccion = modulo_id * 1000 + nivel_id` (Desafíos).

*Ejemplo de cambios en Fase 5:*
```typescript
// ANTES:
{ id: 1, name: "Conteo directo de unidades lineales", seccion: 5011, operacion: "mixta" },
{ id: 11, name: "Desafío 1 (Estándar)", seccion: 50111, operacion: "mixta", isChallenge: true },

// DESPUÉS:
{ id: 1, name: "Conteo directo de unidades lineales", seccion: 101, operacion: "mixta" },
{ id: 11, name: "Desafío 1 (Estándar)", seccion: 1011, operacion: "mixta", isChallenge: true },
```

---

## 📐 Estructura Modular Propuesta

### Pestaña Pedagógica (`PedagogyTab`)
Se divide en:
- `PedagogyTabContainer.tsx`: Maneja los selectores y el estado principal.
- `ProgressConfigTable.tsx`: Renderiza la grilla de reglas y porcentajes de avance por nivel.
- `ConfigFormModal.tsx`: Modal para crear o actualizar criterios de maestría.
- `PhaseFlowDesigner.tsx`: Panel gráfico para el diseño del flujo de mapas.

### Pestaña de Contenido (`ContentTab`)
Se divide en:
- `ContentTabContainer.tsx`: Maneja el ciclo de carga de teoría y preguntas.
- `TheoryEditor.tsx`: Panel enriquecido para editar glosarios, tips y textos teóricos.
- `QuestionTable.tsx`: Grilla interactiva de búsqueda y paginación del banco de preguntas.
- `QuestionFormModal.tsx`: Creador de preguntas y alternativas con resaltador de tokens de error cognitivo (`TokenHighlighter`).
- `StudentViewSimulator.tsx`: Renderiza dinámicamente un sandbox interactivo de la pregunta actual (incluyendo el teclado numérico de la fase) y la teoría para previsualización docente.

---

## 🖼️ 5. Auditoría y Autocuración de Imágenes mediante IA (Fases 3 a 8)

Para solucionar el problema de las imágenes distorsionadas, rotas o inexistentes, se establece un pipeline de autocuración e inicialización:

### A. Script de Auditoría de Base de Datos (`backend/scripts/audit_question_images.py`)
1. **Escaneo de Fases 3 a 8**: El script consulta la base de datos PostgreSQL local para identificar todas las preguntas registradas de las fases 3, 4, 5, 6, 7 y 8.
2. **Identificación de Preguntas Visuales**: Analiza heurísticamente si el enunciado o la configuración requiere una figura o diseño (mediante palabras clave como *"figura"*, *"dibujo"*, *"gráfico"*, *"fracción"*, *"reloj"*, *"termómetro"*, *"urna"*, *"bolas de colores"*, *"dado"*, *"plano cartesiano"*, *"escala"*).
3. **Validación en el Storage (MinIO/Local)**: Realiza una comprobación contra el storage. Si `S3` está configurado, valida la existencia de la `Key` en el bucket `logicakids` de MinIO. De lo contrario, valida la presencia física del asset en el directorio de fallback local (`app/static/graphics/`).
4. **Auto-Generación y Asociación con IA**:
   * Si falta el asset, el script lo genera automáticamente:
     * **Figuras Estándar**: Invoca los generadores procedimentales de `graphics_generator.py` para relojes, planos cartesianos, grillas de área/perímetro, cubos isométricos y termómetros.
     * **Figuras Especiales y Fracciones**: Dibuja representaciones vectoriales limpias usando Pillow (pizzas/barras de fracciones para Fase 4, dados y urnas con bolas de colores para la combinatoria de la Fase 8).
     * **Figuras Conceptuales (Gemini)**: Invoca la API de Gemini (Imagen 3) si hay credenciales para generar la ilustración basada en el enunciado.
   * Sube la imagen y actualiza el campo `datos_numericos` en base de datos con la URL de MinIO.

---

## 🎮 6. Simulador de Flujo Pedagógico Completo (`StudentViewSimulator.tsx`)

El simulador dentro del panel de administrador no se limitará a previsualizar la pregunta aislada, sino que replicará la experiencia exacta del alumno paso a paso:

1. **Revisión de Teoría**: El administrador podrá visualizar la interfaz de NivelTeoria tal como la ve el alumno (texto de descubrimiento, glosario interactivo, advertencias y los 3 ejercicios interactivos obligatorios).
2. **Revisión de Preguntas Guiadas (Paso 1)**: Visualización y prueba del flujo del paso a paso (Tutoría invisible), donde se resalta la información crítica del enunciado y se simula el comportamiento de los tokens de error.
3. **Revisión de Prueba Libre**: Simulación del gameplay con el teclado numérico interactivo de la fase.
4. **Botón Saltar (Skip - Avanzar sin responder)**:
   * Para evitar bloquear la auditoría del docente, el simulador incluirá una opción exclusiva para administradores llamada *"Avanzar sin responder"*.
   * Al presionarla, el simulador registrará el paso como completado y cargará la siguiente pregunta o fase teórica en la cola, permitiendo revisar rápidamente todo el flujo de aprendizaje.

---

## 📝 7. Caja de Retroalimentación del Docente y Pipeline de Corrección con LLM

Para habilitar un ciclo continuo de control de calidad didáctica, se implementa una herramienta de comentarios y corrección automática:

### A. Registro de Comentarios en el Frontend
* En el simulador, el docente contará con un componente `TeacherCommentBox.tsx`.
* Podrá ingresar comentarios específicos de la pregunta actual o la sección de teoría que está auditando (ej. *"Cambiar el enunciado porque confunde manzanas con peras"* o *"La respuesta correcta debe ser 15 y no 12"*).

### B. Endpoint de Feedback y Persistencia en Archivo Local
* Se crea un endpoint en el backend: `POST /api/admin/feedback` (en `backend/app/routers/feedback.py`).
* Al enviar un comentario, este se anexa en formato JSON estructurado en el archivo local de la aplicación:
  `docs/feedback_docente.json`
  ```json
  [
    {
      "id": "uuid-v4",
      "fase_id": 4,
      "seccion_id": 401,
      "pregunta_id": 1285,
      "tipo": "pregunta",
      "comentario": "El gráfico de la fracción 3/4 no carga. Favor generar de nuevo.",
      "fecha": "2026-06-26T15:20:00Z",
      "procesado": false
    }
  ]
  ```

### C. Pipeline de Aplicación del Feedback por LLM (`backend/scripts/apply_teacher_feedback.py`)
1. Un script en segundo plano o una tarea del backend lee el archivo `docs/feedback_docente.json`.
2. Filtra los comentarios con `"procesado": false`.
3. Para cada comentario, la LLM (usando Gemini 1.5) interpreta la solicitud de cambio didáctico:
   * Si pide corrección de texto o explicación: Reescribe el campo `enunciado` o `explicacion_paso_a_paso` en la base de datos de forma automática.
   * Si pide corrección de respuesta o alternativas: Ajusta los valores de las alternativas y la respuesta correcta.
   * Si pide corregir o generar una imagen: Invoca al script de autocuración de imágenes para crear o actualizar el gráfico asociado.
4. Marca el registro en el JSON como `"procesado": true` y registra la fecha de aplicación.

---

## 🧪 8. Plan de Verificación

1. **Auditoría de Imágenes (Fases 3-8)**:
   - Ejecutar el script `audit_question_images.py` y comprobar que identifique preguntas con imágenes rotas o faltantes y cargue los reemplazos procedimentales en MinIO.
2. **Previsualización de Teoría y Preguntas**:
   - Abrir el simulador en el panel de administrador y comprobar que renderice correctamente la teoría de la sección, el paso a paso y el juego libre.
3. **Simulación de Skip**:
   - Presionar "Avanzar sin responder" en el simulador y comprobar que el componente actualice el estado y avance al siguiente item sin lanzar excepciones.
4. **Persistencia de Comentarios**:
   - Agregar comentarios en el banco de preguntas desde el simulador, verificar que la API guarde exitosamente la información y confirmar que se anexe correctamente en `docs/feedback_docente.json`.
5. **Enmascarado en SystemTab**:
   - Validar que el campo de contraseña y base de datos esté protegido visualmente.

---

## 📋 Requerimientos (ADDED Requirements)

### Requirement: Modularización del Panel de Administrador
El panel de administración MUST estructurarse de forma modular dividiendo las pestañas `PedagogyTab` y `ContentTab` en subcomponentes funcionales cohesivos sin alterar el estilo visual de glassmorphism original.

#### Scenario: Carga del panel modularizado
- **WHEN** un usuario con rol de administrador abre el panel de administrador
- **THEN** el sistema carga y renderiza las pestañas utilizando los nuevos subcomponentes manteniendo el diseño visual intacto

### Requirement: Corrección de IDs de Sección en Fases 5 a 8
La aplicación frontend MUST mapear las secciones de las Fases 5 a 8 según la fórmula del backend: `modulo_id * 100 + nivel_id` para práctica, y `modulo_id * 1000 + nivel_id` para desafíos.

#### Scenario: Listado de preguntas de Fase 5 exitoso
- **WHEN** el administrador selecciona la Fase 5 en el banco de preguntas
- **THEN** la tabla de contenido realiza la petición HTTP con el ID de sección correcto y despliega las preguntas correspondientes

### Requirement: Simulador de Flujo Pedagógico en Administrador
El panel de administración MUST incluir un simulador de alumno (`StudentViewSimulator.tsx`) que permita previsualizar la teoría, el flujo de preguntas guiadas y el juego de prueba libre del nivel seleccionado. Las vistas MUST estar envueltas en un contexto falso (`StudentMockProvider`) para evitar colisiones con el estado real del usuario administrador.

#### Scenario: Visualización de teoría en simulador
- **WHEN** el docente abre el simulador de una sección específica
- **THEN** el sistema presenta el texto de descubrimiento, los glosarios de la teoría y los ejercicios interactivos tal y como los visualiza el alumno

### Requirement: Avanzar sin Responder en Simulador
El simulador de estudiante para administradores MUST proveer una opción de "Avanzar sin responder" que permita omitir preguntas y continuar el flujo de auditoría didáctica. Los componentes de frontend (ej. `GuidedQuestionView`) MUST aceptar un flag `isSimulationMode={true}` para que intercepten internamente las llamadas HTTP a `/api/faseX/answer` y eviten ensuciar las estadísticas o arrojar errores de permisos (403).

#### Scenario: Docente salta pregunta
- **WHEN** el docente hace clic en el botón "Avanzar sin responder" en el simulador
- **THEN** el sistema simula el acierto o avanza al siguiente elemento de la cola sin requerir respuesta numérica

### Requirement: Enmascarado de DATABASE_URL en SystemTab
La pestaña de Servidor y BD (`SystemTab.tsx`) MUST proteger visualmente el valor de la contraseña en el campo `DATABASE_URL` por defecto y proveer un control para revelar el texto plano.

#### Scenario: Visualización segura de DATABASE_URL
- **WHEN** el administrador navega a la pestaña Servidor y BD
- **THEN** el campo `DATABASE_URL` oculta la contraseña y muestra un botón de ojo para revelarla

### Requirement: Diagnóstico para Autocuración de Imágenes
El script de backend `backend/scripts/audit_question_images.py` MUST revisar la base de datos de preguntas de las fases 3 a 8 y reportar en consola qué enunciados visuales carecen de imagen en MinIO. Este reporte será consumido por el Agente de IA para proceder a su generación.

#### Scenario: Autocuración asistida por Agente
- **WHEN** se ejecuta el script de auditoría y reporta en consola que una pregunta de la Fase 7 no tiene su imagen de reloj analógico
- **THEN** el Agente Antigravity genera la imagen solicitada (procedimental o usando sus herramientas) y actualiza el sistema

### Requirement: Monitoreo SRE sin error 404
El sistema de monitoreo SRE en el panel de administrador MUST cargar el archivo de progreso sin fallas 404 mediante la inicialización y exposición adecuada del archivo `progreso_sre.json`.

#### Scenario: Visualización del dashboard SRE exitosa
- **WHEN** el administrador navega a la pestaña de Monitoreo SRE
- **THEN** el sistema lee el archivo `progreso_sre.json` desde el servidor local y renderiza los gráficos de progreso técnico sin fallas HTTP 404
