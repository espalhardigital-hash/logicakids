# Mejoras Pendientes — Fase 2 y Fase 3

> **Estado:** Bloque 1 (Fase 4) ya fue implementado y verificado (ver commits/working tree y memoria `known_bugs_fase2_a_4.md`). Este documento cubre **lo que falta**: Bloque 2 (Fase 2) y Bloque 3 (Fase 3), completo con instrucciones exactas para ejecutarlo sin necesidad de re-diagnosticar nada.
>
> **Contexto general:** diagnóstico hecho el 2026-07-21 sobre `D:\Antigravity\APP_Logica_Matematicas_kids\LogicaMath`. Entorno de trabajo: Docker local (`docs/Pruebas_y_Test_Unitario/docker-compose.local.yml`), contenedores `logicakids_local_*`. El backend **no monta el código como volumen** — cualquier cambio en `backend/` o `frontend/` requiere `docker compose build <servicio>` + recrear el contenedor antes de que se vea reflejado (ver sección "Cómo aplicar y verificar" al final).
>
> Decisiones ya tomadas con el usuario (no volver a preguntar):
> - El código muerto de Fase 3 (`OperationBuilder`/`DetectiveNotebook`, tipo `constructor_operaciones`) se **elimina**, no se completa.
> - `isEvaluatorMode`/`handleEvaluatorSkip` en Fase 3 **NO es un bug** — es el modo de previsualización del admin (`StudentViewSimulator`), usado igual en las 9 fases vía `PlayRouteWrapper.tsx`. No tocar.
> - `TipoErrorEnum` usa `native_enum=False` (`app/models/progreso.py:231`, `app/models/pregunta.py:145`) → es un `VARCHAR` validado en Python, no un enum nativo de Postgres. Ampliarlo **no requiere migración Alembic**.
>
> ⚠️ **Salvedad sobre los números de línea:** todos los números de línea citados en este documento son del **2026-07-21**. Si entre esa fecha y la ejecución de este plan alguien más modifica `router.py`, `seed.py`, `Fase3GameScreen.tsx` u otros archivos de Fase 2/3, las líneas pueden haberse corrido y ya no coincidir exactamente. Por eso cada ítem incluye también el **código/fragmento de texto exacto** a modificar — antes de editar, buscar (grep) ese fragmento textual en el archivo actual para confirmar su ubicación real, en vez de asumir que sigue en el número de línea indicado.

---

## Bloque 2 — Fase 2

### 2.1 — Taxonomía de `TipoErrorEnum` rota (P1, analítica pedagógica)

**Problema:** en `LogicaMath/backend/app/fase2/router.py` línea ~918:
```python
tipo_error = TipoErrorEnum(tipo_error_str) if hasattr(TipoErrorEnum, tipo_error_str) else TipoErrorEnum.CALCULO
```
`hasattr(TipoErrorEnum, tipo_error_str)` compara contra el **nombre** del atributo (mayúsculas: `CALCULO`, `IMPULSO`...), pero `tipo_error_str` viene del pool sembrado en minúsculas (`"impulso"`, `"parentesis"`, etc.). Nunca coincide → **todo error cognitivo se registra siempre como `CALCULO`**, perdiendo la taxonomía pedagógica sembrada.

**Strings reales sembrados en `LogicaMath/backend/app/fase2/seed.py`** (grep de `tipo_error`/`errores_previstos`): `"impulso"`, `"parentesis"`, `"calculo"` (único que ya matcheaba), `"inversa"`, `"balanza"`, `"decimal"`, `"vuelto"`, `"suma_decimal"`, `"presupuesto"`, `"distractor"`.

**Fix — Paso 1:** en `LogicaMath/backend/app/models/enums.py`, ampliar `TipoErrorEnum` (definición actual, 11 miembros):
```python
class TipoErrorEnum(str, enum.Enum):
    CALCULO = "calculo"
    LECTURA = "lectura"
    ATENCION = "atencion"
    OPERACION_INCORRECTA = "operacion_incorrecta"
    NO_IDENTIFICA_DATOS = "no_identifica_datos"
    PROBLEMA_INCOMPLETO = "problema_incompleto"
    TABUADA = "tabuada"
    DIVISION = "division"
    VALOR_POSICIONAL = "valor_posicional"
    TROCO = "troco"
    INFERENCIA = "inferencia"
```
Agregar al final, antes del cierre de la clase:
```python
    IMPULSO = "impulso"
    PARENTESIS = "parentesis"
    INVERSA = "inversa"
    BALANZA = "balanza"
    DECIMAL = "decimal"
    VUELTO = "vuelto"
    SUMA_DECIMAL = "suma_decimal"
    PRESUPUESTO = "presupuesto"
    DISTRACTOR = "distractor"
```

