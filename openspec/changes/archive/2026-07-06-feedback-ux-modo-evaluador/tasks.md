## 1. Estructura y Persistencia en el Backend

- [x] 1.1 Crear el modelo SQLAlchemy `UXFeedback` en `LogicaMath/backend/app/models/ux_feedback.py` y registrarlo en el sistema.
- [x] 1.2 Generar la migración de base de datos con Alembic y ejecutarla para crear la tabla `ux_feedback` en PostgreSQL local.
- [x] 1.3 Implementar los esquemas Pydantic para el feedback de UX en `LogicaMath/backend/app/schemas.py`.
- [x] 1.4 Crear el router API `/api/evaluador` con los endpoints `POST /feedback` and `GET /feedback` en el backend.
- [x] 1.5 **Test de Validación del Backend**: Implementar y ejecutar un test unitario en el backend (por ejemplo, con Pytest en `LogicaMath/backend/tests`) que realice peticiones mockeadas a `/api/evaluador/feedback` verificando que se inserten y consulten anotaciones correctamente de la base de datos. Si el test es fallido, corregir la persistencia y la API antes de avanzar.

## 2. Componentes Frontend en React

- [x] 2.1 Implementar el helper de cálculo de selector DOM único `getUniqueSelector` en el frontend.
- [x] 2.2 Crear el componente `<UXFeedbackOverlay>` en React que detecta el modo inspector, resalta los elementos visuales en hover e intercepta clics.
- [x] 2.3 Diseñar el formulario modal flotante que aparece al hacer clic en un elemento para que el evaluador ingrese su comentario, tipo y prioridad.
- [x] 2.4 Integrar el overlay global de feedback en la pantalla principal del juego.
- [x] 2.5 **Test de Validación del Inspector Frontend**: Implementar una prueba automatizada (ej. con Playwright/Vitest en `LogicaMath/frontend/tests`) o realizar una prueba manual documentada levantando el frontend local, verificando que al hacer clic en un elemento del juego (como el visualizador de fracciones) en modo inspector se dibuje el contorno neón, se detenga el flujo del juego y aparezca el modal flotante con el selector DOM correcto. Si la prueba falla, solucionar la interceptación de eventos en React antes de avanzar.

## 3. Panel de Administración de Mejorías UX

- [x] 3.1 Diseñar la vista de administración "Buzón de UX & Mejorías" en `LogicaMath/frontend/components/admin/AdminPanel.tsx` para listar las anotaciones.
- [x] 3.2 Implementar los filtros de Fase, Prioridad y Estado de resolución en la tabla del panel.
- [x] 3.3 Agregar la lógica para actualizar el estado del feedback y registrar notas del desarrollador.
- [x] 3.4 **Test de Validación del Panel de Administración**: Ejecutar pruebas de interfaz o verificación manual para comprobar que el listado carga correctamente todos los feedbacks enviados, los filtros por Fase/Prioridad funcionan y el cambio de estado (ej: marcar como "resuelto") se guarda correctamente en el backend. En caso de fallar, corregir la comunicación frontend-backend en el panel antes de avanzar.

## 4. Integración y Automatización con Antigravity

- [x] 4.1 Crear un comando o script de utilidad en Python que vuelque los feedbacks UX pendientes en formato estructurado para la IA de Antigravity.
- [x] 4.2 Probar el flujo completo: levantar el entorno local, dejar un feedback de prueba, y verificar su persistencia en base de datos.
- [x] 4.3 **Test de Validación de Integración Extremo a Extremo (E2E)**: Realizar un ciclo completo de prueba: registrar un reporte visual de QA en el juego, verificar su persistencia, comprobar su presencia en la vista administrativa, exportar la lista de correcciones mediante el script y validar que el archivo JSON de salida contenga la Fase, el Selector CSS y el Comentario exactos. Si el flujo tiene fallos en algún eslabón, corregir hasta que el test completo sea afirmativo.
