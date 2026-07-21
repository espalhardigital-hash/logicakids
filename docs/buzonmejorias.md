# Diagnóstico: Buzón de Mejorías UX (Modo Evaluador)

> Documento de insumo para aplicar manualmente la metodología OpenSpec (`openspec/`).
> Fecha del diagnóstico: 2026-07-21. Fase: **descubierta y diagnóstico** — nada de esto fue implementado.
> Reproducción en vivo realizada sobre el entorno local (Fase 4, Módulo 1, Nivel 1) con stack docker levantado.

---

## 1. Qué es la feature y dónde vive

La feature tiene 3 capas + 1 pieza de storage:

| Capa | Archivo | Rol |
|---|---|---|
| **Overlay de captura (usuario)** | `LogicaMath/frontend/components/common/UXFeedbackOverlay.tsx` (+ `.css`) | Botón flotante 💬, solo visible si `role === 'ADMIN'`. Inspecciona el DOM, resalta al hover, captura clic, dispara autocaptura con `html2canvas`, abre modal de reporte, hace `POST /evaluador/feedback`. |
| **API + BD** | `LogicaMath/backend/app/routers/ux_feedback.py`, `LogicaMath/backend/app/models/ux_feedback.py`, `LogicaMath/backend/app/schemas.py` | Persiste en tabla `ux_feedbacks`. Endpoints: crear, listar/filtrar, actualizar estado, subir/servir screenshot. |
| **Storage de imágenes** | `LogicaMath/backend/app/core/storage.py` | Sube a MinIO (S3) con fallback a filesystem local. |
| **Buzón (admin)** | `LogicaMath/frontend/components/admin/UXFeedbackTab.tsx`, montado en `AdminPanel.tsx` | Tabla con filtros (fase/prioridad/estado), modal de detalle, cambio de estado, y un botón que copia el string `antigravity --resolve-ux {id}` (decorativo, sin implementación real). |
| **Export hacia LLM/agente** | `LogicaMath/backend/scripts/export_ux_feedback.py` | Vuelca los feedbacks pendientes a `docs/ux_correcciones_pendientes.json` (solo texto/URLs, no descarga imágenes). |

Montaje del overlay: en `LogicaMath/frontend/App.tsx`, cada `FaseNGameScreenWrapper` (Fase 2 a 9) envuelve la pantalla de juego con `<UXFeedbackOverlay fase={N} moduloId={...} nivelId={...} isAdmin={...}>`.

Spec OpenSpec previo ya existente (no cubre imágenes duales ni pipeline LLM):
`openspec/specs/feedback-ux-evaluador/spec.md`

### Dos "modos admin" que se confunden fácil
- **Modo Evaluador** (toggle en `AdminPanel.tsx`, guardado en `localStorage.evaluatorMode`): solo habilita el botón "Saltar" dentro de los juegos para probar el flujo rápido. No tiene relación directa con el overlay de feedback.
- **Overlay de Feedback** (botón 💬): aparece siempre que el usuario logueado tiene `role === 'ADMIN'`, sin importar si el Modo Evaluador está activado o no.

---

## 2. Flujo funcional actual (usuario → admin)

1. Un usuario con rol **ADMIN** entra a cualquier pantalla de juego (Fase 2-9). Aparece el botón flotante 💬 abajo-izquierda.
2. Clic en 💬 → se activa `isInspecting`. Al mover el mouse se dibuja un recuadro punteado morado (`.ux-hover-highlight`) sobre el elemento bajo el cursor.
3. Clic sobre un elemento:
   - Se calcula un `dom_selector` único vía la función `getUniqueSelector()`.
   - Se guarda el `outerHTML` del elemento.
   - Se dispara una captura automática de pantalla completa con `html2canvas(document.body, ...)`.
   - Se abre el modal de reporte (con o sin la captura, según si `html2canvas` tuvo éxito).
4. En el modal: se elige tipo (`bug_visual`, `texto`, `propuesta_ux`, `rendimiento`), prioridad (`baja/media/alta/critica`), se escribe un comentario, y opcionalmente se reemplaza/agrega una imagen (subida manual o pegada con Ctrl+V).
5. Submit → `POST /evaluador/feedback` con: fase, módulo, nivel, paso, `dom_selector`, `viewport`, comentario, tipo, prioridad, `screenshot_url`, y un bloque `app_state` (JSON con timestamp, URL de la página, el `outerHTML`, y el usuario actual **tal como lo reporta el propio cliente**).
6. El admin abre el tab "Buzón de Mejorías UX", filtra por fase/prioridad/estado, ve el detalle (comentario, captura, HTML renderizado en Shadow DOM, selector copiable), y cambia el estado a `en_desarrollo`, `resuelto` o `rechazado`, dejando notas de desarrollador.

### Cómo se identifica quién reportó — hallazgo
El backend **no persiste quién generó el feedback**. `create_ux_feedback()` en `ux_feedback.py` construye el modelo con `UXFeedback(**payload.model_dump())`, ignorando por completo `current_user` (que sí llega autenticado por JWT vía `get_current_user`). La única "identidad" queda en `app_state.user = {username, role}`, un JSON **enviado por el propio cliente**, no verificado ni indexado. No existe columna `reporter_id`/`created_by` en el modelo `UXFeedback`.

---

## 3. Bugs — estado de confirmación

### 🔴 BUG 1 — Autocaptura de pantalla rota siempre (CONFIRMADO en vivo)
**Síntoma reportado por el usuario:** el recuadro de selección no coincide con el área correcta al hacer clic.
**Causa raíz real encontrada (más específica que la hipótesis inicial):**
En consola del navegador, al clicar cualquier elemento con el inspector activo:
```
Error en captura html2canvas: Error: Attempting to parse an unsupported color function "oklch"
```
El paquete `html2canvas` usado no sabe interpretar el espacio de color `oklch()`, que es el que genera Tailwind 4 (usado en todo el proyecto). Como resultado, **la captura automática de pantalla falla en el 100% de los casos**. El `catch` en `UXFeedbackOverlay.tsx` maneja el error y abre igual el modal, pero **sin imagen adjunta**.

**Ubicación en código:** `UXFeedbackOverlay.tsx`, bloque `handleCaptureClick` (llamada a `html2canvas(document.body, {...})`).

**Nota:** este bug es prerequisito de cualquier trabajo de "Change C" (pipeline LLM) — sin capturas válidas no hay imagen que un agente multimodal pueda leer.

---

