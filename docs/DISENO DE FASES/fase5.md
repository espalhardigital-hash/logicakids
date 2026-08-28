# Fase 5 — Fracciones, porcentajes y proporciones

> **Estado:** implementada y auditada localmente el 2026-08-27.
> **Fuente de estado:** [`ESTADO_IMPLEMENTACION_FASES_5_6.md`](../ESTADO_IMPLEMENTACION_FASES_5_6.md).
> Esta ficha sustituye especificaciones antiguas que asignaban decimales a la Fase 5.

## Propósito

El estudiante interpreta fracciones como parte de un todo y de una colección, relaciona porcentajes con representaciones visuales y resuelve razones y proporciones simples. La respuesta debe surgir del razonamiento sobre el enunciado y su visualizador, no de una pista gráfica que revele el resultado.

## Módulos

| Módulo | Foco | Visual dominante |
|---|---|---|
| 1. La fracción visual | Partes de un todo, equivalencias, término faltante, subdivisión, simplificación y detección de errores | Figura parte-todo y tiras fraccionarias comparadas |
| 2. Fracción de cantidad | Partes iguales de una colección | Rejilla de colecciones |
| 3. Porcentajes y comparación | Parte, total y lectura de barras | Gráfico de barras |
| 4. Razones y mezclas | Relaciones entre dos cantidades | Rejilla de razón |

## Contrato de interacción

1. Toda pregunta muestra un enunciado completo y una vía real para responder: alternativa o teclado numérico.
2. Cuando se solicite una respuesta decimal, el teclado ofrece el separador requerido y la validación acepta la representación normalizada.
3. Si el enunciado depende de una figura, la figura se entrega junto a él; si puede resolverse con texto, no se añade un visual decorativo.
4. Al fallar, se muestra respuesta correcta y resolución paso a paso. El estudiante permanece al menos 10 segundos en esa explicación y debe leer todas sus páginas antes de continuar.
5. No hay preguntas espejo, rescates, bypasses ni créditos de progreso por una respuesta incorrecta.
6. Práctica, desafío, teoría y retroalimentación no usan scroll vertical; contenido extenso se pagina.

## Banco y verificaciones

- **1.430 preguntas locales**, identificadas por familia y con contrato visual.
- Módulo 1/Nivel 2: **13 familias**, 9 habilidades y al menos 7 estructuras de respuesta distintas. Las tareas incluyen completar términos, inferir relaciones, leer subdivisiones, corregir equivalencias y simplificar.
- Cada visual usa `requiere_figura` y `tipo_visual`; toda figura requerida es verificable antes de publicar.
- Una equivalencia se representa como relación entre dos tiras. Los términos buscados aparecen como `?` y las equivalencias falsas marcan el dato que debe revisarse, sin exponer la operación ni la solución.
- Cierre vigente: 61 pruebas backend y 56 frontend aprobadas; auditorías profunda y narrativa sin fallos; siembra determinista verificada dos veces.

## Restricciones visuales

- SVG inline, legible y sin resultado ni procedimiento resuelto.
- Una representación debe corresponder exactamente con los valores y operación del enunciado.
- Sin marcos, colores o elementos que compitan con los datos matemáticos.
- El diseño está calibrado para computador y tableta; no se usa el scroll como alternativa de layout.
