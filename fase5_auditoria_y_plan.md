# Auditoría profunda de la Fase 5 y plan de corrección

> **Fecha:** 2026-08-09
> **Alcance:** `LogicaMath/backend/app/fase5/**`, `LogicaMath/backend/tests/test_fase5_vocabulario.py`, `LogicaMath/backend/scripts/audit_fase5_narrativas.py`, `LogicaMath/frontend/components/fase5/**`, `LogicaMath/frontend/components/fase_generic/faseMetadata.ts`
> **Estado del trabajo previo:** la bitácora `fase5nuevoscambios.md` declara *"Implementado y Verificado"*. **Esa afirmación no se sostiene**: la Fase 5 en su estado actual no siembra, no responde y no se puede jugar.

---

## 0. Veredicto

| Área | Estado | Detalle |
|---|---|---|
| Seeder | ❌ **No ejecuta** | 3 `TypeError` por kwargs inexistentes + 2 errores de columna |
| Endpoint `/dashboard` | ❌ **500** | `AttributeError` + `ValidationError` de schema |
| Endpoint `/pregunta` (práctica) | ❌ **404 permanente** | filtro por clave `variante` que el compositor nunca escribe |
| Endpoint `/responder` | ❌ **422 / AttributeError** | el schema pide `respuesta_alumno`, el handler lee `respuesta_dada` |
| Endpoint `/lectura` | ❌ **500** | `ValidationError` + columnas mal nombradas |
| Contenido visual (SVG) | ❌ **Eliminado** | 16 bloques SVG en el seed anterior → 0 en el actual; 10 visualizadores del frontend quedaron muertos |
| Corrección matemática | ⚠️ | 44/120 respuestas de M3N3 y M4N3 son decimales periódicos redondeados (respuesta *incorrecta*) |
| Variedad | ⚠️ | 60 preguntas por bloque generadas desde **4–8 redacciones** (repetición ×7,5 a ×15) |
| Calidad pedagógica | ⚠️ | **30 %** de las preguntas tienen la respuesta impresa literalmente en el enunciado |
| Arnés de tests (11/11 verde) | ⚠️ | Tautológico: no toca modelos, ni schemas, ni router, ni seed |

**Conclusión:** la reestructuración creó un motor de composición razonable como esqueleto, pero lo conectó a un contrato de datos equivocado en los tres extremos (modelos SQLAlchemy, schemas Pydantic y frontend), y en el camino borró la capa visual que era la razón de ser de la fase. Ningún alumno puede jugar la Fase 5 hoy.

---

## PARTE A — Bloqueantes: la Fase 5 no arranca

### BUG-01 · El seeder de teoría revienta con `TypeError` 🔴 CRÍTICO
**Archivo:** [seed.py:91-101](LogicaMath/backend/app/fase5/seed.py:91)
El modelo `NivelTeoria` ([fase2/models.py:54](LogicaMath/backend/app/fase2/models.py:54)) declara las columnas `diccionario`, `advertencia`, `ejemplos`, `interactivos`. El seed pasa `diccionario_clave=`, `advertencia_comun=`, `ejemplos_json=`, `interactivos_json=`.

```
TypeError: 'diccionario_clave' is an invalid keyword argument for NivelTeoria
```
**Fix:** renombrar los 4 kwargs a los nombres reales de columna.

---

### BUG-02 · El seeder de preguntas revienta con `TypeError` 🔴 CRÍTICO
**Archivo:** [seed.py:192-203](LogicaMath/backend/app/fase5/seed.py:192) (y repetido en 240-251, 285-296)
`Pregunta` ([models/pregunta.py:8](LogicaMath/backend/app/models/pregunta.py:8)) **no tiene** las columnas `explicacion` ni `es_activa`.

```
TypeError: 'explicacion' is an invalid keyword argument for Pregunta
```
**Fix:** `explicacion=` → `explicacion_paso_a_paso={"html": ...}` (JSONB) y `es_activa=True` → `estado=StatusEnum.ACTIVO`.
**Nota:** este segundo cambio es además necesario para que el router encuentre las preguntas — todas sus consultas filtran por `Pregunta.estado == StatusEnum.ACTIVO` ([router.py:548](LogicaMath/backend/app/fase5/router.py:548), [556](LogicaMath/backend/app/fase5/router.py:556), [804](LogicaMath/backend/app/fase5/router.py:804)).

---

### BUG-03 · El seeder de configuración revienta con `TypeError` 🔴 CRÍTICO
**Archivo:** [seed.py:109-158](LogicaMath/backend/app/fase5/seed.py:109)
`ConfiguracionProgreso` usa `errores_tolerados`, no `max_errores_tolerados`.

