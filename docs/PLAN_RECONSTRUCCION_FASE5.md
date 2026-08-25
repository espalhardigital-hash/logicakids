# Plan de Reconstrucción — Fase 5 (Fracciones, Porcentajes y Proporciones)

> **Estado:** implementada y verificada localmente el 2026-08-23. Este documento se conserva como plan e inventario histórico; el estado vigente está en [`ESTADO_IMPLEMENTACION_FASES_5_6.md`](./ESTADO_IMPLEMENTACION_FASES_5_6.md).
> **Método normativo a seguir:** [`docs/reestructuracionGeneralFases.md`](./reestructuracionGeneralFases.md) — **léelo completo antes de escribir una sola línea**. Este documento no repite ese método; lo aplica a la Fase 5 con datos concretos y define el orden de ejecución.
> **Mapa canónico:** [`docs/MAPA_CANONICO_FASES.md`](./MAPA_CANONICO_FASES.md) — `fase_id=5` = "Fracciones, Porcentajes y Proporciones" (`app/fase5/`, frontend `Fase5GameScreen.tsx`). Esto es lo correcto hoy; no re-numerar.
> **Precedente directo:** la Fase 4 (Decimales) ya pasó por exactamente este mismo problema y ya está cerrada — ver [`auditoriafase4.md`](../auditoriafase4.md), [`implementacionfase4.md`](../implementacionfase4.md), y el compositor real en `LogicaMath/backend/app/fase4/compositor_fase4.py` + `LogicaMath/backend/app/fase4/data/*.json` como referencia arquitectónica a replicar.

---

## 1. Por qué existe este documento

El usuario pidió explícitamente: **no repetir los mismos errores de tablas, numeración y nombres de CSS que ya pasaron en la Fase 4.** La Fase 5 está "destruida" porque hasta la reestructuración de Fase 4 (cerrada 2026-07-30), **Fase 5 y Fase 4 eran la misma fase con IDs distintos** — se intercambiaron los `fase_id` para que Fase 4 = Decimales y Fase 5 = Fracciones. Ese intercambio dejó exactamente el tipo de residuo que `reestructuracionGeneralFases.md` cataloga como anti-patrón #10 ("Residuo de nomenclatura cruzada"), y no se limpió porque estaba fuera del alcance de esa reestructuración (ver esa doc, §5 "Deudas cruzadas detectadas").

Este documento cierra la Etapa 0 del método (inventario de acoplamiento) con comandos y salidas reales, y traza el resto del camino (Etapas 1-8) con las decisiones específicas que la Fase 5 necesita.

---

## 2. Etapa 0 — Inventario de acoplamiento (YA EJECUTADO, con evidencia)

### 2.1. Estructura actual de `app/fase5/`

| Archivo | Líneas | Qué hace |
|---|---|---|
| `router.py` | 1119 | Endpoints FastAPI. Importa y **re-nombra** schemas de `app/fase2/schemas.py` como `Fase2X as Fase4X` (líneas 21-26) — nombres de tipos literalmente "Fase4" para servir a Fase 5. |
| `seed.py` | 1962 | Generador de preguntas. **No usa compositor**: son funciones `generate_practice_question_fase4(...)` y `generate_challenge_question_fase4(...)` que arman el enunciado con f-strings directo en el cuerpo, exactamente el patrón que Fase 4 tenía **antes** de la corrección de esta sesión. |
| `theory_examples.py` | 812 | Banco de teoría/SVG en diccionarios Python embebidos (no JSON separado). |
| `__init__.py` | 2 | Vacío. |

No existen `compositor_fase5.py`, `schemas.py`, `models.py` ni carpeta `data/` — a diferencia de `app/fase4/`, que sí los tiene.

### 2.2. Residuo textual "Fase 4" dentro de `app/fase5/` (más de 30 ocurrencias)

Confirmado por lectura directa, no por grep superficial. Ejemplos representativos (hay más, ver exploración completa):

