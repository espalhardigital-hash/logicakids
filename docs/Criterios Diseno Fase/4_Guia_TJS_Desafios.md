> ⚠️ **Reestructuración de la Fase 4 en curso.**
> Para todo lo relativo a la **Fase 4**, prevalece `reestructuracion.md` (raíz del repositorio).
> Las derogaciones concretas de este documento están listadas en su sección **A0**.
> Para las demás fases, este documento sigue siendo normativo sin cambios.
> *(Bloque temporal: se retira cuando CH-9 actualice este documento.)*

﻿> ⚠️ **Reestructuración de la Fase 4 en curso.**
> Para todo lo relativo a la **Fase 4**, prevalece 
eestructuracion.md (raíz del repositorio).
> Las derogaciones concretas de este documento están listadas en su sección **A0**.
> Para las demás fases, este documento sigue siendo normativo sin cambios.
> *(Bloque temporal: se retira cuando CH-9 actualice este documento.)*
> ⚠️ **Reestructuración de la Fase 4 en curso.**
> Las derogaciones concretas de este documento están listadas en su sección **A0**.
> Para las demás fases, este documento sigue siendo normativo sin cambios.
> *(Bloque temporal: se retira cuando CH-9 actualice este documento.)*

# Tomo 4: Guía de Desafíos TJS — LogicaKids Pro

> **Versión:** 1.0 | **Última actualización:** 2026-07-24 | **Prioridad documental:** 4

> Nota de autoridad documental: Este documento define el **Modelo B — Evaluación de Juicio Situacional (TJS)**, ámbito **Fases 4 a 11** de LogicaKids Pro. En caso de conflicto con el Tomo 1 (`1_Documento_Rector_Pedagogico.md`) para las Fases 4 a 11, **prevalece este Tomo 4**. Para las Fases 1 a 3, el Tomo 1 (Modelo A — Evaluación de Fluidez) sigue siendo la fuente de verdad exclusiva.

> [!IMPORTANT]
> **GUÍA OPERATIVA PARA DESARROLLADORES E IA:**
> Este documento es la fuente de verdad permanente para construir, auditar y calibrar desafíos TJS. Basta para implementar cualquier desafío de las Fases 4 a 11 **sin consultar ningún otro documento**. El plan de ejecución temporal (`docs/reestructuraciondefases.md`) caduca; este Tomo no.

---

## 1. Propósito y ámbito

### 1.1. Qué regula este documento

Define el **Modelo B — Evaluación de Juicio Situacional (TJS)** para la **Zona de Desafíos** de las Fases 4 a 11 de LogicaKids Pro. Especifica:

- Qué es un TJS y qué lo diferencia del cálculo directo.
- Las cinco formas de ítem admitidas.
- El escalón de dificultad entre desafíos.
- Los parámetros de evaluación (cantidades, tiempos, errores tolerados).
- Las reglas de redacción de enunciados (techo de 50 palabras, datos fuera de prosa).
- El sistema de pistas en los desafíos.
- El puente obligatorio entre la práctica libre y la Zona de Desafíos.
- La tabla de conformidad TJS por fase.

### 1.2. Qué NO regula este documento

- La **Práctica Libre**, el **Bucle Espejo**, el **Bloque de Rescate**, la **aprobación de niveles** y todo lo transversal no tocado por el Modelo B: eso sigue en el Tomo 1 (`1_Documento_Rector_Pedagogico.md`) y aplica a **todas** las fases.
- Las **Fases 1, 2 y 3**: sus desafíos operan bajo el **Modelo A — Evaluación de Fluidez** (Tomo 1, §6), congelado, y están fuera del alcance de este Tomo.
- La **Fase 11 (Simulacros)**: su régimen reproduce las condiciones del examen real (cronómetro global, navegación libre, validación al entregar). No es TJS ni Modelo A; tiene régimen propio.

### 1.3. Relación con los demás Tomos

