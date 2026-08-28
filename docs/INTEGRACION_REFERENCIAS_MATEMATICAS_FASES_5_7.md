# Integración de referencias matemáticas — Fases 5 a 7

**Estado:** implementado y verificado localmente el 2026-08-27.

## Alcance

Las imágenes de referencia se usaron como inspiración pedagógica y visual; no se distribuyen ni se vinculan como activos de la aplicación. La integración crea familias nuevas, generativas y auditables, no copias literales.

| Fase | Aporte incorporado | Representaciones nuevas |
|---|---|---|
| 5 — Fracciones, porcentajes y proporciones | Parte-todo, equivalencias, grupos, porcentajes, tablas y razones | tiras fraccionarias, grupos, cuadrícula de 100, tabla de datos y tabla de razón |
| 6 — Geometría plana y áreas | Lectura de figuras, perímetro y área | malla, triángulo, círculo, paralelogramo, rombo, trapecio y figuras compuestas coherentes |
| 7 — Coordenadas, rutas y tiempo | Rutas, duración y lectura espacial | rutas neutrales y relojes sin revelar el resultado |

## Garantías conservadas

- No hay preguntas espejo en las fases intervenidas.
- Un error muestra explicación y mantiene la corrección obligatoria de diez segundos.
- Las figuras no incluyen la respuesta, la ruta ganadora ni el total calculado.
- Las gráficas son SVG/HTML compactos; los retos permanecen en una ventana fija sin scroll vertical.
- Si el enunciado necesita una figura, la figura viaja con la pregunta y es validada por contrato.

## Volumetría local tras resembrado

- Fase 5: **1.430** preguntas. El bloque de equivalencias de Módulo 1/Nivel 2 quedó compuesto por 13 familias y 9 habilidades observables; se retiraron las operaciones artificiales que reducían el reto a una multiplicación visible.
- Fase 6: **9.150** preguntas; se corrigieron contradicciones entre figura y enunciado en perímetros, áreas y circunferencias.
- Fase 7: **960** preguntas; se eliminaron revelaciones visuales de totales y rutas correctas.

## Evidencia de verificación

- Backend Fase 5: `61 passed` en contratos de contenido, semántica, vocabulario, teoría y banco.
- Frontend completo: `56 passed`; incluye los visuales de equivalencia con términos faltantes y corrección de equivalencias falsas.
- Auditorías profunda y narrativa de Fase 5: cero fallos.
- Compilación de producción del frontend aprobada y contenedores locales redesplegados.

## Deuda explícitamente no ampliada

La renumeración histórica de las fases 8–11 no se mezcla con esta entrega. La Fase 7 local sí quedó identificada como **Coordenadas, Rutas y Tiempo**, que coincide con su contenido publicado. Cualquier ajuste de 8–11 debe seguir una migración canónica separada.
