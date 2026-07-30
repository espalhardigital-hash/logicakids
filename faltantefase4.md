 # Trabajo pendiente — Nueva Fase 4

> **Documento de implementación.** Deriva de una auditoría del commit `b2b1a8b`
> *(v0.0.9 Nueva Fase 4 — Reestructuración completa CH-0 a CH-9)*.
>
> El commit implementó la mayor parte del plan, pero dejó **tres bugs bloqueantes**, **una
> integración sin conectar** y **dos changes sin ejecutar**. Este documento es la lista
> cerrada de lo que falta, con archivo, línea, código actual, código objetivo y comando de
> verificación para cada punto.

---

## Cómo usar este documento

| Regla | Detalle |
|---|---|
| **Precedencia** | `reestructuracion.md` es el QUÉ · `RULES AGENTES/deep_analise_pro.md` es el CÓMO (§25 en particular) · este documento es el **pendiente concreto** |
| **Orden** | Los bloques van en orden de dependencia. **No saltes el Bloque A**: sin él nada de lo demás se puede probar |
| **Verificación** | Cada tarea trae su comando. **Ejecútalo y muestra la salida real.** No des una tarea por hecha sin evidencia (`deep_analise_pro §19`) |
| **Alcance** | Solo local. Sin VPS, sin producción |
| **Fuera de alcance** | Los bugs de Fase 5 y posteriores están inventariados en el Bloque G pero **no se corrigen aquí**, salvo el F3 que es requisito del Bloque A |

### Lo que ya está hecho — NO rehacer

Verificado en el commit. No lo toques:

| Change | Estado |
|---|---|
| **CH-2 (catálogos)** | `escenarios_fase4.json` (80), `plantillas_fase4.json` (72), `confusiones_fase4.json` (48), `nombres_fase4.json` (15). Números exactos del plan |
| **CH-2 (compositor)** | `compositor_fase4.py` con validación fail-closed completa: R1, R2, etiqueta ≤15, enunciado ≤250, opciones ≤60, ≥6 esquemas, ≤25 % |
| **CH-3** | Ventana `950 × 620` en `Fase4Styles.css:712-729`, `overflow-y: hidden !important`, contadores por bloque en `Fase4TheoryModal.tsx:68-81` |
| **CH-4** | `modo_compromiso` / `eleccion_guiada` en `Fase4TheoryModal.tsx:118-120, 388` |
| **CH-5** | 4 módulos × 3 niveles (`seed.py:152-153, 592-593, 958-959`) |
| **CH-6** | 13 bloques de desafío (`seed.py:894-899`) |
| **CH-7** | 12 niveles con los títulos aprobados · 48 ejemplos guiados · TJS de 5 pasos · validador `validar_contenido_pre_siembra()` en `seed.py:140` |
| **CH-8** | Prefijos CSS limpios: fase4=`f4-` (715), fase5=`f5-` (492), fase6=`f6-` (704), **cero cruces** |
| **CH-1 (parcial)** | `FASE_DECIMALES_ID = 4` en `seed.py:44`, `router.py`, `analyze_database.py`; los `DELETE` ya apuntan a esa constante |

---

# BLOQUE A — Bugs bloqueantes (imports rotos)

> 🔴 **Ahora mismo `app.fase4.seed` no se puede importar.** La nueva Fase 4 **no se puede
> sembrar**. Esto es lo primero.

## F1 · `fase4/seed.py` importa un módulo borrado

**Archivo:** `LogicaMath/backend/app/fase4/seed.py`
**Línea:** 37

**Causa:** el commit borró `app/fase5/theory_data.py` y creó `app/fase4/theory_data.py`, pero
el import no se actualizó.

```python
# ACTUAL (línea 37) — el módulo no existe
from app.fase5.theory_data import FASE5_TEORIA_DATA
```

```python
# OBJETIVO
from app.fase4.theory_data import FASE5_TEORIA_DATA
```

> ⚠️ **El nombre del símbolo sigue siendo `FASE5_TEORIA_DATA`** — así se llama en
> `fase4/theory_data.py:17`. **No lo renombres en este paso**; se hace en F8 junto con los
> demás nombres obsoletos, para no mezclar dos raíces en un diff (`deep_analise_pro §17.12`).

