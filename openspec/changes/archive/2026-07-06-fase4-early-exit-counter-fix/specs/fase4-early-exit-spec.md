## ADDED Requirements

### Requirement: Consistencia del Reset de Desafío en Fase 4
El backend de la Fase 4 SHALL implementar el comportamiento de reset absoluto por salida temprana (early exit) de forma idéntica a la Fase 2, garantizando que el contador de intentos históricos se restablezca a cero al reiniciarse el progreso.

#### Scenario: Reinicio completo de progreso por límite de errores superado
- **WHEN** el alumno comete una cantidad de errores en la sesión mayor o igual al límite permitido en el Desafío
- **THEN** el sistema SHALL establecer a `0` los aciertos, el porcentaje y los intentos totales de maestría, eliminar las filas de intentos de esa sección en `intento` y en `intento_pregunta`, y retornar el progreso reiniciado.
