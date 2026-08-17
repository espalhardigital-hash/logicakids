# Estado final de la reformulación — LogicaKids (para tu varredura)

> Rama `mejoras-fases-5-9` (no toca `producion`). App viva en `localhost:3000`.
> 9 fases sembradas · **101 tests en verde** · backend+frontend HTTP 200.

## 1. Lo que quedó COMPLETO y verificado (todas las fases)

| Área | Estado |
|---|---|
| **"Misma pregunta cambiando el nombre" (clones)** | ✅ **Eliminado en fases 4,5,6,7,8,9** (0 familias con enunciado repetido). Causa raíz en Fase 4: valores solo por `fam_idx` → ahora también por `var_idx`. Fases 7/8: dedup por familia. |
| **Integridad estructural** | ✅ 0 `tipo_error` inválido · 0 opciones duplicadas · 0 doble-correcta (todas las fases). |
| **Progreso P1** (rendirse no suma) | ✅ Fases 4, 5, 6, 7. |
| **Salida honrosa** (fallar un desafío NO resetea ni bloquea) | ✅ Fases 4, 5, 6, 7. |
| **Refuerzo al fallar** (solución paso a paso → reformulación, máx 2, luego avanza) | ✅ Fase 5 (motor nuevo). |
| **Teoría real** (no placeholder) | ✅ Fase 5 (12 niveles). Fix crítico: `get_lectura` daba 500 siempre (faltaba import). |
| **Figuras/visualizadores** | ✅ Fase 5 emite `tipo_visual` (pizza/beaker/…); Fase 6 figura de polígono corregida (coincide con la respuesta). |
| **Simulados (Fase 9)** | ✅ **39 preguntas reales del CMRJ** traducidas y verificadas (antes: 3 hardcodeadas, una en portugués). |
| **Fase 8 y 9 sembradas** | ✅ Antes NO se sembraban (imports rotos en el maestro) y Simulados estaba tapado por otro router. Corregido. |
| **Enum crash Fase 5** | ✅ Corregido (500 en cada respuesta incorrecta). |

## 2. Preguntas reales del CMRJ incluidas (por temario, en cada fase)
Del banco Pedro II (`04_Banco_Transcribido`), traducidas al español y verificadas:
- **Simulados (Fase 9):** 19 preguntas reales (examen mixto).
- **En el desafío final de cada fase temática** (`app/content/banco_cmrj.py` →
  `seed_banco_cmrj`, cableado en el seed maestro, idempotente): **19 anclas**
  repartidas — Fase 4 (2), Fase 5 (5), Fase 6 (6), Fase 7 (2), Fase 8 (4).
  Temas: MDC/Euclides, MDC×MMC, divisibilidad, relación de Euler, corona
  circular, balanza, fracción del resto multi-paso, %, tipos sanguíneos, dados,
  perímetros, volumen/capacidad, decimal↔fracción, etc.
- **Pendiente:** el grueso de las 276 fotos + docx 2013-2025 sigue sin
  transcribir (requiere lectura por lotes de las imágenes) — es la expansión de
  contenido que falta para "todas" las preguntas.

## 3. Conteo actual por fase
Fase 1: 400 · 2: 8470 · 3: 9600 · 4: 5406 · 5: 996 · 6: 9150 · 7: 960 · 8: 720 · 9: 200.

## 4. Frontera pendiente (contenido, honesto)
La **maquinaria, la limpieza y la escalera pedagógica están completas**. Lo que
NO está al 100% es la **autoría de contenido profundo a nivel CMRJ en cada
fase**: incorporar el grueso de las **276 fotos + el docx de exámenes
2013-2025** como arquetipos por tema, y la **QA visual** (confirmar figura↔
enunciado por plantilla, que requiere ojos humanos). Está planificado en
`Plan_Banco_CMRJ.md`. Los desafíos ya generan problemas multi-paso con
distractores-trampa (verificado en Fase 4), así que la base es sólida.

## 5. Para tu varredura
- Entra a `localhost:3000` (Ctrl+F5). Prueba una fase: teoría al entrar →
  práctica (figura + al fallar, solución + reformulación con otro contexto) →
  desafío (no debe resetear al fallar) → Simulados (Fase 9) con preguntas CMRJ.
- Dime qué falla / qué refactorizar y lo ataco puntual.

## 6. Herramientas dejadas
`LogicaMath/backend/_local_runner.py` (crear esquema + sembrar una fase sin
Docker) y `_audit_fase.py` (auditoría de arquetipos por fase). Borrables.
