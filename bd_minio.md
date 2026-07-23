---
name: sync-bd-minio-preguntas
description: >
  Skill guía para sincronizar el BANCO DE PREGUNTAS y sus RECURSOS MULTIMEDIA
  (imágenes/figuras) desde el entorno LOCAL hacia una VPS (Desarrollo o Producción),
  preservando de forma absoluta los datos de usuarios, alumnos, administradores y
  puntajes. Documento GENÉRICO: no contiene datos de conexión; el usuario debe
  suministrarlos en tiempo de ejecución. Soporta sincronización TOTAL o PARCIAL
  (por fase / sección / operación / IDs).
metadata:
  type: reference
  domain: infra / data-migration
  scope: preguntas + alternativas + MinIO graphics/
---

# Skill — Sincronización de Base de Datos (Preguntas) y MinIO (Local → VPS)

> **Objetivo:** Migrar el banco de preguntas y sus figuras asociadas desde el entorno
> local hacia el servidor VPS, manteniendo la **integridad absoluta** de los datos de
> los usuarios, alumnos, administradores y puntajes.
>
> **Este documento es GENÉRICO.** No incluye host, puertos, claves ni dominios reales
> de la VPS. Antes de actuar, **el LLM debe solicitar al usuario todos los datos de
> conexión** (ver §2) y **nunca** hardcodearlos ni commitearlos.

---

## 0. Cómo usar esta skill

Cuando el usuario pida "subir/sincronizar las preguntas (o una sección) a producción/desarrollo",
sigue este flujo:

1. **Pregunta el ALCANCE** (§1.2): ¿toda la base o solo una parte? (fase / sección / operación / IDs).
2. **Solicita los DATOS DE CONEXIÓN** (§2). No continúes sin ellos.
3. **Ejecuta un PRE-VUELO (dry-run)** que solo compara y reporta (§5, Fase 1). No escribas nada todavía.
4. **Muestra el plan** al usuario (cuántas se insertarán / actualizarán / se borrarán huérfanas / se preservarán)
   y **pide confirmación explícita** antes de cualquier escritura o borrado.
5. Ejecuta la sincronización en el orden seguro (§5) y **verifica** (§5, Fase 5).

> Todo borrado (DB o MinIO) es una operación difícil de revertir sobre un entorno de
> producción. **Requiere confirmación del usuario** y debe ir precedido por el pre-vuelo.

---

## 1. Modelo mental: ¿qué es "una pregunta" aquí?

### 1.1 Anatomía de una pregunta

Una pregunta **no es una sola fila**. Es un conjunto de tres cosas que viajan juntas:

| Pieza | Dónde vive | Notas |
|---|---|---|
| El enunciado y metadatos | tabla **`preguntas`** | 1 fila por pregunta (PK `id`) |
| Las opciones de respuesta | tabla **`alternativas`** | N filas con FK `pregunta_id` |
| La figura/imagen (si aplica) | **MinIO**, prefijo **`graphics/`** | La URL se guarda en `preguntas.datos_numericos['url']` |

El vínculo pregunta ↔ imagen es **`preguntas.datos_numericos` (JSONB) → campo `url`**.
Ejemplo del contenido de `datos_numericos`:

```json
{ "url": "https://<dominio-público>/<bucket>/graphics/8f3a...e21.png", "tipo_visual": "imagen", "a": 4, "b": 3 }
```

El nombre físico del objeto en MinIO es el **último segmento** de esa URL, siempre bajo
`graphics/` (ej. `graphics/8f3a...e21.png`). El `filename` (UUID) es idéntico en todos los
entornos; **lo único que cambia entre local y VPS es el dominio y el nombre del bucket**
dentro de la URL (ver §4.2).

### 1.2 Alcance: TOTAL o PARCIAL

El usuario pudo haber modificado **solo una sección**, no toda la base. La skill debe
soportar un **filtro de alcance** que se aplica de forma idéntica a la lectura local, a
la comparación con la VPS y a la detección de huérfanas:

- **Total:** todas las preguntas.
- **Por fase:** `WHERE fase_id = :fase`
- **Por bloque:** `WHERE fase_id = :fase AND seccion = :seccion AND operacion = :operacion`
- **Por familia de variantes:** `WHERE estructura_padre_id = :padre`
- **Por IDs explícitos:** `WHERE id = ANY(:ids)`

> **Regla de oro del alcance:** la detección de "preguntas huérfanas a borrar en la VPS"
> (§5, Fase 3.C) debe restringirse **al mismo filtro de alcance**. Si el usuario sincroniza
> solo la Fase 5, **jamás** consideres huérfanas a las preguntas de otras fases.

---

## 2. Datos que el usuario DEBE suministrar (genéricos — pídelos siempre)

No hay valores por defecto seguros para producción. Solicita y confirma:

**Túnel / acceso VPS**
- `<VPS_SSH_USER>@<VPS_HOST>` y comando de túnel SSH (o acceso directo si aplica).

**Base de datos VPS (PostgreSQL)**
- `<VPS_DB_HOST>` (normalmente `localhost` a través del túnel), `<VPS_DB_PORT>`,
  `<VPS_DB_NAME>`, `<VPS_DB_USER>`, `<VPS_DB_PASSWORD>`.

**Base de datos LOCAL**
- URL/parametros de la DB local (típicamente vía `.env.local`).

**MinIO / S3 VPS**
- `<PROD_S3_ENDPOINT>` (endpoint API para subir/borrar),
  `<PROD_S3_PUBLIC_URL>` (dominio público que se escribe dentro de las URLs de la DB),
  `<PROD_S3_ACCESS_KEY>`, `<PROD_S3_SECRET_KEY>`, `<PROD_S3_BUCKET>`.

**MinIO / S3 LOCAL**
- Endpoint local (host vs. dentro de Docker), keys y `<LOCAL_S3_BUCKET>`.

**Alcance** (§1.2): total, o los filtros concretos.

> **Túnel típico** (el usuario aporta usuario/host/puertos reales):
> ```bash
> ssh -L <PUERTO_LOCAL_TUNEL>:localhost:<PUERTO_DB_REMOTO> <VPS_SSH_USER>@<VPS_HOST> -N
> ```
> El proyecto usa la convención de puertos: `5433` = Postgres local del host, `5434` = túnel a
> Desarrollo, `5435` = túnel a Producción. Confírmalos con el usuario; no los asumas.

> **Seguridad:** nunca escribas estos valores en el repositorio, en logs ni en este
> documento. Consúmelos de los `.env` que el usuario indique o pásalos en memoria.

---

## 3. Mapa real de la base de datos

### 3.1 Tablas del DOMINIO DE PREGUNTAS (las únicas que esta skill sincroniza)

**`preguntas`** — banco principal. Columnas relevantes:
`id`, `fase_id`, `seccion`, `sub_nivel`, `estructura_padre_id`, `operacion`,
`tipo_pregunta`, `enunciado`, `respuesta_correcta`, `datos_numericos` (JSONB, **contiene `url`**),
`payload_tokenizado` (JSONB), `explicacion_paso_a_paso` (JSONB), `requiere_subrayado`,
`palabras_clave` (JSONB), `errores_previstos` (JSONB), `creado_por`/`modificado_por`
(FK → `users.id`), `estado`, `revisado_admin`, `revisado_por`, `fecha_revision`,
`fecha_creacion`, `ultima_modificacion`.

**`alternativas`** — opciones de opción múltiple. Columnas:
`id`, `pregunta_id` (FK → `preguntas.id`), `texto`, `es_correcta`, `orden`, `tipo_error`,
`feedback_error`, `fecha_creacion`, `ultima_modificacion`.

> **Bancos relacionados pero SEPARADOS** (no sincronizar salvo que el usuario lo pida
> explícitamente, y siguiendo las mismas reglas de preservación): `simulado_questao`
> (preguntas de simulacros, autocontenidas) y `niveles_teoria_pool` (teoría, no preguntas).

### 3.2 Tablas PROHIBIDAS (⚠️ nunca leer para modificar, nunca escribir, nunca borrar)

Estas contienen usuarios, administradores, alumnos y **puntajes/progreso**:

| Tabla | Contiene |
|---|---|
| `users` | **Usuarios y administradores** (`role='ADMIN'`). Datos personales + auth. |
| `alumnos` | Perfiles pedagógicos de alumnos. |
| `intentos` | Historial de respuestas (**puntajes**). |
| `progreso_maestria` | Progreso/dominio por bloque (**puntajes**). |
| `pool_asignado_alumno` | Preguntas asignadas a cada alumno (**progreso**). |
| `intento_preguntas`, `intento_pasos` | Intentos multi-paso (Fase 2). |
| `simulado_sessions` | Sesiones de simulacros de alumnos. |
| `configuracion_progreso` | Reglas de negocio del admin. |
| `ux_feedbacks` | Feedback de UX (datos de usuarios). |
| `audit_logs`, `platform_settings` | Auditoría y configuración de plataforma. |

> `fases` es una tabla estructural **compartida** (referenciada por FK). Trátala como
> **solo lectura**: no la modifiques ni la borres.

### 3.3 Dependencias de FK hacia `preguntas` (clave para el BORRADO SEGURO)

Verificado en el esquema. Toda pregunta puede estar referenciada por:

- `alternativas.pregunta_id` → **propiedad de la pregunta** (se borra junto con ella).
- `pool_asignado_alumno.pregunta_id` → **progreso de alumno** (BLOQUEA el borrado).
- `intentos.pregunta_id` → **puntaje/historial** (BLOQUEA el borrado).
- `intento_preguntas.pregunta_id` → **intentos Fase 2** (BLOQUEA el borrado).

Además: `intentos.alternativa_id` → `alternativas.id`. Esto implica que **no puedes borrar
una alternativa** si algún `intento` la referencia (ver trampa §7.3).

**Una pregunta de la VPS solo es "borrable con seguridad" si NO existe en ninguna de las
tres tablas de progreso** (`pool_asignado_alumno`, `intentos`, `intento_preguntas`).
Si tiene aunque sea un registro asociado → **se preserva intacta** (borrarla destruiría
puntajes de alumnos).

---

## 4. Mapa de MinIO / S3

### 4.1 Prefijos (el "namespace" del bucket)

| Prefijo / patrón | Contenido | ¿Sincronizar? |
|---|---|---|
| `graphics/<uuid>.<ext>` | **Figuras de preguntas** | ✅ **SÍ — único ámbito permitido** |
| `<uuid>.<ext>` (raíz del bucket) | **Avatares / fotos de perfil** | 🚫 **NUNCA** (datos personales) |
| `screenshots/<uuid>.<ext>` | Capturas de UX Feedback | 🚫 **NUNCA** (datos personales) |

> **Toda operación de MinIO de esta skill se limita al prefijo `graphics/`.** Al listar,
> subir o borrar, usa siempre `Prefix='graphics/'`. Nunca toques la raíz ni `screenshots/`.

### 4.2 Reescritura de URL por entorno (¡obligatoria!)

El objeto físico conserva la misma key (`graphics/<uuid>.<ext>`) en todos los entornos,
pero la URL guardada en `datos_numericos.url` **incluye el dominio y el bucket**, que
difieren entre local y VPS. Al insertar/actualizar una pregunta en la VPS, **reescribe**
la URL:

```
<PROD_S3_PUBLIC_URL>/<PROD_S3_BUCKET>/graphics/<mismo-uuid>.<ext>
```

Conserva el `<uuid>.<ext>` exacto (así la fila apunta al objeto ya subido). Si copias
`datos_numericos` verbatim del local, la URL quedará apuntando al bucket/dominio local y la
imagen **no cargará** en la VPS. (Este es el propósito del script `update_db_urls.py`.)

---

## 5. Procedimiento paso a paso (el algoritmo de la skill)

Orden seguro global: **PRE-VUELO → subir imágenes → sincronizar DB (transacción) →
limpiar imágenes huérfanas → verificar.** (Subir antes de escribir la DB garantiza que las
URLs resuelvan; borrar imágenes al final evita eliminar una figura aún referenciada.)