- `seed.py`: `clear_fase4_data = clear_fase5_data` (alias), `run_fase4_seed = run_fase5_seed` (alias), `def generate_practice_question_fase4(...)`, `def generate_challenge_question_fase4(...)`, prints `"Sembrando NivelTeoria para Fase 4..."`, `"Iniciando inyección de Fase 4 en base de datos..."`, `"Fase 4 seeded successfully!"`.
- `router.py`: clases `Fase4Dashboard`, `Fase4NivelInfo`, `Fase4DesafioInfo`, `Fase4ModuloInfo`, `Fase4PreguntaParaAlumno`, `Fase4AlternativaOut`, `Fase4ContenidoLectura`, `Fase4CerrarRescate` como `response_model`; mensajes de usuario **visibles en producción** como `"¡Felicitaciones! ¡Has dominado la Fase 4 y avanzas a la Fase 5!"` y `"Debes dominar los 25 niveles de Fase 4..."`; clave de config `settings["unlockedLevels"]["fase4"]`.
- `theory_examples.py`: docstring dice "ejemplos... para cada módulo y nivel de Fase 4" sobre una función llamada `obtener_ejemplos_expandidos_fase5`.
- Frontend `Fase5Service.ts`: comentario de cabecera menciona "backend de Fase 4", clave de caché `'dashboard-f4'`, docstring `"Gradúa al alumno de Fase 4 a Fase 5"` sobre `graduateFase5()`.

**Impacto real, no cosmético**: los mensajes de graduación y bloqueo de nivel que ve el alumno **dicen "Fase 4" en la interfaz de Fase 5**. Esto no es solo deuda técnica interna.

### 2.3. Acoplamiento fuera de `app/fase5/` (comando + salida real)

```bash
grep -rn "FASE5_ID\|fase_id *= *5\|faseId: *5" --include=*.py --include=*.ts --include=*.tsx . ../frontend | grep -v "/fase5/"
```
```
./scripts/audit_fase5_deep.py:29:        WHERE p.fase_id = 5
./scripts/sync_minio_vps.py:254:        help="(Legacy) Solo figuras referenciadas por fase_id=5",
./tests/test_sync_helpers.py:69:    sql, params = build_scope_where(fase_id=5)
../frontend/components/fase_generic/faseMetadata.ts:376:  faseId: 5,
```
→ Sin sorpresas peligrosas: son scripts de auditoría/sync y un test, todos legítimamente conscientes del ID. El único hallazgo real es `faseMetadata.ts` (ver §2.5).

```bash
grep -rln "f5-" --include=*.css --include=*.tsx ../frontend | grep -v "components/fase5/"
```
```
../frontend/components/common/UXFeedbackOverlay.tsx
../frontend/dist/assets/Fase5Service-DfDrFKxN.css   (bundle compilado, no fuente)
```
→ `UXFeedbackOverlay.tsx` (componente **compartido** entre todas las fases) contiene una lista hardcodeada `c.startsWith('f4-') || c.startsWith('f5-') || c.startsWith('f6-') ...` para filtrar clases al capturar feedback visual. No es una fuga de estilos (no reutiliza definiciones CSS de otra fase), pero **sí es la clase de acoplamiento que el método prohíbe**: un componente común que necesita conocer manualmente el prefijo de cada fase. Si se agrega una fase nueva y no se actualiza esta lista a mano, el feedback visual de esa fase queda mal filtrado.

```bash
grep -rn "from app.fase5\|import app.fase5" --include=*.py . | grep -v "app/fase5/"
```
```
./app/seed.py:918:        from app.fase5.seed import run_fase5_seed          (legítimo, orquestador)
./app/tests/test_fase_endpoints_contract.py:19: from app.fase5.router import responder_fase5, Fase5ResponderPregunta   (test importa implementación interna, no solo el contrato HTTP)
```

