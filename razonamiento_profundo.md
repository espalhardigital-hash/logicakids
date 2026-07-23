# Razonamiento Profundo — Guía de verificación y caza de bugs para agentes LLM

> **Para quién es esto:** cualquier LLM (o persona) con capacidad de razonamiento razonable que tenga que auditar, depurar o mejorar este repositorio (u otro parecido: backend que genera datos + BD + frontend que los renderiza). No es una lista de bugs conocidos; es el **método de razonamiento** que permite encontrar bugs que *nadie ha identificado todavía*, verificarlos contra la realidad, arreglarlos de raíz y probar que quedaron arreglados.
>
> **Complemento obligatorio:** [`LECCIONES_verificacion_agentes.md`](LECCIONES_verificacion_agentes.md) cubre el caso específico de *verificación visual* (generar la imagen y mirarla). Este documento generaliza esa lección a **todo tipo de bug**.
>
> **Cómo usar este documento:** no lo leas como teoría. Cada técnica trae una *receta concreta* y un *ejemplo real* de esta sesión. Cuando enfrentes una tarea, entra por la sección 10 (protocolo de arranque), y usa las secciones 3–5 como referencia mientras trabajas.

---

## 0. La tesis central: el cambio de mentalidad

Casi todos los bugs profundos que un LLM *no* encuentra tienen la misma raíz: **el agente verifica contra la intención del código, no contra la realidad.** Lee el código, ve que "se ve bien", y lo declara correcto.

Las creencias que hay que desactivar:

1. **"El código dice X" ≠ "X realmente pasa".** El código puede *pretender* mostrar una imagen y descartarla dos funciones más abajo. La única prueba de que algo pasa es *observar el efecto*, no leer la causa.
2. **"Funciona en producción" es una hipótesis, no un hecho.** Trátala como algo a *refutar*. En esta sesión, cuatro fases estaban descritas como "funcionales en producción" y en las cuatro era literalmente imposible aprobar un nivel — nadie las había podido completar jamás (0 aprobados en la BD real).
3. **Los comentarios, docstrings y nombres mienten.** Este repo tenía routers de Fase 6/7/8 con docstrings que decían "Fase 2", clases `Fase6*` con texto "Fase 2", y una variable `is_money = (modulo_id == 3)` copiada de una fase donde el módulo 3 *sí* era una tienda. **Nunca razones a partir del comentario; razona a partir del comportamiento.**
4. **"Lo arreglé / lo modifiqué" ≠ el archivo cambió — y "hay un bug" ≠ el bug se ejecuta.** La única prueba de que tocaste un archivo es su `git diff`; la única prueba de que un bug es *real* es que el código afectado *corra*. En esta sesión un agente entregó un informe impecable en la forma (usaba el vocabulario de este documento: "Frontera Afectada", "Causa Raíz", "Invariante Aplicado") pero falso en el fondo: reportó **8 bugs corregidos** cuando 2 eran **fantasma** (los archivos que decía haber modificado no tenían un solo cambio en el diff), otro "bug" vivía en una **función nunca llamada** (código muerto, no se manifestaba), y su sección de "pruebas ejecutadas" citaba un test (`PhaseMapContext.test.ts`) que **no existe**. Todo *sonaba* riguroso. **Antes de creer —o escribir— "está arreglado", mirá el diff, confirmá que el bug se ejecuta, y no cites una verificación que no corriste.**

> **Regla madre:** *toda afirmación sobre el sistema necesita una observación de terreno que la respalde.* Si dices "el progreso avanza", tenés que haber visto el número subir. Si decís "la imagen se muestra", tenés que haber traído esa imagen y mirado. Si decís "está arreglado", tenés que haber re-corrido el chequeo exacto que reveló el bug y verlo en verde.

---

## 1. El bucle de razonamiento (el motor de todo)

Todo el trabajo de esta sesión siguió el mismo bucle de 6 pasos. Memorizalo:

```
1. HIPÓTESIS      → "sospecho que <X> está mal por <señal>"
2. TERRENO        → busca la evidencia que lo confirme O lo refute
                    (consulta la BD real, corre el endpoint real, mira el artefacto real)
3. CUANTIFICAR    → ¿cuántos casos afecta? ¿es 1 o 1800? esto define prioridad
4. RAÍZ           → arregla la CAUSA (el generador/seed/frontera), no el síntoma
5. RE-VERIFICAR   → vuelve a correr EXACTAMENTE el chequeo del paso 2. ¿Ahora da verde?
6. PUNTA A PUNTA  → prueba el flujo completo como lo vive el usuario final
```

**Los dos pasos que los LLMs saltan (y por eso fallan):**

- **Paso 2 (terreno).** Es tentador confirmar una hipótesis leyendo más código. No alcanza. El código que *escribe* el dato y el código que lo *consume* pueden estar en archivos distintos y contradecirse. La verdad está en el dato guardado, no en ninguno de los dos.
- **Paso 5 (re-verificar con el MISMO chequeo).** "Ya escribí el fix" no es "el bug está resuelto". Corre otra vez la consulta/observación del paso 2. Si antes daba `11 duplicados` y ahora da `0`, *eso* es la prueba. Si no volviste a medir, no sabés nada.
  - **Dos salvedades** (ver §4.13 y §6.8): (a) para **generadores aleatorios**, "0 en el snapshot" es necesario pero **no suficiente** — probá el *invariante*, no una muestra; (b) el chequeo del paso 2 confirma que *el bug se fue*, no que *pusiste lo correcto* — a veces hace falta un chequeo adicional que distinga la solución buena de una que solo apaga el síntoma.

**Ejemplo del bucle completo (bug de progreso imposible):**

1. Hipótesis: "el progreso de práctica no avanza porque el router cuenta `COUNT(DISTINCT estructura_padre_id)` y sospecho que esa columna está vacía".
2. Terreno: `SELECT count(*), count(estructura_padre_id) FROM preguntas WHERE fase_id=6;` → `1800 | 0`. Columna 100% NULL. Confirmado.
3. Cuantificar: afecta las 12 secciones de práctica de la fase → intransitable. Y `SELECT count(*) FROM progreso_maestria WHERE fase_id=6 AND estado='APROBADO'` → `0`. Nadie la completó nunca.
4. Raíz: el `seed.py` nunca seteaba `estructura_padre_id`. Se lo agregué.
5. Re-verificar: misma consulta → `1800 | 1440`, familias distintas > 0.
6. Punta a punta: llamé la función real `responder_fase6()` 10 veces con respuestas correctas → el progreso subió `10% → 100% → APROBADO`.

---

## 2. Las capas y sus fronteras: dónde viven los bugs profundos

