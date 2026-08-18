# Plan (REDISEÑADO) — Banco CMRJ, Simulacros y "Desafío Simulacro"

> **Rediseño 2026-08-18.** Docker está arriba (stack local 6 contenedores) →
> re-seed y verificación EN VIVO restaurados. Además se confirmó que **puedo leer
> las imágenes/PDF directamente** (render PDF→PNG con `pymupdf`), sin depender del
> OCR ruidoso del docx. Esto cambia la estrategia de fuentes.
> **Modo:** ejecución autónoma de inicio a fin, commit por lote, sin pedir permiso.

## Qué cambió respecto al plan anterior
1. **Docker vivo** → cada lote se siembra y se verifica contra la BD real, y el
   redeploy aplica el banco (seeder ya cableado en el maestro).
2. **Fuentes re-jerarquizadas** (tras inspeccionar el material):
   - `CMRJ PRUEBAS ANOS ANTERIORES/*.pdf` y `Colegio Pedro II/*.pdf` = **exámenes
     reales del CMRJ/Pedro II por año** (prova mat. 6º ano 2013-2019, pruebas
     2020/2022-2025, Pedro II 2017-2024). Son PDF **limpios y estructurados** con
     20 preguntas objetivas (A)-(E) c/u. → **fuente de SIMULACRO (nivel 3)**.
   - `01_Fotos_Normalizadas/` (277) = páginas de **libro didáctico** con gabarito
     (respuesta en rojo). Mayoría **nivel fundamental** (numeración romana,
     propiedades, etc.). → **fuente de FAMILIARIZACIÓN (niveles 1-2)**, verificable.
   - `04_Banco_Transcribido/` = ya incorporado (anclas actuales).
3. **Método de lectura:** `pymupdf` renderiza cada página del PDF a PNG (dpi 150)
   → se lee visualmente (fiel, incluye figuras) → se resuelve → se **verifica el
   cálculo** → se traduce a español (contexto neutro) → se estructura.

## Fuente de verdad del banco
- **`app/content/banco_cmrj.py`** — banco curado por `fase → módulo → nivel`
  (`familiariza` | `simulacro`). Cada ítem: enunciado_es, correcta,
  distractores[3], explicacion (pasos), tema, dificultad(1-3), nivel, tipo_visual?.
  Hoy: **25 preguntas verificadas** (fases 4-8), 0 mal formadas, **vivas en BD**.
- **`app/fase11/banco_simulados.py` / `seed_fase9.py`** — Simulados (Fase 9): hoy
  39 preguntas reales; se amplía con los exámenes por año.
- **Inyector `seed_banco_cmrj`** (cableado en `app/seed.py`, idempotente): reparte
  `simulacro → desafío del módulo (mod*1000+13)`; `familiariza → práctica
  (mod*100+3)`. Verificado en vivo (25/25 colocadas, 0 mal formadas).

## Decisiones (default recomendado; revisables)
- **D1 — Prioridad:** primero los **exámenes reales** (mayor valor CMRJ, más
  limpios) → simulacros + anclas por módulo; luego las **fotos** → familiarización.
- **D2 — Idioma/contexto:** todo español, contexto neutro (nombres → neutros;
  R$ → "monedas"/"reales" según convenga). Se conserva la matemática exacta.
- **D3 — Verificación obligatoria (D7 anterior):** cada pregunta con **respuesta
  reproducida a mano**; se descarta lo no verificable o que dependa de una figura
  no reconstruible. Nunca se inyecta una respuesta dudosa en una app para niños.
- **D4 — Figuras:** visualizadores paramétricos de la app; para figuras críticas,
  SVG propio en español (no reuso SVG portugués que revele la respuesta). Sin
  figura reconstruible y crítica → se descarta.
- **D5 — Progresión:** simulacro = nivel 3 (CMRJ real). Familiarización = niveles
  1-2, mismo tema/estructura, números más amables (NO clones por valor).
- **D6 — "Desafío Simulacro":** las preguntas simulacro entran al **desafío del
  módulo** (alcanzable hoy). Sección UI dedicada = mejora opcional posterior.
- **D7 — Dedup:** por enunciado normalizado (no repetir lo ya transcrito).

## Etapas (autónomas, commit por lote)
- **E1 · Exámenes de matemática CMRJ (PDF) por año** — render→leer→verificar→
  traducir→estructurar. Empezar por 2019, 2018, 2017… → banco_simulados (Fase 9)
  + anclas simulacro por módulo/fase temática. Lote = 1 examen (~20 preguntas).
- **E2 · Exámenes Pedro II (2017-2024)** — íd.
- **E3 · Fotos de libro (familiarización)** por lotes de ~10 → niveles 1-2 por tema.
- **E4 · Redeploy + verificación en vivo** tras cada lote (conteos, 0 mal formadas,
  lectura ORM ok, sin dobles-correctas).
- **E5 · (Opcional) Sección "Desafío Simulacro"** con UI dedicada.

## Registro de avance
- ✅ Docker vivo; banco (25) vivo tras redeploy; frontend 200.
- ✅ Método PDF→PNG validado (CMRJ mat. 2019 Q01=25→(A), Q02=9→(B) verificadas).
- ⏳ En curso: E1 (exámenes de matemática por año).
