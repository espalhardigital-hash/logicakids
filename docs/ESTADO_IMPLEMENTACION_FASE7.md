# Estado de implementación — Fase 7

> **Estado:** vigente y verificable en el entorno local.
> **Actualización:** 2026-08-23.
> **Alcance:** `fase_id=7`, Coordenadas, rutas y tiempo.

## Reglas aplicadas

1. No hay preguntas espejo, rutas de rescate ni bypass de explicación publicados para esta fase.
2. Una respuesta incorrecta muestra la respuesta correcta y su resolución; el botón para continuar se habilita después de **10 segundos** y de recorrer todas las páginas de la explicación.
3. Un error no acredita dominio. El progreso solo cuenta aciertos reales.
4. Las pantallas de juego, teoría, corrección y graduación no usan scroll vertical. La teoría se presenta como diapositivas de dos párrafos; el diccionario y los ejemplos también se dividen en páginas.
5. Cada pregunta declara `plantilla_id`, `requiere_figura`, `tipo_visual` y, cuando se requiere, una `url` SVG autocontenida que la pantalla muestra junto al enunciado.

## Banco publicado localmente

- **960 preguntas** en 24 secciones: 12 niveles de práctica (60 preguntas / 20 familias por nivel) y 12 desafíos (25 preguntas en desafíos 1 y 2; 10 en desafío 3).
- Todos los ítems tienen enunciado, respuesta, alternativas distintas, familia identificable y figura SVG disponible.
- Los visuales corresponden al contenido: brújula y giros, rutas y plano cartesiano, reloj y suma de duración, horarios y rutas de transporte.
- Auditoría tras la siembra: 0 banderas `es_espejo`, 0 familias faltantes y 0 figuras requeridas sin recurso.

## Verificación realizada

- `pytest -q tests/test_fase7_content_contract.py`: **48 pruebas aprobadas**.
- Compilación de frontend de producción: aprobada.
- API local: `/fase7/responder` publicada y `/fase7/cerrar-rescate` ausente del OpenAPI.
- Docker local activo: frontend `http://localhost:3000`, backend `http://localhost:8000`.

## Operación local

Para resembrar exclusivamente esta fase:

```powershell
docker exec logicakids_local_backend python -m app.fase7.seed_fase7
```

> La siembra elimina y reconstruye únicamente los datos y progreso de `fase_id=7`; no debe ejecutarse si se necesita conservar ese progreso de alumnos.
