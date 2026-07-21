## 1. Resolución de Fuga de Storage (Backend)

- [x] 1.1 Modificar `delete_file` en `LogicaMath/backend/app/core/storage.py` para utilizar `urllib.parse.urlparse` y resolver de manera robusta la Key completa de S3, incluyendo directorios.
- [x] 1.2 **Test de Verificación 1.1:** Escribir y ejecutar un script de test unitario en Python (`tests/test_storage_delete.py` o similar) que mockee el cliente S3 y verifique que el borrado extrae la Key correcta para URLs con y sin subcarpetas.

## 2. Validación de Parámetros Discretos (Frontend)

- [x] 2.1 Modificar `validarYCorregirParametros` en `LogicaMath/frontend/services/validadorContextual.ts` agregando un fallback matemático robusto con `Math.ceil` / `Math.floor` cuando el delta no encuentre una solución entera en el bucle.
- [x] 2.2 **Test de Verificación 2.1:** Escribir un test unitario en Vitest para comprobar que el validador contextual corrige a un entero válido sin fallas de decimales ante cualquier escenario discreto problemático.

## 3. Segmentación Flexible de Enunciados (Frontend)

- [x] 3.1 Actualizar la división de enunciados para problemas de dos pasos en `LogicaMath/frontend/services/validadorContextual.ts` utilizando una expresión regular flexible con lookbehind.
- [x] 3.2 **Test de Verificación 3.1:** Escribir y correr tests de Vitest verificando que la división del enunciado funciona correctamente con saltos de línea (`\n`), puntos sin espacio, o signos de exclamación e interrogación (`!`, `?`).
