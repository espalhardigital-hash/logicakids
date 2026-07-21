## Why

En la Fase 4 existen dos problemas independientes que degradan la experiencia del alumno:

**1. Scroll vertical en modal de teoría (Frontend UX):** En el Módulo 1, Nivel 3 (y potencialmente en otros niveles de teoría), el contenido de los ejemplos del modal de teoría (`Fase4TheoryModal`) excede el espacio vertical disponible en viewports típicos (como 2560x945), lo que provoca un scroll vertical no deseado. Esto ocurre debido al tamaño del SVG de ejemplo inyectado en línea y al espaciado general del modal, lo cual dificulta la visualización rápida y fluida que se espera para los niños.

**2. Bucle Espejo (Mirror Loop) roto en Práctica Libre (Backend):** Al responder incorrectamente en modo Práctica Libre, el sistema debería activar una "Pregunta Espejo" (variante de la misma familia) presentada en un modal de segunda oportunidad. Actualmente, el frontend tiene el componente `Fase4MirrorModal` completamente preparado y el backend en `/responder` actualiza el `pregunta_id` del pool al de la variante espejo, pero la siguiente llamada a `/pregunta` **nunca devuelve la pregunta espejo** — en su lugar devuelve otra pregunta pendiente del pool. Se identificaron 3 causas raíz en el backend:
- **A.** Falta de `ORDER BY` determinista en la consulta del pool asignado, lo que hace que PostgreSQL (MVCC) devuelva la fila recién actualizada al final.
- **B.** El campo `feedback_tutor` usado en el return del endpoint `/responder` no existe en el schema Pydantic (`Fase2ResultadoRespuesta`), por lo que FastAPI lo descarta silenciosamente y el frontend no muestra feedback textual del tutor.
- **C.** Dos endpoints duplicados para `/cerrar-rescate` (líneas 968 y 1105 de `router.py`), donde FastAPI sobrescribe el primero con el segundo, anulando la lógica de cierre de rescate completa.

## What Changes

### Scope A: Modal de Teoría (Frontend)
- Reducir el tamaño de renderizado y márgenes de los gráficos SVG y visualizadores de fracciones (`PizzaFractionVisualizer` y SVGs incrustados) dentro del contenedor de ejemplos del modal de teoría (`Fase4TheoryModal`).
- Modificar el CSS en `Fase4Styles.css` para hacer más compactos los elementos del modal de teoría (`.f4-reading-card`, `.f4-reading-body`, `.f4-example-box` y `.f4-ex-steps`), y permitir que la tarjeta tenga una altura máxima ligeramente superior en pantallas con mayor altura vertical.
- Ajustar la lógica de extracción de SVGs en `Fase4TheoryModal.tsx` (`extraerSvgYTexto`) para manejar correctamente múltiples SVGs en un mismo enunciado (como en las equivalencias) y no dejar etiquetas HTML abiertas o rotas.

### Scope B: Bucle Espejo del Backend (Bug Fixes)
- Agregar `order_by(PoolAsignadoAlumno.id.asc())` a la consulta del pool en el endpoint `GET /pregunta` de `fase4/router.py` para garantizar que la pregunta espejo recién asignada se devuelva primero.
- Corregir el mapeo del campo de feedback en el `return` del endpoint `POST /responder` de `fase4/router.py`, reemplazando `feedback_tutor` por `feedback_error` para alinearse con el schema `Fase2ResultadoRespuesta`.
- Eliminar el endpoint duplicado de `/cerrar-rescate` (el segundo, línea ~1105) y consolidar toda la lógica de cierre de rescate en un solo endpoint.

## Capabilities

### New Capabilities
<!-- Ninguna nueva capacidad de negocio a nivel conceptual global -->

### Modified Capabilities
- `fase4-theory-ux`: Optimización de la experiencia de usuario y diseño visual en las pantallas de teoría de Fase 4, eliminando scroll vertical innecesario.
- `fase4-mirror-loop-fix`: Corrección de 3 bugs en el backend de Fase 4 que impedían el funcionamiento del Bucle Espejo (Preguntas Espejo) en modo Práctica Libre y el feedback textual del tutor.

## Impact

- `LogicaMath/frontend/components/fase4/Fase4TheoryModal.tsx`: Ajustar el parser de SVGs y compactar el contenedor de visualizaciones.
- `LogicaMath/frontend/components/fase4/Fase4Styles.css`: Rediseñar márgenes, paddings y alturas del modal de teoría.
- `LogicaMath/backend/app/fase4/router.py`: Corregir ORDER BY en pool, feedback_error en return, y eliminar endpoint duplicado de `/cerrar-rescate`.
- `LogicaMath/backend/app/fase2/schemas.py`: Verificar compatibilidad del campo `feedback_error` con el alias `Fase4ResultadoRespuesta`.
