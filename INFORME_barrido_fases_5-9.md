# Informe — Barrido y reformulación de Fases 5 a 9

> **Fecha:** 2026-08-17 (trabajo nocturno autónomo)
> **Alcance:** `LogicaMath/backend` — solo entorno **local** (VPS ignorada, como se pidió).
> **Método:** verificación contra **verdad de terreno** (Postgres local real), siguiendo `razonamiento_profundo.md`. Se levantó el stack local (Postgres 5433 / Redis 6380 / MinIO 9100), se sembró cada fase contra la BD real y se auditó con un script propio de arquetipos de bug.
> **Sin commit** (regla del repo). **Sin cambios en frontend** salvo lo indicado (no hubo).

---

## Resumen ejecutivo

| Fase | Estado inicial | Resultado |
|---|---|---|
| **5** Fracciones/%/Proporciones | Jugable pero con **bug crítico latente** | ✅ Bug crítico corregido + pulido. 34/34 tests. |
| **6** Geometría/Volumen | Sana (reparada antes) | ✅ Verificada sana, sin bugs. |
| **7** Tiempo/Coordenadas | Sana, banco repetitivo | ✅ Verificada + variedad mejorada en 3 secciones. |
| **8** (usuario) Lógica/Combinatoria/Probabilidad | Motor genérico (contenido estático) | ✅ Contenido auditado y sano; seed backend huérfano reparado. |
| **9** (usuario) Simulados Colegio Pedro II | **Doblemente roto** (inalcanzable + sin sembrar + stub) | ✅ Alcanzable + sembrado + **banco real de 20 preguntas**. |

**Los dos "milagros" de la noche:**
1. **Fase 5** tenía un bug que devolvía **500 en toda respuesta incorrecta** (crash al leer de la BD).
2. **Fase 9 (Simulados)** estaba **inalcanzable** para el alumno (otro router la tapaba), **no se sembraba** nunca, y su contenido era un **stub de 3 preguntas** (una en portugués e incontestable). Ahora es una fase real.

---

## FASE 5 — Fracciones, Porcentajes y Proporciones

### 🔴 Bug CRÍTICO corregido: `tipo_error` inválido → crash al leer (500 en cada fallo)
- **Síntoma:** al responder **mal** cualquier pregunta, el "Tutor Invisible" del router lee la alternativa elegida por ORM. La columna `Alternativa.tipo_error` es un `Enum(TipoErrorEnum)`.
- **Causa raíz:** `confusiones_fase5.json` etiquetaba los distractores con valores como `inversion`, `multiplicacion`, `porcentaje_err`, `total_incorrecto`… que **no son miembros de `TipoErrorEnum`**. SQLAlchemy 2.0 (`validate_strings=False`) los **guardaba crudos**, pero al **leer** la fila validaba contra el enum y lanzaba `LookupError`. Verificado: **3.420 alternativas** afectadas; cargar cualquiera por ORM crasheaba.
- **Nota:** un intento previo sin commitear (`tipo_error[:20]`) solo evitaba el error de longitud, **no** el de enum — no resolvía el crash.
- **Fix:** `confusiones_fase5.json` remapeado a miembros válidos (`inversa`, `operacion_incorrecta`, `problema_incompleto`, `division`, `calculo`, `lectura`) — el detalle pedagógico se conserva en `feedback_error`. Añadida **coerción defensiva** `_coerce_tipo_error()` en `compositor_fase5.py` y `seed.py` (blindaje ante futuras ediciones del JSON).
- **Verificado:** 4.560 alternativas se cargan por ORM **sin error**; valores en BD ahora consistentes con el resto de la app (`CALCULO`, `DIVISION`, …).

### 🟠 Pulido de calidad
- **6 respuestas degeneradas** (la respuesta era un literal del enunciado, p.ej. "Divide entre **2**" → respuesta 2). El guard solo miraba los tokens `{...}`, no las **constantes literales** del marco. Añadidos los literales del marco al conjunto de números "visibles" → **0 degeneradas**.
- **4 concordancias de artículo** ("las 1 parte tomadas"). Añadida regla de concordancia artículo+1 en `_normalizar_texto` → **0**.

### Verificación Fase 5
`1140 preguntas / 4560 alternativas`. 0 no-enteros, 0 texto-en-numérico, 0 duplicados, 0 doble-correcta, 0 degeneradas, progreso posible (estructura_padre_id OK), variedad práctica 50-73%. **34/34 tests** en verde.

