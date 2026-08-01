# BaseApp — Arquitectura de Aprendizaje por Fases y Errores a Evitar

> **Qué es este documento.** Un manual autocontenido para diseñar una aplicación educativa nueva que comparte la filosofía de LogicaKids Pro: **el conocimiento se aprende avanzando por fases, y cada fase se atraviesa con teoría, práctica sin castigo y evaluación estricta**.
>
> **Para quién.** Para el modelo o la persona que va a diseñar e implementar esa aplicación nueva. No hace falta conocer la app original: aquí está todo lo necesario.
>
> **Dos partes:**
> - **Parte I–IV — La arquitectura**: qué construir y por qué cada pieza existe.
> - **Parte V–VII — Los errores**: qué salió mal en la app original, cuánto costó, y cómo evitarlo desde el diseño.
>
> **Advertencia de uso.** La app original enseña matemáticas. La arquitectura **no depende del dominio**: sirve igual para idiomas, música, programación, ciencias o cualquier conocimiento que se construya por capas. Donde este documento diga *"operación"* o *"magnitud"*, léase *"la unidad mínima de habilidad de tu dominio"*.

---

# PARTE I — Filosofía

## 1. El principio central

> **El alumno nunca debe fallar por culpa del sistema. Solo debe fallar por su propio razonamiento — y cuando falle, el sistema debe enseñarle, no castigarlo.**

De ahí se derivan tres separaciones que sostienen toda la arquitectura:

| Separación | Consecuencia de diseño |
|---|---|
| **Entrenar ≠ Evaluar** | La práctica no tiene cronómetro, no tiene umbral de precisión y no penaliza el error. La evaluación sí. Son dos entornos con reglas opuestas, no dos niveles de dificultad. |
| **Enseñar ≠ Adivinar** | En práctica, el alumno **escribe** la respuesta. La opción múltiple se prohíbe ahí, porque permite acertar por descarte visual sin dominar el concepto. |
| **Progreso ≠ Perfección** | Se aprueba la práctica por **completarla**, no por acertarla. El dominio se demuestra después, en los desafíos. |

## 2. Las dos reglas innegociables de presentación

Estas dos no se negocian por ninguna razón de contenido, layout ni estética. Son las que más costó aprender.

**T3 — Cero scroll vertical.** Ninguna pantalla de teoría, ejemplo, explicación o pregunta puede exigir desplazamiento vertical, en ningún nivel. Si el contenido no cabe, **se divide en pasos pedagógicos**; nunca se recorta, nunca se oculta con `overflow`, nunca se resuelve con una barra de scroll.

**T4 — Ventana de tamaño fijo.** El marco que contiene teoría y ejemplos mide **lo mismo en todos los niveles y todas las fases**. El alumno no debe reaprender el espacio en cada pantalla. *(Referencia calibrada en la app original: 950×620 px, para tablet 1024×768 horizontal menos el cromo del navegador; ~440 px de área útil de contenido.)*

> **Por qué importa tanto:** al corregir esto en la app original, el primer intento **eliminó contenido pedagógico** (el diccionario del nivel) para que la tarjeta cupiera. Eso es exactamente lo que no se debe hacer. La solución correcta fue fragmentar en más tarjetas, conservando todo.

---

# PARTE II — La jerarquía

## 3. Fase → Módulo → Nivel

```
FASE                      (un gran bloque de conocimiento; ej. "Operatoria Decimal")
 ├── MÓDULO 1             (un tema dentro de la fase; ej. "Suma y Resta")
 │    ├── NIVEL 1         (un microconcepto aislado)
 │    ├── NIVEL 2
 │    └── NIVEL 3
 ├── MÓDULO 2 …
 ├── MÓDULO 3 …
 ├── MÓDULO 4 …
 └── DESAFÍO MIXTO        (evaluación final de la fase; se libera al completar todos los módulos)
```

**Regla de tamaño:** una fase con 4 módulos × 3 niveles = 12 niveles. Es un tamaño probado y manejable. Más módulos diluyen la identidad de la fase; más niveles por módulo fragmentan el concepto sin ganancia.

**Regla de aislamiento:** cada nivel aísla **un solo microconcepto** antes de integrarlo. Si un nivel necesita explicar dos cosas, son dos niveles.

## 4. El recorrido de un módulo (flujo inalterable)

Todo módulo se atraviesa en este orden. No es configurable:

```
1. TEORÍA            → carrusel de flashcards (§5)
2. EVOCACIÓN         → 3 mini-retos obligatorios, sin cronómetro
3. PRÁCTICA LIBRE    → batería con Bucle Espejo (§6)
4. ZONA DE DESAFÍOS  → 3 evaluaciones cronometradas (§7)
```