### 🔴 BUG 2 — Selector incorrecto + "bucle sin opciones" (CONFIRMADO en vivo — misma causa raíz)
**Síntoma reportado por el usuario:** "a veces cuando se da clic entra en bucle sin opciones" + el elemento seleccionado no es el correcto.

**Reproducción realizada:** con el inspector activo en Fase 4 / Módulo 1 / Nivel 1:
- Clic en la tarjeta "Numerador" (coordenada ≈133,271) → elemento resuelto: `div.f4-start-splash` ("Toca para comenzar").
- Clic en el botón "Siguiente" del modal de teoría (coordenada ≈996,786, zona totalmente distinta) → elemento resuelto: **otra vez** `div.f4-start-splash`.

**Causa raíz confirmada:** existe un overlay a pantalla completa (`div.f4-start-splash`, el cartel "Toca para comenzar" de la pantalla de inicio del nivel) que **intercepta todos los clics** mientras el inspector está activo, sin importar dónde se haga clic realmente. El listener del inspector usa `e.preventDefault()` + `e.stopPropagation()` en fase de captura, por lo que ese overlay **nunca llega a descartarse** con el clic — quedando "atrapado" seleccionando siempre el mismo elemento fantasma. Esto es exactamente el "bucle sin opciones" reportado: el usuario no logra nunca seleccionar el elemento real que quiere reportar.

**Bug secundario relacionado (calidad del selector):** el selector generado en este caso es un path posicional largo y frágil:
```
#root > div.min-h-screen.flex.flex-col > div.flex > div > div.f4-screen-wrapper > div.f4-start-splash...
```
en vez de un selector estable basado en `data-component`/`data-testid`.

**Ubicación en código:** `UXFeedbackOverlay.tsx`, listener `handleCaptureClick` registrado con `window.addEventListener('click', handleCaptureClick, true)` — necesita lógica de "atravesar" overlays de splash/loading que no son parte del contenido a reportar (p. ej. usando `document.elementsFromPoint()` en vez de confiar en `e.target`, o desactivando temporalmente `pointer-events` de overlays conocidos mientras el inspector está activo).

---

### 🟡 BUG 3 — Recuadro de resaltado (highlight) desalineado (análisis estático — no reproducido de forma aislada, tapado por el Bug 2 en el repro)
**Causa raíz (por código):**
- `.ux-hover-highlight` en `UXFeedbackOverlay.css` usa `position: absolute`.
- Sus coordenadas (`top`, `left`, `width`, `height`) se calculan con `getBoundingClientRect()` + `window.scrollY`/`scrollX` — es decir, en **espacio de viewport**.
- `position: absolute` se posiciona respecto al ancestro posicionado más cercano. Ese ancestro, en `App.tsx`, es el contenedor `<div className="... max-w-4xl ... relative ...">` (línea ~507), que está **centrado en la pantalla**, no anclado en `(0,0)`.
- Resultado: el recuadro se desplaza exactamente por el offset de ese contenedor centrado respecto al viewport — el mismo patrón visual que se ve en la captura de pantalla que compartió el usuario.

**Dirección de fix sugerida:** cambiar `.ux-hover-highlight` a `position: fixed` (sin sumar `scrollX`/`scrollY`), o renderizarlo vía portal directo a `document.body`.

**Bug relacionado (mismatch conceptual, independiente del bug de posición):** el recuadro resalta el elemento crudo bajo el cursor (`e.target`), pero `getUniqueSelector()` puede "subir" a un contenedor semántico distinto (buscando `data-component`, clases `.f1-`…`.f9-`, `.modal`, `.card`, etc.). Esto significa que el elemento que se ve resaltado visualmente puede no coincidir con el que finalmente se registra como `dom_selector`.

---

## 4. Almacenamiento de imágenes — ¿es MinIO?

Sí, con matices importantes:

- Endpoint de subida: `POST /evaluador/feedback/upload-screenshot` → `storage_service.upload_feedback_screenshot()` en `storage.py`.
- Intenta subir a **MinIO/S3** primero, con key `screenshots/{uuid}.png`.
- Si S3 no está configurado o falla → **fallback automático a filesystem local** (`app/static/screenshots/`).
- La URL que finalmente se guarda en `screenshot_url`:
  - Si sube a S3 con éxito → URL **pública directa** de MinIO (usa `MINIO_EXTERNAL_ENDPOINT` o `S3_PUBLIC_URL`).
  - Si cae al fallback local → ruta proxy del propio backend: `/evaluador/feedback/screenshots/{uuid}` (esta sí requiere autenticación para leerse via `GET /evaluador/feedback/screenshots/{filename}`, que sabe buscar tanto local como en S3 con credenciales).

**Problema de fiabilidad detectado:** no se encontró ninguna política de bucket pública/anónima en el repo (`docker-compose.local.yml`, `.env` de ningún entorno). El bucket `logicakids` es **privado por defecto**. Esto significa que si la subida cae por la rama de "éxito S3", la URL pública directa que se guarda **puede fallar al cargar** (`AccessDenied`) tanto en el `<img>` del modal de admin como en cualquier intento de descarga externa — mientras que existe una ruta proxy autenticada que sí funcionaría, pero el flujo de subida no la usa.

Estado de datos verificado en el entorno local: bucket MinIO `logicakids` **vacío** (0 objetos) — consistente con que la autocaptura nunca ha funcionado (Bug 1) y que nadie ha podido completar aún un reporte con imagen adjunta real.

---

## 5. ¿El LLM llega a leer la imagen al ejecutar la mejora?

**Hoy: no, automáticamente no.**

- El botón "Comando Automático Antigravity" en `UXFeedbackTab.tsx` solo copia el string `antigravity --resolve-ux {id}` al portapapeles. **No existe ningún CLI, script o handler real** que implemente ese comando en todo el repo (confirmado por búsqueda exhaustiva).
- El script `export_ux_feedback.py` (el único puente real hacia un flujo de agente) exporta a `docs/ux_correcciones_pendientes.json` solamente **texto y URLs** de las capturas — nunca descarga ni adjunta los bytes de la imagen.
- El único script que efectivamente llama a un LLM (`apply_teacher_feedback.py`, en `scripts/`) pertenece a **otro flujo distinto** (feedback docente sobre enunciados de preguntas, tabla `feedback_docente.json`) y le manda a Gemini **solo texto** (`contents: [{parts: [{text: prompt}]}]`), sin ninguna imagen adjunta ni capacidad multimodal habilitada.