```
TypeError: 'max_errores_tolerados' is an invalid keyword argument for ConfiguracionProgreso
```

---

### BUG-04 · `ConfiguracionProgreso.operacion` recibe valores fuera del Enum 🔴 CRÍTICO
**Archivo:** [seed.py:119](LogicaMath/backend/app/fase5/seed.py:119), [seed.py:113](LogicaMath/backend/app/fase5/seed.py:113)
La columna es `Enum(OperacionEnum)` y `OperacionEnum` sólo admite `suma | resta | multiplicacion | division | mixta`. El seed inserta `"practica_libre"`, `"fraccion_visual"`, `"fraccion_cantidad"`, `"porcentajes_promedios"`, `"razon_mezclas"` → `StatementError` en el flush.
**Fix:** usar `OperacionEnum.MIXTA` en toda la Fase 5 (es lo que `_seccion_operacion()` devuelve en el router, [router.py:101-107](LogicaMath/backend/app/fase5/router.py:101)) y mover la etiqueta pedagógica del módulo a `topology.py`.

---

### BUG-05 · `orden_desbloqueo` NOT NULL nunca se rellena 🔴 CRÍTICO
**Archivo:** [seed.py:109-158](LogicaMath/backend/app/fase5/seed.py:109)
`orden_desbloqueo = Column(Integer, nullable=False)` sin default → `IntegrityError` en las 25 filas de configuración.

---

### BUG-06 · Todos los bloques de práctica devuelven 404 para siempre 🔴 CRÍTICO
**Archivo:** [router.py:572](LogicaMath/backend/app/fase5/router.py:572)
```python
fam_q = [p for p in preguntas_db if p.estructura_padre_id == fam_id
         and p.datos_numericos.get("variante") == 0]
```
El compositor escribe `datos_numericos = {**valores, "resultado_num", "formula"}` ([compositor_fase5.py:152-156](LogicaMath/backend/app/fase5/compositor_fase5.py:152)) — **la clave `variante` no existe**. `fam_q` siempre vacío → no se crea ninguna fila en `PoolAsignadoAlumno` → [router.py:613](LogicaMath/backend/app/fase5/router.py:613) lanza:

> `404 — No hay suficientes preguntas de la variante original (0) disponibles en el banco`

**Los 12 bloques de práctica (720 preguntas) son injugables.** Sólo los desafíos entrarían, porque su rama no filtra por `variante`.

---

### BUG-07 · `/responder` rechaza el payload del frontend 🔴 CRÍTICO
**Archivos:** [schemas.py:93-103](LogicaMath/backend/app/fase5/schemas.py:93) vs [router.py:694](LogicaMath/backend/app/fase5/router.py:694), [703](LogicaMath/backend/app/fase5/router.py:703), [744-745](LogicaMath/backend/app/fase5/router.py:744)
`Fase5ResponderPregunta` declara `respuesta_alumno: str` (obligatorio) y **no declara** `alternativa_id`. El frontend envía `{respuesta_dada, alternativa_id}` ([Fase5Types.ts](LogicaMath/frontend/components/fase5/Fase5Types.ts)) y el propio handler lee `payload.alternativa_id` / `payload.respuesta_dada`.

Verificado:
```
ValidationError: 1 validation error for Fase5ResponderPregunta
respuesta_alumno  Field required
```
**Ninguna respuesta puede enviarse.** Aunque pasara la validación, el handler caería en `AttributeError`.

---

## PARTE B — Contrato roto entre schemas nuevos, router y frontend

Los schemas nativos de [schemas.py](LogicaMath/backend/app/fase5/schemas.py) se escribieron **inventando campos** en vez de espejar los `Fase2*` que el router y el frontend ya usaban. Resultado verificado con Pydantic 2.13.4:

| # | Schema | Lo que el router envía | Lo que el schema exige | Efecto |
|---|---|---|---|---|
| **BUG-08** 🔴 | `Fase5NivelInfo` | `estado`, `aciertos`, `porcentaje` | `bloqueado`, `aprobado`, `porcentaje_actual` | los extras se descartan → [router.py:289](LogicaMath/backend/app/fase5/router.py:289) `n.estado` → `AttributeError` → **500** |
| **BUG-09** 🔴 | `Fase5DesafioInfo` | `desafio_id`, `dificultad`, `tiempo_limite`, `max_errores`… | `nivel_id` (requerido) | `ValidationError: nivel_id Field required` |
| **BUG-10** 🔴 | `Fase5Dashboard` | `alumno_nombre`, `puntos_totales`, `desafio_mixto_*` | `alumno_id` (requerido) | `ValidationError: alumno_id Field required` |
| **BUG-11** 🔴 | `Fase5ContenidoLectura` | `parrafos`, `tip_pedagogico`, `diccionario`, `interactivos` | `contenido_html` (requerido) | `ValidationError` → **500 en `/lectura`** |
| **BUG-12** 🟠 | `Fase5ResultadoRespuesta` | `early_exit`, `explicacion_profunda` | no existen | se pierden silenciosamente → el modal de rescate y la salida temprana del desafío dejan de funcionar |
| **BUG-13** 🟠 | `Fase5PreguntaParaAlumno` | `aciertos_acumulados`, `intentos_totales`, `porcentaje_actual`, `cantidad_requerida` ([router.py:648-651](LogicaMath/backend/app/fase5/router.py:648)) | no existen | la barra de progreso del juego queda en `undefined` |
| **BUG-14** 🟠 | `Fase5ModuloInfo` | `color`, `estado`, `porcentaje_global` | no existen | tarjetas de módulo sin color ni estado |

**BUG-15 🟠 · `/lectura` además lee columnas inexistentes** — [router.py:972-975](LogicaMath/backend/app/fase5/router.py:972) usa `theory.ejemplos`, `theory.advertencia`, `theory.interactivos`, que sí existen; pero el seed las escribió con los nombres `*_json`, por lo que tras corregir BUG-01 hay que verificar la coherencia de ida y vuelta.

---

## PARTE C — Regresión de contenido: la Fase 5 perdió su capa visual

### BUG-16 · Se borraron los 16 bloques de gráficos SVG 🔴 CRÍTICO (pedagógico)
El seed anterior (`git show HEAD:.../fase5/seed.py`) contenía 16 preguntas con SVG embebido (polígonos, barras, rejillas). El seed actual tiene **cero** referencias a `svg`, `graphics`, `tipo_visual`, `sectors` o `sombreados`.

**Consecuencia en cascada — quedan muertos 10 componentes del frontend:**
`PizzaFractionVisualizer`, `PieChartVisualizer`, `BeakerVisualizer`, `PercentageBeaker`, `RatioGridVisualizer`, `FractionPercentageVisualizer`, `ContextualPercentageVisualizer`, `Fase5InteractiveBarChart`, `Fase5FabricVisualizer`, `Fase5NonHomogeneousPolygon`, más el `Fase5VisualizerEngine` que los despacha por `datos_numericos.tipo_visual`.

Además, la rama de validación de `non_homogeneous_polygon` en [router.py:707-728](LogicaMath/backend/app/fase5/router.py:707) es **código inalcanzable**: nada emite ya ese `tipo_visual`.

Esto contradice frontalmente el diagnóstico previo del proyecto (*"Fase 5: déficit visual, 36 ejercicios interactivos sin figura"*): la reestructuración no lo corrigió, lo llevó al 100 %.

### BUG-17 · `faseMetadata.ts`: la Fase 5 tiene contenido de geometría 🔴
[faseMetadata.ts](LogicaMath/frontend/components/fase_generic/faseMetadata.ts) — `FASE_5` quedó con el título correcto ("Fracciones, Porcentajes y Proporciones", 🍕) pero **sus 4 módulos son de otra fase**: *Perímetro y Borde*, *Área en Cuadrícula*, *Figuras Compuestas*, *Conversión y Pantallas*. Sólo se cambió la cabecera.

### BUG-18 · `FASE_4` se quedó con `modulos: []` 🟠
El contenido offline de la Fase 4 se borró en vez de reemplazarse por el de decimales. La Fase 4 pierde su fallback sin conexión.

### BUG-19 · Colores y nombres desalineados backend↔frontend 🟡
`MODULOS_META` del backend usa `#3B82F6 / #A855F7 / #F97316 / #10B981`; `faseMetadata.FASE_5` usa la paleta rosa `#F43F5E…`.

---

## PARTE D — Errores matemáticos y de semántica

### BUG-20 · El promedio de M3N3 da decimales periódicos redondeados 🔴
**Archivo:** [compositor_fase5.py:204-208](LogicaMath/backend/app/fase5/compositor_fase5.py:204)
```python
rem = (a + b) % 3
c = c_base + ((3 - rem) if rem != 0 else 0)
```
El ajuste es incorrecto: `(a+b+c) ≡ c_base (mod 3)`, así que sólo es divisible si `c_base` ya era múltiplo de 3. **Medido: 18 de 60 preguntas del bloque 303 (30 %) devuelven un promedio no entero**, redondeado a 2 decimales — es decir, la respuesta publicada es **numéricamente falsa**:

> *"Las medidas registradas fueron 12, 18 y 13 puntos. ¿Cuál es la media?"* → **14,33** (real: 14,333…)

**Fix:** `c = c_base + ((3 - (a + b + c_base) % 3) % 3)`.

### BUG-21 · Los porcentajes de mezcla de M4N3 son irracionales 🔴
**Archivo:** [compositor_fase5.py:224-227](LogicaMath/backend/app/fase5/compositor_fase5.py:224) — `b ∈ {3,4,7,9}` sin restricción sobre `a+b`.
**Medido: 26 de 60 preguntas del bloque 403 (43 %)**:

> *"3 ml de activo y 4 ml de agua (total 7 ml), ¿cuál es el porcentaje del activo?"* → **42,86** (real: 42,857142…)

**Fix:** restringir `a+b ∈ {4,5,8,10,20,25,50}` para que `(a*100)/(a+b)` sea siempre entero.

### BUG-22 · Porcentajes fraccionarios sobre objetos contables 🟠
Bloques 301/302: 25 % de 150 → **37,5 objetos**. Un descuento de 37,5 en dinero es tolerable; "37,5 juguetes" no lo es. Falta separar los escenarios de dinero de los de conteo.

### BUG-23 · Escenarios semánticamente incompatibles pasan la validación R2 🟠
La "magnitud" es demasiado gruesa: `esc_pp_notas` (evaluación / puntos) es compatible con las plantillas de tienda, y produce:

> *"En la tienda, **la evaluación** de 50 **puntos** recibe una **rebaja** del 25 %"*
> *"Sofía obtuvo tres puntajes en **juguete**: 15, 16 y 16 **soles**"*

`validar_composicion()` ([compositor_fase5.py:30-62](LogicaMath/backend/app/fase5/compositor_fase5.py:30)) las aprueba porque ambas son `porcentajes_promedios`. **Fix:** añadir un eje `sub_magnitud` (`dinero` | `puntaje` | `conteo` | `volumen`) al contrato R2.

### BUG-24 · Concordancia gramatical singular/plural 🟠
Verificado en salida real: *"tiene **1 partes** pintadas"*, *"seleccionó **1 porciones**"*. Los marcos usan siempre plural.

### BUG-25 · Respuestas decimales con coma en teclado numérico 🟠
`_is_numeric_answer()` ([seed.py:31-34](LogicaMath/backend/app/fase5/seed.py:31)) clasifica `"15,67"` como numérica → `RESPUESTA_NUMERICA` → el alumno debe teclear una coma decimal en un keypad infantil. Es el mismo bug ya registrado para las Fases 5-8.

---

## PARTE E — Variedad y calidad pedagógica del banco

### BUG-26 · El 30 % de las preguntas tiene la respuesta impresa en el enunciado 🔴
5 de las 24 plantillas usan fórmulas identidad (`"a"`, `"b"`, `"total"`): `tpl_m1_n1_identificar`, `tpl_m1_n1_total`, `tpl_m1_n3_usadas`, `tpl_m2_n1_grupos`, `tpl_m2_n2_base`.

> *"Sofía dividió la pizza en 10 partes iguales y comió **4** partes. ¿Qué numerador representa las partes seleccionadas?"* → respuesta **4**

**Medido: 216 de 720 preguntas de práctica (30 %) no requieren ninguna operación.** En los bloques 101 y 201 es el 100 % / 50 % del contenido.

### BUG-27 · Repetición masiva: 60 preguntas por bloque desde 4–8 redacciones 🔴
Sólo hay **2 plantillas por (módulo, nivel)** y `fam_idx % 2` las alterna; `var_idx % 2` elige el marco y `var_idx % len(escenarios)` el escenario. Medición de redacciones distintas por bloque (ignorando números y nombres):

| Bloque | 101 | 102 | 103 | 201 | 202 | 203 | 301 | 302 | 303 | 401 | 402 | 403 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Redacciones | 7 | 5 | 7 | 8 | 8 | 8 | 4 | 4 | 4 | 4 | 4 | 4 |
| Repetición | ×8,6 | ×12 | ×8,6 | ×7,5 | ×7,5 | ×7,5 | ×15 | ×15 | ×15 | ×15 | ×15 | ×15 |

Es exactamente el bug que el commit `4d154fc` corrigió en la Fase 4 — reintroducido aquí.

### BUG-28 · Los desafíos son copias de la práctica con un prefijo 🟠
[seed.py:229-245](LogicaMath/backend/app/fase5/seed.py:229): los 12 desafíos llaman a `componer_pregunta_practica(nivel = niv_id - 10)` con los mismos rangos e insertan `"[Desafío] "` delante. No hay salto de dificultad, ni composición multi-paso, ni distractores más finos.