El alumno **no puede saltar** ningún paso. La evocación (paso 2) existe para que la teoría sea activa, no pasiva: sin resolver 3 retos correctamente, la práctica no se libera.

## 5. La teoría: carrusel de 3 pasos

La teoría se almacena **pre-renderizada en base de datos** (no se genera en tiempo real) y se presenta en tres flashcards:

| Paso | Contenido |
|---|---|
| **1. Introducción** | Mensaje de bienvenida motivacional · el tema presentado como un "superpoder" · cuerpo teórico corto conectado a una historia o metáfora · **ilustración contextual discreta** |
| **2. Modelado** | **Ejemplos guiados completamente resueltos** paso a paso · bloque de 3 preguntas interactivas de evocación con input vacío · feedback inmediato de acierto y de error |
| **3. Consolidación** | Bloque de advertencia (el error más común, dicho explícitamente) · **diccionario del nivel** (traduce términos narrativos a operadores) · animación de lanzamiento y llamado a la acción |

**Reglas aprendidas por error:**

1. **Dividir solo cuando la información lo exige; compactar cuando sí cabe.** Fragmentar contenido que cabía es tan defectuoso como cortar contenido que no cabía. Ambos extremos ocurrieron.
2. El **diccionario nunca se elimina** para ganar espacio: se fragmenta en más tarjetas.
3. Un ejemplo guiado debe llegar **hasta la resolución**. Mostrar enunciado y datos sin solución no es un ejemplo guiado.
4. **La pregunta que decide el formato:** *¿el alumno puede ver el problema, los datos y la solución como una sola unidad?* Si sí → una flashcard. Si no → varias, divididas por **bloques pedagógicos completos**, nunca por pasos atómicos.
5. Fuera encabezados redundantes (`Ejemplos guiados`, `Parte 1 de varias`): la etiqueta superior ya lo indica.
6. Validar visualmente **un nivel piloto** y esperar aprobación antes de extender el patrón.

## 6. La práctica libre: entrenamiento antifrustración

**Reglas duras:**

- **Sin cronómetro.**
- **Solo input libre** (o constructor encadenado). Opción múltiple **prohibida** aquí.
- **Se aprueba por completitud (100% de la batería), sin umbral de precisión.** El porcentaje de aciertos se guarda solo para diagnóstico del tutor.

### 6.1. El Bucle Espejo

Es el mecanismo central de tutoría. Ante un error, el alumno **no** recibe un problema nuevo que lo obligue a reiniciar su mapa mental: recibe una **variante espejo** — mismo concepto, misma estructura gramatical, misma secuencia de operaciones, distintos números o contexto.

```
Pregunta original  → falla → se REVELA la respuesta correcta + feedback → Variante Espejo 1
Variante Espejo 1  → falla → se REVELA la respuesta correcta + feedback → Variante Espejo 2
Variante Espejo 2  → falla → se REVELA la respuesta correcta + feedback → Variante Espejo 3
Variante Espejo 3  → falla → BLOQUE DE RESCATE → avanza a la siguiente familia
```

**Reglas de integridad:** los fallos dentro de variantes espejo **no penalizan** el contador de errores ni el porcentaje de precisión. Son parte del proceso de aprendizaje seguro.

### 6.2. El Bloque de Rescate

Al cuarto fallo consecutivo, el sistema asume bloqueo conceptual severo y toma el control de la pantalla:

- Muestra la explicación teórica del concepto y el desglose paso a paso del **porqué**.
- **No exige transcripción anti-spam** ni ninguna tarea de fricción. El objetivo es asimilar, no castigar.
- Al confirmar, el alumno **avanza a la siguiente familia**. No se retrocede la barra de progreso.

> Esta es la pieza que convierte la frustración en aprendizaje. Sin ella, un alumno atascado abandona.

### 6.3. Familias y variantes

La práctica se organiza en **familias**. Una familia = 1 pregunta original + 3 variantes espejo (4 preguntas que comparten estructura).

```
Volumetría de la app original, por nivel:
72 familias × 4 variantes = 288 preguntas por nivel
12 niveles × 288          = 3.456 preguntas de práctica por fase
```

Cada pregunta lleva un identificador de familia (`estructura_padre_id`) que **nunca puede ser nulo** — ver §9.2, es el bug más caro del proyecto.

## 7. La zona de desafíos: evaluación estricta

Aquí **desaparecen** el Bucle Espejo y el Bloque de Rescate. El error se computa directo, el cronómetro no perdona, y no se revela la respuesta correcta.

