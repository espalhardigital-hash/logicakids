# Plan — De motor generador a Banco Curado de preguntas CMRJ

> **Documento de análisis y plan (no se implementa hasta acordar).**
> **Contexto:** el motor que *generaba* preguntas (compositor) fracasó en diseño:
> produce preguntas mal estructuradas y poco naturales. Se adopta otra
> metodología: un **banco curado de preguntas reales** del examen CMRJ / Colégio
> Pedro II, traducidas al español, con sus figuras, organizadas por temario y
> repartidas en las fases.
> **Fecha:** 2026-08-17.

---

## 1. Análisis del material aportado (`Pedro II/`)

| Carpeta | Contenido | Estado |
|---|---|---|
| `04_Banco_Transcribido/` | **11 bloques temáticos** en Markdown, con ejercicios ya estructurados (ID, **Fase Destino**, enunciado, **Gabarito oficial**, explicación, refs a figura). | **41 ejercicios** transcritos (Bloque 1 = 16; resto 2-4 c/u). **Parcial** — es un excelente arranque, no está completo. |
| `01_Fotos_Normalizadas/` | 276 fotos de ejercicios (fuente original). | Materia prima; la mayoría aún sin transcribir. |
| `02_Figuras_Recortadas/` | 44 figuras recortadas (nombres descriptivos: poliedros, fracciones, gráficos…). | JPG. |
| `03_Figuras_SVG/` | 6 figuras vectorizadas. | Solo 6 de 44 pasadas a SVG. |
| `Fotos para logicakids/` | ~280 fotos WhatsApp (originales). | Materia prima. |
| `Compendio…2013_2025.docx` | Exámenes CMRJ completos 2013-2025 (~671 párrafos, preguntas + gráficas por año). | 60 MB; fuente enorme de preguntas reales por año. |

**Formato de cada ejercicio (ya muy bueno):**
```
### [EX_045_16] Representación Gráfica y Fracciones Equivalentes
- Fase Destino: Fase 2
- Enunciado: "Escreva a fração que representa a parte sombreada..."  (PORTUGUÉS)
- Gabarito Oficial: Círculo 3/8; Barra 2/5
- Recorte: FIG_EX_045_FRACAO_PIZZA_BARRAS.jpg
- Componente SVG: SVG_EX_045_FRACAO_PIZZA_BARRAS.svg
```

**Temario de los 11 bloques:** 1) Sistemas de numeración y operaciones · 2)
Geometría espacial/poliedros · 3) Teoría de números (MMC/MDC/Euler) · 4)
Fracciones · 5) Problemas verbales/decimales · 6) Concursos/olimpiadas · 7)
Magnitudes (capacidad/masa/volumen) · 8) Geometría plana/áreas · 9)
Rectas/ángulos/perímetros/tiempo · 10) Estadística/gráficos/probabilidad · 11)
Porcentajes/finanzas.

---

## 2. El giro metodológico

**Antes:** compositor genera preguntas desde plantillas+valores → resultó
artificial y mal estructurado.

**Ahora:** las preguntas son **reales, curadas y traducidas**; se guardan en la
BD como banco. El backend deja de *inventar* y pasa a *servir* preguntas de
calidad.

### Lo que se REUTILIZA (clave: el trabajo de reformulación NO se pierde)
El motor pedagógico que ya construimos es **independiente de cómo nazcan las
preguntas** y se conserva tal cual:
- **Refuerzo al fallar** (mostrar solución paso a paso → reformulación).
- **Progreso P1** (solo el acierto real cuenta).
- **Salida honrosa** en desafíos (sin reset ni bloqueo).
- **Teoría** por nivel y **visualizadores** (pizza/beaker/…).

Solo cambia **la fuente de las preguntas**: en vez del compositor, un
importador que lee el banco curado. Las "reformulaciones" de una familia pasan a
ser **2-3 preguntas reales del mismo concepto** (curadas), no variantes
generadas.

---

## 3. Arquitectura propuesta

### 3.1 Formato fuente único (banco en el repo)
Convertir los bloques Markdown a un formato **estructurado y validable** (JSON o
YAML) por ejercicio, p.ej. `content/banco_cmrj/<tema>.json`:
```json
{
  "id": "EX_045_16",
  "tema": "fracciones",
  "fase_destino": 5,
  "dificultad": 2,
  "enunciado_es": "Escribe la fracción que representa la parte sombreada...",
  "tipo": "multiple_opcion",
  "alternativas": [{"texto":"3/8","correcta":true}, ...],
  "respuesta": "3/8",
  "explicacion_pasos": ["...", "..."],
  "figura": {"svg":"...", "img":"graphics/ex_045.png"},
  "origen": "CMRJ 2019 Q12"
}
```

