# Razonamiento Profundo PRO — Seguridad, integridad y no-regresión

> ## ⚠️ SUPERSEDED — use the unified manual
>
> **Agents must follow:** [`deep_analise_pro.md`](deep_analise_pro.md) (folder: `RULES AGENTES/`)  
> **Loaders:** [`AGENTS.md`](AGENTS.md) · [`../AGENTS.md`](../AGENTS.md) · [`../.agent/AGENTS.md`](../.agent/AGENTS.md)  
>
> This file is kept as **historical Spanish PRO layer**. Where it conflicts with `deep_analise_pro.md`, **the unified English manual wins**.

---

> **Versión:** 1.0 · **Fecha:** 2026-07-25  
> **Relación con el documento base:** este archivo **extendía y enfatizaba**  
> [`razonamiento_profundo.md`](razonamiento_profundo.md).  
> **Ahora ambos están unificados en** [`deep_analise_pro.md`](deep_analise_pro.md).

---

## Cómo se relacionan los documentos

| Documento | Rol |
|-----------|-----|
| [`razonamiento_profundo.md`](razonamiento_profundo.md) | Método de caza/verificación de bugs de datos y flujo (base) |
| **`razonamiento_profundo_PRO.md` (este)** | Base + **seguridad + integridad + no-regresión** (modo operativo reforzado) |
| [`LECCIONES_verificacion_agentes.md`](LECCIONES_verificacion_agentes.md) | DoD visual de imágenes/SVG |
| [`recomendacion_prioritarias.md`](recomendacion_prioritarias.md) | Qué priorizar a nivel producto (R1–R14) |
| [`DEPLOY.md`](DEPLOY.md) | Despliegue y variables de entorno |
| Documento Rector Pedagógico | Qué *debe* hacer la pedagogía (no se negocia en un fix técnico) |

**Regla de lectura para el agente:**

1. Tarea de bug/auditoría/fix → **empezá por el cheat sheet de este PRO**.  
2. Detalle de arquetipos A–M, SQL de pool, indentación, variedad → consultá el **base**.  
3. Fix visual de imágenes → **LECCIONES**.  
4. Prioridad de producto / hardening de release → **recomendaciones prioritarias**.

---

# CHEAT SHEET (léelo siempre; tarda 60 segundos)

```text
BUCLE PRO (8 pasos — no saltees 2, 5, 7 ni 8)
  1. HIPÓTESIS     → qué está mal y por qué (señal)
  2. TERRENO       → BD / endpoint / UI / diff / log real (no solo código)
  3. CUANTIFICAR   → cuántos casos / fases / usuarios
  4. RADIO         → qué MÁS puede romperse o abrirse (hermanos, auth, seeds, admin)
  5. RAÍZ + SEGURO → fix en la causa; sin bajar seguridad ni inventar bypass
  6. RE-VERIFICAR  → EL MISMO chequeo del paso 2, ahora en verde
  7. NO-REGRESIÓN  → hermanos, camino feliz, camino de error, rol ADMIN vs alumno
  8. SEGURIDAD     → authz, secretos, XSS, cookies, CORS, datos de menores

FRONTERAS DE DATO (bugs pedagógicos)
  generador → seed/BD → router/API → frontend → ojo del usuario

FRONTERAS DE SEGURIDAD (brechas)
  cliente → red/CORS → authn/authz → validación → persistencia → storage → logs

ANTES DE DECLARAR "LISTO"
  □ git diff muestra CADA archivo que afirmás tocar
  □ el bug se ejecuta (call site real) o el cambio es preventivo documentado
  □ mismo chequeo del bug en verde
  □ al menos 1 camino hermano / colateral verificado (no solo el que arreglaste)
  □ no hay secreto en diff, logs ni respuesta HTTP
  □ no hay HTML sin sanitizar nuevo; no hay endpoint admin sin rol
  □ compila (tsc / py_compile / build) con exit 0
  □ reporte separa: ya estaba | yo cambié | sin verificar | cambio de comportamiento

NUNCA
  ❌ "funciona en prod" sin refutar con terreno
  ❌ fix en un hermano sin confirmar estructura local idéntica
  ❌ re-seed / clear sin backup y sin auditar qué borra
  ❌ confiar en docstring / nombre de fase / comentario
  ❌ citar test o HTTP 200 que no corriste
  ❌ bajar auth "para que compile el fix"
  ❌ dangerouslySetInnerHTML sin sanitizeHtml
  ❌ exponer DATABASE_URL / SECRET_KEY / tokens en API o logs
  ❌ tocar fase_id / purge de otra fase por confusión de nombres
```

**Entrada rápida por tipo de tarea**

| Pedido del usuario | Entrar por |
|--------------------|------------|
| Algo está roto / auditar fase | Cheat sheet → §P2 → base §3–5 → §P4 radio → fix → §P6–P8 |
| Mejorar / rediseñar X | Base §12 + PRO §P5 y §P9 |
| Seguridad / hardening | §P3 + §P7 + recomendaciones R2/R12/R13 |
| Auditar reporte de otro agente | Base §11 + PRO §P10 |
| Deploy / prod | Base §7 + PRO §P8 + DEPLOY.md |

---

## P0. Tesis PRO (extiende la regla madre del base)

El documento base establece:

> *Toda afirmación sobre el sistema necesita una observación de terreno.*

**PRO añade tres reglas hermanas:**

1. **Regla de no-daño colateral:** *todo fix debe demostrar que no empeoró un camino vecino.*  
   Arreglar el progreso de la sección 3 no vale si rompés el desafío 11 o el Bucle Espejo.

2. **Regla de no-brecha:** *ningún fix puede intercambiar un bug funcional por una vulnerabilidad.*  
   “Lo hice más fácil de debuggear” no justifica loguear JWT, desactivar CORS, o dejar un endpoint admin abierto.

