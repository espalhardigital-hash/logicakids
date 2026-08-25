# Estado de implementación — Fases 5 y 6

> **Estado:** vigente y verificable en el entorno local.
> **Actualización:** 2026-08-23.
> **Alcance:** `fase_id=5` y `fase_id=6`. Este documento prevalece sobre planes de reconstrucción previos cuando describan un mecanismo ya retirado.

## Decisiones pedagógicas vigentes

1. **No existen preguntas espejo.** Se retiraron del backend, frontend, datos y rutas de Fases 5 y 6. Una variante de valores no es una pregunta espejo: no se sirve como reacción a un error ni comparte una secuencia de reintentos.
2. **Error = corrección obligatoria.** Ante una respuesta incorrecta, el estudiante ve la respuesta correcta y los pasos de resolución. El botón para continuar permanece bloqueado durante **10 segundos** y, cuando hay varios pasos, exige recorrer todas las páginas.
3. **El error no acredita dominio.** El progreso de práctica se obtiene solo con aciertos reales; no existe bypass de explicación ni avance por rendirse.
4. **Cero scroll vertical.** Las pantallas de práctica, teoría, retroalimentación y graduación no desplazan verticalmente. La teoría, diccionario y explicaciones extensas se dividen en diapositivas.
5. **Contrato visual por pregunta.** Toda pregunta declara una familia (`plantilla_id`) y si requiere figura (`requiere_figura`, `tipo_visual`). Si la figura es necesaria, viaja con el enunciado como SVG inline y no revela el resultado.

## Fase 5 — Fracciones, porcentajes y proporciones

- Banco local: **1.296 preguntas**; 12 familias por cada nivel de práctica y desafíos.
- Visuales: pizza/fracción, rejilla de colecciones, gráfico de barras y rejilla de razones según el objetivo matemático.
- Entrada: teclado numérico con separador decimal cuando la respuesta lo requiere.
- Verificación ejecutada: 46 pruebas de Fase 5 aprobadas; auditoría de enunciado, respuesta, fórmula, alternativas y contrato visual sin hallazgos.

## Fase 6 — Geometría plana multiforme y áreas

- Banco local: **9.150 preguntas**: 7.200 de práctica (15 niveles × 120 familias × 4 variantes contextuales) y 1.950 de desafíos (13 bloques × 150).
- Cada registro posee `plantilla_id`, `requiere_figura` y `tipo_visual`; las figuras requeridas son SVG inline coherentes con el enunciado.
- El teclado visual ofrece **coma decimal**; el campo también acepta punto desde teclado físico. La base contiene 1.920 respuestas decimales con coma.
- Verificación ejecutada: 28 pruebas de contrato aprobadas; auditoría local con 0 enunciados vacíos, 0 respuestas vacías, 0 figuras requeridas ausentes y 0 datos espejo.

## Operación local

Los servicios locales se ejecutan desde `Datos_localhost/docker-compose.local.yml`:

```powershell
docker compose -f D:\Antigravity\APP_Logica_Matematicas_kids\Datos_localhost\docker-compose.local.yml up -d --build
```

- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- Base PostgreSQL local: puerto `5433`

Para resembrar Fase 6 localmente:

```powershell
docker exec logicakids_local_backend python -c "import asyncio; from app.fase6.seed import seed_fase6_full; asyncio.run(seed_fase6_full())"
```

> La siembra de Fase 6 purga únicamente los datos de `fase_id=6`; no debe ejecutarse contra un entorno con progreso de alumnos que se quiera conservar.

## Evidencia mínima para cambios posteriores

1. Ejecutar la suite específica de la fase modificada.
2. Reconstruir backend y frontend locales.
3. Auditar la base real: enunciado, respuesta, `plantilla_id`, `tipo_visual`, figura requerida y ausencia de `es_espejo`.
4. Comprobar visualmente la matriz práctica, desafío, teoría y corrección bloqueada en pantalla de escritorio o tableta.
