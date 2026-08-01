# Traspaso operativo: cambios pendientes de Fase 4

Fecha del traspaso: 2026-08-01 (reestructurado — versión anterior fechada 2026-07-31)
Repositorio: `D:\Antigravity\APP_Logica_Matematicas_kids`
Rama observada: `producion`
Commit base observado: `ba7ac96 Version 0.0.9-8 Eliminar residuos de la fase 0` (sin commit nuevo — el trabajo descrito abajo vive sin comitear en el worktree, por instrucción explícita del usuario de no comitear sin pedirlo)

## 0. Qué cambió respecto a la versión anterior de este documento

La versión anterior traía las 3 propuestas OpenSpec (`fase4-content-feedback-correctness`, `fase4-ux-contract-alignment`, `fase4-legacy-debt-verification`) con 0 tareas implementadas. Desde entonces se ejecutó trabajo real, verificado con evidencia ejecutable (no solo prosa), sobre los Cambios 1 y 3, y una parte del Cambio 2. **Este documento ya no repite lo que está hecho** — lo resume en la §1 con su evidencia, y deja el detalle completo solo para lo que falta.

**No reimplementar ni revertir lo de la §1.** Verificar primero con los comandos indicados antes de asumir que algo sigue pendiente.

## 1. Ya completado — resumen con evidencia

### 1.1 Cambio 1 (`fase4-content-feedback-correctness`) — Etapas B, C y D completas

**Bug crítico corregido — feedback cognitivo muerto.** `errores_previstos` se guardaba como `{texto: feedback}` plano; el router lee `errores_previstos["respuestas_erroneas"]` (lista de `{valor, tipo_error, feedback}`). La clave nunca coincidía: `.get("respuestas_erroneas", [])` devolvía `[]` siempre, para las 3.456 preguntas de práctica y las preguntas numéricas de desafío (DF). Se agregó `_construir_errores_previstos()` en `seed.py` y se aplicó en las 6 rutas donde se generaba mal. Verificado con una simulación exacta del bucle del router (`test_feedback_llega_al_alumno_simulando_la_logica_del_router`).

**Bug corregido — `hasattr` mal usado en `router.py`** (línea ~1042): comparaba el valor del enum (`"calculo"`) contra nombres de atributo (`"CALCULO"`), así que siempre clasificaba como `CALCULO`. Cambiado a `try/except ValueError` sobre `TipoErrorEnum(...)`.

**Bug corregido — D2 de división afirmaba "es entero" sin comprobarlo** (`seed.py`, módulo 3, `des_type==12`): con `div` en {4,5·6,0·7,5·9,0} y `divisor` en {0,5·1,0·1,5}, hay combinaciones (ej. 4,5÷1,0=4,5) donde el cociente **no** es entero. Ahora deriva `es_entero` del cociente real con ambas ramas coherentes. 0 inconsistencias en barrido completo (`test_d2_division_es_entero_coincide_con_el_calculo_real`).

**Puerta pedagógica de la §6.2 (antigua) — RESUELTA con evidencia, no es una decisión abierta.** Se verificó contra `escenarios_fase4.json` (el catálogo real, no el plan histórico) la distribución de magnitudes por módulo:

```
(1,'dinero') 8   (1,'longitud') 5   (1,'masa') 5   (1,'temperatura') 2
(2,'dinero') 12  (2,'longitud') 5   (2,'masa') 3
(3,'dinero') 10  (3,'longitud') 5   (3,'masa') 5
(4,'longitud') 20
```

Conclusión verificada: **masa SÍ está en alcance para los Módulos 1-3** (junto a dinero, longitud y temperatura). **Volumen y superficie tienen 0 filas en cualquier módulo** — nunca estuvieron en alcance, se purgaron por completo. **El Módulo 4 es puro-longitud** (20/20 escenarios). No reabrir esta pregunta sin evidencia nueva contra el catálogo real.