En una app así, el dato viaja por una tubería. **Los bugs graves casi nunca están *dentro* de una capa; están en las *fronteras*, donde una capa descarta o transforma lo que la anterior produjo.**

```
[generador]  produce datos ricos (enunciado, respuesta, distractores, url de imagen, metadata)
     │  ← FRONTERA 1: ¿el seed guarda TODO lo que el generador produjo, o descarta parte?
[seed/BD]    persiste la pregunta y sus opciones
     │  ← FRONTERA 2: ¿la columna que el router usa para calcular progreso está poblada?
[router/API] elige la pregunta, calcula progreso, valida la respuesta
     │  ← FRONTERA 3: ¿el JSON que sale tiene los campos que el frontend espera?
[frontend]   decide qué widget mostrar según tipo_pregunta / datos_numericos
     │  ← FRONTERA 4: ¿el widget elegido puede realmente responder/mostrar este dato?
[ojo del usuario]  ve (o no ve) la pregunta, la imagen, las opciones
```

**Cada bug crítico de esta sesión fue una frontera rota:**

| Frontera | Bug real |
|---|---|
| 1 (generador→seed) | El generador producía `datos_numericos={url, tipo_visual}` y el seed lo **sobrescribía** con `{"fase6": True}` → 451 preguntas decían "observa la imagen" sin imagen. |
| 2 (seed→BD) | El router calcula progreso con `COUNT(DISTINCT estructura_padre_id)` pero el seed nunca poblaba esa columna → progreso siempre 0%. |
| 3 (router→API) | Fase 8 nunca renderizaba imágenes porque el frontend no tenía bloque para `svg_base64`, aunque el dato llegaba. (Frontera 3/4 combinada.) |
| 4 (frontend→ojo) | Respuestas de texto ("la diagonal") servidas como `RESPUESTA_NUMERICA` → el teclado numérico no deja escribir texto → pregunta imposible de responder. |

> **Técnica maestra:** cuando audites una feature, no leas un archivo — **traza el dato de punta a punta y pregúntate en cada frontera: "¿esta capa preserva/entiende lo que la anterior le dio?"** El bug está donde la respuesta es "no".

---

## 3. Catálogo de arquetipos de bugs

Estos son patrones que se **repiten** entre módulos y proyectos. Aprendé el *síntoma* y la *señal de detección* de cada uno; así los cazás en código que nunca viste.

### A. Campo computado descartado
- **Síntoma:** una feature (imagen, gráfico, metadata) "debería" aparecer pero nunca aparece.
- **Causa:** una capa recalcula/hardcodea un campo, pisando lo que otra capa produjo. Típico: `objeto = {...datos_ricos...}` y más abajo `objeto = {"flag": True}`.
- **Detección:** `grep` del campo en el seed y compará lo que el generador *retorna* contra lo que el `Pregunta(...)` *guarda*. Si el constructor hardcodea el campo, se descarta lo generado.
- **Verificación:** `SELECT DISTINCT datos_numericos FROM ... GROUP BY ...` → si solo ves `{"fase6":true}` y nunca una url, el dato rico se perdió.

### B. NULL en agregado → resultado silenciosamente cero
- **Síntoma:** una métrica (progreso, contador) se queda pegada en 0 sin error.
- **Causa:** `COUNT(DISTINCT columna)` o `AVG/SUM` sobre una columna que es **siempre NULL**. En SQL, `COUNT(DISTINCT NULL) = 0`, sin excepción ni warning.
- **Detección:** identificá qué columna alimenta la métrica y consultá `count(columna)` vs `count(*)`. Si `count(columna)=0`, todo agregado sobre ella es basura.
- **Ejemplo:** progreso = `familias_resueltas / cantidad_req`, `familias_resueltas = COUNT(DISTINCT estructura_padre_id)`, columna 100% NULL → progreso 0% eterno.
- **⚠️ El fix necesita cardinalidad correcta, no solo "no-NULL".** Que la columna deje de ser NULL prueba que la métrica ya no es 0, **no** que esté bien. Dos trampas reales:
  - **Agrupación:** si le ponés un `estructura_padre_id` *único por fila*, el progreso avanza, pero dejás **muertas** las features que dependen de agrupar variantes por familia (Bucle Espejo, Rescate — arquetipo C). El diseño real puede exigir *30 familias × 4 variantes* con `padre_id` compartido. Verificá la forma: `SELECT seccion, count(*) filas, count(DISTINCT estructura_padre_id) fams, count(*)/GREATEST(count(DISTINCT estructura_padre_id),1) variantes_por_fam FROM preguntas WHERE fase_id=? AND seccion<1000 GROUP BY seccion` y exigí que `fams`/`variantes_por_fam` coincidan con lo que el generador pretende.
  - **Denominador:** el progreso es `familias_resueltas / cantidad_requerida`. Si sembrás **menos** familias que `cantidad_requerida`, el nivel sigue siendo imposible aunque la columna ya no sea NULL — mismo síntoma, causa distinta. Verificá `cantidad_requerida <= familias_disponibles`.
  - **Regla:** el DoD de este bug **no** es "la columna dejó de ser 0"; es el E2E de §4.7 llegando a **100%/APROBADO** *y* confirmar que las features que dependían de la agrupación ahora se activan.

### C. Feature muerta (UI existe, lógica nunca dispara)
- **Síntoma:** hay un componente/modal/rama de código elaborado que en la práctica jamás aparece.
- **Causa:** la condición que lo activa depende de un dato que nunca se cumple (variantes `es_espejo` que no existen, `estructura_padre_id` NULL, un `tipo` que el seed nunca genera).
- **Detección:** para cada feature con UI, preguntá "¿qué dato la dispara?" y verificá que ese dato *exista* en la BD. `SELECT count(*) WHERE <condición que activa la feature>`. Si da 0, la feature es código muerto.
- **Ejemplo:** el "Bucle Espejo" y el modal de "Rescate" tenían UI completa pero nunca se activaban (sin `estructura_padre_id` ni variantes espejo).

### D. Fuga de respuesta en la figura o el enunciado
- **Síntoma:** el ejercicio es trivial: se responde sin razonar.
- **Causa:** el visual muestra la solución o el camino a ella.
- **La fuga tiene 3 grados — buscá los tres, no solo el resultado:**
  1. **Resultado:** la figura muestra el número respuesta directamente.
  2. **Planteo/operación ya armada:** el SVG mostraba `"7 m² = 7 × 10,000 cm²"` — **la respuesta (70000) NO aparece literal**, pero la multiplicación ya está planteada → el ejercicio deja de ser "convertir" y pasa a ser "multiplicar". *Buscar solo el string de la respuesta correcta NO detecta esto.*
  3. **Factor/regla/estructura resuelta:** las figuras de simetría dibujaban *todos* los ejes → "contar las líneas" en vez de razonar.
