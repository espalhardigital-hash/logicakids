# Razonamiento Profundo — Guía de verificación y caza de bugs para agentes LLM

> **Para quién es esto:** cualquier LLM (o persona) con capacidad de razonamiento razonable que tenga que auditar, depurar o mejorar este repositorio (u otro parecido: backend que genera datos + BD + frontend que los renderiza). No es una lista de bugs conocidos; es el **método de razonamiento** que permite encontrar bugs que *nadie ha identificado todavía*, verificarlos contra la realidad, arreglarlos de raíz y probar que quedaron arreglados.
>
> **Complemento obligatorio:** [`LECCIONES_verificacion_agentes.md`](LECCIONES_verificacion_agentes.md) cubre el caso específico de *verificación visual* (generar la imagen y mirarla). Este documento generaliza esa lección a **todo tipo de bug**.
>
> **Cómo usar este documento:** no lo leas como teoría. Cada técnica trae una *receta concreta* y un *ejemplo real* de esta sesión. Cuando enfrentes una tarea, entra por la sección 10 (protocolo de arranque), y usa las secciones 3–5 como referencia mientras trabajas.

---

## 0. La tesis central: el cambio de mentalidad

Casi todos los bugs profundos que un LLM *no* encuentra tienen la misma raíz: **el agente verifica contra la intención del código, no contra la realidad.** Lee el código, ve que "se ve bien", y lo declara correcto.

Las tres creencias que hay que desactivar:

1. **"El código dice X" ≠ "X realmente pasa".** El código puede *pretender* mostrar una imagen y descartarla dos funciones más abajo. La única prueba de que algo pasa es *observar el efecto*, no leer la causa.
2. **"Funciona en producción" es una hipótesis, no un hecho.** Trátala como algo a *refutar*. En esta sesión, cuatro fases estaban descritas como "funcionales en producción" y en las cuatro era literalmente imposible aprobar un nivel — nadie las había podido completar jamás (0 aprobados en la BD real).
3. **Los comentarios, docstrings y nombres mienten.** Este repo tenía routers de Fase 6/7/8 con docstrings que decían "Fase 2", clases `Fase6*` con texto "Fase 2", y una variable `is_money = (modulo_id == 3)` copiada de una fase donde el módulo 3 *sí* era una tienda. **Nunca razones a partir del comentario; razona a partir del comportamiento.**

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

### C. Feature muerta (UI existe, lógica nunca dispara)
- **Síntoma:** hay un componente/modal/rama de código elaborado que en la práctica jamás aparece.
- **Causa:** la condición que lo activa depende de un dato que nunca se cumple (variantes `es_espejo` que no existen, `estructura_padre_id` NULL, un `tipo` que el seed nunca genera).
- **Detección:** para cada feature con UI, preguntá "¿qué dato la dispara?" y verificá que ese dato *exista* en la BD. `SELECT count(*) WHERE <condición que activa la feature>`. Si da 0, la feature es código muerto.
- **Ejemplo:** el "Bucle Espejo" y el modal de "Rescate" tenían UI completa pero nunca se activaban (sin `estructura_padre_id` ni variantes espejo).

### D. Fuga de respuesta en la figura o el enunciado
- **Síntoma:** el ejercicio es trivial: la imagen/texto contiene la respuesta.
- **Causa:** el generador imprime el planteo resuelto en la figura o dibuja la solución.
- **Detección:** por cada pregunta con figura, preguntá "¿un alumno puede responder solo mirando la imagen, sin razonar?". Renderizá la figura y buscá números/líneas que sean la respuesta.
- **Ejemplos:** el SVG de conversión mostraba `"7 m² = 7 × 10,000 cm²"` (la respuesta es 70000, ya planteada); el componente de termómetro imprimía `"Lectura: 25°C"` en una pregunta que pedía leer el termómetro; las figuras de simetría dibujaban *todos* los ejes → "contar las líneas" en vez de razonar.

### E. Pregunta imposible de responder
- **Síntoma:** el usuario no tiene forma de contestar.
- **Causa:** opción múltiple con **0 alternativas** (grilla vacía + botón Confirmar deshabilitado); o respuesta de **texto** servida como tipo **numérico** (teclado numérico, texto no se puede escribir); o un `tipo_pregunta` que el frontend no renderiza.
- **Detección:** cross-check tipo vs contenido:
  - `... WHERE tipo='multiple_opcion' AND (SELECT count(*) FROM alternativas WHERE pregunta_id=p.id)=0` → opción múltiple sin opciones.
  - `... WHERE tipo='respuesta_numerica' AND respuesta_correcta !~ '^-?[0-9]+([.,][0-9]+)?$'` → respuesta de texto en pregunta numérica.
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
- **⚠️ Trampa:** este mismo bug NO estaba en Fase 7/8 (ahí sí había `else:`). **Casi rompo Fase 7 aplicando el fix de Fase 6 a ciegas.** Ver sección 6.

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
- **0 intentos registrados:** si una fase con tráfico tiene 0 filas en `intentos`, probablemente el endpoint de respuesta está crasheando (arquetipo G).
- **Contenido inflado:** una sección con 4× las filas esperadas → siembras repetidas sin limpieza (deuda de datos).

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

