Trabajas en LogicaMath (D:\Antigravity\APP_Logica_Matematicas_kids\LogicaMath). Antes de tocar nada lee, en este orden:
1. reestructuracion.md (raíz del proyecto) — el plan completo de la reestructuración, en especial §1.A y §6.C.
2. faltantefase4.md (raíz del proyecto) — los pasos de implementación ya ejecutados sobre la Fase 4.
3. RULES AGENTES/deep_analise_pro.md, en especial §25 (OpenSpec, operaciones destructivas, contenido generado por IA).
4. AGENTS.md (raíz) — reglas de precedencia del repo.

CONTEXTO: Se intercambiaron las Fases 4 y 5 (la antigua Fase 5 "Operatoria Decimal y Conversiones" es ahora la Fase 4; la antigua Fase 4 "Fracciones" es ahora la Fase 5). La Fase 4 ya fue auditada y corregida a fondo: compositor de preguntas coherente (enunciado y respuesta derivan de la misma fórmula), escala física de las conversiones corregida, gramática corregida, desafíos D1/D2/DF usando el compositor, 5.406 preguntas verificadas en la base de datos local Postgres (contenedor `logicakids_local_db`), 0 huérfanas, 0 `estructura_padre_id` nulo. ESTO YA ESTÁ HECHO, no lo repitas.

REGLAS DURAS QUE NO PUEDES ROMPER:
- Todo en LOCAL. No toques VPS, no toques MinIO remoto, no hagas deploy.
- NO modifiques el contenido, la lógica de generación de preguntas, ni la teoría de ninguna fase que no sea la 4, salvo la única excepción puntual del punto A abajo (que es un fix de arranque, no de contenido).
- No hagas `git commit` ni `git push` bajo ninguna circunstancia. Deja los cambios en el working tree y reporta qué archivos tocaste.
- Todo enunciado nuevo en coma decimal (no punto), sin vocabulario de fracciones, sin volumen ni superficie (C6.5 del plan).
- Cero scroll vertical y ventana de tamaño fijo (T3/T4 del plan) si tocas algo de UI.

TAREAS PENDIENTES, en este orden:

## A. Desbloquear el arranque del backend local (bloqueador actual)
El contenedor `logicakids_local_backend` está en crash-loop. `app/seed.py` línea ~924 hace:
    from app.fase5.seed import run_fase5_seed
pero `app/fase5/seed.py` no define esa función (solo funciones sueltas: `seed_teoria_niveles`, `seed_configuracion_progreso`, etc., y conserva una función mal nombrada `clear_fase4_data` que en realidad pertenece a Fase 5 — residuo del intercambio de nombres).
Acción MÍNIMA y ESCOPADA: agrega en `app/fase5/seed.py` una función `run_fase5_seed()` que orqueste las funciones sueltas ya existentes de ese archivo (síguelas por orden lógico: teoría → práctica → desafíos → configuración, como hace `run_fase4_seed()` en `app/fase4/seed.py` como referencia de patrón). NO reescribas ni "mejores" el contenido de Fase 5 — Fase 5 se auditará después, como su propia fase. Solo necesitas que el import funcione y el contenedor deje de reiniciarse. Si `clear_fase4_data` dentro de `app/fase5/seed.py` está realmente borrando datos de fase_id=5 (verifícalo), puedes renombrarla a `clear_fase5_data` por claridad, pero sin tocar su lógica interna.
Verifica con `docker logs logicakids_local_backend --tail 50` que el contenedor arranca sin excepción y queda "Up" (no "Restarting").

## B. Apoyo visual SVG en el compositor de Fase 4 (C3 del plan — "Decidido", pendiente de implementar)
El compositor (`app/fase4/compositor_fase4.py`) genera enunciados de solo texto. El plan exige apoyo visual SVG en las preguntas (C3), usando los generadores existentes en `app/utils/svg_figuras.py` (ej. `escalera_unidades`, `tabla_datos`, `recta_numerica_decimal`) — NO reintroduzcas el bloque legacy que fue eliminado de `app/fase4/seed.py` (generaba volumen/superficie, prohibido por C6.5, y usaba catálogos rotos).
Regla anti-revelación (crítica, ver reestructuracion.md §C3): la figura SVG puede mostrar los DATOS del problema (una escalera de unidades con la magnitud marcada, una tabla con las cantidades), pero JAMÁS puede ejecutar o insinuar el procedimiento de la operación (ej. no dibujar la flecha de conversión ya resuelta, no mostrar el resultado).
Diseño sugerido: añade al `CompositorFase4.componer_pregunta_practica()` un campo opcional `figura_svg` que:
- Para el módulo 4 (conversiones): use `escalera_unidades(...)` marcando solo la unidad de origen y destino, sin resolver el factor.
- Para módulos 1-3 con `n_datos >= 2`: use `tabla_datos([...])` con los valores en crudo del enunciado (sin el resultado).
Actualiza `app/fase4/seed.py` (`_generate_practice_question` y `_generate_challenge_question` en la rama D1) para insertar `figura_svg` en el HTML del enunciado (como hacía el bloque legacy, con `<br/>`), respetando el presupuesto de caracteres y el alto máximo de SVG en desafíos (140px, ver reestructuracion.md tabla de §8).
Verifica con un script Python (no necesitas Docker para esto) que 20 preguntas de muestra por módulo generan SVG válido y que el SVG no contiene el número de la respuesta correcta.