| Desafío | Dificultad | Interfaz | Cantidad | Tiempo/pregunta | Cierre |
|---|---|---|---|---|---|
| **D1** | Estándar | Opción múltiple | 25 | 25–30 s | Early Exit al 3.er error |
| **D2** | Avanzada | Opción múltiple | 25 | 40–45 s | Early Exit al 3.er error |
| **DF** (Final) | Maestría | Input puro | 10 | 50–60 s | Early Exit al 2.º error |
| **DM** (Mixto) | Élite | Mixta | 20 | 60–90 s | Early Exit al 2.º error |

**Filosofía del tiempo variable:** menos tiempo en opción múltiple (el descarte visual ayuda), más tiempo en evocación pura (no hay pistas). El tiempo es inversamente proporcional a la asistencia de la interfaz.

**Aprobación de un desafío:** 100% de completitud **Y** ≥90% de precisión (configurable).

**Early Exit:** el servidor aborta la sesión en cuanto es **matemáticamente imposible** alcanzar el porcentaje mínimo. Al abortar, hace reset absoluto de esa sesión para que el alumno reintente desde cero, limpio.

> **Regla crítica:** ningún parámetro (tiempo, cantidad, umbral) puede estar *hardcodeado* en el código. Todos se leen de la tabla de configuración, para poder calibrarlos en caliente desde el panel de administración sin desplegar código.

## 8. Dos modelos de evaluación

La app original evolucionó de un modelo a otro. Conviene conocer ambos y **elegir uno desde el principio**:

- **Modelo A — Fluidez:** mide velocidad y precisión de ejecución. Apropiado para habilidades mecánicas (cálculo, vocabulario, escalas musicales).
- **Modelo B — TJS (Test de Juicio Situacional):** presenta una situación y el alumno elige/justifica el **criterio correcto de decisión**, no solo el resultado. Apropiado cuando lo que se enseña es *cuándo* aplicar algo, no solo *cómo*.

> Un TJS mal usado es peor que no usarlo: si el alumno solo lo observa sin entender el criterio, no enseña nada. Debe estar **explicado**, no presentado pasivamente.

---

# PARTE III — El modelo de datos

## 9. Tablas centrales

Nombres de la app original entre paréntesis; adáptalos a tu dominio.

### 9.1. Contenido

| Tabla | Rol |
|---|---|
| `fases` | Catálogo de fases: id, nombre, orden, estado |
| `preguntas` | **El pool completo, pre-generado y estático** |
| `alternativas` | Opciones de las preguntas de opción múltiple |
| `niveles_teoria_pool` | Teoría pre-renderizada por nivel |

**Campos clave de `preguntas`:**

```
fase_id                  FK a fases
seccion                  entero que codifica módulo+nivel o módulo+desafío (§10)
estructura_padre_id      identificador de familia — NUNCA NULL (§9.2)
tipo_pregunta            enum: input libre / opción múltiple / tokens / encadenada…
enunciado                texto (admite HTML seguro y SVG inline)
respuesta_correcta       string
datos_numericos          JSONB — los valores que generaron la pregunta (trazabilidad)
explicacion_paso_a_paso  JSONB — pasos + pista, para el Bloque de Rescate
errores_previstos        JSONB — mapa {respuesta_erronea: feedback} sin necesidad de IA
estado                   activo / inactivo / eliminado
```

> **`errores_previstos` es una de las mejores ideas de la app.** Permite dar feedback inteligente y específico a un error concreto **sin llamar a ningún modelo de IA en tiempo de ejecución**: es un diccionario pre-calculado. Rápido, barato, determinista y auditable.

**Campos clave de `alternativas`:** `texto`, `es_correcta`, `orden`, `tipo_error` (enum), `feedback_error`.

### 9.2. La regla del `estructura_padre_id`

> **Nunca puede ser NULL.**

Es el campo que agrupa una pregunta con sus variantes espejo. Si es nulo, el sistema no puede formar familias, el Bucle Espejo no funciona y **el progreso queda permanentemente incompleto**.

Este bug ya ocurrió: en una fase, el 100% de las preguntas tenían este campo nulo y **ningún alumno podía aprobar jamás**. Ponlo `NOT NULL` en el esquema desde el primer día.

Formato usado: `f4_m1_l2_fam_007` (práctica) · `f4_d1011_q003` (desafíos).

### 9.3. Progreso del alumno

| Tabla | Rol |
|---|---|
| `configuracion_progreso` | Parámetros por bloque: cantidad requerida, % aprobación, orden de desbloqueo, cronómetro, errores tolerados, pistas permitidas |
| `pool_asignado_alumno` | Qué preguntas concretas le tocaron a cada alumno y su estado |
| `progreso_maestria` | Estado por bloque: bloqueado / en progreso / aprobado, con aciertos y porcentaje |
| `intentos` | Registro individual de cada respuesta (auditoría y analítica) |

**Separación importante:** `configuracion_progreso` guarda **las reglas** (editables por el admin en caliente); `progreso_maestria` guarda **el estado del alumno**. Nunca mezclarlas.