**Camino realista para que un agente sí pueda leer la imagen:** dado que el bucket es privado y la URL pública puede no ser accesible externamente, la opción más robusta es que el script de exportación **descargue** las imágenes usando las credenciales S3 (que sí tiene el backend) a una carpeta local (p. ej. `docs/ux_feedback/{id}/actual.png`) y referencie esa ruta local en el JSON — así cualquier agente con acceso al filesystem del repo (como Antigravity, que corre local) puede leerla directamente sin depender de la política del bucket ni de conectividad externa.

---

## 6. Propuesta del usuario: imagen "actual" + imagen "deseada/referencia"

Idea planteada: que al reportar, además de la captura de "cómo está ahora", se pueda adjuntar una segunda imagen mostrando "cómo debería quedar" (tomada de otra app, un ejemplo, o una imagen local).

**Impacto por capa si se implementa:**
- **BD/schema:** hoy `screenshot_url` es una sola columna `String(255)` (`models/ux_feedback.py`, `schemas.py`). No soporta más de una imagen ni roles. Decisión tomada: usar una **columna JSON flexible**, por ejemplo `imagenes = [{url, rol, descripcion}]`, en vez de agregar columnas fijas `screenshot_actual_url` / `screenshot_referencia_url`. Esto permite futuro soporte de N imágenes sin nueva migración.
- **Overlay (usuario):** dos slots en el modal — "Estado actual" (prellenado con la autocaptura, una vez arreglado el Bug 1) y "Referencia / cómo debería verse" (subir archivo o pegar con Ctrl+V, igual que ya existe hoy para una sola imagen).
- **Buzón (admin):** vista comparativa lado a lado en el modal de detalle.
- **Export/LLM:** el JSON de exportación debe incluir ambas imágenes (ya descargadas localmente, ver punto 5) con su rol (`actual` / `referencia`), para que el agente pueda comparar directamente.

---

## 7. Plan de trabajo acordado — 3 changes OpenSpec separados

Se decidió dividir en 3 propuestas independientes (no un único change combinado), dado que mezclan urgencia y riesgo distintos:

### Change A — `fix-ux-inspector-selector` (🔴 Prioridad alta — bloquea el uso actual de la feature)
Alcance:
- **A1.** Resolver el error `oklch` de `html2canvas` (parche/reescritura de colores en `onclone`, o migración a una librería que soporte `oklch` nativamente, ej. `modern-screenshot`/`snapdom`).
- **A2.** Evitar que overlays a pantalla completa (splash de inicio de nivel, loaders, etc.) intercepten y "atrapen" los clics del inspector — usar `document.elementsFromPoint()` o desactivar `pointer-events` de overlays conocidos mientras el inspector está activo.
- **A3.** Corregir el posicionamiento del recuadro de resaltado (`position: fixed` sin sumar scroll, o portal a `document.body`), y asegurar que resalte el mismo elemento que finalmente se registra.
- **A4.** Mejorar la robustez del selector generado (evitar paths posicionales largos cuando existan mejores anclas semánticas).

### Change B — `ux-feedback-dual-image` (🟡 Prioridad media)
- Migración: columna JSON flexible `imagenes` en `ux_feedbacks` (reemplaza o complementa `screenshot_url`).
- Dos slots en el overlay de usuario: actual / referencia.
- Vista comparativa en el detalle del Buzón admin.

### Change C — `ux-feedback-llm-pipeline` (🟡 Prioridad media — depende de que A1 esté resuelto)
- El export descarga las imágenes localmente (usando credenciales S3 ya disponibles en el backend) en vez de solo referenciar URLs.
- Definir un contrato/formato de salida pensado para que un agente multimodal lo consuma directamente (imagen(es) + contexto + comentario).
- Persistir `reporter_id` real (usando `current_user` ya disponible en el endpoint, hoy ignorado) en vez de depender del JSON `app_state.user` enviado por el cliente.
- Normalizar las URLs de imagen para pasar siempre por la ruta proxy autenticada en vez de la URL pública directa de MinIO (evita el problema de bucket privado del punto 4).

---

## 8. Puntos aún abiertos para decidir al redactar cada `proposal.md`

- **Change A:** ¿qué librería reemplaza a `html2canvas` si se decide migrar en vez de parchear (impacto en bundle size / dependencias)?
- **Change A:** ¿lista explícita de overlays "conocidos" a ignorar (splash de nivel, loaders de fase) o detección genérica por z-index/posición fixed a pantalla completa?
- **Change B:** ¿límite de tamaño/cantidad de imágenes por reporte (hoy no hay límite explícito de tamaño de archivo en la subida)?
- **Change C:** ¿el "contrato para agente" debe ser JSON estructurado, Markdown, o ambos? ¿se sigue usando `docs/ux_correcciones_pendientes.json` o se migra a una carpeta por feedback (`docs/ux_feedback/{id}/`)?
- **Change C:** ¿se elimina definitivamente el botón "Comando Automático Antigravity" (hoy decorativo/no funcional) o se implementa realmente un trigger?

---

## Referencias de archivos relevantes (para consulta rápida al redactar los proposals)

- `LogicaMath/frontend/components/common/UXFeedbackOverlay.tsx`
- `LogicaMath/frontend/components/common/UXFeedbackOverlay.css`
- `LogicaMath/frontend/tests/getUniqueSelector.test.ts`
- `LogicaMath/frontend/App.tsx` (montaje del overlay por fase)
- `LogicaMath/frontend/components/admin/UXFeedbackTab.tsx`
- `LogicaMath/frontend/components/admin/AdminPanel.tsx` (tab + toggle Modo Evaluador)
- `LogicaMath/backend/app/routers/ux_feedback.py`
- `LogicaMath/backend/app/models/ux_feedback.py`
- `LogicaMath/backend/app/models/enums.py` (`FeedbackTypeEnum`, `FeedbackStatusEnum`)
- `LogicaMath/backend/app/schemas.py` (`UXFeedbackBase/Create/Update/Response`)
- `LogicaMath/backend/app/core/storage.py` (`upload_feedback_screenshot`, `delete_file`)
- `LogicaMath/backend/scripts/export_ux_feedback.py`
- `LogicaMath/backend/scripts/apply_teacher_feedback.py` (flujo distinto, feedback docente, referencia de cómo ya se llama a Gemini)
- `openspec/specs/feedback-ux-evaluador/spec.md` (spec previo, incompleto respecto a lo diagnosticado)
- Entorno local: `Datos_localhost/.env`, `docs/Pruebas_y_Test_Unitario/docker-compose.local.yml` (config MinIO local, puertos 9100/9101)

