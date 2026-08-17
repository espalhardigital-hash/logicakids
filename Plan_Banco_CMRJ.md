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

## 2. El enfoque correcto (aclarado por el usuario 2026-08-17)

**NO** es reemplazar el motor por un banco estático. Es **arreglar el motor**
para que **genere** preguntas con el estilo, estructura, profundidad y nivel de
las preguntas reales del CMRJ. Las preguntas provistas y los exámenes de años
anteriores son **modelos de referencia** (el "estándar oro" a emular), no filas
a insertar.

- El compositor actual produce preguntas **superficiales y mal estructuradas** →
  se **rediseña**, no se descarta.
- Cada plantilla del generador debe estar **derivada de un arquetipo real** del
  CMRJ: multi-paso, contexto real, figura pertinente, y **distractores que
  encarnan las trampas** típicas del examen.
- Los exámenes 2013-2025 (docx) **calibran el nivel** y alimentan los
  **Simulados**.
- **Objetivo:** que el alumno que completa las fases pueda **aprobar el CMRJ**.

### Lo que se CONSERVA (la filosofía ya desarrollada)
El motor pedagógico es **independiente de la profundidad del contenido** y se
mantiene tal cual: **refuerzo al fallar** (solución paso a paso → reformulación),
**progreso P1**, **salida honrosa**, **teoría** por nivel y **visualizadores**.
Solo cambia la **calidad/profundidad de lo que el generador produce**.

### Alcance
Reestructurar el **contenido** de la **Fase 4 en adelante** (4 decimales, 5
fracciones, 6 geometría espacial, 7, 8 estadística/probabilidad, 9 simulados).
La estructura de fases **se mantiene** (ya coincide con el temario CMRJ); lo que
sube es la **profundidad**.

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

## 6. Plan por etapas (rediseño del generador a nivel CMRJ)

- **F0 · Catálogo de arquetipos por fase.** Leer el material (bloques + fotos +
  docx) y extraer, por tema/fase, los **arquetipos de pregunta** del CMRJ: qué
  pide, estructura multi-paso, contexto, figura, dificultad y las **trampas**
  (errores comunes → distractores). Salida: una ficha de arquetipos por fase.
- **F1 · Prueba de concepto (1 fase).** Rediseñar el generador de **una** fase
  (p.ej. Fase 5 fracciones, que ya tiene el motor listo) con plantillas
  derivadas de los arquetipos: multi-paso, distractores-trampa, figura correcta,
  explicación real. Verificar que genera variedad a nivel CMRJ y es jugable.
- **F2 · Motor de plantillas-arquetipo.** Consolidar el patrón del generador
  (cómo se declara un arquetipo multi-paso con sus trampas y su figura) para
  replicarlo con rapidez y rigor.
- **F3 · Reestructurar Fase 4 → 9** aplicando arquetipos CMRJ por fase, subiendo
  la profundidad; conservar el motor pedagógico.
- **F4 · Simulados (Fase 9)** con preguntas reales por año del docx (examen tipo
  CMRJ) + dificultad escalonada N11<N12<N13 en cada fase.
- **F5 · Figuras**: SVG (o JPG embebido) para los arquetipos que lo requieran.
- **F6 · Verificación integral + QA visual.**

---

## 7. Decisiones abiertas (para ti)

- **DB1 — Punto de partida:** ¿arranco F0 (catálogo de arquetipos) por **todas**
  las fases 4-9, o hago F0+F1 primero solo en **Fase 5** (fracciones) como PoC?
- **DB2 — Material a leer para arquetipos:** ¿me baso en el **banco transcrito**
  (41 ej.) + **docx** de exámenes, o también proceso las **276 fotos** (leyendo
  las imágenes) para ampliar el catálogo?
- **DB3 — Profundidad de la PoC:** ¿cuántos arquetipos por nivel apuntamos
  (p.ej. 3-5 por nivel) para lograr variedad sin colisiones?
- **DB4 — Figuras:** ¿SVG propio o embeber los recortes JPG del material?
- **DB5 — Traducción:** confirmo que todo va en **español** (los modelos están en
  portugués).