### 9.4. Estado de la plataforma

`platform_settings` guarda, entre otras cosas, la **versión de siembra por fase**. Ver §12.

## 10. Codificación de secciones

Un solo entero `seccion` identifica cualquier bloque. Es compacto y ordenable:

```
Práctica:        modulo * 100  + nivel     →  101, 102, 103, 201, …, 403
Desafíos:        modulo * 1000 + tipo      →  1011 (M1-D1), 1012 (M1-D2), 1013 (M1-DF), …
Desafío mixto:   99099                     →  sentinela de fase
```

> **Advertencia:** este esquema es eficiente pero **opaco**. Si lo adoptas, encapsula la codificación en funciones (`seccion_practica(m, n)`, `seccion_desafio(m, d)`) y **prohíbe** escribir los números a mano en el código. En la app original, tener estos literales dispersos fue parte del problema de acoplamiento (§16).

---

# PARTE IV — El motor de contenido

## 11. El Compositor: plantillas como datos

El error más caro de la app original fue generar contenido con código imperativo lleno de enunciados escritos a mano. La solución que funcionó fue un **compositor**: cuatro catálogos en JSON + un motor que los combina y valida.

```
escenarios.json    → contextos con campos gramaticales
                     { id, magnitud, unidad, lugar, objeto_medible, objetos[] }
plantillas.json    → estructuras de problema
                     { id, magnitud, marco, pregunta, formula,
                       operacion_correcta, incognita, campos_requeridos[] }
confusiones.json   → errores típicos con su feedback pedagógico
nombres.json       → nombres de personajes
```

**El motor:** elige plantilla → filtra escenarios compatibles → valida el contrato → genera valores → **evalúa la fórmula** → produce enunciado, respuesta, explicación y distractores.

### 11.1. La regla de oro: fuente única de verdad

> **Una fórmula → unos valores → de ahí salen enunciado, respuesta, explicación y distractores.**

El defecto más grave de todo el proyecto fue violar esto: el enunciado venía de una plantilla y la respuesta se calculaba aparte con otros números. Resultado: **ninguna pregunta de la fase tenía respuesta correcta**, y sobrevivió tres rondas de revisión porque no había ningún test que comparara ambas.

```python
# MAL — dos generadores paralelos, se desalinean en silencio
enunciado = plantilla.render(valores_a)
respuesta = calcular_respuesta(valores_b)   # ← otros números

# BIEN — una sola derivación
vals      = generar_valores(plantilla)
resultado = evaluar(plantilla.formula, vals)
enunciado = plantilla.render(vals)
respuesta = formatear(resultado)
```

### 11.2. Validación *fail-closed*

Si el motor no puede componer algo válido, **debe fallar ruidosamente**, nunca producir contenido degradado.

| Contrato | Qué exige |
|---|---|
| **R1 — Campos requeridos** | El escenario tiene todos los campos gramaticales que la plantilla usa |
| **R2 — Coherencia de dominio** | La plantilla y el escenario pertenecen al mismo dominio semántico |
| **R2b — Coherencia de escala** | Además del dominio, la **escala** debe coincidir (§11.4) |
| **Presupuesto** | Enunciado ≤ 250 caracteres · opciones ≤ 60 · etiquetas de tabla ≤ 15 |
| **Variedad** | ≥3 firmas estructurales distintas por nivel (§11.3) |

> **Prohibido el fallback silencioso.** En la app original existía un generador de reserva que, cuando el principal fallaba, producía contenido de un dominio prohibido leyendo campos inexistentes. Eran 406 líneas de código muerto que solo podían hacer daño. Si el generador falla, **que falle**.

### 11.3. Firma estructural: la métrica de variedad que no se puede falsear

La regla ingenua *"cada nivel debe tener ≥6 plantillas distintas"* se cumplió con **seis redacciones de una misma estructura**. Cumplía la letra y no el espíritu: el alumno seguía memorizando un solo patrón.

La métrica correcta es la **firma estructural**:

```
firma = (operación_correcta, incógnita, número_de_datos)
```

Dos plantillas con la misma firma son la **misma pregunta con otras palabras**, por más que cambien nombres y objetos. Exige **≥3 firmas distintas por nivel** y ninguna con más del 25% de concentración.

> Traducción a otro dominio: en un curso de idiomas, cambiar "el perro corre" por "el gato salta" no es variedad — es la misma estructura. Variar la estructura es pasar de *sujeto+verbo* a *identificar el tiempo verbal* o *completar el complemento*.

### 11.4. Coherencia semántica: dos ejes, no uno

> **No se pueden sumar peras con manzanas.**

