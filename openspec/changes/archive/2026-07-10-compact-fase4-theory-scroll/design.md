## Context

Este change abarca dos dominios independientes de la Fase 4:

### A. Modal de Teoría (Frontend UX)
En el modal de teoría de la Fase 4 (`Fase4TheoryModal.tsx`), el contenido de los ejemplos del Módulo 1 Nivel 3 excede el viewport vertical de pantallas con formato horizontal común como 2560x945 debido a la combinación de:
1. Altura máxima estricta del contenedor principal (`.f4-reading-card` con `max-height: 540px`).
2. Espaciados de layout excesivos (márgenes y paddings en contenedores de ejemplos y cajas de pasos).
3. Dimensiones de las imágenes (especialmente los SVGs embebidos y visualizadores que a menudo no se escalan correctamente o consumen demasiado espacio vertical).
4. El parser `extraerSvgYTexto` actualmente solo extrae el primer SVG del enunciado y deja HTML inválido cuando hay múltiples SVGs.

### B. Bucle Espejo Roto (Backend)
Al responder incorrectamente en modo Práctica Libre, el endpoint `POST /responder` en `fase4/router.py` ejecuta correctamente la lógica de asignar la variante espejo al pool:
```python
# Líneas ~800-815 de router.py
if mirror_q and pool_item:
    pool_item.pregunta_id = mirror_q.id   # ✓ Actualiza correctamente
    pool_item.numero_intentos = 0
    es_espejo = True                       # ✓ Marca correctamente
```
Sin embargo, cuando el frontend llama a `GET /pregunta` para obtener la siguiente pregunta, la consulta SQL del pool **no tiene ORDER BY**:
```python
# Líneas ~487-494 de router.py
result_pool = await db.execute(
    select(PoolAsignadoAlumno).where(and_(...))
    # ← Falta .order_by(PoolAsignadoAlumno.id.asc())
)
```
PostgreSQL con MVCC mueve la fila actualizada al final de la tabla heap, por lo que `pool_pendientes[0]` toma otra pregunta pendiente en lugar de la espejo.

Adicionalmente:
- El campo `feedback_tutor` en el return de `/responder` (L918) **no existe** en el schema Pydantic `Fase2ResultadoRespuesta` (el campo correcto es `feedback_error`), por lo que FastAPI lo descarta silenciosamente.
- Existen **dos** endpoints `POST /cerrar-rescate` (L968 y L1105) con schemas de respuesta diferentes, donde FastAPI registra el segundo y sobrescribe al primero.

## Goals / Non-Goals

**Goals:**
- Compactar el modal de teoría de Fase 4 en pantallas de menor formato vertical (o con relaciones de aspecto anchas) y maximizar el uso del espacio.
- Rediseñar los estilos en `Fase4Styles.css` para optimizar alturas, paddings, y flex gaps en elementos de teoría.
- Ajustar `extraerSvgYTexto` en `Fase4TheoryModal.tsx` para soportar múltiples SVGs limpios en el enunciado sin corromper el HTML.
- Modificar el escalamiento de imágenes para que los SVGs e interactivos integrados no empujen el contenido y causen scroll.
- Corregir el orden de recuperación del pool asignado para que la pregunta espejo se devuelva siempre como primera pendiente tras un fallo.
- Alinear el campo de feedback del tutor con el schema Pydantic para que el frontend reciba el mensaje textual.
- Consolidar los endpoints duplicados de `/cerrar-rescate` en uno solo.

**Non-Goals:**
- Rediseñar la lógica pedagógica del juego de Fase 4 o modificar las preguntas y respuestas.
- Alterar otros componentes de fases distintas a la Fase 4, excepto que se compartan estilos genéricos (los cuales deben protegerse o aislarse mediante clases específicas `.f4-`).
- Modificar el schema `Fase2ResultadoRespuesta` en sí mismo — solo alinear el uso del campo correcto en el router de Fase 4.

## Decisions

### Decision 1: Aumento dinámico de `max-height` en viewports grandes y reducción de padding/gap
- **Alternativa A**: Mantener `max-height: 540px` y reducir drásticamente el tamaño del texto. (Rechazada: Empeora la legibilidad para niños).
- **Alternativa B**: Aumentar `max-height` a `620px` (o usar `min(80vh, 620px)`) para `.f4-reading-card` en viewports altos, y simultáneamente reducir los paddings verticales de `.f4-reading-body` (de `12px 16px` a `10px 14px`), `.f4-example-box` (de `12px 16px` a `8px 12px`), y el gap de `.f4-flashcard-content` (de `8px` a `6px`). (Seleccionada: Proporciona el balance óptimo entre legibilidad y ahorro de espacio vertical).