| Tomo | Qué regula | Relación con este Tomo 4 |
|---|---|---|
| **Tomo 1** — Documento Rector Pedagógico | Arquitectura, pool, práctica libre, Bucle Espejo, Bloque de Rescate, aprobación, Modelo A (§6) | Las reglas transversales del Tomo 1 aplican a todas las fases. El Modelo A (§6) solo rige Fases 1-3. Desde la Fase 4, este Tomo 4 prevalece para los desafíos. |
| **Tomo 2** — Arquitectura Backend y Admin | Esquema, endpoints, Panel de Administrador | Los campos y endpoints que este Tomo exige (p. ej. `errores_tolerados`, endpoint de pistas) se implementan según el Tomo 2. |
| **Tomo 3** — Guía Frontend UX | Interfaz, animaciones, estilos | La interfaz de los desafíos TJS (botón de pista, HUD de errores, render de SVG) sigue las pautas del Tomo 3. |

---

## 2. Qué es un TJS y por qué se adopta

### 2.1. Definición

Un **TJS (Test de Juicio Situacional)** es un ítem que presenta una **situación real y concreta** y exige que el niño **decida qué hacer** (o juzgue lo que otro hizo) **antes** de operar. Se opone al **cálculo directo**, donde el número ya está dado y solo hay que operarlo.

### 2.2. Por qué se adopta

El examen de ingreso al Colégio Pedro II no pregunta "¿cuánto es 12 × 4?". Pregunta si al albañil le alcanza el material, cuál envase conviene, o dónde se equivocó alguien. El TJS cierra esa brecha: el niño no solo debe **calcular bien**, debe **entender en contexto qué le piden y aplicar el concepto correcto**, descartando datos que sobran y procedimientos que no vienen al caso.

### 2.3. Qué NO es un TJS

Para que el generador no produzca cálculo disfrazado:

- **No es un cálculo con una frase de adorno delante.** "Juan tiene 12 cajas de 4, ¿cuántas en total?" **sigue siendo cálculo directo**.
- **No es una adivinanza.** En el Desafío Final el niño **escribe el número exacto** (respuesta numérica), no elige entre opciones. Se conserva la evocación pura y se le suma el razonamiento.
- **No admite opciones absurdas.** Cada distractor es una **confusión conceptual real y nombrada** (ver §6).

---

## 3. Las cinco formas de ítem TJS

Son **cinco formas admitidas**, todas válidas. El generador combina forma × escenario × confusión.

### 3.1. Forma 1 — Decidir entre acciones ("¿cuál conviene?")

Obliga a **calcular ambas opciones** y comparar.

> *Ejemplo:* Dos bolsas de arroz con distinto contenido y precio. ¿Cuál conviene por kilo?

### 3.2. Forma 2 — Juzgar una afirmación ("¿tiene razón?")

Alguien afirma algo; el niño verifica.

> *Ejemplo:* El jardinero dice que con 30 m de alambre alcanza para cercar un cantero de 8,5 m × 7 m. ¿Tiene razón?

### 3.3. Forma 3 — Elegir el procedimiento (qué hay que hacer, no cuánto da)

La respuesta es **el paso**, no el número.

> *Ejemplo:* Para saber cuánta cinta queda de un rollo de 2 m tras cortar 45 cm, ¿qué hay que hacer primero?

### 3.4. Forma 4 — Detectar el error ajeno ("¿dónde se equivocó?")

Se muestra un procedimiento fallido; el niño localiza la falla.

> *Ejemplo:* Beto calculó el área de un triángulo de base 6 cm y altura 4 cm y obtuvo 24 cm². ¿Dónde se equivocó?

### 3.5. Forma 5 — Juzgar suficiencia de datos ("¿alcanza con lo que da?")

El niño decide si los datos bastan, sin calcular nada.

> *Ejemplo:* El enunciado dice "un terreno cuadrado" sin dar la medida del lado. ¿Alcanzan los datos para calcular la superficie?

---

## 4. El escalón entre desafíos

La dificultad **no sube dentro de un desafío**: sube **entre desafíos**. Dentro de un mismo desafío, las preguntas se sirven en orden aleatorio desde el pool, sin ordenarlas de fácil a difícil. El motor de selección aleatoria **NO se toca**.

El escalón es de género, no de aritmética:

| Desafío | Escalón | Registro predominante | Interfaz |
|---|---|---|---|
| **Desafío 1 (D1)** | TJS de **un paso**: identificar y aplicar un solo concepto. | Concreto (objetos que el niño toca). | Opción múltiple |
| **Desafío 2 (D2)** | TJS de **dos pasos**: comparar y decidir, detectar error ajeno, juzgar suficiencia. | Mezclado. | Opción múltiple |
| **Desafío Final (DF)** | TJS **integrado**: modelar y ejecutar, con **al menos un dato irrelevante** y **dos operaciones encadenadas**. | Formal (adulto). | **Respuesta numérica** (el niño escribe el número) |
| **Desafío Mixto (DM)** | Mezcla contenido de todos los módulos de la fase. | Mezclado. | Mixta |

> **Prohibición explícita:** no se introduce rampa de dificultad dentro de un desafío tocando el motor de selección. La progresión ya está garantizada *entre* desafíos. Si el implementador cree necesitar rampa interna, se detiene y consulta al dueño.

---

## 5. Tabla de parámetros de evaluación

### 5.1. Parámetros de siembra inicial (Modelo B)

Estos son **valores de siembra inicial**, no valores hardcoded: se escriben en `configuracion_progreso` y se **calibran en caliente** desde el Panel de Administrador. El backend **siempre** los lee de la BD.

| Bloque | Preguntas (`cantidad_requerida`) | Tiempo por pregunta (`tiempo_default_segundos`) | Interfaz (`tipo_pregunta`) | Errores tolerados (`errores_tolerados`) | Expulsión (Early Exit) |
|---|---|---|---|---|---|
| **Desafío 1** | 12 | 60 s | `MULTIPLE_OPCION` | **2** | al **3er** error |
| **Desafío 2** | 12 | 90 s | `MULTIPLE_OPCION` | **2** | al **3er** error |
| **Desafío Final** | 10 | 120 s | `RESPUESTA_NUMERICA` | **1** | al **2do** error |
| **Desafío Mixto de fase** | 15 | 90 s | mixta | **3** | al **4to** error |

### 5.2. Los errores tolerados se guardan EXPLÍCITOS

A partir de la Fase 4, el umbral de expulsión (Early Exit) **NO se deduce** del porcentaje de aprobación. Se **lee de un campo explícito** en `configuracion_progreso`:

| Propiedad | Valor |
|---|---|
| Nombre de columna | `errores_tolerados` |
| Tipo | `INTEGER` |
| Nullable | `NULL` permitido |
| Semántica | Cantidad de errores que el alumno puede cometer y **seguir**. El error número `errores_tolerados + 1` dispara el Early Exit. |
| Valor NULL | Cuando es NULL, el backend **cae al comportamiento heredado** (`calcular_max_errores` del Tomo 1 §7.3). Así las Fases 1-3 (Modelo A) y cualquier bloque sin migrar siguen funcionando sin cambios. |
| Valores de siembra Modelo B | D1 = 2, D2 = 2, DF = 1, DM = 3. |
| Editable en el Panel | Sí (calibración en caliente). |

**Justificación textual del dueño:** *"2 errores en 12 preguntas garantiza que el niño que responde 10 bien entendió el concepto y no queda atascado por errores de contexto o descuido"*.

El `porcentaje_aprobacion` queda como **dato informativo** (se sigue mostrando y sigue forzándose a 100 % al aprobar por el Tomo 1 §7.8), pero **ya no decide la expulsión** en Modelo B.

### 5.3. Lógica de Early Exit en el backend

```python
# Lee el umbral explícito; cae al heredado solo si es NULL.
if config.errores_tolerados is not None:
    umbral_expulsion = config.errores_tolerados + 1
else:
    umbral_expulsion = calcular_max_errores(cantidad_req, porc_aprobacion)  # Modelo A / heredado

if errores_sesion >= umbral_expulsion:
    early_exit = True
    # ... el reset de sesión y la purga de intentos NO cambian (Tomo 1 §7.2) ...
```

### 5.4. HUD de errores en vivo

El indicador de errores activos en el encabezado del desafío (p. ej. `ERRORES: 1/2`) debe mostrar como denominador **`errores_tolerados`** (no el derivado del porcentaje).

---

## 6. Catálogo de confusiones y distractores

### 6.1. Principio rector

Cada opción falsa en un ítem TJS corresponde a **una confusión concreta y nombrada**, con su feedback específico. **No hay opciones absurdas ni feedback genérico.**

### 6.2. Estructura

Se define por módulo un **catálogo cerrado de 12 confusiones típicas**, con su feedback redactado **UNA vez** y reutilizado por el generador. Se vuelca en:

- `alternativas.tipo_error` + `alternativas.feedback_error` (una fila por opción falsa).
- `preguntas.errores_previstos` (JSONB agregado con las confusiones aplicables al ítem).

### 6.3. Regla del catálogo

El implementador **no inventa** distractores fuera de las 12 confusiones del catálogo del módulo. Si un ítem necesita un distractor que no calza en ninguna de las 12, se reporta: o el ítem está mal formulado, o falta ampliar el catálogo (decisión del dueño).

---

## 7. Banco de escenarios reales

### 7.1. Principio rector

**20 escenarios de vida real por módulo**, definidos a mano y listados uno por uno con nombre, para que el implementador **NO invente contextos** fuera del banco. El generador combina **escenario × rol × objeto × cantidades**.

### 7.2. Progresión de registro dentro del módulo

| Nivel / Desafío | Registro | Escala y contexto |
|---|---|---|
| **N1** / **D1** (mayormente) | **Concreto** | Objetos que el niño toca: la hoja, la caja, la mesa, la botella. |
| **N2** / **D2** (mezclado) | **Cercano** | Escala del mundo cercano del niño: la cancha, el patio, el salón, la cuadra. |
| **N3** / **DF** (predominantemente) | **Formal** | Registro adulto y técnico: el terreno, la parcela, la hectárea, el plano a escala, el presupuesto. |

### 7.3. Regla del ancla

La primera vez que aparece una magnitud grande, la teoría la presenta con un referente comparable ("una hectárea es un cuadrado de 100 por 100 metros, como una cancha y media de fútbol"). Después ya puede usarse desnuda.

### 7.4. Regla del doble registro

El mismo objeto matemático debe aparecer dicho de las **dos maneras** en distintos ítems del mismo módulo: una vez en lenguaje cotidiano ("la cancha del colegio mide 40 m por 20 m") y otra en lenguaje formal ("un terreno rectangular de 40 m por 20 m"), para que el niño vea que es lo mismo con otro traje.

---

## 8. Reglas de redacción de enunciados TJS

Un test de razonamiento matemático no puede convertirse en un test de comprensión lectora: el niño debe fallar por **no razonar**, nunca por **no llegar a leer**.

### 8.1. Las cinco reglas duras

1. **Techo de palabras por enunciado de desafío:** Objetivo de **~30 palabras**, con un **límite duro de 40 palabras**. Se cuenta el texto en prosa; la figura, la tabla y las opciones no cuentan. La prueba de renderizado en pantalla (ventana fija 950×620 px sin scroll) prevalece sobre el conteo de palabras.
2. **Los datos numéricos:**
   > 🔴 **DEROGACIÓN NORMATIVA (A0 #3 — Desafío 1):** La norma de "los datos numéricos NUNCA en prosa" se deroga exclusivamente para el **Desafío 1 (D1)**. En el D1, los datos numéricos sí pueden ir integrados en la prosa narrativa ya que el objetivo pedagógico del D1 es evaluar la habilidad del estudiante para identificar y extraer datos numéricos dentro del texto. Para el D2, DF y DM, los datos continúan presentándose en mini tabla, lista o gráfico SVG para mantener el foco en el juicio situacional.
3. **Vocabulario controlado:** nada que no haya aparecido en la teoría del módulo.
4. **Opciones cortas y paralelas** entre sí: misma longitud y estructura, para que no se descarte por forma. La correcta no puede ser la más larga ni la única con unidad.
5. **Una sola pregunta explícita, siempre en la última línea.**
6. **Alto máximo de gráfico SVG:** Los elementos gráficos o ilustraciones vectoriales SVG inyectadas en enunciados de desafío no pueden exceder una altura máxima de **140 px** para preservar el presupuesto de espacio vertical.

### 8.2. Tres enunciados mal escritos y su corrección

**Mal ❌** (datos en prosa, > 50 palabras):
> "Juan fue a la ferretería y compró un rollo de cable que medía dos metros con cincuenta centímetros, y como no le alcanzó tuvo que volver a comprar otro pedazo de cuarenta y cinco centímetros…"

**Bien ✔** (datos en lista, texto mínimo, una pregunta al final):
> Para instalar una lámpara se usan dos tramos de cable:
> - Tramo 1: 2,5 m
> - Tramo 2: 45 cm
> ¿Cuántos metros de cable se usaron en total?

**Mal ❌** (opciones no paralelas):
> A) La bolsa A
> B) La bolsa B, porque saliendo a 3,90 el kilo es más barata…
> C) Igual
> D) No sé