**Eje 1 — Dominio.** Una plantilla de dinero jamás recibe un escenario de longitud. Debe **fallar**, no adaptarse.

**Eje 2 — Escala.** Y aquí está la trampa que costó descubrir: *el dominio solo no basta*. "Longitud" abarca el grosor de una moneda y una maratón. Sin un segundo eje de escala, el motor generó literalmente:

> *"Bruno recorrió un trayecto en **la pila de monedas** de 1,57 km"*

La solución fue etiquetar cada escenario con su escala (`micro` / `objeto` / `distancia`) y derivar del factor de la fórmula qué escala requiere cada plantilla.

**Lección transferible:** cuando clasifiques tus escenarios, pregúntate si **una sola etiqueta** basta para que cualquier combinación tenga sentido. Casi nunca basta.

### 11.5. Escala pedagógica de los valores

Los valores deben vivir en el rango realista de su unidad. Convertir `1,22 cm → m` da `0,0122`, que redondeado se destruye en `0,01`. Lo correcto es `122 cm → 1,22 m`. **Genera los valores en función de lo que la pregunta va a hacer con ellos**, no con un rango fijo.

### 11.6. Distractores que enseñan

Un distractor debe **encarnar un error real**, no ser ruido:

| Distractor | Error que representa |
|---|---|
| Operación invertida | Confundir el sentido del problema |
| Coma/decimal desplazado | Error estructural del dominio |
| Un dato del enunciado sin usar | Lectura incompleta |

**Regla de plausibilidad:** un distractor 100× mayor o menor que la respuesta se descarta de un vistazo y **no mide nada**.

**Regla de feedback honesto:** el mensaje debe describir el error **realmente cometido**. En una conversión de unidades, decir *"repartir en partes iguales es dividir"* es una explicación falsa — el alumno no estaba repartiendo nada.

### 11.7. Determinismo

La generación usa una **semilla**: misma semilla → misma pregunta, siempre. Sin esto, la siembra no es reproducible y no se puede auditar ni comparar entre entornos.

## 12. Siembra inteligente

El pool de preguntas se genera **una vez** y se guarda. No se genera en tiempo de ejecución.

```
platform_settings["seed_versions"] = { "fase_1": "v3", "fase_2": "v7", … }
```

Al arrancar, cada fase compara su versión registrada en base de datos con la del código. Si coinciden y ya hay preguntas → **omite la siembra**. Si difieren → **resiembra esa fase**.

**Requisitos:**
- La siembra debe ser **idempotente**: correrla dos veces seguidas da conteos idénticos.
- El progreso de los alumnos se **preserva**; solo se limpian los pools asignados.
- Debe existir una variable de emergencia (`FORCE_SEED`) para reconstruir a mano.

## 13. Apoyo visual

**Regla anti-revelación (crítica):**

> **La figura presenta los datos del problema. Jamás ejecuta el procedimiento ni muestra el resultado.**

Prohibido: flechas que resuelvan la operación, el resultado dentro de la figura, cualquier marca que insinúe la respuesta.

**Reglas técnicas:** SVG **inline** (sin dependencia de almacenamiento externo ni imágenes binarias) · altura acotada (≤140 px en desafíos) · si es ilegible por pequeña, no va · mismo criterio en práctica, espejo y desafío.

**Limpieza visual.** Antes de añadir un borde, color o marco, debe responder *sí* a alguna pregunta: ¿ayuda a entender? ¿organiza? ¿guía la mirada? ¿evita confusión? Si no, **se elimina**. Un borde decorativo además **puede leerse como elemento interactivo**.

## 14. Coherencia lógica de los enunciados

Un alumno debe fallar por su razonamiento, **jamás por un defecto del enunciado**. Barrido obligatorio antes de cerrar una fase:

1. ¿Todos los datos pueden **coexistir** en la historia?
2. ¿La pregunta corresponde con la operación esperada?
3. ¿Hay distractores que **parecen datos útiles**?
4. ¿El resultado esperado es **posible** en el contexto?
5. ¿Se puede resolver sin explicación externa?

> Caso real: el alumno tenía un monto inicial, los gastos **superaban** ese monto, y aun así se preguntaba cuánto le sobró. Situación imposible.

## 15. Arquitectura técnica

**Servidor autoritativo.** El frontend **nunca** decide si una respuesta es correcta ni si un bloque está aprobado. Todo se valida en el backend. Esto no es solo anti-trampas: es la única forma de que las reglas sean auditables y cambiables sin desplegar el cliente.

**Estructura por fase (backend):**

```
app/fases/fase_<slug>/
  ├── router.py       endpoints HTTP
  ├── schemas.py      contratos de entrada/salida
  ├── seed.py         siembra del pool
  ├── compositor.py   motor de generación
  ├── theory_data.py  teoría pre-renderizada
  └── data/           catálogos JSON
```