**Decisión Gate 0 (a confirmar con el usuario antes de implementar):**
| Punto de acoplamiento | Decisión propuesta |
|---|---|
| Nombres `Fase4*` dentro de `app/fase5/` (backend + frontend) | Renombrar ahora, es la causa raíz del problema reportado |
| `UXFeedbackOverlay.tsx` con lista de prefijos hardcodeada | Renombrar prefijos, pero **no** rediseñar el mecanismo de filtrado en esta pasada — es una fase 6/7/8/9 con el mismo problema latente, se documenta como deuda compartida |
| `test_fase_endpoints_contract.py` importando `router.py` directo | Se deja — es un test, no código de producción; señalar como mejora futura opcional |
| `faseMetadata.ts` con Fase 4/5 invertidas | Corregir en esta pasada (ver §2.5) — es dato falso que puede reactivarse por error |

### 2.4. Numeración de `seccion` — evaluación de riesgo real

Fase 5 usa el **mismo esquema numérico** que Fase 4: práctica `modulo*100+nivel` (101-403), desafíos `modulo*1000+11/12/13` (1011-4013). A primera vista parece colisión, pero **no lo es**: toda query filtra también por `fase_id`, y `fase_id` se respeta consistentemente en el código actual. Confirmado contra la BD real (ver §2.6): no hay filas de Fase 4 y Fase 5 mezcladas.

**No es necesario cambiar el esquema de numeración.** Es una coincidencia de patrón, no un bug de datos. Si se quiere eliminar la ambigüedad visual para quien lea la tabla `preguntas` directamente, es una mejora cosmética opcional (ej. prefijar `seccion` con el `fase_id`), no un requisito de esta reconstrucción.

### 2.5. `faseMetadata.ts` — datos invertidos (confirmado, `LogicaMath/frontend/components/fase_generic/faseMetadata.ts`)

- Línea 246-248: `FASE_4 = { faseId: 4, nombre: 'Fracciones, Porcentajes y Proporciones', ... }` ← **falso**, `fase_id=4` es Decimales.
- Línea 373-381: `FASE_5 = { faseId: 5, nombre: 'Geometría Plana y Medidas', ... }` ← **falso**, `fase_id=5` es Fracciones (y Geometría es `fase_id=6`).

Ya estaba documentado como deuda conocida en `reestructuracionGeneralFases.md` §5. Actualmente estas entradas **no se leen** (fases 3-8 sirven contenido dinámico desde el backend, no desde este archivo estático), así que el riesgo es de reactivación futura, no de bug activo hoy. Se corrige en esta pasada porque es barato y elimina una mina terrestre.

### 2.6. Estado real del contenido (BD local, evidencia ejecutada)

```sql
SELECT seccion, count(*) total, count(DISTINCT enunciado) unicas
FROM preguntas WHERE fase_id = 5 GROUP BY seccion ORDER BY seccion;
```
Resultado: práctica libre (101-403, 13 secciones) con **58-60/60 únicas** por sección — sano, sin el colapso que tuvo Fase 4. Desafíos (x011-x013, 12 secciones) con **25-30/30 únicas** — peor, con overlaps puntuales:

```sql
-- intersección de enunciados entre secciones de Fase 5
 sec1 | sec2 | coincidencias
 1011 | 1013 | 8
 1012 | 1013 | 7
 1011 | 1012 | 3
 4011 | 4013 | 2
 4011 | 4012 | 1
```

**Diagnóstico**: la Fase 5 **no tiene el colapso catastrófico** que tuvo el Desafío Final de Fase 4 (que era 100% idéntico entre módulos). Tiene una versión más leve del mismo problema estructural — el generador de `seed.py` (mismo patrón `q_idx`-only, sin compositor) ya muestra fugas de variedad puntuales dentro del Módulo 1 y el Módulo 4. Es exactamente el tipo de bug que ese patrón produce tarde o temprano; en Fase 5 recién empieza a notarse.