### BUG-29 · El desafío mixto final usa una sola plantilla por módulo 🟠
[seed.py:278](LogicaMath/backend/app/fase5/seed.py:278): `fam_idx=mod_id` es constante → `plantillas_nivel[mod_id % 2]` fija **una** plantilla por (módulo, nivel). El examen final de 60 preguntas sale de 12 redacciones.

### BUG-30 · Distractores aritméticos sin valor diagnóstico 🔴
[compositor_fase5.py:229-251](LogicaMath/backend/app/fase5/compositor_fase5.py:229): los distractores son `c+1, c-1, c*2, c//2, c+2`. Un alumno los descarta por patrón, no por razonamiento.
**Peor:** `confusiones_fase5.json` se carga en el constructor ([compositor_fase5.py:25-26](LogicaMath/backend/app/fase5/compositor_fase5.py:25)) y **nunca se usa**. Los 12 errores pedagógicos catalogados (invertir numerador/denominador, olvidar multiplicar por el numerador, calcular el descuento sin restarlo…) están escritos y muertos.

### BUG-31 · `Alternativa.tipo_error` y `feedback_error` quedan NULL 🟠
El seed nunca los rellena, por lo que el "Tutor Invisible" del router ([router.py:700-701](LogicaMath/backend/app/fase5/router.py:700)) cae siempre en `TipoErrorEnum.CALCULO` + `"Respuesta incorrecta."`.

### BUG-32 · La explicación es una fórmula cruda 🟡
[compositor_fase5.py:151](LogicaMath/backend/app/fase5/compositor_fase5.py:151):
> `"Resultado obtenido mediante la fórmula: (total/b)*a = 24"`

No es una explicación para un niño: expone nombres de variables internas.

### BUG-33 · El Bucle Espejo nunca se activa 🔴
[router.py:791-822](LogicaMath/backend/app/fase5/router.py:791) busca la variante `variante+1` de la misma `estructura_padre_id`. El seed genera **una sola pregunta por familia** y sin clave `variante`, así que `mirror_q` es siempre `None` y el sistema imprime en bucle:
> `⚠️ Bucle espejo Fase 4 no pudo activarse…`

Todo el mecanismo de refuerzo tras error está inoperativo.

### BUG-34 · `estructura_padre_id` único por pregunta anula el agrupamiento 🟠
[seed.py:190](LogicaMath/backend/app/fase5/seed.py:190): `f5_m{m}_l{n}_fam_{fam:03d}_v{var}` incluye `v{var_idx}` → cada pregunta es su propia "familia". El cálculo de progreso ([router.py:396-411](LogicaMath/backend/app/fase5/router.py:396)) cuenta familias distintas, así que hoy funciona por accidente, pero rompe la semántica de familia y el espejo.

---

## PARTE F — Topología y progresión inconsistentes

### BUG-35 · El dashboard muestra un nivel 3-4 que no existe 🔴
[router.py:219](LogicaMath/backend/app/fase5/router.py:219): `n_ids = range(1, 5) if m_id == 3 else range(1, 4)` y `NIVELES_META[(3,4)]` = *"La Media Aritmética"*. Pero:
- `topology.py` define **3 niveles por módulo** (12 bloques de práctica);
- el seed no crea la sección 304 ni sus preguntas ni su `ConfiguracionProgreso`;
- `Fase5ResponderPregunta.validate_topology` rechaza `(3, 4)` con `ValueError` → **422**.

El alumno ve un nivel que no puede abrir ni superar → **el módulo 3 nunca se completa → la Fase 5 nunca se gradúa**.

### BUG-36 · Los nombres de nivel no describen el contenido generado 🟠
| Nivel | `NIVELES_META` dice | El compositor genera |
|---|---|---|
| (3,2) | "Gráficos Circulares" | descuentos de tienda |
| (3,3) | "Gráficos de Barras" | promedio de tres notas |
| (1,3) | "Áreas y Asimetrías" | resta `b - a` de partes |
| (2,2) | "El Motor de Dos Pasos" | ok |

### BUG-37 · El fallback de configuración nunca coincide 🟠
[router.py:147-155](LogicaMath/backend/app/fase5/router.py:147) busca la sección 0 con `operacion == "mixta"`; el seed la crea con `operacion="practica_libre"` ([seed.py:113](LogicaMath/backend/app/fase5/seed.py:113)) → el fallback devuelve `None` → `404 Configuración de progreso no parametrizada`.