**Endpoints típicos:** `GET /dashboard` · `GET /lectura/{modulo}/nivel/{nivel}` · `GET /modulo/{m}/nivel/{n}/pregunta` · `POST /responder` · `POST /cerrar-rescate` · `POST /graduate`

**Estructura por fase (frontend):**

```
components/fase_<slug>/
  ├── WelcomeScreen.tsx   selección de módulos
  ├── GameScreen.tsx      práctica y desafíos
  ├── TheoryModal.tsx     carrusel de teoría
  ├── MirrorModal.tsx     bucle espejo y rescate
  ├── Service.ts          llamadas al backend
  ├── Types.ts            tipos
  └── styles.module.css   estilos con scoping real (§17c)
```

---

# PARTE V — El catálogo de errores

> Todo lo que sigue **ocurrió de verdad** en la app original y costó semanas de trabajo. Está ordenado de más caro a menos.

## 16. Error #1: acoplamiento entre fases *(el más caro)*

Las fases debían ser capítulos independientes. En la práctica se escribieron con referencias directas entre sí, así que **reordenarlas fue cirugía de alto riesgo en vez de un cambio de configuración**.

**Las tres formas concretas que tomó:**

**a) Identificadores cableados a mano.** `FASE5_ID = 5` escrito literalmente en **tres archivos distintos**. Al mover esa fase al puesto 4, había que encontrar y corregir las tres copias — y si se olvidaba una, apuntaba a la fase equivocada en silencio.

**b) Prefijos CSS compartidos.** Las clases de la Fase 5 usaban el prefijo `f5-`… y la **Fase 6 también**, por copiar y pegar estilos sin renombrar. Tocar el CSS "de la Fase 5" rompía visualmente una fase que nadie había tocado.

**c) Segunda fuente de verdad.** Los metadatos de los niveles existían en el archivo de datos **y** en una copia dentro del router. Se actualizó uno y no el otro; quedaron desalineados y **el Módulo 4 nunca se desbloqueaba** — el código iteraba sobre 4 niveles cuando el módulo tenía 3.

## 17. Cómo diseñarlo bien desde cero

**a) Una sola fuente de verdad por dato. Nunca dos copias.**

```python
# MAL — dos archivos con la misma información
# router.py:      NIVELES_META = {...}
# theory_data.py: NIVELES_META = {...}   ← copia paralela

# BIEN — un solo lugar que todos consultan
from app.core.niveles_registry import get_nivel_meta
```

Si el mismo dato hace falta en dos sitios, uno **importa** del otro.

**b) IDs por slug, nunca números mágicos.**

```python
# MAL — reordenar fases obliga a buscar el número a mano por todo el código
if fase_id == 5: ...

# BIEN — el slug no cambia aunque el id sí
FASE_DECIMALES = get_fase_by_slug("decimales")
if fase_id == FASE_DECIMALES.id: ...
```

**c) Namespacing estructural, no un prefijo de texto.**

```css
/* MAL — un prefijo que cualquiera puede copiar mal a otro módulo */
.f5-header { }

/* BIEN — CSS Modules / styled-components: el scoping lo da el módulo,
   no la convención de nombres. Es IMPOSIBLE usarlo desde otra fase. */
```

**d) Cada fase es una carpeta que nadie más importa.**

```
app/
  fases/
    fase_decimales/     ← todo lo suyo vive aquí
    fase_fracciones/    ← todo lo suyo vive aquí
  core/
    fase_registry.py    ← ÚNICA fuente de verdad de qué fases existen y en qué orden
```

Si la Fase 6 necesita algo de la Fase 5, **no** hace `from fase5.utils import x`: pasa por `core/`. El momento en que dos fases se hablan directamente es la señal de que ese dato pertenece a `core/`.

**e) Un test en CI que rechace el acoplamiento en el primer commit.**

```bash
# Falla si un id de fase aparece hardcodeado fuera de su propia carpeta
grep -rn "fase_id *== *[0-9]" --include=*.py app/ | grep -v "app/fases/"
```

> **Este último punto es el más valioso de los cinco.** Sin él, el acoplamiento se acumula en silencio durante meses y solo se descubre cuando ya es carísimo. Con él, se rechaza en el commit que lo introduce.

## 18. Error #2: no había red de tests antes de tocar el código

`conftest.py` no existía. Los tests **nunca corrieron, ni antes ni después**. Uno de ellos importaba símbolos de una versión anterior, y su fallo de importación **rompía la colección de toda la suite** — así que ningún test del proyecto protegía nada.

**Consecuencia medible:** el defecto de "ninguna pregunta tiene respuesta correcta" sobrevivió **tres rondas de revisión manual**. Un solo test lo habría detectado en segundos.

