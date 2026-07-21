## 1. Instalación de Dependencias

- [x] 1.1 Instalar `html2canvas` en el frontend (`npm install html2canvas` en el directorio correcto)

## 2. Refactorización del Backend

- [x] 2.1 Modificar `upload_feedback_screenshot` en `storage.py` para devolver URLs absolutas apuntando explícitamente a MinIO (`MINIO_EXTERNAL_ENDPOINT`)
- [x] 2.2 Asegurar que el esquema de validación y la columna de la DB para `app_state` acepten la serialización del estado interno sin fallar

## 3. Mejoras en la Captura In-App (Frontend)

- [x] 3.1 Refactorizar `getUniqueSelector` en `UXFeedbackOverlay.tsx` para usar `nth-child` iterativamente en hermanos en lugar de `nth-of-type`, e incluir atributos como `data-testid`
- [x] 3.2 Implementar captura del estado reactivo: recolectar variables clave del contexto/juego para poblar un campo JSON en `app_state`
- [x] 3.3 Integrar `html2canvas` en `handleCaptureClick`: auto-capturar `document.body` y llamar a `handleUploadImage` automáticamente
- [x] 3.4 Agregar *loading state* (spinner/feedback visual) durante los milisegundos que demora `html2canvas` para evitar que el usuario piense que la app se trabó

## 4. Aislamiento en el Panel Administrador

- [x] 4.1 Crear el wrapper `<ShadowDOMWrapper>` (usando `attachShadow`) e inyectar `index.css` de manera programática en él
- [x] 4.2 Reemplazar la renderización directa de `dangerouslySetInnerHTML` dentro de `UXFeedbackTab.tsx` por el nuevo `<ShadowDOMWrapper>`
- [x] 4.3 Validar que los reportes antiguos y nuevos se previsualicen correctamente y no haya interferencias de layout
