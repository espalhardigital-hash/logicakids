## 1. Creación del Fase4VisualizerEngine

- [x] 1.1 Crear el archivo `Fase4VisualizerEngine.tsx` en `LogicaMath/frontend/components/fase4/`.
- [x] 1.2 Mover el código condicional de visualizadores interactivos (pizzas, pie charts, thermómetros, etc.) desde `Fase4GameScreen.tsx` al nuevo engine.
- [x] 1.3 Refactorizar `Fase4GameScreen.tsx` para importar y usar `<Fase4VisualizerEngine />`.
- [x] 1.4 Test de Sección 1: Verificar que el código compila y la pantalla principal de la fase 4 puede acceder a los visualizadores correctamente. Si falla, regresar a los pasos de la sección 1 para aplicar correcciones antes de avanzar a la siguiente sección.

## 2. Refactorización del Fase4MirrorModal (Input Dual y Teclado)

- [x] 2.1 Eliminar el teclado numérico hardcodeado de `Fase4MirrorModal.tsx`.
- [x] 2.2 Importar e integrar el `<CustomKeyboard />` global dentro del Modal Espejo.
- [x] 2.3 Añadir la lógica de estado dual `respuestaNum`, `respuestaDen` y `activeInputField` al Modal Espejo para permitir fracciones.
- [x] 2.4 Renderizar condicionalmente `f4-fraction-input-box` cuando la respuesta correcta contenga el carácter `/`.
- [x] 2.5 Unificar las respuestas al enviar el formulario (Submit) concatenando numerador y denominador si aplica.
- [x] 2.6 Test de Sección 2: Comprobar que TypeScript aprueba los cambios en los imports y la lógica del input dual. Si hay errores, corregir e iterar hasta que compile sin problemas antes de avanzar.

## 3. Integración Visual en el Mirror Modal

- [x] 3.1 Importar `<Fase4VisualizerEngine />` en `Fase4MirrorModal.tsx`.
- [x] 3.2 Renderizar `<Fase4VisualizerEngine />` en el lado izquierdo del Modal Espejo (o arriba del input), pasando las propiedades requeridas para que los niños puedan interactuar visualmente.
- [x] 3.3 Test de Sección 3: Verificar que el componente `Fase4MirrorModal` recibe el engine interactivo correctamente y sin conflictos de variables de estado. Si falla, corregir hasta completar el objetivo de diseño.

## 4. Despliegue y Validación Final

- [x] 4.1 Realizar un redespliegue del contenedor de frontend o el stack local usando Docker (`docker compose -f docs/Pruebas_y_Test_Unitario/docker-compose.local.yml up -d --build`) para asegurar que todos los cambios hagan efecto.