**Barrido exhaustivo (Etapa D) convertido en test mantenido**, no script one-shot: `LogicaMath/backend/tests/test_fase4_barrido_completo.py` genera las 5.406 preguntas reales (3.456 práctica + 1.950 desafíos) y falla ante excepción, placeholder, respuesta vacía, alternativas duplicadas, cantidad de correctas ≠ 1, o `estructura_padre_id` nulo. Incluye test de determinismo (misma semilla → misma pregunta).

**Comando de verificación:**
```powershell
cd LogicaMath\backend
python -m pytest tests\test_fase4_feedback_logico.py tests\test_fase4_barrido_completo.py tests\test_fase4_vocabulario.py -v
```
Estado esperado: 33 tests, todos `PASSED`.

### 1.2 Cambio 3 (`fase4-legacy-debt-verification`) — Etapas A, B y C completas

**Inventario ejecutado con evidencia real** (búsqueda estática + seed + BD real + frontend), no solo prosa:

| Elemento | Consumidores (repo completo) | Decisión | Evidencia |
|---|---|---|---|
| `app/fase4/theme.py` | 0 | **Eliminado** | `grep -rln` repo completo, 0 hits |
| `app/fase4/svg_helpers.py` | 0 (shim `from app.utils.svg_figuras import *` que nadie importaba) | **Eliminado** | ídem |
| `app/fase4/audit_master_fase4.py` | 0 (auditaba rutas de `components/fase5/`, residuo pre-swap) | **Eliminado**, reemplazado por la suite de regresión mantenida | ídem |
| `app/fase4/verify_ch0_to_ch6_scenarios.py` | 0 (mismo problema, cambios CH-0 a CH-6 ya cerrados) | **Eliminado** | ídem |
| `app/fase4/data/catalogo_fase5.json` | 0 (solo un comentario lo mencionaba) | **Eliminado** | ídem |
| 11 clases Pydantic `Fase5*` en `schemas.py`/`router.py` | Los 7 endpoints reales de Fase 4 + `tests/test_fase4_integrity_progression.py` (import corregido tras el rename) | **Renombradas a `Fase4*`** (26+16 ocurrencias) | `grep -rln "Fase5"` repo completo → 0 hits tras el rename |
| `subrayado_tokens` / `constructor_soluciones_chained` | 0 en seed/compositor/DB local (confirmado: `SELECT tipo_pregunta, count(*) FROM preguntas WHERE fase_id=4` → solo `MULTIPLE_OPCION` y `RESPUESTA_NUMERICA`) | **NO eliminado — decisión deliberada, ver §2.1** | conteo real contra BD local |

**Lección aprendida durante la ejecución, dejarla anotada:** al renombrar `Fase5*`→`Fase4*`, la búsqueda inicial (`grep` en `app/`) no encontró consumidores externos, pero `tests/test_fase4_integrity_progression.py` (el test del Cambio 0, ya aprobado 18/18) sí importaba `Fase5CerrarRescate`. Se detectó porque se corrió la suite **completa** después del rename y falló la colección — no antes de renombrar. **Siempre correr la suite completa del repo tras un rename, nunca solo el paquete tocado.**

**Comando de verificación:**
```powershell
cd LogicaMath\backend
python -c "from app.fase4 import router as r; print('OK', len(r.router.routes), 'endpoints')"
python -m pytest tests\ app\tests\ -q --ignore=tests\test_scripts_config.py
```
Estado esperado: import OK con 7 endpoints; suite en verde salvo los 2 fallos preexistentes de conectividad a BD (`test_pool_integrity.py`, `test_fase_endpoints_contract.py` — confirmados con `git stash` como anteriores a este trabajo, no causados por él).

### 1.3 Corrección de un error propio durante la sesión — dejar como caso de estudio

