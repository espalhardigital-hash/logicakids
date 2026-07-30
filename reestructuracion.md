# Reestructuración de Fases — Documento Maestro

> Documento vivo. Se trabaja **fase a fase**. Cada cambio acordado se registra aquí antes de tocar código.
> Estado global: **PLANEACIÓN — nada ejecutado.**

---

---

## Índice

| # | Sección | Contenido |
|---|---|---|
| **1** | Objetivo | Qué persigue la reestructuración |
| **1.A** | Principio de gobierno | 🔑 Solo la Fase 4. Las demás quedan intactas |
| **1.B** | Estructura canónica | Fase → módulos → niveles + desafíos |
| **1.C** | Registro de auditoría | Correcciones aplicadas tras la revisión adversarial |
| **2** | Registro de cambios | Tabla resumen C1–C9 |
| **C1** | Intercambio Fase 4 ↔ Fase 5 | Renumeración de `id`, mecánica del swap |
| **C2** | TJS en los ejemplos guiados | Revelación por pasos con compromiso |
| **C3** | Apoyo visual SVG | Datos fuera de la prosa, regla anti-revelación |
| **C4** | Fuera TJS de práctica y espejo | Devuelve el Bucle Espejo a su diseño |
| **C5** | Paradigma de los desafíos | D1 contexto · D2 TJS · DF integrado · DM mixto |
| **C6** | Estructura de módulos | 4 módulos × 3 niveles |
| **C7** | Variedad real de preguntas | ≥6 esquemas, coherencia de unidades, los 3 bugs |
| **C8** | UX de las pantallas | Layout, `tabla_datos`, separador decimal |
| **C9** | Barrido de banco y MinIO | Eliminación de contenido muerto |
| **4** | Temas transversales | T1 progreso · T2 renombrado · T3 scroll · T4 ventana |
| **5** | Acciones de cierre | A0 derogaciones · A1–A7 cascada documental |
| **6** | Orden de ejecución | 🔑 6 etapas con dependencias críticas |
| **6.A** | Tests y reversión | Qué se rompe y cómo volver atrás |
| **6.B** | Volumen de contenido | Cuánto hay que producir |
| **6.C** | 🎯 **Particion en changes para OpenSpec** | **Artefacto de entrega**: 10 changes, dependencias y criterios de aceptacion |
| **7** | Pendiente | Lo que queda abierto |

### Convención de referencias

| Notación | Significa |
|---|---|
| `§4.3`, `§C1.5`, `§6.A` | Sección **de este documento** |
| «Tomo 1 §4.1», «Tomo 4 §8.1» | Sección **de la documentación normativa** — siempre con el Tomo delante |
| `C1`…`C9` | Cambios decididos |
| `T1`…`T4` | Temas transversales |
| `A0`…`A7` | Acciones de cierre documental |

> ⚠️ El símbolo `§` sin «Tomo» delante se refiere **siempre** a este documento.

---

## 1. Objetivo

Reordenar la secuencia de fases para dar una progresión pedagógica más lógica, y
aprovechar el reordenamiento para revisar teoría, preguntas, desafíos, módulos y niveles.

Los cambios se acuerdan y documentan aquí primero; la ejecución es posterior y explícita.

---

## 1.A Principio de gobierno — la Fase 4 es el piloto ✅

> **Todo lo decidido en este documento se aplica ÚNICAMENTE a la nueva Fase 4.**
> Las demás fases quedan **intactas** hasta nuevo aviso.

**Secuencia acordada:**

```
1. Implementar la Fase 4 con todo lo decidido aquí
2. Analizar el resultado en uso real
3. Refinar lo que haga falta  ← se da por seguro que habrá ajustes
4. Cuando la Fase 4 esté al 100 %, recién entonces
   analizar cómo replicar a las demás fases
```

**Por qué importa este principio:**

- Las reglas T3 y T4 se declaran innegociables **para toda la app**, pero su *aplicación*
  arranca solo en la Fase 4. La regla es global; el despliegue es por fases.
- Ninguna decisión de este documento autoriza tocar las fases 1–3 (congeladas), ni las
  5–11, ni el Tomo 4 en lo que afecte a otras fases.
- Las verificaciones sobre otras fases (p. ej. el formato de los desafíos de 7, 8 y 9)
  quedan **aplazadas**: se harán cuando toque planear esas fases.
- La Fase 4 funciona como **banco de pruebas**: valida las decisiones antes de propagarlas.
  Es lo que evita replicar un error doce veces.

---

## 1.B Estructura canónica de una fase

Referencia obligatoria para todo lo que sigue.

```
FASE  (macroconcepto — ej. Fase 4: Operaciones con Decimales y Conversiones)
│
└── MÓDULOS  (4 en la Fase 4)
    │
    ├── NIVELES        (cantidad variable por módulo: 2, 3, 4 o más)
    │
    └── DESAFÍOS       (3 por módulo, siempre)
        ├── Desafío 1  — estándar
        ├── Desafío 2  — avanzado
        └── Desafío Final — notablemente más complejo que los anteriores
```

### Mecánica de desbloqueo

| Evento | Consecuencia |
|---|---|
| El alumno completa un nivel | Se libera el nivel siguiente |
| El alumno completa **todos** los niveles del módulo | Se liberan los desafíos del módulo |
| Aprueba el Desafío 1 (requisitos mínimos) | Se libera el Desafío 2 |
| Aprueba el Desafío 2 | Se libera el Desafío Final |
| Completa el Desafío Final | **Módulo completo** → se libera el módulo siguiente |

La progresión es estrictamente secuencial en los tres niveles de la jerarquía:
nivel → nivel, desafío → desafío, módulo → módulo.

---

## 1.C Registro de auditoría

Este documento fue sometido a una **auditoría adversarial multi-agente** (6 dimensiones:
contradicciones internas, afirmaciones sobre el código, afirmaciones sobre los Tomos,
aritmética, orden de ejecución, estructura y huecos). Correcciones aplicadas:

| Severidad | Hallazgo | Corregido en |
|---|---|---|
| 🔴 Crítico | Los pasos de reseteo y barrido operaban sobre `fase_id 4` **antes** del intercambio → **habrían destruido Fracciones** | §6 Etapa 3 reordenada: la renumeración va primera + convención de nomenclatura obligatoria |
| 🔴 Crítico | `FASE5_ID = 5` está cableado como **valor**; tras el intercambio el seeder borraría Fracciones y sembraría dentro de su contenedor | §6 paso 3.5 (parametrizar la constante antes de sembrar) |
| 🔴 Crítico | «Escalas de mapas» se reubicaba a la Fase 5 **antes** del intercambio → volvía a Decimales y el barrido lo destruía | §6 paso 3.9 (después del intercambio) |
| 🔴 Crítico | La Fase 6 usa el prefijo CSS `f5-` (445 + 259 usos) → el renombrado la dejaría sin estilos | §4.8 (desacoplar la Fase 6 primero, con prefijos temporales) |
| 🟠 Alto | Cuatro normas vigentes contradichas sin derogarlas | §A0 (derogaciones explícitas) |
| 🟠 Alto | C4 se apoyaba en un «conflicto entre Tomos» inexistente: la cita elidía la cláusula de excepción del Tomo 1 §4.1 | C4.1 reescrita (el fundamento real es la degradación del Bucle Espejo) |
| 🟡 Medio | Tres valores vivos del techo de palabras (50 / 50 / 30) | §4.4 (valor único y flexible: ≈30, duro 40) |
| 🟡 Medio | C7.2 reintroducía TJS en la práctica libre vía dos esquemas de elección | C7.2 (sustituidos por variantes de respuesta numérica) |
| 🟡 Medio | Errores aritméticos en confusiones y balance de niveles | C7.9 y §6.B recalculados |
| 🟡 Medio | Tests, rollback y las verificaciones de §C1.6 no estaban en el plan | §6.A y §6 pasos 0.3 y 3.0 |

---

## 2. Registro de cambios

| # | Cambio | Estado |
|---|---|---|
| C1 | Intercambio Fase 4 ↔ Fase 5 mediante renumeración de `id` | **Decidido — pendiente de detalle de contenido** |
| C2 | Rediseño del TJS en los **ejemplos guiados**: revelación por pasos con compromiso; se reduce a 1 solo TJS | **Decidido** |
| C3 | Apoyo visual SVG en las preguntas: datos fuera de la prosa vía generadores existentes, con regla anti-revelación y tabla de asignación | **Decidido** |
| C4 | Se elimina el TJS de la práctica libre y de las preguntas espejo; vuelven a input libre | **Decidido** |
| C6 | **Reestructuración interna de módulos.** Estructura completa de 4 módulos × 3 niveles | ✅ **APROBADA por el usuario** |
| C7 | **Variedad real de preguntas.** ≥6 esquemas estructurales por nivel + reglas R1–R4 de coherencia semántica y de unidades | ✅ **Decidido** |
| C8 | **UX de las pantallas de pregunta.** Layout aprobado, corrección del bug de `tabla_datos`, visor sobre el teclado | ✅ **Decidido** |
| C9 | **Barrido del banco de preguntas y de MinIO.** Eliminar preguntas, teoría, configuraciones e imágenes muertas. Depende de T1 | ✅ **Decidido** |
| C5 | **Cambio de paradigma en los desafíos.** El TJS deja de ser universal: D1 = problema de contexto, D2 = TJS, DF = contexto integrado numérico. Incluye calibración de carga, contexto portante y preguntas de dos pasos | **Decidido y confirmado** |

---

## C1 — Intercambio Fase 4 ↔ Fase 5

### C1.1 Estado actual

Origen: `LogicaMath/backend/app/seed.py` → `FASES_DATA`

| id | orden | nombre |
|---|---|---|
| 4 | 4 | Fracciones, Porcentajes y Proporciones |
| 5 | 5 | Operatoria Decimal y Conversiones |

### C1.2 Estado deseado

| id | orden | nombre |
|---|---|---|
| 4 | 4 | Operatoria Decimal y Conversiones |
| 5 | 5 | Fracciones, Porcentajes y Proporciones |

### C1.3 Justificación pedagógica

**Motivo principal — falencia detectada:** los alumnos llegan a Fracciones **sin dominar
los decimales**, y el tema de fracciones los necesita (equivalencias como `0,5 = ½`,
porcentajes como decimales, conversión fracción → decimal). El orden actual obliga a
enseñar fracciones apoyándose en algo que aún no se ha visto.

Invirtiendo el orden, cuando el alumno llegue a Fracciones **ya sabrá qué es un decimal**,
y esa base podrá usarse explícitamente.

**Motivo secundario:** decimales y conversiones de medida extienden directamente el sistema
numérico posicional que el alumno ya domina. Fracciones, porcentajes y proporciones exigen
romper el pensamiento del número entero — un salto conceptual mayor. Colocar decimales
antes suaviza la curva.

#### ⚠️ Consecuencia obligatoria: la teoría de decimales NO puede citar fracciones

En la nueva Fase 4 el alumno **todavía no conoce las fracciones**. Cualquier texto que diga
*«recuerda que 0,5 es lo mismo que ½»*, *«como ya viste con las fracciones…»* o
*«esto es una fracción decimal»* queda **roto**: se apoya en algo no estudiado.

Es un fallo traicionero porque **no produce ningún error técnico**. Nada falla en pantalla;
el niño simplemente lee una explicación apoyada en algo que desconoce y se pierde.

Casos a revisar en particular:

| Concepto | Formulación válida | Formulación prohibida |
|---|---|---|
| Décima | «primera cifra a la derecha de la coma, **partes de 10**» | «un décimo, ¹⁄₁₀» |
| Centésima | «segunda cifra, **partes de 100**» | «una centésima, ¹⁄₁₀₀» |

> ✅ *La formulación actual del diccionario del Nivel 1 ya es correcta* — define décimas y
> centésimas como «partes de 10» y «partes de 100», sin nombrar fracciones.

**Tarea pendiente:** auditar `theory_data.py` (68 KB) y los enunciados de la fase en busca
de referencias a fracciones, y devolver el inventario de puntos a reescribir.

**Sentido inverso:** la Fase 5 (Fracciones) **sí podrá apoyarse en decimales** tras el
cambio. Eso no rompe nada — es exactamente el beneficio buscado.

### C1.4 Decisión técnica: **renumeración real de `id`** ✅

Se descarta el intercambio de solo `orden`. Se renumera el `id` y **el contenido viaja
con el contenedor**: las tablas de preguntas y teoría de la actual fase 5 pasan a
referenciar `fase_id = 4`.

No hay intercambio de contenido posterior — renumerar el id ya mueve todo lo que cuelga de él.

### C1.5 Mecánica obligatoria del intercambio

`id` es clave primaria y **ambos valores ya existen**, por lo que un `UPDATE` directo
colisiona. El intercambio requiere **tres pasos con un id temporal**:

```
1. fase 4 (Fracciones)  →  id temporal (ej. 904)
2. fase 5 (Decimales)   →  id 4
3. id temporal 904      →  id 5
```

Reglas:

- Todo dentro de **una sola transacción**. Una interrupción a mitad deja una fase en id
  temporal y registros huérfanos.
- Aplica en cascada a **toda tabla que referencie `fase_id`**: niveles, preguntas, teoría,
  progreso.
- El id temporal debe estar fuera del rango de fases reales para no colisionar.

### C1.6 Verificación previa pendiente

- [ ] ¿Las claves foráneas tienen `ON UPDATE CASCADE`? Si sí, las tablas hijas se
      actualizan solas. Si no, hay que actualizarlas explícitamente en orden y quizá
      diferir restricciones.
- [ ] Inventario completo de tablas con `fase_id` (no asumir que son solo niveles y preguntas).
- [ ] ¿El frontend deriva el número visible de `orden` o de `id`?
- [ ] ¿El desbloqueo de progresión usa `orden` o `id`?
- [ ] ¿Existen textos, títulos o teoría con "Fase 4" / "Fase 5" escrito de forma literal?
- [ ] ¿Hay referencias cruzadas entre la teoría de una fase y la otra?

*(Verificación no ejecutada — se hará cuando se cierre la planeación.)*

### C1.7 Estructura de módulos de la nueva Fase 4 ✅

**Decidido:** se conservan los 4 módulos actuales de la fase de decimales, **en el mismo orden**.

| # | Módulo | Descripción |
|---|---|---|
| 1 | Suma y Resta de Decimales | Alineación de comas, enteros, décimas y centésimas |
| 2 | Multiplicación de Decimales | Conteo de cifras decimales y factores |
| 3 | División con Decimales | Cocientes decimales y desplazamiento de comas |
| 4 | Conversión de Unidades | Escalera métrica: m, cm, mm, km y superficie |

#### ⚠️ Consecuencia: el seed actual tiene 5 módulos, no 4

`fase5/seed.py` línea 782 siembra **cinco** módulos (`for mod_id in range(1, 6)`), y su
cabecera lo confirma: *"16 bloques × 150; 15 de módulo + 1 mixto"* → 15 ÷ 3 = 5 módulos.

Por contenido, los módulos 3, 4 y 5 del seed son **todos de conversión**:

| Módulo del seed | Genera |
|---|---|
| 3 | `escalera_unidades("lineal", ["cm","dm","m"])` |
| 4 | `escalera_unidades("cubica", ["mL","L"])` — capacidad |
| 5 | `escalera_unidades("cuadrada", ["cm²","dm²","m²"])` — superficie |

La estructura objetivo agrupa los tres en un solo módulo 4 («Conversión de Unidades —
escalera métrica: m, cm, mm, km y superficie») y añade un módulo de **División con
Decimales** que el seed no refleja con ese número.

**Por tanto la migración sí toca la estructura de módulos:** hay que consolidar de 5 a 4 y
remapear el contenido. No es solo renumerar la fase.

#### Volumetría resultante

$$\text{bloques de desafío} = (4 \times 3) + 1 = 13$$

| | Bloques | Preguntas de desafío (150 c/u) |
|---|---|---|
| Seed actual (5 módulos) | 16 | 2.400 |
| **Objetivo (4 módulos)** | **13** | **1.950** |
| Diferencia | −3 | **−450 a desactivar** |

> Recordatorio del Tomo 4 §12.1: las preguntas **nunca se borran** — se marcan
> `estado = INACTIVO`, porque hay FK desde `intentos` y `alternativas`.

---

## C2 — TJS en los ejemplos guiados

> **Alcance de este bloque:** únicamente los TJS que viven dentro de los **ejemplos guiados**.
> Los TJS en otras instancias del módulo (N3, desafíos D1/D2/DF/DM) se analizan por separado, más adelante.

### C2.1 Problema detectado

En el formato actual, el ejemplo guiado TJS presenta **enunciado + 3 opciones + solución en un
solo bloque**. El alumno ve la respuesta antes de haber pensado la pregunta: nunca hay un
momento en que deba comprometerse con algo. El resultado es lectura pasiva.

El Tomo 4 (§10.2) lo cataloga literalmente como *"TJS resuelto"* — contenido de lectura.
No fue interactivo por diseño. Es un error de concepción: se colocó un formato de
evaluación donde no se evalúa nada.

### C2.2 Decisión ✅

**No se elimina el TJS de los ejemplos guiados. Se rediseña su presentación.**

Se sustituye el bloque único por una **revelación por pasos con un momento de compromiso**
antes de mostrar la solución.

| Paso | Se muestra | El alumno |
|---|---|---|
| 1 | La situación y la pregunta. **Sin opciones.** | Lee y entiende el contexto |
| 2 | Qué se le pide decidir | Comprende que es un juicio, no un cálculo |
| 3 | Las tres opciones | **Elige** ← momento de compromiso |
| 4 | La resolución paso a paso | Contrasta con su elección |
| 5 | Por qué las otras opciones tentaban | Ve la trampa de cada distractor |

### C2.3 Regla que sostiene el diseño — «compromiso sin consecuencia»

> La elección del **Paso 3 no puntúa, no penaliza y no bloquea el avance.**
> Se exige la acción; no se cobra el error.

Motivo: si puntuara, el ejemplo guiado dejaría de ser un ejemplo y se convertiría en
evaluación disfrazada. La función declarada en el Tomo 4 §10.4 es **modelar** el juicio y
las trampas, no medirlo. El compromiso añade atención sin añadir ansiedad.

Corolario: **el alumno ve el Paso 5 completo aunque haya acertado.** El valor está en
entender por qué las otras opciones tentaban, no en haber acertado.

### C2.4 Cantidad y composición de los ejemplos guiados ✅

**Decidido:** el bloque baja de 5 a **4 ejemplos guiados**, con **un solo TJS** (antes eran
2 — los ejemplos 4 y 5).