### Fase 0 — Preparación
- Recibe alcance (§1.2) y datos de conexión (§2).
- Abre túneles SSH. Verifica conectividad a **ambas** DBs y **ambos** MinIO.
- Convierte la URL de DB async (`+asyncpg`) a síncrona si usas `psycopg2`, y codifica `#`
  de contraseñas como `%23` (ver helpers en los scripts existentes).

### Fase 1 — PRE-VUELO (dry-run, solo lectura, NO escribe)
Compara local vs VPS **dentro del alcance** y reporta:
- Preguntas locales que **faltan** en la VPS → se **insertarán**.
- Preguntas presentes en ambas → según la **política de conflicto** (ver Fase 3.B).
- Preguntas en la VPS que **ya no están** en local (dentro del alcance) → candidatas a
  borrado; de estas, cuántas son **borrables** vs **preservadas** (por tener progreso).
- Figuras `graphics/` locales que faltan en la VPS → se **subirán**.
- Figuras `graphics/` en la VPS no referenciadas por ninguna pregunta válida → candidatas a limpieza.

Reutiliza `scripts/compare_environments.py` como base. **Muestra el plan y pide confirmación.**

### Fase 2 — Sincronización de imágenes (MinIO `graphics/`)
- Determina el conjunto de figuras a subir: los `filename` extraídos de
  `datos_numericos.url` de las preguntas **dentro del alcance** (o todo `graphics/` si es total).
- Sube local → VPS **solo** las que faltan (idempotente; re-subir es inocuo pero evítalo).
- Trabaja en lotes con reintentos. **No borres nada aquí** (la limpieza va en Fase 4).
- Base reutilizable: `scripts/sync_minio_vps.py` (soporta `--fase5-only`; generalízalo al alcance pedido).

### Fase 3 — Sincronización de DB (`preguntas` + `alternativas`), en UNA transacción con rollback

**A. Leer** local (dentro del alcance): preguntas + sus alternativas. Leer de la VPS los
`id` existentes (dentro del alcance).

**B. Insertar/actualizar según la POLÍTICA DE CONFLICTO** (confírmala con el usuario):
- **`insert-new` (por defecto, más seguro — coincide con la regla "dejar intacta"):**
  inserta solo las preguntas locales que **no existen** en la VPS. Las que ya existen se
  **dejan intactas** (no sobrescribir, no duplicar).
- **`upsert` (solo si el usuario quiere empujar cambios de una sección que editó):**
  además actualiza las existentes. ⚠️ Si actualizas, **no reescribas las `alternativas`
  de preguntas que ya tienen `intentos`** (rompería `intentos.alternativa_id`, §7.3):
  para esas, actualiza solo la fila `preguntas` y conserva sus alternativas.

  > **Matching de identidad:** ambas políticas asumen que el `id` identifica la misma
  > pregunta en ambos entornos (linaje común por seed). **Verifícalo** antes (§7.1). Si los
  > `id` divergieron, empareja por firma de contenido (`fase_id`+`seccion`+`operacion`+
  > `enunciado`+`respuesta_correcta`) o por `estructura_padre_id`, no por `id`.

- Al insertar, **reescribe `datos_numericos.url`** al dominio/bucket de la VPS (§4.2).
- **FK `creado_por` / `modificado_por` → `users.id`:** si el admin referenciado **no existe**
  en `users` de la VPS, pon esos campos en `NULL` (nunca insertes usuarios). Ver §7.2.
- Serializa correctamente los campos **JSONB** (`datos_numericos`, `payload_tokenizado`,
  `explicacion_paso_a_paso`, `palabras_clave`, `errores_previstos`).

**C. Borrado seguro de huérfanas** (VPS-en-alcance − local-en-alcance): para cada
candidata, comprueba las 3 tablas de progreso (§3.3):
```sql
SELECT EXISTS (
  SELECT 1 FROM pool_asignado_alumno WHERE pregunta_id = :id
  UNION ALL SELECT 1 FROM intentos           WHERE pregunta_id = :id
  UNION ALL SELECT 1 FROM intento_preguntas  WHERE pregunta_id = :id
);
```
- Si **existe** progreso → **preserva** (no borres). Cuéntala como "preservada".
- Si **no** → borra primero sus `alternativas`, luego la `pregunta`.