**Fix — Paso 2:** en `router.py:918`, reemplazar:
```python
tipo_error = TipoErrorEnum(tipo_error_str) if hasattr(TipoErrorEnum, tipo_error_str) else TipoErrorEnum.CALCULO
```
por:
```python
tipo_error = TipoErrorEnum(tipo_error_str) if tipo_error_str in TipoErrorEnum._value2member_map_ else TipoErrorEnum.CALCULO
```

**Riesgo:** ninguno — no requiere migración (columna es `VARCHAR` validado en Python). Verificar que `Alternativa.tipo_error` (`app/models/pregunta.py:145`) y `Intento.tipo_error` (`app/models/progreso.py:231`) siguen aceptando los nuevos valores (deberían, mismo enum).

---

### 2.2 — Módulo 4 (Constructor) nunca dispara el rescate/explicación (P1, UX de aprendizaje)

**Problema:** hay dos bloques relacionados con el "Bucle Espejo" en `router.py`:

- **Bloque A** (selección de pregunta espejo, dentro de `get_pregunta_fase2`, líneas ~679-722): NO filtra por `modulo_id` — ya sirve preguntas espejo al Módulo 4 sin restricción.
- **Bloque B** (cálculo de `soporte_avanzado`, dentro de `responder_fase2`, líneas ~1236-1254):
```python
espejo = False
intentos_espejo = 0
soporte_avanzado = False

if not es_correcta and modulo_id in (1, 2, 3) and pregunta.estructura_padre_id:
    res_fam = await db.execute(
        select(Intento)
        .join(Pregunta, Intento.pregunta_id == Pregunta.id)
        .where(and_(
            Intento.alumno_id == alumno.id,
            Pregunta.estructura_padre_id == pregunta.estructura_padre_id
        ))
        .order_by(Intento.fecha.desc(), Intento.id.desc())
    )
    family_attempts = res_fam.scalars().all()
    intentos_espejo = len(family_attempts)

    espejo = intentos_espejo > 0
    soporte_avanzado = intentos_espejo >= (MAX_ESPEJO + 1)
```
La condición `modulo_id in (1, 2, 3)` excluye explícitamente el Módulo 4 → un alumno que falla repetidamente en el Constructor de Soluciones **nunca** recibe la explicación de rescate (`soporte_avanzado` queda en `False` para siempre), aunque el Bloque A sí le sigue sirviendo variantes espejo.

**Fix:** quitar la restricción de módulo en el Bloque B:
```python
if not es_correcta and pregunta.estructura_padre_id:
```
(dejar el resto de la lógica igual).

**Verificación manual sugerida:** en el navegador, fallar 4 veces seguidas la misma familia de preguntas en Módulo 4 de Fase 2 y confirmar que aparece el modal/explicación de rescate (como ya pasa en Módulos 1-3).

---

### 2.3 — Eliminar código muerto `generators.py` (P2, limpieza)

**Archivo:** `LogicaMath/backend/app/fase2/generators.py` (553 líneas).

Confirmado por grep en todo `backend/`: **0 imports** de este módulo (`from .generators`, `from app.fase2.generators`, etc. no aparecen en ningún otro archivo). Toda la generación real de preguntas de Fase 2 ocurre en `app/fase2/seed.py`. `generators.py` duplica lógica pedagógica con un formato de `errores_previstos` incompatible con el usado en producción.

**Fix:** eliminar el archivo completo. No requiere ningún otro cambio (nada lo referencia).

---

### 2.4 — Doble-submit / condición de carrera en `/responder` (P2)

