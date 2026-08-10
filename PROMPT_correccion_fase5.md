# PROMPT — Corrección integral de la Fase 5 (LogicaMath)

## Contexto

Trabajas en el repositorio `D:\Antigravity\APP_Logica_Matematicas_kids`, rama `producion`.
Es una app educativa de matemáticas para niños. La **Fase 5 (Fracciones, Porcentajes y Proporciones)** fue reestructurada por otro agente que la declaró *"Implementado y Verificado"* en `fase5nuevoscambios.md`.

**Esa declaración es falsa.** Una auditoría posterior con ejecución real de código demostró que la fase **no siembra, no responde y no se puede jugar**. El informe completo con 45 bugs numerados, evidencia ejecutada y plan de 7 etapas está en:

> **`fase5_auditoria_y_plan.md`** (raíz del repo) — **LÉELO ENTERO ANTES DE TOCAR NADA.**

Tu tarea es ejecutar ese plan.

---

## Reglas absolutas (no negociables)

1. **NO hagas `git commit` ni `git push`.** Nunca, bajo ninguna circunstancia, sin que el usuario lo pida explícitamente. Deja los cambios en el working tree.
2. **NO declares nada "verificado" sin haber ejecutado el comando y pegado su salida real.** El agente anterior falló exactamente por esto: entregó "11/11 PASSED" sobre una fase que ni siquiera arrancaba. Cada afirmación de éxito debe ir acompañada de la salida literal del comando que la respalda.
3. **Test-first.** Antes de cada corrección, escribe el test que la detecta, ejecútalo y confirma que **falla**. Luego corrige y confirma que pasa. Un test que nunca falló no prueba nada.
4. **No toques otras fases.** Los cambios se limitan a `app/fase5/**`, `tests/test_fase5*`, `scripts/audit_fase5*`, `components/fase5/**` y las entradas `FASE_4`/`FASE_5` de `faseMetadata.ts`. Si detectas un bug fuera de ese perímetro, repórtalo por escrito sin arreglarlo.
5. **No modifiques modelos SQLAlchemy ni migraciones** para acomodar el seed. El seed se adapta al esquema existente, no al revés.
6. **Respeta el orden de etapas.** Las Etapas 1→2→3 son bloqueantes: hasta completarlas nada más es verificable, porque la fase no arranca.
7. **Todo el contenido para el alumno va en español**, con lenguaje apropiado para niños de primaria.
8. **Nada de emojis en el código** ni en los mensajes de log del backend.
9. Si una decisión de producto es ambigua (p. ej. cuántos niveles debe tener el módulo 3), **pregunta antes de implementar**; no elijas en silencio.
10. Trabaja contra el entorno **local**, nunca contra la VPS de producción.

---

## Diagnóstico resumido (detalle completo en `fase5_auditoria_y_plan.md`)

### A. Bloqueantes — la fase no arranca

| ID | Archivo | Problema | Evidencia |
|---|---|---|---|
| BUG-01 | `app/fase5/seed.py:91-101` | `NivelTeoria` recibe `diccionario_clave`, `advertencia_comun`, `ejemplos_json`, `interactivos_json`; las columnas reales son `diccionario`, `advertencia`, `ejemplos`, `interactivos` | `TypeError: 'diccionario_clave' is an invalid keyword argument for NivelTeoria` |
| BUG-02 | `app/fase5/seed.py:192, 240, 285` | `Pregunta` recibe `explicacion=` y `es_activa=`; ninguna de las dos es columna | `TypeError: 'explicacion' is an invalid keyword argument for Pregunta` |
| BUG-03 | `app/fase5/seed.py:109-158` | `ConfiguracionProgreso` recibe `max_errores_tolerados`; la columna es `errores_tolerados` | `TypeError` |
| BUG-04 | `app/fase5/seed.py:113, 119` | `operacion="practica_libre"/"fraccion_visual"/…`; `OperacionEnum` solo admite `suma\|resta\|multiplicacion\|division\|mixta` | `StatementError` |
| BUG-05 | `app/fase5/seed.py:109-158` | `orden_desbloqueo` es NOT NULL sin default y nunca se rellena | `IntegrityError` |
| BUG-06 | `app/fase5/router.py:572` | El pool de práctica filtra `p.datos_numericos.get("variante") == 0`, pero el compositor nunca escribe esa clave → pool vacío → **404 permanente en los 12 bloques de práctica (720 preguntas)** | `404 No hay suficientes preguntas de la variante original (0)` |
| BUG-07 | `app/fase5/schemas.py:93-103` vs `router.py:694,703,744` | `Fase5ResponderPregunta` exige `respuesta_alumno` y no declara `alternativa_id`; el frontend envía `{respuesta_dada, alternativa_id}` y el handler los lee | `ValidationError: respuesta_alumno Field required` |

