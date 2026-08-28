# Contrato de progresión de práctica

> **Estado:** normativo y vigente desde 2026-08-28.
> **Alcance:** niveles de práctica de las fases implementadas 1–9. Los simulacros y desafíos conservan su configuración propia.

## Regla única

1. Un nivel de práctica se completa al alcanzar **10 aciertos reales**.
2. La interfaz muestra `PROGRESO n/10` y `CORRECTAS n`, usando el mismo contador persistido por el backend.
3. El porcentaje es `min(100, aciertos × 10)`. Nunca se muestra un valor superior a `10/10` ni un porcentaje superior a 100%.
4. El décimo acierto aprueba el nivel inmediatamente. No se exige una pregunta 11 o 12 para cerrar.
5. Una respuesta incorrecta, una explicación, un bypass o una familia ya resuelta no incrementan el contador de aciertos.
6. La cobertura de familias pertenece a la auditoría del banco; no es una segunda condición invisible para aprobar al estudiante.
7. Las filas de práctica usan `cantidad_requerida=10` y `porcentaje_aprobacion=100`. El valor global del panel administrativo usa el mismo contrato.

## Alcance de datos

Son práctica las secciones `100–999`, la sección por defecto `0` y las cuatro filas heredadas `fase_id=1, seccion=1`. Las secciones de desafío (`>=1000`, incluidas las mixtas `99099`) no se normalizan y conservan sus cantidades, tiempos y tolerancias.

La normalización local se ejecuta de forma idempotente con:

```powershell
docker compose -f Datos_localhost/docker-compose.local.yml exec -T backend python -m scripts.normalize_practice_progress_goal
```

El proceso preserva estados ya aprobados, limita contadores históricos superiores a 10, aprueba progresos que ya tenían al menos 10 aciertos y no modifica preguntas, intentos ni configuraciones de desafío.

## Precedencia documental

Este contrato reemplaza cualquier referencia histórica a 15 o 50 preguntas de práctica, a aprobación con 80/90%, o a `COUNT(DISTINCT estructura_padre_id)` como condición de avance. Esas cifras pueden seguir apareciendo en planes históricos no normativos; no deben volver a implementarse.

## Evidencia de cierre — 2026-08-28

- Configuraciones activas normalizadas: **117** filas de práctica en fases 1–8, incluidas las cuatro filas heredadas de fase 1.
- Configuraciones de práctica inválidas después de la migración: **0**.
- Progresos con más de 10 aciertos después de la migración: **0**.
- Pruebas backend transversales: **146 aprobadas**.
- Pruebas frontend: **61 aprobadas**.
- Compilación TypeScript y build Vite de producción: **aprobados**.