| # | Tipo | Pasos |
|---|---|---|
| 1 | Cálculo resuelto | 1 |
| 2 | Cálculo resuelto | 1 |
| 3 | Cálculo resuelto | 1 |
| 4 | **TJS guiado con compromiso** (formato §C2.2) | **5** |
| | **Total** | **8 pasos** |

**Motivos de bajar a 4 en lugar de reponer un quinto:**

1. El TJS nuevo ocupa **5 pasos**, no 1. Con el formato de C2 pesa más en pantalla que los
   dos ejemplos pasivos que sustituye.
2. El nivel queda en ~15 pasos; con 5 ejemplos serían ~17, demasiado largo para una sesión
   de un niño de 10 años.
3. Tres ejemplos de cálculo resuelto cubren el procedimiento; un cuarto añadiría repetición,
   no comprensión.

### C2.4bis Verificación técnica del frontend ✅ *(realizada)*

Revisados `Fase5TheoryModal.tsx`, `Fase5Types.ts` y `Fase5GameScreen.tsx`.

**Veredicto: C2 requiere desarrollo de frontend, pero es composición, no invención.**

**Estado actual del carrusel.** Construye un array plano de *slides* desde cuatro fuentes:

| Fuente | Estructura | Interacción |
|---|---|---|
| `parrafos: string[]` | Texto de teoría | Solo lectura |
| `diccionario` | Términos y definiciones | Solo lectura |
| `ejemplos` | `{enunciado, pasos[], respuesta}` | **Solo lectura — sin opciones** |
| `interactivos` | `{enunciado, respuesta, feedback_acierto, feedback_error}` | Input + botón *Verificar* |

🔴 **No existe ningún tipo de paso con opción múltiple en el carrusel.**

**Piezas reutilizables ya existentes:**

| # | Pieza | Dónde |
|---|---|---|
| 1 | Maquinaria de pasos (`currentStep`, `slides`, `goToStep`, animación) | `Fase5TheoryModal.tsx` |
| 2 | **Patrón «comprometerse → revelar»** — el alumno responde, pulsa *Verificar*, recibe feedback. Es la interacción de C2, con input en vez de opciones | `interactivos` |
| 3 | Render de opción múltiple (`alternativas`, `tipo_pregunta: 'multiple_opcion'`) | `Fase5GameScreen.tsx` |

**Lo que hay que construir:**

| Pieza | Trabajo |
|---|---|
| Tipo `ejemplos_tjs` en `Fase5Lectura` | Alternativas + explicación de cada distractor |
| Slide con opciones dentro del carrusel | Trasplantar el render de alternativas del GameScreen |
| Estado «elegida pero sin consecuencia» | El interactivo hoy califica; C2 debe **avanzar siempre** (§C2.3) |

**Estimación:** moderado. No es un componente desde cero.

**Hallazgos colaterales:**

- 🔧 **Contador único confirmado.** `Fase5TheoryModal.tsx:192` renderiza
  `Paso {currentStep + 1} de {totalSteps}` sobre un array plano que mezcla teoría, ejemplos
  e interactivos. Los **contadores por bloque** (§4.5) exigen reagrupar ese array.
  Trabajo pequeño, pero real.
- ✅ **Buena noticia para T3.** Ya existe `chunkArray(readingData.ejemplos, 1)`: el carrusel
  **ya sabe partir contenido en varios slides**. La división por presupuesto (§4.3) puede
  apoyarse en un mecanismo que ya funciona.

### C2.5 Repercusiones

**Favorables**

- Corrige la pasividad, que era el síntoma real.
- Conserva el modelado de trampas y distractores (se habría perdido al eliminar el TJS).
- Refuerza el puente práctica → desafío del Tomo 4 §10 en lugar de debilitarlo.
- **Alivia T3/T4**: estos bloques eran los más largos y los principales causantes de scroll.
  Partidos en pasos de ≤60 palabras, caben en la ventana fija.
- Reducir de 2 TJS a 1 baja aún más el volumen de contenido por nivel.

**Costos**

- Requiere **soporte técnico nuevo en el frontend**: el carrusel teórico hoy solo renderiza
  pasos de lectura. Hace falta un tipo de paso que acepte una elección y revele después.
  ⚠️ *Verificar si ya existe algo reutilizable.*
- Aplica a las fases ya construidas bajo Modelo B: **4 (fracciones), 5 (decimales) y 6 (geometría)**.
- Es más trabajo que eliminar: hay que reestructurar contenido, no borrarlo.

**Cascada documental**

- Tomo 4 §10.2 — la fila de ejemplos guiados cambia de formato y de cantidad.
- Tomo 4 §10.4 — se reescribe: dejan de ser *"TJS resuelto"*.
- Tomo 4 §14 (volumetría) — cambia el conteo.
- Añadir al Tomo 4 la anatomía de los 5 pasos.

---

## C3 — Apoyo visual SVG en las preguntas

### C3.1 Problema detectado

En los **interactivos de evocación** del carrusel teórico, los datos numéricos viajan
embebidos en la prosa:

> *"Zoe compra una carpeta a R$ 2,15 y un cuaderno a R$ 3,60. ¿Cuánto pagó en total?"*

Esto incumple la **Decisión 10** del proyecto (datos fuera de la prosa), ya codificada en
el Tomo 4 §8. Para un niño de 10 años obliga a leer, extraer y retener mientras lee —
carga cognitiva ajena al concepto que se evalúa.

Además, por efecto de T4 (ventana fija), **más de la mitad de la pantalla queda vacía**.

### C3.2 Hallazgo: la infraestructura ya existe ✅

`app/utils/svg_figuras.py` es un módulo central de generación SVG **por plantilla**, con
~40 generadores, alimentando **13.440 preguntas en todas las fases**. No requiere desarrollo nuevo.

Los dos principios rectores ya son doctrina del código:

```python
def escalera_unidades(...):
    """Escalera de conversion. Anti-revelacion: NO escribe el resultado."""

def tabla_datos(...):
    """Mini tabla. Datos numericos aqui, NO en la prosa (Decision 10)."""
```

**El problema no es capacidad, es adopción:** la infraestructura se aplicó a los enunciados
TJS (`fase5/seed.py` líneas 309, 379, 448) pero **no** a los interactivos de evocación.

### C3.3 Taxonomía del apoyo visual

| Tipo | Ejemplo | Efecto |
|---|---|---|
| Decorativo | Un cuaderno sonriente | ❌ Distrae; compite por atención sin aportar |
| Representativo | Dibujo de carpeta y cuaderno | ⚠️ Neutro; ambienta pero no se usa para resolver |
| **Organizador** | Los precios en columna, alineados por la coma | ✅ **Estructura el dato y libera memoria de trabajo** |

**Criterio de verificación:** si al borrar el gráfico la pregunta se vuelve más difícil de
leer, el gráfico servía. Si no cambia nada, era decoración.

### C3.4 Regla anti-revelación ✅

> **El visual presenta los datos; nunca ejecuta el procedimiento.**
> Puede mostrar *qué hay*. No puede mostrar *qué hacer con ello*.

Ejemplo de la frontera, con `escalera_unidades`: resalta el peldaño de origen y el de
destino y muestra el factor (`x10/div10`), pero **no escribe el valor convertido**.
Muestra el terreno, no el recorrido.

Contraejemplo prohibido: dibujar 15 cucharadas para "un frasco de 150 mL con dosis de
10 mL" — permitiría contar en vez de dividir.

### C3.5 Tabla de asignación generador ↔ tipo de dato ✅

El visual **se deriva del tipo de dato**, no se decide pregunta por pregunta. Esto es lo
que hace la medida viable a escala de miles de preguntas.

| Tipo de dato en la pregunta | Generador |
|---|---|
| Dos o más cantidades a operar (dinero, medidas) | `tabla_datos` |
| Comparación entre dos alternativas | `comparador_opciones` |
| Posición o valor entre décimas / centésimas | `recta_numerica_decimal` |
| Conversión entre unidades | `escalera_unidades` |
| Comparación de longitudes a escala | `svg_scale_bar` |

### C3.6 Repercusiones

**Favorables**
- Sin desarrollo nuevo: es invocar generadores existentes desde el seed de los interactivos.
- Cumple la Decisión 10, hoy incumplida en esas pantallas.
- Aprovecha el espacio que T4 ya reserva y hoy se desperdicia.
- Escala por plantilla; no requiere diseño manual por pregunta.

**Riesgos**
- ⚠️ El SVG del proyecto ya falló una vez: DOMPurify borraba atributos geométricos y las
  figuras salían vacías. Está corregido, pero **ampliar el uso amplía la superficie de ese
  riesgo** — incluirlo explícitamente en las pruebas.
- La asignación generador ↔ pregunta exige criterio en la siembra, no es automática.

---

## C4 — Fuera TJS de la práctica libre y de las preguntas espejo

### C4.1 Tensión entre Tomos — *(corregido tras auditoría)*

> ⚠️ **Corrección de auditoría.** Una versión anterior de esta sección afirmaba que existía
> un *«conflicto»* entre Tomos, citando el Tomo 1 §4.1 con una elisión que **omitía su
> cláusula de excepción**. El texto real es:
>
> *«Se prohíbe el uso de opciones múltiples en esta etapa, **salvo que una fase específica
> justifique una interacción especial**, porque el objetivo es eliminar el factor de
> adivinanza»* — Tomo 1 §4.1, línea 136.
>
> Con esa salvedad **no hay conflicto normativo**: el Tomo 1 ya contemplaba la excepción que
> el N3 TJS necesitaba. La decisión C4 **sigue siendo válida**, pero se sostiene sobre otro
> fundamento — el que sigue.

| Fuente | Qué establece |
|---|---|
| **Tomo 1 §4.1** | Prohíbe la opción múltiple en práctica libre **salvo excepción justificada**, para *eliminar el factor de adivinanza* |
| **Tomo 4 §10.2** | *«N3 de práctica → TJS ligero»* — invoca de hecho esa excepción |

Las cinco formas de TJS son **de elección** por definición (¿cuál conviene?, ¿tiene razón?,
¿dónde se equivocó?, ¿alcanzan los datos?). El N3 era, por tanto, práctica libre operando
bajo la excepción del §4.1.

**El fundamento real de C4 no es normativo sino de diseño:** esa excepción, aplicada al N3,
**rompe el mecanismo del Bucle Espejo** — como demuestra C4.2. El Tomo 1 permitía la
excepción, pero no previó que colisionara con su propio sistema de rescate.

### C4.2 El daño concreto: el Bucle Espejo se degrada con opciones múltiples

El Bucle Espejo fue diseñado sobre el supuesto de **input libre**:

| Intento | Qué ocurre |
|---|---|
| Falla la original | Revela la correcta → inyecta Variante Espejo 1 |
| Falla E1 | Revela la correcta → inyecta Variante Espejo 2 |
| Falla E2 | Revela la correcta → inyecta Variante Espejo 3 |
| Falla E3 | **Bloque de Rescate** ← la enseñanza real |

Con input libre, quien no entiende falla las cuatro y **llega al Rescate**. Con tres
opciones, cada intento tiene 1/3 de acierto por azar:

> **≈80% de probabilidad de acertar al menos uno de los cuatro intentos adivinando.**

Es decir: 4 de cada 5 alumnos que no entienden nada **escapan del bucle por azar y nunca
llegan al Bloque de Rescate** — justo la pieza diseñada para rescatarlos.

Problema adicional: la *variante espejo* conserva escenario, estructura y distractores
casi idénticos. Tras ver la respuesta revelada, el alumno **reconoce la posición de la
respuesta sin entender el concepto**. Con aritmética eso no ocurre porque hay que recalcular.

### C4.3 Decisión ✅

> **No hay TJS en la práctica libre ni en las preguntas espejo.**

La práctica libre vuelve íntegramente a **input libre**, conforme al Tomo 1 §4.1.
El N3 deja de ser «TJS ligero».

**Dónde vive el TJS a partir de ahora:**

| Instancia | ¿TJS? |
|---|---|
| Niveles de práctica libre (N1, N2, N3…) | ❌ No — input libre |
| Preguntas espejo (Bucle Espejo) | ❌ No — input libre |
| Interactivos de evocación | ❌ No — cálculo directo (ya era así) |
| **Ejemplo guiado** | ✅ Sí — uno solo, con el formato de C2 |
| **Desafíos D1 / D2 / DF / DM** | ✅ Sí — TJS estricto |

### C4.4 Repercusiones

**Favorables**
- Ya no hace falta invocar la excepcion del Tomo 1 §4.1: la practica libre vuelve a ser input libre puro, que es el caso por defecto de la norma.
- **El Bucle Espejo recupera su supuesto de diseño.** No requiere ningún cambio: vuelve a
  funcionar como fue concebido, sin escape por azar.
- El Bloque de Rescate vuelve a ser inevitable para quien no domina el concepto.
- Desaparece el problema de los módulos con menos de 3 niveles: ya no se exige un N3 con
  rol especial.
- Menos contenido TJS que producir y mantener.

**A vigilar**
- ⚠️ El puente práctica → desafío del Tomo 4 §10 **se apoya ahora en una sola pieza**: el
  ejemplo guiado de C2. Queda mitigado porque C2 lo convirtió en activo (con compromiso)
  en lugar de pasivo, pero conviene verificar que basta.

**Cascada documental**
- Tomo 4 §10.2 — la fila «N3 de práctica / TJS ligero» desaparece o pasa a cálculo directo.
- Tomo 4 §10.3 — «Reglas del N3 (TJS ligero)» se elimina por completo.
- Tomo 1 §4.1 — la prohibición de opción múltiple queda vigente sin excepciones.

---

## C5 — Cambio de paradigma en los desafíos: el TJS deja de ser universal

### C5.1 Diagnóstico

El enfoque anterior llevó **todos** los desafíos a formato TJS. Fue un mal enfoque: el
examen de ingreso del Colégio Pedro II contiene **ambos** tipos de ítem. Si todo el
entrenamiento es juicio situacional, el alumno llega preparado para un examen que no existe.

Falta entrenar una habilidad distinta y crítica: **traducir un enunciado en contexto a una
operación**. Es lo que más se falla en un examen de ingreso y hoy la zona de evaluación no
la ejercita.

### C5.2 Los tres formatos, separados

| Formato | Qué se le da | Qué hace el alumno |
|---|---|---|
| Cálculo directo | `2,15 + 3,60` | Opera. Nada que interpretar |
| **Problema de contexto** | *"Ana compró un cuaderno de R$ 3,50 y un lápiz de R$ 8,50. ¿Cuánto gastó?"* | **Lee, extrae, infiere**, traduce a operación y opera |
| **TJS** | *"Ana tiene R$ 10. ¿Le alcanza para ambos?"* | **Decide qué hay que hacer**, opera y **juzga** el resultado |

> ⚠️ Esto contradice al Tomo 4 §2.3, que hoy descalifica el problema de contexto
> (*"sigue siendo cálculo directo"*). **El Tomo 4 debe corregirse**: el problema de
> contexto se reconoce como formato legítimo con valor propio.

### C5.3 Decisión ✅ — un solo desafío TJS por módulo

| Desafío | Formato | Interfaz | Habilidad evaluada |
|---|---|---|---|
| **D1 — estándar** | **Problema de contexto** | Opción múltiple | Leer, extraer, inferir y traducir a operación |
| **D2 — avanzado** | **TJS** | Opción múltiple | Decidir y juzgar antes de operar |
| **DF — final** | Problema de contexto integrado | Respuesta numérica | Resolver sin apoyo: dato irrelevante + dos operaciones encadenadas |
| **DM — mixto de fase** | Mezcla de formatos | Mixta | Lo más parecido al examen real |

Escalón resultante: **comprender → juzgar → ejecutar solo.**
Cada peldaño evalúa algo distinto, no tres versiones del mismo formato.

### C5.4 Argumento técnico: por qué el TJS no puede ir en el DF

El DF es `RESPUESTA_NUMERICA`. Ninguna de las cinco formas TJS admite respuesta numérica:

| Forma TJS | Respuesta natural | ¿Numérica? |
|---|---|---|
| 1 — ¿Cuál conviene? | "A" o "B" | ❌ |
| 2 — ¿Tiene razón? | Sí / No | ❌ |
| 3 — ¿Qué hay que hacer primero? | Un procedimiento | ❌ |
| 4 — ¿Dónde se equivocó? | Un lugar | ❌ |
| 5 — ¿Alcanzan los datos? | Sí / No | ❌ |

El DF **ya estaba en contradicción con su propia definición** en el Tomo 4. Sacarlo del TJS
resuelve esa contradicción en lugar de agravarla.

### C5.5 El D1 es la excepción a C3 — y la regla es coherente

C3 exige datos fuera de la prosa. Aplicado al D1 **destruiría lo que el D1 mide**: si los
importes se sirven en una tabla, ya no hay que leer ni inferir.

Regla unificadora:

> **Se retira la carga cognitiva ajena a lo que se está midiendo.**
> - En práctica y teoría se mide el **concepto** → leer es carga ajena → datos estructurados (C3).
> - En el **D1** se mide **la lectura misma** → nada es ajeno → **datos en la prosa**.

No es una excepción arbitraria: es la misma regla aplicada con coherencia. El andamio se
retira justo donde se evalúa la habilidad que el andamio sustituía.

### C5.6 Lo que se conserva del Tomo 4 aunque el D1 deje de ser TJS

**El catálogo de confusiones (§6) sigue vigente.** Los distractores no pueden ser números
al azar: cada opción falsa es el resultado de un error real y nombrable.

Ejemplo con `R$ 3,50 + R$ 8,50 = R$ 12,00`:

| Opción | Origen del error |
|---|---|
| **12,00** | ✅ Correcta |
| 11,00 | Olvidó el acarreo (`0,50 + 0,50 = 1,00`) |
| 12,10 | Alineó mal la coma |
| 5,00 | Restó en vez de sumar (mala interpretación del enunciado) |

Así el D1 sigue siendo **diagnóstico**: la opción elegida revela *qué* entendió mal el
alumno, no solo que falló.

También se conserva la regla de **una sola pregunta al final del enunciado** (§8).

> ⚠️ **El techo de palabras NO es 50.** Fue rebajado en §4.4 tras medirlo contra la pantalla
> real. Ver §4.4 para el valor vigente.

### C5.7 Repercusiones

**Favorables**
- 🎯 **La deuda de las fases 7, 8 y 9 se abarata drásticamente.** El Tomo 4 §12 las declara
  NO CONFORMES por tener desafíos de "cálculo directo" y exige migrar los 3. Bajo el nuevo
  paradigma **solo 1 de 3 necesita ser TJS**: si sus D1 y DF ya son problemas de contexto,
  ya son conformes. La deuda pasaría de 9 desafíos a 3.
  ⚠️ *Verificar qué formato tienen hoy realmente.*
