## 1. Ajustes de Estilos CSS en Frontend

- [x] 1.1 Modificar en `Fase4Styles.css` el modal `.f4-reading-card` para aumentar `max-height` a `min(85vh, 620px)` en viewports grandes y medianos.
- [x] 1.2 Reducir el padding de `.f4-reading-body` a `10px 14px` en `Fase4Styles.css`.
- [x] 1.3 Reducir el padding y el margen inferior de `.f4-example-box` en `Fase4Styles.css`.
- [x] 1.4 Reducir el tamaño máximo de los SVGs dentro de la columna visual de ejemplos en `Fase4Styles.css` (`.f4-example-visuals svg` a `75px`).
- [x] 1.5 Reducir el gap de `.f4-flashcard-content` y `.f4-ex-steps` en `Fase4Styles.css`.

## 2. Refactorización del Componente de Teoría

- [x] 2.1 Modificar la función `extraerSvgYTexto` en `Fase4TheoryModal.tsx` para admitir y extraer múltiples etiquetas `<svg>` globalmente y acumularlas en la vista de visuals.
- [x] 2.2 Proteger el renderizado del HTML de enunciados para evitar que queden etiquetas divs o párrafos rotos abiertos.

## 3. Pruebas y Verificación del Modal de Teoría

- [x] 3.1 Iniciar el entorno de desarrollo local con Docker Compose para validar la visualización de la teoría.
- [x] 3.2 Verificar que el modal de teoría del Módulo 1 Nivel 3 en Fase 4 no presente scroll vertical en un viewport representativo de 2560x945.
- [x] 3.3 Validar que los ejemplos con múltiples SVGs (Módulo 1 Nivel 2) se sigan renderizando correctamente.

## 4. Corrección de Bugs del Bucle Espejo (Backend)

- [x] 4.1 Agregar `.order_by(PoolAsignadoAlumno.id.asc())` a la consulta `select(PoolAsignadoAlumno)` en el endpoint `GET /pregunta` de `fase4/router.py` (~L487-494) para garantizar orden determinista del pool.
- [x] 4.2 Agregar `.order_by(PoolAsignadoAlumno.id.asc())` a la segunda consulta del pool en `GET /pregunta` (~L603-610, bloque de recarga tras siembra).
- [x] 4.3 Corregir el campo `feedback_tutor=feedback_msg` → `feedback_error=feedback_msg` en el `return Fase4ResultadoRespuesta(...)` del endpoint `POST /responder` (~L918).
- [x] 4.4 Eliminar el segundo endpoint duplicado `POST /cerrar-rescate` (~L1105-L1167) de `fase4/router.py`, manteniendo solo el primero (~L968-L1064).
- [x] 4.5 Verificar que el tipo `Fase4AnswerResult` en `Fase4Types.ts` del frontend acepte el campo correcto (`feedback_error` en lugar de o además de `feedback_tutor`), y ajustar si es necesario para que el frontend muestre el feedback textual.

## 5. Pruebas y Verificación del Bucle Espejo

- [x] 5.1 Reconstruir el backend local con Docker Compose (`--build`) para aplicar los cambios de `router.py`.
- [x] 5.2 Navegar a Fase 4 > Módulo 1 > Nivel 1 (Práctica Libre), responder incorrectamente y verificar que se active el modal de Pregunta Espejo (`Fase4MirrorModal`).
- [x] 5.3 Verificar que el feedback textual del tutor sea visible en la UI tras una respuesta incorrecta (no solo animación rojo/temblor).
- [x] 5.4 Verificar que `POST /cerrar-rescate` funcione correctamente tras agotar los 3 niveles de espejo (soporte avanzado).

## 6. Nueva Geometría de 12 Porciones (rect_asymmetric_twelfths)

- [x] 6.1 Crear función `_build_rect_asymmetric_twelfths()` en `seed.py` con 7 sectores (4 rectángulos + 4 triángulos = 12/12).
- [x] 6.2 Registrar la geometría en el generador de preguntas del Módulo 1 (polígono no homogéneo) con fracciones doceavas.
- [x] 6.3 Registrar la geometría en el generador de preguntas del Módulo 3 (porcentajes, nivel 1) con porcentajes compatibles.
- [x] 6.4 Agregar ejemplo explicativo SVG de 12 porciones en `theory_examples.py` sección `(1, 3)` con visualización coloreada por sector.
- [x] 6.5 Reconstruir imagen Docker del backend y re-sembrar la BD local exitosamente.