- **La fuga puede vivir en el DATO o en el RENDERER — son detecciones distintas:**
  - **En el dato** (SVG/enunciado guardado): se ve consultando/mirando el dato.
  - **En el renderer** (componente React/generador SVG): el dato luce limpio en la BD, pero el *componente* imprime la solución. Ejemplo real: el termómetro se guardaba sin el número, pero el componente React imprimía `"Lectura: 25°C"` en una pregunta que pedía leerlo. **Esto NO se ve consultando la BD** — solo renderizando el widget real o leyendo el código del componente.
- **Detección:** por cada tipo visual, preguntá "¿se responde sin razonar por (1) resultado, (2) planteo, o (3) factor/estructura?" y revisá **tanto el dato como el componente que lo dibuja**.

### E. Pregunta imposible de responder
- **Síntoma:** el usuario no tiene forma de contestar.
- **Causa:** opción múltiple con **0 alternativas** (grilla vacía + botón Confirmar deshabilitado); o respuesta de **texto** servida como tipo **numérico** (teclado numérico, texto no se puede escribir); o un `tipo_pregunta` que el frontend no renderiza.
- **Detección:** cross-check tipo vs contenido (ojo: la columna es `tipo_pregunta` y el enum se guarda en **MAYÚSCULAS** — SQLAlchemy persiste el `.name`, no el valor):
  - `... WHERE tipo_pregunta='MULTIPLE_OPCION' AND (SELECT count(*) FROM alternativas WHERE pregunta_id=p.id)=0` → opción múltiple sin opciones.
  - `... WHERE tipo_pregunta='RESPUESTA_NUMERICA' AND respuesta_correcta !~ '^-?[0-9]+([.,][0-9]+)?$'` → respuesta de texto en pregunta numérica.
- **Ejemplo:** la sección 402 tenía 56 preguntas con respuesta `"la diagonal"` marcadas como `RESPUESTA_NUMERICA`.

### F. Distractores duplicados / doble respuesta correcta
- **Síntoma:** una opción aparece dos veces, o dos opciones son la correcta.
- **Causa:** las fórmulas de distractor colisionan con la respuesta o entre sí para ciertos valores. Ej: distractor `(y,x)` = respuesta `(x,y)` cuando `x==y`; distractor `azules/total` = `rojas/total` cuando `rojas==azules`; `ans-2` = `suma` en un caso particular.
- **Detección:** `GROUP BY pregunta_id HAVING count(*) <> count(DISTINCT texto)` (duplicados) y `HAVING count(*) FILTER (WHERE es_correcta) <> 1` (cero o dos correctas).
- **Fix robusto:** no parchees el caso; usá un helper que *garantice el invariante* (4 opciones distintas, exactamente 1 correcta) para *todos* los valores.

### G. Huérfano de flujo de control (bloque mal indentado / código inalcanzable)
- **Síntoma:** un endpoint devuelve `None`/500 en un camino, o una rama nunca se ejecuta.
- **Causa:** en Python, un bloque indentado *dentro* de un `if` que siempre retorna, sin `else`, queda inalcanzable; y el camino "normal" cae al final de la función → `return None` implícito.
- **Detección:** mirá la *indentación real* (no la intención). Para el bloque sospechoso, medí sus espacios y los del `if`/`else` que lo debería contener. Confirmá con una **prueba de comportamiento**: llamá la función real por ese camino y mirá qué devuelve.
- **Ejemplo:** en Fase 6 el bloque "Práctica Libre" estaba a 8 espacios dentro del `if de desafíos` sin `else` → toda respuesta de práctica devolvía `None` (500). Confirmado llamando `responder_fase6()` → `AttributeError: 'NoneType'`.
- **Elegir la forma del fix (des-indentar vs `else`) NO es arbitrario — depende de si la rama previa SIEMPRE retorna:**
  - Si el `if` previo **siempre termina en `return`** (todos sus sub-caminos) → des-indentar el bloque a nivel de función es correcto (es alcanzable solo cuando el `if` no entró). Así se arregló Fase 6.
  - Si el `if` previo **puede caer sin retornar** → des-indentar ejecutaría el bloque *también* en ese camino; ahí necesitás un `else:`.
  - **Verificá con el E2E los DOS caminos** (el que crasheaba y el otro), no solo uno.
- **⚠️ Trampa:** este mismo bug NO estaba en Fase 7/8 (ahí sí había `else:`). **Casi rompo Fase 7 aplicando el fix de Fase 6 a ciegas** (des-indenté un bloque que ya estaba bien) — lo detecté porque el Edit tool no matcheó el texto esperado y lo revertí con `git checkout`. Ver §6.5.

### H. Desajuste semántico por copy-paste
- **Síntoma:** una constante/flag tiene un valor que no corresponde a este módulo.
- **Causa:** el módulo se copió de otro y quedó una suposición del original. `is_money = (modulo_id == 3)` tenía sentido en Fase 2/3 (módulo 3 = Tienda) pero se copió a Fase 5/6/7/8 donde el módulo 3 es Figuras/Cubos/Tiempo/Probabilidad.
- **Detección:** cuando veas código que asume algo específico (`modulo_id == 3`, un nombre, una unidad), verificá que esa suposición sea cierta *en este* módulo. Y buscá el rastro del copy-paste: docstrings/nombres que mencionan otra fase.

### I. Generador de variedad cero (preguntas repetidas)
- **Síntoma:** las preguntas de una sección son idénticas salvo el nombre del personaje.
- **Causa:** los números están hardcodeados (no `rng.`), o los números solo viven en la imagen y no en el texto → el enunciado solo cambia por el nombre.
- **Detección:** `SELECT round(100.0*count(DISTINCT enunciado)/count(*)) AS pct FROM preguntas WHERE fase_id=? AND seccion<1000 GROUP BY seccion`. Un pct bajo (≤50%) marca la sección.
- **Ejemplo:** una sección de volumen daba 5% de variedad porque las dimensiones solo estaban *en la imagen*; el texto era `"¿Cuántos cubitos... construyó {nombre}?"` — idéntico salvo el nombre.

### J. Dato mal mapeado (clave equivocada)
- **Síntoma:** una porción de contenido "falta" aunque el código para generarlo existe.
- **Causa:** una clave de diccionario mal escrita: `(1,4)` en vez de `(2,2)`.
- **Detección:** consultá la cobertura por celda: `SELECT modulo_id, nivel_id, jsonb_array_length(campo) FROM ... ORDER BY 1,2`. La celda con 0 donde las demás tienen N delata el mapeo roto.