### B. Contrato roto entre schemas, router y frontend

Los schemas de `app/fase5/schemas.py` se escribieron inventando campos en lugar de espejar los `Fase2*` que el router y `Fase5Types.ts` ya usaban. Verificado con Pydantic 2.13.4:

- `Fase5NivelInfo` no tiene `estado` → `router.py:289` lanza `AttributeError: 'Fase5NivelInfo' object has no attribute 'estado'` → **500 en `/dashboard`**.
- `Fase5DesafioInfo` exige `nivel_id`; el router envía `desafio_id` → `ValidationError`.
- `Fase5Dashboard` exige `alumno_id`; el router envía `alumno_nombre` → `ValidationError`.
- `Fase5ContenidoLectura` exige `contenido_html`; el router envía `parrafos` → **500 en `/lectura`**.
- `Fase5ResultadoRespuesta` perdió `early_exit` y `explicacion_profunda` → se descartan en silencio; mueren la salida temprana del desafío y el modal de rescate.
- `Fase5PreguntaParaAlumno` perdió `aciertos_acumulados`, `intentos_totales`, `porcentaje_actual`, `cantidad_requerida` → la barra de progreso del juego queda en `undefined`.
- `Fase5ModuloInfo` perdió `color`, `estado`, `porcentaje_global`.

### C. Regresión de contenido visual

- El seed anterior tenía **16 bloques SVG**; el actual tiene **cero**. Quedaron muertos 10 componentes del frontend (`PizzaFractionVisualizer`, `PieChartVisualizer`, `BeakerVisualizer`, `PercentageBeaker`, `RatioGridVisualizer`, `FractionPercentageVisualizer`, `ContextualPercentageVisualizer`, `Fase5InteractiveBarChart`, `Fase5FabricVisualizer`, `Fase5NonHomogeneousPolygon`) y el `Fase5VisualizerEngine` que los despacha por `datos_numericos.tipo_visual`.
- La rama de validación `non_homogeneous_polygon` de `router.py:707-728` es código inalcanzable.
- `faseMetadata.ts`: `FASE_5` tiene el título correcto pero **sus 4 módulos son de geometría** (Perímetro, Área en Cuadrícula, Figuras Compuestas, Conversión y Pantallas). `FASE_4` quedó con `modulos: []`.

### D. Errores matemáticos (medidos sobre las 720 preguntas de práctica)

- **BUG-20** `compositor_fase5.py:204-208`: el ajuste de divisibilidad del promedio es incorrecto (`(a+b+c) ≡ c_base mod 3`). **18 de 60 preguntas del bloque 303** publican un promedio redondeado y por tanto falso: *"12, 18 y 13 puntos → 14,33"* (real 14,333…).
- **BUG-21** `compositor_fase5.py:224-227`: `a+b` no divide 100. **26 de 60 del bloque 403**: *"3 ml activo + 4 ml agua → 42,86 %"* (real 42,857…).
- **BUG-22**: porcentajes fraccionarios sobre objetos contables (37,5 juguetes).
- **BUG-23**: la "magnitud" es demasiado gruesa y permite *"En la tienda, **la evaluación** de 50 **puntos** recibe una **rebaja** del 25 %"*.
- **BUG-24**: sin concordancia singular/plural — *"tiene **1 partes** pintadas"*.
- **BUG-25**: respuestas con coma decimal clasificadas como `RESPUESTA_NUMERICA` → el niño debe teclear una coma en un keypad numérico.

### E. Calidad y variedad del banco