---
---

# PARTE II — Contenido OpenSpec listo para materializar

> Todo lo de abajo está redactado en el formato exacto que ya usa este repo (ver `openspec/changes/archive/2026-07-06-feedback-ux-modo-evaluador/`). Los "puntos abiertos" de la Sección 8 ya fueron **resueltos como decisiones tomadas** en cada `design.md`. Para materializarlo, creá una carpeta por change y copiá cada bloque en su archivo.

## Cómo materializarlo en `openspec/`

Para cada change, crear la estructura:

```
openspec/changes/<AAAA-MM-DD>-<nombre-change>/
├── .openspec.yaml
├── proposal.md
├── design.md
├── tasks.md
└── specs/feedback-ux-evaluador/spec.md      # delta (ADDED/MODIFIED Requirements)
```

Los 3 changes **modifican la misma capability existente** `feedback-ux-evaluador` (no crean una nueva). La spec consolidada vive en `openspec/specs/feedback-ux-evaluador/spec.md`; cada change aporta un **delta** que luego se fusiona al archivar.

Orden recomendado de ejecución: **A → C → B** (A desbloquea la captura, C construye el pipeline sobre capturas válidas, B agrega la segunda imagen encima). A puede ir solo; C depende de A1; B es independiente pero se beneficia de A1.

---

# CHANGE A — `fix-ux-inspector-selector`  🔴 Alta

### `.openspec.yaml`
```yaml
schema: spec-driven
created: 2026-07-21
```

### `proposal.md`
```markdown
## Why

El Inspector de Feedback UX (Modo Evaluador) está inutilizable en la práctica. Dos bugs confirmados por reproducción en vivo (Fase 4, Módulo 1, Nivel 1) lo bloquean: (1) la captura automática de pantalla falla en el 100% de los casos porque el `html2canvas` empaquetado no puede parsear los colores `oklch()` que genera Tailwind 4, y (2) un overlay a pantalla completa ("Toca para comenzar", `div.f4-start-splash`) intercepta todos los clics del inspector, de modo que el evaluador siempre selecciona el mismo elemento fantasma y no logra reportar el elemento real — el "bucle sin opciones" reportado. Mientras estos fallos existan, el canal de feedback no cumple su propósito y todo trabajo posterior (imágenes duales, pipeline de IA) carece de base.

## What Changes

- **Motor de captura compatible con CSS moderno**: reemplazar el motor de captura de pantalla por uno que soporte `oklch()` nativamente, con degradación elegante a captura manual si falla.
- **Selección de clic a prueba de overlays**: la interceptación de clics debe atravesar overlays de gate/splash/loader y seleccionar el elemento de contenido real bajo el cursor, sin quedar atrapada en el overlay superior.
- **Resaltado (highlight) alineado**: el recuadro de resaltado debe coincidir exactamente con el elemento bajo el cursor, independientemente del scroll o de contenedores centrados.
- **Selector DOM robusto**: preferir anclas estables (`data-component` / `data-testid`) sobre paths posicionales frágiles.

## Capabilities

### Modified Capabilities
- `feedback-ux-evaluador`: se refuerzan los requisitos de captura de clic, resaltado visual y captura de imagen para garantizar precisión y evitar el atrapamiento por overlays.

## Impact

- **Frontend**: `LogicaMath/frontend/components/common/UXFeedbackOverlay.tsx` (lógica de captura, hit-testing, highlight), `UXFeedbackOverlay.css` (posicionamiento del highlight), `package.json` (posible nueva dependencia de captura), y `data-component` en los contenedores raíz de los `FaseXGameScreen`.
- **Backend / BD**: sin cambios.
```

### `design.md`
```markdown
## Context

La reproducción en vivo confirmó que el inspector es inservible por dos causas concurrentes. La consola arroja `Error: Attempting to parse an unsupported color function "oklch"` en cada intento de captura, y clics en coordenadas totalmente distintas (tarjeta "Numerador" en ~133,271 y botón "Siguiente" en ~996,786) resuelven ambos al mismo `div.f4-start-splash`. Además, el recuadro de resaltado usa `position: absolute` con coordenadas de viewport dentro de un contenedor `.max-w-4xl relative` centrado, lo que lo desplaza.

## Goals / Non-Goals

**Goals:**
- Que la captura automática produzca una imagen válida en pantallas con Tailwind 4 (oklch).
- Que un clic del inspector seleccione el elemento de contenido real, no un overlay de gate/splash/loader.
- Que el recuadro de resaltado coincida pixel a pixel con el elemento bajo el cursor.
- Que el selector generado sea estable ante cambios menores de estructura.

**Non-Goals:**
- No se agregan imágenes duales (eso es Change B).
- No se toca el pipeline de exportación hacia IA (eso es Change C).
- No se rediseña el modal ni el panel de administración.

## Decisions

### 1. Reemplazar el motor de captura por `snapdom` (alternativa: `modern-screenshot`)
- **Decisión**: sustituir `html2canvas` por `snapdom`, que soporta `oklch()` y CSS moderno de forma nativa y produce mejor fidelidad. La captura automática pasa a ser *best-effort*: si falla, el modal se abre igual y el evaluador puede subir/pegar manualmente.
- **Razón**: parchear `html2canvas` reescribiendo oklch→rgb en `onclone` es frágil porque oklch aparece en muchísimas propiedades computadas (color, background, border, shadow, gradientes); mantener ese parche sería una fuente constante de regresiones.
- **Alternativas descartadas**: (a) `modern-screenshot` — válida y equivalente, queda como plan B si `snapdom` da problemas de bundle; (b) parche `onclone` de html2canvas — frágil; (c) eliminar la captura automática y dejar solo manual — pierde el valor de "captura de contexto en un clic".

### 2. Hit-testing con `document.elementsFromPoint()` + skip-list heurística
- **Decisión**: al clicar, en lugar de confiar en `e.target`, usar `document.elementsFromPoint(x, y)` y seleccionar el primer elemento "de contenido", saltando overlays de gate identificados por heurística: elementos que cubren >90% del viewport, sin texto semántico propio relevante, o cuyas clases contengan `splash`, `overlay`, `backdrop`, `loading`, `gate`. El inspector no debe impedir el descarte natural de esos overlays.
- **Razón**: los gates full-screen (splash de inicio, loaders de fase) son la causa raíz confirmada del atrapamiento; hay que "ver a través" de ellos.
- **Alternativas descartadas**: (a) desactivar `pointer-events` temporalmente en una lista fija de overlays conocidos — requiere mantener una lista y es frágil ante nuevos overlays; (b) exigir que el evaluador descarte el splash antes de inspeccionar — mala UX y no resuelve loaders intermedios.

### 3. Recuadro de resaltado con `position: fixed`
- **Decisión**: cambiar `.ux-hover-highlight` a `position: fixed` y usar `rect.top`/`rect.left` **sin** sumar `scrollX`/`scrollY`. El highlight debe rodear el mismo elemento que `elementsFromPoint` seleccionará (no un ancestro distinto).
- **Razón**: `getBoundingClientRect()` ya devuelve coordenadas de viewport; con `fixed` no hay que compensar el contenedor centrado ni el scroll.
- **Alternativas descartadas**: portal a `document.body` con `absolute` + coordenadas de documento — equivalente pero más código y más superficie de error.

### 4. Selector estable con `data-component`
- **Decisión**: `getUniqueSelector` prioriza `data-testid`/`data-component`; como parte del change se agregan atributos `data-component` a los contenedores raíz de cada `FaseXGameScreen` y a los modales/visualizadores clave, para que exista siempre un ancla estable.
- **Razón**: los paths posicionales (`#root > div... > div:nth-child(3)`) se rompen ante cualquier reordenamiento del árbol.
- **Alternativas descartadas**: aceptar paths posicionales (frágiles); usar XPath (frágil y poco legible para grep).