**Problema:** `LogicaMath/frontend/components/fase2/Fase2Service.ts` ya define y usa `fetchDeduplicated` (líneas ~38-50) en `getFase2Dashboard`, `getFase2Question` y `getFase2Reading`, pero **no** en `submitFase2Answer` (líneas ~85-94):
```typescript
export async function submitFase2Answer(
  payload: Fase2AnswerPayload
): Promise<Fase2AnswerResult> {
  const res = await fetchWithTimeout(`${API_URL}/fase2/responder`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  });
  return handleResponse<Fase2AnswerResult>(res);
}
```
Un doble-click o retry de red puede disparar dos POST casi simultáneos para la misma pregunta, duplicando aciertos/intentos.

**Fix:**
```typescript
export async function submitFase2Answer(
  payload: Fase2AnswerPayload
): Promise<Fase2AnswerResult> {
  const key = `answer-${payload.pregunta_id}`;
  return fetchDeduplicated(key, async () => {
    const res = await fetchWithTimeout(`${API_URL}/fase2/responder`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(payload),
    });
    return handleResponse<Fase2AnswerResult>(res);
  });
}
```
**Nota:** la key usa solo `pregunta_id` (no la respuesta), a propósito — colapsa reenvíos accidentales de la misma pregunta en vuelo, sin bloquear el envío de la siguiente pregunta real una vez cargada.

---

### 2.5 — (Opcional, menor prioridad, más riesgo) Deduplicar fallback de configuración

**No es un bug, es deuda técnica.** En `fase2/router.py` hay ~6 ocurrencias del patrón `if config: ... else: global_cfg = await _get_global_config(db) ...` en distintas funciones (líneas aprox. 301, 597, 784, 1112, 1190, 1326 — pueden haberse corrido levemente tras los cambios de 2.1/2.2). **Ya se verificó que NO son estructuralmente idénticas** — hay 4 variantes distintas (precarga incondicional en dashboard; fallback de tiempo/cronómetro con 3 sub-casos; fallback combinado desafío-vs-práctica; fallback simple de solo `cantidad_requerida`).

**Recomendación si se aborda:** no intentar un único helper universal. Extraer 2 helpers parametrizados:
- `_resolve_tiempo_config(config, global_cfg, modulo_id, nivel_id)`
- `_resolve_cantidad_porcentaje(config, global_cfg, modulo_id, nivel_id)`

**Requiere tests de regresión antes de tocar** (afecta cronómetro y % de aprobación reales). Hacer esto **último**, solo si 2.1-2.4 quedaron estables y probados. Si no hay tiempo, dejarlo para otra ronda — no es urgente.

---

## Bloque 3 — Fase 3

### 3.1 — Normalización de dinero frágil (P1)

**Problema:** en `LogicaMath/backend/app/fase3/router.py`, función `responder_fase3` (~líneas 769-771):
```python
resp_dada = (payload.respuesta_dada or "").strip().lower().replace(",", ".").replace("r$ ", "")
resp_corr = respuesta_correcta_str.strip().lower().replace(",", ".").replace("r$ ", "")
es_correcta = resp_dada == resp_corr
```
El archivo **ya importa** `normalize_response` (línea 35: `from ..utils.math_utils import normalize_response, calcular_max_errores`) pero nunca la usa aquí — solo usa `calcular_max_errores`. La comparación manual no maneja `"r$"` sin espacio, no redondea decimales de dinero, y puede rechazar "5.00"/"5,00" como distintos de "5" (la BD guarda enteros).

**Fix:** el módulo relevante para "modo dinero" es el Módulo 3 (`MODULOS_META[3]`, tienda/dinero). Reemplazar por:
```python
is_money = (modulo_id == 3)
resp_dada = normalize_response(payload.respuesta_dada, is_money)
resp_corr = normalize_response(respuesta_correcta_str, is_money)
es_correcta = resp_dada == resp_corr
```
**Firma de referencia** (`LogicaMath/backend/app/utils/math_utils.py`, archivo completo ~43 líneas, ya usada igual en `fase2/router.py`):
```python
def normalize_response(val: str, is_money: bool = False) -> str:
    ...
```

**Verificación manual:** responder un pago en Módulo 3 con "5", "5.00" y "5,00" y confirmar que las tres se aceptan como equivalentes cuando la respuesta correcta es "5".

---

### 3.2 — `max_errores` recalculado y desincronizable en el cliente (P1)