- Los problemas de contexto son **más baratos de generar** que los TJS: escenario + números,
  frente a escenario + confusión nombrada + 3 distractores justificados.
- El DM pasa a tener sentido pleno: mezcla módulos **y** formatos = lo más parecido al examen real.
- La opción múltiple en D1/D2 es aceptable aquí (a diferencia de la práctica, ver C4): con
  12 preguntas y 2 errores tolerados hay que acertar 10 seguidas — el azar no basta.
- T3/T4 se cumple más fácil en D1 que en un TJS: el problema de contexto es más corto.

**Costos**
- Re-siembra de D1 y DF en las fases ya construidas (4, 5 y 6): 2 de 3 desafíos × 150
  preguntas × nº de módulos.
- ⚠️ **T3/T4 en la zona de desafíos no admite la salida "dividir en pasos"**: bajo cronómetro
  el alumno necesita ver enunciado y opciones a la vez. Hay que resolverlo con presupuesto
  de contenido estricto, no con paginación.

**Cascada documental (Tomo 4)**
- §2.3 — deja de descalificar el problema de contexto.
- §3 — las cinco formas TJS pasan a aplicar **solo al D2**.
- §4 — el escalón se redefine por **formato**, no por número de pasos.
- §10.2 — tabla del puente.
- §12 — tabla de conformidad completa (y la deuda de 7–9 se recalcula).

---

### C5.8 Principio rector: los desafíos no re-evalúan el concepto, añaden capas de carga

El concepto **ya se evaluó en la práctica libre**. La zona de desafíos no vuelve a medirlo:
añade **grados de carga** sobre un concepto ya dominado.

| Etapa | Qué añade | Qué mide |
|---|---|---|
| **Práctica libre** | Nada — concepto desnudo | ¿Domina la operación? |
| **D1** | **Carga simple** | ¿Reconoce la operación dentro de una situación? |
| **D2** | **Carga de juicio** (TJS) | ¿Decide qué hacer antes de operar? |
| **DF** | **Carga total** | ¿Sostiene todo junto, sin apoyo? |

No son tres exámenes del mismo concepto: son **cuatro grados de carga**.

### C5.9 Calibración operativa de la carga ✅

«Carga simple» debe ser medible, o los generadores derivan y el D1 acaba siendo tan difícil
como el DF. Definición por seis parámetros contables:

| Dimensión | **D1 — carga simple** | **D2 — TJS** | **DF — carga total** |
|---|---|---|---|
| Datos a extraer | **Exactamente 2** | 2 – 3 | **3 o más** |
| Operaciones | **1** | 1–2 + juicio | **2 encadenadas** |
| Dato irrelevante | **Ninguno** | Opcional | **Al menos 1, obligatorio** |
| ¿La operación está señalada? | **Sí** — palabra clave visible (*"en total"*, *"le quedan"*) | No | **No** — hay que inferirla |
| Longitud del enunciado | **≈ 20 palabras** | ≈ 30 | ≈ 30 |
| Interfaz | Opción múltiple | Opción múltiple | **Respuesta numérica** |

La fila decisiva es la cuarta: en el D1 la palabra clave **entrega** la operación (la carga
está en situar los números en contexto); en el DF esa señal desaparece.

**Estos seis parámetros son contables → se puede escribir un validador automático** que
rechace un D1 con 3 datos o sin palabra clave. Es lo que impide que el escalón se degrade
con el tiempo.

### C5.10 Especímenes canónicos — Módulo 1, suma de decimales

> **D1 · carga simple**
> *Ana compró un cuaderno de R$ 3,50 y un lápiz de R$ 8,50. ¿Cuánto gastó **en total**?*
> — 2 datos · 1 operación · señal explícita · 23 palabras

> **D2 · TJS**
> *Ana lleva R$ 12,00. Quiere el cuaderno de R$ 3,50 y el lápiz de R$ 8,50. ¿Le alcanza?*
> — Hay que decidir qué comparar antes de operar

> **DF · carga total**
> *Ana llevó R$ 20,00. Compró un cuaderno de R$ 3,50, un lápiz de R$ 8,50 y **miró** una mochila de R$ 45,00. ¿Cuánto le sobró?*
> — 3 datos (uno irrelevante) · 2 operaciones encadenadas · sin señal · respuesta numérica

Sube la **carga**, no la dificultad aritmética.

### C5.11 El DF exige contexto portante, no ilustrativo ✅

La situación del DF **no puede ser decorativa**: debe obligar al alumno a pensar en el
contexto para resolver.

> **Prueba del contexto portante:** quita el contexto y deja solo los números.
> Si el alumno todavía puede resolver → el contexto era **decoración**.
> Si sin el contexto la pregunta se vuelve irresoluble o ambigua → el contexto **carga peso**.

| Enunciado | Al quitar el contexto | Veredicto |
|---|---|---|
| *"Ana compró 3,50 y 8,50. ¿Cuánto gastó en total?"* | `3,50 + 8,50` — problema idéntico | ❌ Ilustrativo |
| *"Ana necesita 2,4 L de jugo. Cada botella trae 1 L. ¿Cuántas botellas compra?"* | `2,4 ÷ 1 = 2,4` — **pero la respuesta es 3** | ✅ **Portante** |

**Tres mecanismos que hacen portante el contexto en decimales:**

| Mecanismo | Ejemplo |
|---|---|
| **Redondeo forzado por la realidad** | Botellas, cajas, dosis: no existen fracciones de objeto |
| **Dato implícito en la situación** | *"pagó con un billete de R$ 20"* — el 20 no se enuncia como dato |
| **Restricción que invalida el resultado aritmético** | *"las dosis deben ser completas"*, *"la cinta no se puede empalmar"* |

### C5.12 Preguntas de dos pasos en el DF ✅

Algunas preguntas del DF deben exigir **inferir un valor intermedio** que no aparece en el
enunciado, y usarlo para llegar al resultado.

> *Ana llevó R$ 20,00. Compró 3 cuadernos de R$ 3,50 cada uno. ¿Cuánto le devolvieron?*
> **Paso 1 (inferido):** 3 × 3,50 = 10,50 ← este valor no está escrito
> **Paso 2:** 20,00 − 10,50 = **9,50**

Esto distingue «dos operaciones» de «dos pasos encadenados»: el valor intermedio debe
producirlo el alumno para poder continuar.

**No todas las preguntas son así.** Proporción objetivo: **≈15% del pool**, de modo que en
una sesión de 10 preguntas el alumno encuentre en promedio 1–2 de mayor dificultad.

#### Compatibilidad con la prohibición del Tomo 4 §4

El Tomo 4 prohíbe explícitamente *"introducir rampa de dificultad dentro de un desafío
tocando el motor de selección"*. **Esta decisión no la vulnera:**

| | Qué es | ¿Prohibido? |
|---|---|---|
| Rampa | Ordenar las preguntas de fácil a difícil dentro del desafío | ❌ Sí |
| **Lo decidido** | Pool **heterogéneo**, servido en **orden aleatorio** | ✅ No — la prohibición apunta al *orden*, no a la *variedad* |

**Decisión: Opción A** — sembrar ≈15% de preguntas de dos pasos y dejar que el azar reparta.

- ✅ **El motor de selección aleatoria NO se toca.**
- Consecuencia aceptada: **varianza entre alumnos** — algunos recibirán 0 preguntas de dos
  pasos y otros 3 o 4. Se considera aceptable: un examen real tampoco reparte la dificultad
  de forma pareja.
- Se descarta la Opción B (muestreo estratificado para garantizar 1–2 por sesión) porque
  **sí tocaría el motor de selección**, con riesgo sobre once fases en producción.

### C5.13 Regla de las tres capas — no se evalúa una convención que no se enseñó ✅

**Problema detectado por el usuario:** si el DF exige redondeo por contexto (la cuenta da
2,4 pero la respuesta válida es 3) y el alumno nunca aprendió esa convención, la experiencia
es *"hice bien la cuenta y me dice que está mal"*. No enseña: desmoraliza y **le hace dudar
de la aritmética que sí domina**.

> **Regla:** no se evalúa una convención que no se haya enseñado antes.
> Si el DF exige redondeo por contexto, ese criterio debe estar en la teoría de algún nivel
> del módulo. La secuencia lo garantiza: los desafíos solo se abren cuando todos los niveles
> están completos.

**Capa 1 — Enseñarlo en la teoría.** Paso dedicado en el nivel donde aparece por primera vez:

> 📦 **Cuando el resultado no puede partirse**
> A veces la cuenta da un decimal, pero la realidad no lo admite.
> Necesitas 2,4 litros y cada botella trae 1 litro. 2 botellas **no alcanzan**. Necesitas **3**.
> Regla: si sobra aunque sea un poquito, **se sube al siguiente entero**.

**Capa 2 — La unidad delata la naturaleza de la respuesta.** El enunciado pide el objeto,
no el número:

- ✅ *"¿Cuántas **botellas** compra?"* → las botellas se cuentan enteras
- ❌ *"¿Cuánto es 2,4 ÷ 1?"* → invita a responder el decimal

**Capa 3 — Feedback específico para el error previsto.** La infraestructura **ya lo soporta**:
el Tomo 4 §11 exige `errores_previstos` (JSONB) y el seed de la fase ya mapea respuestas
numéricas equivocadas a feedback concreto. Se registra `2,4` como error previsto:

> *"Tu cuenta está bien: 2,4. Pero no se pueden comprar 2,4 botellas — con 2 te faltaría.
> Necesitas 3."*

Matiz decisivo: **primero se valida la aritmética, después se corrige la interpretación.**
El alumno no queda pensando que sumó mal; sabe exactamente dónde estuvo el desvío.

### C5.14 El Desafío Mixto (DM) ✅

**Ámbito confirmado:**

| Desafío | Ámbito | Cuándo se libera |
|---|---|---|
| D1, D2, DF | **Por módulo** | Al completar todos los niveles del módulo |
| **DM** | **Uno solo por fase** | Al completar **todos los módulos** de la fase |

El DM es la prueba final que cierra la fase.

**Composición decidida:** el DM se integra con preguntas de los **tres formatos** (D1, D2 y
DF), cubriendo **todos los módulos** de la fase.

| Formato | Cantidad (de 15) |
|---|---|
| D1 — problema de contexto, opción múltiple | 5 |
| D2 — TJS, opción múltiple | 5 |
| DF — contexto integrado, respuesta numérica | 5 |

Esto da por fin sentido pleno a la interfaz **«mixta»** ya sembrada para la sección `99099`.

**Pool propio, no reutilización.** «Integrado por preguntas de D1, D2 y DF» significa
**replicar los formatos en su propio pool**, no reutilizar las preguntas ya respondidas:

| | Consecuencia |
|---|---|
| ❌ Reutilizar preguntas ya vistas | Mide memoria, no dominio; además exigiría tocar el motor de selección |
| ✅ **Pool propio con los tres formatos** | Preguntas nuevas, misma evaluación. Es lo que ya existe en la sección `99099` |

⚠️ **Punto de calibración a vigilar:** el DM tolera 3 errores en 15 (hay que acertar 12).
Con 5 preguntas de formato DF —sin opciones, las más duras— puede resultar más exigente que
el propio DF, que tolera 1 error en 10. Revisar con datos reales; el parámetro es calibrable
en caliente desde el Panel, así que no bloquea la implementación.

## C6 — Reestructuración interna de los módulos de la Fase 4

### C6.1 Estado actual del seed (5 módulos × 3 niveles = 15 niveles)

| Módulo | N1 | N2 | N3 |
|---|---|---|---|
| **1** | Suma alineando la coma | Resta con completado de ceros | Combinadas en contexto |
| **2** | Multiplicación con conteo de posiciones | 🔴 **División con desplazamiento de la coma** | 🔴 Repartición y costo unitario (división) |
| **3** | Escalera métrica lineal | Operaciones con unidades mixtas | Escalas de mapas y rutas por tramos |
| **4** | Escalera cúbica | Volumen y capacidad: dm³=L, cm³=mL | Problemas de capacidad en contexto |
| **5** | Escalera cuadrada | Pulgadas y pies a cm | Hectáreas, m² y reparto en lotes |

### C6.2 🔴 Error detectado: no existe módulo de División

El módulo 2 actual **mezcla multiplicación y división**: sus niveles 2 y 3 son de división.
La tarjeta de la UI anuncia «División con Decimales» como módulo 3, pero **ese módulo no
existe en el seed**.

### C6.3 Decisiones ✅

**a) Módulo 2 — solo multiplicación.** Progresión por cifras decimales y por número de
operandos que las llevan:

| Nivel | Caracterización | Ejemplo |
|---|---|---|
| N1 | Un factor con decimales, **1 cifra decimal** | `4,5 × 3` |
| N2 | Un factor con decimales, **2 cifras decimales** | `4,52 × 3` |
| N3 | **Ambos factores con decimales** | `45,2 × 2,52` |

El N3 es el salto real: hay que contar las cifras decimales de ambos factores para colocar
la coma en el producto («conteo de cifras decimales y factores», según la tarjeta).

**b) Módulo 3 — solo división, misma lógica.**

| Nivel | Caracterización | Ejemplo |
|---|---|---|
| N1 | Dividendo con 1 cifra decimal, divisor entero | `4,5 ÷ 3` |
| N2 | Dividendo con 2 cifras decimales, divisor entero | `4,52 ÷ 2` |
| N3 | **Ambos con decimales** | `45,2 ÷ 2,5` |

⚠️ El N3 introduce un **concepto nuevo, no solo más dificultad**: con divisor decimal hay
que **desplazar la coma en ambos** antes de dividir. Requiere teoría propia.

**c) Módulo 4 — unidades de medida, SIN volumen ni capacidad.**

> Volumen y capacidad **salen de la Fase 4**: corresponden a la fase de Geometría Espacial
> y Volumen.

| Contenido actual | Destino |
|---|---|
| Módulo 4 completo (escalera cúbica, dm³=L, capacidad) | ➡️ Fuera — a la fase de Geometría 3D |
| Nivel 502 «Pulgadas y pies a cm» | ➡️ **Descartar** — unidades imperiales, fuera del alcance del examen |

### C6.4 Mapa de reestructuración de módulos

| Módulo objetivo | Origen | Trabajo |
|---|---|---|
| **1 — Suma y Resta de Decimales** | Módulo 1 actual | ✅ Encaja; revisión menor |
| **2 — Multiplicación de Decimales** | Módulo 2 actual **quitando división** | 🔧 Rehacer N2 y N3 |
| **3 — División con Decimales** | **No existe.** Semilla: N2 y N3 del módulo 2 actual | 🔨 Módulo nuevo, 3 niveles |
| **4 — Conversión de Unidades** | Consolidar módulos 3 y 5 actuales (el 4 sale de la fase) | ✂️ De 6 niveles candidatos a 3 |

### C6.5 Módulo 4 — Conversión de Unidades ✅

**Superficie sale de la Fase 4**: corresponde a Geometría Plana y Áreas. El módulo 4 trata
**exclusivamente unidades de medida lineales**.

El nivel de escalera métrica original concentraba demasiada información, por lo que **se
parte en dos niveles según la dirección de la conversión**:

| Nivel | Título | Contenido | Ejemplo |
|---|---|---|---|
| N1 | **Bajar la escalera** | De unidad mayor a menor → **multiplicar** | `1,25 m → 125 cm` |
| N2 | **Subir la escalera** | De unidad menor a mayor → **dividir** | `450 cm → 4,5 m` |
| N3 | Operaciones con unidades mixtas | Convertir **antes** de operar; ambas direcciones | `1,2 m + 80 cm` |

**Justificación del corte por dirección:** el error clásico en conversiones no es la escalera
en sí, sino **multiplicar cuando había que dividir**. Separar por dirección aísla esa
confusión concreta. El N3 exige ambas direcciones y decidir cuál aplicar — integra los dos
anteriores.

Es la misma lógica estructural de los módulos 2 y 3: dos niveles que aíslan un caso cada
uno, y un tercero que los combina.

### C6.6 Estructura objetivo consolidada — 4 módulos × 3 niveles = 12 niveles

> ✅ **APROBADA por el usuario.** Esta es la estructura definitiva de la nueva Fase 4.
> El Módulo 1 se conserva sin cambios: su eje de progresión es la operación (suma → resta →
> combinadas), coherente con el patrón *aislar caso 1 → aislar caso 2 → integrar* que siguen
> los otros tres módulos.

| Módulo | Nivel | Título | Contenido | Ejemplo |
|---|---|---|---|---|
| **1** — Suma y Resta de Decimales<br>*magnitudes: dinero, masa, longitud, temperatura* | N1 | Suma alineando la coma | Alinear por la coma, mismo nº de decimales | `3,50 + 8,50` |
| | N2 | Resta con completado de ceros | Distinto nº de decimales; completar con ceros | `5,3 − 1,25` |
| | N3 | Combinadas en contexto | Suma y resta encadenadas en situación real | `20,00 − (3,50 + 8,50)` |
| **2** — Multiplicación de Decimales<br>*magnitudes: dinero, masa, longitud* | N1 | Un factor decimal · 1 cifra | Factor decimal × entero | `4,5 × 3` |
| | N2 | Un factor decimal · 2 cifras | Factor decimal × entero | `4,52 × 3` |
| | N3 | Ambos factores decimales | Contar cifras decimales de ambos | `45,2 × 2,52` |
| **3** — División con Decimales<br>*magnitudes: dinero, masa, longitud* | N1 | Dividendo decimal · 1 cifra | Dividendo decimal ÷ entero | `4,5 ÷ 3` |
| | N2 | Dividendo decimal · 2 cifras | Dividendo decimal ÷ entero | `4,52 ÷ 2` |
| | N3 | Divisor decimal | Desplazamiento de la coma en ambos | `45,2 ÷ 2,5` |
| **4** — Conversión de Unidades<br>*magnitud: solo longitud* | N1 | Bajar la escalera | Mayor → menor: multiplicar | `1,25 m → 125 cm` |
| | N2 | Subir la escalera | Menor → mayor: dividir | `450 cm → 4,5 m` |
| | N3 | Operaciones con unidades mixtas | Convertir antes de operar | `1,2 m + 80 cm` |

### C6.7 Contenido que sale de la Fase 4

| Sale | Destino |
|---|---|
| Escalera cúbica · dm³=L, cm³=mL · Capacidad en contexto | ➡️ Geometría Espacial y Volumen |
| **Superficie · m², cm², hectáreas** | ➡️ **Geometría Plana y Áreas** |
| Pulgadas y pies a cm | ❌ Descartar — fuera del alcance del examen |
| **Escalas de mapas y rutas por tramos** | ➡️ **Fase 5** (Fracciones, Porcentajes y **Proporciones**) — ver nota |