**Bien ✔** (opciones cortas, paralelas):
> A) Bolsa A
> B) Bolsa B
> C) Cuestan igual
> D) Bolsa A, por traer menos

---

## 9. Sistema de pistas en los desafíos

En un desafío no hay segundos intentos (no existe el Bucle Espejo): el niño que no entiende **qué le piden** falla y, al tercer error, es expulsado. La pista existe para **evitar la expulsión injusta** de quien sabe el concepto pero se traba con el enunciado.

### 9.1. Qué dice y qué NO dice una pista

Una pista **REENCUADRA, no resuelve**: reformula la pregunta en palabras más simples y señala **qué datos sirven**.

**NUNCA:**
- Nombra la operación (sumar, restar, multiplicar, dividir, "el área es base por altura").
- Adelanta el resultado o un resultado intermedio.

**Ejemplos de pistas BUENAS (reencuadran):**
1. "Fíjate en cuánto cuesta **un solo kilo** en cada bolsa, no el precio de toda la bolsa."
2. "Pregúntate cuánto alambre necesitas para dar **toda la vuelta** al cantero, pasando por los cuatro lados."
3. "Compará un triángulo con el **rectángulo** del mismo largo y alto: ¿ocupa lo mismo o menos?"
4. "Primero pensá **cuánta superficie** hay que cubrir; recién después mirá cuánto cubre cada caja."

**Ejemplos de pistas PROHIBIDAS (revelan operación o resultado):**
1. ❌ "Dividí el precio entre los kilos: 8,40 ÷ 2."
2. ❌ "Sumá los cuatro lados: 8,5 + 7 + 8,5 + 7."
3. ❌ "El área del triángulo es base × altura ÷ 2."
4. ❌ "Te van a hacer falta 6 cajas, así que multiplicá por 40."

### 9.2. Parámetros de la pista

| Parámetro | Valor por defecto | Columna en `configuracion_progreso` | Editable |
|---|---|---|---|
| Pistas por sesión de desafío | **3** | `pistas_max_por_sesion` | Sí |
| Máximo por pregunta | **1** | (regla de negocio del endpoint) | — |
| Penalización por pista | **5 segundos** del cronómetro de esa pregunta | `pistas_penalizacion_segundos` | Sí |
| Efecto en la precisión | **Ninguno** (no penaliza aciertos ni errores) | — | — |
| Registro de uso | Se guarda para el Tutor IA | tabla `uso_pista` | — |

### 9.3. Dónde vive el texto de la pista

Dentro del JSONB `preguntas.explicacion_paso_a_paso`, en la **clave** `pista_reencuadre` (string). **No migra esquema** (la columna ya existe). Ejemplo:

```json
{
  "html": "<p>Explicación paso a paso del Bloque de Rescate…</p>",
  "pista_reencuadre": "Fíjate en cuánto cuesta un solo kilo en cada bolsa, no el precio de toda la bolsa."
}
```

### 9.4. Regla de seguridad

El texto de la pista **NO viaja en el payload inicial** de la pregunta (se leería desde las herramientas del navegador). Se sirve **solo** por un endpoint dedicado (`POST /fase{N}/desafio/pista`), bajo demanda, y ese endpoint registra el uso.

### 9.5. Contrato del endpoint de pistas

**Ruta:** `POST /fase{N}/desafio/pista`

**Entrada:**
```json
{
  "pregunta_id": 4567,
  "seccion": 1011
}
```

**Salida 200:**
```json
{
  "pregunta_id": 4567,
  "pista_texto": "Fíjate en cuánto cuesta un solo kilo en cada bolsa…",
  "pistas_restantes": 2,
  "penalizacion_segundos": 5
}
```