Un primer intento de "limpieza de teoría" (antes de verificar el catálogo real) sobre-corrigió 3 ejemplos guiados en `theory_examples.py` (Módulos 2 y 3), quitando "harina/kg" y reemplazándolo por longitud, asumiendo que masa estaba prohibida en toda la Fase 4. **Esto fue un error**: se revirtió al confirmar contra `escenarios_fase4.json` que masa sí está en alcance para Módulos 1-3. El test `test_teoria_sin_magnitudes_ajenas_a_fase4` quedó corregido para prohibir masa/kg/harina/peso **solo en el Módulo 4** (puro-longitud), y prohibir volumen/superficie/litro en **todos** los módulos (0 filas en el catálogo, en cualquier módulo). Si el siguiente modelo va a tocar teoría/ejemplos de nuevo: **verificar primero contra `escenarios_fase4.json`, nunca asumir el alcance de memoria ni desde un plan histórico** (`docs/reestructuraciondefases.md` describe una versión anterior del alcance y no es la fuente de verdad).

### 1.4 Fuga de dominio encontrada en vivo, corregida

`LogicaMath/frontend/components/map/PhaseMapScreen.tsx` (tarjeta de Fase 4 en el mapa) describía la fase como *"conversión de unidades de longitud, volumen y superficie"* — detectado navegando la app real, no por grep. Corregido a *"Operaciones con decimales y conversión de unidades de longitud"*.

### 1.5 Verificación manual en vivo — hecha por el usuario, parcial

El usuario probó personalmente en `http://localhost:3000` con la cuenta admin (`amilcar@gmail.com`, desbloquea todas las fases sin progresión):
- **Cero scroll en la primera pantalla probada: PASS**, confirmado por el usuario ("funciona perfectamente").
- Encontró en una captura real una pregunta de desafío D1 (Módulo 3, sección 3011) con el encabezado mostrando "NIVEL 11" en vez de "Desafío 1". **Confirmado como bug real y corregido** — ver §1.6.

### 1.6 Corregido tras la verificación del usuario — bug de rotulado del encabezado

`Fase4GameScreen.tsx` renderizaba `NIVEL {nivelId}` de forma incondicional en el badge del encabezado (`f4-badge-level`), pero en desafíos `nivelId` codifica el tipo de desafío (11/12/13/99), no un nivel real — el Módulo 3 solo tiene 3 niveles, así que "NIVEL 11" era una confusión real para el alumno. Se agregó `headerLevelLabel` (memo) que muestra "DESAFÍO 1/2/FINAL" o "MIXTO" cuando `isChallenge`, y "NIVEL N" solo en práctica. Verificado con `tsc --noEmit` (0 errores) y build de producción.

### 1.7 Cambio 2 §3.3-3.4 (marco decorativo del SVG) — implementado con opt-in seguro, sin tocar fases hermanas

Se agregó un parámetro `marco: bool = True` a `_svg_container()`, `tabla_datos()`, `escalera_unidades()` y `diagrama_conversion()` en `app/utils/svg_figuras.py`. **El default no cambió** (`True` = mismo comportamiento de siempre, para las fases 5/6/7 que comparten estas funciones). Se pasó `marco=False` solo en los llamadores de Fase 4: `compositor_fase4.py::_figura_svg()` (usado por práctica y por el D1 vía `comp_d1`) y las dos `tabla_datos(...)` de los bloques DF en `seed.py`. Verificado con un test directo que confirma que el default sigue con `border:2px solid` y que `marco=False` lo quita.

### 1.8 Cambio 3 §2.3 (retirar `constructor_soluciones_chained`/`subrayado_tokens`) — ejecutado

Con autorización explícita del usuario para asumir el riesgo sin poder probar el flujo en un navegador en vivo (el panel de navegador de esta sesión dejó de componer frames de forma estable — ver §1.9), se retiró el código muerto:

- **Backend** (`router.py`): eliminada la rama `elif tipo_pregunta == "constructor_soluciones_chained":` de la validación de respuesta (~15 líneas) y el bloque completo de integración `IntentoPregunta`/`IntentoPaso` (~50 líneas). `paso_aprobado`/`valor_paso1_congelado` quedan siempre `None` (antes solo se asignaban dentro de la rama eliminada, así que el comportamiento real no cambia). Las tablas `IntentoPregunta`/`IntentoPaso` **no se tocaron** — Fase 2 las sigue usando activamente.
- **Frontend** (`Fase4GameScreen.tsx`): eliminados los 8 puntos de ramificación (142 líneas totales, incluido un bloque JSX completo de ~130 líneas para el flujo de pasos encadenados y el "fallback" de `subrayado_tokens`).
- **Tipos**: `Fase4Types.ts` y `schemas.py` ya no declaran esos dos valores de `tipo_pregunta`.

