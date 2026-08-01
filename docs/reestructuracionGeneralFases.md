# Reestructuración General de Fases — Método y Lecciones

> **Estado:** normativo. Base metodológica para reestructurar **cualquier fase** de LogicaKids Pro.
> **Origen:** errores reales cometidos durante la reestructuración de la Fase 4 (cerrada el 2026-07-30).
> **Fase piloto validada:** Fase 4 — *Operatoria Decimal y Conversiones*.
>
> Documentos relacionados:
> - [`auditoriafase4.md`](../auditoriafase4.md) — bitácora de auditoría (qué falló, con evidencia).
> - [`implementacionfase4.md`](../implementacionfase4.md) — memoria de implementación (qué se construyó).
> - [`reestructuraciondefases.md`](./reestructuraciondefases.md) — plan histórico de la Fase 4. **No normativo**: es prueba del planeamiento, no instrucción universal.
> - [`Criterios Diseno Fase/5_Criterios_Teoria_Ejemplos_y_Visuales.md`](./Criterios%20Diseno%20Fase/5_Criterios_Teoria_Ejemplos_y_Visuales.md) — reglas de UX validadas en la Fase 4.

---

## 0. Para qué existe este documento

La Fase 4 funcionó al final, pero costó **mucho más de lo que debía**. No por el tamaño del contenido, sino por el **orden en que se hicieron las cosas**.

Este documento existe para que la Fase 5 y las siguientes **no repitan la secuencia**. No es un plan de contenido: es un método de trabajo.

Su tesis central:

> **El costo de una reestructuración no lo determina cuánto contenido hay que mover, sino cuánto acoplamiento oculto hay que desenredar y cuántas verificaciones faltan para detectar un error temprano.**

---

## 1. Los cinco fallos raíz de la Fase 4

Cada uno está documentado con evidencia en `auditoriafase4.md`. No son opiniones: son hechos verificados.

### 1.1. No existía red de tests antes de tocar el código

`conftest.py` no existía. Los tests de la fase **nunca corrieron, ni antes ni después** del cambio. Uno de ellos (`test_fase4_vocabulario.py`) importaba vocabulario de la fase anterior e iteraba un nivel `(3,4)` inexistente; su fallo de importación **rompía la colección de toda la suite**, así que ningún test del proyecto protegía nada.

**Consecuencia medible:** el defecto más grave de toda la reestructuración —*ninguna pregunta de práctica tenía respuesta correcta*— sobrevivió **tres rondas de revisión** porque no había un test que comparara enunciado contra respuesta.

### 1.2. "Piezas creadas y no conectadas"

Este es **el patrón de fallo número uno**, y se repitió al menos tres veces:

| Pieza construida | Estado real al declararse "completo" |
|---|---|
| `compositor_fase4.py` (motor de variedad) | Existía en disco; el seeder seguía leyendo el catálogo viejo. **No estaba en efecto.** |
| Compositor en desafíos (D1/D2/DF/DM) | Conectado solo a práctica. Los desafíos seguían con enunciados hardcodeados. |
| Script de verificación `verify_*.py` | Apuntaba a un módulo en ruta equivocada. **Un validador que no se ejecuta no valida nada.** |

**Lección:** que un archivo exista no significa que el sistema lo use. Hay que verificar el **punto de entrada real** (el seeder, el router), no la existencia del archivo.

### 1.3. Reportes de éxito sin evidencia ejecutada

Se declaró un commit como *"Reestructuración completa CH-0 a CH-9"*. La auditoría posterior encontró que **CH-0 y CH-9 no se habían implementado en absoluto**, y que un import roto (`from app.fase5.theory_data import ...`, archivo que ese mismo commit borró) **impedía sembrar la fase**.

**Lección:** la prosa de un agente no es evidencia. Solo cuenta el comando ejecutado y su salida.

### 1.4. Acoplamiento entre fases por constantes cableadas

Este es **el error de arquitectura de fondo**, y el más caro:

- `FASE5_ID` cableado como literal en **tres archivos distintos**.
- Prefijos CSS compartidos: la **Fase 6 usaba el prefijo `f5-`**.
- `NIVELES_META` duplicado en el router como **segunda fuente de verdad**, desalineado con `theory_data.py`.

**Consecuencia medible:** por ese desalineamiento, el **Módulo 4 nunca se desbloqueaba** — el código iteraba `range(1, 5)` sobre los niveles del módulo 3, que solo tenía 3, así que el progreso quedaba permanentemente incompleto.

**Lección:** cuando las fases no son módulos aislados, reordenarlas no es un cambio de configuración: es cirugía de alto riesgo.

#### 1.4.1. Cómo diseñar módulos desacoplados desde el inicio (para apps nuevas)

Lo de arriba es el diagnóstico sobre código ya existente. Si estás **diseñando un módulo nuevo desde cero** (una fase nueva, o una app completamente distinta con la misma forma modular), estas cinco reglas evitan que el problema exista, en vez de tener que detectarlo después:

**a) Una sola fuente de verdad por dato, nunca dos copias**

```python
# MAL — dos archivos con la misma información, que se desalinean en silencio
# router.py:      NIVELES_META = {...}
# theory_data.py: NIVELES_META = {...}   (copia paralela)

# BIEN — un solo lugar que todos consultan
from app.core.niveles_registry import get_nivel_meta
```

Si el mismo dato hace falta en dos archivos, uno de los dos **importa** del otro. Nunca se copia y pega.

**b) IDs nunca como número mágico — se resuelven por nombre/slug**

```python
# MAL — el número está memorizado en el código; reordenar fases obliga a buscarlo a mano
if fase_id == 5:
    ...

# BIEN — el slug no cambia aunque el id sí
FASE_DECIMALES = get_fase_by_slug("decimales")
if fase_id == FASE_DECIMALES.id:
    ...
```

**c) Namespacing real en CSS/nombres, no solo un prefijo de texto**

```css
/* MAL — un prefijo de texto que cualquiera puede copiar a otro módulo por error */
.f5-header { }

/* BIEN — scoping estructural (CSS Modules / styled-components / carpeta por fase),
   donde es imposible que otro módulo lo use por accidente, no solo "improbable"  */
```

**d) Cada fase es una carpeta que ningún otro módulo importa directamente**

```
app/
  fases/
    fase_decimales/     ← todo lo de esta fase vive aquí
    fase_fracciones/    ← todo lo de esta fase vive aquí
  core/
    fase_registry.py    ← ÚNICA fuente de verdad de qué fases existen y su orden
```

Si la Fase 6 necesita algo de la Fase 5, no hace `from fase5.utils import algo`: pasa por una interfaz común en `core/`. El momento en que dos fases se "hablan" directamente es la señal de que ese dato debería vivir en `core/`.

**e) Un test o `grep` en CI que detecte acoplamiento en el primer commit, no dos años después**

```bash
# Falla si aparece el id/slug de una fase hardcodeado fuera de su propia carpeta
grep -rn "FASE5_ID\|fase_id *== *5" --include=*.py app/ | grep -v "app/fases/fase_fracciones/"
```

Este es el punto más valioso de los cinco: sin él, el acoplamiento se acumula en silencio durante meses. Con él, se detecta y se rechaza en el mismo commit que lo introduce.

### 1.5. Contenido generado sin fuente única de verdad

El compositor calculaba el **enunciado** desde una plantilla y la **respuesta** desde otro generador, con números distintos. Resultado: cero preguntas correctas en toda la fase.

**Lección:** una fórmula → unos valores → de ahí salen **enunciado, respuesta, explicación y distractores**. Nunca dos generadores paralelos.

---

## 2. Orden de planeación correcto

El error de secuencia de la Fase 4 fue **implementar primero y verificar después**. El orden correcto invierte eso.