3. **Regla de integridad del cambio:** *el sistema después del cambio debe seguir cumpliendo los invariantes de producto, pedagogía y seguridad que ya tenía (salvo cambio de comportamiento explícito y aceptado).*  
   Si cambiás semántica observable (desbloqueo, herencia de config, formato de respuesta), **decilo** y verificá el impacto en datos existentes.

### Creencias extra a desactivar (además de las del base §0)

5. **"Solo toqué un archivo"** ≠ el radio de explosión es uno. Un helper compartido, un seed, un CSS global o un middleware afecta N superficies.  
6. **"Es solo frontend"** ≠ no hay riesgo de seguridad. XSS + token en `localStorage` = sesión robada.  
7. **"Es solo un seed"** ≠ no hay riesgo de integridad. Un `fase_id` mal puesto purga otra fase o desbloquea contenido equivocado.  
8. **"Lo dejé como en el hermano"** ≠ es seguro. El hermano puede estar mal (copy-paste), o la estructura local ya era correcta (casi se rompe Fase 7 des-indentando como Fase 6).  
9. **"Funciona con mi usuario admin"** ≠ funciona para el alumno. Authz se prueba con **ambos roles**.  
10. **"El linter pasó"** ≠ la app es íntegra. Compilar no prueba Early Exit, ni XSS, ni que el pool tenga 1 correcta.

---

## P1. Bucle PRO de 8 pasos (el motor reforzado)

El base tiene 6 pasos. PRO **conserva esos 6** e inserta disciplina de radio y seguridad:

```text
1. HIPÓTESIS
2. TERRENO              (igual que base)
3. CUANTIFICAR          (igual que base)
4. RADIO DE EXPLOSIÓN   ★ PRO — ¿qué más se toca o se arriesga?
5. RAÍZ + DISEÑO SEGURO ★ PRO — fix de causa sin bajar el piso de seguridad
6. RE-VERIFICAR         (mismo chequeo del bug)
7. NO-REGRESIÓN         ★ PRO — hermanos, roles, caminos colaterales
8. SEGURIDAD / INTEGRIDAD DE CIERRE ★ PRO — checklist §P7–P8
(+ PUNTA A PUNTA del base se integra en 6–7)
```

### P1.1 Paso 4 — Radio de explosión (obligatorio antes de codear)

Antes de editar, escribí (aunque sea en el pensamiento del agente) una tabla:

| Superficie | ¿La toco? | ¿Puede romperse? | Cómo lo verificaré después |
|------------|-----------|------------------|----------------------------|
| Fase N router | sí/no | … | contract / E2E responder |
| Fases hermanas N±1 | | copy-paste / helper | grep + 1 smoke |
| Seed / SEED_VERSIONS | | pool, imágenes | audit SQL § base 5 |
| Auth / cookies / roles | | login, admin | login alumno + admin |
| Admin panel | | config global | no correr clear por error |
| Frontend widget / HTML | | XSS, layout | sanitize + render |
| MinIO / URLs | | 404, bucket | curl 200 |
| Progreso de alumnos existentes | | desbloqueo, maestría | no migrar IDs a ciegas |
| Logs / PII menores | | privacidad | grep secretos en diff |

Si una celda de “puede romperse” no tiene “cómo verificaré”, **no tenés plan de cierre**.

### P1.2 Paso 5 — Raíz + diseño seguro

Preguntas obligatorias al diseñar el fix:

1. ¿La causa está en generador, seed, frontera, renderer o auth? (no parchear síntoma)  
2. ¿El fix introduce HTML crudo, `eval`, `innerHTML`, o desactiva una guarda?  
3. ¿Amplía quién puede llamar un endpoint?  
4. ¿Escribe en tablas de usuario/progreso de más de una fase?  
5. ¿El invariante nuevo es medible? (ej. “4 alts distintas, 1 correcta, HTML sanitizado, 401 sin token”)

### P1.3 Paso 7 — Matriz mínima de no-regresión

Para **cualquier** fix de fase/router/seed, verificá al menos:

| Camino | Qué mirar |
|--------|-----------|
| Camino que arreglaste | el bug original en verde |
| Camino feliz hermano | otra sección/módulo de la misma fase |
| Camino de error | respuesta incorrecta sigue dando feedback (no 500) |
| Desafío (si existe) | Early Exit / vidas no se rompieron |
| Rol alumno | no ve endpoints admin |
| Rol admin (si tocaste admin) | sigue autenticado y autorizado |
| Compile-gate | `tsc --noEmit` y/o import del módulo Python |

Para **cualquier** fix de auth/HTML/admin, sumá §P7 completo.

---

## P2. Mapa de fronteras PRO (dato + seguridad)

El base describe la tubería pedagógica. PRO la mantiene y añade la tubería de confianza:

### P2.1 Fronteras de dato (resumen del base — no se retiran)

```text
[generador] → [seed/BD] → [router/API] → [frontend] → [usuario]
     F1            F2            F3              F4
```

Bugs típicos: campo descartado, NULL en agregados, feature muerta, pregunta imposible, fuga de respuesta, variedad cero.  
**Detalle y SQL:** `razonamiento_profundo.md` §2–§5.

### P2.2 Fronteras de seguridad (nuevas)

```text
[navegador] → [CORS/TLS] → [authn JWT/cookie] → [authz rol] → [validación input]
     S1            S2               S3                  S4              S5
        → [negocio/router] → [BD] → [MinIO/S3] → [logs/analytics] → [admin]
               S6             S7       S8              S9              S10
```