## F2 · `fase4/seed.py` importa la función con el nombre cruzado

**Archivo:** `LogicaMath/backend/app/fase4/seed.py`
**Línea:** 138

**Causa:** el renombrado cruzó los nombres de función entre las dos fases.

| Archivo | Función que define |
|---|---|
| `fase4/theory_examples.py:9` | `obtener_ejemplos_expandidos_fase5` ← nombre obsoleto |
| `fase5/theory_examples.py:6` | `obtener_ejemplos_expandidos_fase4` ← nombre obsoleto |

```python
# ACTUAL (línea 138) — apunta al módulo de la OTRA fase
from app.fase5.theory_examples import obtener_ejemplos_expandidos_fase5
```

```python
# OBJETIVO — módulo propio, nombre tal como está definido hoy
from app.fase4.theory_examples import obtener_ejemplos_expandidos_fase5
```

Solo cambia `fase5` → `fase4` en la ruta del módulo. El nombre de la función se corrige en F8.

## F3 · `fase5/seed.py` importa del módulo de la Fase 4

**Archivo:** `LogicaMath/backend/app/fase5/seed.py`
**Línea:** 27

Se corrige **aquí y no en el Bloque G** porque, mientras `fase5/seed.py` importe de
`app.fase4.theory_examples`, cualquier renombrado en F8 romperá la Fase 5 en cascada.

```python
# ACTUAL (línea 27)
from app.fase4.theory_examples import obtener_ejemplos_expandidos_fase4
```

```python
# OBJETIVO — módulo propio
from app.fase5.theory_examples import obtener_ejemplos_expandidos_fase4
```

## F4 · Scripts de auditoría con imports rotos

Tres archivos importan de `app.fase5` lo que vive en `app.fase4`:

| Archivo | Línea | Import actual | Objetivo |
|---|---|---|---|
| `fase4/verify_ch0_to_ch6_scenarios.py` | 42 | `from app.fase5.seed import (` | `from app.fase4.seed import (` |
| `fase4/verify_ch0_to_ch6_scenarios.py` | 47 | `from app.fase5.compositor_fase4 import CompositorFase4` | `from app.fase4.compositor_fase4 import CompositorFase4` |
| `fase4/audit_ch6_desafios.py` | 46 | `from app.fase5.seed import (` | `from app.fase4.seed import (` |
| `fase4/audit_master_fase4.py` | 47 | `from app.fase5.seed import (` | `from app.fase4.seed import (` |

> 📌 `verify_ch0_to_ch6_scenarios.py` es el script que **debía** verificar CH-0 a CH-6. Estaba
> roto, y por eso los bugs F1, F2 y F5 pasaron desapercibidos. Arreglarlo y **ejecutarlo** es
> parte de la tarea.

## ✅ Puerta de verificación del Bloque A

Ejecuta **exactamente esto**. Los cuatro módulos deben decir `OK`:

```bash
cd LogicaMath/backend
python -c "
import sys; sys.path.insert(0,'.')
for m in ['app.fase4.seed','app.fase4.router','app.fase5.seed','app.fase5.router']:
    try:
        __import__(m); print(f'{m}: OK')
    except Exception as e:
        print(f'{m}: {type(e).__name__}: {e}')
"
```

Y después el script de verificación, que ya debe arrancar:

```bash
cd LogicaMath/backend && python -m app.fase4.verify_ch0_to_ch6_scenarios
```

> **No pases al Bloque B hasta que los cuatro imports digan `OK`.**

---

# BLOQUE B — Conectar el compositor (el pendiente más importante)

> 🔴 **Los catálogos nuevos y el compositor existen pero NO se usan.** El seeder sigue
> leyendo el catálogo antiguo. Toda la corrección de variedad de C7 está en disco y **sin
> efecto**.

## F5 · El seeder ignora el compositor y usa el catálogo viejo

**Estado actual — evidencia:**