### Pendiente (mejora, no bug)
- **Capa visual (`tipo_visual`)**: las preguntas interactivas siguen sin figura (0/1140). La teoría sí tiene SVG (8/12 niveles). Es la Etapa 6 del `fase5_auditoria_y_plan.md`, un trabajo de contenido amplio, no un bloqueante de juego.

---

## FASE 6 — Geometría Espacial, Volumen y Magnitudes

**Auditada sana** (reparada en sesiones previas). `9150 preguntas`. Verificado contra Postgres real:
- Sin `tipo_error` inválido, sin duplicados, sin doble-correcta, progreso OK (1800 familias × 4 variantes), lectura ORM OK.
- **0 preguntas que digan "observa/figura" sin imagen embebida** (el viejo bug de imágenes está resuelto).
- Las 1.920 respuestas decimales (círculos con π) **son contestables**: el teclado tiene botón decimal y `normalize_response` normaliza coma↔punto.
- Las "degeneradas" que marca una auditoría genérica son **falsos positivos** (el número aparece dentro del markup del SVG embebido, no en texto legible; contar vértices de la figura ES el objetivo).

**Única limitación (contenido, no bug):** pocas figuras SVG distintas por sección (5-12), muy reutilizadas. Mejorarlo requiere generar más figuras geométricas — no se hizo esta noche.

---

## FASE 7 — Tiempo, Coordenadas y Frecuencias

**Auditada sana.** `480 preguntas`. Sin bugs críticos (enum válido, progreso OK, sin duplicados/doble-correcta).
- Las preguntas de "elige entre 3 opciones A/B/C" tienen 3 alternativas **por diseño** (no es bug).

### 🟢 Mejora de banco aplicada
3 secciones puramente de texto tenían **una sola redacción** (variedad 5%). Se añadieron **4 fraseos** por sección (mismo patrón `plantillas`+`rng.choice` que ya usan las secciones de alta variedad):
- **202** (traslación de coordenadas): robot / mapa del tesoro / nave…
- **303** (suma de tiempos): viaje / película / estudio / tren…
- **401** (frecuencia): autobús / tren / metro…

Variedad de esas secciones: **5% → 20%** (4× más fraseos, además de la variación numérica). La sección 301 (reloj) ya tiene **imagen SVG variable**, así que su texto redundante no es problema.

---

## FASE 8 (del usuario) — Lógica, Combinatoria y Probabilidad

**Importante:** en `App.tsx`, la Fase 8 del usuario se renderiza con el **motor genérico** (`FaseGenericGameScreen`), con contenido **estático** en `faseMetadata.ts` (`FASE_8`, 🎲). No usa un seed de backend.

- **Contenido auditado (56 preguntas):** 0 opciones duplicadas, 0 respuesta ausente de opciones, 0 respuestas numéricas con la respuesta impresa, 0 respuestas de texto en preguntas de teclado numérico. Estructuralmente **sano**.
- Menor: 5 enunciados de ejercicios interactivos repetidos entre niveles (redundancia de curación, no bug).

### Reparación colateral (backend huérfano)
El `fase_id=8` de backend ("Secuencias/Combinatoria", en `app/fase9/seed_fase8.py`) está **huérfano** (App.tsx no lo enruta), y su seed **crasheaba** por un import equivocado (`from app.fase8.content_fase8` → el archivo está en `app/fase9/`). Corregido para que no rompa el sembrado maestro.

---

## FASE 9 (del usuario) — Simulados Colegio Pedro II

Era la fase en peor estado. Tres problemas encadenados, todos corregidos:

### 🔴 1. Inalcanzable (route shadowing)
`app/fase9/router.py` (sirve `fase_id=8`) y `app/fase11/router.py` (sirve `fase_id=9`, los Simulados reales) declaraban **las mismas rutas** `/fase9/*`. `fase9_router` se registraba **primero** en `main.py` → ganaba la resolución → el frontend de Simulados (`fase11`, que llama a `/fase9`) recibía contenido de `fase_id=8` (vacío). **Verificado** resolviendo el handler real de `/fase9/dashboard`.
- **Fix:** en `main.py` se **desregistraron** los routers huérfanos `fase8_router` y `fase9_router` (restos de una renumeración; ningún componente vivo del frontend los usa). Verificado: `/fase9/dashboard` ahora resuelve **solo** a `app.fase11.router` (Simulados).