| Frontera | Pregunta de integridad |
|----------|------------------------|
| S1 Cliente | ¿Se confía en el cliente para progreso, nota o rol? (debe ser **no**) |
| S2 CORS/TLS | ¿Orígenes exactos en prod? ¿credenciales + `*`? |
| S3 Authn | ¿Token en `localStorage`? ¿Cookie sin `HttpOnly`/`Secure`? |
| S4 Authz | ¿El endpoint valida ADMIN vs alumno? ¿IDOR (ver/editar otro alumno)? |
| S5 Validación | ¿Pydantic/límites? ¿HTML de admin/seed sanitizado al guardar y al render? |
| S6 Negocio | ¿Se puede forzar `bloque_completado` o `aprobado` desde el body? |
| S7 BD | ¿SQL crudo con input? ¿purge acotado por `fase_id` correcto? |
| S8 Storage | ¿URLs firmadas? ¿bucket público con datos privados? |
| S9 Logs | ¿JWT, contraseñas, respuestas de menores, PII? |
| S10 Admin | ¿`system-config` y secretos detrás de flag + rol? |

> **Técnica maestra PRO:** al auditar un cambio, trazá **ambas** tuberías. Un fix puede sanar F2 (seed) y romper S4 (authz) en el mismo PR.

---

## P3. Catálogo de arquetipos PRO

### P3.1 Arquetipos del base (A–M) — se conservan

No se eliminan. Usalos tal cual en `razonamiento_profundo.md` §3:

| ID | Nombre corto |
|----|----------------|
| A | Campo computado descartado |
| B | NULL en agregado → cero silencioso |
| C | Feature muerta (UI sin dato) |
| D | Fuga de respuesta en figura/enunciado |
| E | Pregunta imposible de responder |
| F | Distractores duplicados / doble correcta |
| G | Huérfano de flujo / indentación |
| H | Desajuste semántico por copy-paste |
| I | Generador de variedad cero |
| J | Dato mal mapeado (clave) |
| K | Entorno obsoleto (prod código viejo) |
| L | Fix fantasma / crédito falso |
| M | Bug en código inalcanzable |

### P3.2 Arquetipos de seguridad (N–V) — nuevos

#### N. Confianza en el cliente (client-authoritative leak)

- **Síntoma:** el alumno “aprueba” sin merecerlo, o el admin ve datos ajenos.  
- **Causa:** el frontend calcula progreso/desbloqueo o manda `es_correcta` / `porcentaje` y el backend lo cree.  
- **Detección:** buscá en body de requests campos de resultado; en backend, buscá asignaciones desde el payload a `ProgresoMaestria` sin recalcular.  
- **Regla:** el backend **recalcula** corrección y progreso. El cliente solo envía la respuesta del alumno.  
- **Fix:** ignorar campos de resultado del cliente; tests que manden `es_correcta=true` falso y fallen.

#### O. Authz ausente o incompleta (IDOR / rol roto)

- **Síntoma:** con token de alumno se llama `/admin/...` o se lee progreso de otro `alumno_id`.  
- **Causa:** falta `Depends(get_current_admin)` o se usa el `alumno_id` del body en vez del de la sesión.  
- **Detección:**  
  1. Lista endpoints nuevos/modificados.  
  2. Llamá cada uno sin token → 401.  
  3. Con token alumno → 403 en admin.  
  4. Con token alumno A y recurso de B → 403/404.  
- **Fix:** identidad siempre desde sesión; nunca confiar en IDs de “a quién afecto” sin ownership check.

#### P. XSS / HTML pedagógico sin sanitizar

- **Síntoma:** teoría o enunciado con `<script>` o handlers se ejecutan en el navegador.  
- **Causa:** `dangerouslySetInnerHTML` sin `sanitizeHtml` / DOMPurify; o sanitización solo en un componente.  
- **Detección:** `grep dangerouslySetInnerHTML`; cada hit debe pasar por helper único.  
- **Fix:** allowlist de tags/clases pedagógicas; sanitizar al **render** y, si es posible, al **guardar** en admin.  
- **No-regresión:** spans `keyword-highlight` deben seguir viéndose (no “arreglar XSS” destrozando pedagogía).

#### Q. Secreto o configuración sensible expuesta

- **Síntoma:** en Network tab o en `/admin/system-config` aparecen `DATABASE_URL`, keys S3, `SECRET_KEY`.  
- **Causa:** endpoint de debug en prod; logs con headers Authorization; error 500 con stack + env.  
- **Detección:** grep de `SECRET`, `DATABASE_URL`, `S3_SECRET` en routers y respuestas; flags `ENABLE_SYSTEM_CONFIG_ENDPOINT`.  
- **Fix:** flag off en prod; respuestas de error genéricas al cliente; secretos solo en env/Portainer.

#### R. Sesión débil (token en storage, cookie mal puesta)

- **Síntoma:** XSS puede robar sesión; cookie accesible por JS; cookie sin Secure en HTTPS.  
- **Causa:** JWT en `localStorage`; `SESSION_MODE` inconsistente; `credentials` no enviadas.  
- **Detección:** buscar `auth_token` / `localStorage` en frontend; revisar `Set-Cookie` en login prod.  
- **Fix (prod):** cookie HttpOnly + Secure + SameSite; frontend `credentials: "include"`; CORS sin `*`.  
- **Compat local:** modo token solo con `ENVIRONMENT=development` documentado.

#### S. CORS / CSRF mal configurado

- **Síntoma:** en prod funciona “todo origen”, o con cookies el browser bloquea.  
- **Causa:** `ALLOWED_ORIGINS=*` + credentials; o al revés, cookie sin CORS de dominio real.  
- **Detección:** leer `main.py` CORS y env de prod.  
- **Fix:** lista exacta de dominios; al usar cookies, nunca wildcard.

#### T. Upload / storage inseguro

- **Síntoma:** avatar u objeto en MinIO ejecutable, path traversal, o URL que lista el bucket.  
- **Causa:** content-type no validado; key controlada por el usuario sin prefijo; bucket público amplio.  
- **Detección:** revisar `storage.py` y endpoints de upload; probar extensión `.html` / MIME raro.  
- **Fix:** allowlist de MIME/tamaños; keys con UUID + prefijo de usuario; URLs firmadas cuando aplique.