**Balance:** de 15 niveles a 12. Salen 3 de capacidad, 2 de superficie, 1 imperial y 1 de
escalas; entran 3 nuevos de división y se rehacen 2 de multiplicación.

> 📌 **Nota sobre «Escalas de mapas» (nivel 303 actual).** No es conversión de unidades sino
> **razonamiento proporcional** (*1 cm en el mapa = 5 km en la realidad*). Se traslada a la
> Fase 5, cuyo tema son precisamente las proporciones.
>
> **De momento solo queda anotado**, no planificado: la Fase 5 se analizará y mejorará
> después. El objetivo de esta nota es que el material ya esté identificado cuando toque
> planear esa fase, sin tener que redescubrirlo.

---

## C7 — Variedad real de preguntas y coherencia semántica

### C7.1 Problema detectado

Tres preguntas consecutivas del pool de desafíos, tal como se sirven hoy:

| | Salma | Sofía | Thiago |
|---|---|---|---|
| Escenario | carteles de la carretera | **distancia a la escuela** | **altura del edificio** |
| Datos | R$ 14,31 / R$ 6,02 | **R$** 20,40 / **R$** 8,56 | **R$** 11,76 / **R$** 4,97 |
| Pregunta | ¿Qué operación calcula el total acumulado? | *idéntica* | *idéntica* |
| Opciones | Multiplicar · Sumar · Sumar sin alinear · Restar | *idénticas* | *idénticas* |
| Respuesta correcta | Sumar | Sumar | Sumar |

**Dos fallos distintos, no uno.**

### C7.2 Fallo 1 — Cero variedad estructural

La respuesta correcta es «Sumar» en las tres. Un alumno que vea diez de estas aprende una
regla que **no es matemática**:

> *«En estas preguntas siempre hay que elegir la que dice Sumar.»*

Y acierta el 100 % **sin leer el enunciado**. Memoriza el tipo de respuesta en lugar de
construir el mecanismo lógico.

#### Causa técnica

En `_generate_practice_question` la estructura se ramifica **por nivel**, no por familia:

```python
if nivel_id == 1:   ...
elif nivel_id == 2: ...
else:               ...
```

Dentro de cada rama, `fam_idx` solo altera **valores numéricos**:

```python
m_val = round(1.10 + item_offset + rng.uniform(0.01, 0.05), 2)
```

→ **120 familias por nivel, numéricamente distintas pero estructuralmente idénticas.**

> 🔍 **La variación espejo sí está bien diseñada.** El Tomo 1 §4.3 pide que la variante
> espejo conserve *«la misma estructura gramatical y la misma secuencia de operaciones»* —
> correcto para un espejo. **El bug es que esa mismidad se filtró al nivel de familia:** lo
> que debía ser idéntico entre las 4 variantes de una familia acabó siendo idéntico entre
> las 120 familias.

#### Qué es variedad real

| Eje | Hoy | ¿Cambia el razonamiento? |
|---|---|---|
| Personaje (Salma / Sofía / Thiago) | ✅ varía | ❌ No |
| Objeto (carteles / distancia / altura) | ✅ varía | ❌ No |
| Números | ✅ varía | ❌ No |
| **Operación correcta** | ❌ siempre sumar | ✅ **Sí** |
| **Dónde está la incógnita** | ❌ siempre el total | ✅ **Sí** |
| **Formulación de la pregunta** | ❌ idéntica | ✅ **Sí** |
| **Nº de datos** | ❌ siempre 2 | ✅ **Sí** |
| **Rol del contexto** | ❌ decorativo | ✅ **Sí** |

Los tres ejes que hoy varían son precisamente los que **no** afectan al razonamiento.

#### Decisión ✅ — esquemas estructurales por nivel

En lugar de *1 plantilla × 120 familias*, se definen **mínimo 6 esquemas estructuralmente
distintos por nivel**; cada familia adopta uno.

Ejemplo para Módulo 1 · N1 (suma alineando la coma):

| # | Esquema | Incógnita | Operación correcta |
|---|---|---|---|
| 1 | `A + B = ?` | El total | Sumar |
| 2 | `A + ? = T` | **Una parte** | **Restar** |
| 3 | Sobrante: `T − (A + B) = ?` | El resto | Sumar y restar |
| 4 | Corregir un resultado errado: se da `X` mal calculado y se pide el correcto | El total real | Sumar |
| 5 | `A + B + C = ?` | Total con **3 datos** | Sumar |
| 6 | `A + B` con un dato irrelevante | Total, filtrando ruido | Sumar |

Con esto, *«la respuesta es Sumar»* deja de funcionar como atajo: en el esquema 2 hay que
**restar** aunque el contexto hable de juntar.

> ⚠️ **Corrección de auditoría.** Una versión anterior incluía los esquemas *«¿le alcanza?»*
> y *«¿es correcto?»*. Ambos son **formas TJS** y su respuesta natural es Sí/No, incompatible
> con el **input libre** que C4.3 fijó para la práctica libre. Se sustituyeron por variantes
> de **respuesta numérica** que conservan el mismo cambio de operación sin reintroducir la
> opción múltiple — y con ella el escape por azar del Bucle Espejo (C4.2).

**Límite de concentración:** ningún esquema puede superar el **25 % del pool** de un nivel.

#### Prueba de la plantilla (auditoría automatizable)

> Toma 5 preguntas al azar del pool. Si comparten el mismo esqueleto —misma formulación,
> mismo conjunto de opciones y misma operación correcta— **no hay variedad real**, por
> muchos nombres distintos que tengan.

### C7.3 Fallo 2 — Incoherencia semántica y de unidades

> *«Salma reúne montos en **la distancia a la escuela**»* — con valores en **R$**.

Se está midiendo una distancia en reales. El generador enchufa un generador de dinero en
escenarios arbitrarios. No es solo raro: **enseña que las unidades no importan.**

#### Decisión ✅ — reglas de coherencia

> **No se pueden sumar peras con manzanas.**

| # | Regla |
|---|---|
| **R1** | **Escenario → magnitud → unidad es una terna coherente**, elegida en conjunto. El generador nunca combina las tres de forma independiente |
| **R2** | **No se operan magnitudes distintas entre sí.** `R$ 14,31 + 6,02 m` está prohibido |
| **R3** | Unidades distintas de la **misma** magnitud solo se combinan donde el nivel **enseña esa conversión** (Módulo 4 · N3: `1,2 m + 80 cm`). Fuera de ahí, prohibido |
| **R4** | **Plausibilidad de escala:** la magnitud debe ser realista para el objeto. Un edificio no mide 4,5 cm; un lápiz no cuesta R$ 4.500 |

#### Ternas válidas para la Fase 4

| Magnitud | Unidad | Escenarios coherentes |
|---|---|---|
| Dinero | R$ | Compras, precios, vueltos, ahorros, presupuestos |
| Longitud | km, m, cm, mm | Distancias, alturas, cintas, cuerdas, telas |
| Masa | kg, g | Pesos, ingredientes, paquetes |
| Capacidad | L, mL | Bebidas, recipientes — **solo como contexto**, no como tema de conversión (ver C6.7) |

> ⚠️ En el **Módulo 4** (Conversión de Unidades) la magnitud queda restringida a **longitud**,
> conforme a C6.5. En los módulos 1–3 cualquier magnitud es válida como contexto, siempre que
> respete R1–R4.

### C7.4 Repercusiones

**Favorables**
- Elimina la memorización de patrón, que invalidaba silenciosamente la evaluación.
- La coherencia de unidades refuerza el «contexto portante» de C5.11: si la unidad importa,
  el contexto deja de ser decorativo.
- Ambas reglas son **auditables automáticamente** (concentración de esquemas, terna
  magnitud-unidad-escenario).

**Costos**
- Reescribir los generadores: de 1 plantilla por nivel a **≥ 6 esquemas** por nivel.
  Es el cambio de generación más profundo del documento.
- Requiere un **catálogo de escenarios por magnitud** que hoy no existe de forma explícita.

**Cascada documental**
- Tomo 4 §7 («Banco de escenarios reales») — incorporar las ternas coherentes y R1–R4.
- Tomo 1 §4.3 — aclarar que la mismidad estructural aplica **solo entre variantes espejo**,
  nunca entre familias.

---

### C7.5 Solución técnica — separar datos de código ✅

**Causa arquitectónica común a los tres bugs:** las plantillas viven como literales de
Python dentro del generador, mientras los escenarios viven en un catálogo JSON. El código
solo conoce el *nombre* del escenario, y el catálogo no sabe cómo se usará.

#### Bug 1 — El escenario debe declarar su papel gramatical

Hoy la plantilla impone la preposición: `f"{personaje} compra en {esc['nombre'].lower()}."`

**Solución:** el escenario deja de ser una cadena y pasa a tener **campos por función
gramatical**.

```json
{
  "id": "panaderia", "modulo_id": 1,
  "magnitud": "dinero", "unidad": "R$",
  "lugar": "la panadería",
  "objetos": ["pan", "leche", "bizcocho"],
  "sujeto_medible": "la cuenta"
}
```

| Marco de la plantilla | Campo usado | Resultado |
|---|---|---|
| `{personaje} compra en {lugar}` | `lugar` | *«Ana compra en la panadería»* ✅ |
| `{personaje} compra {objeto}` | `objetos` | *«Ana compra pan»* ✅ |
| `{sujeto_medible} suma…` | `sujeto_medible` | *«La cuenta suma…»* ✅ |

Para escenarios sin lugar (longitud, Módulo 4):

```json
{
  "id": "altura_edificio", "modulo_id": 4,
  "magnitud": "longitud", "unidad": "m",
  "objeto_medible": "el edificio", "atributo": "la altura"
}
```

→ *«Ana mide **la altura** del **edificio**»* ✅

**Regla:** una plantilla solo usa campos que declara necesitar (`campos_requeridos`), y el
generador **rechaza** un escenario que no los tenga.

#### Bug 2 — Magnitud como contrato verificado

Plantilla y escenario declaran su magnitud; el generador la verifica:

```python
if plantilla["magnitud"] != escenario["magnitud"]:
    raise ValueError(
        f"R2 violada: plantilla '{plantilla['id']}' es de {plantilla['magnitud']} "
        f"y el escenario '{escenario['id']}' es de {escenario['magnitud']}"
    )
```

1. La **unidad sale del escenario** (`R$`, `m`, `kg`), nunca del literal de la plantilla.
2. Un escenario de longitud **jamás** alimenta una plantilla de dinero: falla en la siembra,
   no en producción.
3. **R2 deja de ser recomendación y pasa a ser restricción ejecutable.**

#### Bug 3 — Las plantillas pasan a ser datos

Problema de fondo: hoy **añadir variedad exige tocar código Python**. Por eso hay tres
plantillas y nadie las amplió.

**Solución:** catálogo `plantillas_fase4.json`, hermano del de escenarios.

```json
{
  "id": "m1_n1_esq2_parte_faltante",
  "modulo_id": 1, "nivel_id": 1,
  "magnitud": "dinero",
  "campos_requeridos": ["lugar", "objetos"],
  "marco": "{personaje} necesita {meta} para {objeto} en {lugar}. Ya juntó {a}.",
  "pregunta": "¿Cuánto le falta?",
  "operacion_correcta": "restar",
  "incognita": "parte",
  "n_datos": 2
}
```

| | Antes | Ahora |
|---|---|---|
| Añadir un esquema | Editar Python y redesplegar | Añadir una entrada JSON |
| Verificar variedad | Leer código | Agrupar por `operacion_correcta` |
| Auditar R1–R4 | Imposible | Automático sobre el JSON |

La **prueba de la plantilla** (§C7.2) se vuelve trivial: agrupar el pool por `plantilla_id`
y comprobar que ninguna supere el 25 %.

#### El generador pasa a ser un compositor

```
1. Elegir esquema del catálogo (rotando, ≤25 % por esquema)
2. Filtrar escenarios: magnitud == esquema.magnitud
                       y que tengan los campos_requeridos
3. Componer el enunciado
4. Validar ANTES de sembrar:
     · desafíos: objetivo ≈30, límite duro 40 (§4.4) · práctica: ≈50
     · etiquetas de tabla ≤15 caracteres      ← C8.1
     · unidad coherente con la magnitud       ← R2
     · plausibilidad de escala                ← R4
5. Si falla cualquier validación → error, no se siembra
```

El generador deja de **inventar** enunciados y pasa a **componer y verificar**.

#### Alcance del trabajo (solo Fase 4)

| Tarea | Volumen |
|---|---|
| Reestructurar escenarios con campos gramaticales | ~80 (4 módulos × 20) |
| Escribir catálogo de esquemas | ≥6 por nivel × 12 niveles = **≥72** |
| Convertir el generador en compositor con validación | 1 refactor |

### C7.6 Reparto del catálogo de escenarios del Módulo 2

El Módulo 2 actual **mezcla multiplicación y división** (bug C6.2), y sus 20 escenarios
reflejan esa mezcla. Al separar en M2 (multiplicación) y M3 (división), **no hay que
escribir 40 escenarios desde cero**: los existentes ya se reparten entre ambos.

| ➡️ Nuevo **M2 — Multiplicación** | ➡️ Nuevo **M3 — División** |
|---|---|
| El precio por bala del quiosco | Repartir la cuenta del helado |
| Las copias de la tarea | La pizza dividida entre hermanos |
| Los lápices de colores | El premio de la rifa repartido |
| El paquete de chicles | El promedio de las notas |
| Las manzanas por peso | La cuenta del restaurante dividida |
| Los refrigerantes de la fiesta | El reparto de las propinas |
| El pan francés por kilo | Las cuotas del plan de salud |
| Las entradas del cine en familia | Las parcelas del videojuego |
| Los cuadernos del año escolar | |
| La carne por kilo del asado | |
| El precio unitario del mayorista | |
| La comisión del vendedor | |

**Balance:** ~12 escenarios para M2 y ~8 para M3. Solo hay que **completar** cada uno hasta
20, no crearlos de cero: ~8 nuevos para M2 y ~12 para M3, en lugar de 40.

### C7.7 Plan del catálogo de escenarios por módulo ✅

**Magnitudes admitidas por módulo:**

| Módulo | Magnitudes | Motivo |
|---|---|---|
| **1** — Suma y Resta | Dinero, masa, longitud, temperatura | Varias magnitudes **aumentan la variedad** (objetivo de C7). Si todo fuera dinero, el alumno aprendería la asociación falsa *«decimales = dinero»* |
| **2** — Multiplicación | Dinero, masa, longitud | Ídem |
| **3** — División | Dinero, masa, longitud | Ídem |
| **4** — Conversión | **Solo longitud** | Aquí la magnitud **es el tema** (C6.5) |

En todos los casos rigen R1–R4: la terna escenario → magnitud → unidad se elige en conjunto
y nunca se operan magnitudes distintas entre sí.

**Origen de los 80 escenarios (4 × 20):**

| Módulo objetivo | Origen | Trabajo |
|---|---|---|
| **1** — Suma y Resta | Módulo 1 actual (20) | ✅ Se conservan; añadir campos gramaticales |
| **2** — Multiplicación | ~12 del módulo 2 actual (los de multiplicar) | Completar ~8 |
| **3** — División | ~8 del módulo 2 actual (los de repartir) | Completar ~12 |
| **4** — Conversión | Módulo 3 actual, longitud (20) | ✅ Se conservan; añadir campos gramaticales |

**Escenarios que salen del catálogo de la Fase 4:**

| Origen | Escenarios | Destino |
|---|---|---|
| Módulo 4 actual (capacidad) | 20 | ➡️ Geometría Espacial y Volumen |
| Módulo 5 actual (superficie) | 20 | ➡️ Geometría Plana y Áreas |

**Balance:** de 100 escenarios actuales, **60 se conservan** (módulos 1, 2 y 3 actuales),
40 salen a otras fases, y hay que **escribir ~20 nuevos** para completar M2 y M3. No se
parte de cero en ningún módulo.

### C7.8 Nombres canónicos de módulo — fuente única ✅

**Problema:** las cabeceras de nivel muestran nombres distintos a las tarjetas
(*«MÓDULO 3: SISTEMA MÉTRICO»* frente a *«División con Decimales»*).

**Decisión:** nombres **genéricos según el contenido**, con una **única fuente de verdad**
usada por tarjeta y cabecera.

| Módulo | Nombre canónico | Subtítulo de tarjeta |
|---|---|---|
| 1 | **Suma y Resta** | Alineación de comas, décimas y centésimas |
| 2 | **Multiplicación** | Conteo de cifras decimales |
| 3 | **División** | Cocientes y desplazamiento de comas |
| 4 | **Unidades de Medida** | Escalera métrica: km, m, cm, mm |

#### 🔴 Verificación realizada — son dos fuentes de verdad, y una está mal

| Pantalla | Fuente | Archivo |
|---|---|---|
| **Tarjeta** del dashboard | `modulo.nombre` — **backend** | `WelcomeScreenPhase5.tsx:488` |
| **Cabecera** del nivel | `MODULE_NAMES` — **constante hardcodeada en frontend** | `Fase5TheoryModal.tsx:19` |

```typescript
const MODULE_NAMES: Record<number, string> = {
  1: 'Operaciones Decimales',      // real: Suma y Resta
  2: 'Unidades y Conversiones',    // real: Multiplicación y División  ❌
  3: 'Sistema Métrico',            // real: conversión lineal
  4: 'Resolución de Problemas',    // real: capacidad                  ❌
  5: 'Desafío Integrador',         // real: superficie                 ❌
};
```

**La constante no describe el contenido real.** Un alumno que hace multiplicación ve
*«MÓDULO 2: UNIDADES Y CONVERSIONES»*.

**Corrección:** eliminar `MODULE_NAMES` y leer el nombre del backend, como hace la tarjeta.
Fuente única.

### C7.9 Redistribución de las confusiones ✅

El catálogo tiene **60 confusiones**, 12 por cada uno de los **5 módulos actuales**.

| Confusiones de… | Destino |
|---|---|
| Módulo 1 viejo (suma/resta) — 12 | ✅ Módulo 1 nuevo |
| Módulo 2 viejo (mult. **y** división) — 12 | ✂️ Repartir entre M2 y M3 nuevos |
| Módulo 3 viejo (longitud) — 12 | ✅ Módulo 4 nuevo |
| Módulo 4 viejo (capacidad) — 12 | ➡️ Sale a Geometría 3D |
| Módulo 5 viejo (superficie) — 12 | ➡️ Sale a Geometría Plana |

**Balance (corregido tras auditoría):** **36 utilizables** (12 del M1 + 12 del M2 viejo +
12 del M3-longitud) para 4 módulos que necesitan **48** → **escribir 12 nuevas**, sobre todo
para División (desplazamiento de coma, resto decimal, cociente menor que 1).