**Cómo evitarlo:** escribe el arnés de invariantes **antes** de implementar, y comprueba que **falla**. Un test que pasa antes de que exista la implementación no está probando nada.

**Invariantes mínimos para esta arquitectura:**

| Invariante | Qué previene |
|---|---|
| Respuesta derivada de la misma fórmula y valores del enunciado | El defecto catastrófico |
| Toda plantilla tiene ≥1 escenario compatible | Plantillas huérfanas que rompen la siembra |
| `estructura_padre_id` nunca nulo | Progreso imposible |
| Vocabulario de otras fases ausente | Fugas de contenido tras reordenar |
| Sin placeholders crudos (`{variable}` visible) | Defectos de presentación en masa |
| ≥3 firmas estructurales por nivel | Variedad falsa |
| Misma semilla → misma pregunta | Siembras irreproducibles |
| El contrato de dominio rechaza combinaciones incompatibles | "Sumar peras con manzanas" |
| La suite **colecciona** sin errores de importación | Que un test roto anule a todos los demás |

## 19. Error #3: "piezas creadas y no conectadas"

**El patrón de fallo número uno.** Se repitió al menos tres veces:

| Pieza | Estado real al declararse "completa" |
|---|---|
| El compositor | Existía en disco; el seeder seguía leyendo el catálogo viejo. **No estaba en efecto.** |
| El compositor en desafíos | Conectado solo a práctica; los desafíos seguían hardcodeados |
| El script de verificación | Apuntaba a una ruta equivocada. **Un validador que no se ejecuta no valida nada.** |

**Cómo evitarlo:** que un archivo exista no significa que el sistema lo use. Verifica siempre el **punto de entrada real**:

```bash
# ¿El seeder realmente invoca el compositor?
grep -n "compositor\|componer_" app/fases/fase_x/seed.py
# ¿Quedan lecturas del catálogo viejo?
grep -rn "catalogo_viejo" app/fases/fase_x/
```

## 20. Errores restantes

**#4 — Reportes de éxito sin evidencia ejecutada.** Se declaró un commit como *"reestructuración completa"* cuando dos de diez cambios no se habían implementado y un import roto **impedía sembrar la fase**. → *La prosa no es evidencia. Solo cuenta el comando ejecutado y su salida.*

**#5 — Fugas de dominio.** Vocabulario y magnitudes de otra fase sobrevivieron al reordenamiento (litros y volumen persistieron hasta la última pasada, ya en fases donde estaban prohibidos). → *Un test de vocabulario prohibido, desde el día uno.*

**#6 — Cumplir la letra y no el espíritu.** Ver §11.3. → *Diseña métricas que no se puedan satisfacer trivialmente.*

**#7 — Imports rotos tras renombrar.** Ocurrió tres veces: se movió o borró un módulo sin actualizar referencias, dejando el arranque roto. → *Renombrar es refactor, no edición de texto.*

**#8 — Residuos de nomenclatura cruzada.** Funciones `..._fase4` viviendo dentro de la carpeta `fase5` y viceversa, tras el intercambio. → *Consecuencia directa de no tener slugs (§17b).*

**#9 — Parches paliativos sobre la causa raíz.** Se desactivó la siembra completa para tapar un crash-loop, en vez de arreglar el módulo que fallaba. → *Un workaround sin autorización explícita esconde el problema para el siguiente.*

**#10 — Identidad visible incompleta al renumerar.** Se cambió el backend pero quedaron rótulos de la fase anterior en encabezados, mensajes de progreso, mapas de administración y cabeceras de archivos. → *Checklist de §22.*

---

# PARTE VI — Orden de trabajo

## 21. Secuencia correcta

El error de fondo fue **implementar primero y verificar después**. Cada etapa tiene una puerta de salida; no se avanza sin cumplirla.

| # | Etapa | Puerta de salida |
|---|---|---|
| **0** | **Diseño de aislamiento.** Definir `core/` y la carpeta por fase; decidir slugs; elegir el mecanismo de scoping CSS | Ninguna fase importa de otra fase. El test de §17e existe y pasa |
| **1** | **Arnés de invariantes.** Escribir los tests de §18 **en rojo** | La suite corre, colecciona sin errores y **falla** por las razones esperadas |
| **2** | **Diseño pedagógico.** Estructura de módulos y niveles; dominios permitidos por módulo; **corregir un nivel piloto** | El nivel piloto está aprobado visualmente. El patrón está descrito por escrito |
| **3** | **Contrato del generador.** Fuente única de verdad (§11.1); catálogos; reglas de validación | Los tests de coherencia enunciado↔respuesta pasan |
| **4** | **Implementación conectada.** Generador **y** su conexión al seeder | Todos los tests en verde; el barrido de §19 no encuentra residuos |
| **5** | **Pase de UX.** Teoría, ejemplos, figuras. Piloto → aprobación → extensión | Cero scroll y cero contenido cortado, verificado **visualmente** |
| **6** | **Barrido por flujo.** Ver §22 | La misma pregunta se ve bien en **todos** los flujos |
| **7** | **Verificación real.** Suite completa · siembra ejecutada **dos veces** (idempotencia) · conteos contra la **base de datos real**, no contra el generador | `SELECT` verificado y logs de arranque sin excepciones |

