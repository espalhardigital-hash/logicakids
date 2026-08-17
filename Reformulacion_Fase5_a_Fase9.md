# Reformulación de la Fase 5 a la Fase 9

> **Documento de trabajo colaborativo.** Aquí escribimos, paso a paso, qué vamos
> a hacer para reformular las Fases 5 a 9 de LogicaKids. El usuario dicta los
> pasos; el asistente los captura y presenta **opciones** en cada decisión.
> Nada se implementa hasta que un paso quede acordado aquí.
>
> **Rama de trabajo:** `mejoras-fases-5-9` (no toca `producion`).
> **Fecha de inicio:** 2026-08-17.

---

## 1. Objetivo

Que un alumno que **complete las Fases 5 a 9 esté realmente preparado para el
examen de admisión del Colégio Militar (CMRJ)** — nivel olimpiada (ver
`coelgiomilitar.md`).

- **Dificultad escalonada hacia CMRJ:** la práctica es accesible y sube
  gradualmente; solo los desafíos finales y los Simulados llegan al nivel real
  del examen.
- Gráficas correctas (que coincidan con la pregunta) y contenido sin bugs.

---

## 2. Diagnóstico (problemas reales ya detectados y verificados)

Base de por qué hay que reformular, no solo parchar:

| # | Problema | Estado |
|---|---|---|
| D1 | **El "Bucle Espejo" NO es viable** tal como está formulado (confirmado por el usuario tras múltiples tests). Mecánica a **reemplazar**, no a arreglar. | ⛔ A rediseñar |
| D2 | **Gráficas que NO coinciden con la respuesta.** Ej. probado: Fase 6 "¿cuántos vértices?" dibujaba siempre un cuadrado aunque la respuesta fuera triángulo/pentágono/etc. | ⚠️ Parcial (sec 101 corregida) |
| D3 | **Fase 5 no tiene figuras** en las preguntas interactivas (0 `tipo_visual`). | ⛔ Pendiente |
| D4 | **Los desafíos son iguales a la práctica** (solo se les añade "[Desafío]"); no hay salto de dificultad hacia CMRJ. | ⛔ Pendiente |
| D5 | **Simulados (Fase 9)** era un stub de 3 preguntas (una en portugués). Ya se reemplazó por un banco base de 20 (ampliable). | ✅ Base hecha |
| D6 | Enredo de numeración backend/frontend (fase8/fase9 huérfanos; Simulados vivía tapado). | ✅ Corregido |
| D7 | Contenido más fácil que el examen real; falta cubrir temas CMRJ (primos, MCD/MCM, calendario modular, 3D, redondeo comercial, fracciones anidadas). | ⛔ Pendiente |
| D8 | **Backend en bucle de reinicio** (ExitCode 1): el master llamaba `run_fase5_seed()` sin `session`, que la función exige → tumbaba el arranque → "Error de conexión" en el login. | ✅ Corregido (sesión opcional) |

*(Bugs críticos ya corregidos y commiteados: crash de enum en Fase 5, routing y sembrado de Simulados. Ver `INFORME_barrido_fases_5-9.md`.)*

---

## 3. Fase 5 — decisiones del usuario (2026-08-17)

### 3.0 Lo que está BIEN (no se toca)
- Fase 5 = **Fracciones, Porcentajes y Proporciones**. La filosofía y los 4
  módulos son correctos: **Fracción Visual · Fracción de Cantidad · Porcentaje
  Rápido y Promedio · Razón y Mezclas**.

### 3.1 Lo que se REFORMULA en Fase 5
- **Tipo de preguntas** (los tipos actuales no son los adecuados). *(Definir cuáles.)*
- **Distribución de niveles** dentro de los módulos (hoy está desbalanceada). *(Definir.)*
- **Teoría**: reformular la teoría que ve el alumno al entrar a cada nivel.
- **Sistema Espejo**: se elimina el mecanismo actual y se reemplaza por el de 3.2.

### 3.2 Nuevo sistema de refuerzo (reemplaza al Espejo) — batería libre / práctica

Flujo definido por el usuario:

1. El alumno **entra al nivel → ve la TEORÍA** (reformulada).
2. Responde preguntas de la batería (práctica libre).
3. **Si acierta:** avanza; cuenta para el progreso.
4. **Si FALLA una pregunta:**
   1. Se le muestra la **respuesta correcta** y el **procedimiento paso a paso**
      (cómo se llega a esa respuesta) — una explicación pedagógica real, no una
      fórmula cruda.
   2. La siguiente pregunta **NO sale de la batería**: es la **misma pregunta
      REFORMULADA** — mismo concepto pero **distinto contexto y distintos
      valores** (no la misma con otros números). El alumno la resuelve.
   3. Si **vuelve a fallar** → se muestra de nuevo el error + procedimiento y se
      presenta **otra reformulación**. Esto ocurre **como máximo 2 veces**.
   4. Si falla por **tercera vez** → se le muestra la solución y se **pasa a
      otra pregunta** (nueva, de la batería) para **no crear un círculo**.

**Diferencias clave vs el espejo actual (por qué el actual no sirve):**
- Hoy la "variante" es el **mismo escenario** con otros números → se siente
  igual. Ahora debe cambiar **contexto Y valores** (reformulación genuina).
- Hoy la explicación es una fórmula cruda → ahora es un **procedimiento paso a
  paso**.
- Hoy el tope es 3 (`MAX_ESPEJO`) → ahora **2 reformulaciones y se avanza**.

### 3.3 Análisis del PROGRESO (para decidir)

**Cómo funciona hoy:** el progreso cuenta *familias distintas resueltas* /
`cantidad_requerida`. Pero cuenta como "resuelta" tanto un **acierto** como un
**rendirse** (`BYPASS_EXPLICACION`). ⇒ hoy se puede llegar al **100 % fallando
todo** (el bypass avanza igual). Esto choca con el objetivo CMRJ.

**Opciones para el nuevo progreso (elige una):**
- **P1 (exigente/honesto, recomendado):** solo cuenta la familia si el alumno la
  **resuelve correctamente** (en el original o en una de las 2 reformulaciones).
  Si agota las reformulaciones sin acertar, avanza a otra pregunta pero **esa
  familia NO suma** al progreso.
- **P2 (indulgente, como hoy):** rendirse tras las reformulaciones **sí cuenta**
  como resuelta (para no frustrar). El progreso mide "vistas", no "dominadas".
- **P3 (intermedio):** el acierto en el original vale completo; acertar en una
  reformulación vale igual; rendirse cuenta como **medio** o no cuenta pero
  tampoco bloquea el nivel si el % global de aciertos supera un umbral.

### 3.4 Decisiones tomadas
- **DA1 → P1 (exigente/honesto).** El progreso solo cuenta una familia si el
  alumno la **resuelve correctamente** (original o una reformulación). Rendirse
  tras las reformulaciones **NO suma** al progreso (avanza a otra pregunta, pero
  esa familia no cuenta). *Implicación técnica (para después):* quitar la
  cláusula `BYPASS_EXPLICACION` de `_recalcular_porcentaje_fase5`.
- **DA2 → Reformulaciones PRE-SEMBRADAS en la BD (no al vuelo).** Cada familia
  tiene su original + **2-3 reformulaciones** ya guardadas, cada una con
  **distinto contexto (escenario) Y distintos valores** — no la misma con otros
  números. Motivo: más controlable que generar en tiempo de ejecución.
  *Implicación técnica (para después):* el seed debe garantizar que las 2-3
  variantes de una familia usen **escenarios distintos** (hoy comparten
  escenario); el runtime deja de "generar" y solo selecciona la siguiente
  reformulación no vista de la familia; tope **2 reformulaciones**, luego avanza.

- **DA3 → Visual-interactivo por módulo (Opción 1).** Los visualizadores YA
  existen en el frontend (`components/fase5/*`) y el motor
  `Fase5VisualizerEngine` ya los despacha por `datos_numericos.tipo_visual`;
  están **muertos** solo porque el seed no emite `tipo_visual`. Mapa objetivo
  (componente real ↔ `tipo_visual`):

  | Módulo | Concepto | `tipo_visual` | Componente |
  |---|---|---|---|
  | M1 Fracción Visual | leer/marcar partes de un todo | `pizza` (y `pie`) | PizzaFractionVisualizer / PieChartVisualizer |
  | M2 Fracción de Cantidad | fracción de un grupo/cantidad | `bar_chart` o `ratio_grid` | Fase5InteractiveBarChart / RatioGridVisualizer |
  | M3 Porcentaje y Promedio | % y descuentos / promedio | `percentage_beaker` (+ `bar_chart` para promedio) | PercentageBeaker / Fase5InteractiveBarChart |
  | M4 Razón y Mezclas | razón y mezcla | `ratio_grid` o `beaker` | RatioGridVisualizer / BeakerVisualizer |

  Respuesta en **opción múltiple** apoyada por la figura. *(Sub-elección
  pendiente: en M2 y M4, cuál de las dos alternativas de visual usar — se afina
  al diseñar cada nivel.)*
  *Implicación técnica (para después):* el seed de Fase 5 debe emitir
  `tipo_visual` + el **payload** que cada componente espera (p.ej. pizza:
  `cortes`, `seleccionadas`; ratio_grid: filas/columnas; beaker: nivel/target).