**Lógica (orden exacto):**
1. Autenticar → obtener `alumno`.
2. Validar que `seccion` es un **desafío** (no práctica). Si es práctica → `403`.
3. Cargar `config` → `pistas_max_por_sesion`, `pistas_penalizacion_segundos`.
4. Contar pistas usadas en la sesión. Si `usadas >= pistas_max_por_sesion` → `409` `"cupo_agotado"`.
5. Verificar que no hay pista previa para esta `pregunta_id` en la sesión. Si ya la pidió → `409` `"pista_ya_usada"`.
6. Leer `explicacion_paso_a_paso["pista_reencuadre"]`. Si falta → `422` `"sin_pista"`.
7. Registrar el uso (tabla `uso_pista`).
8. Devolver `pista_texto`, `pistas_restantes`, `penalizacion_segundos`.

### 9.6. Penalización: no penaliza la precisión

- Se descuentan `pistas_penalizacion_segundos` (5 s) del cronómetro **de esa pregunta**, no del cronómetro global.
- La pista **NO** cuenta como error ni reduce el porcentaje de precisión.
- El descuento no puede llevar el cronómetro por debajo de 0.

### 9.7. Interfaz

- **Botón de bombilla** (💡) en la tarjeta de pregunta del desafío.
- Al pulsarlo: llama al endpoint, anima el descuento del cronómetro y muestra el texto en un panel dentro de la tarjeta.
- El botón se **deshabilita para esa pregunta** una vez usada.
- Cuando `pistas_restantes == 0`, se deshabilita en toda la sesión y muestra un contador (p. ej. `Pistas: 0/3`).

---

## 10. El puente práctica → desafío

### 10.1. Riesgo que cierra

La práctica libre entrena **cálculo directo** y el desafío exige **juicio** bajo cronómetro y con expulsión. Sin puente, el niño se enfrentaría por primera vez al formato TJS contrarreloj y con Early Exit.

### 10.2. Las tres piezas obligatorias

| Pieza | Formato | Cronómetro | Bucle Espejo / Rescate | Función |
|---|---|---|---|---|
| N1, N2 de práctica | Cálculo directo | No | Sí | Fijar el microconcepto. |
| **N3 de práctica** | **TJS ligero** | **No** | **Sí** | Ver la forma TJS sin presión. |
| 3 interactivos de evocación | Cálculo directo | No | (input, acierto obligatorio) | Confirmar el concepto antes de aplicarlo. |
| Ejemplos guiados 1-3 | Cálculo resuelto | — | — | Modelar el cálculo. |
| **Ejemplos guiados 4-5** | **TJS resuelto paso a paso** | — | — | Modelar el **juicio** y las trampas. |
| Desafíos D1/D2/DF/DM | TJS estricto | **Sí** | No (hay pistas, §9) | Evaluar el juicio bajo presión. |

### 10.3. Reglas del N3 (TJS ligero)

El Nivel 3 de cada módulo usa una de las 5 formas de ítem TJS, pero es **práctica libre**: sin cronómetro, con Bucle Espejo y con Bloque de Rescate. En `configuracion_progreso`, mantiene `usa_cronometro = false` y **no** lleva `errores_tolerados` (no hay Early Exit en práctica).

### 10.4. Reglas de los ejemplos guiados

De los 5 ejemplos guiados obligatorios del carrusel teórico, los **2 últimos** son TJS resueltos paso a paso. Muestran: la situación, **qué hay que decidir**, **por qué las otras opciones son tentadoras** (la confusión de cada distractor) y **dónde está la trampa**.

Los **3 interactivos de evocación** siguen siendo cálculo directo. Verifican que el concepto quedó, no el juicio. **No** se convierten en TJS.

---

## 11. Contrato de datos de un ítem TJS

Verificado contra la BD real. Todo ítem TJS sembrado debe cumplir:

| Campo (`preguntas`) | Valor obligatorio |
|---|---|
| `tipo_pregunta` | `MULTIPLE_OPCION` en D1 y D2; `RESPUESTA_NUMERICA` en el Desafío Final. |
| `enunciado` | ≤ 50 palabras; datos fuera de la prosa (SVG inline, mini tabla o lista); una sola pregunta en la última línea. |
| `estructura_padre_id` | **NUNCA NULL**. Agrupa la familia; su NULL fue el bug que dejó 0 aprobados en fases ≥5. |
| `errores_previstos` (JSONB) | Catálogo de confusiones aplicables al ítem (§6), no textos genéricos. |
| `explicacion_paso_a_paso` (JSONB) | Incluye la clave `pista_reencuadre` (§9.3) además de la explicación del Bloque de Rescate. |
| `alternativas.tipo_error` + `feedback_error` | En D1/D2: una fila por opción; las falsas apuntan a una confusión nombrada con su feedback específico. |

