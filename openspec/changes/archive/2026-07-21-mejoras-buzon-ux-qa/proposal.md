## Why

Actualmente, el sistema "Buzón de Mejorías UX & QA" requiere intervención manual para las capturas de pantalla, presenta problemas de aislamiento de CSS (fugas de estilos en la vista previa del admin) al usar `dangerouslySetInnerHTML`, y genera un contexto insuficiente para diagnosticar errores lógicos (falta del estado reactivo de la app). Además, los selectores DOM pueden ser imprecisos y la gestión de URLs de las capturas con MinIO no siempre resulta clara para ser interpretada por modelos de lenguaje en tareas automatizadas. Esta actualización resolverá estas limitaciones creando una herramienta más autónoma y robusta.

## What Changes

- **Auto-Captura de Pantalla:** Se integrará `html2canvas` para capturar la vista de forma automática al momento de hacer clic en un elemento del DOM, eliminando la necesidad de subidas o paste manual de imágenes por parte del revisor.
- **Aislamiento en Shadow DOM:** La previsualización de fragmentos HTML en el Admin Panel dejará de depender de `dangerouslySetInnerHTML` en el layout principal. Se usará un Shadow DOM (o iframe) para asegurar que no se pierdan estilos (como `index.css`) ni colisionen clases.
- **Captura de Estado de la Aplicación:** Se expandirá la intercepción del DOM para que, además del HTML, se capture el estado interno (variables del contexto global de React, Zustand/Redux), facilitando diagnosticar si el error visual viene de un estado corrompido.
- **Mayor Precisión del Selector DOM:** Refactorización de la función generadora de selectores DOM (`getUniqueSelector`) para que los paths capturados sean unívocos y más exactos.
- **Enlace Absoluto a MinIO:** Aseguramiento y normalización de la URL de las capturas para que apunten explícita e inequívocamente al objeto de MinIO. Esta relación garantizará que cuando un LLM necesite aplicar cambios basándose en el buzón, tenga acceso directo a la evidencia visual.

## Capabilities

### New Capabilities
- `auto-screenshot`: Automatización de captura visual en caliente mediante `html2canvas` al interceptar elementos del DOM.
- `shadow-dom-preview`: Renderizado seguro y asilado de fragmentos HTML en el panel administrador.
- `state-capture`: Mecanismo para adjuntar estados internos reactivos a los reportes visuales del buzón.

### Modified Capabilities
- `ux-feedback-system`: Se modificarán los requerimientos de estructura de almacenamiento para dar cabida a nuevos estados, validación del link hacia MinIO, y refinamiento en la lógica de generación del selector del DOM.

## Impact

- Modifica componentes principales en Frontend (como `UXFeedbackOverlay.tsx`, `UXFeedbackTab.tsx`).
- Introduce nuevas dependencias en el proyecto frontend (ej. `html2canvas`).
- Afecta potencialmente la definición del payload hacia el Backend (`POST /evaluador/feedback`), que ahora incluirá mayor profundidad en `app_state`.
- Mejora la robustez de las herramientas de diagnóstico para los LLMs integrados (Antigravity).