- **DA4 → Nueva distribución de niveles (APROBADA).** Mismos 4 módulos × 3
  niveles de práctica, escalonados:

  | Módulo | N1 | N2 | N3 |
  |---|---|---|---|
  | **M1** Fracción Visual | Lectura de fracciones | Fracciones equivalentes | **Comparar fracciones** (mayor/menor) |
  | **M2** Fracción de Cantidad | 1/n de una cantidad | a/b de una cantidad (2 pasos) | **Problema inverso / resto** |
  | **M3** Porcentaje y Promedio | %clave (10/25/50) | Descuentos y aumentos (multi-paso) | Promedio / media |
  | **M4** Razón y Mezclas | Razón simple (a:b) | Reparto proporcional / regla de tres | Mezclas y % de volumen |

  Cambio principal vs hoy: M1-N3 deja de ser "resta" y pasa a **comparación de
  fracciones**. Los desafíos (11/12/13) de cada módulo escalan estos conceptos
  hacia nivel CMRJ.

- **DA5 → Teoría rica y visual (Opción A).** Hoy la teoría es casi todo
  placeholder (`texto_descubrimiento` de relleno, diccionario de 1 término); solo
  los ejemplos guiados son reales. Por cada nivel se escribirá: (1) explicación
  en 2-3 párrafos con 1 mini-ejemplo resuelto, (2) diccionario de 2-3 términos,
  (3) 2-3 ejemplos guiados con la figura del módulo, (4) un dato "¿Sabías
  que…?", (5) un interactivo de calentamiento con la figura.

---

## 3.6 Desafíos: control de dificultad y anti-frustración (analizar antes de aprobar)

**Problema confirmado en el código actual (Salida Temprana):** al superar el
límite de errores en un desafío, el sistema **resetea el progreso a cero**, deja
el nivel **BLOQUEADO**, **borra intentos y pool**, y obliga a **repetir el
desafío completo desde cero** ("¡Misión abortada!"). Sin repaso ni refuerzo. Con
dificultad CMRJ, esto es un **círculo vicioso**: fallar → reset → repetir lo
mismo → fallar → reset.

### DA6 — ¿Qué tan CMRJ son los desafíos? (control de dificultad)
- **A1 (recomendada) — Escalonado en 3 pasos:** desafío N11 = práctica
  reforzada; N12 = intermedio; N13 = *pre-CMRJ*. El **CMRJ pleno vive solo en
  los Simulados (Fase 9)**. El niño llega a lo más duro solo tras dominar lo
  previo.
- **A2 — Todos los desafíos a CMRJ:** máxima exigencia; alto riesgo de
  frustración. No recomendada.
- **A3 — Adaptativa:** la dificultad sube o baja según el desempeño del niño.

### DA7 — Qué pasa al fallar un desafío (romper el círculo vicioso)
- **B1 (recomendada) — Repaso dirigido + salida honrosa:** al llegar al límite
  de errores, mensaje **positivo** ("Aún no, reforcemos esto"), se envía al niño
  a **practicar el concepto específico que falló** (con el refuerzo de la
  práctica: solución + reformulaciones) y **al reintentar el desafío trae
  preguntas distintas**. No hay reset brutal ni bloqueo permanente.
- **B2 — Modo guiado tras X fallos:** si falla el desafío 2 veces, se ofrece una
  versión con pistas/dificultad reducida para destrabar, y luego se retoma.
- **B3 — Sin expulsión:** el desafío se puede **pausar y retomar**; se aprueba
  por acumulación de aciertos; nunca se "reinicia a cero".

**Salvaguardas comunes propuestas (para ambas):**
- **Umbral de aprobación razonable** (p.ej. 70-80 %, no 90-100 %) para que unos
  pocos ítems muy difíciles no impidan pasar.
- **Anti-círculo garantizado:** tras fallar, el niño NUNCA vuelve de inmediato
  al desafío idéntico; pasa por un refuerzo primero, y el reintento usa ítems
  distintos.
- **Reconocer el esfuerzo:** feedback/estrellas por progreso parcial.