**Problema:** en `LogicaMath/frontend/components/fase3/Fase3GameScreen.tsx` líneas ~509-520:
```tsx
const maxErroresPermitidos = useMemo(() => {
  if (!isChallenge) return 0;
  const porcAprobacion = 90;
  let minAciertosReq = maxAciertos;
  for (let c = 0; c <= maxAciertos; c++) {
    if (Math.floor((c / maxAciertos) * 100) >= porcAprobacion) {
      minAciertosReq = c;
      break;
    }
  }
  return maxAciertos - minAciertosReq;
}, [isChallenge, maxAciertos]);
```
Esto reimplementa en TypeScript la función `calcular_max_errores` de `math_utils.py`, con `porcAprobacion = 90` **hardcodeado**. Si un admin cambia `porcentaje_aprobacion` vía `ConfiguracionProgreso` para una sección específica, el contador "ERRORES: X/Y" del frontend queda desincronizado del límite real que aplica el backend.

**Confirmado que el backend ya devuelve el valor correcto:** `Fase3ResultadoRespuesta.max_errores_tolerados` (campo ya existe en `Fase3Types.ts` línea ~48, y el router ya lo calcula y devuelve en ambas ramas de respuesta, `router.py` líneas ~846 y ~914, vía `calcular_max_errores(cantidad_req, porc_aprobacion)`).

**Fix:**
1. Eliminar el `useMemo` de las líneas 509-520.
2. Agregar un `useState<number | null>` (ej. `maxErroresTolerados`) inicializado en `null`.
3. Al recibir la primera respuesta de un desafío (donde el backend ya manda `max_errores_tolerados`), guardar ese valor en el state y usarlo para el contador "ERRORES: X/Y".
4. Antes de la primera respuesta (no hay dato del backend todavía), mostrar un placeholder genérico (ej. ocultar el contador o mostrar "—") en vez de recalcularlo localmente.

---

### 3.3 — Eliminar código muerto `constructor_operaciones` (decisión ya tomada: eliminar)

**Confirmado por grep:** `LogicaMath/backend/app/fase3/seed.py` solo genera `TipoPreguntaEnum.RESPUESTA_NUMERICA` y `TipoPreguntaEnum.MULTIPLE_OPCION` — nunca `constructor_operaciones`. La siguiente rama en `LogicaMath/frontend/components/fase3/Fase3GameScreen.tsx` (~líneas 1078-1087) es código inalcanzable:
```tsx
{pregunta.tipo_pregunta === 'constructor_operaciones' && (
  <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
    <motion.div ...>
      <DetectiveNotebook textSegments={tokens} onDataFound={handleDataFound} />
    </motion.div>
    <div className="flex flex-col justify-end">
      <OperationBuilder availableNumbers={availableNumbers} onSubmit={handleSubmit} onClear={() => {}} />
    </div>
  </div>
)}
```

**Fix — pasos en orden:**
1. Confirmar (grep rápido) que `OperationBuilder.tsx` y `DetectiveNotebook.tsx` (`LogicaMath/frontend/components/fase3/`) no se importan desde ningún otro archivo del repo además de `Fase3GameScreen.tsx`.
2. Eliminar la rama JSX de arriba en `Fase3GameScreen.tsx` (y cualquier estado/handler que solo exista para alimentarla, ej. `tokens`, `availableNumbers`, `handleDataFound` si no se usan en otra parte del componente — verificar antes de borrar).
3. Eliminar `LogicaMath/frontend/components/fase3/OperationBuilder.tsx` y `DetectiveNotebook.tsx`.
4. En `LogicaMath/frontend/components/fase3/Fase3Types.ts`, quitar `'constructor_operaciones'` del union de `tipo_pregunta` (línea ~17: `tipo_pregunta: 'respuesta_numerica' | 'multiple_opcion' | 'constructor_operaciones'` → quitar el tercer valor).

---

### 3.4 — Doble-submit / condición de carrera en `/responder` (P2)

**Mismo patrón que 2.4.** En `LogicaMath/frontend/components/fase3/Fase3Service.ts`, `fetchDeduplicated` ya se usa en `getFase3Dashboard`, `getFase3Question`, `getFase3Reading` (todas con su propia key `*-f3`), pero **no** en `submitFase3Answer` (~líneas 86-95):
```typescript
export async function submitFase3Answer(
  payload: Fase3AnswerPayload
): Promise<Fase3AnswerResult> {
  const res = await fetchWithTimeout(`${API_URL}/fase3/responder`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  });
  return handleResponse<Fase3AnswerResult>(res);
}
```