**D. `commit`** al final; ante cualquier error, **`rollback`** (la DB es transaccional).

Base reutilizable: `scripts/sync_db_and_minio_prod.py` (revísalo a la luz de §7: por
defecto hace `upsert` + reescritura de alternativas + copia `datos_numericos` verbatim
sin reescribir la URL; ajústalo a la política y a la reescritura de URL antes de usarlo en prod).

### Fase 4 — Limpieza de imágenes huérfanas en MinIO (post-commit)
Solo **después** de un `commit` exitoso de la DB:
- Recolecta el conjunto de `filename` referenciados por **TODAS** las preguntas válidas de
  la VPS (no solo las del alcance — una figura del alcance podría compartirse con una
  pregunta fuera de alcance).
- Lista `graphics/` en la VPS; **borra solo** las keys que **no** estén referenciadas por
  ninguna pregunta. Nunca toques raíz ni `screenshots/`.
- Si tienes dudas sobre una key, **no la borres** (la limpieza es opcional; el objetivo
  primario es que no falten imágenes).

### Fase 5 — Verificación
- Re-ejecuta la comparación (`compare_environments.py`) y confirma 0 faltantes en el alcance.
- Verifica integridad física con HEAD sobre MinIO (patrón de `scripts/verify_minio_integrity.py`):
  toda pregunta visual debe tener su objeto presente en la VPS.
- Reporta al usuario: insertadas / actualizadas / preservadas / borradas / imágenes subidas /
  imágenes huérfanas eliminadas.

---

## 6. Reglas críticas (la caja roja) — ⚠️ INVIOLABLES

**En la base de datos, PROHIBIDO** leer-para-modificar, alterar, insertar o borrar en:
`users` (usuarios **y administradores**), `alumnos`, `intentos`, `progreso_maestria`,
`pool_asignado_alumno`, `intento_preguntas`, `intento_pasos`, `simulado_sessions`,
`configuracion_progreso`, `ux_feedbacks`, `audit_logs`, `platform_settings`.
Solo consulta `pool_asignado_alumno`/`intentos`/`intento_preguntas` en modo **lectura**
para decidir si una huérfana es borrable (§3.3), nunca para escribir.

**Nunca borres una pregunta de la VPS que tenga progreso/intentos de alumnos.** Preservar
puntajes tiene prioridad sobre limpiar huérfanas.

**En MinIO, PROHIBIDO** tocar, modificar o borrar avatares (objetos en la raíz del bucket)
y `screenshots/`. Toda operación se limita a `graphics/`.

**Dominio confinado:** tu permiso se limita a `preguntas`, `alternativas` y al prefijo
`graphics/`. Cualquier otra tabla o prefijo está fuera de alcance.

**Confirmación humana:** todo borrado (DB o MinIO) y toda escritura en producción requiere
el pre-vuelo (§5, Fase 1) y confirmación explícita del usuario.

---

## 7. Trampas conocidas (pitfalls) — léelas antes de escribir en producción

### 7.1 El `id` puede no significar lo mismo en ambos entornos
El emparejamiento por `id` solo es válido si local y VPS comparten linaje (mismo seed).
Si divergieron, un `id` local puede corresponder a una pregunta distinta en la VPS →
sobrescribirías/borrarías la equivocada. **Verifica el linaje** (compara enunciados de
algunos `id` comunes en el pre-vuelo) antes de confiar en el `id`; si no coinciden, empareja
por firma de contenido o `estructura_padre_id`.

### 7.2 FK a `users` al insertar preguntas
`preguntas.creado_por` y `modificado_por` referencian `users.id`. Si insertas una pregunta
cuyo admin creador **no existe** en la VPS, el `INSERT` **falla por FK**. Solución: pon esos
campos en `NULL` cuando el usuario no exista en la VPS. **Jamás** crees usuarios para "arreglarlo".