**Decidido (2026-08-17):** **DA6 → A1** (escalonado en 3 pasos; CMRJ pleno solo
en Simulados) y **DA7 → B1** (repaso dirigido + salida honrosa; sin reset ni
bloqueo) + las **tres salvaguardas** (umbral 70-80 %, anti-círculo garantizado,
reconocer esfuerzo).

## 4. Plan de implementación — Fase 5 (para aprobar antes de codear)

> Ordenado por dependencia. Cada etapa se **verifica contra el Postgres local
> real** antes de avanzar (método `razonamiento_profundo.md`). No se toca
> `producion`; todo en rama `mejoras-fases-5-9`.

**E1 · Estructura de familia con reformulaciones pre-sembradas (DA2). ✅ HECHO.**
*(Verificado: 144 familias × 4 miembros — 1 original + 3 reformulaciones; 0
familias con escenario repetido; `orden_refuerzo` + `escenario_id` etiquetados.)*
Cada familia (`estructura_padre_id`) = 1 **original** + 2-3 **reformulaciones**,
cada una con **escenario distinto Y valores distintos**. Se etiqueta el rol en
`datos_numericos` (p.ej. `orden_refuerzo`: 0=original, 1..3=reformulación). El
compositor debe garantizar escenario distinto entre las variantes de una misma
familia (hoy comparten escenario).
*Verif.:* cada familia tiene 1 original + 2-3 reformulaciones; escenarios
distintos dentro de la familia; 0 duplicados de enunciado por familia.

**E2 · Tipos visuales por módulo (DA3). ✅ HECHO (datos) · QA visual en E10.**
`_visual_payload` en el compositor emite `tipo_visual` + payload que casa con el
contrato de cada componente y **no revela** la respuesta: M1 `pizza`
(cortes/sombreados; M1N2 num_base/den_base/factor), M2 `pizza`, M3 `percentage_
beaker` (+ `bar_chart` en promedio), M4 `ratio_grid`.
*(Verificado: 576/576 práctica con tipo_visual; claves coinciden con los props
del `Fase5VisualizerEngine`. Falta QA visual en vivo tras rebuild — E9/E10.)*

**E3 · Nueva distribución de niveles (DA4). ✅ HECHO (nombres) · reframe M1N3 parcial.**
`NIVELES_META` alineado a DA4 con nombres que describen el contenido REAL (sin
mismatch): M1-N3 "Comparar Partes de un Todo", M2-N3 "Problema Inverso y Resto",
M3 "Porcentajes Clave / Descuentos y Aumentos / Promedio", M4 "Razón / Reparto /
Mezclas y % de Volumen".
*Pendiente (mejora):* un tipo genuino "comparar DOS fracciones" (2 sujetos /
respuesta de texto) requiere extender el compositor; queda como enhancement.
También: escenario dinero↔puntaje en promedio (M3N3) a depurar.

**E4 · Explicaciones paso a paso reales. ✅ HECHO.**
Narrador basado en el AST de la fórmula: evalúa cada sub-operación con los
valores reales y muestra la aritmética ("10 − 4 = 6"; "48 ÷ 3 = 16").
*(Verificado: 0 explicaciones con fórmula cruda; pasos correctos por concepto.)*
*Pendiente menor:* narración de % muestra `total×pct` intermedio (correcto pero
mejorable) y hay escenarios dinero↔puntaje mal mezclados (se corrige en E3).

**E5 · Nuevo flujo de refuerzo en el router (reemplaza el espejo). ✅ HECHO.**
Al fallar en práctica: devuelve **solución paso a paso (E4) + la siguiente
reformulación** (orden_refuerzo+1, otro contexto). Tope **2 reformulaciones**
(`MAX_ESPEJO=2`); a la 3ª, muestra solución y **avanza a otra familia** (marca
el slot cerrado; sin acierto no cuenta → P1). Respuesta lleva `explicacion`
(pasos), `intentos_espejo_actuales/max`, `soporte_avanzado`.
*(Verificado E2E in-process: original→reformulación(chocolate)→reformulación
(bandera)→avanza a otra familia; escenarios distintos; fallar no sube el %.)*

**E6 · Progreso P1 (DA1). ✅ HECHO.**
`_recalcular_porcentaje_fase5`: eliminada la cláusula `BYPASS_EXPLICACION`; solo
cuentan familias con **acierto real** (original o reformulación).

