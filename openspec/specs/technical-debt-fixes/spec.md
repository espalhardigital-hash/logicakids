# technical-debt-fixes Specification

## Purpose
TBD - created by archiving change deuda-tecnica-auditoria-codigo. Update Purpose after archive.
## Requirements
### Requirement: Borrado Consistente de Archivos en S3
El sistema SHALL extraer correctamente la clave (Key) completa de S3 para cualquier URL pública proporcionada al método `delete_file`, preservando cualquier prefijo de subdirectorio (ej. `graphics/`) para asegurar que la eliminación física del objeto en S3/MinIO no falle silenciosamente ni deje huérfanos.

#### Scenario: Eliminar archivo didáctico organizado en subdirectorios
- **WHEN** el servicio de storage intenta eliminar el archivo de imagen de URL `http://localhost:9100/graphics/fase4/pregunta.png`
- **THEN** el sistema SHALL resolver la clave de S3 como `graphics/fase4/pregunta.png` y llamar exitosamente a `delete_object` del cliente S3.

### Requirement: Validación Contextual Robusta para Objetos Discretos
El validador de parámetros didácticos del frontend SHALL garantizar que, cuando un tipo de objeto es de clase `discreto` e indivisible y no se permiten decimales, los parámetros numéricos resultantes sean siempre enteros. Si la búsqueda heurística inicial en un rango de delta pequeño (< 15) no encuentra una solución exacta, el sistema SHALL aplicar un mecanismo de fallback infalible para forzar que el parámetro `cantidadPorCaja` sea múltiplo del divisor.

#### Scenario: Fallo heurístico inicial de corrección de enteros
- **WHEN** la búsqueda heurística inicial falla en encontrar un delta idóneo menor a 15
- **THEN** el validador SHALL aplicar la fórmula de fallback calculando la cantidad corregida como el múltiplo exacto de `divisor` mayor o igual a `cantidadPorCaja`.

### Requirement: Segmentación Flexible de Enunciados Multi-Paso
El validador del frontend SHALL admitir enunciados con terminadores de oración flexibles (como signos de exclamación `!`, interrogación `?`, saltos de línea `\n` o puntos seguidos directamente de texto sin espacio) al segmentar el texto para flujos de dos pasos.

#### Scenario: Segmentación de enunciado con salto de línea y signos de puntuación
- **WHEN** se segmenta un enunciado de dos pasos que contiene saltos de línea y signos de interrogación
- **THEN** el sistema SHALL dividir la oración usando una expresión regular flexible, asignando la primera frase con su signo de puntuación al Paso 1 y el resto de la cadena al Paso 2.