| Módulo nuevo | Heredadas | A escribir |
|---|---|---|
| 1 — Suma y Resta | 12 | 0 |
| 2 — Multiplicación | ~6 (del M2 viejo) | ~6 |
| 3 — División | ~6 (del M2 viejo) | ~6 |
| 4 — Unidades de Medida | 12 (del M3 viejo) | 0 |
| **Total** | **36** | **12** |

### C7.10 Volumetría de la práctica libre — ajustada ✅

**Estado actual:** 120 familias × 4 variantes (1 original + 3 espejo) = **480 preguntas por
nivel**, de las que el alumno responde 15.

Con ≥6 esquemas (C7.2), 120 familias darían 20 por esquema — más de lo necesario.

**Ajuste decidido:**

| | Antes | Ahora |
|---|---|---|
| Esquemas por nivel | 1 | **≥ 6** |
| Familias por esquema | — | **12** |
| Familias por nivel | 120 | **72** |
| Variantes por familia | 4 | 4 *(sin cambio)* |
| **Preguntas por nivel** | **480** | **288** |
| El alumno responde | 15 | 15 |

**Sobreaprovisionamiento resultante:** 72 originales para 15 respondidas ≈ **4,8×** —
suficiente para evitar repetición entre reintentos.

**Efecto:** la siembra de práctica baja de 5.760 a **3.456 preguntas** en la fase, y a
cambio la variedad estructural pasa de 1 a ≥6 esquemas. Menos volumen, más variedad —
que es exactamente el objetivo de C7.

### C7.11 `NOMBRES_POOL` pasa al catálogo ✅

Los personajes salen hoy de `NOMBRES_POOL`, una constante de Python
(`seed.py:147` y `:573`). Por coherencia con el principio de C7 —*las plantillas son datos,
no código*— se traslada al catálogo JSON junto a escenarios, esquemas y confusiones.

## C8 — UX de las pantallas de pregunta

Detectado sobre una pantalla real del Desafío Mixto (respuesta numérica con teclado).

### C8.1 🔴 Bug de renderizado — colisión de texto en `tabla_datos`

En la tercera fila, la etiqueta *«Promoción no comprada»* **se superpone** con su valor
`R$ 12,60`, y la fila queda cortada por el borde inferior del contenedor.

**Causa** — `tabla_datos` usa columnas de ancho fijo:

```python
rh=22; cw=90   # alto de fila 22px, ancho de columna 90px
```

Con `cw=90` y fuente de 11 px caben ~15 caracteres. *«Promoción no comprada»* tiene **21**:
desborda y pisa la columna del valor. `th` se calcula por número de filas sin contemplar el
desbordamiento, de ahí el corte.

**Doble corrección:**

| Ámbito | Medida |
|---|---|
| **Generador** | `tabla_datos` debe medir la etiqueta y ajustar `cw`, o truncar con elipsis |
| **Contenido** | Límite duro de **≤ 15 caracteres** en etiquetas de tabla. *«Promoción no comprada»* → **«Promoción»** |

### C8.2 Layout aprobado ✅

```
┌──────────────────────────────┬─────────────────┐
│  Dante compra en la tienda.  │   ┌─────────┐   │
│                              │   │  22,74  │   │  ← visor grande
│  ┌────────────────────────┐  │   └─────────┘   │
│  │ Producto A    R$ 18,57 │  │   7   8   9     │
│  │ Producto B    R$  4,17 │  │   4   5   6     │
│  │ Promoción     R$ 12,60 │  │   1   2   3     │
│  └────────────────────────┘  │   ,   0   ⌫     │
│                              │                 │
│  ¿Cuánto paga por A y B?     │  [ Confirmar ]  │
└──────────────────────────────┴─────────────────┘
```

**Cambios respecto al estado actual:**

| # | Problema actual | Corrección |
|---|---|---|
| 1 | El campo de respuesta **parece un botón** (recuadro redondeado con `?`) y está en el panel **opuesto** al teclado: el alumno pulsa a la derecha y el número aparece a la izquierda | **Visor sobre el teclado**, mismo panel, cifra grande, aspecto de visor (sin borde de acción) |
| 2 | ~200 px muertos entre pregunta y campo, más un vacío a la derecha del teclado | Espacio reasignado a **ensanchar la tabla**, que es lo que hoy no se lee |
| 3 | Valores sin alinear | **Alineados por la coma** — refuerza el concepto de la propia fase |
| 4 | Orden de lectura difuso | **Contexto → datos → pregunta** |

### C8.3 El dato irrelevante se presenta sin distintivo visual ✅

*«Promoción»* es el dato irrelevante que C5.9 exige en el DF.

| Opción | Efecto |
|---|---|
| Distinguirlo (gris, cursiva) | El alumno lo descarta **sin leer** → anula el propósito |
| **Presentarlo idéntico** ✅ | Obliga a leer y decidir qué sirve |

Filtrar el ruido **es** la habilidad que el DF evalúa. La etiqueta debe ser legible y honesta;
que sea irrelevante se deduce **del enunciado**, no del formato.

### C8.4 Separador decimal — unificar a coma ✅

**Problema:** la tecla decimal muestra `.` mientras los importes del enunciado usan `,`.
Dos símbolos distintos para lo mismo, en la fase que enseña **precisamente qué es la coma
decimal**.

**Decisión: el teclado numérico muestra `,`**, igual que los enunciados.

| | Antes | Ahora |
|---|---|---|
| Tecla del separador | `.` | **`,`** |
| Enunciados y tablas | `,` | `,` |
| Visor de la respuesta | — | `,` |

**Entrada flexible sin cambios:** el Tomo 1 §4.4 exige que los inputs acepten **tanto `.`
como `,`** (regex `/^[0-9,.\-]*$/`). Esa validación **se conserva** — un alumno con teclado
físico puede seguir escribiendo punto. Lo que cambia es **lo que se muestra**, no lo que se
acepta.

⚠️ **Cascada documental:** el Tomo 1 §4.4 recomienda hoy lo contrario —
*«las teclas de separadores en los teclados numéricos virtuales deben mostrar de manera
unificada el punto (`.`) […] facilitando la familiarización con las notaciones numéricas
universales»*. Debe corregirse **para la Fase 4**: prima la coherencia con el enunciado
sobre la familiarización con la notación universal, porque el concepto que se está
enseñando es la coma decimal.

### C8.5 Incoherencia semántica del escenario

*«Dante compra en **la alfombra de la sala**»* — escenario sin sentido. Es el mismo fallo
registrado en **C7.3**: el generador combina personaje + lugar + magnitud de forma
independiente. Se corrige con las reglas R1–R4.

---

## C9 — Barrido del banco de preguntas y de MinIO

### C9.1 Necesidad

La reestructuración deja **contenido muerto** que ya no se usará en la nueva Fase 4:
preguntas de módulos consolidados o eliminados, teoría de niveles que desaparecen,
configuraciones huérfanas e imágenes que nadie referencia. Debe eliminarse, no acumularse.

### C9.2 🔑 Dependencia de orden — T1 desbloquea el borrado

El Tomo 4 §12.1 establece que las preguntas **nunca se borran**, solo se marcan
`estado = INACTIVO`, *«porque hay FK desde `intentos` y `alternativas`»*.

**Pero T1 (§4.6) borra el progreso de la Fase 4 en adelante — y con él los `intentos`.**
Al desaparecer esas referencias, el borrado real pasa a ser posible.

```
1. Resetear progreso (T1)        → desaparecen los intentos
2. Verificar que no quedan FK    → confirmar huérfanas
3. Barrido real del banco (C9)   → ahora sí se puede borrar
4. Sembrar el contenido nuevo
```

> ⚠️ **El orden no es negociable.** Intentar el barrido antes del reseteo choca contra las
> FK. Y sembrar antes de barrer mezcla contenido nuevo con residuo viejo.

### C9.3 Alcance del barrido

**Base de datos — solo Fase 4:**

| Tabla | Qué se elimina |
|---|---|
| `preguntas` | Preguntas de práctica y desafío de los módulos consolidados o eliminados |
| `alternativas` | Filas dependientes de esas preguntas |
| `niveles_teoria_pool` | Teoría de los niveles que desaparecen (capacidad, superficie, pulgadas, escalas) |
| `configuracion_progreso` | Filas de secciones inexistentes tras C6 (módulo 5 completo, secciones `5011–5013`, `501–503`) |
| `intentos` | Ya eliminados por T1 |

**Volumetría estimada del residuo:**

| Origen | Preguntas |
|---|---|
| 3 bloques de desafío que sobran (C6: de 16 a 13) | ~450 |
| Práctica de los niveles eliminados (capacidad, superficie…) | ~2.400 |
| Preguntas rehechas por C5 (D1 y DF re-sembrados) | ~1.200 |

**MinIO — prefijo `graphics/`:**

- Las fases 5–6 ya hacen *auto-skip* de MinIO por usar **SVG inline**
  (`fase5/seed.py`: *«Cero MinIO / PNG»*). Lo que quede allí de esta fase es **legado
  anterior a la migración a SVG**.
- Identificación de huérfanos: recorrer `datos_numericos.url` de las preguntas vivas y
  contrastar contra los objetos del bucket. Todo objeto de la Fase 4 **no referenciado** se
  elimina.
- ⚠️ Verificar que ninguna URL de otra fase apunte al mismo objeto antes de borrar.

### C9.4 Precauciones

| # | Precaución |
|---|---|
| 1 | **Solo Fase 4.** Ninguna otra fase se toca (§1.A) |
| 2 | **Copia de seguridad de BD y bucket antes de barrer.** El borrado real no es reversible, a diferencia del `INACTIVO` |
| 3 | Ejecutar primero en **local**, verificar, y solo después en VPS — conforme al procedimiento de `RULES AGENTES/bd_minio.md` |
| 4 | Modo **dry-run obligatorio** antes del borrado real: listar qué se eliminaría y cuánto |
| 5 | Verificar que **no queda ninguna FK** apuntando a las filas a borrar |

### C9.5 Repercusión sobre el Tomo 4

El §12.1 dice *«nunca borrar»* como regla absoluta. Debe matizarse:

> La prohibición de borrar aplica **mientras existan referencias desde `intentos` o
> `alternativas`**. Cuando el progreso de la fase se ha reseteado íntegramente y no quedan
> referencias, el barrido real es preferible al marcado `INACTIVO`: evita arrastrar
> residuo indefinidamente.

---

## 4. Temas transversales — se resuelven al final

Afectan a **todas** las fases que se reestructuren, no solo a C1. Se tratan una sola vez,
con criterio único, cuando se conozca el alcance total.

| # | Tema | Estado |
|---|---|---|
| T1 | **Progreso de los alumnos.** Se resetea desde la Fase 4 en adelante; se conserva hasta la Fase 3. Ver §4.6 | ✅ **Decidido** |
| T3 | **🚫 CERO SCROLL VERTICAL — regla innegociable de diseño.** Ningún contenido de la app puede requerir scroll vertical: teoría, explicaciones, enunciados de preguntas, diccionario de nivel. Todo debe caber en pantalla. Cuando el contenido no cabe, **se divide en varios pasos**, nunca se hace scrollable. Aplica a **toda la app**, en cualquier fase, módulo y nivel — no solo a lo que se reestructure. | **Decidido — regla permanente** |
| T4 | **📐 VENTANA DE TAMAÑO FIJO — regla innegociable de diseño.** El contenedor de los pasos con teoría y ejemplos debe tener **siempre las mismas dimensiones**, en todos los niveles, módulos y fases. No crece ni encoge según el contenido. Garantiza consistencia de UX: el alumno siempre encuentra los controles en el mismo sitio y no percibe saltos entre pasos. **Dimensiones fijadas: 950 × 620 px** (ver §4.2) | ✅ **Decidido con números** |
| T2 | **Nombres de carpetas y componentes.** Renombrado total para alinear carpeta ↔ archivo ↔ constante, incluida la deuda preexistente. Ver §4.7 | ✅ **Decidido — alcance A2** |

### 4.1 Consecuencia combinada de T3 + T4 — presupuesto de contenido

Ventana de tamaño fijo (T4) + prohibición de scroll (T3) implican que **cada paso tiene un
presupuesto máximo de contenido que no se puede exceder**. Esto convierte una regla de UI
en una **regla de redacción**:

- Todo texto de teoría, ejemplo, enunciado o diccionario debe **escribirse para caber**.
- Cuando un contenido excede el presupuesto, **no se reduce la letra ni se hace scroll**:
  se divide en un paso más.
- El presupuesto debe quedar **definido numéricamente** (caracteres o líneas por bloque,
  nº de tarjetas de diccionario por paso) para que sea verificable de forma automática.

### 4.2 Dispositivos soportados y dimensiones de la ventana ✅

**Dispositivos de uso confirmados:**

| Dispositivo | ¿Soportado? | Motivo |
|---|---|---|
| Computador de escritorio | ✅ Sí | — |
| Tablet (Samsung Tab S6 e iPad), **en horizontal** | ✅ Sí — **dispositivo mínimo** | Es la referencia de calibración |
| Tablet en vertical | ❌ No | Orientación bloqueada a horizontal |
| Móvil | ❌ **Excluido** | Espacio insuficiente para imágenes y texto |

**Cálculo del dispositivo más restrictivo** — iPad clásico, 1024 × 768 CSS en horizontal:

| Concepto | Valor |
|---|---|
| Viewport horizontal | 1024 × 768 |
| Barra del navegador | −80 px |
| **Alto útil** | **≈ 688 px** |

**Dimensiones fijadas de la ventana:**

$$\boxed{950 \times 620 \text{ px}}$$

> 📌 **Hallazgo:** bloquear la orientación **solo compra ancho, no alto**. El alto siempre
> lo determina la orientación horizontal, así que son 620 px en cualquier caso. Y como el
> scroll es un problema de **altura**, T3 es igual de exigente con o sin bloqueo. El bloqueo
> se adopta porque gana 230 px de ancho gratis.

> ⚠️ **El problema ya existe hoy.** La ventana de teoría actual mide ≈ 790 × 765 px:
> **desborda el alto disponible en ~145 px**. El scroll detectado no es un caso límite sino
> un fallo estructural, y en tablet es peor que en el desktop donde se observó.

### 4.3 Presupuesto de contenido por paso ✅

**Principio:** el contenido se escribe **para la tablet**, no la ventana se estira para el
contenido. En desktop la ventana sigue siendo 950 × 620 y queda centrada con márgenes.

> ⚠️ **Reducir para que quepa significa reducir la cantidad de información, nunca el tamaño
> de la letra.** Encoger la fuente rompería T4 (ventana igual, contenido no) y para un niño
> de 10 años la letra pequeña es peor que un paso extra.

**Reparto vertical de los 620 px:**

| Zona | Alto |
|---|---|
| Cabecera (módulo · nivel · título · contador) | ~90 px |
| **Área de contenido** | **~440 px** ← lo único negociable |
| Pie (Atrás / Siguiente) | ~90 px |

Con tipografía de 18 px e interlineado 1,6 → ~29 px por línea → **≈15 líneas máximas**,
a ~85 caracteres por línea sobre 950 px de ancho:

$$440 \div 29 \approx 15 \text{ líneas} \times 85 \approx 1.275 \text{ caracteres absolutos}$$

El máximo teórico no es el objetivo: un bloque lleno hasta el borde agobia. Presupuestos
con holgura:

| Tipo de paso | Presupuesto | Equivale a |
|---|---|---|
| Texto narrativo puro | **≤ 800 caracteres** | ~9 líneas |
| Texto + SVG (figura ~200 px) | **≤ 400 caracteres** | ~5 líneas + figura |
| Reglas numeradas | **máx. 4 reglas** de ≤ 120 car. | — |
| Diccionario | **4 tarjetas** (2 × 2) | ~240 px |
| Pregunta con opciones | Enunciado ≤ 250 car. + 4 opciones ≤ 60 car. c/u | — |
| Desafío (D1 / D2 / DF) | Enunciado **≤ 30 palabras** + SVG ≤ 140 px + 4 opciones | ver §4.4 |

**Todos los límites son contables → validador automático en la siembra.** Es lo que impide
que T3 se degrade con el tiempo.

**Contraste con el estado actual:** el paso de teoría del Módulo 1 · Nivel 1 tiene ~1.100
caracteres de narrativa + 4 reglas + 6 tarjetas de diccionario. Con este presupuesto se
divide en **4 pasos**, no en 1.

### 4.4 Excepción: en los desafíos NO se puede dividir en pasos ✅

T3 resuelve el desbordamiento dividiendo en pasos. **En la zona de desafíos esa salida no
está disponible:** bajo cronómetro el alumno necesita ver **enunciado y opciones a la vez**
para decidir. Separarlos le obligaría a memorizar los datos mientras corre el reloj — eso
deja de evaluar decimales y pasa a evaluar memoria.

**El desbordamiento medido:**

| Elemento | Alto estimado |
|---|---|
| Enunciado (50 palabras, techo del Tomo 4) | ~120 px |
| SVG con los datos | ~200 px |
| 4 opciones | ~180 px |
| **Total** | **~500 px** |
| Disponible | **440 px** |
| **Déficit** | **≈ 60 px** (sin contar HUD de errores ni botón de pista) |

**Decisión: recortar el contenido, no la fiabilidad de la evaluación.**

| Medida | Antes | Ahora | Libera |
|---|---|---|---|
| **A** — Techo del enunciado en desafíos | 50 palabras | **30 palabras** | ~50 px |
| **B** — Alto máximo del SVG en desafíos | 200 px | **140 px** | ~60 px |
| ~~C~~ — Reducir a 3 opciones | — | ❌ **Descartada** | — |

Se descarta la opción C porque subiría la probabilidad de acierto por azar del 25 % al 33 %,
y la fiabilidad de la evaluación es lo único que no conviene tocar en la zona de desafíos.

#### El techo es flexible, no rígido ✅

**≈30 palabras es el objetivo, no un corte seco.** Lo que no es negociable es T3 (cero
scroll); las palabras son el medio, no el fin.

| Umbral | Valor | Tratamiento |
|---|---|---|
| **Objetivo** | ≈ 30 palabras | Lo que debe buscar el redactor |
| **Tolerancia** | hasta 35 | Aceptable si el enunciado lo necesita |
| **Límite duro** | **40 palabras** | El validador rechaza por encima |
| **Prueba real** | *cabe en 950 × 620 sin scroll* | Manda sobre cualquier cifra |

Si un enunciado de 34 palabras cabe con su SVG y sus opciones, es válido. Si uno de 28 no
cabe, hay que acortarlo. **La pantalla decide; el número orienta.**