### Decision 2: Reducción del tamaño máximo de SVGs en ejemplos de teoría
- **Alternativa A**: Mantener `max-width: 90px !important` y `max-height: 90px !important`. (Rechazada: Sigue siendo demasiado grande para el layout compacto).
- **Alternativa B**: Ajustar a `max-width: 75px !important` y `max-height: 75px !important` para los SVGs en `.f4-example-visuals svg` y aplicar márgenes verticales de `0` en vez de `10px auto` dentro del inline style de los SVGs. (Seleccionada: Libera aproximadamente 30-40px de espacio vertical).

### Decision 3: Corrección del parser `extraerSvgYTexto` para múltiples SVGs
- **Alternativa A**: Regex simple no codiciosa que reemplace y extraiga todos los SVGs. (Seleccionada: Se modifica la expresión regular para buscar globalmente todos los bloques `<svg>...</svg>` y acumularlos en la sección visual, dejando el texto limpio de etiquetas HTML rotas).

### Decision 4: Orden determinista del pool asignado (Bug A)
- **Alternativa A**: Agregar `.order_by(PoolAsignadoAlumno.id.asc())` a la consulta existente del pool en `GET /pregunta`. (Seleccionada: Mínimo cambio, garantiza que la fila con menor `id` — la que fue asignada primero y luego actualizada con la variante espejo — se recupere primero en `pool_pendientes[0]`).
- **Alternativa B**: Usar un campo `prioridad` o `es_espejo` en `PoolAsignadoAlumno` para ordenar. (Rechazada: Requiere migración de base de datos y es innecesariamente complejo para el bug actual).

### Decision 5: Alineación del campo de feedback (Bug B)
- **Alternativa A**: Renombrar `feedback_tutor` a `feedback_error` en el `return` de `/responder` en `router.py`. (Seleccionada: El schema Pydantic `Fase2ResultadoRespuesta` define `feedback_error: Optional[str]`, y ese es el campo que FastAPI serializa. El cambio es de una sola línea).
- **Alternativa B**: Agregar `feedback_tutor` al schema Pydantic. (Rechazada: El schema es compartido con Fase 2 y el campo `feedback_error` ya existe con la semántica correcta).

### Decision 6: Consolidación de endpoint duplicado (Bug C)
- **Alternativa A**: Eliminar el segundo endpoint `POST /cerrar-rescate` (L1105-L1167) y mantener el primero (L968-L1064) que contiene la lógica completa de bypass + recálculo de porcentaje + detección de fase completada. (Seleccionada: El primer endpoint es más completo y maneja correctamente el cierre del rescate con registro de intento BYPASS_EXPLICACION).
- **Alternativa B**: Fusionar ambos endpoints. (Rechazada: El primero ya tiene toda la lógica necesaria; el segundo es redundante y más simple).

## Risks / Trade-offs

- **[Riesgo UX]**: En pantallas extremadamente pequeñas (móviles), los elementos del modal de teoría pueden quedar demasiado juntos.
  - **Mitigación**: Los media queries en `Fase4Styles.css` ya adaptan el layout a columna en pantallas de menos de 600px de ancho. Se mantendrán las reglas de responsive para asegurar que no se rompa la vista móvil.

- **[Riesgo Backend]**: Eliminar el segundo endpoint de `/cerrar-rescate` podría dejar huérfano algún flujo del frontend que lo consuma con el schema `Fase4CerrarRescate`.
  - **Mitigación**: El frontend (`Fase4Service.ts`) solo tiene una función `submitFase4CloseRescue` que llama a `POST /cerrar-rescate`. Se verificará que el frontend parsee correctamente la respuesta del endpoint consolidado.

- **[Riesgo de Regresión]**: Cambiar el campo `feedback_tutor` → `feedback_error` podría afectar al frontend si este consumiera explícitamente `feedback_tutor`.
  - **Mitigación**: El tipo `Fase4AnswerResult` del frontend define `feedback_tutor: string`, por lo que el frontend **sí espera `feedback_tutor`** — pero actualmente lo recibe vacío porque FastAPI lo descarta. Se evaluará si renombrar el campo en el schema Pydantic (agregar `feedback_tutor`) o en el frontend (cambiar a `feedback_error`).