### 7.3 Borrar `alternativas` de una pregunta con intentos rompe FK
`intentos.alternativa_id` referencia `alternativas.id`. Un patrón de "borrar e reinsertar
alternativas" (como hace el script actual en cada upsert) **falla** si algún alumno respondió
esa pregunta. Por eso la política `upsert` **no** debe reescribir alternativas de preguntas
con `intentos`; y estas preguntas, además, están preservadas por §3.3 si fueran huérfanas.

### 7.4 URL con bucket/dominio incorrecto
Copiar `datos_numericos` verbatim deja la `url` apuntando al bucket/dominio local → imagen
rota en la VPS. **Reescribe siempre** (§4.2).

### 7.5 Alcance en la detección de huérfanas
Detectar huérfanas sobre **toda** la VPS cuando el usuario solo sincroniza una sección
borraría preguntas de otras secciones. **Restringe la detección al alcance** (§1.2).

### 7.6 Limpieza de figuras huérfanas contra el conjunto global
Antes de borrar una key de `graphics/`, verifica que **ninguna** pregunta de la VPS
(de cualquier fase/sección) la referencie. Una figura puede compartirse.

### 7.7 MinIO no es transaccional
Si la DB hace `rollback`, las imágenes ya subidas quedan (inocuo: son huérfanas que la
Fase 4 puede limpiar). Nunca borres imágenes antes del `commit` de la DB.

### 7.8 Endpoints local: host vs Docker
El endpoint del MinIO local difiere si corres desde el host (`http://localhost:<puerto>`)
o dentro de un contenedor (`http://minio:9000`). Confirma cuál aplica.

---

## 8. Scripts existentes reutilizables (en `LogicaMath/backend/scripts/`)

| Script | Qué hace | Uso en esta skill |
|---|---|---|
| `compare_environments.py` | Compara preguntas/alternativas y figuras `graphics/` entre local, dev y prod. | **Pre-vuelo (Fase 1)** y verificación (Fase 5). |
| `sync_minio_vps.py` | Sube figuras `graphics/` de local a la VPS (`--env dev/prod`, `--fase5-only`). | **Fase 2** (generalizar el filtro al alcance). |
| `sync_db_and_minio_prod.py` | Sincroniza imágenes + `preguntas`/`alternativas`, con borrado seguro de huérfanas. | Base de **Fase 3** — **ajústalo** por §7.1/§7.2/§7.3/§7.4 (política de conflicto y reescritura de URL) antes de prod. |
| `update_db_urls.py` | Reescribe las URLs de `datos_numericos` al dominio/bucket destino. | Referencia para la **reescritura de URL (§4.2)**. |
| `verify_minio_integrity.py` | HEAD-check de que cada pregunta visual tiene su objeto en MinIO. | **Verificación (Fase 5)**. |
| `audit_question_images.py` | Audita y **autogenera** figuras faltantes (procedimental/Gemini). | Opcional: sanear figuras faltantes en local **antes** de sincronizar. |

> Estos scripts contienen valores específicos del entorno (endpoints/keys/buckets).
> **Parametrízalos** con los datos que aporte el usuario (§2); no reutilices credenciales
> hardcodeadas ni las copies a este documento.

---

## 9. Checklist final de seguridad

- [ ] Alcance definido y confirmado (total o filtros concretos).
- [ ] Datos de conexión suministrados por el usuario (nada hardcodeado).
- [ ] Túneles y conectividad a ambas DBs y ambos MinIO verificados.
- [ ] Pre-vuelo (dry-run) ejecutado; plan mostrado; **confirmación explícita** obtenida.
- [ ] Imágenes `graphics/` subidas (solo faltantes) — sin tocar raíz ni `screenshots/`.
- [ ] DB sincronizada en transacción; política de conflicto aplicada; URLs reescritas;
      FK a `users` en `NULL` cuando corresponde.
- [ ] Huérfanas **con progreso preservadas**; solo borradas las verdaderamente seguras.
- [ ] Limpieza de figuras huérfanas contra el conjunto global (post-commit) — opcional y prudente.
- [ ] Verificación (compare + HEAD) sin faltantes en el alcance.
- [ ] Tablas de `users`, `alumnos`, puntajes/progreso, avatares y `screenshots/` **intactas**.
- [ ] Reporte final entregado al usuario.