```
grep compositor LogicaMath/backend/app/fase4/seed.py   →  (vacío)

seed.py:46   CATALOGO_PATH = os.path.join(..., "data", "catalogo_fase5.json")   ← el ANTIGUO
seed.py:197  escenarios_mod = [e for e in CATALOGO_DATA["escenarios"] ...]
seed.py:198  confusiones_mod = [c for c in CATALOGO_DATA["confusiones"] ...]
```

`compositor_fase4.py` solo lo importa `verify_ch0_to_ch6_scenarios.py`. **El seeder nunca lo
invoca.**

### ⚠️ Advertencia crítica: NO es un reemplazo directo

Las firmas coinciden, pero **los retornos NO**:

| | `_generate_practice_question` (`seed.py:190`) | `componer_pregunta_practica` (`compositor:76`) |
|---|---|---|
| Firma | `(modulo_id, nivel_id, fam_idx, var_idx, seed_val)` | **idéntica** |
| Retorno | Dict **listo para BD**: `fase_id`, `seccion`, `estructura_padre_id`, `operacion`, `tipo_pregunta`, `enunciado`, `respuesta_correcta`, `datos_numericos`, `explicacion_paso_a_paso`, `errores_previstos`, `requiere_subrayado`, `estado` | Dict **parcial**: `plantilla_id`, `escenario_id`, `modulo_id`, `nivel_id`, `enunciado`, `operacion_correcta`, `respuesta_correcta` |

> 🔴 **Si sustituyes la función entera, pierdes `estructura_padre_id`.** El Tomo 4 §11 lo
> marca como el bug histórico que dejó **0 aprobados** en las fases ≥5 cuando quedó en NULL.
> También perderías `explicacion_paso_a_paso` (que alimenta el Bloque de Rescate) y
> `errores_previstos` (que alimenta el feedback diagnóstico y la Capa 3 de C5.13).

### Integración correcta

El compositor aporta **enunciado, respuesta y variedad**. El seeder conserva **los campos de
BD**. Patrón:

```python
# En seed.py, junto a los demás imports
from app.fase4.compositor_fase4 import CompositorFase4

_COMPOSITOR = CompositorFase4()   # carga los 4 catálogos nuevos una sola vez


def _generate_practice_question(modulo_id, nivel_id, fam_idx, var_idx, seed_val) -> dict:
    # 1) El compositor compone y VALIDA (R1, R2, presupuestos, etiquetas)
    comp = _COMPOSITOR.componer_pregunta_practica(
        modulo_id, nivel_id, fam_idx, var_idx, seed_val
    )

    # 2) El seeder envuelve con los campos de BD que el compositor no produce
    fam_id = f"f4_m{modulo_id}_l{nivel_id}_fam_{fam_idx:03d}"
    return {
        "fase_id": FASE_DECIMALES_ID,
        "seccion": modulo_id * 100 + nivel_id,
        "estructura_padre_id": fam_id,          # ← NUNCA None (Tomo 4 §11)
        "operacion": _op_enum(comp["operacion_correcta"]),
        "tipo_pregunta": tipo_preg,              # práctica libre → NO multiple_opcion (C4)
        "enunciado": comp["enunciado"],
        "respuesta_correcta": comp["respuesta_correcta"],
        "datos_numericos": datos_num,
        "explicacion_paso_a_paso": explicacion,
        "errores_previstos": err_dict,           # desde confusiones_fase4.json
        "requiere_subrayado": False,
        "estado": StatusEnum.ACTIVO,
    }
```

### Requisitos de la integración

| # | Requisito |
|---|---|
| 1 | `estructura_padre_id` **nunca** None (Tomo 4 §11) |
| 2 | La práctica libre **no** usa `MULTIPLE_OPCION` (C4.3) |
| 3 | Las 4 variantes de una familia comparten `estructura_padre_id` — 1 original + 3 espejo |
| 4 | `errores_previstos` se puebla desde `confusiones_fase4.json`, no con texto genérico (C5.6) |
| 5 | En el DF, `errores_previstos` incluye la **respuesta aritmética sin ajustar** cuando hay redondeo por contexto (C5.13, capa 3) |
| 6 | 72 familias × 4 variantes por nivel (C7.10) |
| 7 | `catalogo_fase5.json` deja de usarse. **No lo borres**: renómbralo a `catalogo_fase5.json.deprecated` o déjalo sin referencias |
| 8 | Añade `_COMPOSITOR.verificar_pool_nivel(pool, m, n)` al validador pre-siembra, para los 12 niveles |