**Fix:**
```typescript
export async function submitFase3Answer(
  payload: Fase3AnswerPayload
): Promise<Fase3AnswerResult> {
  const key = `answer-f3-${payload.pregunta_id}`;
  return fetchDeduplicated(key, async () => {
    const res = await fetchWithTimeout(`${API_URL}/fase3/responder`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(payload),
    });
    return handleResponse<Fase3AnswerResult>(res);
  });
}
```
*(Nota adicional detectada en el diagnóstico: `graduateFase3` tampoco usa `fetchDeduplicated`. No estaba en el alcance original pero es el mismo patrón — opcional aplicar el mismo fix ahí si se quiere ser exhaustivo.)*

---

### 3.5 — (Opcional, deuda técnica menor) `_sync_unlocked_levels` duplicada entre Fase 2 y Fase 3

**No es un bug funcional** — confirmado que Fase 3 tiene su propia copia de `_sync_unlocked_levels` (`fase3/router.py` líneas ~53-80), correctamente namespaced bajo `settings["unlockedLevels"]["fase3"]` (no colisiona con la de Fase 2, que usa `["fase2"]` o el namespace que le corresponda). Es duplicación de código, no un error de comportamiento.

**Si se aborda:** extraer a un helper compartido, ej. `app/utils/settings_sync.py`, con firma `async def sync_unlocked_levels(db, alumno_id, operacion, fase_key: str)`, y llamarlo desde ambos routers pasando `"fase2"`/`"fase3"` como parámetro. Baja prioridad — dejar para el final o para otra ronda de refactor.

---

## Cómo aplicar y verificar (ambos bloques)

1. **Aplicar los cambios de código** con Edit/Write sobre los archivos indicados arriba.
2. **Rebuild obligatorio** (el contenedor backend NO tiene volumen montado — un cambio en disco no se refleja solo con `docker restart`):
   ```bash
   cd D:\Antigravity\APP_Logica_Matematicas_kids
   docker compose -f docs/Pruebas_y_Test_Unitario/docker-compose.local.yml build backend
   docker compose -f docs/Pruebas_y_Test_Unitario/docker-compose.local.yml up -d --no-deps backend
   ```
   Si se tocó también el frontend (2.4, 3.2, 3.3, 3.4), agregar `frontend` al build/up.
3. **Backend no trae pytest instalado en la imagen** — para correr los tests localmente:
   ```bash
   docker exec -u root logicakids_local_backend pip install --quiet pytest pytest-asyncio
   docker exec -u root logicakids_local_backend python -m pytest -q --ignore=tests/test_scripts_config.py
   ```
   `test_scripts_config.py` falla por un import roto preexistente (`app.core.config` no existe, es `app.config`) — no relacionado con estas correcciones, ignorar.
   **Nota:** ya existen 4 tests preexistentes fallando sin relación con Fase 2/3 (`test_contextual_percentages.py`, 3 en `test_fase4_vocabulario.py`) — no son parte de este alcance, no deberían empeorar ni mejorar con estos cambios.
4. **Frontend (Vitest) se corre en el host, no en el contenedor** (el contenedor de frontend es solo nginx sirviendo el build estático):
   ```bash
   cd LogicaMath/frontend
   npm run test
   ```
5. **Prueba manual en navegador** (`http://localhost:3000`): usuario admin `amilcar@gmail.com` / contraseña ver `LogicaMath/backend/manual_scripts/create_users.py` (se resetea en cada arranque del backend), o usuario de prueba `prueba@gmail.com` / `pruebas`. El admin tiene todas las fases "Dominada" y puede usar "Repasar Fase" para entrar directo a cualquier módulo/nivel sin tener que progresar orgánicamente.
6. **Actualizar memoria** `known_bugs_fase2_a_4.md` (en el directorio de memoria del proyecto) marcando cada ítem de este documento como corregido a medida que se completa, y borrar/archivar este archivo `mejoriasFase2y3.md` una vez que Bloque 2 y 3 queden implementados y verificados.