#### U. Inyección o query insegura

- **Síntoma:** (menos frecuente con SQLAlchemy) SQL/command con f-strings de input.  
- **Causa:** `text(f"SELECT ... {user_input}")`.  
- **Detección:** grep de `text(f`, `execute(f`, shell=True con input.  
- **Fix:** parámetros bindeados; nunca interpolar input en SQL.

#### V. Escalada por re-seed / admin destructivo

- **Síntoma:** un “fix de contenido” borra intentos o progreso; o se re-siembra la fase equivocada.  
- **Causa:** confusión de `fase_id` / nombres de carpeta; `clear_*` más amplio de lo documentado; endpoint admin sin confirmación.  
- **Detección:** leer el `delete` exacto; simular en staging; contar filas de `users`/`alumnos` antes/después.  
- **Fix:** clear acotado; backup; confirmación humana en prod; mapa canónico de fases (R1).

### P3.3 Arquetipos de integridad / no-regresión (W–Z) — nuevos

#### W. Regresión de hermano (fix local, daño colateral)

- **Síntoma:** Fase 6 bien, Fase 7 rota (o práctica bien, desafío roto).  
- **Causa:** helper compartido, CSS global, cambio de schema de respuesta, des-indentado copiado.  
- **Detección:** matriz del paso 7; diff de hermanos; smoke del camino no tocado.  
- **Regla:** un bug encontrado es plantilla de búsqueda (base §4.11), pero un **fix** también es plantilla de **riesgo** en hermanos.

#### X. Invariante pedagógicamente roto “a favor del fix”

- **Síntoma:** progreso ya no es 0, pero Bucle Espejo murió; o la figura ya no filtra la respuesta pero quedó vacía.  
- **Causa:** se optimizó el síntoma (NULL→valor único por fila) sin respetar 30 familias × 4 variantes.  
- **Detección:** cardinalidad de familias + E2E de features que dependen de la agrupación (base arquetipo B).  
- **Regla:** el DoD no es “el síntoma se fue”; es “el invariante de diseño se cumple”.

#### Y. Cambio de comportamiento silencioso

- **Síntoma:** datos viejos de config dejan de aplicar; desbloqueo cambia para alumnos existentes.  
- **Causa:** refactor de herencia Global→Fase→Módulo, renumeración, sentinel sections.  
- **Detección:** comparar semántica before/after con filas reales de `configuracion_progreso`.  
- **Regla:** reportar sección “cambio de comportamiento” (base §12.10). Nunca “es solo cleanup”.

#### Z. Contaminación de alcance (diff con dos raíces)

- **Síntoma:** PR de “fix botón” también reescribe auth y renombra fases.  
- **Causa:** el agente encontró otros problemas y los metió.  
- **Detección:** `git diff --stat` desproporcionado al pedido.  
- **Regla:** out-of-scope → tarea aparte con prompt autocontenido (base §12.12). **Excepto** si el out-of-scope es una **brecha de seguridad activa explotable**: ahí se documenta y se ofrece fix inmediato al usuario, sin mezclar en silencio.

---

## P4. Técnicas PRO de caza (además del base §4)

Usá primero las del base (interrogar BD, cross-check, render visual, E2E endpoint, hermanos, señales 0 aprobados).  
PRO añade:

### P4.1 Amenaza en 10 minutos (STRIDE light)

Para el módulo que tocás, preguntá:

| Letra | Pregunta rápida |
|-------|-----------------|
| S Spoofing | ¿Puedo fingir ser otro usuario? |
| T Tampering | ¿Puedo alterar progreso/respuestas en tránsito o en body? |
| R Repudiation | ¿Queda audit log de acciones admin sensibles? |
| I Info disclosure | ¿La API devuelve de más (otras fases, otros alumnos, secretos)? |
| D DoS | ¿Un seed/upload puede tumbar el proceso? |
| E Elevation | ¿Un alumno llega a ruta admin? |

No hace falta un informe formal: con 6 respuestas honestas ya priorizás tests.

### P4.2 Diff adversarial

Antes de merge mental, leé tu propio `git diff` como atacante:

1. ¿Aparece un endpoint nuevo sin `Depends`?  
2. ¿Se relajó una condición `if role == ADMIN`?  
3. ¿Hay `dangerouslySetInnerHTML` nuevo?  
4. ¿Hay `console.log` de token/user?  
5. ¿Hay `ALLOWED_ORIGINS` o flags de seguridad tocados?  
6. ¿Hay `delete(` / `clear_` / `SEED_VERSIONS`?

### P4.3 Prueba de roles cruzados (obligatoria si tocás auth o admin)

```text
A) sin token        → 401 en rutas protegidas
B) alumno           → 200 en sus rutas; 403 en /admin/*
C) admin            → 200 en admin; no ve tokens de otros en claro
D) alumno A → recurso B → denegado
```

### P4.4 Prueba de contrato de respuesta (anti-regresión de frontend)

Si cambiaste un JSON de `responder_faseN` o dashboard:

1. Listá campos que el frontend lee (`grep` del service TS).  
2. Asegurate de no renombrar/quitar sin migrar el frontend.  
3. Ideal: test de contrato (recomendación R4).

### P4.5 Prueba de purge acotado

Si tu fix toca seed/clear:

```sql
-- ANTES
SELECT 'preguntas' t, count(*) FROM preguntas WHERE fase_id = :F
UNION ALL SELECT 'otras_fases', count(*) FROM preguntas WHERE fase_id <> :F
UNION ALL SELECT 'users', count(*) FROM users
UNION ALL SELECT 'alumnos', count(*) FROM alumnos;

-- DESPUÉS del clear/reseed de F: users/alumnos/otras_fases deben ser IGUALES
```

### P4.6 Búsqueda de regresiones por patrón (cuando encontrás un bug)

Como el base §4.11, pero con checklist de seguridad:

```text
grep del patrón en:
  - todas las fases (fase1..fase11)
  - admin/
  - routers de auth
  - componentes shared/
  - utils de storage
```

Un XSS en Fase 8 TheoryModal implica revisar **todos** los TheoryModal.

---

## P5. Condiciones de integridad antes de escribir código

No abras el editor hasta poder marcar:

### P5.1 Integridad de comprensión

- [ ] Sé qué archivo es la **fuente de verdad** del bug (seed vs router vs UI).  
- [ ] Sé el `fase_id` real (no el nombre de carpeta solo) — ver mapa canónico si existe (R1).  
- [ ] Sé si el flujo es **práctica**, **desafío TJS** o **simulado** (reglas distintas).  
- [ ] Leí al menos un **hermano que funciona** (o confirmé que todos están rotos igual).

### P5.2 Integridad de alcance

- [ ] El pedido del usuario está acotado; lo out-of-scope está listado.  
- [ ] No mezclaré renumeración de fases + auth + feature nueva en el mismo diff.  
- [ ] Si el cambio es grande: diagnóstico con `archivo:línea` y, si es UI, mockup/alcance (base §12).

### P5.3 Integridad de seguridad previa

- [ ] El camino actual **requiere auth** donde corresponde (no lo “simplificaré” quitándola).  
- [ ] No planeo loguear secretos “temporalmente”.  
- [ ] Si toco HTML, usaré el helper de sanitización del proyecto.  
- [ ] Si toco prod: backup y confirmación humana (base §7).

### P5.4 Integridad de datos de menores (contexto escolar)

- [ ] No exportaré dumps con alumnos a sitios públicos.  
- [ ] No pegaré en el chat/reporte contraseñas, tokens ni datos personales innecesarios.  
- [ ] Scripts de prueba limpian `Intento`/`ProgresoMaestria` de prueba al final (base §4.7).

---

## P6. Cómo escribir el fix PRO (extiende base §6)

Conservá las reglas del base:

1. Raíz, no síntoma.  
2. Invariantes con helper, no parches puntuales.  
3. Preservar pedagogía.  
4. Subir `SEED_VERSIONS` si el fix es de datos.  
5. No aplicar fix hermano a ciegas.  
6. Re-medir variedad.  
7. Si cambiás tipo de respuesta, verificá el frontend.  
8. El fix necesita terreno que distinga solución buena de “apaga síntoma”.

**Añadidos PRO:**

9. **Authz first:** todo endpoint nuevo nace con dependencia de auth y test 401/403.  
10. **Sanitize by default:** todo HTML nuevo pasa por helper único; no inventes un sanitize local distinto.  
11. **Fail closed:** si falta config de seguridad en prod, no abras el sistema; fallá el arranque o deshabilitá la feature peligrosa.  
12. **Least privilege en scripts:** un script de auditoría es read-only por defecto; write exige flag `--apply` y confirmación.  
13. **Feature flags para riesgos:** cambios de auth/cookies detrás de `SESSION_MODE` / env, con rollback.  
14. **Una raíz por PR/diff** salvo emergencia de seguridad.  
15. **Compatibilidad de payload:** preferí añadir campos opcionales antes de renombrar los que el frontend ya consume.  
16. **Comentarios honestos:** si corregís un docstring mentiroso (“Fase 2” en Fase 6), actualizalo; no agregues más mentiras.

### P6.1 Plantilla de invariante del fix (copiá en el reporte)

```markdown
### Invariante del fix
- Bug original (terreno): …
- Invariante funcional: …
- Invariante de seguridad: … (ej. "sin token → 401", "HTML sanitizado")
- Invariante pedagógico: … (ej. "30 familias × 4 variantes")
- Chequeo que falla si el fix es plausible-pero-malo: …
- Hermanos verificados: …
- Cambio de comportamiento para datos existentes: ninguno | describir
```

---

## P7. Checklist de seguridad de cierre (cada cambio relevante)

Marcá lo que aplique. Si tocaste auth, HTML, admin, storage o CORS, **casi todo aplica**.

### P7.1 Autenticación y sesión

- [ ] Rutas protegidas devuelven 401 sin credenciales.  
- [ ] No se introdujo auth opcional “por comodidad” en prod.  
- [ ] No se guardó JWT nuevo en lugares más débiles que antes.  
- [ ] Logout invalida la sesión en el modo usado (cookie/token).  
- [ ] `credentials: "include"` si el modo es cookie.

### P7.2 Autorización

- [ ] Endpoints `/admin/*` exigen rol ADMIN.  
- [ ] No hay IDOR: el alumno solo accede a su progreso.  
- [ ] Acciones destructivas (delete user, clear fase, reseed) no están al alcance de alumno.  
- [ ] WebSockets admin no filtran datos sensibles a clientes no autorizados.

### P7.3 XSS y render HTML

- [ ] `grep dangerouslySetInnerHTML` en archivos tocados → todos sanitizados.  
- [ ] No se añadió `eval`, `document.write`, ni markdown crudo sin filtro.  
- [ ] Clases pedagógicas (`keyword-highlight`) siguen permitidas y visibles.

### P7.4 Secretos y configuración

- [ ] Diff sin `.env`, passwords, keys.  
- [ ] Respuestas de error sin connection strings.  
- [ ] `ENABLE_SYSTEM_CONFIG_ENDPOINT` no quedó en true “para probar” en prod.  
- [ ] Logs sin `Authorization` ni cookie completa.

### P7.5 CORS y headers

- [ ] No se introdujo `allow_origins=["*"]` con credentials.  
- [ ] Headers de seguridad no se desactivaron sin motivo (`ENABLE_SECURITY_HEADERS`).  

### P7.6 Uploads y MinIO

- [ ] Validación de tipo/tamaño si se tocó upload.  
- [ ] No se hizo el bucket más público de lo necesario.

### P7.7 Dependencias