## ✅ Puerta de verificación del Bloque B

```bash
cd LogicaMath/backend
# 1) El compositor está conectado
grep -n "compositor_fase4\|CompositorFase4" app/fase4/seed.py

# 2) El catálogo viejo ya no se usa
grep -n "catalogo_fase5.json" app/fase4/seed.py    # debe salir vacío

# 3) La validación falla cerrado ante una violación deliberada de R2
python -c "
import sys; sys.path.insert(0,'.')
from app.fase4.compositor_fase4 import CompositorFase4
c = CompositorFase4()
try:
    c.validar_composicion({'id':'t','magnitud':'dinero','campos_requeridos':[]},
                          {'id':'e','magnitud':'longitud'})
    print('FALLO: acepto una violacion de R2')
except ValueError as e:
    print('OK, rechaza R2:', e)
"

# 4) estructura_padre_id nunca None
python -c "
import sys; sys.path.insert(0,'.')
from app.fase4.seed import _generate_practice_question as g
n = sum(1 for m in range(1,5) for l in range(1,4) for f in range(3) for v in range(4)
        if g(m,l,f,v,1000+f) .get('estructura_padre_id') is None)
print('preguntas con estructura_padre_id None:', n, '(debe ser 0)')
"
```

---

# BLOQUE C — Infraestructura de tests

## F6 · No existe `conftest.py`: los tests nunca han corrido

**Estado:** los 10 tests fallan con `fixture 'db_session' not found`. **No es una regresión** —
no existe `conftest.py` en todo el backend y el commit no lo tocó. Nunca hubo puerta de test.

**Consecuencia:** el criterio de aceptación de CH-8 (*"la suite pasa en verde"*) no detectó
ninguno de los bugs de este documento.

**Tarea:** crear `LogicaMath/backend/app/tests/conftest.py` con una fixture `db_session`
asíncrona que use `AsyncSessionLocal` de `app/db/session.py`.

```python
# LogicaMath/backend/app/tests/conftest.py
import pytest_asyncio
from app.db.session import AsyncSessionLocal

@pytest_asyncio.fixture
async def db_session():
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()   # los tests no persisten nada
```

> ⚠️ `deep_analise_pro §15.5`: si un test crea `Intento` o `ProgresoMaestria`, debe borrarlos
> en `finally`. La fixture hace `rollback`, pero verifícalo por test.

**Además:** `test_pool_integrity.py:29,47,65` filtra `fase_id.in_([1..8])` y `range(1,9)`.
Revisa que sus invariantes siguen teniendo sentido con la Fase 4 reestructurada.

## ✅ Puerta de verificación del Bloque C

```bash
cd LogicaMath/backend && python -m pytest app/tests/ -q --no-header
```

Debe pasar en verde. **Si algún test falla, arréglalo; no lo marques como `skip`.**

---

# BLOQUE D — CH-0 (no se implementó)

## F7 · Falta el bloque de precedencia en 6 documentos

**Verificado:** ninguno de los 6 documentos menciona `reestructuracion.md`.

Añade este bloque **al inicio** de cada uno, antes de cualquier norma:

```markdown
> ⚠️ **Reestructuración de la Fase 4 en curso.**
> Para todo lo relativo a la **Fase 4**, prevalece `reestructuracion.md` (raíz del repositorio).
> Las derogaciones concretas de este documento están listadas en su sección **A0**.
> Para las demás fases, este documento sigue siendo normativo sin cambios.
> *(Bloque temporal: se retira cuando CH-9 actualice este documento.)*
```

| # | Archivo |
|---|---|
| 1 | `docs/Criterios Diseno Fase/1_Documento_Rector_Pedagogico.md` |
| 2 | `docs/Criterios Diseno Fase/2_Arquitectura_Backend_y_Admin.md` |
| 3 | `docs/Criterios Diseno Fase/3_Guia_Frontend_UX.md` |
| 4 | `docs/Criterios Diseno Fase/4_Guia_TJS_Desafios.md` |
| 5 | `docs/Criterios Diseno Fase/guia_creacion_fase.md` |
| 6 | `docs/MAPA_CANONICO_FASES.md` |