También: el docstring de `scripts/audit_fase5_deep.py` dice "9,600 preguntas" pero la BD local tiene **1.140** — desalineado, hay que verificar si es un seed parcial, una versión vieja del generador, o el docstring quedó desactualizado. No asumir: correr `python -m app.fase5.seed` (o el entrypoint que corresponda) contra una BD limpia y contar de nuevo antes de diseñar el volumen objetivo.

### 2.7. Lo que SÍ está bien (para no rehacer trabajo que no hace falta)

- **Frontend visual**: los 18 componentes en `components/fase5/` (`Fase5GameScreen.tsx`, `PizzaFractionVisualizer.tsx`, `RatioGridVisualizer.tsx`, etc.) tienen nombres coherentes con el tema real (fracciones/porcentajes/razones) y **no** tienen residuo textual de "fase4" ni de otro dominio. La limpieza es un problema de backend + `Fase5Service.ts`, no de UI.
- **Tema pedagógico**: `theory_examples.py` ya cubre 4 módulos coherentes con el nombre canónico: Fracción Visual, Fracción de Cantidad, Porcentajes Rápidos y Promedios, Razón y Mezclas. No hace falta rediseñar el contenido pedagógico desde cero, solo reconstruir el motor que lo genera y limpiar el nombrado.
- **Higiene mecánica de datos**: 0 placeholders vacíos, 0 URLs locales filtradas, 0 caracteres corruptos, conteo de alternativas correcto (`scripts/audit_fase5_deep.py`, corrido contra BD real).

---

## 3. Camino recomendado (Etapas 1-8 de `reestructuracionGeneralFases.md`, aplicadas a Fase 5)

No repito la explicación de cada etapa — está en el documento madre. Acá solo lo específico de Fase 5.

**Etapa 1 (arnés de tests, en rojo):** Adaptar `test_fase4_vocabulario.py` como plantilla — mismo tipo de invariantes (respuesta derivada de la misma fórmula, toda plantilla con escenario compatible, `estructura_padre_id` nunca nulo, vocabulario prohibido de otras fases ausente, determinismo semilla→pregunta). Antes de escribir el test, correr `pytest --collect-only` sobre todo el proyecto y confirmar que colecciona sin errores de import (repetir el chequeo, no asumir que sigue en verde).

**Etapa 2 (piloto):** Elegir **un** módulo de Fase 5 (sugerido: Módulo 1, "La Fracción Visual", nivel 1) para validar el patrón antes de extender a los otros 3 módulos × 3-4 niveles.

**Etapa 3-5 (compositor):** Replicar la arquitectura de `compositor_fase4.py` + `data/*.json`:
- `compositor_fase5.py` con `plantillas_fase5.json` + `escenarios_fase5.json` (mismo contrato: `campos_requeridos`, validación de magnitud fail-closed, `validar_composicion`).
- Módulos/magnitudes de Fase 5 son distintos de Fase 4 (fracciones puras, fracción-de-cantidad, porcentaje, razón/proporción) — el contrato de magnitud tiene que reflejar **estas** reglas propias, no copiar las de decimales. Definir por escrito qué combinaciones son válidas antes de generar plantillas (mismo error que costó caro en Fase 4: "sumar peras con manzanas").
- Los desafíos (D1/D2/DF/DM) deben conectarse al compositor desde el primer commit, no como una fase 2 posterior — ese fue exactamente el punto donde Fase 4 se rompió (compositor conectado solo a práctica, desafíos con enunciados hardcodeados hasta el final).
- Verificación de conexión real, no de existencia de archivo: `grep -n "_COMPOSITOR\|componer_pregunta" app/fase5/seed.py` debe dar resultado antes de dar por conectado.