- [ ] No se añadió dependencia desconocida sin necesidad.  
- [ ] No se pinneó un paquete a versión claramente vulnerable a propósito.

---

## P8. Checklist de integridad y no-regresión de cierre

### P8.1 Funcional

- [ ] Mismo chequeo del bug en verde (base paso 5).  
- [ ] E2E del flujo usuario (base §4.7 / visual si aplica).  
- [ ] Al menos un camino hermano verificado.  
- [ ] Camino de error no devuelve 500/`None`.  
- [ ] Si hubo seed: versión subida **y** re-siembra confirmada en el dato servido.  
- [ ] Si hubo prod: backup, conteos de tablas no tocadas estables, healthcheck, grep de marca en contenedor (base §7).

### P8.2 Contrato API ↔ Frontend

- [ ] Campos que el frontend usa siguen presentes.  
- [ ] Enums `tipo_pregunta` en el case que el backend persiste (MAYÚSCULAS).  
- [ ] No se rompió el prefijo `/api` / strip middleware sin actualizar clientes.

### P8.3 Integridad de fases y datos

- [ ] `fase_id` del seed/router coincide con el mapa canónico (no purgar otra fase).  
- [ ] Cardinalidad de familias/variantes coherente si tocaste `estructura_padre_id`.  
- [ ] 0 preguntas MULTIPLE_OPCION con 0 alternativas (LEFT JOIN del base §5).  
- [ ] 0 RESPUESTA_NUMERICA con texto no numérico (si el tipo no cambió a propósito).

### P8.4 Integridad del reporte (base §11, reforzado)

- [ ] Cada archivo reclamado aparece en `git diff HEAD --stat`.  
- [ ] No hay crédito de fixes preexistentes (`blame` si hay duda).  
- [ ] Tests citados existen y se corrieron (salida real).  
- [ ] Separás: ya estaba | cambié yo | sin verificar | cambio de comportamiento.  
- [ ] No inflás el conteo de “bugs corregidos”.

### P8.5 Compile e higiene

- [ ] `tsc --noEmit` y/o build frontend si tocaste TS/TSX.  
- [ ] Módulo Python importa / tests unitarios del área.  
- [ ] Sin harness temporales dejados en el árbol (base §12.6).  
- [ ] Sin secretos ni dumps enormes añadidos al git.

---

## P9. Protocolo de arranque PRO (extiende base §10)

Antes de proponer cambios:

1. **Stack y entornos** (local / desarrollo / produción) — paths y dominios reales.  
2. **Mapa de IDs de fase** si la tarea cruza fases (R1): no confíes en el nombre de carpeta.  
3. **Hermano que funciona** como oráculo.  
4. **Salud de datos** (base §5) en la fase objetivo.  
5. **Salud de seguridad rápida:**  
   - ¿Login exige credenciales?  
   - ¿`/admin` sin token falla?  
   - ¿Hay `system-config` expuesto?  
6. **Señales estructurales:** 0 aprobados, 0 intentos, seed version mismatch (base §4.12, arquetipo K).  
7. **Trazá una feature de punta a punta** (dato + una frontera de seguridad).  
8. **Recién entonces** hipótesis + radio de explosión (§P1.1) + bucle.

Si la tarea es “mejorar X”: base §12 completo + §P5 de este PRO.

Si la tarea es “auditar un reporte”: §P10.

---

## P10. Integridad del reporte PRO (extiende base §11)

Además de cruzar afirmaciones contra diff/compilador/endpoint:

### P10.1 Sección obligatoria en todo informe de fix

```markdown
## Resumen honesto
- Pedido del usuario:
- Archivos realmente modificados (según git diff):
- Bugs/features reales corregidos (con terreno):
- Hallazgos de seguridad (si hubo):
- No-regresiones verificadas:
- Sin verificar (falta de terreno):
- Cambios de comportamiento:
- Riesgos residuales:
```

### P10.2 Señales de reporte falso (rechazalo, incluso el tuyo)

| Señal | Acción |
|-------|--------|
| “8 bugs” pero diff toca 1 archivo cosmético | recontar con terreno |
| Cita test inexistente | invalidar verificación |
| “100% del admin funcional” sin abrir UI | degradar a “no verificado” |
| “Apliqué el mismo fix a todas las fases” sin diffs por fase | verificar cada una |
| “No hay impacto de seguridad” en un cambio de auth | exigir matriz de roles |

### P10.3 Cuando el informe es de seguridad

Nunca pegues el exploit completo con payload real contra prod en un doc público del repo si expone a alumnos. Describí la clase de bug, el archivo, y un PoC **seguro** en local/staging.

---

## P11. Recetario PRO (comandos y chequeos)

### P11.1 Del base (se conservan)

Usá el recetario SQL/Python de `razonamiento_profundo.md` §5 para:

- duplicados y 0 alternativas (LEFT JOIN)  
- variedad por sección  
- NULL en `estructura_padre_id`  
- texto en pregunta numérica  
- cross-check imagen  
- E2E `responder_faseN`  
- prod vs código desplegado  

### P11.2 Seguridad — authz smoke (httpx / curl)

```bash
# Ajustá host y rutas reales del entorno
BASE=https://localhost/api   # o el de tu env

# Sin token
curl -s -o /dev/null -w '%{http_code}\n' "$BASE/admin/..."   # espera 401/403

# Con token alumno (no admin)
curl -s -o /dev/null -w '%{http_code}\n' \
  -H "Authorization: Bearer $ALUMNO_TOKEN" "$BASE/admin/..."  # espera 403

# Con token admin
curl -s -o /dev/null -w '%{http_code}\n' \
  -H "Authorization: Bearer $ADMIN_TOKEN" "$BASE/admin/..."   # espera 200
```

### P11.3 XSS — grep de render inseguro