### BUG-38 · Los desafíos se quedan sin cronómetro 🟠
El seed no fija `usa_cronometro`, `tiempo_default_segundos` ni `tipo_feedback` → defaults `False / NULL / "simple"`. En [router.py:341-342](LogicaMath/backend/app/fase5/router.py:341) `if not usa_crono: tiempo_limite = 0`. Los 12 desafíos y el mixto pierden el cronómetro de diseño (25/40/50 s) y la práctica pierde el feedback `detallado` que activa la tutoría ([router.py:828](LogicaMath/backend/app/fase5/router.py:828)).

### BUG-39 · Contradicción en el criterio de graduación 🟠
[router.py:1095-1099](LogicaMath/backend/app/fase5/router.py:1095) exige 25 aprobados y el mensaje dice *"13 de práctica y 12 desafíos"*; la topología define 12 + 12 + 1 mixto. Con BUG-35 vigente el conteo real nunca llega.

### BUG-40 · `_sync_unlocked_levels` con mapa muerto 🟡
[router.py:45-53](LogicaMath/backend/app/fase5/router.py:45): `cat_map` sólo conoce suma/resta/multiplicación/división; la Fase 5 siempre pasa `"mixta"` → todo cae en `challenge`. El resto del mapa es código muerto heredado.

### BUG-41 · El desafío mixto extrae preguntas de práctica 🟡
[router.py:544-550](LogicaMath/backend/app/fase5/router.py:544): para `modulo_id == 99` selecciona **todas** las preguntas de la fase, sin filtrar por sección, así que el examen final puede servir ítems triviales del bloque 101.

---

## PARTE G — El arnés de verificación da falsos positivos

### BUG-42 · `test_fase5_vocabulario.py` es tautológico 🟠
- `test_respuesta_deriva_de_la_formula` compara `_evaluar_formula()` **consigo misma** → no puede fallar.
- `test_variedad_estructural_por_nivel` exige `>= 2` firmas: es exactamente lo que hay (2 plantillas). Pasa mientras la repetición es ×15.
- No hay ni un test que instancie `Pregunta`, `NivelTeoria`, `ConfiguracionProgreso` ni los schemas Pydantic → los 7 bloqueantes de la Parte A pasaron inadvertidos con "11/11 PASSED".
- No hay test de exactitud numérica (decimales periódicos) ni de respuesta-visible-en-el-enunciado.

### BUG-43 · `audit_fase5_narrativas.py` mide la invariante inversa 🟡
Verifica que las variables de la fórmula **aparezcan** en el texto (lección del bug `formula_oculta` de Fase 4). No detecta el caso opuesto — que la respuesta esté *literalmente impresa* — que es el defecto real aquí (BUG-26). Reporta "0 alertas" sobre un banco donde el 30 % no exige cálculo.

### BUG-44 · Residuos textuales de "Fase 4" 🟡
Quedan en comentarios y mensajes: [router.py:189](LogicaMath/backend/app/fase5/router.py:189), [198](LogicaMath/backend/app/fase5/router.py:198), [207](LogicaMath/backend/app/fase5/router.py:207), [218](LogicaMath/backend/app/fase5/router.py:218), [384](LogicaMath/backend/app/fase5/router.py:384), [816](LogicaMath/backend/app/fase5/router.py:816) (`"Bucle espejo Fase 4"`, visible en logs), [914](LogicaMath/backend/app/fase5/router.py:914), [924](LogicaMath/backend/app/fase5/router.py:924) (`/fase4/graduate`), [979](LogicaMath/backend/app/fase5/router.py:979), [988](LogicaMath/backend/app/fase5/router.py:988). También `Fase5Types.ts` línea 4: *"Espeja exactamente los schemas de la Fase 4"*.

### BUG-45 · `eval()` sobre cadena de datos 🟡
[compositor_fase5.py:73](LogicaMath/backend/app/fase5/compositor_fase5.py:73). Hoy el JSON es propio y `__builtins__` está anulado, pero basta un `plantillas_fase5.json` editado por un admin para ejecutar código. Sustituir por un evaluador de AST con lista blanca de operadores.

---

# PLAN DE IMPLEMENTACIÓN

Ordenado por dependencia. **No avanzar de etapa sin la verificación en verde.**