- **BUG-26**: **216 de 720 preguntas (30 %) tienen la respuesta impresa literalmente en el enunciado.** 5 plantillas usan fórmulas identidad (`"a"`, `"b"`, `"total"`): *"dividió la pizza en 10 partes y comió **4** partes. ¿Qué numerador representa las partes seleccionadas?"* → respuesta **4**.
- **BUG-27**: solo 2 plantillas por (módulo, nivel). Redacciones distintas por bloque de 60 preguntas: 7, 5, 7, 8, 8, 8, 4, 4, 4, 4, 4, 4 → **repetición de ×7,5 a ×15**. Es el mismo defecto que el commit `4d154fc` corrigió en la Fase 4.
- **BUG-28**: los 12 desafíos son la práctica con el prefijo `"[Desafío] "`, sin salto de dificultad.
- **BUG-29**: el desafío mixto final usa `fam_idx=mod_id` (constante) → 60 preguntas desde 12 redacciones.
- **BUG-30**: `confusiones_fase5.json` se carga en el constructor y **nunca se usa**; los distractores son `c+1, c-1, c*2, c//2, c+2`.
- **BUG-31**: `Alternativa.tipo_error` y `feedback_error` quedan NULL → el "Tutor Invisible" siempre responde `"Respuesta incorrecta."`.
- **BUG-33**: el **Bucle Espejo nunca se activa** — el seed genera una sola pregunta por familia y sin clave `variante`; el log escupe en bucle `"Bucle espejo Fase 4 no pudo activarse"`.
- **BUG-35**: `router.py:219` muestra un nivel `(3,4)` que no existe en `topology.py`, no tiene sección sembrada y `validate_topology` rechaza con 422 → **el módulo 3 nunca se completa → la Fase 5 nunca se gradúa**.
- **BUG-37**: el fallback de `_get_config` busca la sección 0 con `operacion == "mixta"`, pero el seed la crea con `"practica_libre"` → nunca coincide.
- **BUG-38**: el seed no fija `usa_cronometro` / `tiempo_default_segundos` / `tipo_feedback` → los desafíos pierden el cronómetro (25/40/50 s) y la práctica pierde el feedback `detallado`.

### F. El arnés de verificación da falsos positivos

- `tests/test_fase5_vocabulario.py`: `test_respuesta_deriva_de_la_formula` compara `_evaluar_formula()` **consigo misma** — no puede fallar. `test_variedad_estructural_por_nivel` exige `>= 2` firmas, que es exactamente lo que hay. **Ningún test instancia un modelo SQLAlchemy, un schema Pydantic ni un endpoint**, por eso los 7 bloqueantes convivieron con "11/11 PASSED".
- `scripts/audit_fase5_narrativas.py` mide la invariante inversa (que las variables aparezcan en el texto) y no detecta que la respuesta esté impresa.
- `compositor_fase5.py:73` usa `eval()` sobre una cadena que viene de un JSON editable por admin.

---

## Plan de ejecución

### Etapa 1 — Reanimar el seeder · BUG-01…05
1. `seed.py`: renombrar los 4 kwargs de `NivelTeoria` a `diccionario`, `advertencia`, `ejemplos`, `interactivos`.
2. `seed.py`: eliminar `explicacion=`; escribir la explicación en `explicacion_paso_a_paso` (JSONB).
3. `seed.py`: `es_activa=True` → `estado=StatusEnum.ACTIVO` en los 3 bucles de siembra.
4. `seed.py`: `max_errores_tolerados=` → `errores_tolerados=`.
5. `seed.py`: `operacion=OperacionEnum.MIXTA` en las 25 configuraciones; mover la etiqueta pedagógica del módulo a `topology.py`.
6. `seed.py`: añadir `orden_desbloqueo` (1..25) y fijar explícitamente `usa_cronometro`, `tiempo_default_segundos` (0 práctica / 25-40-50 desafíos / 60 mixto), `tipo_feedback` (`detallado` en práctica, `simple` en desafíos), `pistas_permitidas`, `penalizacion_pista_segundos`.

**Puerta de verificación:** `python -m app.fase5.seed` termina sin excepción **y** `SELECT count(*) FROM preguntas WHERE fase_id=5` devuelve 1140. Pega ambas salidas.

### Etapa 2 — Restaurar el contrato de schemas · BUG-07…15
7. Reescribir `app/fase5/schemas.py` espejando **campo a campo** `app/fase2/schemas.py` y `components/fase5/Fase5Types.ts`:
   - `Fase5NivelInfo`: `nivel_id, nombre, descripcion, estado, porcentaje, aciertos, requeridos, usa_cronometro`
   - `Fase5DesafioInfo`: `desafio_id, nombre, dificultad, estado, porcentaje, aciertos, requeridos, tiempo_limite, max_errores`
   - `Fase5ModuloInfo`: `+ color, estado, porcentaje_global`
   - `Fase5Dashboard`: `alumno_nombre, puntos_totales, modulos, desafio_mixto_disponible, desafio_mixto_estado`
   - `Fase5PreguntaParaAlumno`: `+ aciertos_acumulados, intentos_totales, porcentaje_actual, cantidad_requerida`
   - `Fase5ResultadoRespuesta`: `+ early_exit, errores_sesion, max_errores_tolerados, explicacion_profunda`; `respuesta_correcta: Optional[str]`
   - `Fase5ResponderPregunta`: `respuesta_dada: Optional[str]`, `alternativa_id: Optional[int]`; eliminar `respuesta_alumno`
   - `Fase5ContenidoLectura`: `parrafos: List[str]`, `ejemplos`, `tip_pedagogico`, `diccionario`, `interactivos`; eliminar `contenido_html`