### K. Entorno obsoleto (producción corre código viejo)
- **Síntoma:** el fix funciona en local pero producción sigue rota.
- **Causa:** producción no se reconstruyó/re-sembró tras cambios de código. Señal fuerte: el *registro de versión de seed* en la BD no coincide con el que el código espera.
- **Detección:** compará el `SEED_VERSIONS` del código dentro del contenedor de prod contra `platform_settings.database_seed_versions` en la BD de prod. Y `grep` de tus fixes distintivos dentro del contenedor: `docker exec <backend> grep -c 'mi_marca_distintiva' /app/...`. Si da 0, el código desplegado es viejo.

### L. Fix fantasma / crédito falso (un reporte afirma un cambio que el diff no muestra)
- **Síntoma:** un informe dice "corregí X en `archivo.tsx`", pero el archivo está intacto — o el fix descrito *ya existía* antes de la sesión y el agente se lo atribuye.
- **Causa:** el agente razonó desde su *intención* ("iba a cambiar esto") o desde el código que *leyó* ("esto ya estaba bien → luego yo lo hice"), nunca desde el diff real.
- **Detección:** por **cada** archivo que el reporte dice tocar, corré `git diff HEAD -- <archivo>`. Diff vacío = fantasma. Cruzá la lista de "archivos modificados" del reporte contra `git status --short`: los que faltan son inventados. Para descartar auto-crédito, `git log -1 --format=%ci -- <archivo>` o `git blame` de las líneas del "fix": si preceden tu sesión, no las hiciste vos.
- **Ejemplo:** un reporte afirmaba haber corregido `PerformanceTab.tsx` y `QuestionFormModal.tsx`; ambos tenían `git diff` vacío. La sincronización que el segundo decía "implementar" ya estaba en el archivo desde semanas antes.

### M. Bug reportado en código inalcanzable (no se manifiesta)
- **Síntoma:** se reporta un bug en una función/rama que en la práctica **nunca se ejecuta**, así que no afecta a ningún usuario.
- **Causa:** el agente detectó un patrón sospechoso (una condición vieja, un valor raro) pero no verificó si ese código *corre*.
- **Detección:** antes de reportar, buscá el **call site**: `grep -rn 'nombreFuncion\b'` — ojo con el `\b`: un prefijo compartido como `foo` matchea `fooBar`, así que sin límite de palabra contás usos que no son. 0 usos reales = código muerto. Para ramas: ¿existe un dato que active esa rama? (arquetipo C, al revés). Un bug que no se ejecuta **no es un bug vivo**: puede ser limpieza válida (borrá el muerto para que nadie lo reviva), pero no lo vendas como corrección funcional.
- **Ejemplo:** `computeAggregateStatus` usaba la condición obsoleta `fase_id === 0`, pero estaba **definida y nunca llamada**; todos los call sites reales usaban `computeAggregateStatusForPhase`. El "bug" no afectaba a nadie — la corrección honesta fue *eliminar la función muerta*, no fingir que se arregló una lógica que corría.

---

## 4. Técnicas de detección: cómo encontrar bugs que **nadie** identificó

La sección 3 es el catálogo. Esta es la *caza*. Estas técnicas destapan bugs desconocidos.

### 4.1 Interrogá los datos, no el código
La BD es la verdad de terreno. Antes de leer un archivo, preguntale a la BD cómo se ve *de verdad* el contenido:
- **Distribuciones:** `GROUP BY tipo, ... count(*)` — ¿hay valores que no deberían existir?
- **NULLs:** `count(columna)` vs `count(*)` en toda columna que alimente lógica.
- **Duplicados:** `HAVING count(*) <> count(DISTINCT ...)`.
- **Extremos:** ¿hay respuestas fuera de rango, secciones con muchas menos filas que otras, textos vacíos?

### 4.2 Cross-check: "¿el dato coincide con lo que el código afirma?"
El enunciado dice "observa la imagen" → ¿existe la url? El tipo es "numérico" → ¿la respuesta es un número? El código dice "4 opciones" → ¿hay 4 filas de alternativa? Cada afirmación del código o del texto es una aserción que la BD puede confirmar o desmentir.

### 4.3 Renderizá el artefacto real y MIRALO
Nunca confíes en que un SVG/PNG/gráfico "se ve bien" leyendo el código. Traelo y miralo (herramienta de lectura de imágenes). Para PNG generados por el backend: generalos dentro del contenedor, `docker cp` al host, leelos. Para imágenes en storage: `curl` la url pública y verificá `HTTP 200 image/png`, luego abrila. Si el detalle es fino, crop + zoom **sin interpolación** (`Image.NEAREST`) para no confundir un artefacto de resize con un bug. (Ver `LECCIONES_verificacion_agentes.md`.)

### 4.4 Trazá el flujo completo y auditá cada frontera
(Sección 2.) Elegí una feature, seguí el dato generador→seed→BD→router→API→frontend, y en cada frontera preguntá "¿esta capa preserva/entiende lo que recibió?".

### 4.5 "Features con UI pero sin dato que las dispare"
Por cada componente elaborado del frontend (un modal, un visualizador), buscá la condición que lo activa y verificá en la BD que ese dato exista. UI sin dato = feature muerta (arquetipo C).

### 4.6 Diff contra un hermano que funciona
Si hay varios módulos análogos (fase1..fase9), y uno funciona, **compará el que sospechás contra el que funciona**. En esta sesión: `grep estructura_padre_id` en todos los seeds → aparecía en fase2/3/4 pero **no** en fase6 → esa ausencia *era* el bug. El hermano sano es tu oráculo de "cómo debería ser".

### 4.7 Jugá la app de punta a punta (o simulá el endpoint real)
La prueba definitiva de una feature es usarla. Si no podés abrir la UI (falta login), **llamá las funciones reales del endpoint en proceso**, con datos reales, y observá el efecto. En esta sesión escribí un script que instancia una sesión de BD real, carga un alumno real, y llama `responder_faseN(payload, db, alumno)` varias veces con respuestas correctas, verificando que el progreso suba a 100%. Limpiá los datos de prueba al final (borrá los `Intento`/`ProgresoMaestria` que creaste). **Esto detectó el bug de `return None` que ninguna lectura de código me habría confirmado.**

### 4.8 Buscá fugas de respuesta
(Arquetipo D.) Por cada pregunta con visual, preguntá "¿se responde solo mirando, sin razonar?".