**Etapa 3.1 (variedad narrativa — bug crítico confirmado en producción de Fase 4, 2026-08-09, NO repetir):** Al generar los textos alternativos por plantilla (equivalente a `marcos_alternativos` / `enrich_templates_36.py` de Fase 4), 31/72 plantillas de Fase 4 quedaron con marcos narrativos que **ocultaban una variable que la fórmula necesitaba** para calcular la respuesta (ej. una plantilla con `formula="a*b"` cuyo texto alternativo solo narraba `n_cant` y `a`, en un patrón de frase escrito para una fórmula distinta del mismo grupo). El síntoma en producción, reportado por un alumno real con capturas de pantalla: el recuadro de datos (SVG) mostraba dos filas con la misma etiqueta ("Medida unitaria" repetida), una de ellas con un valor que **nunca aparecía en el enunciado**, y la "respuesta correcta" almacenada no se podía deducir del texto que el alumno leía — se derivaba de una variable fantasma. Causa raíz: el generador de variantes agrupaba varias fórmulas relacionadas-pero-distintas bajo un mismo texto base, escrito solo para la más simple del grupo.
  - **Regla obligatoria para Fase 5**: cada grupo de variantes narrativas debe generarse por la clave exacta `(magnitud, formula)`, nunca por una agrupación aproximada o "suficientemente parecida". Antes de aceptar un texto de variante como válido, verificar programáticamente que **todas** las variables que la fórmula usa (`re.findall` sobre la fórmula, filtrado a los tokens numéricos reales) aparecen como placeholder en el texto — si falta una, es un bug, no una libertad de redacción.
  - Si dos plantillas comparten magnitud pero tienen fórmulas distintas (por ejemplo `a*b` vs `a/n_cant`), **no** deben compartir el mismo banco de frases narrativas aunque el tema (dinero, masa, longitud...) sea el mismo.
  - Si la representación visual (SVG/tabla) muestra más de un dato con el mismo rol semántico (ej. dos "medidas", dos "precios"), las etiquetas deben diferenciarse (`Medida A`/`Medida B`, no dos veces "Medida unitaria") — cuidado con el presupuesto de caracteres de las etiquetas SVG (`app/utils/svg_figuras.py::tabla_datos()` en Fase 4 tiene un límite duro de 15 caracteres por etiqueta; verificar si Fase 5 reutiliza el mismo helper o tiene el suyo).
  - Este chequeo debe formar parte del arnés de tests/auditoría desde la Etapa 1, no descubrirse después con un alumno real en producción — replicar el chequeo `[formula_oculta]` de `scripts/audit_fase4_narrativas.py` (línea ~85-93) como parte de `scripts/audit_fase5_narrativas.py` (o el nombre equivalente) antes de generar el volumen final de plantillas.

**Etapa 5.1 (limpieza de nombrado, específica de Fase 5):** Renombrar sistemáticamente todo lo catalogado en §2.2 y §2.3: `Fase4X` → `Fase5X` en `router.py`, funciones `_fase4` → `_fase5` en `seed.py`, mensajes de usuario visibles, comentarios/docstrings, `Fase5Service.ts`. Un solo commit dedicado a esto, separado de los cambios de contenido, para que sea revisable en un diff limpio.

**Etapa 8 (cierre):** Además de lo que pide el método general, confirmar específicamente:
- Conteo de preguntas post-reconstrucción documentado y justificado (resolver la discrepancia 1.140 vs 9.600 de §2.6).
- Re-correr el chequeo de unicidad de §2.6 contra la BD ya reconstruida: 0 coincidencias cruzadas entre secciones de Fase 5.
- Re-correr `scripts/audit_fase5_deep.py` (higiene mecánica) — debe seguir en verde.
- `docs/DISENO DE FASES/fase4.md` y `fase5.md` están cruzados en su nombre de archivo respecto al contenido que describen (ver Exploración, punto 7) — corregir o al menos anotar claramente al cierre, para no confundir a la próxima fase que se reconstruya.

---

## 4. Decisiones que necesita el humano antes de arrancar la implementación

