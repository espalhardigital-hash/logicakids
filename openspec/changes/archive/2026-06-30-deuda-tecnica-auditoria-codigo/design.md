## Context

La auditoría técnica identificó tres problemas de software críticos:
1. Fallos en el borrado de almacenamiento S3 cuando las URLs usan subdirectorios.
2. Inconsistencia numérica en el frontend que permite mostrar cantidades decimales ("3.5 manzanas") en enunciados discretos si la búsqueda por delta inicial falla.
3. Fallo en la división de enunciados para problemas de dos pasos cuando el enunciado usa saltos de línea (`\n`), puntos sin espacio, o signos `?`/`!`.

## Goals / Non-Goals

**Goals:**
- Resolver de manera robusta el parseo de la clave S3/MinIO para borrado de archivos, garantizando que incluya subdirectorios.
- Asegurar de forma infalible que las preguntas de objetos discretos indivisibles no muestren decimales en la interfaz del alumno.
- Hacer más flexible la división de oraciones en enunciados del Tutor Invisible (Paso 1 y Paso 2).

**Non-Goals:**
- Cambiar la base de datos o modificar la lógica de persistencia de MinIO.
- Rediseñar el flujo del motor de plantillas o los generadores matemáticos del backend.

## Decisions

### Decisión 1: Parseo de la clave S3 con urllib.parse
- **Opción A (Recomendada):** Utilizar `urllib.parse.urlparse` para extraer el path de la URL del recurso de MinIO/S3. Si el path empieza con el nombre del bucket (`/bucket_name/`), eliminar el prefijo para extraer la clave (Key) exacta de objeto, incluyendo todas las subcarpetas del storage.
- **Alternativa Considerada:** Usar RegExp complejas. Rechazada debido a la fragilidad frente a cambios de host (localhost, IP o nombres de dominio de producción).

### Decisión 2: Fallback Matemático para Evitar Decimales en Objetos Discretos
- **Opción A (Recomendada):** Si la heurística de búsqueda de delta menor a 15 no encuentra un factor válido, aplicar un fallback automático asignando `cantidadCorregida = Math.ceil(cantidadPorCaja / divisor) * divisor` (o `Math.floor` si da mayor al límite superior). Al ser la cantidad por caja un múltiplo exacto del divisor, el total de objetos siempre será divisible por el divisor, asegurando respuestas enteras.
- **Alternativa Considerada:** Aumentar el límite de delta a 100. Rechazada porque no garantiza matemáticamente al 100% que se encuentre una solución si el divisor es muy grande o la cantidad muy pequeña.

### Decisión 3: Segmentación Flexible con Expresiones Regulares
- **Opción A (Recomendada):** Reemplazar `enunciadoTemplate.split(". ")` por `enunciadoTemplate.split(/(?<=[.?!])(?:\s+|\n+)/)`. Esta expresión regular divide por cualquier terminador de oración (`.`, `?`, `!`) seguido de cualquier espacio en blanco o salto de línea, utilizando un lookbehind positivo para conservar el signo de puntuación en la oración de origen.
- **Alternativa Considerada:** Hacer splits sucesivos con diferentes delimitadores. Rechazada por su excesiva complejidad e ineficiencia de código.

## Risks / Trade-offs

- **[Riesgo]** En la decisión 2, forzar la cantidad por caja a un múltiplo del divisor mediante `Math.ceil` podría generar un número de objetos considerablemente mayor al esperado en enunciados con cantidades bajas.
  - *Mitigación:* Se utilizará la opción de redondeo hacia arriba o hacia abajo que resulte en un valor positivo distinto de cero más cercano a la cantidad original.