## Etapa 1 — Reanimar el seeder (bloqueante) · BUG-01…05
1. `seed.py`: `diccionario_clave→diccionario`, `advertencia_comun→advertencia`, `ejemplos_json→ejemplos`, `interactivos_json→interactivos`.
2. `seed.py`: eliminar `explicacion=`; escribir la explicación en `explicacion_paso_a_paso={"html": ...}`.
3. `seed.py`: `es_activa=True` → `estado=StatusEnum.ACTIVO` en los 3 bucles de siembra.
4. `seed.py`: `max_errores_tolerados=` → `errores_tolerados=`.
5. `seed.py`: `operacion=OperacionEnum.MIXTA` en las 25 `ConfiguracionProgreso`.
6. `seed.py`: añadir `orden_desbloqueo` (1..25) y fijar explícitamente `usa_cronometro`, `tiempo_default_segundos` (0 práctica / 25-40-50 desafíos / 60 mixto), `tipo_feedback` (`detallado` práctica, `simple` desafíos), `pistas_permitidas`, `penalizacion_pista_segundos`.
7. **Verificación:** `python -m app.fase5.seed` termina sin excepción y `SELECT count(*) FROM preguntas WHERE fase_id=5` = 1140.

## Etapa 2 — Restaurar el contrato de schemas · BUG-07…15
8. Reescribir `schemas.py` espejando **campo a campo** `fase2/schemas.py` + `Fase5Types.ts`:
   - `Fase5NivelInfo`: `nivel_id, nombre, descripcion, estado, porcentaje, aciertos, requeridos, usa_cronometro`.
   - `Fase5DesafioInfo`: `desafio_id, nombre, dificultad, estado, porcentaje, aciertos, requeridos, tiempo_limite, max_errores`.
   - `Fase5ModuloInfo`: `+ color, estado, porcentaje_global`.
   - `Fase5Dashboard`: `alumno_nombre, puntos_totales, modulos, desafio_mixto_disponible, desafio_mixto_estado`.
   - `Fase5PreguntaParaAlumno`: `+ aciertos_acumulados, intentos_totales, porcentaje_actual, cantidad_requerida`.
   - `Fase5ResultadoRespuesta`: `+ early_exit, errores_sesion, max_errores_tolerados, explicacion_profunda`; `respuesta_correcta: Optional[str]`.
   - `Fase5ResponderPregunta`: `respuesta_dada: Optional[str]`, `alternativa_id: Optional[int]` (eliminar `respuesta_alumno`).
   - `Fase5ContenidoLectura`: `parrafos: List[str]`, `ejemplos`, `tip_pedagogico`, `diccionario`, `interactivos` (eliminar `contenido_html`).
9. Añadir `model_config = ConfigDict(extra="forbid")` a los schemas de salida para que un desajuste futuro falle en tests, no en producción.
10. Mantener `validate_topology` pero **después** de arreglar BUG-35.
11. **Verificación:** test que instancie cada schema con exactamente los kwargs que el router envía.

## Etapa 3 — Desbloquear el pool y la progresión · BUG-06, 33-41
12. Decidir la topología canónica: **3 niveles × 4 módulos**. Eliminar `NIVELES_META[(3,4)]` y cambiar [router.py:219](LogicaMath/backend/app/fase5/router.py:219) a `range(1, 4)`; alinear el mensaje de `/graduate` a "12 de práctica, 12 desafíos y 1 mixto".
13. Renombrar `NIVELES_META` para que describa el contenido real (BUG-36).
14. Generar variantes espejo: por cada familia, 1 original (`variante: 0`) + 3 espejos (`variante: 1..3`) con los mismos parámetros estructurales y números distintos; `estructura_padre_id` **compartido** por la familia (sin `_v{var}`).
15. Escribir `variante` dentro de `datos_numericos` en el compositor → desbloquea BUG-06 y BUG-33 de una vez.
16. Corregir el fallback de `_get_config` (sección 0 con `operacion` coherente).
17. Filtrar el desafío mixto a las secciones de desafío, no a toda la fase.
18. Limpiar `cat_map` de `_sync_unlocked_levels`.
19. **Verificación:** test de integración que recorra `/dashboard → /pregunta → /responder` de un bloque de práctica completo y de un desafío hasta el 100 %.

## Etapa 4 — Corregir la matemática · BUG-20…25
20. `_generar_valores` M3N3: `c = c_base + ((3 - (a + b + c_base) % 3) % 3)`.
21. `_generar_valores` M4N3: restringir `(a, b)` a pares cuyo `a+b` divida 100 (`4, 5, 8, 10, 20, 25, 50`).
22. Añadir al compositor un **invariante duro**: si `resultado_num` no es entero y el escenario no es de tipo `dinero`, se rechaza la composición (fail-closed, como ya hace `validar_composicion` con R1/R2).
23. Separar escenarios por `sub_magnitud` (`dinero`, `puntaje`, `conteo`, `volumen`) y exigir coincidencia en R2 → elimina "la evaluación recibe una rebaja".
24. Añadir campos `singular`/`plural` a los escenarios y un helper `_concordar(n, sing, plur)` en el compositor.
25. Si se conservan respuestas con decimal, forzar `MULTIPLE_OPCION` (nunca teclado numérico).