### 🔴 2. Nunca se sembraba
El sembrador maestro (`app/seed.py`) importaba de rutas inexistentes (`app.fase9.seed_fase9`, `app.fase8.seed_fase8`) → capturaba el error y **omitía** Fase 8 y Fase 9 en cada deploy.
- **Fix:** corregidas las importaciones a las reales (`app.fase11.seed_fase9`, `app.fase9.seed_fase8`).

### 🔴 3. Contenido = stub de 3 preguntas
`seed_fase9.py` generaba las 200 preguntas eligiendo al azar entre **3 preguntas hardcodeadas** (una en **portugués** e incontestable: "volume do sarcófago" sin números), con un tag `[Qi]` contaminando el enunciado y explicación "automática".
- **Fix:** creado **`app/fase11/banco_simulados.py`** — banco de **20 preguntas reales** basadas en el análisis del examen CMRJ (`coelgiomilitar.md`), adaptadas al español, con respuesta **verificada**, 3 distractores pedagógicos (varios encarnan las "trampas" del examen) y explicación. La distribución ahora entrega **10 preguntas DISTINTAS por simulacro** (muestreo sin reemplazo) y variedad entre secciones.
- Temas cubiertos: media, sistema métrico, fracciones de cantidad, % del remanente, cubo pintado, romanos, dado, primos, poliedros (V+C+A), MCM, fracción irreducible, calendario modular, promedio, MCD, perímetro, área compuesta (L), redondeo de latas, fracción continua, potencias de 10.

### Verificación Fase 9
`200 preguntas / 800 alternativas`. 0 duplicados, 0 doble-correcta, 0 degeneradas, 0 portugués, 0 tag `[Q`, todas 4 opciones, ORM OK. Progreso por `aciertos_acumulados` (correcto para un examen). 10 preguntas distintas por sección.

---

## Archivos modificados / creados

**Backend (modificados):**
- `app/fase5/data/confusiones_fase5.json` — tipos de error a enum válido
- `app/fase5/compositor_fase5.py` — coerción de enum + guard de literales del marco + concordancia de artículo
- `app/fase5/seed.py` — coerción defensiva de `tipo_error`
- `app/fase7/seed_fase7.py` — variedad de fraseo en secciones 202/303/401
- `app/fase9/seed_fase8.py` — import `content_fase8` corregido
- `app/main.py` — desregistrados routers huérfanos fase8/fase9 (des-shadowing de Simulados)
- `app/seed.py` — imports de seed de Fase 8 y 9 corregidos

**Backend (nuevos):**
- `app/fase11/banco_simulados.py` — banco real de Simulados (contenido de producción)
- `_local_runner.py`, `_audit_fase.py` — **herramientas de verificación local** (crear esquema + seed + auditoría sin Docker). Se pueden borrar; las dejé por si quieres re-verificar.

## Cómo re-verificar (local, sin Docker backend)
Con el stack local levantado (`Datos_localhost/docker-compose.local.yml` → postgres/redis/minio):
```bash
cd LogicaMath/backend
export DATABASE_URL='postgresql+asyncpg://logicakids_local_user:LogicaKids2026%23Local@localhost:5433/logicakids_local'
export S3_ENDPOINT_URL='http://localhost:9100' REDIS_URL='redis://localhost:6380/0' ENVIRONMENT=local
python _local_runner.py seed 9    # siembra una fase (5..9)
python _audit_fase.py 9           # audita arquetipos de bug
```

## Recomendaciones (para cuando revises)
1. **Limpieza de la renumeración 8/9/10/11**: los directorios `app/fase8` y `app/fase9` (backend) y `components/fase8`, `components/fase9` (frontend) son huérfanos. Conviene eliminarlos en una tarea dedicada para evitar futuras confusiones.
2. **Fase 5 capa visual** (Etapa 6 del plan) si se quiere cerrar el déficit visual.
3. **Fase 6/7 variedad de figuras/fraseo** si se quiere subir aún más la riqueza del banco.
4. Bug menor multiplataforma: `main.py` línea ~51 imprime `❌` en el `except` de `create_all`, lo que crashea en consolas no-UTF8 (solo afecta Windows; Docker/Linux va con UTF-8).
