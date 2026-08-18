# Plan — Banco CMRJ completo, Simulacros y "Desafío Simulacro"

> **Modo:** ejecución autónoma de inicio a fin (sin esperar aprobación entre
> lotes). El usuario revisará por la noche. Este doc fija el plan y las
> **decisiones tomadas con default recomendado** (revisables después).
> **Fecha:** 2026-08-17.

## Objetivo
1. **Incorporar TODAS las preguntas** de las fotos (`01_Fotos_Normalizadas`, 276)
   y del docx de exámenes 2013-2025.
2. **Desarrollar preguntas** basadas en las fotos (mismo corte, no clones).
3. **Simulacros**: traer los exámenes por año → Simulados (Fase 9).
4. **Escalera de familiarización**: preguntas *similares al simulacro pero de
   menor dificultad*, distribuidas en las fases/módulos, para que al llegar al
   simulacro el nivel no sea 100% extraño.
5. **Sección "Desafío Simulacro"** por módulo: 2 preguntas profundas nivel
   simulacro que el alumno resuelve antes de pasar; si no puede, se le da la
   explicación paso a paso.

## Arquitectura
- **`app/content/banco_cmrj.py`** (ya existe) crece hasta contener TODO el banco,
  organizado `por fase → por tema → por dificultad (1..3) → nivel
  (practica|simulacro)`. Cada ítem: enunciado_es, correcta, distractores[3],
  explicacion (pasos), tema, dificultad, nivel, tipo_visual opcional.
- **Importador** `seed_banco_cmrj` (ya cableado en el maestro) reparte:
  - dificultad 1-2 (practica) → pool de práctica del módulo correspondiente.
  - dificultad 3 (simulacro) → nueva sección **"Desafío Simulacro"** del módulo
    (2 preguntas) + Simulados (Fase 9).
- **Sección "Desafío Simulacro"**: `seccion = modulo*100 + 9` (109, 209, 309,
  409…) por fase, con 2 preguntas nivel simulacro. Config con umbral y el
  refuerzo paso-a-paso ya existente (mostrar solución al fallar).
- **Simulacros (Fase 9)**: se amplía con los exámenes por año del docx.

## Decisiones tomadas (default recomendado; revisables)
- **D1 — Fuente de fotos:** `01_Fotos_Normalizadas` (276) como canónica (las
  WhatsApp son duplicados). Proceso por **lotes de ~12**.
- **D2 — Idioma:** todo al **español**, contexto neutro (nombres brasileños →
  neutros; R$ se mantiene como moneda del enunciado o se neutraliza a "monedas").
- **D3 — Figuras:** visualizadores paramétricos de la app cuando aplique; para
  figuras críticas (plantas, gráficos de sectores) genero **SVG propio en
  español** (no reuso los SVG portugueses que revelan la respuesta). Preguntas
  sin figura crítica → solo texto.
- **D4 — Dificultad:** simulacro = **nivel 3** (CMRJ real); las "similares de
  menor dificultad" = **niveles 1-2**, mismo tema/estructura, números más
  amables, distribuidas en los niveles bajos del módulo.
- **D5 — "Desafío Simulacro":** sección nueva por módulo con **2 preguntas**
  nivel simulacro; al fallar se muestra la explicación paso a paso (refuerzo ya
  existente). Backend primero; integración de UI se documenta si requiere
  frontend.
- **D6 — Deduplicación:** por enunciado normalizado (evitar repetir lo ya
  transcrito en `04_Banco_Transcribido`).
- **D7 — Verificación:** cada pregunta con respuesta **verificada** (cálculo
  reproducido); descarto las que no pueda verificar o que dependan de una figura
  que no puedo reconstruir.

## Etapas (todas autónomas)
- **E1 · Procesar las 276 fotos por lotes** (~12/lote): extraer todas las
  preguntas legibles → traducir → estructurar → append a `banco_cmrj.py`
  (por fase/tema/dificultad/nivel). Commit por lote.
- **E2 · Procesar el docx** (exámenes por año) → simulacros → ampliar Fase 9.
- **E3 · Escalera de familiarización:** por cada arquetipo simulacro, versión(es)
  de menor dificultad distribuidas en niveles 1-2 de la fase.
- **E4 · Sección "Desafío Simulacro"** por módulo (2 preguntas nivel 3) — seed +
  config + (si aplica) router/frontend.
- **E5 · Verificación integral + redeploy.**

## Registro de avance (se actualiza por lote)
- (pendiente de iniciar E1)