Verificado: `python -c "from app.fase4 import router"` OK con 7 endpoints, suite backend 64/64, `tsc --noEmit` 0 errores, frontend 46/46 tests, build de producción exitoso (el chunk de `Fase4GameScreen` bajó de tamaño). **No verificado**: el flujo real de envío de respuesta en un navegador — la suite existente no ejercita esta pantalla interactiva punto a punto. Si el siguiente modelo tiene Playwright funcional, correr el flujo completo de `multiple_opcion` y `respuesta_numerica` en Fase 4 como primera prioridad, antes de asumir que esto quedó perfecto.

### 1.9 Limitación de entorno encontrada — panel de navegador sin composición de frames

Durante esta sesión, el panel de navegador conectado dejó de renderizar frames de forma estable a mitad de una verificación en vivo (login como admin, medición DOM) — mismo error desde el inicio ("Browser pane is not displayed, so the page is not compositing frames"), no algo introducido por este trabajo. `get_page_text`/`read_page` funcionaron para estados simples (confirmar que un texto cambió tras reconstruir el contenedor) pero no de forma confiable para flujos con estado async (login, redirecciones). Si el siguiente modelo tiene un navegador funcional, no asuma que esta limitación persiste — puede ser específica de esa sesión.

## 2. Decisiones tomadas que el siguiente modelo debe respetar (o reabrir explícitamente con el usuario)

### 2.1 `constructor_soluciones_chained` / `subrayado_tokens` — RETIRADOS (ver §1.8)

Ya no es una decisión pendiente. Se retiraron con autorización explícita del usuario, sin verificación en navegador del flujo de envío de respuesta (ver §1.8 y §1.9 para el detalle y la limitación reconocida). **Pendiente real:** si el siguiente modelo tiene Playwright/navegador funcional, verificar en vivo que `multiple_opcion` y `respuesta_numerica` siguen funcionando correctamente en Fase 4 tras esta remoción — es la única prueba que faltó.

### 2.2 Marco decorativo del SVG — RESUELTO con opt-in seguro (ver §1.7)

Ya no es una decisión pendiente del usuario. Se implementó un parámetro `marco: bool` (default `True`, sin cambiar el comportamiento de ninguna fase hermana) en las 4 funciones de `svg_figuras.py`, y se pasó `marco=False` solo en los llamadores de Fase 4. Verificado a nivel de código que el default no cambió. **Pendiente real:** confirmación visual en navegador de que las figuras de Fase 4 se ven bien sin el marco (no solo que el atributo SVG cambió) — no se pudo hacer por la limitación de §1.9.

## 3. Reglas obligatorias para el siguiente modelo (sin cambios respecto a la versión anterior)

Antes de editar:

1. Leer `AGENTS.md`.
2. Leer la Parte I de `RULES AGENTES/deep_analise_pro.md`.
3. Para estos cambios cargar también las secciones 6, 7, 8, 9, 10 y 11 del manual.
4. Leer `docs/Criterios Diseno Fase/5_Criterios_Teoria_Ejemplos_y_Visuales.md` para teoría, ejemplos, SVG y cero scroll.
5. Leer `docs/reestructuracionGeneralFases.md` — método de reestructuración, anti-patrones encontrados en esta fase, no repetirlos.
6. Usar la skill `openspec-apply-change` y leer todos los `contextFiles` devueltos por OpenSpec.
7. Ejecutar **un solo cambio a la vez** y marcar cada tarea únicamente después de obtener evidencia.

Invariantes que no se pueden debilitar:

- Fase 4 conserva 25 bloques canónicos y gradúa únicamente a Fase 5.
- El servidor deriva fase/sección desde la pregunta y aplica bloqueos antes de crear progreso.
- Los GET de Fase 4 son de solo lectura; el reinicio continúa siendo POST explícito.
- No se borra progreso, intento histórico ni pregunta con referencias sin snapshot, estrategia y aprobación.
- No se altera la teoría o los ejemplos visualmente aprobados salvo un caso medido o una contradicción pedagógica aprobada.
- Cero scroll significa contenido medido y visible; `overflow:hidden` no es evidencia.
- No se eliminan símbolos, ramas o archivos por su nombre: se prueban productores, consumidores, datos e imports dinámicos **en todo el repositorio, no solo en el paquete que se está tocando** (ver §1.2, la lección del rename).
- Masa es una magnitud válida en los Módulos 1-3 de Fase 4; no es deuda ni fuga de dominio (ver §1.1). Solo volumen, superficie y (dentro del Módulo 4) masa/dinero están prohibidos.
- Toda afirmación de finalización debe tener comando, resultado y artefacto reproducible — nunca solo prosa.

## 4. Lo que falta — único trabajo real pendiente

Todo lo de esta sección requiere **navegador real** (Playwright o manual) contra el stack local. Nada de esto es verificable por grep o por generación aislada en Python.

### 4.0 Confirmado en vivo por el usuario en dos rondas — funcionalmente cerrado

El usuario probó manualmente en `http://localhost:3000` tras los cambios de §1.6-1.8, primero de forma general y luego con una segunda ronda de pruebas manuales adicionales, y confirmó ambas veces que **Fase 4 funciona bien**. Esto cubre el punto más crítico que quedaba abierto — que responder preguntas (`multiple_opcion` y `respuesta_numerica`) sigue funcionando después de retirar el código muerto de `constructor_soluciones_chained` de la función de envío de respuesta en `router.py`, el encabezado del desafío y el marco del SVG.

**Estado: funcionalmente cerrado.** No es necesario repetir estas pruebas salvo que aparezca un síntoma concreto nuevo. Lo que queda (abajo, §4.1-§4.2) es exhaustividad formal — matriz completa de medición, infraestructura Playwright y cierre/archivado de OpenSpec — no corrección de bugs pendientes.

### 4.1 Cambio 2 — Etapas A, B, C, D, E completas (ninguna tarea con evidencia todavía)

Ruta: `openspec/changes/fase4-ux-contract-alignment/`

**Prompt inicial:**
```text
Implementa el cambio OpenSpec fase4-ux-contract-alignment. Los Cambios
fase4-integrity-progression y fase4-content-feedback-correctness ya están
completos (ver docs/HANDOFF_CAMBIOS_PENDIENTES_FASE4.md §1.1). Lee ese
documento completo antes de empezar, y todos los contextFiles del cambio.
No rediseñes teoría o ejemplos ya aprobados. El stack local ya está arriba
(docker ps) y Fase 4 ya está resembrada con el contenido corregido — no
necesitas resembrar salvo que cambies contenido. Usa la cuenta admin
(amilcar@gmail.com) para saltarte el bloqueo de progresión y llegar directo
a Fase 4.
```

**Tareas pendientes (17/17, ninguna con evidencia):**

- **1.2-1.3**: pruebas rojas para requeridos 12/12/10/15, secuencia D1→D2→DF, matriz de casos visuales máximos (teoría, diccionario, ejemplo, práctica, espejo, D1/D2/DF/mixto) en 950×620 y 1024×768.
- **2.1-2.4**: confirmar que el DTO de pregunta trae `cantidad_requerida`/`porcentaje_aprobacion`/`errores_tolerados`/`tiempo_default_segundos` efectivos (Network tab); que el frontend no duplica estos cálculos con defaults propios; que un error de red en responder/cerrar-rescate/reiniciar/graduar se ve como error visible, no como avance silencioso.
- **3.1-3.4**: marco decorativo ya implementado con opt-in seguro (§1.7/§2.2) — falta solo la confirmación **visual** de que Fase 4 se ve bien sin marco y que Fase 5/6 conservan el suyo (§4.0 punto 3); confirmar que todo SVG de desafío mide ≤140 px y no revela la respuesta.
- **4.1-4.3**: medición DOM real (Playwright o consola del navegador) de `scrollHeight`/`clientHeight`/bounding boxes en la matriz completa de 1.3, no solo la primera pantalla ya confirmada por el usuario (§1.5).
- **5.1-5.3**: pruebas de componentes/servicio, build de producción, prueba de una fase hermana consumidora de `svg_figuras.py` para descartar regresión, capturas + mediciones guardadas en `verification-evidence.md`.