---

## 12. Tabla de conformidad TJS por fase

Dos modelos de evaluación conviven en el producto:

- **Modelo A — Evaluación de Fluidez**: el formato original, definido en el §6 del Tomo 1. Ámbito declarado: **Fases 1 a 3**. Congelado.
- **Modelo B — Evaluación de Juicio Situacional (TJS)**: el formato definido en este Tomo 4. Ámbito declarado: **Fases 4 a 11**. Prevalece sobre el Tomo 1 en caso de conflicto.

| Fase | Nombre | Modelo aplicable | Estado de conformidad | Interfaz actual de los desafíos | Acción requerida |
|---|---|---|---|---|---|
| 1 | Aritmética Básica | **Modelo A** | **EXCLUIDA — congelada** | Fluidez (cálculo directo) | **Ninguna. Prohibido tocar.** |
| 2 | Desarrollo Numérico y Razonamiento | **Modelo A** | **EXCLUIDA — congelada** | Fluidez (cálculo directo) | **Ninguna. Prohibido tocar.** |
| 3 | Problemas de Texto y Sistemas Simples | **Modelo A** | **EXCLUIDA — congelada** | Fluidez (cálculo directo) | **Ninguna. Prohibido tocar.** |
| 4 | Fracciones, Porcentajes y Proporciones | Modelo B | **CONFORME** (tras migración aditiva) | TJS | Migración completada. |
| 5 | Operatoria Decimal y Conversiones | Modelo B | **CONFORME POR DISEÑO** | TJS | Se construye ya conforme a este Tomo. |
| 6 | Geometría Plana Multiforme y Áreas | Modelo B | **CONFORME POR DISEÑO** | TJS | Se construye ya conforme a este Tomo. |
| 7 | Geometría Espacial, Volumen y Magnitudes | Modelo B | **NO CONFORME — deuda declarada** | Cálculo directo | Migración a TJS pendiente (mismo patrón aditivo que Fase 4). |
| 8 | Coordenadas, Rutas y Tiempo | Modelo B | **NO CONFORME — deuda declarada** | Cálculo directo | Migración a TJS pendiente. |
| 9 | Probabilidad, Combinatoria y Lógica | Modelo B | **NO CONFORME — deuda declarada** | Cálculo directo | Migración a TJS pendiente. |
| 10 | Razonamiento Abstracto y Visual | Modelo B (previsto) | **NO APLICA TODAVÍA** | — (sin contenido) | Ninguna. Solo se reserva el número. |
| 11 | Simulacros | **Ninguno de los dos** | **NO APLICA — régimen propio** | Formato de examen real | Su evaluación imita el examen del Colégio Pedro II, no el TJS. |

### 12.1. Lectura de la deuda declarada

Las Fases 7, 8 y 9 están construidas y funcionan en producción con desafíos de cálculo directo. Migrarlas a TJS es trabajo pendiente reconocido, con el mismo patrón aditivo de la Fase 4 (marcar `estado = INACTIVO` las preguntas viejas de desafío y sembrar las nuevas, **nunca borrar**, porque hay FK desde `intentos` y `alternativas`). Se declara para que nadie la descubra y la trate como un bug.

### 12.2. Advertencia: las Fases 1, 2 y 3 están congeladas a propósito

> **NADIE debe "arreglar" las Fases 1, 2 y 3 hacia TJS.**

Sus desafíos usan el Modelo A (Tomo 1, §6): opción múltiple y evocación pura sobre cálculo directo, con tiempos cortos y umbral de expulsión derivado de la Tabla Maestra de Tolerancia (Tomo 1, §7.3). **Eso no es una omisión, es el diseño.**

Razones:
1. **Pedagógica:** en las tres primeras fases el objetivo es la automatización de la fluidez. El TJS mide otra cosa y llega cuando corresponde: a partir de la Fase 4.
2. **De producto:** están validadas en producción con alumnos reales.
3. **Documental:** si una auditoría automática marca las Fases 1-3 como "no conformes al Tomo 4", **la auditoría está mal configurada**: el ámbito del Tomo 4 empieza en la Fase 4.