1. **Alcance del renombrado**: ¿renombrar también `UXFeedbackOverlay.tsx` para que no dependa de una lista hardcodeada de prefijos por fase (arreglo de raíz), o solo actualizar la lista con el prefijo correcto de Fase 5 (parche, deuda documentada)? Recomendación: parche ahora, arreglo de raíz como tarea aparte que toque las 9 fases a la vez.
2. **Volumen objetivo de preguntas**: la discrepancia 1.140 vs "9.600" del docstring necesita resolverse con una cifra objetivo explícita antes de diseñar el compositor (cuántas familias × variantes × niveles).
3. **`faseMetadata.ts`**: ¿corregir los datos invertidos ahora (barato, cierra un riesgo latente) o dejarlo documentado como deuda ya que hoy no se lee? Recomendación: corregir ahora, es un cambio de una tabla de constantes, no de lógica.
4. **Docs cruzados** (`fase4.md`/`fase5.md` con contenido intercambiado): ¿renombrar los archivos o dejarlos como están y solo anotar la inconsistencia? Recomendación: renombrar, cuesta un `git mv`.

---

## 5. Prompt listo para la implementación (para otra sesión/LLM)

```
Vas a reconstruir la Fase 5 de LogicaKids Pro (fase_id=5, "Fracciones, Porcentajes y
Proporciones", app/fase5/). Antes de escribir código:

1. Leé completo docs/reestructuracionGeneralFases.md — es el método normativo, escrito
   específicamente a partir de los errores reales de la reestructuración de Fase 4.
2. Leé completo docs/PLAN_RECONSTRUCCION_FASE5.md — ya tiene la Etapa 0 (inventario de
   acoplamiento) ejecutada con comandos y salidas reales contra este repo. No la repitas
   desde cero; verificá que siga vigente y seguí desde la Etapa 1.
3. Usá LogicaMath/backend/app/fase4/compositor_fase4.py y su carpeta data/*.json como
   referencia arquitectónica directa — es el patrón ya validado en producción.

Reglas no negociables (del método, repetidas acá porque son las que más costaron en
Fase 4):
- Un cambio a la vez, con verificación ejecutada entre cambios. No declares nada
  "completo" sin pegar el comando y su salida real.
- La respuesta correcta de cada pregunta tiene que derivarse de la MISMA fórmula y
  valores que arman el enunciado — nunca dos generadores paralelos.
- Cada texto narrativo alternativo de una plantilla debe mostrar TODAS las variables que
  su fórmula usa (verificarlo programáticamente, no a ojo). Un bug real de este tipo llegó
  a producción en Fase 4 (31/72 plantillas, ver Etapa 3.1 de PLAN_RECONSTRUCCION_FASE5.md)
  y solo se detectó por un reporte de un alumno con captura de pantalla, meses después de
  desplegado. No repetir: agrupar variantes narrativas por (magnitud, fórmula) exacta,
  nunca por aproximación temática.
- Los desafíos se conectan al compositor desde el primer commit, no como paso final.
- Un generador que falla debe fallar ruidosamente (raise), nunca devolver contenido de
  respaldo silencioso.
- Verificá conexión real de cada pieza nueva (que el seeder la invoque), no su
  existencia en disco.
- Antes de cerrar: pytest en verde, auditoría de unicidad contra la BD real (0
  coincidencias entre secciones), scripts/audit_fase5_deep.py en verde, y un reseed
  ejecutado dos veces consecutivas con conteos idénticos.

Antes de implementar, las decisiones de la sección 4 de PLAN_RECONSTRUCCION_FASE5.md
tienen que estar confirmadas por el usuario — no las asumas.
```

---

## 6. Lo que este documento NO incluye (a propósito)

- No rediseña el contenido pedagógico de los 4 módulos — ya está razonablemente definido en `theory_examples.py` y es coherente con el nombre canónico.
- No define las plantillas/escenarios concretas del futuro `compositor_fase5.py` — eso es Etapa 3, posterior a las decisiones de la sección 4.
- No toca Fase 6-9, aunque comparten el mismo componente `UXFeedbackOverlay.tsx` con el mismo acoplamiento latente — queda anotado como deuda compartida, no como parte de esta reconstrucción.