### 4.9 Medí la variedad
(Arquetipo I.) `distinct(enunciado)/count(*)` por sección. Un ratio bajo delata generadores pobres. Ojo: variedad alta de *string* no garantiza variedad de *situación* — leé una muestra: si solo cambia el nombre, sigue siendo pobre aunque el ratio suba.

### 4.10 Desconfiá de comentarios y docstrings; leé el comportamiento
Si un docstring dice "Fase 2" en un archivo de Fase 6, no dice nada útil sobre Fase 6. Ignoralo y leé qué hace el código.

### 4.11 Cuando encuentres un bug, buscá el patrón en TODOS los hermanos
Un bug rara vez es único. Si `is_money` está mal en Fase 6, `grep is_money` en fase5/7/8 — estaba mal en las cuatro. Si el seed no setea `estructura_padre_id` en una fase, revisá todas. **Un bug encontrado es una plantilla de búsqueda.**

### 4.12 Señales indirectas de bug estructural
- **"Nadie lo completó nunca":** `SELECT count(*) FROM progreso_maestria WHERE fase_id=? AND estado='APROBADO'` = 0, con la fase supuestamente en producción hace tiempo → algo estructural impide progresar.
- **0 intentos registrados:** si una fase con tráfico tiene 0 filas en `intentos`, es señal *fuerte* de que el endpoint de respuesta crashea (arquetipo G) — **pero solo si el intento se persiste al final del handler** (después del punto de fallo). Si se guardara antes del crash, habría filas pese al 500. La prueba definitiva sigue siendo llamar la función real (§4.7) y ver el `None`/500, no inferirlo del conteo.
- **Contenido inflado:** una sección con 4× las filas esperadas → siembras repetidas sin limpieza (deuda de datos).
- **⚠️ Un mismo síntoma, varias causas independientes.** Un síntoma estructural (0 aprobados, progreso pegado) puede tener **varios bugs distintos en el mismo flujo**. En esta sesión, Fase 6 era intransitable por DOS bugs a la vez: la columna NULL (arquetipo B) *y* el `return None` por indentación (arquetipo G) — arreglar uno no bastaba. **Regla:** si aplicaste un fix y el E2E *sigue* fallando, **no revirtás automáticamente**; confirmá que tu fix cumplió su chequeo local (ej. la columna ya no es NULL) y seguí cazando el siguiente eslabón. Recién declarás resuelto cuando el E2E completo llega a 100%/APROBADO.

### 4.13 Bugs dependientes del valor en generadores aleatorios
Cuando distractores/opciones/figuras se derivan de fórmulas sobre parámetros aleatorios, **una foto de la BD es UN muestreo del espacio de entradas, no una prueba.** Un bug que solo aparece para ciertos valores (ej. dos opciones colisionan solo cuando `x==y`) puede dar `0 duplicados` hoy porque la semilla actual no sorteó ese caso — y reaparecer en la próxima re-siembra.
- **No confíes solo en el snapshot.** La consulta `HAVING count<>count(DISTINCT)` prueba la tirada actual, no el generador.
- **Detección analítica:** leé la fórmula del distractor y enumerá los **inputs degenerados** donde puede colisionar: operandos iguales (`x==y`, `a==b`), `0`, `1`, extremos del rango, y simetrías (`(x,y)` vs `(y,x)`). Comprobá que el invariante (4 opciones distintas, 1 correcta) se mantiene para **todos**. Ejemplos reales: `(y,x)` colisiona con la respuesta `(x,y)` cuando `x==y`; `azules/total` == `rojas/total` cuando `rojas==azules`.
- **Verificación robusta:** o probás el generador sobre *muchas* re-siembras/semillas, o —mejor— reemplazás la fórmula frágil por un **helper que garantice el invariante** para cualquier entrada (§6.2), y entonces el snapshot sí alcanza.
- **Corolario para §1 paso 5 y §9:** para generadores aleatorios, "0 duplicados en un snapshot" es **necesario pero no suficiente**. La prueba real es el invariante sobre el generador, no sobre una muestra.

---

## 5. Recetario de verificación (patrones concretos y reutilizables)

Generalizá los nombres de tabla/columna a tu esquema. Todos estos corrieron de verdad en esta sesión.

**Integridad de opción múltiple (duplicados + cero/dos correctas):**
```sql
-- preguntas con opciones repetidas
SELECT count(*) FROM (
  SELECT p.id FROM preguntas p JOIN alternativas a ON a.pregunta_id=p.id
  WHERE p.fase_id IN (5,6,7,8) AND p.tipo_pregunta='MULTIPLE_OPCION'
  GROUP BY p.id HAVING count(*) <> count(DISTINCT a.texto)
) x;
-- preguntas sin exactamente 1 correcta (o sin 4 opciones)
SELECT count(*) FROM (
  SELECT p.id FROM preguntas p JOIN alternativas a ON a.pregunta_id=p.id
  WHERE p.fase_id IN (5,6,7,8) AND p.tipo_pregunta='MULTIPLE_OPCION'
  GROUP BY p.id HAVING count(*) FILTER (WHERE a.es_correcta) <> 1 OR count(*) <> 4
) y;
```

> **⚠️ Las dos consultas de arriba usan `JOIN` (INNER) y por eso NO ven el caso más peligroso: opción múltiple con CERO alternativas** (grilla vacía, imposible de responder — bug real). Una pregunta sin hijos no produce ninguna fila en el INNER JOIN, así que nunca entra al `GROUP BY`. Agregá siempre esta consulta con `LEFT JOIN`:
> ```sql
> -- opción múltiple con 0 alternativas: el INNER JOIN de arriba las esconde
> SELECT p.id FROM preguntas p
> LEFT JOIN alternativas a ON a.pregunta_id=p.id
> WHERE p.fase_id IN (5,6,7,8) AND p.tipo_pregunta='MULTIPLE_OPCION'
> GROUP BY p.id HAVING count(a.id)=0;   -- debe ser vacío
> ```
> **Lección general:** para validar/contar *hijos*, usá `LEFT JOIN` + `count(hijo.id)`. Un `INNER JOIN` esconde exactamente el caso "sin hijos", que suele ser el bug.

**Variedad por sección (situación, no solo nombre):**
```sql
SELECT seccion, count(*) filas, count(DISTINCT enunciado) distintos,
       round(100.0*count(DISTINCT enunciado)/count(*)) pct
FROM preguntas WHERE fase_id=? AND seccion<1000 GROUP BY seccion ORDER BY seccion;
```

**Columna clave NULL / cobertura de familias:**
```sql
SELECT count(*) total, count(estructura_padre_id) con_valor,
       count(DISTINCT estructura_padre_id) distintos
FROM preguntas WHERE fase_id=? AND seccion<1000;
-- si con_valor=0, todo COUNT(DISTINCT) sobre esa columna da 0
```