## Risks / Trade-offs

- **[Riesgo] Nueva dependencia de captura**: `snapdom` agrega peso al bundle y una superficie de compatibilidad nueva.
  - *Mitigación*: la captura es best-effort; si la librería falla, el flujo sigue funcionando con subida manual. Validar bundle size en el build.
- **[Riesgo] La skip-list heurística podría saltar un overlay que sí es contenido reportable** (ej. un modal legítimo a pantalla completa).
  - *Mitigación*: la heurística exige varias condiciones combinadas (tamaño + ausencia de semántica + clases de gate); los modales de teoría tienen `data-component` y texto propio, por lo que no son saltados.
- **[Trade-off] Agregar `data-component` toca varios componentes de fase**: más archivos en el diff, pero es cambio aditivo sin riesgo funcional.
```

### `tasks.md`
```markdown
## 1. Motor de captura compatible con oklch

- [ ] 1.1 Evaluar e instalar `snapdom` (o `modern-screenshot` como alternativa) en `LogicaMath/frontend`.
- [ ] 1.2 Reemplazar la llamada a `html2canvas` en `UXFeedbackOverlay.tsx` por el nuevo motor, manteniendo la lógica best-effort (si falla, abrir el modal igual y permitir subida manual).
- [ ] 1.3 **Test de validación**: levantar el frontend local, activar el inspector en Fase 4 (Tailwind 4 / oklch), hacer un reporte y verificar en la consola que NO aparece el error `oklch` y que la imagen se adjunta al modal. Si falla, corregir antes de avanzar.

## 2. Selección de clic a prueba de overlays

- [ ] 2.1 Reemplazar el uso de `e.target` por `document.elementsFromPoint()` con la skip-list heurística de overlays de gate/splash/loader.
- [ ] 2.2 Asegurar que el inspector no impida el descarte natural de esos overlays.
- [ ] 2.3 **Test de validación**: en Fase 4 Nivel 1 con el splash "Toca para comenzar" presente, clicar dos elementos distintos (una tarjeta de teoría y un botón) y verificar que el `dom_selector` resultante corresponde a cada elemento real y NO a `f4-start-splash`. Si falla, corregir antes de avanzar.

## 3. Recuadro de resaltado alineado

- [ ] 3.1 Cambiar `.ux-hover-highlight` a `position: fixed` en `UXFeedbackOverlay.css` y ajustar el cálculo de coordenadas en `UXFeedbackOverlay.tsx` (sin sumar scroll).
- [ ] 3.2 Hacer que el highlight rodee el mismo elemento que se seleccionará al clicar.
- [ ] 3.3 **Test de validación**: mover el mouse sobre varios elementos (con y sin scroll de la página) y verificar visualmente que el recuadro coincide exactamente con el borde del elemento. Si hay desfase, corregir antes de avanzar.

## 4. Selector DOM robusto

- [ ] 4.1 Agregar `data-component` a los contenedores raíz de cada `FaseXGameScreen` y a los modales/visualizadores clave.
- [ ] 4.2 Ajustar/confirmar que `getUniqueSelector` prioriza estas anclas.
- [ ] 4.3 Actualizar `getUniqueSelector.test.ts` con casos de overlay y de ancla `data-component`.
- [ ] 4.4 **Test de validación**: ejecutar `vitest` sobre `getUniqueSelector.test.ts` y verificar que los selectores generados son estables (no posicionales) para los elementos anclados. Si falla, corregir antes de avanzar.
```

### `specs/feedback-ux-evaluador/spec.md` (delta)
```markdown
## MODIFIED Requirements

### Requirement: Captura de clic en el elemento visual
El sistema SHALL interceptar el clic sobre el componente de contenido real bajo el cursor cuando el Inspector de UX esté activo, atravesando overlays de gate, splash o loader a pantalla completa que no formen parte del contenido reportable.

#### Scenario: Clic con overlay de gate presente
- **WHEN** el evaluador tiene el inspector activo y existe un overlay a pantalla completa (por ejemplo, un splash "Toca para comenzar") sobre el contenido del juego, y hace clic sobre un elemento de contenido.
- **THEN** el sistema SHALL seleccionar el elemento de contenido real (no el overlay), desplegar el modal y registrar un `dom_selector` correspondiente a ese elemento.

#### Scenario: Clics en elementos distintos producen selectores distintos
- **WHEN** el evaluador clica dos elementos visualmente distintos de la misma pantalla.
- **THEN** el sistema SHALL producir un `dom_selector` distinto y correcto para cada uno.

## ADDED Requirements

### Requirement: Captura de pantalla compatible con CSS moderno
El sistema SHALL generar una captura de pantalla válida aunque los estilos de la página utilicen funciones de color modernas como `oklch()`; si la captura automática falla, el sistema SHALL abrir el formulario de reporte igualmente y permitir adjuntar una imagen manualmente.