Cada etapa tiene una **puerta de salida** (gate): no se avanza sin cumplirla.

### Etapa 0 — Inventario de acoplamiento *(antes de tocar una sola línea)*

Antes de diseñar nada, averiguar **qué del resto del sistema depende de esta fase**.

Barridos obligatorios:

```bash
# Constantes e identificadores de la fase cableados fuera de su carpeta
grep -rn "FASE5_ID\|fase_id *= *5\|faseId: *5" --include=*.py --include=*.ts --include=*.tsx .

# Prefijos CSS de esta fase usados por otras fases
grep -rn "f5-" --include=*.css --include=*.tsx . | grep -v "components/fase5/"

# Segundas fuentes de verdad: metadatos duplicados entre router y datos
grep -rn "NIVELES_META\|MODULOS_META" --include=*.py .

# Imports cruzados entre fases
grep -rn "from app.fase[0-9]" --include=*.py app/ | grep -v "app/fase5/"
```

> **Gate 0:** existe una lista escrita de cada punto de acoplamiento, con decisión explícita por cada uno: *se desacopla ahora* / *se deja y se documenta como deuda*. Ningún punto puede quedar sin decisión.

### Etapa 1 — Contrato de invariantes y arnés de tests *(en rojo, antes de implementar)*

Escribir los tests **antes** de la implementación, y comprobar que **fallan**. Un test que pasa antes de implementar no está probando nada.

Invariantes mínimos, derivados de los fallos de la Fase 4:

| Invariante | Qué previene |
|---|---|
| Respuesta derivada de la misma fórmula y valores del enunciado | El defecto catastrófico (§1.5) |
| Toda plantilla tiene al menos un escenario compatible | Plantillas huérfanas que rompen la siembra |
| `estructura_padre_id` nunca nulo | Progreso imposible (Tomo 4 §11) |
| Vocabulario prohibido ausente (dominio de otra fase) | Fugas de contenido tras el intercambio |
| Coma decimal, sin placeholders crudos, sin `de el` | Defectos de presentación en masa |
| Variedad estructural real (firmas, no reformulaciones) | Cumplir la letra y no el espíritu de la regla |
| Determinismo: misma semilla → misma pregunta | Siembras irreproducibles |
| Contrato de magnitud rechaza combinaciones incompatibles | "Sumar peras con manzanas" |

Referencia ejecutable: `LogicaMath/backend/tests/test_fase4_vocabulario.py`.

> **Gate 1:** la suite existe, corre, y **falla** por las razones esperadas. Además: `pytest` colecciona el proyecto completo sin errores de importación.

### Etapa 2 — Diseño pedagógico y nivel piloto

Definir estructura (módulos × niveles), objetivos y magnitudes/dominios permitidos por módulo. Corregir **un solo nivel piloto** y **esperar aprobación visual** antes de extender.

> **Gate 2:** el nivel piloto está aprobado visualmente por el responsable humano. El patrón está descrito por escrito, no solo aplicado.

### Etapa 3 — Contrato de datos del generador

Definir la fuente única: `fórmula + valores → enunciado, respuesta, explicación, distractores`. Los distractores deben encarnar **errores reales** (operación invertida, coma desplazada, dato olvidado), no ruido aleatorio, y ser **plausibles en magnitud** — un distractor 100 veces mayor que la respuesta se descarta de un vistazo y no mide nada.

> **Gate 3:** los tests de la Etapa 1 sobre coherencia enunciado↔respuesta pasan en verde.

### Etapa 4 — Operaciones irreversibles, aisladas

El intercambio de claves primarias es **la única operación genuinamente irreversible**. Todo lo demás se corrige iterando.

Reglas:

1. Dump lógico verificado **antes** (y comprobar que el dump no está vacío y es restaurable).
2. Ejecutar en una transacción única, con id temporal para evitar colisión de PK.
3. Checkpoint de verificación propio antes de continuar.
4. Nunca mezclarla en el mismo paso con cambios de contenido.