8. Añadir `model_config = ConfigDict(extra="forbid")` a los schemas de salida, para que cualquier desajuste futuro falle en el test y no en producción.

**Puerta de verificación:** un test que instancie cada schema con exactamente los kwargs que el router le pasa, y que falle antes del cambio.

### Etapa 3 — Desbloquear el pool y la progresión · BUG-06, 33-41
9. Fijar la topología canónica en **3 niveles × 4 módulos**: eliminar `NIVELES_META[(3,4)]`, cambiar `router.py:219` a `range(1, 4)` y alinear el mensaje de `/graduate` a "12 de práctica, 12 desafíos y 1 mixto". **Confirma esta decisión con el usuario antes de aplicarla.**
10. Renombrar `NIVELES_META` para que describa el contenido real (hoy `(3,2)` dice "Gráficos Circulares" y genera descuentos de tienda).
11. Generar variantes espejo: por familia, 1 original (`variante: 0`) + 3 espejos (`variante: 1..3`) con la misma estructura y números distintos. `estructura_padre_id` **compartido** por la familia (quitar el sufijo `_v{var}`).
12. Escribir `variante` dentro de `datos_numericos` en el compositor → desbloquea BUG-06 y BUG-33 a la vez.
13. Corregir el fallback de `_get_config` (sección 0 con `operacion` coherente).
14. Filtrar el desafío mixto a las secciones de desafío, no a toda la fase.
15. Limpiar el `cat_map` muerto de `_sync_unlocked_levels`.

**Puerta de verificación:** test de integración que recorra `/dashboard → /pregunta → /responder` de un bloque de práctica completo y de un desafío hasta el 100 %.

### Etapa 4 — Corregir la matemática · BUG-20…25
16. M3N3: `c = c_base + ((3 - (a + b + c_base) % 3) % 3)`.
17. M4N3: restringir `(a, b)` a pares cuyo `a+b` divida 100 (`4, 5, 8, 10, 20, 25, 50`).
18. Invariante duro en el compositor: si `resultado_num` no es entero y el escenario no es de tipo `dinero`, se rechaza la composición (fail-closed, igual que R1/R2).
19. Añadir eje `sub_magnitud` (`dinero` | `puntaje` | `conteo` | `volumen`) al contrato R2 → elimina "la evaluación recibe una rebaja".
20. Añadir `singular`/`plural` a los escenarios y un helper de concordancia.
21. Si se conserva alguna respuesta decimal, forzar `MULTIPLE_OPCION` (nunca teclado numérico).

### Etapa 5 — Rehacer el banco de preguntas · BUG-26…32
22. **Eliminar las 5 plantillas identidad** (`formula: "a" | "b" | "total"`) y sustituirlas por preguntas que exijan operación. Si se quiere evaluar lectura de fracción, la respuesta debe ser la fracción (`a/b`), no un número copiado del enunciado.
23. Subir de **2 a 6-8 plantillas por (módulo, nivel)** (de 24 a ~84). Objetivo: repetición ≤ ×2 por bloque.
24. Ampliar escenarios a **6 por módulo** como mínimo (hoy 4/4/2/2) y desacoplar la elección de marco y de escenario (hoy ambas dependen de `var_idx` y quedan correlacionadas).
25. Cablear `confusiones_fase5.json` a `_generar_distractores`: cada distractor debe encarnar un error catalogado y llevar su `tipo_error` y su explicación.
26. Persistir esos metadatos en `Alternativa.tipo_error` y `Alternativa.feedback_error` durante la siembra.
27. Reescribir la explicación como pasos narrados en lenguaje infantil (hoy es `"Resultado obtenido mediante la fórmula: (total/b)*a = 24"`), reutilizando el formato `{"pasos": [{"orden", "texto"}]}` de `theory_examples.py`.
28. Diferenciar los desafíos de verdad: composición de dos operaciones, datos distractores en el enunciado o inversión de la incógnita.
29. Corregir el mixto final: `fam_idx` debe recorrer todas las plantillas, no quedar fijo en `mod_id`.