#### Scenario: Captura en pantalla con colores oklch
- **WHEN** el evaluador genera un reporte en una pantalla estilizada con Tailwind 4 (colores `oklch()`).
- **THEN** la captura SHALL completarse sin error y adjuntarse automáticamente al reporte.

#### Scenario: Degradación elegante si la captura falla
- **WHEN** el motor de captura automática falla por cualquier motivo.
- **THEN** el sistema SHALL abrir el modal de reporte sin bloquear al evaluador y permitir subir o pegar una imagen manualmente.

### Requirement: Resaltado visual preciso del elemento
El sistema SHALL dibujar el recuadro de resaltado (highlight) de manera que coincida exactamente con los límites del elemento bajo el cursor, independientemente del scroll de la página o de contenedores posicionados.

#### Scenario: Resaltado con la página desplazada
- **WHEN** el evaluador mueve el cursor sobre un elemento con la página parcialmente desplazada (scroll).
- **THEN** el recuadro de resaltado SHALL rodear exactamente ese elemento, sin desfase.
```

---

# CHANGE B — `ux-feedback-dual-image`  🟡 Media

### `.openspec.yaml`
```yaml
schema: spec-driven
created: 2026-07-21
```

### `proposal.md`
```markdown
## Why

Al reportar una mejoría, el evaluador solo puede adjuntar una imagen ("cómo está ahora"). Falta poder expresar visualmente "cómo debería quedar" (un ejemplo tomado de otra app o una imagen de referencia local). Un par de imágenes actual/referencia comunica la intención de diseño mucho mejor que un párrafo de texto y es directamente consumible por un agente de IA multimodal en la fase de resolución.

## What Changes

- **Modelo de datos multi-imagen**: reemplazar el único `screenshot_url` por una estructura flexible que soporte varias imágenes con rol y descripción.
- **Dos slots en el overlay de usuario**: "Estado actual" (precargado con la autocaptura) y "Referencia / cómo debería verse" (subida manual o pegado).
- **Vista comparativa en el Buzón admin**: mostrar actual y referencia lado a lado en el detalle del reporte.

## Capabilities

### Modified Capabilities
- `feedback-ux-evaluador`: se extiende el modelo de anotación para soportar múltiples imágenes con rol semántico (actual/referencia) y su visualización comparativa.

## Impact

- **Backend / BD**: nueva columna JSON `imagenes` en `ux_feedbacks` (migración Alembic); `models/ux_feedback.py`, `schemas.py`, endpoints en `routers/ux_feedback.py`.
- **Frontend**: `UXFeedbackOverlay.tsx` (dos slots de imagen), `UXFeedbackTab.tsx` (vista comparativa).
- **Compatibilidad**: `screenshot_url` se conserva como espejo legacy del primer elemento con rol `actual`.
```

### `design.md`
```markdown
## Context

Hoy `screenshot_url` es una única columna `String(255)`. La captura automática representa el "estado actual"; no existe forma de adjuntar una imagen de referencia. El usuario pidió explícitamente poder mostrar "cómo está" y "cómo debería ser".

## Goals / Non-Goals

**Goals:**
- Soportar al menos dos imágenes por reporte con rol semántico (`actual`, `referencia`).
- Precargar la imagen `actual` con la autocaptura (una vez que Change A la hace funcionar).
- Permitir adjuntar la imagen `referencia` por subida o pegado.
- Mostrar ambas imágenes comparadas en el panel de administración.

**Non-Goals:**
- No se arregla la captura automática aquí (depende de Change A).
- No se construye el pipeline de exportación a IA (Change C).
- No se soporta edición/anotación sobre las imágenes (fuera de alcance en esta versión).

## Decisions

### 1. Columna JSON flexible `imagenes`
- **Decisión**: agregar `imagenes = [{ "url": str, "rol": "actual"|"referencia", "descripcion": str|null }]` como columna JSON en `ux_feedbacks`. Mantener `screenshot_url` como espejo del primer elemento con rol `actual` para no romper el admin ni datos existentes.
- **Razón**: soporta N imágenes y roles futuros sin nueva migración; no rompe compatibilidad.
- **Alternativas descartadas**: dos columnas fijas `screenshot_actual_url` / `screenshot_referencia_url` — no escala; tabla hija `ux_feedback_images` — sobre-ingeniería para el volumen esperado.

### 2. Límites de subida explícitos
- **Decisión**: máximo 2 imágenes por reporte en esta versión (1 actual + 1 referencia), tamaño máximo 5 MB por imagen, tipos `image/*`. El backend valida y rechaza con 4xx claro.
- **Razón**: hoy no hay límite de tamaño en la subida; conviene acotarlo antes de multiplicar imágenes.
- **Alternativas descartadas**: sin límite (riesgo de abuso/espacio); N imágenes libres (innecesario ahora).

### 3. Precarga de `actual` desde la autocaptura
- **Decisión**: el slot "actual" se precarga con la captura automática; el evaluador puede reemplazarla. El slot "referencia" siempre es manual.
- **Razón**: mantiene el valor de "captura de contexto en un clic" y separa claramente los dos roles.

## Risks / Trade-offs

- **[Riesgo] Migración de datos existentes**: registros previos solo tienen `screenshot_url`.
  - *Mitigación*: la migración puede poblar `imagenes` a partir de `screenshot_url` existente (rol `actual`), o dejar `imagenes` vacío y leer el fallback legacy.
- **[Trade-off] Doble fuente de verdad temporal** (`screenshot_url` + `imagenes`): se acepta durante la transición; documentar que `imagenes` es la fuente primaria.
```

### `tasks.md`
```markdown
## 1. Modelo y migración

- [ ] 1.1 Agregar columna JSON `imagenes` al modelo `UXFeedback` en `models/ux_feedback.py`.
- [ ] 1.2 Crear la migración Alembic y ejecutarla en la BD local; poblar `imagenes` desde `screenshot_url` existente si corresponde.
- [ ] 1.3 Actualizar los esquemas Pydantic (`UXFeedbackBase/Create/Response`) en `schemas.py` para incluir `imagenes` con validación de rol.
- [ ] 1.4 **Test de validación**: test Pytest que cree un feedback con dos imágenes (actual+referencia) vía `POST /evaluador/feedback` y verifique que se persisten y devuelven correctamente. Si falla, corregir antes de avanzar.

## 2. Overlay de usuario — dos slots