**Script de medición ya usado y validado con el usuario** (pegar en consola del navegador, F12):
```javascript
(() => {
  const el = document.querySelector('.f4-theory-modal, .f4-question-card, .f4-game-container') || document.body;
  console.log('scrollHeight:', el.scrollHeight, '| clientHeight:', el.clientHeight,
              '| ¿hay overflow real?:', el.scrollHeight > el.clientHeight);
  console.log('bounding box:', el.getBoundingClientRect());
})();
```

**Criterio de salida:** 17/17 con evidencia; todos los casos máximos caben en 950×620 y 1024×768; SVG de desafío ≤140 px sin marco decorativo ni revelación (o decisión explícita del usuario de mantener el marco); fase hermana verificada sin regresión; `openspec.cmd validate fase4-ux-contract-alignment --strict` pasa.

### 4.2 Cambio 3 — Etapa D (infraestructura de pruebas) y Etapa E (cierre), 5 de 20 tareas restantes

Ruta: `openspec/changes/fase4-legacy-debt-verification/`

Las Etapas A, B y C (tareas 1.1 a 3.3) ya están hechas — ver §1.2. Falta:

**Etapa D — infraestructura de pruebas (tareas 4.1-4.4):**
- Corregir los Playwright de Fase 4 para que declaren/inicien su propio servidor, sin depender de estado manual ni de `reload=true` destructivo.
- Integrar esas pruebas en los comandos estándar del repo (no dejarlas como script manual sin documentar).
- Reemplazar cualquier verificación de CSS por texto con medición DOM real, y demostrar que el auditor **falla** ante un fixture deliberadamente recortado (para probar que el auditor mismo funciona).

**Etapa E — cierre del programa (tareas 5.1-5.5):**
- Suite completa (backend + frontend + typecheck + build + E2E) desde entorno limpio.
- Seed efímero + recorrido autenticado real hasta la graduación a Fase 5.
- Verificar rol administrador y una fase hermana (no solo Fase 4).
- Inspección perceptual desktop/tablet con capturas.
- Diff final: confirmar que ninguna otra fase cambió sin prueba colateral.
- Crear `openspec/changes/fase4-legacy-debt-verification/verification-evidence.md` con la tabla de la §1.2 de este documento como base, más lo que falta.
- Pedir aprobación del usuario antes de sincronizar specs o archivar.

**Criterio de salida:** 20/20 con evidencia; `openspec.cmd validate fase4-legacy-debt-verification --strict` pasa.

## 5. Preparación segura común (sin cambios)

### 5.1 Base de prueba aislada para pruebas destructivas

No usar `logicakids_local` para nada que escriba/reseeed de forma experimental. Crear una copia con nombre único (`logicakids_fase4_test_YYYYMMDD_HHMM`):

1. Confirmar `docker ps` y que PostgreSQL está saludable.
2. Inventariar la base local en modo de solo lectura.
3. Crear la base temporal con el usuario PostgreSQL del contenedor.
4. Copiar esquema y datos mediante `pg_dump`/`psql` sin imprimir contraseñas.
5. Sobrescribir `DATABASE_URL` y `ENVIRONMENT=test` solo para el proceso de prueba.
6. Ejecutar pruebas, API y reseed únicamente en la copia.
7. Detener servidores temporales y eliminar la base de prueba exacta.
8. Repetir la auditoría de solo lectura sobre `logicakids_local` y comparar conteos.

No escribir una URL con credenciales en logs, Markdown o comandos versionados.