> ⚠️ **Valor único vigente.** Esta sección deroga cualquier mención anterior a un techo de
> 50 palabras (C5.6, C5.9). El validador del paso 4.5 usa **estos** números.

> 📌 **Efecto secundario favorable:** enunciados más cortos son más fáciles de leer para un
> niño bajo presión de tiempo. El techo de 50 palabras del Tomo 4 nunca se calibró contra
> una pantalla real.

⚠️ **Cascada documental:** el Tomo 4 §8 («cinco reglas duras» de redacción) debe bajar su
techo de 50 a 30 palabras **para los desafíos**.

### 4.5 Contadores de progreso por bloque ✅

El contador único (`PASO 7 DE 10`) queda **sustituido por contadores independientes por
bloque** dentro del nivel.

**Motivo:** al dividir la teoría por presupuesto (§4.3) y adoptar el ejemplo guiado de 5
pasos (C2), el total por nivel pasa de ~10 a ~15 pasos. Un contador único que arranca en
«PASO 1 DE 15» desmotiva.

| Bloque | Pasos hoy | Tras la reestructuración | Contador |
|---|---|---|---|
| Teoría | 1 (con scroll) | ~4 | *Teoría 1 de 4* |
| Ejemplos guiados de cálculo | 3 | 3 | *Ejemplo 1 de 3* |
| Ejemplo guiado TJS | 2 (pasivos) | 5 (formato C2) | *Ejemplo 1 de 5* |
| Interactivos de evocación | 3 | 3 | *Tu turno 1 de 3* |
| **Total** | ~10 | **~15** | — |

**Doble beneficio:** el alumno percibe tramos cortos en lugar de una cuesta larga, y cada
etiqueta **comunica qué está haciendo** en ese momento.

---

### 4.6 T1 — Progreso de los alumnos ✅

**Decisión: se borra el progreso de los alumnos en esta fase.** El alumno tendrá que hacer
la Fase 4 obligatoriamente.

**Justificación — el progreso antiguo apunta a un mundo que ya no existe:**

| Decisión | Efecto sobre el progreso registrado |
|---|---|
| Renumerar `fase_id` 4 ↔ 5 (C1) | Apunta a otra fase |
| Consolidar 5 módulos en 4 (C6) | Los módulos 4 y 5 antiguos desaparecen |
| Módulo 3 nuevo — División (C6) | No existía; nadie tiene progreso ahí |
| Rehacer M2 · N2 y N3 (C6) | Apunta a niveles con otro contenido |
| Sacar capacidad y superficie (C6) | 5 niveles dejan de existir en esta fase |
| Re-sembrar D1 y DF (C5) | Las preguntas respondidas quedan inactivas |

De 15 niveles **sobreviven reconocibles unos 5**, y los desafíos se rehacen casi por
completo. Arrastrar el progreso con precisión sería trabajo caro para conservar un dato que
en su mayoría ya no significa nada.

**Argumento pedagógico adicional:** un alumno que ya cursó decimales lo hizo **después** de
fracciones. Con el orden nuevo, volver a pasar por la fase en su posición correcta no es un
castigo — es exactamente la secuencia que la reestructuración busca darle.

#### Alcance del reseteo ✅ — corte en la Fase 3

> **Se resetea todo el progreso desde la Fase 4 en adelante.**
> El progreso máximo que un alumno puede conservar es **hasta la Fase 3 completa**.

| Fases | Progreso | Motivo |
|---|---|---|
| **0, 1, 2, 3** | ✅ **Se conserva** | Operan bajo **Modelo A**, están **congeladas** y su contenido no se toca. Su progreso sigue siendo válido y significativo |
| **4 a 11** | ❌ **Se resetea** | Ver justificación abajo |

**Por qué el corte no puede ser solo la Fase 4:**

La renumeración **corrompe también el significado del progreso de la Fase 5**. Un alumno que
aprobó Fracciones tiene registrado *«fase_id 4 aprobada»*; tras el intercambio, `fase_id 4`
**es Decimales**. Su registro afirmaría que aprobó una fase que nunca cursó.

Resetear solo la Fase 4 dejaría esa contradicción viva. El corte en la Fase 3 la elimina de
raíz.

> 📌 **Matiz respecto al principio de gobierno (§1.A).** Esta decisión afecta al
> **progreso** de las fases 5–11, no a su **contenido**. Las demás fases siguen intactas en
> teoría, preguntas, niveles y desafíos: lo único que se borra es el registro de avance del
> alumno, precisamente porque la renumeración lo vuelve ambiguo.

### 4.7 T2 — Renombrado total de carpetas, componentes y constantes ✅

**Decisión: alcance A2 — renombrar todo**, incluida la deuda preexistente. Mantiene el
repositorio limpio, corrige errores antiguos y deja la app coherente de extremo a extremo.

> 📌 **Única excepción autorizada al principio de gobierno (§1.A).** Se justifica porque
> es **higiene de nomenclatura, no cambio de contenido**: renombrar archivos en las fases
> 8, 9 y 11 no altera su teoría, preguntas, niveles ni evaluación.

#### Parte 1 — Intercambio Fase 4 ↔ Fase 5

Como `fase4` y `fase5` **ya existen ambas**, hay colisión: se requiere nombre temporal,
igual que con los `id` de la BD (§C1.5).

```
1. fase4 (Fracciones)  →  fase_tmp
2. fase5 (Decimales)   →  fase4
3. fase_tmp            →  fase5
```

| Ámbito | Elementos a cambiar |
|---|---|
| **Backend** | `app/fase5/` ↔ `app/fase4/`; imports `from app.fase5 …` en `main.py`, routers y scripts; constante `FASE5_ID` → `FASE4_ID`; prefijos de ruta del router |
| **Frontend** | `components/fase5/` ↔ `components/fase4/`; los 6 archivos `Fase5*.tsx/.ts`; `WelcomeScreenPhase5.tsx`; imports en `App.tsx` y `PlayRouteWrapper.tsx`; llamadas al API |
| **CSS** ⚠️ | `Fase5Styles.css` (60 KB) y el prefijo de clases `f5-*` → `f4-*` |

⚠️ **El CSS es el punto más delicado.** El prefijo `f5-` aparece en cientos de clases
(`f5-step-indicator`, `f5-ex-step`, `f5-question-card`…). CSS y TSX deben actualizarse
**a la vez y sin desfase**: si uno cambia y el otro no, la fase queda sin estilos.
Además el Tomo 1 §4.5 documenta clases por nombre (`.f2-question-card`, `.f2-submit-btn`),
por lo que hay cascada documental.

#### Parte 2 — Deuda preexistente (inventario verificado)

**Frontend — 25 archivos con nombre incorrecto:**

| Carpeta | Archivos que contiene | Desfase |
|---|---|---|
| `fase8/` | `Fase7GameScreen.tsx`, `Fase7Service.ts`, `Fase7Styles.css`, `Fase7Types.ts`, `Fase7TheoryModal.tsx`, `Fase7MirrorModal.tsx`, `Fase7InteractiveCoordinatePlane.tsx`, `Fase7SplitVisualizer.tsx`, `WelcomeScreenPhase7.tsx` | **−1** |
| `fase9/` | `Fase8GameScreen.tsx`, `Fase8Service.ts`, `Fase8Styles.css`, `Fase8Types.ts`, `Fase8TheoryModal.tsx`, `Fase8MirrorModal.tsx`, `Fase8FabricHistogram.tsx`, `WelcomeScreenPhase8.tsx` | **−1** |
| `fase11/` | `Fase9GameScreen.tsx`, `Fase9Service.ts`, `Fase9Styles.css`, `Fase9Types.ts`, `Fase9TheoryModal.tsx`, `Fase9MirrorModal.tsx`, `Fase9ResultsScreen.tsx`, `WelcomeScreenPhase9.tsx` | **−2** |

**Backend:**

| Carpeta | Constante que usa | Desfase |
|---|---|---|
| `app/fase9/` | `FASE8_ID` | −1 |
| `app/fase11/` | `FASE9_ID` | −2 |

> 🔍 **Diagnóstico:** el desfase de **−2** en la Fase 11 indica que hubo **dos inserciones
> de fase** en el pasado y el renombrado nunca se completó. Es deuda acumulada, no un
> descuido puntual — razón adicional para saldarla ahora y no arrastrarla a una tercera
> renumeración.

Cada carpeta arrastra además su propio prefijo CSS (`f7-`, `f8-`, `f9-`), con la misma
exigencia de sincronía CSS ↔ TSX.

### 4.8 🔴 Prefijos CSS — cada fase debe tener el suyo ✅

**Hallazgo de auditoría:** la Fase 6 **reutiliza el prefijo `f5-`** de forma masiva.

| Archivo | Usos de `f5-` |
|---|---|
| `fase6/Fase6Styles.css` | **445** |
| `fase6/Fase6GameScreen.tsx` | 133 |
| `fase6/WelcomeScreenPhase6.tsx` | 64 |
| `fase6/Fase6TheoryModal.tsx` | 50 |
| `fase6/Fase6MirrorModal.tsx` | 12 |

Renombrar `f5-` → `f4-` sin más **dejaría la Fase 6 sin estilos**. Contradice la
justificación de §4.7 y el principio de gobierno §1.A.

#### Decisión ✅ — cada fase con su propio prefijo

> **Cada fase mantiene el prefijo de su número.** No se comparten prefijos entre fases:
> es lo que produjo este acoplamiento.

| Fase | Prefijo objetivo |
|---|---|
| Decimales (nueva Fase 4) | `f4-` |
| Fracciones (nueva Fase 5) | `f5-` |
| **Geometría Plana (Fase 6)** | **`f6-`** ← hoy usa `f5-` incorrectamente |

#### Procedimiento — prefijos temporales

Igual que con los `id` y las carpetas, hay **colisión**: `f4-` y `f5-` ya existen. Se resuelve
en tres pasos con prefijo temporal, y **CSS y TSX se cambian siempre en el mismo commit**.

```
Paso 1 · Desacoplar la Fase 6  (independiente, sin colisión)
   fase6:  f5-  →  f6-        (445 CSS + 259 TSX)
   ✅ Verificar que la Fase 6 renderiza con estilos antes de seguir

Paso 2 · Liberar f4-
   fase4 (Fracciones):  f4-  →  ftmp4-

Paso 3 · Ocupar f4-
   fase5 (Decimales):   f5-  →  f4-

Paso 4 · Cerrar el ciclo
   ftmp4-  →  f5-
```

| Regla | Motivo |
|---|---|
| El **paso 1 va primero y se verifica solo** | Es el único que corrige deuda ajena al intercambio; si falla, no arrastra al resto |
| **CSS y TSX en el mismo commit**, siempre | Un desfase deja la fase sin estilos |
| **Verificar visualmente tras cada paso** | Un prefijo huérfano no produce error: produce una pantalla sin estilo |
| Buscar `f5-` en **todo** el frontend antes de empezar | Puede haber más acoplamientos no inventariados |

> 📌 **Excepción al principio de gobierno.** El paso 1 modifica archivos de la Fase 6. Se
> autoriza porque **es requisito técnico ineludible** para renombrar la Fase 4 sin romperla,
> y porque corrige una deuda que ya existía. No altera contenido pedagógico.

## 5. Acciones de cierre — reestructuración documental

A ejecutar **al terminar la fase de planeación**, no antes.
**Alcance: solo lo que afecte a la Fase 4** (ver §1.A — principio de gobierno).

### A0 · 🔴 Derogaciones normativas explícitas *(añadido tras auditoría)*

La auditoría encontró **cuatro normas vigentes** que el plan contradice sin declararlo. Se
autorizan las derogaciones — *el análisis reestructura el conjunto, y los Tomos se actualizan
en consecuencia* — pero deben quedar **escritas**, o un implementador que siga los Tomos
revertirá las decisiones.

| # | Norma vigente | Dónde | Decisión que la deroga | Justificación |
|---|---|---|---|---|
| 1 | *«por lo menos **5 ejemplos guiados**… en todas las fases»* | Tomo 1 §3.1, línea 111 | **C2.4 → 4 ejemplos** | El TJS nuevo ocupa 5 pasos, no 1: el bloque **crece** en pantalla aunque baje de 5 a 4 ejemplos. La norma contaba ejemplos, no carga |
| 2 | *«Pool de práctica libre con **exactamente 120 familias** por nivel»* | Tomo 1 §11, línea 524 · Tomo 4 §14 | **C7.10 → 72 familias** | 120 familias de **un solo esquema** dan menos variedad real que 72 repartidas en ≥6 esquemas. La norma medía volumen, no variedad |
| 3 | *«Los datos numéricos **NUNCA en prosa**»* | Tomo 4 §8.1 regla 2 · §11 | **C5.5 → en el D1 van en prosa** | El D1 evalúa **extraer el dato del texto**. La norma protege contra la carga ajena al concepto; en el D1 esa carga **es** el concepto |
| 4 | *«Bajo ninguna circunstancia se deben modificar o **re-numerar** los `fase_id`… **en producción**»* | `MAPA_CANONICO_FASES.md`, regla 1 | **C1 → renumeración 4 ↔ 5** | La norma acota a **producción**; el trabajo es **solo local** (§6). Al promover habrá que derogarla formalmente o migrar de otro modo |

**Acción:** cada Tomo afectado recibe una nota de derogación con su justificación, no un
borrado silencioso de la regla anterior.

> 📌 **Hallazgo colateral.** `MAPA_CANONICO_FASES.md` **ya está desalineado con el código
> hoy**, antes de tocar nada: sus nombres de fase no coinciden con `app/seed.py` en la
> mayoría de las filas. Es la *«fuente de verdad contradictoria»* que A7 advierte, y conviene
> resolverlo al ejecutar A1.

### A1 · `docs/MAPA_CANONICO_FASES.md`

| Qué cambia | Origen |
|---|---|
| Intercambio del orden Fase 4 ↔ Fase 5 | C1 |