- [ ] 2.1 Modificar el modal de `UXFeedbackOverlay.tsx` para exponer dos slots: "Estado actual" (precargado) y "Referencia / cómo debería verse".
- [ ] 2.2 Aplicar los límites de subida (máx 2 imágenes, 5 MB, `image/*`) en cliente y backend.
- [ ] 2.3 **Test de validación**: manual documentado — subir una imagen de referencia además de la actual y verificar que ambas se envían y guardan con su rol. Si falla, corregir antes de avanzar.

## 3. Vista comparativa en el Buzón admin

- [ ] 3.1 Modificar el modal de detalle en `UXFeedbackTab.tsx` para mostrar actual y referencia lado a lado.
- [ ] 3.2 **Test de validación**: abrir en el panel un feedback con dos imágenes y verificar que ambas se renderizan comparadas. Si falla, corregir antes de avanzar.
```

### `specs/feedback-ux-evaluador/spec.md` (delta)
```markdown
## ADDED Requirements

### Requirement: Adjuntar imágenes de estado actual y de referencia
El sistema SHALL permitir al evaluador adjuntar a un reporte hasta dos imágenes con rol semántico: una que represente el estado actual y otra que represente la referencia o resultado deseado.

#### Scenario: Reporte con imagen actual y de referencia
- **WHEN** el evaluador adjunta una imagen de estado actual y una imagen de referencia y envía el reporte.
- **THEN** el sistema SHALL persistir ambas imágenes con su rol (`actual`, `referencia`) y descripción opcional, y el backend SHALL retornar 201.

#### Scenario: Límite de imágenes y tamaño
- **WHEN** el evaluador intenta adjuntar una imagen que excede el tamaño máximo permitido o supera la cantidad máxima de imágenes.
- **THEN** el sistema SHALL rechazar la subida con un mensaje de error claro, sin corromper el reporte.

### Requirement: Visualización comparativa en el panel de administración
El Panel de Administración SHALL mostrar las imágenes de estado actual y de referencia de un reporte de forma comparativa.

#### Scenario: Detalle de feedback con dos imágenes
- **WHEN** el administrador abre el detalle de un feedback que contiene imágenes actual y referencia.
- **THEN** el panel SHALL renderizar ambas imágenes identificadas por su rol.
```

---

# CHANGE C — `ux-feedback-llm-pipeline`  🟡 Media (depende de A1)

### `.openspec.yaml`
```yaml
schema: spec-driven
created: 2026-07-21
```

### `proposal.md`
```markdown
## Why

Hoy no existe un camino real para que un agente de IA "lea" el feedback y sus imágenes al resolver una mejora: el botón "Comando Automático Antigravity" solo copia un string decorativo (`antigravity --resolve-ux {id}`) sin implementación, el exportador vuelca únicamente URLs de texto, y el bucket MinIO es privado, por lo que esas URLs pueden no ser accesibles. Además, no se persiste quién reportó cada feedback. Este cambio construye un pipeline reproducible que empaqueta cada reporte (contexto + comentario + imágenes descargadas localmente) en un formato que un agente multimodal puede consumir directamente.

## What Changes

- **Descarga local de imágenes**: el exportador descarga las imágenes de cada feedback (con credenciales S3 del backend) a una carpeta local por reporte.
- **Paquete de contexto para agente**: generar, por reporte, un artefacto legible por IA (Markdown + JSON) con fase/módulo/nivel/selector/comentario y rutas locales de imágenes.
- **Identidad real del reportante**: persistir `reporter_id` desde el usuario autenticado en vez del JSON `app_state.user` enviado por el cliente.
- **Normalización de URLs de imagen**: servir siempre las imágenes vía la ruta proxy autenticada en lugar de la URL pública directa de MinIO.
- **Comando de resolución real**: reemplazar el string decorativo por un comando/script que genere el paquete de contexto de un feedback puntual.

## Capabilities

### Modified Capabilities
- `feedback-ux-evaluador`: se añade el pipeline de exportación consumible por IA, la identidad persistida del reportante y la normalización de acceso a imágenes.

## Impact

- **Backend**: `scripts/export_ux_feedback.py` (descarga de imágenes + generación del paquete), `routers/ux_feedback.py` (persistir `reporter_id`, servir vía proxy), `models/ux_feedback.py` + migración (`reporter_id`), `core/storage.py` (helper de descarga).
- **Frontend**: `UXFeedbackTab.tsx` (reemplazo o eliminación del botón "Comando Automático Antigravity").
- **Docs/salida**: nueva carpeta `docs/ux_feedback/{id}/` con imágenes y artefacto de contexto.
```

### `design.md`
```markdown
## Context

El único script que llama a un LLM (`apply_teacher_feedback.py`) es de otro flujo (feedback docente) y manda solo texto. El buzón UX no tiene pipeline de IA real. El bucket `logicakids` es privado (sin policy pública en el repo), así que las URLs directas de MinIO pueden dar `AccessDenied`. El agente Antigravity corre en local y puede leer el filesystem del repo.

## Goals / Non-Goals

**Goals:**
- Que un agente multimodal pueda leer, por cada feedback pendiente, su comentario, contexto e imágenes sin depender de conectividad externa ni de la política del bucket.
- Persistir de forma confiable quién reportó cada feedback.
- Que las imágenes sean accesibles de forma consistente (proxy autenticado).

**Non-Goals:**
- No se implementa la ejecución automática de las correcciones por IA (el agente sigue resolviendo a nivel de código fuente en local).
- No se arregla la captura (Change A) ni se agregan imágenes duales (Change B); C consume lo que esos produzcan.

## Decisions

### 1. Descargar imágenes a `docs/ux_feedback/{id}/`
- **Decisión**: el exportador descarga cada imagen usando el cliente S3 autenticado del backend a `docs/ux_feedback/{id}/{rol}.png`, y referencia esas rutas locales en el artefacto de salida.
- **Razón**: el bucket es privado; una ruta local elimina la dependencia de policy pública y de red, y es directamente legible por el agente local.
- **Alternativas descartadas**: hacer el bucket público o usar URLs prefirmadas (decisión de infra/seguridad, no la tomamos aquí); seguir con URLs de texto (no legibles por el agente).

### 2. Artefacto de contexto Markdown + JSON por feedback
- **Decisión**: generar `docs/ux_feedback/{id}/instruccion.md` (legible para el agente: contexto + comentario + referencias a imágenes locales) y mantener el `ux_correcciones_pendientes.json` como índice estructurado.
- **Razón**: el Markdown con rutas de imagen locales es lo que un agente multimodal consume mejor; el JSON sirve de índice para automatización.
- **Alternativas descartadas**: solo JSON (menos legible para el agente); solo Markdown (peor para automatización/índice).