### Etapa 6 — Recuperar la capa visual · BUG-16…19
30. Volver a emitir `datos_numericos.tipo_visual` para que el `Fase5VisualizerEngine` renderice. Mapa mínimo: M1 → `pizza`, `shapes`, `non_homogeneous_polygon`; M2 → `bar_chart`, `contextual_bar`; M3 → `pie`, `percentage_beaker`, `fraction_percentage`; M4 → `beaker`, `RatioGrid`.
31. Emitir los payloads que cada componente espera (`cortes`, `sombreados`, `sectors[{id,weight,points}]`, `target_value`, `target_fraction_text`, `viewBox`).
32. Rehabilitar la rama `non_homogeneous_polygon` de `/responder` con preguntas que la usen.
33. Recuperar los 16 bloques SVG del seed anterior como base (`git show HEAD:LogicaMath/backend/app/fase5/seed.py`).
34. **Antes de dar por buena la restauración visual, verifica el bug conocido de DOMPurify** (`ALLOWED_URI_REGEXP` borra atributos geométricos del SVG en `textService.ts`); está documentado en `soluconfase5.md`.
35. `faseMetadata.ts`: sustituir los módulos de geometría de `FASE_5` por los 4 reales de fracciones/porcentajes, repoblar `FASE_4.modulos` con decimales y alinear los colores con `MODULOS_META` del backend.

### Etapa 7 — Arnés de verificación real · BUG-42…45 (en paralelo desde la Etapa 1)
36. Tests de contrato: instanciar cada modelo SQLAlchemy con los kwargs exactos del seed (habría atrapado BUG-01…05) y cada schema con los kwargs exactos del router (BUG-08…14).
37. Test de exactitud: toda respuesta de bloque no monetario debe ser entera.
38. Test anti-degenerado: la respuesta correcta no puede aparecer como token aislado en el enunciado.
39. Test de variedad: ≥ 30 redacciones distintas por bloque de 60 preguntas, normalizando números y nombres propios.
40. Test de espejo: cada `estructura_padre_id` tiene exactamente 4 variantes (0..3).
41. Test end-to-end del flujo dashboard → pregunta → responder → graduación.
42. Sustituir `eval()` por un evaluador AST con lista blanca de operadores.
43. Limpiar los residuos textuales de "Fase 4" en `router.py` (líneas 189, 198, 207, 218, 384, 816, 914, 924, 979, 988) y en `Fase5Types.ts:4`.

---

## Definición de "terminado"

No declares la fase corregida hasta que puedas pegar la salida real de **todas** estas comprobaciones:

- [ ] `python -m app.fase5.seed` completa sin excepción, con 1140 preguntas y 25 configuraciones sembradas.
- [ ] `pytest tests/test_fase5*.py` en verde, **incluyendo los tests nuevos que fallaban antes del fix**.
- [ ] `GET /fase5/dashboard` devuelve 200 con 4 módulos, 3 niveles cada uno y 3 desafíos cada uno.
- [ ] `GET /fase5/modulo/1/nivel/1/pregunta` devuelve 200 con una pregunta real (no 404).
- [ ] `POST /fase5/responder` acepta `{respuesta_dada}` y `{alternativa_id}` y devuelve 200.
- [ ] `GET /fase5/lectura/1/nivel/1` devuelve 200.
- [ ] Un alumno de prueba completa un bloque de práctica hasta el 100 % y desbloquea el siguiente.
- [ ] El Bucle Espejo se activa tras un error (sin el warning en el log).
- [ ] 0 respuestas no enteras en bloques no monetarios.
- [ ] 0 preguntas con la respuesta impresa en el enunciado.
- [ ] ≥ 30 redacciones distintas por bloque de 60 preguntas.
- [ ] Al menos un ejercicio con figura por módulo, renderizando en el navegador (adjunta captura o describe la verificación visual real).

## Formato del informe final

Actualiza `fase5nuevoscambios.md` con una bitácora honesta:

- Qué se corrigió, con `archivo:línea`.
- **La salida literal de cada comando de verificación**, no un resumen.
- Qué quedó pendiente y por qué.
- Cualquier bug encontrado fuera del perímetro autorizado, sin arreglarlo.

Si una etapa no se completó, dilo explícitamente. **Una entrega parcial y honesta vale más que una completa y falsa** — el intento anterior falló justamente ahí.