> 🔴 **No modifiques ningún contenido normativo.** Solo añades el bloque.

## ✅ Puerta de verificación del Bloque D

```bash
cd "D:/Antigravity/APP_Logica_Matematicas_kids"
for f in "docs/Criterios Diseno Fase"/*.md docs/MAPA_CANONICO_FASES.md; do
  grep -q "reestructuracion.md" "$f" && echo "OK  $f" || echo "FALTA $f"
done
```

---

# BLOQUE E — Calidad del contenido

## F8 · Nombres obsoletos dentro de `fase4/`

Tras el renombrado quedaron símbolos que aún dicen `fase5` dentro de la Fase 4. Son la causa
raíz de F1 y F2, y volverán a producir el mismo error si alguien los toca sin contexto.

| Archivo | Símbolo actual | Objetivo |
|---|---|---|
| `fase4/theory_data.py:17` | `FASE5_TEORIA_DATA` | `FASE4_TEORIA_DATA` |
| `fase4/theory_examples.py:9` | `obtener_ejemplos_expandidos_fase5` | `obtener_ejemplos_expandidos_fase4` |
| `fase4/seed.py:112` | `clear_fase5_data()` | `clear_fase4_data()` |
| `fase5/theory_examples.py:6` | `obtener_ejemplos_expandidos_fase4` | `obtener_ejemplos_expandidos_fase5` |

> ⚠️ **Colisión.** `fase4/theory_examples.py` define `..._fase5` y `fase5/theory_examples.py`
> define `..._fase4`. Renombrar los dos a la vez produce un cruce transitorio.
> Usa **nombre temporal**, igual que con los `id` y los prefijos CSS:
>
> ```
> 1. fase5/theory_examples.py:  obtener_ejemplos_expandidos_fase4 → ..._tmp
> 2. fase4/theory_examples.py:  obtener_ejemplos_expandidos_fase5 → ..._fase4
> 3. fase5/theory_examples.py:  ..._tmp                           → ..._fase5
> ```
>
> Actualiza los importadores en el **mismo commit**: `fase4/seed.py:138`, `fase5/seed.py:27`,
> y los tres scripts de auditoría.

## F9 · Docstring desfasado en `seed.py`

**Archivo:** `LogicaMath/backend/app/fase4/seed.py` · **línea 8**

```
ACTUAL:    - 2.400 preguntas de desafíos (16 bloques × 150 preguntas; 15 de módulo + 1 mixto 99099).
OBJETIVO:  - 1.950 preguntas de desafíos (13 bloques × 150 preguntas; 12 de módulo + 1 mixto 99099).
```

Revisa todo el docstring de cabecera: puede tener más cifras de la estructura de 5 módulos.

## F10 · Variedad estructural insuficiente en 8 de 12 niveles

**Medición** — firma estructural `(operación, incógnita, n_datos)` de los 6 esquemas por nivel:

| Nivel | Firmas | Veredicto |
|---|---|---|
| M1N1, M1N2, M1N3, M4N3 | 4–5 | ✅ Cumple |
| M2N1, M2N2, M2N3 | **1** | ❌ 6 redacciones de una estructura |
| M3N1, M3N2, M3N3 | **1** | ❌ |
| M4N1, M4N2 | **1** | ❌ |

**Ejemplo de M2N1** — los 6 esquemas son todos `(multiplicar, producto, 2 datos)`, y solo
cambia la redacción:

> *"¿Cuánto pagó en total por los N paquetes?"* · *"¿Cuál es la masa total del cargamento?"* ·
> *"¿Cuántos usó en total?"* …

**Matiz importante:** que M2 sea siempre `multiplicar` **es correcto** — es el módulo de
multiplicación. Y la regla formal del ≤25 % por esquema **sí se cumple**. Lo que falta es
variar los otros dos ejes que C7.2 exige:

| Eje | Cómo variarlo sin salir del concepto del módulo |
|---|---|
| **`incognita`** | `a × b = ?` (producto) · `a × ? = c` (factor que falta) · verificar un resultado dado |
| **`n_datos`** | 2 · 3 (tres factores) · 3 con **un dato irrelevante** |

**Tarea:** editar `plantillas_fase4.json` para que **cada uno de los 8 niveles alcance al
menos 3 firmas estructurales distintas**. No añadas plantillas: **reescribe** las existentes
cambiando `incognita` y `n_datos`, y ajusta `marco` y `pregunta` en consecuencia.

**Verificación:**

```bash
cd LogicaMath/backend/app/fase4/data
python -c "
import json,io
pl=json.load(io.open('plantillas_fase4.json',encoding='utf-8'))
mal=[]
for m in (1,2,3,4):
    for n in (1,2,3):
        sub=[p for p in pl if p['modulo_id']==m and p['nivel_id']==n]
        f={(p['operacion_correcta'],p['incognita'],p['n_datos']) for p in sub}
        print(f'M{m}N{n}: {len(f)} firmas')
        if len(f)<3: mal.append(f'M{m}N{n}')
print('INCUMPLEN:', mal or 'ninguno')
"
```

## F11 · `overflow-y: auto` latente en el carrusel

**Archivo:** `LogicaMath/frontend/components/fase4/Fase4Styles.css` · **línea 1698**

```css
.flashcard-body {
  overflow-y: auto;      /* ← contradice T3 */
}
```

La clase **se usa**: `Fase4TheoryModal.tsx:211` → `className="f4-reading-body flashcard-body"`.

Hoy lo neutraliza `.f4-reading-body { overflow-y: hidden !important }` (línea 733), así que
**no hay bug visible**. Pero si alguien retira ese `!important`, **el scroll vuelve en
silencio** y T3 se rompe sin que nada avise.

**Tarea:** cambiar `overflow-y: auto` → `overflow-y: hidden` en `.flashcard-body`, o quitar
la clase del `className` en el TSX.

## F12 · Datos duplicados en los ejemplos guiados

**Archivo:** `LogicaMath/backend/app/fase4/theory_examples.py`

Los enunciados ponen los datos **en la prosa y en la tabla**:

```python
"enunciado": "Mía compra un libreta por R$ 3,25 y un lápiz por R$ 1,40. ¿Cuánto pagó en total?<br/>" +
             tabla_datos([("Libreta", "R$ 3,25"), ("Lápiz", "R$ 1,40")], ...)
```

No es incorrecto, pero **no logra lo que C3 buscaba**: reducir la carga de leer y extraer.

**Tarea:** dejar los importes **solo en la tabla**:

```python
"enunciado": "Mía compra una libreta y un lápiz. ¿Cuánto pagó en total?<br/>" +
             tabla_datos([("Libreta", "R$ 3,25"), ("Lápiz", "R$ 1,40")], ...)
```

> ⚠️ **Excepción C5.5: NO apliques esto al D1.** En el Desafío 1 los datos van **en la prosa
> a propósito**, porque ahí se evalúa extraerlos del texto. Esta tarea es solo para los
> ejemplos guiados y los interactivos de evocación.

---

# BLOQUE F — CH-9 (no se implementó)

## F13 · Actualizar los Tomos

`docs/` no se tocó en el commit. Ejecuta la cascada completa de `reestructuracion.md` §5:

| Acción | Destino |
|---|---|
| **A0** | Las 4 derogaciones normativas explícitas, con justificación |
| **A1** | `docs/MAPA_CANONICO_FASES.md` — intercambio 4↔5 + realinear los nombres con `SELECT id, nombre FROM fases` (hoy discrepan en la mayoría de las filas) |
| **A2** | `3_Guia_Frontend_UX.md` — T3, T4, 950×620, presupuestos, contadores por bloque |
| **A3** | `4_Guia_TJS_Desafios.md` — el más afectado: §2.3, §3, §4, §8, §10.2, §10.3, §10.4, §11, §12, §14, §15 |
| **A4** | `1_Documento_Rector_Pedagogico.md` — §4.1, §4.2–4.3, §11 + derogaciones de §3.1 y §11 |
| **A5** | `guia_creacion_fase.md` — estructura canónica y presupuestos |
| **A6** | `2_Arquitectura_Backend_y_Admin.md` — tipo `ejemplos_tjs`, validador, constante renombrada |
| **A7** | Higiene: decidir el destino de `docs/reestructuraciondefases.md` (844 KB, declarado caducable por el Tomo 4) |