### 3. Persistir `reporter_id` desde el usuario autenticado
- **Decisión**: agregar columna `reporter_id` a `ux_feedbacks` y poblarla en `create_ux_feedback` desde `current_user` (ya disponible en el endpoint, hoy ignorado). El `app_state.user` del cliente queda solo como dato informativo.
- **Razón**: la identidad debe venir del token, no de un JSON manipulable por el cliente.
- **Alternativas descartadas**: seguir confiando en `app_state.user` (spoofeable, no consultable).

### 4. Normalizar acceso a imágenes vía proxy autenticado
- **Decisión**: el `screenshot_url`/`imagenes[].url` que se sirve al panel y se usa en export apunta a la ruta proxy autenticada `GET /evaluador/feedback/screenshots/{filename}` en vez de la URL pública directa de MinIO.
- **Razón**: funciona con bucket privado y unifica local y S3 bajo un mismo acceso autenticado.
- **Alternativas descartadas**: exponer el bucket públicamente (riesgo de seguridad fuera de este alcance).

### 5. Comando de resolución real (reemplaza el string decorativo)
- **Decisión**: reemplazar el botón que copia `antigravity --resolve-ux {id}` por uno que copie/dispare un comando real que genera el paquete de contexto de ese feedback puntual (o eliminarlo si se prefiere invocar solo el export global). Decisión por defecto: **reemplazar por un script real dirigido a un id**.
- **Razón**: hoy induce a error (parece automatización, no hace nada).

## Risks / Trade-offs

- **[Riesgo] Las imágenes en `docs/` no deben commitearse** (pueden ser pesadas o sensibles).
  - *Mitigación*: agregar `docs/ux_feedback/` a `.gitignore` (coherente con la regla del repo de no versionar artefactos de datos).
- **[Riesgo] Migración de `reporter_id`**: registros antiguos no tienen reportante.
  - *Mitigación*: columna nullable; backfill best-effort desde `app_state.user` si existe.
- **[Trade-off] El proxy autenticado agrega un salto** frente a servir la imagen directa: se acepta a cambio de fiabilidad con bucket privado.
```

### `tasks.md`
```markdown
## 1. Identidad del reportante

- [ ] 1.1 Agregar columna `reporter_id` (nullable) al modelo `UXFeedback` y migración Alembic.
- [ ] 1.2 Poblar `reporter_id` desde `current_user` en `create_ux_feedback`.
- [ ] 1.3 **Test de validación**: Pytest que cree un feedback autenticado y verifique que `reporter_id` corresponde al usuario del token (no al `app_state.user`). Si falla, corregir antes de avanzar.

## 2. Normalización de acceso a imágenes

- [ ] 2.1 Hacer que las URLs devueltas por la subida y servidas al panel usen la ruta proxy autenticada.
- [ ] 2.2 **Test de validación**: subir una imagen con S3 activo y verificar que la URL resultante es servible por el backend autenticado (no depende de policy pública del bucket). Si falla, corregir antes de avanzar.

## 3. Pipeline de exportación para IA

- [ ] 3.1 Extender `export_ux_feedback.py` para descargar, por cada feedback pendiente, sus imágenes a `docs/ux_feedback/{id}/{rol}.png` con el cliente S3 autenticado.
- [ ] 3.2 Generar `docs/ux_feedback/{id}/instruccion.md` (contexto + comentario + rutas locales de imágenes) y mantener el índice `ux_correcciones_pendientes.json`.
- [ ] 3.3 Agregar `docs/ux_feedback/` a `.gitignore`.
- [ ] 3.4 Reemplazar el botón "Comando Automático Antigravity" en `UXFeedbackTab.tsx` por un comando real dirigido a un id (o eliminarlo).
- [ ] 3.5 **Test de validación E2E**: dejar un feedback con imagen, correr el export, y verificar que en `docs/ux_feedback/{id}/` existan las imágenes descargadas y el `instruccion.md` con el contexto y el comentario exactos. Si algún eslabón falla, corregir hasta que el ciclo completo sea afirmativo.
```

### `specs/feedback-ux-evaluador/spec.md` (delta)
```markdown
## ADDED Requirements

### Requirement: Identidad persistida del reportante
El sistema SHALL registrar la identidad del evaluador que crea cada feedback a partir del usuario autenticado, no de datos provistos por el cliente.

#### Scenario: Feedback creado por un evaluador autenticado
- **WHEN** un evaluador autenticado envía un reporte de feedback.
- **THEN** el sistema SHALL persistir su identidad (`reporter_id`) derivada del token de autenticación.

### Requirement: Acceso confiable a las imágenes de feedback
El sistema SHALL servir las imágenes de feedback a través de una ruta autenticada que funcione independientemente de la política de acceso público del almacenamiento de objetos.

#### Scenario: Imagen almacenada en bucket privado
- **WHEN** una imagen de feedback se almacena en un bucket S3/MinIO privado.
- **THEN** el panel de administración y el pipeline de exportación SHALL poder recuperarla vía la ruta proxy autenticada sin requerir acceso público al bucket.

### Requirement: Paquete de contexto consumible por un agente
El sistema SHALL producir, para cada feedback pendiente, un paquete de contexto local que incluya sus metadatos, comentario e imágenes descargadas, legible por un agente de IA multimodal sin depender de conectividad externa.

#### Scenario: Exportación de feedbacks pendientes
- **WHEN** se ejecuta el proceso de exportación de feedbacks pendientes.
- **THEN** el sistema SHALL generar, por cada feedback, un artefacto local con su contexto, comentario y las imágenes (estado actual y referencia) descargadas a rutas locales.
```

---

## Checklist final antes de mover un change a "activo"

- [ ] Los 4 archivos (`proposal.md`, `design.md`, `tasks.md`, `specs/feedback-ux-evaluador/spec.md`) creados bajo `openspec/changes/<fecha>-<nombre>/`.
- [ ] `.openspec.yaml` presente con `schema: spec-driven` y `created`.
- [ ] Cada requisito redactado con `SHALL` + al menos un `#### Scenario` con `WHEN`/`THEN`.
- [ ] Cada bloque de `tasks.md` termina con un "Test de validación" (patrón del repo).
- [ ] Al archivar el change, fusionar el delta en `openspec/specs/feedback-ux-evaluador/spec.md`.