## C. Verificación completa contra la base de datos real (una vez desbloqueado A)
1. Reconstruye el contenedor backend (`docker compose -f Datos_localhost/docker-compose.local.yml up -d --build backend` o el compose que corresponda) y confirma que queda "Up" y sano.
2. Corre el seed de Fase 4 DOS VECES consecutivas (para probar idempotencia) y confirma que la segunda corrida produce exactamente los mismos conteos: 12 filas en `niveles_teoria_pool`, 5.406 en `preguntas` (3.456 práctica + 1.950 desafíos), 26 en `configuracion_progreso`, 0 `estructura_padre_id` nulos.
3. Corre `python -m pytest app/tests/test_fase_endpoints_contract.py -k "4-responder_fase4" -v` desde dentro del contenedor backend (ahí SÍ hay red hacia Postgres) y confirma que pasa en verde. Si sigue fallando, reporta el traceback completo — no lo ocultes.
4. Corre la suite completa de backend (`pytest tests/ app/tests/`) y de frontend (`npm run test -- --run` y `npx tsc --noEmit`) y reporta cualquier fallo NUEVO que no exista ya (el fallo preexistente en `test_ux_feedback.py::test_create_ux_feedback_multiple_images` es conocido y ajeno a Fase 4; no lo intentes arreglar).

## D. Cierre de residuos textuales y documentación
1. En `app/fase4/seed.py`:
   - Línea ~9 (docstring del módulo): dice "16 filas en configuracion_progreso (4 módulos × 4 config por módulo)" pero la función real inserta 26 filas (1 fila de práctica libre + 12 de práctica por módulo/nivel + 12 de desafíos por módulo/tipo + 1 mixta). Corrige el docstring a 26 y describe la composición real.
   - Línea ~189 (comentario de sección): dice "GENERADOR DE PRÁCTICA (7.200 preguntas = 15 niveles x 120 fam x 4)" — es un residuo de la ANTIGUA Fase 4 (fracciones). El valor real es 3.456 preguntas = 4 módulos × 3 niveles × 72 familias × 4 variantes. Corrígelo.
2. `docs/MAPA_CANONICO_FASES.md`: realinéalo contra el estado real de la tabla `fases` en la BD local. Ejecuta `SELECT id, nombre, orden FROM fases ORDER BY id;` contra `logicakids_local_db` y usa ese resultado como fuente de verdad. NO modifiques las fases 6-11 más allá de reflejar lo que ya está en la tabla; solo corrige donde el documento diga algo distinto de la BD.
3. `AGENTS.md` (raíz): la fila `| [reestructuracion.md](./reestructuracion.md) | 🚧 Phase 4 restructuring — WHAT to do (active) |` y cualquier bloque de precedencia "ACTIVE RESTRUCTURING" siguen marcando la Fase 4 como trabajo activo. Dado que la Fase 4 ya está operativa (tras completar A, B y C de este prompt), cambia el estado de esa fila a algo como "✅ Phase 4 restructuring — completed, kept as historical reference" y retira cualquier instrucción de precedencia que obligue a leer `reestructuracion.md` como bloqueante para trabajar en OTRAS fases. NO borres el archivo ni pierdas su contenido: solo cambia su estado de "activo" a "completado".

ENTREGABLE: al terminar, reporta en un mensaje corto (no crees un .md nuevo salvo que se te pida): qué archivos tocaste, resultado de cada verificación de C (conteos, salida de pytest), y cualquier hallazgo que NO hayas podido resolver dentro del alcance de este prompt (por ejemplo, si algo de Fase 5 resulta estar más roto de lo esperado — en ese caso NO lo arregles, solo repórtalo).