**E7 · Teoría rica y visual (DA5).**
Escribir la teoría de los 12 niveles (párrafos + mini-ejemplo + diccionario 2-3
+ ejemplos guiados con figura + "¿sabías?" + interactivo de calentamiento).
*Verif.:* 0 placeholders; teoría renderiza con figuras en `/lectura`.

**E8 · Desafíos anti-frustración (DA7 B1) ✅ HECHO · dificultad escalonada (DA6 A1) ⏭ pendiente (con E3).**
Salida honrosa verificada E2E: al superar el límite de errores, `early_exit` con
mensaje positivo, **sin reset ni bloqueo** (progreso conservado, estado
EN_PROGRESO), se limpia el pool para reintentar con ítems distintos y se
reinicia el contador de errores. Umbrales de aprobación: desafíos 80 %, mixto
70 % (antes 100 %). *Pendiente:* escalonar la dificultad real N11<N12<N13 (parte
de contenido, junto a E3).

**(diseño original) E8 · Desafíos escalonados + anti-frustración (DA6 A1 · DA7 B1).**
- Dificultad escalonada: **N11 práctica reforzada · N12 intermedio · N13
  pre-CMRJ**; CMRJ pleno solo en Simulados (Fase 9). Dejar de copiar la práctica
  con prefijo "[Desafío]".
- **Reemplazar la "Salida Temprana" destructiva** (reset a cero + BLOQUEADO +
  borrado) por **repaso dirigido + salida honrosa**: al llegar al límite de
  errores → mensaje positivo → enviar a reforzar el concepto fallado (práctica
  con solución + reformulaciones) → al reintentar, el desafío trae **ítems
  distintos**. Sin reset ni bloqueo permanente.
- **Salvaguardas:** umbral de aprobación **70-80 %**; **anti-círculo**
  garantizado (nunca reintento inmediato del desafío idéntico); estrellas /
  feedback por progreso parcial.
*Verif.:* E2E — fallar un desafío NO resetea a cero ni bloquea; enruta a
refuerzo; el reintento usa ítems distintos; se aprueba a ≥ umbral.

**E9 · Frontend.**
`Fase5GameScreen` / `Fase5VisualizerEngine` consumen `tipo_visual` y el nuevo
flujo (mostrar solución → reformulación). Reemplazar/retirar la lógica de
`Fase5MirrorModal` acorde al nuevo refuerzo.
*Verif.:* `tsc --noEmit` limpio, `vite build` OK, prueba en `localhost:3000`.

**E10 · Verificación integral.**
Re-seed + auditoría (figura↔respuesta, escenarios distintos/familia, 2-3
reformulaciones, explicaciones reales, progreso P1) + E2E + tests.

> **Fases 6-9:** una vez validada Fase 5 como plantilla, se replica el patrón
> (tipos visuales correctos, refuerzo, progreso P1, dificultad escalonada) fase
> por fase.

---

## 5. Registro de decisiones

| Fecha | Decisión | Elegido |
|---|---|---|
| 2026-08-17 | Prioridad general | Nivel CMRJ real, dificultad **escalonada** |
| 2026-08-17 | Bucle Espejo actual | **Se descarta** (no viable); reemplazado por sistema 3.2 |
| 2026-08-17 | Módulos de Fase 5 | Correctos, **no se tocan** (filosofía OK) |
| 2026-08-17 | Refuerzo tras error | Mostrar solución paso a paso → reformulación (otro contexto+valores) → máx 2 → avanzar |
| 2026-08-17 | DA1 Progreso | **P1**: solo cuenta si resuelve correcto; rendirse no suma |
| 2026-08-17 | DA2 Reformulaciones | **Pre-sembradas** (2-3 por familia), otro contexto+valores; no al vuelo |
| 2026-08-17 | DA3 tipos de pregunta | **Visual-interactivo por módulo** (pizza/bar/ratio/beaker) + opción múltiple |
| 2026-08-17 | DA4 distribución de niveles | **Aprobada** (M1-N3 → comparar fracciones; resto escalonado) |
| 2026-08-17 | DA5 teoría | **Opción A** (teoría rica y visual por nivel) |
| 2026-08-17 | DA6 dificultad desafíos | **A1** (escalonado; CMRJ pleno solo en Simulados) |
| 2026-08-17 | DA7 fallo de desafío | **B1** (repaso dirigido + salida honrosa; sin reset/bloqueo) + salvaguardas |
| 2026-08-17 | Plan de implementación Fase 5 (E1–E10) | **Redactado** — pendiente de tu aprobación |