> **Gate 4:** `SELECT id, nombre, orden FROM fases` devuelve el mapeo esperado, y el backup está verificado.

### Etapa 5 — Implementación conectada

Implementar el generador **y conectarlo**. Verificación explícita de conexión:

```bash
# El seeder, ¿realmente invoca el compositor?
grep -n "_COMPOSITOR\|componer_pregunta" app/fase5/seed.py

# ¿Quedan lecturas del catálogo viejo?
grep -rn "catalogo_fase4.json\|CATALOGO_DATA\[" app/fase5/
```

**No dejar generadores de reserva silenciosos.** En la Fase 4, el bloque *legacy* de respaldo (406 líneas) generaba contenido de un dominio prohibido y leía campos inexistentes. Si el generador principal falla, la siembra **debe fallar ruidosamente**, no colar una pregunta de otra magnitud.

> **Gate 5:** los tests de la Etapa 1 pasan **todos** en verde, y el barrido de conexión no encuentra residuos.

### Etapa 6 — Pase de UX

Teoría, ejemplos guiados, figuras. Reglas completas en [`5_Criterios_Teoria_Ejemplos_y_Visuales.md`](./Criterios%20Diseno%20Fase/5_Criterios_Teoria_Ejemplos_y_Visuales.md). Siempre: piloto → aprobación → extensión.

> **Gate 6:** cero scroll vertical y cero contenido cortado, verificado visualmente, no inferido del código.

### Etapa 7 — Barrido por flujo, no por componente

El mismo contenido reaparece en: práctica libre · batería · bucle espejo · bloque de rescate · desafíos de módulo · desafío mixto · vistas admin/preview.

> **Gate 7:** la misma pregunta se ve correcta en **todos** los flujos donde aparece.

### Etapa 8 — Verificación real y cierre

1. Suite backend + frontend + `tsc --noEmit` en verde (fallos preexistentes ajenos, identificados y separados).
2. Verificación contra **base de datos real**, no solo contra el generador Python.
3. Siembra ejecutada **dos veces** consecutivas: los conteos deben ser idénticos (idempotencia).
4. Despliegue y lectura de logs.
5. Documento de cierre: qué fue plan, qué fue implementación, qué queda como deuda.

> **Gate 8:** conteos verificados con `SELECT` contra la BD real, y logs de arranque sin excepciones.

---

## 3. Reglas de delegación a agentes de IA

La Fase 4 la implementaron varios modelos. Ninguno falló por incapacidad: fallaron porque **nadie verificaba sus entregas contra ejecución real** hasta que fue tarde.

| Regla | Por qué |
|---|---|
| **Exigir el comando y su salida**, no el resumen en prosa | Se declaró "CH-0 a CH-9 completo" con la fase imposible de sembrar |
| **El criterio de aceptación es "suite en verde"**, no "reporte de éxito" | Un arnés de tests detecta en segundos lo que una auditoría manual tarda días en encontrar |
| **Verificar conexión, no existencia** de cada pieza nueva | §1.2, el patrón de fallo número uno |
| **Un cambio a la vez**, con verificación entre cambios | Los errores se acumulan y se ocultan entre sí |
| **Prohibir parches paliativos** sin autorización explícita | Se usó `SEED_DB=false` para tapar un crash-loop en vez de arreglar la raíz |
| **Exigir reporte de lo NO resuelto** | Lo que un agente calla es lo que después cuesta caro |

---

## 4. Catálogo de anti-patrones

Todos observados en la Fase 4. Buscar activamente cada uno.

