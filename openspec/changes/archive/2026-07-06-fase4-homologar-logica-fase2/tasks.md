## 1. Backend Updates (router.py)

- [x] 1.1 Inyectar `es_espejo=True` en `datos_numericos` dentro del endpoint `get_pregunta` cuando la variante es mayor a cero.
- [x] 1.2 Implementar el booleano `soporte_avanzado` en el endpoint `responder` (basado en intentos familiares fallidos).
- [x] 1.3 Crear el endpoint `@router.post("/cerrar-rescate")` idéntico al de la Fase 2.
- [x] 1.4 Realizar test (Playwright/pytest/manual) para verificar que el backend funciona correctamente y entrega los estados esperados.

## 2. Shared Types

- [x] 2.1 Agregar la propiedad opcional `soporte_avanzado?: boolean;` a la interfaz `Fase4AnswerResult` en `Fase4Types.ts`.

## 3. Frontend Updates (Fase4GameScreen.tsx)

- [x] 3.1 Agregar el listener de websockets `sync_required` en un `useEffect`.
- [x] 3.2 Crear y añadir el modal en línea `Fase4RescateModal` para mostrar el soporte avanzado.
- [x] 3.3 Modificar `loadNextQuestion` para que lea `es_espejo` desde los `datos_numericos` inyectados y abra `Fase4MirrorModal`.
- [x] 3.4 Refactorizar `handleSubmit` para que en caso de error espejo o rescate simplemente navegue hacia `loadNextQuestion()` o asigne el modal, igual que en Fase 2, eliminando las recargas de pregunta manuales.
- [x] 3.5 Realizar test (Playwright/manual) de todo el flujo Frontend de la Fase 4 para corroborar comportamiento.

## 4. Despliegue y Validación

- [x] 4.1 Actualizar el repositorio de GitHub (commit y push a `desarrollo`).
- [x] 4.2 Hacer deploy local de todos los contenedores y verificar funcionamiento. (NOTA: Si se requiere ejecutar seed para poblar la DB, la ejecución debe ser 100% automatizada a través de comandos o scripts, sin requerir ningún paso manual).
- [x] 4.3 Hacer deploy en VPS (Desarrollo) y leer logs para corroborar que los contenedores están funcionando correctamente sin errores. (De requerir DB seed, debe hacerse 100% automático).
- [x] 4.4 Hacer deploy en VPS (Producción) y leer logs para corroborar que los contenedores de producción están funcionando correctamente. (De requerir DB seed, debe hacerse 100% automático).