| 🔴 **Derogar la regla 1** («bajo ninguna circunstancia re-numerar `fase_id`») o acotarla explícitamente a producción (A0 #4) | C1 |
| Realinear los nombres de fase con `app/seed.py` — hoy discrepan en la mayoría de las filas | Hallazgo de auditoría |

⚠️ **Debe actualizarse junto con la renumeración de la BD, no al final.** Es el documento
«canónico» del orden: si queda desfasado, alguien lo consultará y actuará según él mientras
contradice a la base de datos.

### A2 · `docs/Criterios Diseno Fase/3_Guia_Frontend_UX.md`

| Qué añadir | Origen |
|---|---|
| **T3 — cero scroll vertical** (regla innegociable) | T3 |
| **T4 — ventana fija de 950 × 620 px** | T4, §4.2 |
| Dispositivos soportados: desktop + tablet horizontal; **móvil excluido** | §4.2 |
| **Presupuesto de contenido por paso** (tabla de límites contables) | §4.3 |
| Regla: reducir **cantidad de información**, nunca el tamaño de la letra | §4.3 |
| **Contadores por bloque** en lugar de contador único | §4.5 |
| Tipo de paso nuevo: opciones con revelación posterior | C2.4bis |

### A3 · `docs/Criterios Diseno Fase/4_Guia_TJS_Desafios.md` — el más afectado

| § | Qué cambia | Origen |
|---|---|---|
| §2.3 | **Deja de descalificar el problema de contexto** — pasa a ser formato legítimo | C5.2 |
| §3 | Las cinco formas TJS aplican **solo al D2** | C5.3 |
| §4 | El escalón se redefine por **formato**, no por número de pasos | C5.3 |
| §4 | Aclarar que **pool heterogéneo ≠ rampa**: la prohibición apunta al *orden*, no a la *variedad* | C5.12 |
| §8 | Techo del enunciado en desafíos: **de 50 a 30 palabras** | §4.4 |
| §8 | Alto máximo del SVG en desafíos: **140 px** | §4.4 |
| §10.2 | Tabla del puente: fuera «N3 → TJS ligero»; ejemplos guiados de 5 a **4**, con 1 TJS | C4, C2.4 |
| §10.3 | **Eliminar** «Reglas del N3 (TJS ligero)» | C4.3 |
| §10.4 | Reescribir: el ejemplo guiado deja de ser «TJS resuelto» → **TJS guiado con compromiso** (5 pasos) | C2.2 |
| §11 | Contrato del ítem: `errores_previstos` debe cubrir el **error de convención** (respuesta aritmética sin ajuste) | C5.13 |
| §12 | Tabla de conformidad: recalcular qué significa «conforme» bajo el nuevo paradigma | C5.7 |
| §14 | Volumetría: **13 bloques** (4 módulos × 3 + 1 DM), no 16 | C6 |
| **§14** | 🔴 **Derogar** «120 familias / 480 preguntas por nivel» → **72 / 288** (A0 #2) | C7.10 |
| **§8.1 regla 2** | 🔴 **Derogar** «datos numéricos NUNCA en prosa» **solo para el D1** (A0 #3) | C5.5 |
| §8.1 regla 1 | Techo de palabras: **≈30 objetivo, 40 duro**, con la prueba de pantalla por encima del número | §4.4 |
| §15 | Codificación de `seccion`: verificar tras la renumeración | C1 |
| — | **Sección nueva:** anatomía de los 5 pasos del ejemplo guiado TJS | C2.2 |
| — | **Sección nueva:** calibración de carga D1/D2/DF (seis parámetros) | C5.9 |
| — | **Sección nueva:** prueba del contexto portante y sus tres mecanismos | C5.11 |

### A4 · `docs/Criterios Diseno Fase/1_Documento_Rector_Pedagogico.md`

| § | Qué cambia | Origen |
|---|---|---|
| §4.1 | La prohibición de opción múltiple en práctica libre queda **vigente sin excepciones** (desaparece el conflicto con el Tomo 4) | C4.3 |
| §4.2–4.3 | El Bucle Espejo **no cambia**: recupera su supuesto de diseño (input libre) — dejar constancia | C4.4 |
| §11 | Checklist de creación de fases: incorporar T3, T4 y presupuestos | T3, T4 |
| **§3.1** | 🔴 **Derogar** el mínimo de 5 ejemplos guiados → **4** para la Fase 4 (A0 #1) | C2.4 |
| **§11** | 🔴 **Derogar** «exactamente 120 familias por nivel» → **72** para la Fase 4 (A0 #2) | C7.10 |

### A5 · `docs/Criterios Diseno Fase/guia_creacion_fase.md`

| Qué añadir | Origen |
|---|---|
| Estructura canónica: 4 módulos × 3 niveles, patrón *aislar → aislar → integrar* | C6.6 |
| T3, T4 y presupuesto de contenido como requisitos de creación | §4.3 |
| Regla: **no se evalúa una convención que no se enseñó** (las tres capas) | C5.13 |

### A6 · `docs/Criterios Diseno Fase/2_Arquitectura_Backend_y_Admin.md`

| Qué añadir | Origen |
|---|---|
| Tipo de dato `ejemplos_tjs` en la estructura de lectura | C2.4bis |
| Validador automático de presupuesto de contenido en la siembra | §4.3 |
| 🔴 **Derogar** el contrato de `ejemplo_guiado` que exige **mínimo 5** → **4** (A0 #1) | C2.4 |
| Renombrar la constante `FASE5_ID` → `FASE_DECIMALES_ID` y documentar su valor | Etapa 3, paso 3.5 |

### A7 · Higiene documental

| Acción | Detalle |
|---|---|
| `docs/reestructuraciondefases.md` (844 KB) | El propio Tomo 4 lo declara **caducable** (*"el plan de ejecución temporal caduca; este Tomo no"*). Decidir si sigue vigente o se mueve a `docs/historico/` |
| Ubicación de **este** documento | ✅ **Se queda en la raíz del proyecto** (`reestructuracion.md`) |

> ⚠️ Ya existen **tres** documentos con nombre parecido sobre reestructuración de fases.
> Es exactamente la situación que genera fuentes de verdad contradictorias.

---

## 6. Orden de ejecución

Secuencia ordenada por **dependencias reales**: si un paso requiere otro, el requerido va
antes. No es un orden de preferencia — romperlo rompe la reestructuración.

### ⚠️ Entorno: TODO EN LOCAL ✅

> **Ningún paso de esta secuencia toca el VPS ni producción.**
> Todos los cambios, pruebas y manipulaciones de base de datos se ejecutan **solo en local**.

Los scripts de sincronización (`sync_db_and_minio_prod.py`, `sync_minio_vps.py`) quedan
**fuera de alcance**. La promoción a otros entornos se planeará por separado, cuando la
Fase 4 esté validada (§1.A).

### 🚨 Riesgo detectado al construir la secuencia

**El contenido que migra a otras fases debe reubicarse ANTES del barrido.**

C6.7 envía a otras fases la capacidad (→ Geometría 3D), la superficie (→ Geometría Plana) y
«Escalas de mapas» (→ Fase 5). C9 borra de la Fase 4 todo lo que sobra. **Si C9 se ejecuta
primero, ese contenido se destruye en lugar de migrar.**

Son ~2.400 preguntas de práctica, 5 niveles de teoría, 40 escenarios y 24 confusiones que
habría que reescribir desde cero cuando toque planear esas fases.

#### Solución: módulo aparcado en la fase destino ✅

El contenido **no se exporta a un archivo: se reubica dentro de la fase destino** como un
**módulo nuevo, desordenado y aparcado**, pendiente de análisis futuro.

| Contenido | Fase destino |
|---|---|
| Capacidad y volumen (dm³, L, mL) | Geometría Espacial y Volumen |
| Superficie (m², cm², hectáreas) | Geometría Plana y Áreas |
| Escalas de mapas y rutas | Fase 5 (Proporciones) |

**Reglas de la reubicación:**

| # | Regla |
|---|---|
| 1 | Se cambia `fase_id` al de la fase destino; el contenido **no se borra** |
| 2 | Recibe un **`modulo_id` reservado alto** (≥ 90) para no colisionar con los módulos reales de esa fase |
| 3 | Se marca **inactivo**: el alumno no lo ve ni se le desbloquea |
| 4 | No se reorganiza ni se revisa ahora — queda **aparcado tal cual** hasta que se planee esa fase |

> ✅ **Ventaja sobre exportar a JSON:** el contenido sigue vivo en la base de datos con sus
> relaciones intactas (alternativas, teoría, escenarios). Cuando toque planear Geometría, el
> material está donde debe estar, solo hay que ordenarlo.

> 📌 **Sobre el principio de gobierno (§1.A):** esto añade un módulo inactivo a otras
> fases, pero **no modifica su contenido activo**. Es depósito, no reestructuración.

---

### Etapa 0 — Preparación y respaldo

| # | Paso | Depende de | Motivo |
|---|---|---|---|
| 0.1 | **Copia de seguridad de BD y bucket MinIO local** | — | El borrado de C9 no es reversible |
| 0.2 | **Reubicar capacidad → `fase_id 7` y superficie → `fase_id 6`** como **módulo aparcado inactivo**, `modulo_id ≥ 90`. **«Escalas de mapas» NO se toca aquí** — va en el paso 3.9 | 0.1 | 🚨 Ver riesgo arriba. Sus fases destino no participan del intercambio, por eso pueden reubicarse ya |
| 0.3 | **Verificar la copia de seguridad**: restaurarla en una BD desechable y comprobar que la app arranca | 0.1 | Una copia sin verificar no es una copia |

### Etapa 1 — Catálogos y generador *(sin tocar producción)*

| # | Paso | Depende de | Motivo |
|---|---|---|---|
| 1.1 | **Corregir el bug de `tabla_datos`** (C8.1) | — | Todo lo que se siembre después usa ese generador; corregirlo antes evita multiplicar el bug |
| 1.2 | Reestructurar el **catálogo de escenarios** con campos gramaticales (C7.5, C7.7) | — | Base del compositor |
| 1.3 | Escribir el **catálogo de esquemas** ≥6 por nivel (C7.5) | 1.2 | Los esquemas declaran `campos_requeridos` del escenario |
| 1.4 | **Redistribuir confusiones** y escribir las ~18 que faltan (C7.9) | — | |
| 1.5 | Mover **`NOMBRES_POOL`** al catálogo (C7.11) | — | Coherencia |
| 1.6 | **Refactor del generador a compositor con validación** (C7.5) | 1.1–1.5 | Consume todos los catálogos anteriores |
| 1.7 | Unificar la **fuente de los nombres de módulo** (C7.8) | — | Antes de renombrar nada |

### Etapa 2 — Frontend *(paralelizable con la Etapa 1)*

| # | Paso | Depende de | Motivo |
|---|---|---|---|
| 2.1 | **Ventana fija 950 × 620** (T4) | — | Base de T3 |
| 2.2 | **Layout de pregunta**: visor sobre el teclado, tabla ensanchada, orden contexto→datos→pregunta (C8.2) | 2.1 | |
| 2.3 | **Separador decimal a coma** (C8.4) | 2.2 | |
| 2.4 | **Paso con elección** en el carrusel (C2.4bis) | 2.1 | Requisito de C2 |
| 2.5 | **Contadores por bloque** (§4.5) | 2.4 | El array de slides se reagrupa |

### 🚨 Convención obligatoria de nomenclatura

> **Prohibido escribir «Fase 4» a secas en esta sección.**
> El intercambio de `id` ocurre **dentro** del plan: antes de él `fase_id 4` es **Fracciones**
> y los Decimales están en `fase_id 5`. Un paso que diga «barrer la Fase 4» ejecutado antes
> del intercambio **borra Fracciones**.

Nomenclatura obligatoria en todo paso de §6:

| Escribir | Significa |
|---|---|
| `fase_id 5 (Decimales, PRE-swap)` | Antes del intercambio |
| `fase_id 4 (Decimales, POST-swap)` | Después del intercambio |
| `fase_id 4 (Fracciones, PRE-swap)` | Antes del intercambio |
| `fase_id 5 (Fracciones, POST-swap)` | Después del intercambio |

### Etapa 3 — Datos *(orden crítico, no alterable)*

> ⚠️ **La renumeración va PRIMERO.** Así todo lo posterior opera sobre
> `fase_id 4 = Decimales` sin ambigüedad. (Corrige el fallo crítico detectado en auditoría:
> con la renumeración al final, los pasos de reseteo y barrido actuaban sobre Fracciones.)

| # | Paso | Depende de | Motivo |
|---|---|---|---|
| 3.0 | **Verificaciones previas de §C1.6** — en especial: ¿las FK tienen `ON UPDATE CASCADE`? + inventario completo de tablas con `fase_id` | 0.2 | 🔑 Si no hay CASCADE, el paso 3.2 falla o deja huérfanos |
| 3.1 | **Congelar el acceso de alumnos a la app local** | — | Evita escrituras concurrentes durante una renumeración de clave primaria |
| 3.2 | **Renumeración de `id` 4 ↔ 5** vía id temporal (904), **una sola transacción** (C1, §C1.5) | 3.0, 3.1 | **Va primero**: elimina toda ambigüedad posterior |
| 3.3 | **Actualizar `MAPA_CANONICO_FASES.md`** (A1) | 3.2 | ⚠️ Inmediatamente: si no, contradice la BD |
| 3.4 | **Verificación de sanidad:** `SELECT nombre FROM fases WHERE id=4` **debe** devolver la fase de decimales. Si no, **abortar y restaurar** | 3.2 | Puerta de seguridad antes de cualquier borrado |
| 3.5 | **Parametrizar `FASE5_ID`** → renombrar a `FASE_DECIMALES_ID` con valor **4** en `app/fase5/seed.py:44`, `router.py:47` y `analyze_database.py:18` | 3.4 | 🔑 Ver aviso crítico abajo |
| 3.6 | **Resetear progreso** de `fase_id 4 (Decimales, POST-swap)` en adelante (T1) | 3.5 | Elimina los `intentos` |
| 3.7 | **Verificar que no quedan FK** apuntando a las filas a borrar | 3.6 | Confirmación antes del borrado |
| 3.8 | **Barrido del banco y de MinIO** sobre `fase_id 4 (Decimales, POST-swap)` (C9) — **dry-run obligatorio primero** | 3.7 | 🔑 Solo posible sin FK |
| 3.9 | **Reubicar «Escalas de mapas»** a `fase_id 5 (Fracciones/Proporciones, POST-swap)` | 3.8 | ⚠️ Ver aviso crítico abajo |

#### 🔴 Aviso crítico — `FASE5_ID` es un VALOR, no un nombre

Verificado en el código:

```python
# app/fase5/seed.py:44
FASE5_ID = 5

# líneas 110-114, dentro de clear_fase5_data(), que corre al INICIO del seed (línea 829)
await session.execute(delete(Intento).where(Intento.fase_id == FASE5_ID))
await session.execute(delete(PoolAsignadoAlumno).where(PoolAsignadoAlumno.fase_id == FASE5_ID))
await session.execute(delete(Pregunta).where(Pregunta.fase_id == FASE5_ID))
await session.execute(delete(ConfiguracionProgreso).where(ConfiguracionProgreso.fase_id == FASE5_ID))
await session.execute(delete(NivelTeoria).where(NivelTeoria.fase_id == FASE5_ID))
```

**Tras el intercambio, `fase_id 5` es Fracciones.** Si la siembra corre sin actualizar esa
constante, el seeder **borra íntegramente Fracciones** y siembra la nueva Fase 4 dentro de
su contenedor.

Por eso el paso 3.5 **no es opcional ni cosmético**: es la diferencia entre sembrar en el
sitio correcto y destruir una fase que debía quedar intacta. Y por eso **se adelanta a la
Etapa 3**, en lugar de esperar al renombrado de la Etapa 5.

#### 🔴 Aviso crítico — «Escalas de mapas» y el intercambio

C6.7 envía ese contenido a la fase de Proporciones. **Si se reubica antes del intercambio**
(como preveía el plan original en el paso 0.2), se escribe `fase_id 5`… y el intercambio lo
devuelve a `fase_id 4`, es decir **de vuelta a Decimales**, donde el barrido lo destruye.

Por eso su reubicación se traslada al paso **3.9, después del intercambio y del barrido**,
apuntando explícitamente a `fase_id 5 (Fracciones/Proporciones, POST-swap)`.

Los otros dos destinos (capacidad → Geometría 3D, superficie → Geometría Plana) no sufren
este problema porque sus fases no participan del intercambio: se reubican en el paso 0.2.

### Etapa 4 — Siembra

| # | Paso | Depende de | Motivo |
|---|---|---|---|
| 4.1 | Sembrar **estructura de módulos y niveles** en `fase_id 4 (Decimales, POST-swap)` (C6.6) | 3.9, 1.6 | Requiere `FASE_DECIMALES_ID = 4` (paso 3.5) |
| 4.2 | Sembrar **teoría** por presupuesto (§4.3) y **ejemplos guiados** (C2) | 4.1, 2.4 | El paso con elección debe existir |
| 4.3 | Sembrar **práctica libre** — input libre, 72 familias × 4 (C4, C7.10) | 4.1, 1.6 | |
| 4.4 | Sembrar **desafíos** D1 / D2 / DF / DM (C5) | 4.1, 1.6 | |
| 4.5 | **Validación automática** del pool: presupuestos, R1–R4, ≤25 % por esquema | 4.2–4.4 | Nada se da por bueno sin verificar |
| 4.6 | **Actualizar y ejecutar los tests** — ver §6.A | 4.5 | La suite actual queda rota por el intercambio |

### Etapa 5 — Renombrado de código

| # | Paso | Depende de | Motivo |
|---|---|---|---|
| 5.1 | **Renombrar carpetas y componentes** 4 ↔ 5 vía nombre temporal (T2, §4.7) | 4.6 | Las constantes de `fase_id` ya se corrigieron en el paso 3.5 |
| 5.2 | **Desacoplar el prefijo CSS de la Fase 6** — ver §4.8 | 5.1 | 🔴 La Fase 6 usa `f5-`; sin esto el renombrado la deja sin estilos |
| 5.3 | **Renombrar prefijos CSS** a su fase, vía prefijo temporal — ver §4.8 | 5.2 | ⚠️ CSS y TSX en el mismo commit |
| 5.4 | **Saldar la deuda preexistente** de nomenclatura en fases 8, 9 y 11 (§4.7) | 5.3 | Independiente; se hace al final por ser el paso de menor riesgo |

### Etapa 6 — Documentación

| # | Paso | Depende de |
|---|---|---|
| 6.1 | Actualizar Tomos 1–4 y `guia_creacion_fase.md` (A2–A6) | 5.3 |
| 6.2 | Higiene documental: `reestructuraciondefases.md` (A7) | 6.1 |

---

### Dependencias críticas — resumen

| # | Dependencia | Si se rompe |
|---|---|---|
| 1 | **3.2 (renumeración) antes que 3.6 y 3.8** | 🔴 El reseteo y el barrido caen sobre **Fracciones** y la destruyen |
| 2 | **3.5 (`FASE_DECIMALES_ID = 4`) antes que 4.1** | 🔴 El seeder borra Fracciones y siembra la Fase 4 dentro de su contenedor |
| 3 | **3.9 (escalas) después de 3.2** | 🔴 El intercambio devuelve el contenido a Decimales y el barrido lo destruye |
| 4 | **5.2 (desacoplar Fase 6) antes que 5.3** | 🔴 La Fase 6 queda **sin estilos** |
| 5 | 0.2 antes de 3.8 | Se destruye el contenido que debía migrar a otras fases |
| 6 | 3.0 (¿hay `ON UPDATE CASCADE`?) antes de 3.2 | La renumeración falla o deja registros huérfanos |
| 7 | 3.4 (verificación de sanidad) antes de 3.6 | Se borra sin confirmar que el intercambio salió bien |
| 8 | 3.6 antes de 3.8 | El barrido choca contra las FK de `intentos` |
| 9 | 3.8 antes de 4.x | Se mezcla contenido nuevo con residuo viejo |
| 10 | 1.1 (`tabla_datos`) antes de 4.x | Se siembran miles de preguntas con la tabla rota |
| 11 | 3.2 junto a 3.3 | El mapa canónico contradice a la base de datos |
| 12 | 2.4 antes de 4.2 | Los ejemplos guiados TJS no se pueden renderizar |
| 13 | 4.6 (tests) antes de 5.1 | Se renombra sobre contenido no validado |
| 14 | CSS y TSX en el mismo commit | La fase queda **sin estilos** |

Las cuatro primeras provienen de la **auditoría adversarial** del documento y **causan
pérdida de datos** si se ignoran.

---

## 6.A Tests y plan de reversión

### Tests — la suite actual queda rota

El intercambio y el renombrado rompen la suite existente por dos vías verificadas:

| Archivo | Qué se rompe |
|---|---|
| `app/tests/test_fase_endpoints_contract.py` | Importa `from app.fase5.router import responder_fase5` y `from app.fase4.router import responder_fase4`. El renombrado (5.1) **rompe la colección de pytest**; además su `parametrize` con `fase_id` 4 y 5 queda **semánticamente invertido** tras el intercambio |
| `app/tests/test_pool_integrity.py` | Filtra `fase_id.in_([1..8])` y `range(1, 9)` sobre `seccion < 1000`. Tras el barrido y la re-siembra sus invariantes se aplican a contenido distinto sin que nadie lo revise |

**Paso 4.6 — acciones obligatorias:**

1. Actualizar los imports y la parametrización de `test_fase_endpoints_contract.py`
2. Revisar los invariantes de `test_pool_integrity.py` contra la nueva estructura
3. **Añadir tests nuevos** para lo que la auditoría demostró que nadie vigilaba:
   - que ninguna etiqueta de `tabla_datos` supere 15 caracteres (C8.1)
   - que ningún esquema supere el 25 % del pool de un nivel (C7.2)
   - que magnitud de plantilla y de escenario coincidan (R2)
   - que los presupuestos de contenido se respeten (§4.3)
4. La suite **debe pasar en verde** antes de entrar en la Etapa 5

### Plan de reversión

Hay **cuatro pasos irreversibles encadenados**: 3.2 (renumeración de clave primaria),
3.6 (borrado de progreso), 3.8 (borrado real del banco) y 3.9 (reubicación).

| Concepto | Definición |
|---|---|
| **Dónde vive la copia** | Volcado completo de la BD local + copia del bucket MinIO, con marca de tiempo, fuera del repositorio |
| **Verificación de la copia** | Paso 0.3: restaurarla en una BD desechable y comprobar que la app arranca. **Una copia sin verificar no es una copia** |
| **Punto de no retorno** | El paso **3.8** (borrado real). Hasta ahí, restaurar la copia devuelve el sistema íntegro |
| **Criterio de aborto** | Si el paso 3.4 (verificación de sanidad) falla → **abortar y restaurar**, no intentar arreglar sobre la marcha |
| **Si 3.2 se corta a mitad** | La transacción debe hacer `ROLLBACK` completa. Si aun así queda una fase en el id temporal 904 → restaurar la copia. **No intentar reparar manualmente** |
| **Registro** | Anotar en qué paso se está antes de ejecutarlo, para saber a qué punto volver |

---

## 6.B Volumen de contenido a producir

Las preguntas se **generan**; la teoría y los ejemplos guiados se **escriben**. Este es el
cuello de botella real del plan.

### Teoría — 7 de 12 niveles son nuevos o rehechos

| Módulo | Nivel | Estado |
|---|---|---|
| **1** | N1 · Suma alineando la coma | ✅ Existe — revisar y repartir en pasos |
| | N2 · Resta con completado de ceros | ✅ Existe — revisar |
| | N3 · Combinadas en contexto | ✅ Existe — revisar |
| **2** | N1 · Un factor decimal · 1 cifra | ♻️ Adaptar del actual «Multiplicación con conteo de posiciones» |
| | N2 · Un factor decimal · 2 cifras | 🔨 **Nuevo** (hoy ese hueco es de división) |
| | N3 · Ambos factores decimales | 🔨 **Nuevo** |
| **3** | N1 · Dividendo decimal · 1 cifra | 🔨 **Nuevo** |
| | N2 · Dividendo decimal · 2 cifras | 🔨 **Nuevo** |
| | N3 · Divisor decimal | ♻️ Semilla: el actual «División con desplazamiento de la coma» |
| **4** | N1 · Bajar la escalera | ✂️ Split del actual «Escalera métrica lineal» |
| | N2 · Subir la escalera | ✂️ Split del mismo |
| | N3 · Unidades mixtas | ✅ Existe — revisar |

**Balance (corregido tras auditoría):**

| Estado | Niveles | Cuáles |
|---|---|---|
| ✅ Se conservan | **4** | M1 N1–N3, M4 N3 |
| ♻️ Se adaptan | **2** | M2 N1, M3 N3 |
| 🔨 Nuevos de raíz | **4** | M2 N2, M2 N3, M3 N1, M3 N2 |
| ✂️ Split de uno existente | **2** | M4 N1, M4 N2 |
| | **12** | |

### Ejemplos guiados — 48 en total

| | Cantidad |
|---|---|
| Niveles | 12 |
| Ejemplos por nivel (C2.4) | 4 |
| **Total** | **48** |
| De ellos, **TJS** con formato de 5 pasos (C2.2) | **12** |
| De cálculo resuelto | 36 |

### Además, por cada nivel

- Repartir la teoría en ~4 pasos según el presupuesto de 800 caracteres (§4.3) — **flexible**,
  lo determina el contenido, no un número fijo
- 3 interactivos de evocación con apoyo visual SVG (C3)
- Diccionario en tarjetas de 4 por paso

### Modo de producción del contenido ✅

**El contenido se genera con asistencia (IA), no se redacta enteramente a mano.**

Consecuencias que esto tiene sobre el plan:

| | Implicación |
|---|---|
| ✅ **El volumen deja de ser el cuello de botella** | 48 ejemplos guiados y 12 niveles de teoría son abordables |
| ⚠️ **La validación pasa a ser el cuello de botella** | Contenido generado exige verificación sistemática, no muestreo |
| 🔑 **El paso 4.5 (validación automática) se vuelve crítico** | Es la única defensa contra el tipo de fallo que ya sufrimos: escenarios incoherentes, plantillas repetidas, tablas desbordadas |
| 📋 **Los catálogos son el insumo de la generación** | Escenarios, esquemas y confusiones bien definidos producen contenido correcto; mal definidos lo multiplican mal |

> 💡 **Lección de la auditoría:** los bugs de C7 y C8 nacieron de generación automática sin
> validación. La generación asistida es viable **si y solo si** las reglas R1–R4, los
> presupuestos (§4.3) y la prueba de la plantilla se verifican **antes de sembrar**.

---

---

## 6.C Partición en changes para OpenSpec

> 🎯 **Esta sección es el artefacto de entrega.** Contiene todo lo necesario para ejecutar
> `openspec propose` sin tener que interpretar el resto del documento.

### 6.C.1 Principio de partición

Las **etapas de §6 y los changes de OpenSpec son ejes ortogonales** y no deben confundirse:

| | Criterio de agrupación |
|---|---|
| **Etapas de §6** | Dependencia técnica (qué debe ocurrir antes de qué) |
| **Changes de OpenSpec** | Un *root concern* verificable de extremo a extremo |

Tomar una etapa como change produce lotes sin criterio de aceptación: C7 vive en la Etapa 1
(catálogos) **y** en la Etapa 4 (siembra), así que *«las preguntas tienen ≥6 esquemas»* no es
comprobable hasta que ambas se completan.

> **Regla:** cada change es una **rebanada vertical**, implementable **y verificable** por sí
> sola. Las etapas de §6 pasan a ser el **grafo de dependencias entre changes**.

Cumple `openspec/config.yaml` (*one root concern per change set*) y `deep_analise_pro.md`
§17.12 (*don't mix two roots in one diff*).

### 6.C.2 Los diez changes

| # | Change | Contiene | Etapa §6 |
|---|---|---|---|
| **CH-0** | 🚧 Nota de precedencia documental | Bloque de precedencia en los 4 Tomos y en `MAPA_CANONICO_FASES.md` | — (previo a todo) |
| **CH-1** | Fundación de datos: intercambio y saneamiento | C1, T1, C9, paso 3.5 | 0 y 3 |
| **CH-2** | Motor de generación: catálogos y compositor | C7, C8.1 | 1 |
| **CH-3** | Contenedor visual: ventana fija y cero scroll | T3, T4, §4.2, §4.3, §4.5, C8.2–C8.4 | 2 |
| **CH-4** | Carrusel: paso con elección | C2 (frontend) | 2 |
| **CH-5** | Contenido: estructura de módulos y práctica libre | C6, C4 | 4 |
| **CH-6** | Contenido: desafíos | C5 | 4 |
| **CH-7** | Contenido: teoría y ejemplos guiados | C2 (contenido), C3, C5.13 | 4 |
| **CH-8** | Nomenclatura: carpetas, componentes y CSS | T2, §4.8 | 5 |
| **CH-9** | Documentación normativa completa | A0–A7 | 6 |

### 6.C.2bis 🚧 CH-0 — Nota de precedencia documental *(va primero)*

**Problema que resuelve.** Los Tomos **contradicen activamente** lo que se va a implementar:

| El Tomo dice | El plan hace |
|---|---|
| Tomo 1 §3.1 — *«por lo menos 5 ejemplos guiados»* | 4 |
| Tomo 1 §11 — *«exactamente 120 familias por nivel»* | 72 |
| Tomo 4 §8.1 — *«los datos numéricos NUNCA en prosa»* | En el D1 sí van en prosa |
| Tomo 4 §10.2 — *«N3 de práctica → TJS ligero»* | C4 lo elimina |
| `MAPA_CANONICO_FASES.md` regla 1 — *«bajo ninguna circunstancia re-numerar `fase_id`»* | C1 los renumera |

**Y CH-9 (que los corrige) es el último change.** Es decir: durante CH-1 … CH-8 un agente que
consulte los Tomos encontrará normas que le ordenan lo contrario — y `deep_analise_pro §4`
le obliga a **detenerse y preguntar** ante una contradicción. El conflicto existe desde el
primer change, pero su corrección estaba programada para el último.

**Qué hace CH-0.** Añade un bloque de precedencia —tres o cuatro líneas— al inicio de cada
documento afectado. **No reescribe nada**: solo declara qué manda mientras dure la
reestructuración.

Documentos a marcar:

| Documento |
|---|
| `docs/Criterios Diseno Fase/1_Documento_Rector_Pedagogico.md` |
| `docs/Criterios Diseno Fase/2_Arquitectura_Backend_y_Admin.md` |
| `docs/Criterios Diseno Fase/3_Guia_Frontend_UX.md` |
| `docs/Criterios Diseno Fase/4_Guia_TJS_Desafios.md` |
| `docs/Criterios Diseno Fase/guia_creacion_fase.md` |
| `docs/MAPA_CANONICO_FASES.md` |

Texto del bloque (adaptar el nombre del documento):

> ⚠️ **Reestructuración de la Fase 4 en curso.**
> Para todo lo relativo a la **Fase 4**, prevalece `reestructuracion.md` (raíz del repositorio).
> Las derogaciones concretas de este documento están listadas en su sección **A0**.
> Para las demás fases, este documento sigue siendo normativo sin cambios.
> *(Bloque temporal: se retira cuando CH-9 actualice este documento.)*

**Criterios de aceptación**

- WHEN se abre cualquiera de los 6 documentos → THEN el bloque de precedencia aparece antes de cualquier norma
- WHEN un agente consulta una regla derogada por A0 → THEN el bloque lo remite a `reestructuracion.md`
- WHEN se lee el contenido normativo → THEN **no** ha sido modificado: solo se añadió el bloque
- WHEN se revisan las demás fases → THEN sus normas siguen vigentes sin cambio

**Por qué va primero.** Es el único change que **no depende de nada** y del que **dependen
todos los demás** para no entrar en conflicto. Cuesta minutos y elimina el riesgo de raíz,
en lugar de confiar en que cada prompt lo recuerde.

### 6.C.3 Grafo de dependencias

```
CH-0 ──→ (habilita todo lo demás)   PRIMERO Y SOLO: elimina el conflicto documental

CH-2 ──┐
CH-3 ──┼── pueden arrancar en paralelo tras CH-0 (no tocan la base de datos)
CH-4 ──┘

CH-1 ──┬──→ CH-5 ──┐
       ├──→ CH-6 ──┼──→ CH-8 ──→ CH-9
CH-2 ──┼──→ CH-7 ──┘
CH-4 ──┘
```

| Dependencia | Motivo |
|---|---|
| **CH-0 → todos** | Sin la nota de precedencia, los Tomos contradicen la implementación y el agente se detiene a preguntar (`deep_analise_pro §4`) |
| CH-1 → CH-5, CH-6, CH-7 | No se siembra sobre una BD sin renumerar ni barrer |
| CH-2 → CH-5, CH-6, CH-7 | El compositor y los catálogos son el insumo de la siembra |
| CH-4 → CH-7 | Sin el paso con elección, el ejemplo guiado TJS no se puede renderizar |
| CH-5, CH-6, CH-7 → CH-8 | No se renombra sobre contenido sin validar |
| CH-8 → CH-9 | La documentación describe el estado final |

### 6.C.4 ⚠️ CH-1 es irreversible — no sigue el ciclo normal

El ciclo *propose → implementar → probar → siguiente* asume que un fallo se corrige y se
repite. **CH-1 contiene borrados reales y una renumeración de clave primaria: sobre eso no
se itera.**

Procedimiento obligatorio y distinto para CH-1:

```
1. Ensayar CH-1 COMPLETO sobre una COPIA de la BD local
2. Verificar sus criterios de aceptación sobre esa copia
3. DESCARTAR la copia
4. Solo entonces ejecutar sobre la BD local real
```

Los demás changes sí siguen el ciclo normal.

### 6.C.5 Criterios de aceptación por change

Redactados para convertirse directamente en `#### Scenario:` con `WHEN` / `THEN`.

**CH-1 — Fundación de datos**

- WHEN se consulta `SELECT nombre FROM fases WHERE id = 4` → THEN devuelve la fase de decimales
- WHEN se consulta `SELECT nombre FROM fases WHERE id = 5` → THEN devuelve la fase de fracciones
- WHEN se cuentan filas por `fase_id` en las fases 0–3 → THEN los conteos son idénticos a los previos a CH-1
- WHEN se busca contenido de capacidad o superficie en `fase_id 4` → THEN no hay resultados
- WHEN se busca el módulo aparcado en `fase_id 6` y `fase_id 7` → THEN existe con `modulo_id ≥ 90` e inactivo
- WHEN se consulta el progreso de un alumno en fases ≥ 4 → THEN está vacío
- WHEN se consulta su progreso en fases 0–3 → THEN está intacto

**CH-2 — Motor de generación**

- WHEN una plantilla de magnitud `dinero` recibe un escenario de magnitud `longitud` → THEN el generador falla con error explícito (R2)
- WHEN una plantilla exige un campo que el escenario no tiene → THEN el generador falla (R1)
- WHEN se agrupa el pool de un nivel por `plantilla_id` → THEN ningún esquema supera el 25 %
- WHEN se cuentan los esquemas de un nivel → THEN son ≥ 6
- WHEN una etiqueta de `tabla_datos` supera 15 caracteres → THEN el validador la rechaza
- WHEN se renderiza una tabla de 3 filas con etiquetas al límite → THEN no hay solapamiento ni recorte

**CH-3 — Contenedor visual**

- WHEN se abre cualquier paso en 1024×768 (tablet horizontal) → THEN no aparece scroll vertical
- WHEN se mide el contenedor en cualquier nivel y fase → THEN es 950×620
- WHEN un paso de teoría supera 800 caracteres → THEN el validador lo rechaza
- WHEN se muestra el teclado numérico → THEN la tecla decimal muestra `,`
- WHEN el alumno escribe `.` en el input → THEN se acepta igualmente
- WHEN se avanza por un nivel → THEN el contador es por bloque, no global

**CH-4 — Carrusel: paso con elección**

- WHEN el alumno llega al paso 3 del ejemplo guiado TJS → THEN no puede avanzar sin elegir una opción
- WHEN elige una opción incorrecta → THEN avanza igualmente y ve la resolución
- WHEN elige la correcta → THEN ve igualmente el paso 5 con la explicación de todos los distractores
- WHEN se consulta el puntaje del nivel → THEN la elección del paso 3 no lo ha alterado

**CH-5 — Estructura y práctica libre**

- WHEN se listan los módulos de `fase_id 4` → THEN son exactamente 4, con los nombres canónicos de C7.8
- WHEN se listan los niveles de cada módulo → THEN son exactamente 3
- WHEN se sirve una pregunta de práctica libre → THEN su `tipo_pregunta` no es `MULTIPLE_OPCION`
- WHEN se cuentan las familias de un nivel → THEN son 72, con 4 variantes cada una
- WHEN el alumno falla 4 veces seguidas en práctica → THEN aparece el Bloque de Rescate

**CH-6 — Desafíos**

- WHEN se listan los bloques de desafío de la fase → THEN son 13 (4 módulos × 3 + 1 DM)
- WHEN se sirve una pregunta del D1 → THEN es problema de contexto con opción múltiple y palabra clave que señala la operación
- WHEN se sirve una del D2 → THEN es TJS con opción múltiple
- WHEN se sirve una del DF → THEN es `RESPUESTA_NUMERICA` con al menos un dato irrelevante
- WHEN se sirve una del DM → THEN el pool mezcla los tres formatos
- WHEN un enunciado de desafío supera 40 palabras → THEN el validador lo rechaza
- WHEN el DF exige redondeo por contexto → THEN existe un `errores_previstos` para la respuesta aritmética sin ajustar

**CH-7 — Teoría y ejemplos guiados**

- WHEN se cuentan los ejemplos guiados de un nivel → THEN son 4
- WHEN se identifica el TJS entre ellos → THEN es exactamente 1 y tiene 5 pasos
- WHEN un interactivo de evocación presenta datos → THEN están fuera de la prosa
- WHEN el enunciado del D1 presenta datos → THEN están **en** la prosa (excepción C5.5)
- WHEN un visual acompaña una pregunta → THEN no ejecuta el procedimiento (regla anti-revelación)
- WHEN la teoría menciona décimas o centésimas → THEN no usa el vocabulario de fracciones

**CH-8 — Nomenclatura**

- WHEN se busca `f5-` en `components/fase6/` → THEN no hay resultados
- WHEN se abre la Fase 6 → THEN renderiza con estilos
- WHEN se compara carpeta, nombre de archivo y constante de cada fase → THEN coinciden con su número
- WHEN se ejecuta la suite completa → THEN pasa en verde

**CH-9 — Documentación**

- WHEN se lee cada Tomo afectado → THEN no contradice la implementación
- WHEN se lee `MAPA_CANONICO_FASES.md` → THEN coincide con `SELECT id, nombre FROM fases`
- WHEN se busca una regla derogada → THEN aparece su derogación explícita con justificación (A0)

### 6.C.6 Non-goals — obligatorio en cada proposal

`openspec/config.yaml` exige una sección de *non-goals*. Estos valen para **todos** los changes:

| Fuera de alcance | Motivo |
|---|---|
| Cualquier fase que no sea la Fase 4 | §1.A — principio de gobierno |
| Las fases 1, 2 y 3 | Congeladas bajo Modelo A (Tomo 1 §6) |
| VPS, producción y scripts de sincronización | §6 — todo el trabajo es local |
| Reorganizar el contenido aparcado en Geometría | Se analiza cuando se planee esa fase |
| El motor de selección aleatoria de preguntas | Prohibición del Tomo 4 §4; C5.12 la respeta |
| El Bucle Espejo y el Bloque de Rescate | C4 los devuelve a su diseño original sin tocar su lógica |

**Excepciones autorizadas al principio de gobierno** — cada proposal que las contenga debe
declararlas:

| Change | Excepción | Justificación |
|---|---|---|
| CH-1 | Resetea el progreso de las fases 5–11 | La renumeración vuelve ambiguo ese registro (§4.6) |
| CH-1 | Añade un módulo aparcado inactivo a las fases 6 y 7 | Depósito, no reestructuración (§6) |
| CH-8 | Renombra el prefijo CSS de la Fase 6 | Requisito técnico ineludible (§4.8) |
| CH-8 | Corrige la nomenclatura de las fases 8, 9 y 11 | Higiene, sin cambio de contenido (§4.7) |

### 6.C.7 Impacto sobre datos de alumnos — obligatorio declararlo

`openspec/config.yaml` exige *call out behavior changes for existing student data*.

| Change | Impacto |
|---|---|
| **CH-1** | 🔴 **Borra el progreso de todas las fases ≥ 4.** Conserva íntegro el de las fases 0–3 |
| CH-5, CH-6, CH-7 | El contenido cambia: el progreso previo carecería de sentido aunque se conservara |
| Resto | Sin impacto sobre datos de alumnos |

### 6.C.8 Orden de ejecución sugerido

| Fase de trabajo | Changes | ¿Paralelo? |
|---|---|---|
| **0ª** | **CH-0** | ❌ Va primero, solo |
| 1ª | CH-2, CH-3, CH-4 | ✅ Sí — ninguno toca la BD |
| 2ª | **CH-1** | ❌ No — ensayo sobre copia primero (§6.C.4) |
| 3ª | CH-5, CH-6, CH-7 | ✅ Sí entre ellos, tras CH-1 y CH-2 |
| 4ª | CH-8 | ❌ Requiere todo lo anterior validado |
| 5ª | CH-9 | ❌ Describe el estado final |

Arrancar por la 1ª tiene una ventaja: **valida el enfoque sin riesgo alguno sobre los datos.**

## 7. Pendiente de definir — global

- Resto de reordenamientos de fases (se añadirán a la tabla de la sección 2)
- Orden de ejecución una vez cerrada la planeación completa