1. **Pieza creada y no conectada** — existe en disco, nadie la invoca.
2. **Validador que no se ejecuta** — apunta a una ruta equivocada; no valida nada.
3. **Segunda fuente de verdad** — metadatos duplicados entre router y datos, que se desalinean en silencio.
4. **Import roto tras renombrar** — se mueve o borra un módulo sin actualizar referencias. Ocurrió al menos tres veces (`fase5.theory_data`, el script de verificación, `app.fase8.seed_fase8`).
5. **Cumplir la letra, no el espíritu** — "≥6 esquemas" satisfecho con seis redacciones de **una misma estructura**. Por eso la métrica correcta es la **firma estructural** `(operación, incógnita, nº de datos)`, no el conteo de plantillas.
6. **Fuga de dominio** — vocabulario o magnitudes de otra fase que sobreviven al intercambio (litros y volumen persistieron en la Fase 4 hasta la última pasada).
7. **Coherencia física ignorada** — la magnitud sola no basta. `longitud` abarca el grosor de una moneda y una maratón; sin un eje de **escala**, se generó *"recorrió un trayecto en la pila de monedas de 1,57 km"*.
8. **Fallback silencioso** — un generador de reserva que produce contenido inválido en lugar de fallar.
9. **Enunciado lógicamente imposible** — los gastos superan el monto inicial y aun así se pregunta cuánto sobró. El alumno falla por el enunciado, no por su razonamiento.
10. **Residuo de nomenclatura cruzada** — funciones `..._fase4` viviendo en la carpeta `fase5` y viceversa.

---

## 5. Deudas cruzadas detectadas (fuera del alcance de la Fase 4)

Reveladas al tocar código compartido. **No se corrigieron** por disciplina de alcance. Deben tratarse en su propia fase:

| Deuda | Impacto |
|---|---|
| Fase 1 con `estructura_padre_id` **100% NULL** | Mismo patrón que impedía el progreso en Fase 4 |
| Fase 8: módulo de siembra inexistente (`app.fase8.seed_fase8`) | Rompe el arranque completo del backend si se invoca |
| `test_scripts_config.py` no colecciona (`app.core.config` no existe) | Test muerto |
| `test_ux_feedback.py::test_create_ux_feedback_multiple_images` falla | Preexistente, subsistema del buzón |
| `faseMetadata.ts` declara "Fase 4: Fracciones" | Dato inalcanzable hoy, pero mentiroso si se reactiva |

---

## 6. Checklist de arranque para la próxima fase

Antes de escribir la primera línea de la Fase 5:

- [ ] Etapa 0 ejecutada: lista escrita de acoplamientos, con decisión por cada uno
- [ ] `pytest` colecciona el proyecto completo sin errores de importación
- [ ] Arnés de invariantes escrito y **fallando** por las razones correctas
- [ ] Dominio/magnitudes permitidos por módulo, declarados por escrito
- [ ] Vocabulario prohibido (el que pertenece a otras fases) declarado como test
- [ ] Fuente única de verdad del generador, definida antes de implementar
- [ ] Acceso reproducible a una BD de prueba, disponible **desde el día uno**
- [ ] Operación irreversible identificada y aislada, con backup verificado
- [ ] Criterio de aceptación acordado con quien implemente: **suite en verde**, no prosa

---

## 7. Beneficios comprobados del método

Lo que la Fase 4 sí dejó como ganancia reutilizable:

1. **Compositor con contrato de validación** (`compositor_fase4.py`): plantillas como datos + escenarios con campos gramaticales, con validación *fail-closed*. Replicable a cualquier fase.
2. **Firma estructural** como métrica de variedad no manipulable.
3. **Regla anti-revelación**: la figura presenta datos, jamás ejecuta el procedimiento.
4. **T3/T4** (cero scroll, ventana fija) como reglas innegociables de diseño.
5. **Arnés de regresión**: un test por cada defecto encontrado, para que no vuelva.
6. **Separación documental de tres capas**: plan (qué se acordó) · implementación (qué se construyó) · deuda (qué queda). Sin esa separación, un agente lee un plan viejo como si fuera la norma actual.

---

## 8. La lección de una sola frase

> **Construir el arnés de verificación primero, desacoplar antes de mover, y no aceptar nunca "está hecho" sin la salida del comando que lo demuestra.**

Todo lo demás de este documento es desarrollo de esa frase.