### 12.3. Regla de precedencia documental

1. Este Tomo 4 manda sobre el formato de los desafíos de las Fases 4 a 11.
2. El Tomo 1 manda sobre todo lo demás (teoría, práctica libre, Bucle Espejo, Bloque de Rescate, aprobación) **en todas las fases**, y sobre el formato de desafío **solo en las Fases 1 a 3**.

---

## 13. Tabla comparativa Modelo A vs Modelo B

| Dimensión | **Modelo A — Fluidez** (Fases 1-3, congelado) | **Modelo B — TJS** (Fases 4-11, este Tomo) |
|---|---|---|
| **Qué mide** | Velocidad y precisión de cálculo (fluidez). | Juicio: decidir **qué** calcular, con qué datos, descartando lo que sobra. |
| **Pregunta típica** | "¿Cuánto es 12 × 4?" | "El albañil dice que con 8 m² le alcanza, ¿tiene razón?" |
| **Origen del ítem** | Cálculo directo parametrizado. | Situación real (banco de 20 escenarios por módulo, §7). |
| **Formato D1 / D2** | Opción múltiple, cálculo. | Opción múltiple, ítem TJS (una de las 5 formas de §3). |
| **Formato Desafío Final** | Evocación pura (`input`), cálculo. | Juicio con respuesta numérica: decide qué calcular y escribe el número. |
| **Cantidades por desafío** | 25 / 25 / 10 / 20 (D1/D2/DF/DM). | **12 / 12 / 10 / 15**. |
| **Tiempo por pregunta** | 25-30 / 40-45 / 50-60 s; DM 60-90 s. | **60 / 90 / 120 s** (D1/D2/DF); **DM 90 s**. |
| **Tolerancia de errores** | **Deducida** del porcentaje de aprobación. | **Explícita** en `errores_tolerados`: **2 / 2 / 1 / 3**. |
| **Distractores** | Descarte visual; valor "cercano" al correcto. | **Confusión conceptual nombrada** (catálogo de 12 por módulo, §6). |
| **Redacción** | Libre (cálculo desnudo permitido). | Techo de 50 palabras, datos fuera de la prosa, opciones paralelas, una sola pregunta (§8). |
| **Sistema de pistas** | No tiene. | **Sí**: 3 por sesión, reencuadra sin resolver, cuesta 5 s (§9). |
| **Puente desde práctica** | No aplica. | **Sí**: N3 en TJS ligero + 2 ejemplos guiados TJS (§10). |
| **Motor de selección** | Aleatorio del pool. **No se toca.** | Aleatorio del pool. **No se toca.** |
| **Fuente de verdad** | Tomo 1, §6. | **Este documento (Tomo 4).** |

---

## 14. Volumetría (referencia rápida)

La Fase 4 consta de una volumetría estructural de **13 bloques** (4 módulos × 3 niveles de práctica libre + 1 Desafío Mixto global).

> 🔴 **DEROGACIÓN NORMATIVA (A0 #2 — Fase 4):** Para la Fase 4, la norma de "120 familias por nivel" se deroga y se establece en **72 familias por nivel (288 familias por fase / 1.152 preguntas totales)**. Justificación: 72 familias derivadas de $\ge 6$ esquemas generadores independientes garantizan mayor variedad didáctica real que 120 familias derivadas de 1 solo esquema monótono.

| Tipo de batería | Familias por nivel | Preguntas por familia | Total sembrado por nivel | El niño responde |
|---|---|---|---|---|
| **Práctica libre** | **72** | 4 (1 original + 3 espejo) | **288** | **15** (`cantidad_requerida`) |
| **Desafío (D1, D2, DF, DM)** | — | — | **150** por desafío | Según tabla §5.1 |

---

## 15. Codificación de `seccion` (referencia rápida)

| Tipo | Fórmula | Ejemplo (M3, N2) |
|---|---|---|
| Práctica libre | `modulo_id × 100 + nivel_id` | `302` |
| Desafío 1 | `modulo_id × 1000 + 11` | `3011` |
| Desafío 2 | `modulo_id × 1000 + 12` | `3012` |
| Desafío Final | `modulo_id × 1000 + 13` | `3013` |
| Desafío Mixto de fase | `99099` | — |