**Y al terminar:** retirar el bloque temporal de F7 de los 6 documentos, y el bloque
`🚧 ACTIVE RESTRUCTURING` de `AGENTS.md`.

> 🔴 **No borres en silencio una regla derogada.** Cada derogación lleva su justificación.

---

# BLOQUE G — Fuera de alcance (inventario, no se corrige aquí)

Bugs conocidos posteriores a la Fase 4. Quedan registrados para cuando se planeen esas fases:

| # | Hallazgo |
|---|---|
| 1 | `fase5/theory_examples.py` define `obtener_ejemplos_expandidos_fase4` — nombre cruzado (F8 lo corrige solo si se hace el renombrado completo) |
| 2 | `audit_ch6_desafios.py` y `audit_master_fase4.py` importan de `app.fase5.seed` (F4 lo cubre) |
| 3 | Fases 8, 9 y 11 renombradas: verificar rutas de API y carga en `App.tsx` |
| 4 | `MAPA_CANONICO_FASES.md` desalineado con `app/seed.py` en la mayoría de las filas — **precede** a esta reestructuración |

---

# Puerta de verificación global

Antes de declarar el trabajo terminado, los cinco comandos deben pasar:

```bash
cd LogicaMath/backend

# 1) Todos los módulos importan
python -c "
import sys; sys.path.insert(0,'.')
mods=['app.fase4.seed','app.fase4.router','app.fase4.compositor_fase4',
      'app.fase5.seed','app.fase5.router','app.main']
bad=[]
for m in mods:
    try: __import__(m)
    except Exception as e: bad.append((m,type(e).__name__,str(e)[:60]))
print('ROTOS:', bad or 'ninguno')
"

# 2) El compositor está conectado y el catálogo viejo no se usa
grep -c "CompositorFase4" app/fase4/seed.py
grep -c "catalogo_fase5.json" app/fase4/seed.py    # debe ser 0

# 3) La suite pasa en verde
python -m pytest app/tests/ -q --no-header

# 4) El script de verificación corre y pasa
python -m app.fase4.verify_ch0_to_ch6_scenarios

# 5) Sin nombres obsoletos dentro de fase4
grep -rn "fase5\|FASE5" app/fase4/*.py | grep -v "^app/fase4/compositor" || echo "limpio"
```

Y en el frontend:

```bash
cd LogicaMath/frontend && npx tsc --noEmit && npm run test
```

---

# Orden de ejecución

| Paso | Bloque | Contenido | Por qué en este orden |
|---|---|---|---|
| 1 | **A** | F1, F2, F3, F4 — imports | Sin esto nada se puede probar |
| 2 | **C** | F6 — `conftest.py` | Necesitas la puerta de test **antes** de cambiar lógica |
| 3 | **B** | F5 — conectar el compositor | El pendiente de mayor valor. Ya tienes tests para respaldarlo |
| 4 | **D** | F7 — CH-0 | Barato; elimina el conflicto documental |
| 5 | **E** | F8, F9, F10, F11, F12 — calidad | F8 (renombrado) al final del bloque: toca muchos archivos |
| 6 | **F** | F13 — CH-9 | Describe el estado final; va último |

**Regla transversal:** un bloque por commit, con su puerta de verificación en verde antes de
pasar al siguiente (`deep_analise_pro §17.9`: suite completa, no solo lo que tocaste).

---

## Nota final

Los tres bugs bloqueantes del Bloque A los habría detectado **un solo comando**:

```bash
python -c "import app.fase4.seed"
```

Conviene añadir esa comprobación como puerta obligatoria antes de dar cualquier change por
cerrado. Es la lección más rentable de esta auditoría.
