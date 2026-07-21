## Context

El Desafío de la Fase 4 acumula intentos históricos globales en `progreso.intentos_totales` sin resetearlos a cero cuando el alumno es expulsado o al iniciar la sesión desde cero, lo que causa un error visual persistente en el frontend (`ERRORES: 61/2`). La Fase 2 cuenta con el reset absoluto que limpia `intentos_totales` y purga las tablas hijas `intento` e `intento_pregunta`, sirviendo como el patrón correcto de implementación.

## Goals / Non-Goals

**Goals:**
- Resetear `progreso.intentos_totales = 0` en el backend al ocurrir el `early_exit` en la Fase 4.
- Borrar todos los intentos históricos de la sección/desafío en las tablas `intento` e `intento_pregunta` al gatillar el `early_exit` en la Fase 4.
- Resetear `progreso.intentos_totales = 0` en `get_pregunta` de la Fase 4 cuando se crea/siembra el pool de preguntas desde cero.

**Non-Goals:**
- No se modificará el frontend ni los esquemas Pydantic para mantener la compatibilidad al 100%.

## Decisions

### 1. Reset de maestría e intentos en responder
- **Decisión:** En `responder_pregunta` de `app/fase4/router.py`, al cumplirse la condición `errores_sesion >= max_errores_desafio`:
  - Agregar `progreso.intentos_totales = 0` y `progreso.aciertos_acumulados = 0`.
  - Ejecutar queries de eliminación de intentos:
    ```python
    await db.execute(delete(Intento).where(and_(
        Intento.alumno_id == alumno.id,
        Intento.fase_id == FASE4_ID,
        Intento.seccion == seccion
    )))
    ```
    Y de la misma forma para `IntentoPregunta` cargando primero las IDs de las preguntas de la sección.
- **Razonamiento:** Alineamiento exacto con la Fase 2 y solución definitiva al residuo de intentos en base de datos.

### 2. Reset de intentos en get_pregunta
- **Decisión:** En `get_pregunta` de `app/fase4/router.py`, cuando se limpia el pool y se siembra de nuevo:
  - Establecer `progreso.intentos_totales = 0` y `progreso.aciertos_acumulados = 0` si es un desafío, para asegurar que la nueva partida comience limpia.
- **Razonamiento:** Asegura que si el alumno inicia una nueva sesión de desafío desde cero (tras aprobar o abortar), los intentos históricos no influyan.

## Risks / Trade-offs

- **[Risk] Pérdida de analíticas históricas detalladas de intentos:** Borrar registros en `Intento` descarta los clics erróneos detallados en la base de datos de producción para ese alumno en ese nivel.
  - **Mitigación:** Es un trade-off aceptable y requerido pedagógicamente para mantener el bucle limpio y coherente con las demás fases de la suite.

## Auditoría y Análisis de Fases 5 a 8

Se realizó un análisis estático de código en el backend de las Fases 5, 6, 7 y 8 (`app/fase5/router.py`, etc.) para verificar si presentaban la misma anomalía que la Fase 4:
- **Resultado:** **Las Fases 5 a 8 están libres de este problema.**
- **Evidencia:** Al gatillar la expulsión por early exit, los routers de las Fases 5, 6, 7 y 8 ejecutan de forma nativa e integrada:
  ```python
  progreso.intentos_totales = 0
  await db.execute(delete(Intento).where(...))
  ```
  Asimismo, en la carga inicial de pregunta (`get_pregunta`), estas fases también resetean `intentos_totales = 0` y limpian el historial de intentos en la base de datos, manteniéndose fieles al diseño de referencia de la Fase 2. Por tanto, el cambio se centrará exclusivamente en resolver la anomalía de la Fase 4.