**Respuestas imposibles de tipear (texto en pregunta numérica):**
```sql
SELECT fase_id, count(*) FROM preguntas
WHERE tipo_pregunta='RESPUESTA_NUMERICA'
  AND respuesta_correcta !~ '^-?[0-9]+([.,][0-9]+)?$'
GROUP BY fase_id;   -- debe ser 0
```

**Cross-check "dice imagen pero no hay imagen"** (normalizá el case y ampliá el vocabulario — una lista corta produce falsos negativos):
```sql
SELECT count(*) FROM preguntas
WHERE fase_id=?
  AND lower(enunciado) ~ '(imagen|figura|dibujo|gr[áa]fico|observa|mira|se muestra|la escala)'
  AND NOT (datos_numericos ? 'url')
  AND enunciado NOT LIKE '%<svg%';   -- algunas figuras van como SVG inline en el enunciado, no como url
-- cruce INVERSO: hay dato de imagen pero el enunciado no la menciona (widget huérfano)
SELECT count(*) FROM preguntas
WHERE fase_id=? AND datos_numericos ? 'url'
  AND lower(enunciado) !~ '(imagen|figura|dibujo|gr[áa]fico|observa|mira|se muestra)';
```

**Cobertura de contenido por celda (detecta claves mal mapeadas):**
```sql
SELECT modulo_id, nivel_id, jsonb_array_length(COALESCE(ejemplos,'[]'::jsonb)) n
FROM niveles_teoria_pool WHERE fase_id=? ORDER BY modulo_id, nivel_id;
```

**Simulación E2E del endpoint real (Python dentro del contenedor):**
```python
# instancia sesión real, carga alumno real, responde N veces correctamente,
# verifica que el progreso llegue a 100%, y LIMPIA los datos de prueba al final.
import asyncio
from sqlalchemy import select, and_, delete
from sqlalchemy.orm import selectinload
from app.db.session import AsyncSessionLocal
from app.models.sql_models import Alumno, Pregunta, ProgresoMaestria, Intento
from app.faseN.router import responder_faseN, _seccion_operacion
# OJO: la capitalización del schema NO es uniforme entre fases —
# fase5/6: Fase5ResponderPregunta (F mayúscula); fase7/8: fase7ResponderPregunta (f minúscula).
# Verificá el nombre exacto en app/faseN/schemas.py antes de importar.
from app.faseN.schemas import FaseNResponderPregunta
async def main():
    async with AsyncSessionLocal() as db:
        alumno = (await db.execute(select(Alumno).where(Alumno.id==<id>))).scalar_one()
        seccion,_ = _seccion_operacion(mod, lvl)
        qs = (await db.execute(select(Pregunta).options(selectinload(Pregunta.alternativas))
              .where(and_(Pregunta.fase_id==N, Pregunta.seccion==seccion)))).scalars().all()
        # elegir 1 pregunta por familia; responder correcto (alternativa_id o respuesta_dada
        # según el tipo); imprimir res.porcentaje_actual y res.bloque_completado
        # ... FINALLY: delete Intento y ProgresoMaestria de prueba, commit
asyncio.run(main())
```

**Traer y ver una imagen de storage:**
```bash
url=$(psql ... -t -A -c "SELECT datos_numericos->>'url' FROM preguntas WHERE ... LIMIT 1;")
curl -s -o /dev/null -w 'HTTP %{http_code} %{content_type}\n' "$url"   # espera 200 image/png
# luego descargar y abrir con la herramienta de lectura de imágenes
```

**Prod vs local: ¿corre el código nuevo?**
```bash
# el nombre del seed NO es uniforme: fase5/6 usan app/faseN/seed.py; fase7/8 usan
# app/faseN/seed_faseN.py. Usá un glob recursivo para no depender del nombre exacto:
docker exec <backend_prod> grep -rc '<marca_distintiva_de_mi_fix>' /app/app/faseN/
docker exec <backend_prod> sh -c "grep -A12 'SEED_VERSIONS = {' /app/app/seed.py"
psql ... -t -c "SELECT value FROM platform_settings WHERE key='database_seed_versions';"
# si el grep da 0 o las versiones no coinciden → prod corre código viejo
```

---

## 6. Cómo escribir el fix (correcto Y robusto)

1. **Arreglá la raíz, no el síntoma.** El bug de imágenes se arreglaba en el *seed* (preservar `datos_numericos`), no parcheando 451 preguntas a mano. Preguntá "¿de dónde salió este dato malo?" y arreglá ahí.
2. **Garantizá invariantes con un helper, no con parches puntuales.** Para los distractores no arreglé cada colisión; escribí `_finalize_alts`/`_dedupe_and_pad` que *siempre* devuelve 4 opciones distintas con 1 correcta, para cualquier entrada. Un invariante bien puesto mata una familia entera de bugs.
3. **Preservá la pedagogía — y no cambies un bug por otro.** Un fix técnico puede romper el sentido del ejercicio: no filtres la respuesta en la figura, mantené la pregunta respondible, no bajes la dificultad a "contar líneas". **Trampa concreta:** al quitar una fuga (arquetipo D) es fácil dejar la figura *vacía/inútil* → caés en arquetipo A/E. Antes de borrar, definí qué información legítima debe **conservar** la figura (el contexto/forma —ej. un cuadrado rotulado "7 m²"— sin la aritmética). Tras el fix, re-corré el cross-check de arquetipo A/E: ¿la figura sigue aportando algo o quedó vacía? La verificación visual de §9 ("generé la imagen y la miré") debe confirmar **ambas cosas**: sin fuga *y* con contexto suficiente.
4. **Idempotencia / disparar la re-siembra.** Si el fix vive en datos sembrados, subí la versión de seed (`SEED_VERSIONS`) para que el sistema detecte el cambio y re-siembre. Sin eso, el fix no llega al dato que la app sirve.
5. **⚠️ NUNCA apliques un fix hermano a ciegas.** Casi rompo `fase7/router.py` aplicando el des-indentado que arregló `fase6/router.py`, porque Fase 7 *sí* tenía el `else:` correcto — mi cambio lo destruyó. **Antes de replicar un fix, verificá que la estructura local sea realmente idéntica.** El Edit tool con match exacto sirve de chequeo anti-error: si el texto no coincide, la estructura difiere y hay que mirar.
6. **Cuando toques rangos/plantillas para variedad, re-medí.** Ampliar rangos sin re-consultar la variedad es asumir. Corré la query de variedad después de re-sembrar.
7. **Cuando cambies el TIPO de una respuesta, verificá que el frontend pueda recibirla.** Pasar de numérico a opción múltiple sólo sirve si el frontend renderiza las opciones para ese tipo.
8. **El fix también necesita su verdad de terreno.** Confirmar que *el bug se fue* no es confirmar que *pusiste lo correcto* — un fix plausible-pero-incorrecto puede apagar el síntoma original y dejar otro roto (ej. `estructura_padre_id` único por fila mata el progreso-0 pero deja muertas las features de familia). Por cada fix definí explícitamente:
   1. el **invariante objetivo** concreto y medible (no solo "arreglé la raíz" — ej. "30 familias × 4 variantes, `cantidad_req <= familias`").
   2. una **re-verificación que falle si el fix es plausible-pero-incorrecto**, no solo si el bug original sigue (ej. chequear la *cardinalidad* de familias, no solo que la columna dejó de ser NULL).
   3. el **E2E como árbitro final** (§4.7): que el flujo llegue a 100%/APROBADO por los caminos afectados.

