# Fase 6 — Geometría plana multiforme y áreas

> **Estado:** implementada y auditada localmente el 2026-08-23.
> **Fuente de estado:** [`ESTADO_IMPLEMENTACION_FASES_5_6.md`](../ESTADO_IMPLEMENTACION_FASES_5_6.md).
> Esta ficha reemplaza versiones históricas con contenido 3D, volumen, Tangram o magnitudes físicas, que no pertenecen a la Fase 6 vigente.

## Propósito

El estudiante reconoce propiedades de figuras planas, calcula perímetros, interpreta áreas en malla y descompone figuras compuestas. Cada pregunta muestra las medidas y la figura necesarias para resolverla, sin revelar el procedimiento.

## Módulos y niveles

| Módulo | Niveles | Aprendizaje central |
|---|---:|---|
| 1. Perímetro y borde | 4 | Lados, vértices, clasificación y perímetro de figuras planas |
| 2. Área en malla | 3 | Conteo y composición de unidades cuadradas |
| 3. Figuras compuestas | 5 | Descomposición, suma y resta de áreas |
| 4. Conversión y pantallas | 3 | Lectura de medidas, equivalencias y resolución encadenada |

Cada módulo incluye desafíos estándar, avanzado y de maestría, más un desafío mixto de fase.

## Contrato de contenido y UX

1. El banco local contiene 9.150 preguntas: 7.200 de práctica y 1.950 de desafíos.
2. Toda pregunta tiene `plantilla_id`, `requiere_figura` y `tipo_visual`; una figura requerida se inserta como SVG inline con las medidas reales de la pregunta.
3. No existen preguntas espejo, rutas de rescate ni progreso obtenido por bypass. Un error genera explicación obligatoria de 10 segundos, con respuesta correcta y pasos paginados.
4. Toda pantalla de teoría, práctica, desafío, feedback y graduación cabe sin scroll vertical. Teoría, diccionario y explicaciones largas se reparten en diapositivas.
5. Las respuestas decimales se muestran con coma. El teclado visual incorpora coma decimal y el campo acepta punto desde teclado físico.
6. La figura presenta los datos, no el resultado, la operación ejecutada ni flechas que indiquen la solución.

## Evidencia de publicación local

- 28 pruebas de contrato del banco aprobadas.
- 0 enunciados vacíos, 0 respuestas vacías, 0 figuras requeridas ausentes y 0 datos de pregunta espejo tras el resembrado.
- Backend y frontend se reconstruyen con `Datos_localhost/docker-compose.local.yml`.
