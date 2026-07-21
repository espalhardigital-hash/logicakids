## Context

La Fase 4 maneja la lógica de validación de respuestas y control de flujo mediante el uso de React hooks e interacciones en `handleSubmit`. Con el tiempo, este flujo acumuló diferencias con el patrón original y maduro de la Fase 2, provocando regresiones, ciclos infinitos (al fallar múltiples veces el espejo), y pérdida de estado al recargar la página durante una pantalla modal.

## Goals / Non-Goals

**Goals:**
- Portar de manera 1:1 los flujos de "Espejo", "Early Exit" y "Rescate" de Fase 2 hacia Fase 4.
- Desacoplar la UI de Fase 4, usando el modelo `loadNextQuestion()` de Fase 2 como única fuente de verdad.
- Proveer soporte avanzado al alumno cuando falla múltiples veces la misma pregunta, previniendo el abandono del usuario por frustración.

**Non-Goals:**
- No rediseñar la parte gráfica y estilos de la Fase 4; el UI visual permanece intacto.
- No alterar las fórmulas o el generador de preguntas de matemáticas.

## Decisions

- **Inyección de `es_espejo` en la carga**: En lugar de depender de la respuesta previa para saber si mostrar el modal de espejo, el backend inyectará este estado en la carga para que el flujo sea robusto ante recargas.
- **Implementación del Rescate Modal (Soporte Avanzado)**: Adaptaremos `Fase2RescateModal` a `Fase4RescateModal` para mostrar explicaciones enriquecidas e invocar el endpoint `/cerrar-rescate`.
- **Refactorización de `handleSubmit`**: La lógica para abrir el espejo dejará de forzar peticiones manuales al servidor. Simplemente llamará `loadNextQuestion()`, y el flujo normal de carga detectará el estado `es_espejo` desde el backend, tal cual ocurre en Fase 2.

## Risks / Trade-offs

- **Risk:** Cambiar la estructura del JSON en el backend (`Fase4PreguntaParaAlumno`) podría afectar pruebas automatizadas existentes.
  - *Mitigación:* Se agregará `es_espejo` dentro de `datos_numericos` que es un diccionario flexible y no romperá el schema.
- **Risk:** Los límites de iteración del bucle espejo deben coincidir entre ambos endpoints en `router.py`.
  - *Mitigación:* Usaremos la misma constante `MAX_ESPEJO` existente en `Fase2` y `Fase4`.