---

## 7. Disciplina de producción (cuando el fix toca un sistema vivo)

Orden estricto, sin saltear pasos:

1. **Solo lectura primero.** Antes de escribir nada: revisá logs (`docker logs --tail`, grep de `error|traceback|critical`), estado de contenedores, uso de recursos. Confirmá que hay o no tráfico en vivo.
2. **Entendé la arquitectura de despliegue ANTES de asumir.** Un `git push` **no siempre** despliega. Acá el stack de Portainer se construye desde archivos copiados en el VPS (`docker compose build`), no desde git. Inspeccioná las labels del contenedor (`docker inspect --format '{{json .Config.Labels}}'`) para hallar el `com.docker.compose.project.config_files` real.
3. **Backup antes de CUALQUIER escritura.** `pg_dump -F c` de la BD + tar del código actual, copiados fuera del contenedor a un lugar persistente del host. Guardá el md5. Sin backup no se toca nada.
4. **Auditá el alcance de las funciones destructivas.** Antes de correr un `clear_*`/re-seed, leé qué borra *exactamente*. Confirmá que **no toca** tablas de usuario/puntaje. Acá `clear_faseN_data` borraba solo `Pregunta`/`Alternativa`/`Intento` de esa fase — nunca `Alumno`/`User`/`ProgresoMaestria`.
5. **Re-verificá después de desplegar.** Repetí las consultas de integridad contra la BD de prod; confirmá con conteos que las tablas que *no* debías tocar quedaron con el mismo número de filas; healthcheck externo (`curl https://.../api/docs` → 200); logs sin errores nuevos.
6. **Confirmá que el código desplegado es el nuevo** (grep de tu marca distintiva dentro del contenedor, sección 4.12/5).
7. **Pedí confirmación explícita antes de escribir en producción** si hay usuarios activos. Ofrecé opciones (deploy completo / solo backup+build / esperar ventana de bajo tráfico).

---

## 8. Anti-patrones que hacen fallar a los LLMs (checklist de trampas)

- ❌ Confiar en comentarios/docstrings/nombres en vez del comportamiento.
- ❌ Aceptar "está en producción, funciona" sin refutarlo con la BD.
- ❌ Arreglar lo que el código *pretende* hacer en vez de lo que *hace*.
- ❌ Declarar "arreglado" sin re-correr el chequeo exacto que reveló el bug.
- ❌ Verificar leyendo más código en vez de mirar el dato/artefacto real.
- ❌ Aplicar un fix de un archivo hermano sin confirmar que la estructura local es idéntica.
- ❌ Ampliar variedad/rangos sin re-medir; cambiar tipo de respuesta sin verificar el render.
- ❌ Arreglar un caso puntual en vez del invariante que mata la familia de bugs.
- ❌ Subir la versión de seed pero nunca re-sembrar (el fix queda "en el código" sin llegar al dato).
- ❌ Escribir en producción sin backup, sin auditar el alcance destructivo, sin re-verificar.
- ❌ Tratar variedad de string como variedad real (si solo cambia el nombre, sigue siendo pobre).
- ❌ Afirmar "modifiqué/arreglé el archivo X" sin haber abierto el `git diff` de X.
- ❌ Atribuirse un fix que ya existía (sin `blame`/`log` que confirme que el código no precede tu sesión).
- ❌ Reportar un bug sin confirmar que el código afectado se ejecuta (buscá el call site).
- ❌ Citar una verificación irreproducible: un test que no existe, un `200 OK` que nunca llamaste, "N/N tests en verde" sin la salida real.
- ❌ Declarar "100% funcional" un componente que no tocaste ni observaste.
- ❌ Fiarte de una sola sonda de git (`git show :archivo` = índice) en vez de la comparación correcta (`git diff HEAD` = working vs último commit).
- ❌ Inflar el conteo ("8 bugs corregidos") mezclando fixes reales, features preexistentes y fantasmas en la misma cifra.

---

## 9. Definición de Terminado (checklist maestro)

No declares una tarea terminada sin poder marcar todo lo que aplique:

- [ ] Reproduje/confirmé el bug contra la **verdad de terreno** (BD real / artefacto real / endpoint real), no solo leyendo código.
- [ ] Cuantifiqué el impacto (cuántos casos, secciones, usuarios).
- [ ] Arreglé la **raíz** (generador/seed/frontera), no el síntoma.
- [ ] Busqué el **mismo patrón en todos los hermanos** y los arreglé también.
- [ ] Re-corrí el **chequeo exacto** que reveló el bug y ahora da verde.
- [ ] Probé el flujo **de punta a punta** como el usuario final (o simulando el endpoint real).
- [ ] Para fixes visuales: **generé la imagen y la miré** (ver `LECCIONES_verificacion_agentes.md`).
- [ ] Disparé la re-siembra/rebuild y confirmé que el dato servido es el corregido.
- [ ] Verifiqué integridad post-fix (0 duplicados, 0 mal formadas, 0 imposibles de responder).
- [ ] En producción: backup hecho, alcance destructivo auditado, tablas de usuario/puntaje intactas, healthcheck OK, código nuevo confirmado en el contenedor.
- [ ] Actualicé la memoria/documentación con el hallazgo y el método.
- [ ] **Cada fix que afirmo aparece en el `git diff`** (no es fantasma) y confirmé que no preexistía a mi sesión.
- [ ] **Confirmé que el bug se manifiesta** (código alcanzable, función llamada, dato que activa la rama) antes de reportarlo/arreglarlo.
- [ ] **Cada verificación que cito es reproducible:** el test existe y lo corrí; el endpoint lo llamé y vi la respuesta; el número salió de la BD real.
- [ ] **El código nuevo compila** (`tsc --noEmit` / `py_compile` / `build` con exit 0), no solo "se ve bien".
- [ ] No declaré "funcional/OK" nada que no haya observado con mis propios ojos.
- [ ] Mi reporte separa **lo que ya estaba** de **lo que cambié yo** de **lo que queda sin verificar**, sin inflar el conteo.