### 3.2 Importador (reemplaza al compositor en el seed)
Un `seed` que lee `content/banco_cmrj/*.json` y crea `Pregunta`+`Alternativa`
en la BD, agrupando por concepto en familias (para el refuerzo). El compositor
queda deprecado (o como respaldo hasta migrar todo).

### 3.3 Figuras
- Preferir **SVG** (nítidas, ligeras, ya hay 6). Convertir las 44 recortadas a
  SVG progresivamente, o embeber el JPG como imagen mientras tanto (`tipo_visual:
  imagen` ya soportado).

---

## 4. Decisión grande: estructura de temario ↔ fases

El banco propone su propio mapa ("Fase Destino": aritmética=1, fracciones=2,
álgebra=3, lógica=4…), que **no coincide** con las fases actuales de la app
(donde, p.ej., fracciones = Fase 5). Hay que decidir:

- **Opción T1 — Reordenar las fases al temario CMRJ** (recomendada a futuro): las
  9 fases pasan a reflejar la progresión del examen (numeración → fracciones →
  teoría de números → geometría → magnitudes → estadística/prob → …). Es el
  orden pedagógico real del CMRJ. Implica renumerar contenido.
- **Opción T2 — Mantener las fases actuales** y volcar cada bloque del banco a la
  fase actual que corresponda por tema (fracciones→Fase 5, geometría→Fase 6,
  etc.). Menos disruptivo; algunos temas nuevos (teoría de números, sistemas de
  numeración) necesitarían ubicación.
- **Opción T3 — Híbrido:** empezar volcando a las fases actuales (T2) y, cuando el
  banco esté completo, evaluar el reordenamiento (T1).

---

## 5. Pipeline de contenido (de foto a pregunta jugable)

1. **Transcripción** foto → ejercicio estructurado (PT). *Hecho: 41; falta el
   grueso de 276 fotos + exámenes del docx.*
2. **Traducción** PT → ES (revisada, con vocabulario infantil).
3. **Estructurar** a JSON/YAML validable (enunciado, tipo, alternativas,
   gabarito, pasos, figura, tema, fase, dificultad).
4. **Figuras**: recorte → SVG (o embeber JPG).
5. **Importar** a la BD con el nuevo seeder; agrupar en familias por concepto.
6. **Verificar** (auditoría: figura↔enunciado, 1 correcta, respuesta válida,
   dificultad escalonada) + QA visual.

---

## 6. Plan por etapas (propuesto)

- **F0 · Prueba de concepto (1 tema):** tomar Fracciones (Bloque 4, ya con
  figuras/SVG), estructurarlo a JSON, escribir el importador, sembrar esas
  preguntas reales en la fase de fracciones y verlas jugables con el motor
  actual (refuerzo/teoría/visual). Valida toda la cadena con poco riesgo.
- **F1 · Formato + importador definitivos** a partir de la PoC.
- **F2 · Completar transcripción/traducción** del resto de bloques y del docx
  (por lotes temáticos).
- **F3 · Figuras a SVG** (o embebido) para todo el banco.
- **F4 · Volcado por fases** (según decisión T1/T2/T3) y retiro del compositor.
- **F5 · Dificultad escalonada + Simulados** por año (del docx) como examen
  final tipo CMRJ.
- **F6 · QA visual + verificación integral.**

---

## 7. Decisiones abiertas (para ti)

- **DB1 — Estructura de fases:** ¿T1 (reordenar al temario CMRJ), T2 (mantener
  fases actuales), o T3 (híbrido)?
- **DB2 — Formato fuente:** ¿JSON estructurado (recomendado, validable) o seguir
  en Markdown como fuente?
- **DB3 — Alcance de transcripción:** ¿completo tú la transcripción de las 276
  fotos + docx, o lo hago yo por lotes (leyendo las imágenes)?
- **DB4 — Figuras:** ¿priorizar SVG (más trabajo, mejor calidad) o embeber los
  JPG recortados de entrada?
- **DB5 — Compositor:** ¿deprecarlo del todo o dejarlo como respaldo temporal?
- **DB6 — Punto de partida:** ¿arrancamos la PoC (F0) por **Fracciones**?