**Cross-check "dice imagen pero no hay imagen":**
```sql
SELECT count(*) FROM preguntas
WHERE fase_id=? AND (enunciado LIKE '%imagen%' OR enunciado LIKE '%Observa%')
  AND NOT (datos_numericos ? 'url');
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
docker exec <backend_prod> grep -c '<marca_distintiva_de_mi_fix>' /app/app/faseN/seed.py
docker exec <backend_prod> sh -c "grep -A12 'SEED_VERSIONS = {' /app/app/seed.py"
psql ... -t -c "SELECT value FROM platform_settings WHERE key='database_seed_versions';"
# si el grep da 0 o las versiones no coinciden → prod corre código viejo
```

---

## 6. Cómo escribir el fix (correcto Y robusto)

1. **Arreglá la raíz, no el síntoma.** El bug de imágenes se arreglaba en el *seed* (preservar `datos_numericos`), no parcheando 451 preguntas a mano. Preguntá "¿de dónde salió este dato malo?" y arreglá ahí.
2. **Garantizá invariantes con un helper, no con parches puntuales.** Para los distractores no arreglé cada colisión; escribí `_finalize_alts`/`_dedupe_and_pad` que *siempre* devuelve 4 opciones distintas con 1 correcta, para cualquier entrada. Un invariante bien puesto mata una familia entera de bugs.
3. **Preservá la pedagogía.** Un fix técnico puede romper el sentido del ejercicio: no filtres la respuesta en la figura, mantené la pregunta respondible, no bajes la dificultad a "contar líneas".
4. **Idempotencia / disparar la re-siembra.** Si el fix vive en datos sembrados, subí la versión de seed (`SEED_VERSIONS`) para que el sistema detecte el cambio y re-siembre. Sin eso, el fix no llega al dato que la app sirve.
5. **⚠️ NUNCA apliques un fix hermano a ciegas.** Casi rompo `fase7/router.py` aplicando el des-indentado que arregló `fase6/router.py`, porque Fase 7 *sí* tenía el `else:` correcto — mi cambio lo destruyó. **Antes de replicar un fix, verificá que la estructura local sea realmente idéntica.** El Edit tool con match exacto sirve de chequeo anti-error: si el texto no coincide, la estructura difiere y hay que mirar.
6. **Cuando toques rangos/plantillas para variedad, re-medí.** Ampliar rangos sin re-consultar la variedad es asumir. Corré la query de variedad después de re-sembrar.
7. **Cuando cambies el TIPO de una respuesta, verificá que el frontend pueda recibirla.** Pasar de numérico a opción múltiple sólo sirve si el frontend renderiza las opciones para ese tipo.

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

---

## 10. Protocolo de arranque para un repo desconocido

Cuando entres a una tarea nueva, hacé esto *antes* de proponer cambios:

1. **Mapeá el stack y los entornos.** ¿Qué es backend/frontend/BD/storage? ¿Hay local/desarrollo/producción separados? ¿Dónde vive el "dato de verdad" (BD dinámica vs archivo estático)? Revisá memoria/CLAUDE.md/docs.
2. **Encontrá el "hermano que funciona".** Si hay N módulos análogos, identificá uno sano; será tu oráculo de "cómo debería ser" para diffs.
3. **Corré las consultas de salud base** (sección 5): distribución de tipos, NULLs en columnas clave, duplicados, variedad, cross-checks "dice X pero el dato es Y". Esto suele destapar 2-3 bugs en la primera pasada.
4. **Elegí una feature y trazala de punta a punta** (sección 2/4.4). Auditá cada frontera.
5. **Señales indirectas** (4.12): ¿alguna fase con 0 aprobados/0 intentos pese a estar "en producción"? Empezá por ahí.
6. **Solo entonces** formulá hipótesis y entrá al bucle de la sección 1.

---

## Apéndice: relación con otros documentos

- **`LECCIONES_verificacion_agentes.md`** — caso profundo de *verificación visual*: por qué un fix de imagen no está terminado hasta generar el artefacto y mirarlo, con checklist de "Definition of Done" visual. Este documento (§4.3, §9) lo incorpora como una técnica; leelo entero antes de tocar generación de imágenes.
- **Memoria del proyecto** (`memory/`) — inventario vivo de bugs concretos ya encontrados y arreglados por fase. Consultalo para no re-descubrir lo ya resuelto; **este** documento es el *método* para encontrar lo que aún no está en esa lista.

> **La idea de una frase:** *no confíes en lo que el código dice que hace — interrogá al dato, mirá el artefacto, jugá el flujo, y no declares nada resuelto hasta que la misma medición que te mostró el bug te muestre que se fue.*