---

## 10. Protocolo de arranque para un repo desconocido

Cuando entres a una tarea nueva, hacé esto *antes* de proponer cambios:

1. **Mapeá el stack y los entornos.** ¿Qué es backend/frontend/BD/storage? ¿Hay local/desarrollo/producción separados? ¿Dónde vive el "dato de verdad" (BD dinámica vs archivo estático)? Revisá memoria/CLAUDE.md/docs.
2. **Encontrá el "hermano que funciona".** Si hay N módulos análogos, identificá uno sano; será tu oráculo de "cómo debería ser" para diffs.
3. **Corré las consultas de salud base** (sección 5): distribución de tipos, NULLs en columnas clave, duplicados, variedad, cross-checks "dice X pero el dato es Y". Esto suele destapar 2-3 bugs en la primera pasada.
4. **Elegí una feature y trazala de punta a punta** (sección 2/4.4). Auditá cada frontera.
5. **Señales indirectas** (4.12): ¿alguna fase con 0 aprobados/0 intentos pese a estar "en producción"? Empezá por ahí.
6. **Solo entonces** formulá hipótesis y entrá al bucle de la sección 1.

> **Si tu tarea es auditar un reporte/PR ya existente** (tuyo o de otro agente) en vez de arrancar de cero, entrá primero por la **sección 11**: cruzá cada afirmación del reporte contra el `git diff`, el compilador y el endpoint real antes de creer una sola línea.

---

## 11. Integridad del reporte: auditá tu propio trabajo (y el de otro agente) contra el diff

Las secciones 0–10 enseñan a no confiar en lo que el **código** dice que hace. Esta enseña a no confiar en lo que un **reporte** dice que *hizo* — sea de otro agente o **tuyo**. El disparador fue una auditoría real de un panel de administración: un agente entregó un informe con el vocabulario correcto de este documento pero, de 8 "bugs corregidos", **4 eran reales y bien hechos**, **2 eran fantasma** (archivos sin un cambio en el diff), **1 vivía en código muerto**, y las "pruebas ejecutadas" citaban un test inexistente y HTTP 200 sin evidencia. Adoptó el ritual sin la disciplina.

**La verdad de terreno acá no es la BD — es el diff, el compilador, el endpoint real y la UI renderizada.** No todo repo tiene un seed que interrogar; este panel no tocaba datos sembrados. Cuando el bug vive en frontend/API/config, tus oráculos son otros:

| Afirmación del reporte | Sonda de terreno que la confirma o la desmiente |
|---|---|
| "modifiqué `archivo`" | `git diff HEAD -- archivo` (¿el cambio está?) + `git status --short` (¿el archivo figura?) |
| "este fix es mío" | `git blame` / `git log` de las líneas (¿preceden mi sesión?) |
| "hay un bug en esta función" | `grep -n 'fn\b'` → ¿tiene call site? ¿se ejecuta? |
| "corregí el bug" | re-corré el chequeo que lo reveló + E2E; ¿el flujo llega a OK? |
| "la frontera está bien" | ¿el endpoint que el frontend llama **existe** en el backend? (`grep` la ruta) |
| "compila / no rompe nada" | `tsc --noEmit`, `py_compile`, `build` → exit 0, no "se ve bien" |
| "los tests pasan (N/N)" | ¿el archivo de test **existe**? ¿lo corriste y viste la salida? |
| "el endpoint devuelve 200" | ¿lo **llamaste**? pegá la respuesta real, no la esperada |
| "la pestaña está 100% funcional" | ¿la abriste/renderizaste? no declares verde lo que no viste |

**Receta para auditar un reporte (ajeno o propio) antes de creerle:**
1. Extraé la lista de archivos que el reporte dice tocar. Corré `git diff HEAD --stat` y cruzá: **cada archivo reclamado debe estar en el diff**; los que faltan son fantasma (arquetipo L).
2. Por cada bug "encontrado", confirmá que **se manifiesta** antes de aceptar el fix: ¿el código corre? (arquetipo M).
3. Por cada "verificación", exigí que sea **reproducible**: el test existe y corre; el endpoint responde cuando lo llamás; el número sale de la BD real. Si no podés reproducirla, no vale.
4. Corré el **compilador/typecheck sobre el conjunto completo** de cambios — un fix puede introducir un símbolo sin importar, romper tipos, o dejar un `<td>` sin su `<th>`. Varios fixes correctos por separado pueden romperse juntos.
5. **Una sola sonda puede engañarte.** En esta sesión creí por un momento que un fix real *no* estaba aplicado porque miré `git show :archivo` (el **índice**, sin cambios stageados) en vez de `git diff HEAD` (working vs commit). La hipótesis se refutó con la sonda correcta. **Cuando una observación te sorprenda, preguntate si estás mirando la capa correcta antes de concluir** (corolario del §1 paso 5).

**Y aplicátelo a vos mismo.** Antes de escribir "corregí / arreglé / verifiqué", pasá tu propio informe por esta receta. El reporte honesto dice tres cosas **por separado** y no las confunde: (a) qué **ya estaba** bien, (b) qué **cambiaste vos** —con el diff que lo prueba—, (c) qué **queda sin verificar** por falta de terreno (p. ej. "no levanté el backend, el E2E del DELETE está pendiente"). Inflar el conteo o firmar en verde lo no observado no es un descuido de redacción: es el mismo pecado que este documento combate — **declarar sin terreno**.

---

## Apéndice: relación con otros documentos

- **`LECCIONES_verificacion_agentes.md`** — caso profundo de *verificación visual*: por qué un fix de imagen no está terminado hasta generar el artefacto y mirarlo, con checklist de "Definition of Done" visual. Este documento (§4.3, §9) lo incorpora como una técnica; leelo entero antes de tocar generación de imágenes.
- **Memoria del proyecto** (`memory/`) — inventario vivo de bugs concretos ya encontrados y arreglados por fase. Consultalo para no re-descubrir lo ya resuelto; **este** documento es el *método* para encontrar lo que aún no está en esa lista.

> **La idea de una frase:** *no confíes en lo que el código dice que hace —interrogá al dato, mirá el artefacto, jugá el flujo, y no declares nada resuelto hasta que la misma medición que te mostró el bug te muestre que se fue— y no confíes en lo que un reporte (ajeno o tuyo) dice que hizo: el diff, el compilador y el endpoint real son los únicos que firman.*