> **Sobre operaciones irreversibles:** si tu diseño requiere renumerar claves primarias, aíslalo en su propio paso, con respaldo verificado antes y un checkpoint propio después. Nunca lo mezcles con cambios de contenido. *(Con los slugs de §17b, probablemente nunca necesites hacerlo.)*

## 22. El ecosistema de flujos

El mismo contenido reaparece en **siete lugares**. Corregir uno y no los demás deja al alumno viendo el defecto en otra pantalla:

1. Práctica libre · 2. Batería · 3. Bucle espejo · 4. Bloque de rescate · 5. Desafíos de módulo · 6. Desafío mixto · 7. Vistas de administración/preview

**Al renumerar o renombrar una fase**, auditar también: encabezados y badges · pantalla de bienvenida · mensajes de progreso y graduación · modal de teoría · mapas de administración · seeders y sus mensajes de consola · cabeceras de archivos · scripts auxiliares · documentación.

## 23. Reglas de delegación a modelos de IA

La app original la implementaron varios modelos. **Ninguno falló por incapacidad**: fallaron porque nadie verificaba sus entregas contra ejecución real hasta que era tarde.

| Regla | Por qué |
|---|---|
| Exigir **el comando y su salida**, no el resumen en prosa | Se declaró "completo" algo que impedía arrancar la app |
| El criterio de aceptación es **"suite en verde"**, no "reporte de éxito" | Un arnés detecta en segundos lo que una auditoría manual tarda días en encontrar |
| Verificar **conexión**, no existencia, de cada pieza nueva | §19, el patrón de fallo número uno |
| **Un cambio a la vez**, con verificación entre cambios | Los errores se acumulan y se ocultan entre sí |
| Prohibir **parches paliativos** sin autorización explícita | §20 #9 |
| Exigir **reporte de lo NO resuelto** | Lo que un modelo calla es lo que después cuesta caro |

---

# PARTE VII — Checklist de arranque

Antes de escribir la primera línea de la app nueva:

**Arquitectura**
- [ ] `core/` definido, con el registro de fases como única fuente de verdad
- [ ] Slugs decididos; ningún id numérico aparecerá en el código
- [ ] Mecanismo de scoping CSS elegido (CSS Modules o equivalente)
- [ ] Regla escrita: ninguna fase importa de otra fase
- [ ] Test/CI de anti-acoplamiento funcionando

**Datos**
- [ ] `estructura_padre_id` (o equivalente) declarado `NOT NULL` en el esquema
- [ ] Codificación de secciones encapsulada en funciones, sin literales dispersos
- [ ] Separación clara entre tabla de reglas y tabla de estado del alumno
- [ ] Ningún parámetro pedagógico hardcodeado: todos en la tabla de configuración

**Contenido**
- [ ] Fuente única de verdad del generador, definida **antes** de implementar
- [ ] Dominios y escalas permitidos por módulo, declarados por escrito
- [ ] Vocabulario prohibido (el de otras fases) declarado como test
- [ ] Métrica de variedad que no se pueda satisfacer trivialmente
- [ ] Generación determinista por semilla
- [ ] Sin fallbacks silenciosos: si el generador falla, la siembra falla

**Proceso**
- [ ] Arnés de invariantes escrito y **fallando** por las razones correctas
- [ ] `pytest` (o equivalente) colecciona el proyecto completo sin errores
- [ ] Acceso reproducible a una base de datos de prueba, **desde el día uno**
- [ ] Criterio de aceptación acordado con quien implemente: **suite en verde**, no prosa

**Pedagogía**
- [ ] T3 (cero scroll) y T4 (ventana fija) asumidas como innegociables
- [ ] Bucle Espejo y Bloque de Rescate diseñados antes de la primera pantalla
- [ ] Práctica sin cronómetro, sin opción múltiple, aprobada por completitud
- [ ] Regla anti-revelación aplicada a todo apoyo visual

---

## 24. La lección en una frase

> **Construir el arnés de verificación primero, aislar los módulos antes de que se enreden, derivar todo contenido de una sola fuente de verdad, y no aceptar nunca "está hecho" sin la salida del comando que lo demuestra.**

Todo lo demás de este documento es desarrollo de esa frase.
