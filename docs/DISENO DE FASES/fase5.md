# Fase 5 — Fracciones, porcentajes y proporciones

> **Estado:** implementada y auditada localmente el 2026-08-23.
> **Fuente de estado:** [`ESTADO_IMPLEMENTACION_FASES_5_6.md`](../ESTADO_IMPLEMENTACION_FASES_5_6.md).
> Esta ficha sustituye especificaciones antiguas que asignaban decimales a la Fase 5.

## Propósito

El estudiante interpreta fracciones como parte de un todo y de una colección, relaciona porcentajes con representaciones visuales y resuelve razones y proporciones simples. La respuesta debe surgir del razonamiento sobre el enunciado y su visualizador, no de una pista gráfica que revele el resultado.

## Módulos

| Módulo | Foco | Visual dominante |
|---|---|---|
| 1. La fracción visual | Partes de un todo, lectura de numerador y denominador | Pizza o banda fraccionada |
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

- 1.296 preguntas locales, identificadas por familia y con contrato visual.
- Cada visual usa `requiere_figura` y `tipo_visual`; toda figura requerida es verificable antes de publicar.
- La suite específica de Fase 5 y la auditoría de fórmulas, alternativas y contrato de figura son requisitos de cierre.

## Restricciones visuales

- SVG inline, legible y sin resultado ni procedimiento resuelto.
- Una representación debe corresponder exactamente con los valores y operación del enunciado.
- Sin marcos, colores o elementos que compitan con los datos matemáticos.
- El diseño está calibrado para computador y tableta; no se usa el scroll como alternativa de layout.