**Nota de esta sesión:** el trabajo de las §1.1 y 1.2 sí se ejecutó directamente contra `logicakids_local` (reseed de Fase 4 con `docker exec logicakids_local_backend python -m app.fase4.seed`, repetido varias veces), porque no había alumnos reales con progreso en Fase 4 en esa base — se verificó antes de cada reseed (`SELECT count(*) FROM preguntas WHERE fase_id=4`, `progreso_maestria`, `pool_asignado_alumno`). Si el siguiente modelo va a reseedear de nuevo, repetir esa misma verificación de "no hay progreso real que perder" antes de hacerlo, o usar una base aislada si ya hay alumnos probando.

### 5.2 Evidencia de cada cambio

Crear/actualizar desde el inicio: `openspec/changes/<NOMBRE_CAMBIO>/verification-evidence.md`, con la tabla:

| Requisito | Terreno previo | Cambio | Comando/artefacto | Resultado | Límites |
|---|---|---|---|---|---|

Usar únicamente `PASS`, `FAIL`, `BLOCKED`, `UNVERIFIED` o `N/A` con justificación. Una tarea marcada no sustituye la evidencia.

## 6. Comandos mínimos de verificación

```powershell
# OpenSpec
cd D:\Antigravity\APP_Logica_Matematicas_kids
openspec.cmd validate <NOMBRE_CAMBIO> --strict
openspec.cmd instructions apply --change <NOMBRE_CAMBIO> --json

# Backend — suite completa (33 tests nuevos de Fase 4 + resto del repo)
cd LogicaMath\backend
python -m pytest tests\ app\tests\ -q --ignore=tests\test_scripts_config.py

# Frontend
cd ..\frontend
npx tsc --noEmit
npm run test -- --run
npm run build

# Reseed local (si se cambia contenido; verificar antes que no hay progreso real que perder)
docker exec logicakids_local_backend python -m app.fase4.seed

# E2E (una vez arreglada la Etapa D del Cambio 3)
npx playwright test tests\fase4_multiple_opcion.spec.ts --project=chromium --reporter=line
```

## 7. Puertas de detención

Detenerse y pedir decisión si ocurre cualquiera de estos casos:

- El reseed cambiaría IDs referidos por intentos históricos reales (no sintéticos de prueba).
- La base resuelta no es inequívocamente local/test.
- Una supuesta rama muerta tiene registros o consumidor activo que la búsqueda anterior no cubrió.
- Un cambio a `_svg_container`/`svg_figuras.py` afecta visualmente una fase hermana sin aprobación explícita del usuario.
- La solución visual exige ocultar contenido o reducir tipografía fuera del diseño.
- Un test no puede ejecutarse por falta de servidor, navegador, Docker o base.
- El diff invade otra fase o excede el alcance del cambio activo.

La puerta no ejecutada queda `BLOCKED` o `UNVERIFIED`; nunca se marca como PASS.

## 8. Handoff entre modelos

Al terminar cada sesión, actualizar este documento (no solo `verification-evidence.md`) y dejar:

- qué se hizo en esta sesión, con comandos y resultados exactos;
- decisiones del usuario tomadas (o preguntas que quedaron sin responder);
- estado de procesos temporales (contenedores, bases de prueba);
- siguiente tarea exacta.

El modelo receptor debe volver a comprobar terreno, diff y estado OpenSpec — no debe confiar solo en el resumen del modelo anterior.

## 9. Sincronización y archivo (sin cambios)

No archivar automáticamente al completar código. Orden final tras aprobación del usuario:

1. Confirmar que los tres cambios pendientes muestran todas sus tareas completas.
2. Revisar `verification-evidence.md` de cada uno.
3. Ejecutar la matriz final desde entorno limpio.
4. Sincronizar delta specs con las specs principales mediante la skill `openspec-sync-specs`.
5. Solicitar aprobación explícita.
6. Archivar cada cambio mediante `openspec-archive-change`.
7. Verificar `openspec.cmd list --json` y actualizar `docs/README.md` si cambia la fuente de verdad.

No hacer commit, push, deploy ni sincronización a producción sin solicitud explícita del usuario.