## Etapa 5 — Rehacer el banco de preguntas · BUG-26…32
26. **Eliminar las 5 plantillas identidad** (`formula: "a" | "b" | "total"`) y reemplazarlas por preguntas que exijan operación. Donde se quiera evaluar lectura de fracción, la respuesta debe ser la fracción (`a/b`), no un número copiado.
27. Subir de **2 a 6-8 plantillas por (módulo, nivel)** → 24 plantillas actuales pasan a ~84. Objetivo: ≤ ×2 de repetición por bloque (hoy ×7,5-×15).
28. Ampliar escenarios: mínimo **6 por módulo** (hoy 4/4/2/2) y desacoplar la elección de marco y de escenario (hoy ambos dependen de `var_idx`, quedan correlacionados).
29. Cablear `confusiones_fase5.json` a `_generar_distractores`: cada distractor debe encarnar un error catalogado y llevar su `tipo_error` + `explicacion`.
30. Persistir esos metadatos en `Alternativa.tipo_error` y `Alternativa.feedback_error` durante la siembra.
31. Reescribir `explicacion_paso_a_paso` como pasos narrados en lenguaje infantil (sin nombres de variables internas), reutilizando el formato `{"pasos": [{"orden", "texto"}]}` que ya usa `theory_examples.py`.
32. Diferenciar los desafíos: composición de dos operaciones, datos distractores en el enunciado, o inversión de la incógnita. Nunca `"[Desafío] " + práctica`.
33. Corregir el mixto final: `fam_idx` debe recorrer todas las plantillas (`fam_idx = q_count`), no quedar fijo en `mod_id`.

## Etapa 6 — Recuperar la capa visual · BUG-16…19
34. Reintroducir la generación de `datos_numericos.tipo_visual` para que el `Fase5VisualizerEngine` vuelva a renderizar. Mapa mínimo por módulo:
   - M1 → `pizza`, `shapes`, `non_homogeneous_polygon`
   - M2 → `bar_chart`, `contextual_bar`
   - M3 → `pie`, `percentage_beaker`, `fraction_percentage`
   - M4 → `beaker`, `RatioGrid`
35. Emitir los payloads que cada componente espera (`cortes`, `sombreados`, `sectors[{id,weight,points}]`, `target_value`, `target_fraction_text`, `viewBox`).
36. Rehabilitar la rama `non_homogeneous_polygon` de `/responder` con preguntas que la usen.
37. Recuperar los 16 bloques SVG del seed anterior (`git show HEAD:LogicaMath/backend/app/fase5/seed.py`) como base de la teoría/ejemplos.
38. **Verificar el bug conocido de DOMPurify** (`ALLOWED_URI_REGEXP` borrando atributos geométricos en `textService.ts`) antes de dar por buena la restauración visual — está documentado en `soluconfase5.md`.
39. `faseMetadata.ts`: reemplazar los módulos de `FASE_5` (geometría) por los 4 reales de fracciones/porcentajes; repoblar `FASE_4.modulos` con decimales; alinear colores con `MODULOS_META`.

## Etapa 7 — Arnés de verificación real · BUG-42…45
40. Tests de contrato: instanciar cada modelo SQLAlchemy con los kwargs exactos del seed (habría atrapado BUG-01…05) y cada schema con los kwargs exactos del router (BUG-08…14).
41. Test de exactitud: **toda** respuesta de bloque no monetario debe ser entera.
42. Test anti-degenerado: la respuesta correcta **no puede** aparecer como token aislado en el enunciado (BUG-26).
43. Test de variedad: redacciones distintas por bloque ≥ 30 sobre 60 preguntas (normalizando números y nombres).
44. Test de espejo: cada `estructura_padre_id` tiene exactamente 4 variantes (0..3).
45. Test de integración end-to-end del flujo dashboard → pregunta → responder → graduación.
46. Sustituir `eval()` por evaluador AST con lista blanca.
47. Limpiar los residuos textuales de "Fase 4" (BUG-44).

---

## Orden de ejecución recomendado

```
Etapa 1 → 2 → 3   (la fase vuelve a ser jugable; sin esto nada más es verificable)
Etapa 4 → 5       (el contenido deja de ser incorrecto y repetitivo)
Etapa 6           (la fase recupera su identidad visual)
Etapa 7           (en paralelo desde la Etapa 1: cada test se escribe antes del fix)
```

**Recomendación fuerte:** aplicar la Etapa 7 en modo *test-first*. Los 7 bloqueantes de la Parte A convivieron con un arnés declarado "11/11 PASSED" precisamente porque ningún test cruzaba la frontera entre el compositor y la base de datos.