```bash
# Desde LogicaMath/frontend
rg "dangerouslySetInnerHTML" -n
rg "innerHTML\s*=" -n
rg "sanitizeHtml|DOMPurify" -n
```

Cada hit de `dangerouslySetInnerHTML` debe estar a ≤ pocas líneas de `sanitizeHtml(...)`.

### P11.4 Secretos en el diff

```bash
git diff HEAD | rg -i "password|secret_key|api_key|begin rsa|database_url|eyJ" 
# si matchea algo real → NO commitear / sacar del diff
```

### P11.5 Superficie admin y system-config

```bash
rg "system-config|SYSTEM_CONFIG|ENABLE_SYSTEM_CONFIG" -n LogicaMath/backend
rg "SESSION_MODE|COOKIE_SECURE|ALLOWED_ORIGINS" -n LogicaMath/backend
```

### P11.6 Radio de fases (copy-paste)

```bash
# Ejemplo: buscá el patrón que arreglaste
rg "is_money|estructura_padre_id|datos_numericos\s*=" -n LogicaMath/backend/app/fase*
```

### P11.7 Integridad post-clear

```sql
SELECT fase_id, count(*) FROM preguntas GROUP BY 1 ORDER BY 1;
SELECT count(*) FROM users;
SELECT count(*) FROM alumnos;
-- comparar con snapshot pre-operación
```

### P11.8 Frontend: token en storage (deuda conocida)

```bash
rg "localStorage\.(get|set)Item\(['\"]auth" -n LogicaMath/frontend
```

Si tu cambio **añade** nuevos usos en prod, es regresión de seguridad (arquetipo R). Preferí no expandir esa superficie.

---

## P12. Definition of Done PRO (checklist maestro)

El DoD del base §9 **sigue valiendo completo**. PRO exige **además**, cuando aplique:

### Del base (no retirar — resumido)

- [ ] Terreno real del bug  
- [ ] Impacto cuantificado  
- [ ] Raíz arreglada  
- [ ] Patrón buscado en hermanos  
- [ ] Mismo chequeo en verde  
- [ ] Punta a punta / E2E  
- [ ] Visual mirado si es imagen  
- [ ] Re-seed/rebuild confirmado  
- [ ] Integridad de pool post-fix  
- [ ] Prod: backup + alcance + health + código nuevo en contenedor  
- [ ] Diff real; bug se manifiesta; verificaciones reproducibles  
- [ ] Compila; no firmes lo no observado  
- [ ] Reporte honesto sin inflar conteos  

### Añadidos PRO

- [ ] **Radio de explosión** documentado y verificado en al menos un colateral.  
- [ ] **Matriz de roles** si tocaste auth/admin/API sensible.  
- [ ] **XSS/HTML** saneado en archivos tocados; pedagogía visual intacta.  
- [ ] **Cero secretos** en diff, logs de demo y respuestas.  
- [ ] **No se bajó** CORS/headers/auth “para que pase”.  
- [ ] **fase_id** correcto; no se purgó/alteró otra fase.  
- [ ] **Invariante pedagógico** medible (no solo “ya no es NULL”).  
- [ ] **Cambio de comportamiento** declarado o “ninguno”.  
- [ ] **Riesgo residual** listado (deuda conocida no escondida).  
- [ ] **Out-of-scope** derivado a tarea aparte (salvo brecha crítica acordada).  

---

## P13. Escenarios guiados (cómo piensa el agente PRO)

### Escenario A — “El progreso de la Fase N no avanza”

1. Terreno BD: `count(estructura_padre_id)` vs `count(*)` (base B).  
2. E2E `responder_faseN` (base G también puede ser `None`).  
3. Radio: si tocás seed, ¿imágenes/datos_numericos se preservan? (A).  
4. Fix en seed/router raíz; re-seed con versión.  
5. No-regresión: práctica **y** desafío; cardinalidad de familias.  
6. Seguridad: el script E2E limpia datos de prueba; no loguea tokens.  

### Escenario B — “Hay que mostrar HTML de teoría más bonito”

1. No inventes otro pipeline de HTML.  
2. Reutilizá `sanitizeHtml` / allowlist.  
3. Verificá visualmente highlights.  
4. Grep de otros TheoryModal (hermanos + XSS N).  
5. Diff adversarial: ¿algún `dangerouslySetInnerHTML` sin sanitize?

### Escenario C — “El admin necesita un endpoint para ver config del sistema”

1. Default: **deshabilitado en prod** (`ENABLE_SYSTEM_CONFIG_ENDPOINT=false`).  
2. Si se habilita: solo ADMIN + nunca devolver secretos crudos.  
3. Tests: alumno 403, sin token 401.  
4. Documentar en DEPLOY.  
5. No lo dejes true “un rato” en el VPS.

### Escenario D — “Apliqué el fix de Fase 6 a Fase 7”

1. **STOP.** Compará estructura real (base §6.5).  
2. Si el `else` ya existe, no des-indentes.  
3. Verificá ambos caminos E2E.  
4. Reportá “evaluado, no aplicable” si no había bug — eso es integridad, no pereza.

### Escenario E — “Re-sembrar producción Fase 4”

1. Solo lectura: logs, tráfico, versión seed.  
2. Backup `pg_dump`.  
3. Leer `clear_*`: ¿toca alumnos?  
4. Conteos pre.  
5. Apply + re-seed.  
6. Conteos post (otras fases/users iguales).  
7. SQL de integridad pool + healthcheck + grep código nuevo.  
8. Confirmación humana antes del write.

### Escenario F — “Otro agente dice que cerró 8 bugs de seguridad”

1. Base §11 + §P10.  
2. Cada bug → diff + call site + prueba.  
3. Separar: real / fantasma / código muerto / no verificado.  
4. No merges ni deploys basados en el resumen solo.

---

## P14. Anti-patrones PRO (checklist de trampas extra)

Además de la lista del base §8:

- ❌ Arreglar un bug y no correr **ningún** camino colateral.  
- ❌ “Temporalmente” quitar auth, CORS estricto o sanitización.  
- ❌ Ampliar `localStorage` de tokens en código nuevo de prod.  
- ❌ Purgar/reseedar sin confirmar `fase_id` canónico.  
- ❌ Confiar en el body del cliente para `es_correcta` / progreso.  
- ❌ Dejar harness, `.env`, dumps o reportes Playwright en el commit.  
- ❌ Mezclar hardening de auth con renumeración de fases en un solo cambio.  
- ❌ Declarar “sin impacto de seguridad” sin mirar el diff adversarial.  
- ❌ Sanitizar tan agresivo que rompe la pedagogía y no re-verificar UI.  
- ❌ Escribir en prod porque “el fix es chico”.  
- ❌ Callar un cambio de comportamiento sobre alumnos ya existentes.  
- ❌ Usar datos reales de menores en capturas/reportes públicos.  
- ❌ Copiar un endpoint admin “abierto” de un snippet de internet.  
- ❌ Tratar un hallazgo de seguridad out-of-scope como basura silenciosa **sin avisar**.

---

## P15. Matriz de decisión rápida: ¿puedo mergear / dar por cerrado?

| Pregunta | Si la respuesta es NO |
|----------|------------------------|
| ¿El terreno del bug original está en verde? | No cerrar |
| ¿El diff contiene lo que el reporte dice? | No cerrar |
| ¿Compila el área tocada? | No cerrar |
| ¿Hay al menos un colateral verificado? | No cerrar (salvo cambio trivial de docs) |
| ¿Authz sigue fail-closed? | No cerrar |
| ¿HTML nuevo sanitizado? | No cerrar |
| ¿Secretos fuera del diff? | No cerrar / no pushear |
| ¿fase_id correcto en seeds/deletes? | No cerrar |
| ¿Usuario avisado de cambio de comportamiento? | No cerrar si hay impacto en datos viejos |
| ¿Prod: backup + confirmación si escribiste? | No escribir / rollback |

---

## P16. Alineación con recomendaciones prioritarias

Cuando tu trabajo toque estos temas, leé la R correspondiente en `recomendacion_prioritarias.md` y aplicá el DoD PRO:

| R | Tema | Énfasis PRO |
|---|------|-------------|
| R1 | Mapa canónico de fases | Evita arquetipo V y purges cruzados |
| R2 | Hardening prod | §P7 completo |
| R4 | Contratos por fase | §P4.4 y no-regresión de payload |
| R5 | Motor genérico | Radio enorme → §P1.1 + hermanos |
| R7 | Audit pool | Automatiza base §5 + P8.3 |
| R8 | CI | Compile-gate + tests en cada PR |
| R11 | Política git | Sin dumps/secretos |
| R12 | Sanitización HTML | Arquetipo P |
| R13 | Cookies HttpOnly | Arquetipo R |

---

## P17. Relación con el documento base (qué no se pierde)

Este PRO **no retira**:

- La tesis de terreno vs intención  
- El bucle de hipótesis → re-verificación  
- El modelo de fronteras de dato  
- Los arquetipos A–M  
- Las técnicas §4 del base  
- El recetario SQL/E2E  
- Cómo escribir fixes robustos §6  
- Disciplina de producción §7  
- Anti-patrones LLM §8  
- DoD §9  
- Protocolo de arranque §10  
- Integridad de reportes §11  
- Aterrizaje de cambios grandes §12  

**Los incorpora por referencia y los refuerza** con:

- Bucle de 8 pasos  
- Fronteras de seguridad S1–S10  
- Arquetipos N–Z  
- Condiciones previas de integridad §P5  
- Checklists de seguridad y no-regresión  
- Recetario de authz/XSS/secretos  
- DoD PRO y escenarios guiados  

Si hay conflicto de detalle pedagógico/SQL, **prevalece el base** en su terreno.  
Si hay conflicto de seguridad vs “atajo para que compile”, **prevalece este PRO** (fail closed).

---

## P18. Idea de una frase (modo PRO)

> *No solo demuestres que el bug se fue: demostrá que el camino vecino sigue vivo, que la puerta de admin sigue cerrada, que el HTML no ejecuta código, que el seed no purgó otra fase, y que tu reporte no miente sobre el diff — porque en una app escolar, un fix que abre una brecha o borra progreso ajeno es peor que el bug original.*

---

## Apéndice A — Orden de lectura sugerido para un agente nuevo

1. **Cheat sheet** (arriba)  
2. **P0–P1** (tesis y bucle 8 pasos)  
3. **P3** (arquetipos N–Z; A–M en el base cuando caces bugs de pool)  
4. **P5** antes de editar  
5. **P6–P8** mientras cerrás  
6. **P12** DoD antes de entregar  
7. Base completo cuando el bug sea de seed/progreso/imágenes  
8. LECCIONES si hay PNG/SVG  

## Apéndice B — Plantilla corta de “plan antes de codear”

```markdown
## Plan (antes de editar)
- Hipótesis:
- Terreno a consultar:
- fase_id / rutas / roles involucrados:
- Radio de explosión (tabla):
- Invariantes a preservar:
- Riesgos de seguridad:
- Plan de no-regresión:
- Fuera de alcance:
```

## Apéndice C — Plantilla corta de “cierre”

```markdown
## Cierre
- Diff real (archivos):
- Terreno del bug (antes → después):
- Colaterales verificados:
- Seguridad (§P7) aplicable y resultado:
- Integridad pool/fases:
- Compilación/tests:
- Comportamiento cambiado:
- Residual / follow-ups:
```

---

*Fin de `razonamiento_profundo_PRO.md`.*  
*Documento base intacto: `razonamiento_profundo.md`.*  
*Usar ambos: el base para profundidad de caza pedagógica; PRO como capa obligatoria de seguridad e integridad en cada cambio.*
