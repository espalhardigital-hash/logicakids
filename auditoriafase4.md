Este documento Describe el Proceso de reestructuracion de la Fase 4

Contexto :
EL programa app logicakids tenia una estructura de datos que estaba en un archivo llamado fase4.json  que estaba جدا anticuado y con muchos errores , este archivo se usaba para la generacion de preguntas y desafios de la fase 4 .
por lo cual se decidio reestructurar la fase 4 para que fuera mas modular y facil de mantener y se pudiera agregar nuevos niveles y desafios facilmente . Ademas la actual fase 4 era la antigua fase 5 por lo que se debia cambiar el orden en el app mudando sus tablas , Id y otras implicaciones
Usando Claude Code Con el moduelo Opus 5 ultracode mediante analisi preguntas y respuestas con el ingeniero de Software se contruyo el documento
reestructuracion.md (ruta del documento D:\Antigravity\APP_Logica_Matematicas_kids\reestructuracion.md)

--------------------------------------------------------------
PARTE 1 
en el se consigna toda la informacion necesaria de lo que se debe implementar para reestructura la nueva Fase 4 OPeraciones Decimales y conversion de unidades de longitud

Se utilizo antigravity de Gemini 3.6 hight para ejecutar la implementaciones propuestas en el documento reestructuracion.md 
la implementacion se utilizo la metodologia spec drive usando el framework de openspec como se puede apreciar en los archivo o change D:\Antigravity\APP_Logica_Matematicas_kids\openspec\changes que guardan los cambios que se implementaron

Esta implementacion usando gemini 3,6 Hight se realizaron paso a paso con los siguinetes protma :
" 
🔧 Prompt 0 — Apertura de sesión
Úsalo una vez al empezar cada sesión de trabajo, antes de cualquier change.

FUENTES Y PRECEDENCIA, en este orden:
1. reestructuracion.md (raíz del repo) — fuente de verdad de QUÉ hacer. Prevalece sobre
   cualquier otra fuente para todo lo relativo a la Fase 4.
2. RULES AGENTES/deep_analise_pro.md — fuente de verdad de CÓMO trabajar. Lee en particular
   la §25 (spec-driven, programas de varios changes, operaciones destructivas en local,
   contenido generado).
3. docs/Criterios Diseno Fase/ (Tomos 1-4) y docs/MAPA_CANONICO_FASES.md — normativa de las
   DEMÁS fases. Para la Fase 4, donde contradigan a reestructuracion.md, prevalece
   reestructuracion.md; las derogaciones están listadas en su sección A0.

REGLAS DE ESTA SESIÓN:
- Trabajas SOLO EN LOCAL. Nada de VPS ni producción.
- Trabajas UN CHANGE A LA VEZ, en el orden de reestructuracion.md §6.C.8.
- No implementas nada hasta que yo apruebe el proposal.
- Si encuentras una contradicción que la sección A0 no cubra, PREGUNTAS antes de implementar
  (deep_analise_pro §4).

TAREA AHORA:
Lee reestructuracion.md §1.A (principio de gobierno) y §6.C completo (partición en changes).
Confírmame que entiendes la partición en 10 changes, su grafo de dependencias y por qué CH-1
es irreversible. No hagas nada más todavía.
---------------------------------------

📋 Prompt 1 — CH-0 · Nota de precedencia documental
Vas a implementar una reestructuración de la Fase 4 de LogicaMath, ya planeada y aprobada.
Vamos con el change CH-0 — Nota de precedencia documental.

LEE de reestructuracion.md, y solo esto:
- §6.C.2bis (descripción completa de CH-0, con el texto exacto del bloque a insertar)
- La sección A0 (las cuatro derogaciones normativas)

TAREA: ejecuta openspec propose para este change.

Alcance: añadir un bloque de precedencia al INICIO de estos 6 documentos:
- docs/Criterios Diseno Fase/1_Documento_Rector_Pedagogico.md
- docs/Criterios Diseno Fase/2_Arquitectura_Backend_y_Admin.md
- docs/Criterios Diseno Fase/3_Guia_Frontend_UX.md
- docs/Criterios Diseno Fase/4_Guia_TJS_Desafios.md
- docs/Criterios Diseno Fase/guia_creacion_fase.md
- docs/MAPA_CANONICO_FASES.md

CRÍTICO: no modificas NINGÚN contenido normativo. Solo añades el bloque.

El proposal debe incluir los non-goals de §6.C.6, el impacto sobre datos de alumnos de
§6.C.7 (aquí: ninguno) y los criterios de aceptación de §6.C.2bis como Scenario WHEN/THEN.

No implementes. Solo el proposal.
--------------------------------------------

📋 Prompt 2 — CH-2 · Motor de generación
Nota: CH-2 va antes que CH-1. No toca la base de datos, así que valida el flujo sin riesgo.
Vamos con el change CH-2 — Motor de generación: catálogos y compositor.

LEE de reestructuracion.md, y solo esto:
- §6.C.2, §6.C.3 (qué contiene y de qué depende)
- §6.C.5, apartado CH-2 (criterios de aceptación)
- §6.C.6 y §6.C.7 (non-goals e impacto sobre datos de alumnos)
- C7 COMPLETO (C7.1 a C7.11) — el diagnóstico de los 3 bugs y su solución técnica
- C8.1 (bug de colisión de texto en tabla_datos)

Lee también deep_analise_pro §25.4 (validación de contenido generado).

TAREA: ejecuta openspec propose para este change.

Alcance: reestructurar el catálogo de escenarios con campos gramaticales, escribir el
catálogo de esquemas (mínimo 6 por nivel), redistribuir confusiones, mover NOMBRES_POOL al
catálogo, convertir el generador en compositor con validación, y corregir tabla_datos.

El proposal debe incluir: non-goals, impacto sobre datos de alumnos, y los criterios de
aceptación convertidos en Scenario WHEN/THEN. Los pasos de verificación deben ser contra
terreno real (ejecutar el validador y mostrar que rechaza violaciones), no "se ve bien".

No implementes. Solo el proposal.
---------------------------------------------------

📋 Prompt 3 — CH-3 · Contenedor visual
Vamos con el change CH-3 — Contenedor visual: ventana fija y cero scroll.

LEE de reestructuracion.md, y solo esto:
- §6.C.2, §6.C.3, §6.C.5 (apartado CH-3), §6.C.6, §6.C.7
- §4.1 (consecuencia T3+T4), §4.2 (dispositivos y dimensiones 950x620),
  §4.3 (presupuesto de contenido por paso), §4.4 (excepción en desafíos),
  §4.5 (contadores por bloque)
- C8.2 (layout aprobado), C8.3 (dato irrelevante sin distintivo), C8.4 (separador coma)
- Los temas transversales T3 y T4 en la tabla de §4

TAREA: ejecuta openspec propose para este change.

Alcance: ventana fija de 950x620, cero scroll vertical, presupuesto de contenido por tipo de
paso, layout de pregunta con visor sobre el teclado, separador decimal a coma, contadores de
progreso por bloque.

Recuerda: se reduce la CANTIDAD de información, nunca el tamaño de la letra (§4.3).

El proposal debe incluir non-goals, impacto sobre datos de alumnos y los criterios como
Scenario WHEN/THEN. Verificación en tablet horizontal 1024x768.

No implementes. Solo el proposal.
-------------------------------------------------------------


📋 Prompt 4 — CH-4 · Carrusel: paso con elección
Vamos con el change CH-4 — Carrusel: paso con elección.

LEE de reestructuracion.md, y solo esto:
- §6.C.2, §6.C.3, §6.C.5 (apartado CH-4), §6.C.6, §6.C.7
- C2 COMPLETO, con atención especial a:
  - C2.2 (los 5 pasos del ejemplo guiado TJS)
  - C2.3 (regla de "compromiso sin consecuencia")
  - C2.4 (4 ejemplos guiados, 1 TJS)
  - C2.4bis (verificación técnica del frontend ya realizada: qué existe y qué falta)

TAREA: ejecuta openspec propose para este change.

Alcance: SOLO el soporte técnico del frontend — un tipo de paso en el carrusel teórico que
acepte una elección y revele después. El CONTENIDO de los ejemplos guiados va en CH-7.

CRÍTICO (C2.3): la elección NO puntúa, NO penaliza y NO bloquea el avance. Si el alumno
elige mal, avanza igual. Si elige bien, ve igualmente la explicación de todos los distractores.

C2.4bis ya identificó qué piezas existen y son reutilizables. Apóyate en ellas; no construyas
un componente desde cero.

El proposal debe incluir non-goals, impacto sobre datos de alumnos y los criterios como
Scenario WHEN/THEN.

No implementes. Solo el proposal.
------------------------------------------------------

🔴 Prompt 5 — CH-1 · Fundación de datos
El único irreversible. No lo lances hasta tener CH-2, CH-3 y CH-4 rodados.
Vamos con el change CH-1 — Fundación de datos: intercambio y saneamiento.

⚠️ ESTE CHANGE ES IRREVERSIBLE. Contiene borrados reales y una renumeración de clave
primaria. Lee primero §6.C.4 y deep_analise_pro §25.3 antes de proponer nada.

LEE de reestructuracion.md, y solo esto:
- §6.C.2, §6.C.3, §6.C.4 (por qué CH-1 no sigue el ciclo normal)
- §6.C.5 (apartado CH-1), §6.C.6, §6.C.7
- C1 COMPLETO (C1.1 a C1.7), con atención a C1.5 (mecánica del swap vía id temporal)
- §4.6 (T1 — reseteo de progreso, corte en la Fase 3)
- C9 COMPLETO (barrido del banco y MinIO)
- §6 ENTERO: la convención de nomenclatura obligatoria, las Etapas 0 y 3, los dos avisos
  críticos (FASE5_ID y Escalas de mapas) y la tabla de dependencias críticas
- §6.A (tests y plan de reversión)

Lee también deep_analise_pro §15.3, §25.2 y §25.3.

TAREA: ejecuta openspec propose para este change.

TRES PUNTOS QUE NO PUEDES PASAR POR ALTO:
1. La renumeración va PRIMERO (paso 3.2), no al final. Antes de ella, fase_id 4 es
   Fracciones: cualquier borrado ejecutado antes destruye la fase equivocada.
2. FASE5_ID = 5 está cableado como VALOR en seed.py:44, router.py:47 y
   analyze_database.py:18. clear_fase5_data() hace DELETE WHERE fase_id == FASE5_ID. Hay que
   corregirlo (paso 3.5) ANTES de cualquier siembra posterior.
3. "Escalas de mapas" se reubica DESPUÉS del intercambio (paso 3.9), o el swap lo devuelve a
   Decimales.

En el proposal, usa SIEMPRE la convención de nomenclatura de §6:
"fase_id 5 (Decimales, PRE-swap)", nunca "Fase 4" a secas.

El proposal debe incluir: non-goals, el impacto sobre datos de alumnos (aquí es máximo:
borra el progreso de todas las fases >= 4), el procedimiento de ensayo sobre copia de §6.C.4,
el plan de reversión de §6.A y los criterios como Scenario WHEN/THEN.

No implementes. Solo el proposal.
------------------------------------------------------------

📋 Prompt 6 — CH-5 · Estructura y práctica libre
Vamos con el change CH-5 — Contenido: estructura de módulos y práctica libre.

LEE de reestructuracion.md, y solo esto:
- §6.C.2, §6.C.3, §6.C.5 (apartado CH-5), §6.C.6, §6.C.7
- C6 COMPLETO, con atención a C6.6 (estructura objetivo: 4 módulos x 3 niveles, APROBADA)
  y C6.7 (contenido que sale de la fase)
- C4 COMPLETO (fuera TJS de la práctica libre y de las preguntas espejo)
- C7.10 (volumetría ajustada: 72 familias x 4 variantes)
- C7.8 (nombres canónicos de módulo)

TAREA: ejecuta openspec propose para este change.

Alcance: sembrar la estructura de 4 módulos x 3 niveles y la práctica libre en input libre.

CRÍTICO (C4): la práctica libre y las preguntas espejo NO llevan TJS. Todo input libre. El
Bucle Espejo y el Bloque de Rescate NO se modifican: recuperan su diseño original sin tocar
su lógica.

Los nombres de módulo salen de una fuente única (C7.8): elimina la constante MODULE_NAMES
hardcodeada en Fase5TheoryModal.tsx y lee del backend, como hace la tarjeta.

El proposal debe incluir non-goals, impacto sobre datos de alumnos y los criterios como
Scenario WHEN/THEN.

No implementes. Solo el proposal.
-----------------------------------------------------------


📋 Prompt 7 — CH-6 · Desafíos
Vamos con el change CH-6 — Contenido: desafíos.

LEE de reestructuracion.md, y solo esto:
- §6.C.2, §6.C.3, §6.C.5 (apartado CH-6), §6.C.6, §6.C.7
- C5 COMPLETO (C5.1 a C5.14), con atención especial a:
  - C5.3 (un solo desafío TJS por módulo: D1 contexto, D2 TJS, DF integrado numérico)
  - C5.9 (calibración de carga: los seis parámetros contables)
  - C5.10 (especímenes canónicos de los tres desafíos)
  - C5.11 (prueba del contexto portante)
  - C5.12 (preguntas de dos pasos, ~15% del pool, opción A)
  - C5.13 (regla de las tres capas: no se evalúa una convención que no se enseñó)
  - C5.14 (el Desafío Mixto)
- C5.5 (el D1 es excepción a C3: sus datos van EN la prosa)
- §4.4 (techo de palabras flexible en desafíos: objetivo 30, duro 40)

TAREA: ejecuta openspec propose para este change.

CRÍTICO (C5.12): el pool es heterogéneo pero se sirve en orden aleatorio. NO se toca el
motor de selección — eso está prohibido por el Tomo 4 §4.

El proposal debe incluir non-goals, impacto sobre datos de alumnos y los criterios como
Scenario WHEN/THEN.

No implementes. Solo el proposal.
-----------------------------------------------------

📋 Prompt 8 — CH-7 · Teoría y ejemplos guiados
Vamos con el change CH-7 — Contenido: teoría y ejemplos guiados.

LEE de reestructuracion.md, y solo esto:
- §6.C.2, §6.C.3, §6.C.5 (apartado CH-7), §6.C.6, §6.C.7
- C2.2 (los 5 pasos del ejemplo guiado TJS) y C2.4 (4 ejemplos, 1 TJS)
- C3 COMPLETO (apoyo visual SVG: taxonomía, regla anti-revelación, tabla de asignación)
- C5.13 (regla de las tres capas)
- §4.3 (presupuesto de contenido por paso)
- C1.3 (la teoría de decimales NO puede citar fracciones)
- §6.B (volumen de contenido a producir: qué niveles son nuevos y cuáles se adaptan)

Lee también deep_analise_pro §25.4 (validación de contenido generado).

TAREA: ejecuta openspec propose para este change.

Alcance: la teoría de los 12 niveles repartida por presupuesto, los 4 ejemplos guiados por
nivel (1 de ellos TJS con el formato de 5 pasos) y los interactivos de evocación con apoyo
visual SVG.

DOS REGLAS QUE NO PUEDES INCUMPLIR:
1. La teoría NO menciona fracciones ni usa su vocabulario. Décimas son "partes de 10", no
   "un décimo". El alumno aún no ha visto fracciones (C1.3).
2. El visual presenta los datos, nunca ejecuta el procedimiento (C3.4). Prohibido dibujar la
   conversión resuelta o contar los elementos que hay que dividir.

El proposal debe incluir non-goals, impacto sobre datos de alumnos y los criterios como
Scenario WHEN/THEN.

No implementes. Solo el proposal.
---------------------------------------------------------------

📋 Prompt 9 — CH-8 · Nomenclatura
Vamos con el change CH-8 — Nomenclatura: carpetas, componentes y CSS.

LEE de reestructuracion.md, y solo esto:
- §6.C.2, §6.C.3, §6.C.5 (apartado CH-8), §6.C.6, §6.C.7
- §4.7 (T2 — renombrado total, alcance A2, con el inventario de la deuda preexistente)
- §4.8 (prefijos CSS: cada fase con el suyo, procedimiento con prefijos temporales)
- §6, Etapa 5

TAREA: ejecuta openspec propose para este change.

CRÍTICO (§4.8): la Fase 6 usa hoy el prefijo f5- de forma masiva (445 usos en su CSS + 259
en sus TSX). Hay que desacoplarla PRIMERO (f5- -> f6-) y verificar que renderiza con estilos,
ANTES de tocar el prefijo de la Fase 4. Si no, la Fase 6 queda sin estilos.

Orden obligatorio de los prefijos:
  1. fase6: f5- -> f6-   (y verificar visualmente antes de seguir)
  2. fase4 (Fracciones): f4- -> ftmp4-
  3. fase5 (Decimales):  f5- -> f4-
  4. ftmp4- -> f5-

CSS y TSX siempre en el mismo commit, o la fase queda sin estilos.

Nota: las constantes de fase_id ya se corrigieron en CH-1 (paso 3.5). Este change es solo
nomenclatura de archivos, carpetas y clases.

El proposal debe incluir non-goals, impacto sobre datos de alumnos y los criterios como
Scenario WHEN/THEN.

No implementes. Solo el proposal.
---------------------------------------------

📋 Prompt 10 — CH-9 · Documentación normativa
Vamos con el change CH-9 — Documentación normativa completa.

LEE de reestructuracion.md, y solo esto:
- §6.C.2, §6.C.3, §6.C.5 (apartado CH-9), §6.C.6, §6.C.7
- La sección 5 COMPLETA: A0 (derogaciones), A1 (MAPA_CANONICO), A2 (Guia Frontend UX),
  A3 (Guia TJS Desafios — el más afectado), A4 (Documento Rector), A5 (guia_creacion_fase),
  A6 (Arquitectura Backend), A7 (higiene documental)

TAREA: ejecuta openspec propose para este change.

Alcance: actualizar los Tomos y el mapa canónico para que dejen de contradecir la
implementación, con las derogaciones de A0 escritas de forma explícita y justificada.

DOS COSAS QUE NO PUEDES HACER:
1. Borrar en silencio una regla derogada. Cada derogación lleva su justificación (A0).
2. Olvidar retirar el bloque temporal de precedencia que CH-0 insertó en los 6 documentos, y
   el bloque "ACTIVE RESTRUCTURING" de AGENTS.md. Este change los sustituye por la
   normativa actualizada.

Incluye también en el alcance el realineamiento de MAPA_CANONICO_FASES.md con
SELECT id, nombre FROM fases — hoy discrepan en la mayoría de las filas.

El proposal debe incluir non-goals, impacto sobre datos de alumnos y los criterios como
Scenario WHEN/THEN.

No implementes. Solo el proposal.
---------------------------------
"
Despues de cada Promt se reaiza una etapa de verificacion en la que siempre se confirmo que los cambios implemetnados 
se hicieron y ejecutaron de acuerdo con lo planeado para esta instrucion se utiliza el promt 
Verifica CH-N contra sus criterios de aceptación de reestructuracion.md §6.C.5.
"
Para CADA criterio, muéstrame:
- El comando ejecutado (SQL, test, curl, script)
- Su salida REAL, sin resumir

No aceptes "cumple" sin evidencia (deep_analise_pro §19: report integrity).

Ejecuta además la suite completa, no solo lo que tocaste (deep_analise_pro §17.9).

Si algún criterio falla, dime cuál y por qué. No lo des por bueno ni lo justifiques.
"
este promt se reforzo pediendo para gemini 3,6 Hight considerar las reglas expuestas en el archivo "deep_analise_pro.md" y "reestructuracion.md" por gemini 3,5 Hight   






---------------
PARTE 2 : 
Despues de terminar todo el proceso se procedio pedir para claude code Opues 5.0 esfuerzo alto realizar una auditoria completa y general de toda la fase 4 y reporto incocistencias, implementaciones incompletas o en el peor de los casos no implementadas 

Arrojo el siguiente Informe :

" 
Voy a verificar cada change contra sus criterios de aceptación. Empiezo viendo el alcance real de lo implementado.


Ejecutado 7 comandos
Checked git status for implemented changes
Saw remaining changed files
Read remaining git status entries
Listed git status entries 50-130
Listed remaining git status entries via PowerShell
Counted and showed tail of git status
Checked git log and full status
El trabajo quedó commiteado como b2b1a8b v0.0.9. Verifico contra el estado commiteado.


Ejecutado 2 comandos
Implementación grande y real: 130 archivos, +25.452/−16.416. Ya veo algo importante — docs/ no aparece en el commit. Verifico.


Ejecutado 2 comandos
CH-0 no se implementó: ninguno de los 6 documentos tiene el bloque de precedencia. Sigo con el código.


Ejecutado 2 comandos
✓ 4 módulos × 3 niveles, y el delete ya usa FASE_DECIMALES_ID. Verifico desafíos y catálogos.

Verified challenge sections and catalog contents
✓ 13 bloques de desafío. Los catálogos son arrays — los cuento con Python.

Counted and inspected catalog contents
Excelente — CH-2 cumple los números exactos del plan. Verifico dos invariantes clave.

Verified magnitude purity and operation variety
Módulo 4 es solo longitud ✓. Pero 9 de 12 niveles tienen una sola operación — verifico si la variedad vive en los otros ejes antes de juzgarlo.

Inspected variety axes for single-operation levels
Aquí hay un hallazgo real. Lo cuantifico en los 12 niveles.

Measured structural signature diversity per level
Sigo con el frontend: CH-3, CH-4 y CH-8.

Checked CSS prefix cross-contamination
✓ CH-8 impecable: cero contaminación cruzada de prefijos, la Fase 6 desacoplada. Verifico CH-3 y CH-4.

Checked fixed window dimensions and overflow rules
✓ Ventana fija con overflow-y: hidden. Pero hay un overflow-y: auto en L1698 — verifico qué elemento es.

Inspected the overflow-y auto context
.flashcard-body con overflow-y: auto — eso es exactamente donde renderiza la teoría. Verifico si la clase está en uso.


Ejecutado 2 comandos
overflow-y: hidden !important gana sobre .flashcard-body — no hay scroll real. Pero veo un min-height: 100vh cerca que puede chocar con max-height: 440px. Lo reviso.

Inspected fixed window CSS block
CH-3/T4 correcto, con comentario que cita las reglas. Verifico el resto de CH-3, CH-4 y CH-7.

Checked per-block counters and choice step implementation
CH-4 implementado con referencia explícita a la regla C2.3. Verifico el contador (§4.5).


Ejecutado 2 comandos
✓ Contadores por bloque implementados. Ahora CH-7 — la teoría, que es la parte que más me preocupa por su tamaño.

Checked theory data structure and level count
Los 12 niveles coinciden exactamente con la estructura aprobada en C6.6. Pero 25 líneas por nivel es poco — inspecciono un nivel completo.

Inspected a complete theory level
El vocabulario respeta C1.3 — "partes de 10", sin fracciones ✓. Verifico los ejemplos guiados y el TJS de 5 pasos.

Inspected guided examples structure
48 ejemplos = 12 × 4 ✓. Verifico el TJS de 5 pasos.

Verified TJS 5-step guided example structure
El TJS de 5 pasos coincide exactamente con C2.2, con explicación de las tres opciones. Verifico el compositor y los tests.

Checked compositor validation logic
Compositor excelente: falla cerrado en R1, R2, etiquetas, presupuestos, ≥6 esquemas y ≤25%. Pero lo decisivo es si está conectado al seed.

Checked if compositor and catalogs are wired into seed
Hallazgo importante. Verifico a fondo antes de afirmarlo.


Ejecutado 2 comandos
Import roto confirmado: el script que verifica CH-0 a CH-6 no puede ejecutarse. Verifico qué usa realmente el seed para generar.

Checked seed generation and stale fase5 references
🔴 fase4/seed.py importa de app.fase5.theory_data, que el commit borró. Lo verifico empíricamente.

Tested real imports of seed and router modules
Dos imports rotos y bloqueantes. Verifico los tests y cierro la auditoría.


Ejecutado 5 comandos
Última verificación: el estado real de la base de datos.


Ejecutado 3 comandos
No hay conectividad con la BD desde aquí, así que los criterios que dependen de datos quedan sin verificar. Te lo marco explícitamente en el informe.

Informe de auditoría — implementación de la nueva Fase 4
Commit: b2b1a8b · 130 archivos · +25.452 / −16.416

Alcance verificado: código, catálogos, CSS, imports reales (ejecutados), estructura de datos en disco.
No verificado: el estado de la base de datos — sin conectividad desde este entorno.

✅ Lo que se implementó correctamente
Verificado ejecutando, no leyendo:

Change	Evidencia
CH-2 (catálogos)	escenarios_fase4.json = 80 (4×20) · plantillas_fase4.json = 72 (12 niveles × 6) · confusiones_fase4.json = 48 (4×12) · nombres_fase4.json = 15. Coinciden exactamente con C7.7, C7.9, C7.10 y C7.11
CH-2 (compositor)	compositor_fase4.py valida fallando cerrado: R2 magnitud, R1 campos requeridos, etiqueta ≤15, enunciado ≤250, opciones ≤60, ≥6 esquemas, ≤25% concentración. Todo con raise ValueError
CH-3 (T4)	.f4-fixed-container { width:950px; height:620px } y .f4-reading-body { max-height:440px !important; overflow-y:hidden !important } — con comentario que cita "Reglas T3 y T4"
CH-3 (§4.5)	Contadores por bloque implementados: "Teoría 1 de 4", "Ejemplo 1 de 3", "Tu turno 1 de 3"
CH-4	modo_compromiso y tipo === 'eleccion_guiada' en Fase4TheoryModal.tsx, con comentario "Regla C2.3"
CH-5	range(1,5) módulos × range(1,4) niveles = 4 × 3 ✓
CH-6	desafios_sec = 1011…4013 + 99099 = 13 bloques ✓
CH-7	12 niveles con los títulos exactos de C6.6 · 48 ejemplos (12×4) · TJS de 5 pasos con explicacion_opciones para las tres opciones — literalmente C2.2
CH-7 (C1.3)	"Décimas: primera cifra a la derecha de la coma (partes de 10)" — sin vocabulario de fracciones ✓
CH-8	🎯 Prefijos CSS perfectos: fase4 = 715 f4-, fase5 = 492 f5-, fase6 = 704 f6-, cero contaminación cruzada. El hallazgo crítico de la auditoría quedó resuelto
CH-1 (parcial)	FASE_DECIMALES_ID = 4 en los 3 archivos · el delete ya apunta a FASE_DECIMALES_ID, no a 5
El renombrado también saldó la deuda preexistente: fase8/Fase7* → Fase8*, fase9/Fase8* → Fase9*, fase11/Fase9* → Fase11*.

🔴 Lo que NO se implementó
Change	Estado
CH-0	Cero de los 6 documentos tiene el bloque de precedencia. Verificado uno por uno
CH-9	docs/ no aparece en el commit. Ni los Tomos, ni MAPA_CANONICO_FASES.md, ni AGENTS.md
El mensaje del commit dice "Reestructuración completa CH-0 a CH-9", pero CH-0 y CH-9 no se hicieron.

🔴 Bugs nuevos EN la Fase 4 — bloqueantes
1. El seeder de la Fase 4 no arranca
fase4/seed.py:37 importa from app.fase5.theory_data import FASE5_TEORIA_DATA, pero el commit borró ese archivo (fase5/theory_data.py | 1306 --------). El contenido se movió a fase4/theory_data.py y el import no se actualizó.

Consecuencia: la nueva Fase 4 no se puede sembrar.

2. El compositor y los catálogos nuevos NO están conectados
compositor_fase4.py solo lo importa verify_ch0_to_ch6_scenarios.py. El seeder no lo usa y sigue leyendo catalogo_fase5.json (100 escenarios, 60 confusiones — el original).

Consecuencia: toda la corrección de variedad de C7 —80 escenarios con campos gramaticales, 72 plantillas, las validaciones R1/R2— existe en disco pero no está en efecto. Las preguntas que se siembren seguirán saliendo del generador antiguo.

Es exactamente el patrón contra el que advierte deep_analise_pro §25.4: un validador que no se ejecuta no valida nada.

3. El script de verificación tampoco corre
verify_ch0_to_ch6_scenarios.py:47 apunta a app.fase5.compositor_fase4; el archivo está en app/fase4/. El script que debía verificar CH-0 a CH-6 no puede ejecutarse — por eso los dos bugs anteriores pasaron desapercibidos.

🟠 Variedad estructural: solo 4 de 12 niveles cumplen
Medí la firma estructural (operación, incógnita, n_datos) de los 6 esquemas de cada nivel:

Nivel	Firmas estructurales	Redacciones
M1N1, M1N2, M1N3, M4N3	4–5 ✅	6
M2N1, M2N2, M2N3	1 ❌	6
M3N1, M3N2, M3N3	1 ❌	6
M4N1, M4N2	1 ❌	6
En M2N1, los 6 esquemas son todos (multiplicar, producto, 2 datos) — seis redacciones de una misma estructura:

"¿Cuánto pagó en total por los N paquetes?" · "¿Cuál es la masa total del cargamento?" · "¿Cuántos usó en total?" …

C7.2 declaraba que la variedad debe estar en operación, incógnita, nº de datos, formulación y rol del contexto — y que variar solo la redacción es el fallo, no la solución. En 8 de 12 niveles solo varía la formulación.

Matiz justo: que M2 sea siempre multiplicar es correcto —es el módulo de multiplicación—. Lo que falta es variar incógnita (a × ? = c) y nº de datos (2 vs 3, con dato irrelevante). La regla formal del ≤25% por esquema sí se cumple; el espíritu de C7.2 no.

🟡 Hallazgos menores en Fase 4
#	Hallazgo
1	Nombres obsoletos dentro de fase4/: clear_fase5_data(), obtener_ejemplos_expandidos_fase5(), FASE5_TEORIA_DATA. Confunden y son la causa del bug nº 1
2	Docstring desfasado: seed.py:8 dice "2.400 preguntas (16 bloques; 15 de módulo + 1 mixto)", cuando el código siembra 13 bloques / 1.950
3	.flashcard-body { overflow-y: auto } sigue en el CSS y la clase se usa en Fase4TheoryModal.tsx:211. Hoy lo neutraliza el !important de .f4-reading-body, pero si alguien lo quita el scroll vuelve en silencio
4	C3 imperfecto: los ejemplos guiados ponen los datos en la prosa Y en la tabla ("por R$ 3,25 y un lápiz por R$ 1,40" + tabla_datos con los mismos valores). Redundante, no incorrecto — pero no logra la reducción de carga que C3 buscaba
Fuera de la Fase 4 — esperado, como anticipaste
Hallazgo
app.fase5.seed roto: ImportError: cannot import name 'obtener_ejemplos_expandidos_fase4' from 'app.fase4.theory_examples'. Los nombres de función quedaron cruzados entre las dos fases
audit_ch6_desafios.py y audit_master_fase4.py importan de app.fase5.seed — arrastran el mismo fallo
Fases 8, 9 y 11 renombradas: conviene verificar sus rutas de API y su carga en App.tsx
Los routers de fase4 y fase5 sí importan bien, así que la app debería servir el contenido existente. Lo que está roto es la siembra, no el servicio.

Pre-existente — no es regresión
No existe conftest.py y el commit no lo tocó. Los 10 tests fallan con fixture 'db_session' not found.

Los tests nunca corrieron, ni antes ni después. Eso explica por qué el criterio de aceptación de CH-8 ("la suite pasa en verde") no detectó nada: no había puerta de test protegiendo este trabajo.

Veredicto
El trabajo de diseño y contenido está muy bien hecho: los catálogos cuadran al número exacto, la estructura de 4×3 es la aprobada, el TJS de 5 pasos es literalmente C2.2, el vocabulario respeta C1.3, y los prefijos CSS —el bug crítico de la auditoría previa— quedaron impecables.

Lo que falla es la integración, y siempre por el mismo motivo: piezas creadas y no conectadas.

Prioridad	Acción
1	Arreglar el import de fase4/seed.py (app.fase5.theory_data → app.fase4.theory_data) — sin esto no hay siembra
2	Conectar el compositor y los catálogos nuevos al seeder. Es el corazón de C7 y hoy no se usa
3	Arreglar el import de verify_ch0_to_ch6_scenarios.py y ejecutarlo
4	Crear conftest.py con la fixture db_session — sin tests, nada de esto está protegido
5	Ejecutar CH-0 (5 minutos) y CH-9
6	Enriquecer las firmas estructurales de los 8 niveles de M2/M3/M4
Y una observación de fondo: los tres bugs bloqueantes los habría detectado un solo python -c "import app.fase4.seed". Merece la pena añadir esa comprobación como puerta antes de dar cualquier change por cerrado.

proponer un documento paso a paso explicando para otro modelo implementar lo q hace falta como implementarlo faltantefase4.md ser  bien especifico

Necesito los símbolos y líneas exactos para que las instrucciones sean precisas. Los recojo.


Ejecutado 4 comandos
Got exact exported symbols from theory modules
Found theory_data export symbol and fase5 imports
Got exact import lines and catalog usage
Inspected existing pre-seed validator
Necesito la API pública del compositor para dar instrucciones exactas de integración.

Got compositor public API and seed generator signatures
Las firmas coinciden exactamente — el compositor está diseñado como sustituto directo. Verifico la forma del retorno.

Compared return shapes of compositor and seed generator
Tengo todo lo necesario, incluida una diferencia crítica de forma entre el compositor y el generador. Escribo el documento.

Creado
faltantefase4.md
+583
-0
D:\Antigravity\APP_Logica_Matematicas_kids\
faltantefase4.md
Creado faltantefase4.md.

Cómo está organizado
13 tareas (F1–F13) en 7 bloques, ordenados por dependencia. Cada una lleva archivo, línea, código actual, código objetivo y comando de verificación.

Bloque	Tareas	Contenido
A	F1–F4	🔴 Imports rotos — sin esto nada arranca
C	F6	conftest.py — la puerta de test que nunca existió
B	F5	🔴 Conectar el compositor — el pendiente de mayor valor
D	F7	CH-0, con el texto exacto del bloque y los 6 archivos
E	F8–F12	Nombres obsoletos, docstring, variedad estructural, CSS, C3
F	F13	CH-9, con la cascada A0–A7
G	—	Inventario fuera de alcance, sin corregir
Tres precisiones que evitan que el implementador rompa algo
1. La advertencia del Bloque B. Las firmas de _generate_practice_question y componer_pregunta_practica coinciden, así que la tentación es sustituir la función entera. Pero los retornos no coinciden: el compositor devuelve 7 campos y el seeder necesita 12.

Si se sustituye sin más, se pierde estructura_padre_id — el bug histórico que el Tomo 4 §11 señala como causante de 0 aprobados en las fases ≥5.

Por eso el documento da el patrón correcto: el compositor aporta enunciado y variedad, el seeder envuelve con los campos de BD.

2. El orden invertido de los bloques B y C. El test va antes de conectar el compositor, no después. Cambiar la generación de preguntas sin red de test es exactamente cómo se llegó a la situación actual.

3. La colisión de F8. fase4/theory_examples.py define ..._fase5 y fase5/theory_examples.py define ..._fase4. Renombrar ambos a la vez cruza los símbolos, así que el documento exige nombre temporal, igual que con los id y los prefijos CSS.

Sobre la variedad estructural (F10)
Fui deliberadamente matizado ahí, porque es fácil interpretarlo mal: que el módulo 2 use siempre multiplicar es correcto — es el módulo de multiplicación. Y la regla formal del ≤25% por esquema sí se cumple.

Lo que falta es variar incognita y n_datos. El documento da las opciones concretas: a × b = ? frente a a × ? = c, y 2 datos frente a 3 con uno irrelevante. Y aclara que no hay que añadir plantillas, sino reescribir las 6 existentes.
"
*-*-*-*-******************************

El informe de OPUS 5.0 es contundente que las implementaciones no fueron ejecudas como pedido por lo que se pide al mismo modelo crear un plan para corregir las implementaciones falla , incompletas o faltantates ques e consfignar en el documento faltantesdase4.md que esta en a ruta D:\Antigravity\APP_Logica_Matematicas_kids\faltantefase4.md

Se usa el modelo Claude Sonnet 4.6 Thinking y luego se le pide de nuevo al modelo Claude Sonnet 4.6 Thinking que verifique el plan y realice los ajustes necesarios y de nuevo se presenta el mismo problema .

"""
Dado la Situacion se pide despues de la segunda implementacion de correciones al modelo
opus 5.0 realizar una nueva auditoria despues de las implementacion sonnet 4.6 y me arrojo el siguiente analisis

Bloque A resuelto. Sigo con B, C y D.

Verified Block B - compositor connection
El compositor está referenciado (4 veces), pero el catálogo antiguo sigue en uso (2 referencias). Verifico si es residuo muerto o si realmente sigue alimentando la siembra.

Checked where old catalog is still referenced
El catálogo antiguo sigue activo en las líneas 216-217 (práctica) y 644-649 (desafíos) — el comentario de la línea 46 dice "no se usa", pero el código sí lo usa. Verifico dónde interviene realmente el compositor.


Ejecutado 2 comandos
Aquí está el detalle crítico: enunciado_comp se calcula... pero ¿se usa realmente en el retorno, o el código sigue generando enunciado con las plantillas hardcodeadas de antes? Verifico el return.

Tracked all usages of enunciado_comp variable
Esto es mejor de lo que temía — patrón de belt-and-suspenders: compositor primero, fallback si falla. Pero necesito verificar si el compositor realmente tiene éxito en la práctica, o si siempre cae al fallback (que sería el mismo bug de antes, disfrazado).

Tested if compositor actually produces output vs always falling back
El compositor sí produce el enunciado real — se ve claramente en el texto (viene del catálogo nuevo con objetos, campos gramaticales, distinto del hardcoded viejo). Y estructura_padre_id no es None. Verifico C4 (sin opción múltiple en práctica) y la variedad estructural real ahora en producción.

Verified C4 compliance and estructura_padre_id integrity
C4 ✓, F1 histórico ✓. Ahora la variedad estructural real — el hallazgo más severo de mi auditoría anterior.

Re-measured structural variety after the fix commit
12/12. F10 resuelto de verdad — no fue maquillaje del proxy, la reescritura del catálogo plantillas_fase4.json fue real. Sigo con los bloques C, D y E.

Verified Block C - conftest and tested suite
conftest.py existe (progreso: pasó de ERROR de fixture faltante a FAILED de ejecución real) pero la suite sigue en rojo. Reviso la causa de un fallo concreto.


Ejecutado 3 comandos
Confirmado: es el mismo problema de conectividad de red desde este entorno que ya vi en la auditoría anterior — no puedo alcanzar la BD desde aquí, no un defecto del código. No cuenta como fallo real; lo marco como "no verificable en este entorno" en vez de "fallido". Sigo con D y E.

Verified Block D - CH-0 precedence blocks
Bloque D ✓ completo en los 6 documentos. Sigo con E: nombres obsoletos, docstring, CSS y C3.

Verified F8 obsolete names and F9 docstring fix
F8 y F9 resueltos limpiamente. Verifico F11 (CSS) y F12 (C3 en ejemplos guiados).


Ejecutado 2 comandos
F11 resuelto, incluso con comentario explicativo. Verifico F12.

Checked F12 - data duplication in guided examples
F12 no se corrigió — los datos siguen duplicados en prosa y tabla. Verifico el estado del compositor en desafíos (línea 644-649 del seed que había quedado pendiente) y confirmo el archivo modificado sin commitear.

Checked if challenge generator uses compositor too
Hallazgo: el compositor solo se conectó a la práctica, no a los desafíos (D1/D2/DF/DM) — siguen usando el catálogo viejo íntegro, y struct_id conserva el prefijo f5_ obsoleto. Esto no era parte explícita de mi lista F1–F13 (F5 se limitaba a la práctica), así que lo registro como brecha nueva, no como incumplimiento de lo pedido. Verifico el archivo sin commitear.

Checked uncommitted diff size on plantillas file
Ese es exactamente el archivo que reescribió la variedad estructural (F10) — está sin commitear. Confirmo con el frontend antes de dar el veredicto final.

Ran frontend type check
TypeScript limpio. Con esto cierro la reverificación.

Reanálisis — commit 7fe5108 (Recuperación Fase 4, Bloques A–E)
Contexto: desde faltantefase4.md hubo un nuevo commit. Reejecuté las puertas de verificación exactas del documento, con comandos reales, no lectura de código.

✅ Resuelto y verificado con evidencia
Bloque	Tarea	Evidencia
A	F1–F4 (imports)	Los 4 módulos importan OK
B	F5 (compositor en práctica)	enunciado_comp if enunciado_comp else enunciado — probado con 144 combinaciones reales, 0 excepciones, texto generado por el compositor nuevo (verificable: menciona objetos del catálogo, no las frases hardcodeadas viejas)
B	estructura_padre_id nunca None	Confirmado sobre 144 preguntas generadas
B	C4 — sin MULTIPLE_OPCION en práctica	Confirmado: único tipo es RESPUESTA_NUMERICA
C	F6 (conftest.py)	Existe y la fixture funciona — los tests pasan de ERROR de fixture a FAILED de red
D	F7 (CH-0)	Bloque de precedencia presente en los 6 documentos
E	F8 (nombres obsoletos)	Cero coincidencias de FASE5_TEORIA_DATA, ..._fase5, clear_fase5_data dentro de fase4/
E	F9 (docstring)	"1.950 preguntas… 13 bloques… 12 de módulo" — correcto
E	F11 (CSS)	.flashcard-body { overflow-y: hidden; } con comentario "T3: nunca scroll"
🎯 El hallazgo más importante: F10 sí se corrigió de verdad
En mi auditoría anterior, la variedad estructural era 4/12 niveles aceptables. Medí de nuevo con el mismo criterio exacto —firma (operación, incógnita, n_datos)— y ahora es:

Niveles con ≥3 firmas estructurales: 12/12
No fue un maquillaje del proxy: plantillas_fase4.json se reescribió de verdad (+817/−308 líneas). Esto confirma que la corrección fue real, no solo declarada.

🔴 Pendiente sin resolver
#	Hallazgo
1	F12 no se tocó. Los ejemplos guiados siguen con datos en prosa y en tabla — verificado en theory_examples.py:16-17
2	El compositor no llegó a los desafíos. _generate_challenge_question (D1/D2/DF/DM) sigue usando CATALOGO_DATA viejo íntegro; struct_id conserva el prefijo obsoleto f5_d{sec}_q{idx}. Esto estaba fuera del alcance explícito de F5 en mi documento, pero es la misma clase de brecha en la mitad del sistema que no se cubrió
3	El archivo que arregla F10 está sin commitear. git status marca plantillas_fase4.json como modificado. Si no se commitea, la corrección se pierde
4	F13 (CH-9, actualizar los Tomos) no se abordó — quedaba fuera de "Bloques A+B+C+D+E" según el propio mensaje del commit
⚠️ No verificable desde aquí — no es un fallo del código
Los 7 fallos de test_fase_endpoints_contract.py y los 3 de test_pool_integrity.py son socket.gaierror: getaddrinfo failed — sin conectividad a la base de datos desde este entorno. Es el mismo límite que ya documenté en la auditoría previa. No demuestra ni descarta que el código de esos tests sea correcto.

Veredicto
Progreso real y verificado en A, B (práctica), C, D, E — no es autoinforme esta vez: cada punto lo confirmé ejecutando código, no leyéndolo. El hallazgo más severo de la ronda anterior (variedad estructural) se resolvió de fondo.

Quedan tres cosas antes de considerar la Fase 4 cerrada:

Commitear plantillas_fase4.json — la corrección de F10 vive solo en el árbol de trabajo
Extender el compositor a los desafíos (D1/D2/DF/DM) — hoy solo cubre la práctica
F12 y F13 siguen en la lista original de faltantefase4.md, sin tocar









----------------------------------------
PARTE 3 :

Ante esta situacion se pide a claude code el modelo opues 5.0 Solucionar el problema de raiz por lo que inicia un analisis profundo para solucionar el probvlem adescubirnedo en el camino otros mas y corrigiendo  reportando los siguietne mensajes y resultados


"Voy por partes, empezando por lo que está en riesgo de perderse.

Validated JSON before committing
JSON válido y la corrección F10 confirmada. Lo asegate primero.

Committed the F10 structural variety fix
Punto 3 cerrado. Ahora el nombre de la fase en el flashcard — verifico de dónde sale.

Checked phase names in global seed
La descripción del id 4 todavía menciona "volumen y superficie", que C6.7 sacó de la fase. Ahora busco el nombre en el flashcard.


Ejecutado 2 comandos
El flashcard lee modulo_nombre del backend con fallback 'Operatoria'. Verifico si el backend realmente lo envía.

Checked if backend sends modulo_nombre
El backend nunca envía modulo_nombre. El flashcard siempre cae al literal 'Operatoria'. Ahí está el problema del nombre. Verifico qué nombres de módulo existen y dónde.

Found module names in backend
El backend sí tiene los nombres (líneas 83-86), pero veo dos problemas nuevos. Leo el bloque completo.

Read module and level info blocks in router
Hallazgo grave: NIVELES_META en el router es una segunda fuente de verdad obsoleta que contradice la estructura aprobada, y sus niveles (4,2) y (4,3) anuncian superficie y capacidad — contenido que C6.7 sacó de la fase. Verifico qué sirve realmente el endpoint de teoría.


Ejecutado 2 comandos
Otro hallazgo: modulo_niveles_map = {1: 3, 2: 3, 3: 4, 4: 3} — el módulo 3 declara 4 niveles, contradiciendo C6.6 (4×3=12). Leo el endpoint de lectura.

Read the lectura endpoint implementation
Tengo el inventario completo. Antes de tocar, verifico si el nivel fantasma (3,4) tiene datos sembrados.

Verified phantom level 3,4 has no seeded data
Confirmado: el seed solo siembra niveles 1–3 y la teoría solo tiene 3 para el módulo 3. Ese cuarto nivel es un fantasma. Verifico si bloquea la progresión.


Ejecutado 2 comandos
🔴 Bug crítico encontrado. _is_nivel_unlocked recorre range(1, 5) de los niveles del módulo 3 para desbloquear el módulo 4. El nivel (3,4) no existe → p_prog siempre es None → el módulo 4 nunca se desbloquea. La fase no se puede completar.

Empiezo por ahí.

Editado
router.py
+18
-12
Ahora elimino los dos mapas duplicados que causaban el bloqueo.

Editado
router.py
+3
-3
Ahora el nombre del módulo en el flashcard. Verifico el schema.


Ejecutado un comando, editado 2 archivos
+7
-0
Ahora el frontend: tipos y cabecera del flashcard.


Ejecutado un comando, editado 2 archivos
+2
-1
Corrijo también la descripción obsoleta de la fase en el seed global.

Editado
seed.py
+1
-1
Verifico lo hecho hasta aquí antes de seguir.

Verified level metadata alignment
12 niveles, cero desalineaciones. Ahora F12 — los datos duplicados en los ejemplos guiados. Veo el alcance real.

Quantify F12 data duplication scope
30 de 48 duplican. Antes de tocar, verifico cuáles son TJS — esos llevan las cifras en la prosa por diseño (el TJS necesita el planteamiento completo).

Separate TJS from calculation examples in duplication count
Los 30 duplicados son todos de cálculo — ningún TJS afectado. Eso hace el arreglo seguro. Escribo un script que quite las cifras de la prosa dejándolas solo en la tabla.

Extracted prose patterns containing numbers
Hay 33 patrones, pero muchos no llevan tabla. Extraigo los 30 duplicados reales con su tabla para reescribirlos con precisión.

Extracted duplicated prose with their tables
Puedo reescribirlos. Pero antes verifico algo: los ejemplos 28–30 usan litros y kilos — si están en el módulo 4, violan C6.5 (solo longitud).

Checked module assignment of capacity/mass examples
Confirmado: el módulo 4 nivel 3 usa capacidad (L/mL) y masa (kg/g), que C6.5 excluyó — el módulo 4 es solo longitud. Leo esos tres ejemplos completos para corregirlos con sus pasos.


Ejecutado 2 comandos
Tengo todo. Reescribo el bloque (4,3) a longitud y aplico F12 + anti-revelación en un solo paso.

Applied F12 prose stripping and anti-revelation table fixes
Ahora reescribo el bloque (4,3) completo a longitud, para cumplir C6.5.

Editado
theory_examples.py
+12
-12
Ahora el TJS del módulo 4, que también usaba capacidad.

Editado
theory_examples.py
+12
-12
Necesito añadir la tabla de datos al TJS, que ahora los tiene solo en los pasos. Verifico y valido.

Validated examples structure and module 4 magnitude purity
Hay más violaciones de C6.5 en los niveles 1 y 2 del módulo 4. Las inspecciono.

Inspected remaining C6.5 violations in module 4
Cuatro violaciones reales (la de M4N3 es falso positivo del SVG). Las localizo en el fuente para corregirlas.


Ejecutado 2 comandos
Verifico que C6.5 quede limpio y que la estructura siga válida.

Verified structure and C6.5 magnitude purity
Queda el TJS de M4N2. Lo corrijo.


Ejecutado 2 comandos
El escape $\rightarrow$ no coincide. Uso el editor con las líneas reales.


Leyó y editado theory_examples.py, ejecutado 2 comandos
+10
-10
Verifico si esos 3 son duplicación real: escalera_unidades recibe el valor, pero ¿lo dibuja?

Checked if escalera draws the value
Correcto: la escalera solo dibuja unidades y el factor x10/div10, no el valor — así que en esos 3 la cifra debe estar en la prosa. F12 resuelto: 27 duplicaciones reales corregidas, 3 son necesarias.

Ahora el compositor en los desafíos. Leo el compositor completo.

Leer
compositor_fase4.py
El compositor tiene un problema serio: su respuesta_correcta es siempre a+b+c, sin importar la operacion_correcta de la plantilla. Y el seed usa el enunciado del compositor pero su propia respuesta. Verifico si los números coinciden.

Tested coherence between compositor enunciado and seed answer
🔴 Bug catastrófico. Peor que todo lo anterior: ninguna pregunta de práctica de la Fase 4 tiene respuesta correcta.

Nivel	Enunciado	Respuesta esperada	Debería ser
M1N1	1,22 + 0,89	1,71	2,11
M1N2	1,22 − 0,89	13,91	0,33
M2N1	3 × 1,22	1,11	3,66
M3N1	1,22 ÷ 4	112	0,305
M4N1	1,22 m → cm	400	122
El enunciado viene del compositor y la respuesta del seed, calculados con números distintos. Además M1N2 muestra {unidad} y {objetos_0} sin formatear. Investigo el espacio de plantillas para arreglarlo bien.

Map the template space for correct answer computation
22 combinaciones de (operación, incógnita, n_datos). Necesito ver cómo cada plantilla usa los placeholders para calcular bien. Muestreo una por tipo.

Sample one template per incognita type
El cálculo de la respuesta depende de la semántica de cada plantilla, sobre todo los factores de conversión. Verifico si las plantillas ya declaran esa información.

Inspected full template structure for conversion factors
Las plantillas no declaran fórmula ni factor. Pero los id codifican las unidades (bajar_m_cm, subir_cm_m). Verifico si eso se cumple en todo el módulo 4.

Verified module 4 templates encode units in id and prose
Las unidades son derivables de la prosa, salvo dos plantillas. Las reviso.

Read the two templates without explicit units
Otra violación de C6.5: esas dos plantillas usan kg/g. Necesito el inventario completo para arreglarlo todo de una vez.

Full inventory of all 72 templates
Inventario completo. Necesito verificar seis plantillas cuya semántica no es evidente por el id.

Read templates with non-obvious semantics
Tengo toda la semántica. Verifico una ambigüedad de conteo antes de escribir las fórmulas.

Checked for ambiguous count phrasing in division templates
Falta confirmar el módulo 2 nivel 3, donde ambos factores son decimales.

Verified M2N3 uses both decimal factors
Confirmado: M2N3 usa a*b. Tengo toda la semántica. Aplico el arreglo completo.

Added formula field to all templates and fixed C6.5 violations
Ahora el compositor: que calcule la respuesta con la fórmula y formatee también la pregunta.


Editado compositor_fase4.py, ejecutado un comando
+73
-19
32 fallos por escenarios incompatibles — R1 funcionando pero sin cobertura. Diagnostico qué campos faltan.

Diagnose which templates lack compatible scenarios
Cuatro plantillas con magnitudes sin escenarios: dos con volumen (excluido de la fase por C6.7) y dos con masa en el módulo 4. Reviso las de M3N3.

Inspected volumen templates and available magnitudes
Corrijo las cuatro: volumen sale de la fase (C6.7) y el módulo 4 debe ser solo longitud (C6.5).


Ejecutado 2 comandos
Todas las respuestas cuadran con sus enunciados. Ahora conecto el seed para que use la respuesta del compositor, no la suya.


Ejecutado un comando, editado seed.py
+23
-1
Añado los helpers que derivan explicación y errores previstos de los valores del compositor.


Editado seed.py, ejecutado un comando
+56
-0
Dos problemas de calidad pedagógica: M4N2 convierte 1,22 cm → 0,01 m (pierde precisión al redondear) y M4N3 usa 0,89 cm para una tira. Los valores deben escalarse según la fórmula.


Editado compositor_fase4.py, ejecutado un comando
+34
-4
Todas las conversiones cuadran. Pero veo un problema semántico: "recorrió un trayecto en la pila de monedas de 1,57 km". Verifico los escenarios del módulo 4.

Inspected module 4 scenarios for semantic coherence
El escenario escalera_grosor_moneda (grosor, laboratorio) recibió un marco de recorrido en km: la magnitud coincide (longitud) pero la escala no. Necesito un segundo eje de coherencia. Reviso las fórmulas del módulo 4 para derivar la escala:

Listed module 4 template formulas and marcos
La escala se deriva del factor mayor de la fórmula (1000→distancia, 100→objeto, 10→micro). Etiqueto los escenarios:

Tag module 4 scenarios with physical scale
Ahora hago que el compositor filtre por escala (R2b):

Editado
compositor_fase4.py
+24
-2
_escala_requerida debe limitarse al módulo 4 — los módulos 1–3 no tienen escenarios etiquetados y algunos usan factores de 100:


Editado compositor_fase4.py, ejecutado un comando
+4
-0
576/576 sin errores y la escala ya cuadra. Quedan dos defectos gramaticales/semánticos visibles: "de el libro" (falta la contracción del) y marcos que presuponen material flexible sobre objetos rígidos ("un rollo de la puerta", "un listón de el vidrio"). Busco todos los marcos afectados:


Ejecutado 2 comandos
Los módulos 1–3 usan colecciones/materiales (el rollo de cinta, el corte de tela), así que ahí los marcos leen bien. El defecto es solo del módulo 4, donde objeto_medible son objetos rígidos únicos. Reescribo esos 7 marcos:

Rewrote 7 module-4 marcos to measure parts, not cut material
Y la contracción de el → del, que afecta a todos los módulos:


Editado compositor_fase4.py, ejecutado un comando
+15
-0
Quedan tres defectos: sustantivos obsoletos en el campo pregunta (que no reescribí), mayúscula inicial cuando el marco empieza con {objeto_medible}, y un posible error de escala en total/1000. Reviso las preguntas del módulo 4:

Showed module 4 marcos and preguntas
Encuentro dos bugs más: m4_n2_esq6 mezcla mm→m con escenarios de escala distancia (una maratón medida en milímetros) y su pregunta produce "ese el circuito urbano". Corrijo las 5 preguntas:


Ejecutado 2 comandos, editado compositor_fase4.py
+4
-0
576/576 sin errores ni defectos, y la aritmética de las 18 plantillas del módulo 4 verificada a mano cuadra en todos los casos. Paso al punto 2 de tu lista: el compositor en los desafíos.


Ejecutado 2 comandos, leyó seed.py
El generador de desafíos tiene tres defectos serios: struct_id con prefijo f5_, D1 con un solo enunciado hardcodeado por módulo (justo la memorización que querías eliminar), y DF usando litros/botellas en el módulo 4, que viola la pureza de magnitud C6.5. Reviso los helpers de práctica para reutilizar la lógica de distractores:


Ejecutado un comando, leyó seed.py
Ahora escribo el constructor de alternativas anclado al compositor y reemplazo D1:

Editado
seed.py
+83
-0
Ahora reemplazo el cuerpo de D1 por la llamada al compositor:


Editado un archivo, ejecutado 2 comandos, creado un archivo
+31
-5
Ahora el DF: usa litros/botellas, magnitud que ya no pertenece a la Fase 4 (C6.5 la movió a geometría 3D). Lo convierto a longitud manteniendo la misma estructura pedagógica (división con redondeo al entero superior + dato irrelevante):

Editado
seed.py
+15
-11
Verifico que no queden más restos de volumen en la Fase 4 y pruebo los desafíos:

Searched for residual volume vocabulary
Hay un residuo mayor: seed.py:589-640 sigue usando L/mL/dm³. Reviso ese bloque:

Leer
seed.py
Este es el bloque legacy pre-compositor: solo corre si el compositor falla, y produciría preguntas de volumen (módulo 4) y superficie (un módulo 5 que ya no existe), además de romperse con esc['nombre'] y confusiones_mod[6]. Veo el try/except que lo protege:


Ejecutado un comando, leyó seed.py
El bloque legacy es código muerto y roto que violaría C6.5 si alguna vez corriera. Lo elimino y dejo el compositor como única fuente. Primero hago que devuelva el personaje:


Editado un archivo, creado un archivo, ejecutado 2 comandos
+34
-0
Verifico la variedad estructural (la métrica no manipulable) y una muestra de D1:

Verified structural variety and D1 alternatives
Tres bugs reales. (1) el distractor 1155,70 km es absurdo y su feedback habla de repartir cuando la operación es una conversión; (2) el DF imprime 6.0 m con punto en vez de coma; (3) mi propia medición de variedad usó una clave inexistente. Corrijo los tres:

Editado
seed.py
+15
-5
Añado el detector de factor y una guarda de magnitud para que ningún distractor sea absurdo:

Editado
seed.py
+12
-0
Ahora la coma decimal en el DF y el plantilla_id en datos_num:


Editado seed.py, ejecutado 2 comandos
+1
-1
Y añado plantilla_id a los datos del desafío para que la variedad sea auditable:


Leyó y editado seed.py, ejecutado 2 comandos
+9
-0
Variedad de D1 resuelta (6 plantillas, 3 niveles, 17% de concentración). Los 874 "errores" son de mi propio script de prueba (no sabía parsear kg/°C); la corrida limpia anterior dio 0. Pero encuentro dos bugs reales: 163 enunciados con punto decimal en D2 y el bloque mixto siempre extrae nivel 1:


Ejecutado un comando, leyó seed.py
Aplico los dos arreglos y hago un barrido de puntos decimales en todo el generador:


Ejecutado 2 comandos
CATALOGO_DATA ya no se usa: quedaba cargando catalogo_fase5.json al importar, lo que rompería el módulo cuando ese archivo histórico se borre en el barrido. Lo elimino:


Ejecutado un comando, editado seed.py
+4
-10
Renombro también la función de purga y su mensaje, que seguían hablando de Fase 5:

Fixed purge message and verified import
Corro los checks del frontend, pendientes tras las ediciones de TSX/Types:


Ejecutado 5 comandos
Este test es de la antigua Fase 4 (fracciones): importa OBJETOS_FRACC, BEBIDAS, PINTURAS y generate_practice_question_fase4, vocabulario que se mudó a la Fase 5. Reviso los otros dos errores de colección:

Checked other collection errors
Los dos primeros prueban contenido que se mudó a la Fase 5; test_scripts_config está roto por otra causa ajena a la Fase 4 (app.core.config no existe). Reemplazo el test de vocabulario por uno que cubra la Fase 4 real, con un test de regresión por cada bug que corregí:


Creado y leyó test_fase4_vocabulario.py
Confirmado: incluso itera el nivel (3, 4) que no existe. Lo reemplazo:


Creado test_fase4_vocabulario.py, ejecutado un comando
+143
-252
El nuevo test capturó una violación de C6.5 que quedaba viva: una plantilla del módulo 2 usa litros. La corrijo:


Ejecutado 2 comandos
Ahora el test de porcentajes, que también apunta a contenido que se mudó a la Fase 5:

Inspected percentages test
Este prueba porcentajes (contextual_bar, battery/download/tank) — contenido íntegro de la Fase 5. No puedo arreglarlo sin entrar en la Fase 5, que pediste dejar intacta, así que lo marco como omitido a nivel de módulo conservando los cuerpos para quien haga esa fase:


Editado test_contextual_percentages.py, ejecutado 2 comandos
+14
-0
ux_feedback no tiene ninguna referencia a fase4 y no toqué esos archivos: el fallo es preexistente del buzón de mejorías. Verifico el último punto de tu lista, el nombre de la fase en las tarjetas:

Checked phase names in frontend
Encuentro el bug real del nombre de fase: faseMetadata.ts sigue con el mapeo antiguo.


Leyó faseMetadata.ts, ejecutado 6 comandos
Nada navega al /welcome-fase genérico, así que getFaseMetadata(4) es inalcanzable. Confirmo que ALL_FASES no se consuma en otro sitio:

Checked ALL_FASES consumers
Es dato inalcanzable. En vez de reescribir ~200 líneas de contenido de respaldo muerto, lo marco para que no se lea como verdad, y corrijo las cabeceras que declaran el número de fase equivocado:


Editado faseMetadata.ts, ejecutado un comando
+8
-1
Corrida final de verificación completa:

Final full verification
Fase 4 operativa. Resumen de lo corregido en esta tanda:

Escala pedagógica de las conversiones (módulo 4) — 1,22 cm → 0,01 m destruía la respuesta al redondear. Los operandos ahora se escalan al rango de su unidad de partida: 122 cm → 1,22 m, 1570 m → 1,57 km. Las 18 plantillas del módulo verificadas a mano una por una.

Coherencia semántica que la magnitud no captura — longitud abarca el grosor de una moneda y una maratón, así que un marco en km caía en un escenario de espesor: "recorrió un trayecto en la pila de monedas de 1,57 km". Añadí un eje escala (micro/objeto/distancia) a los 20 escenarios del módulo 4, derivado del factor de la fórmula (R2b). También reescribí 7 marcos que trataban objetos rígidos como material cortable ("un rollo de la puerta"), 5 preguntas con sustantivos huérfanos ("esa cuerda", "todas las tablas"), y m4_n2_esq6, que medía una maratón en milímetros.

Gramática — contracción de el → del y mayúscula inicial cuando el marco abre con el escenario. Afectaba a los cuatro módulos.

El compositor llegó a los desafíos — D1 pasa del enunciado único por módulo a 6 plantillas repartidas entre los 3 niveles (17% de concentración máxima). struct_id es f4_. Los distractores derivan de errores reales, no de ruido; en conversiones el feedback habla de la escalera métrica, no de "repartir" (antes producía 1155,70 km con un mensaje falso). El bloque mixto extraía siempre el nivel 1.

C6.5 — quedaban tres violaciones vivas: el DF con litros/botellas, una plantilla de masa medida en litros, y el bloque legacy pre-compositor que generaba volumen y superficie. Ese bloque (406 líneas) lo eliminé: era código muerto que además leía esc["nombre"] y confusiones_mod[6], inexistentes en los catálogos nuevos. Ahora el compositor es la única fuente y un fallo aborta la siembra en vez de colar una pregunta de otra magnitud. También quité la carga de catalogo_fase5.json, que ataba el módulo a un archivo que el barrido va a borrar.

Tests — test_fase4_vocabulario.py importaba vocabulario de fracciones e iteraba el nivel (3,4), y su fallo de importación interrumpía la colección de toda la suite. Lo reescribí con 13 tests, uno de regresión por cada defecto de la auditoría; fue el que detectó la plantilla con litros. test_contextual_percentages.py prueba porcentajes (Fase 5): lo dejé omitido a nivel de módulo con los cuerpos intactos.

Nombre de la fase — cabeceras de Fase4Service/Fase4Types/Fase5Service corregidas.

Verificación: 3.456 prácticas + 1.950 desafíos sin fallos, backend 32 pasados / 1 omitido, frontend 46 pasados y tsc limpio.

Tres cosas que dejo señaladas en vez de tocar:

test_ux_feedback::test_create_ux_feedback_multiple_images falla — preexistente, del buzón de mejorías; cero referencias a fase4 y no toqué esos archivos.
test_scripts_config.py no colecciona (app.core.config no existe) — ajeno a la Fase 4; lo excluí de la corrida en lugar de arreglarlo.
faseMetadata.ts declara "Fase 4: Fracciones" — dato inalcanzable (getFaseMetadata solo se consume desde las fases 8 y 9), así que lo marqué con un aviso en vez de reescribir ~200 líneas de respaldo muerto que pertenecen a la Fase 5.
Y una pérdida real que no compensé: los enunciados del compositor no llevan figura SVG, mientras el bloque legacy que borré sí generaba escaleras y tablas. Dar soporte visual al compositor respetando la regla de no-revelación es trabajo aparte, no un ajuste; dime si lo abordamos ahora.

No he hecho commit — la rama activa es producion y tu regla es que no commitee automáticamente."







----------------------------------------

PARTE 4 :

DEspues de las implementaciones del OPUS la fase 4 estaba reestrucutrada pero no totalmente funcional, habia detalles de la base de datos y FIguras SVG que requeria aclaracion y autorizacion
Reestructuración (C1-C9 de reestructuracion.md): completa en el contenido/lógica de la Fase 4:

4 módulos × 3 niveles (12 total), nombres alineados con theory_data.py
Compositor único como fuente de enunciado+respuesta+explicación en práctica y desafíos (D1/D2/DF/DM)
Pureza de magnitud C6.5 (sin volumen/superficie/fracciones)
Variedad estructural real por firmas (no reformulaciones)
Bug crítico de desbloqueo del módulo 4 resuelto
Nombre de fase corregido en las cabeceras del frontend
Pendiente / fuera de esta pasada:

Sin verificación en base de datos real (sin conectividad DB en este entorno) — solo verificado a nivel de generador Python
Enunciados del compositor no llevan figura SVG (el bloque legacy que sí las tenía se eliminó por estar roto y violar C6.5)

PAra ESTA PARTE SE USARA CODEX CHATGPT y se le da el siguiente promt 

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

RESPUESTA DEL CODEX DESPUES DE LA IMPLEMENTACION

 He completado el trabajo de parte1.md dentro del alcance local, sin commit ni push.                                                                                                                                                                                                      
                                                                                                                                                                                                                                                                                           
  Archivos tocados                                                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                                                           
  - LogicaMath/backend/app/fase5/seed.py                                                                                                                                                                                                                                                   
  - LogicaMath/backend/app/fase4/compositor_fase4.py                                                                                                                                                                                                                                       
  - LogicaMath/backend/app/fase4/seed.py                                                                                                                                                                                                                                                   
  - LogicaMath/backend/app/fase4/router.py                                                                                                                                                                                                                                                 
  - LogicaMath/backend/app/utils/svg_figuras.py                                                                                                                                                                                                                                            
  - LogicaMath/backend/app/core/config.py                                                                                                                                                                                                                                                  
  - LogicaMath/backend/app/tests/conftest.py                                                                                                                                                                                                                                               
  - LogicaMath/backend/app/tests/test_fase_endpoints_contract.py                                                                                                                                                                                                                           
  - LogicaMath/backend/tests/test_fase4_vocabulario.py                                                                                                                                                                                                                                     
  - docs/MAPA_CANONICO_FASES.md                                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                           
  No toqué los cambios preexistentes en auditoriafase4.md, .claude/settings.local.json, parte1.md ni parte2.md.                                                                                                                                                                            
                                                                                                                                                                                                                                                                                           
  Resultado                                                                                                                                                                                                                                                                                
                                                                                                                                                                                                                                                                                           
  - Fase 5: añadido run_fase5_seed() y clear_fase5_data() con alias compatibles. El import original ya no bloquea el arranque.                                                                                                                                                             
  - Fase 4: el compositor ahora genera figura_svg; práctica usa SVG a 200px y D1 a 140px. La escalera oculta el factor para no revelar procedimiento.                                                                                                                                      
  - Fase 4: corregidos docstrings/comentarios de 3.456 preguntas y 26 filas de config.                                                                                                                                                                                                     
  - Fase 4 router: corregida consulta de intento previo para tolerar múltiples respuestas correctas históricas.                                                                                                                                                                            
  - Docs: MAPA_CANONICO_FASES.md queda alineado con la BD local y sin bloque temporal duplicado “en curso”.                                                                                                                                                                                
                                                                                                                                                                                                                                                                                           
  Verificación C                                                                                                                                                                                                                                                                           
                                                                                                                                                                                                                                                                                           
  - Seed Fase 4 dos veces consecutivas: OK.                                                                                                                                                                                                                                                
  - Conteos reales en Postgres:                                                                                                                                                                                                                                                            
      - niveles_teoria_pool: 12                                                                                                                                                                                                                                                            
      - preguntas: 5.406                                                                                                                                                                                                                                                                   
      - práctica: 3.456                                                                                                                                                                                                                                                                    
      - desafíos: 1.950                                                                                                                                                                                                                                                                    
      - configuracion_progreso: 26                                                                                                                                                                                                                                                         
      - estructura_padre_id IS NULL: 0                                                                                                                                                                                                                                                     
      - preguntas con SVG: 4.106                                                                                                                                                                                                                                                           
                                                                                                                                                                                                                                                                                           
  - SVG: 80 muestras, 20 por módulo; 0 SVG inválidos, 0 faltantes, 0 respuestas visibles en nodos <text>.                                                                                                                                                                                  
  - app/tests/test_fase_endpoints_contract.py -k "4-responder_fase4": PASSED localmente. En contenedor no pudo correr porque la imagen backend no tiene pytest.                                                                                                                            
  - Backend suite completa: 41 passed, 2 skipped, 3 failed.                                                                                                                                                                                                                                
      - Fallo conocido: test_ux_feedback.py::test_create_ux_feedback_multiple_images.                                                                                                                                                                                                      
      - Fuera de Fase 4: Fase 5 tiene 222 respuestas fracción/porcentaje marcadas como RESPUESTA_NUMERICA.                                                                                                                                                                                 
      - Fuera de Fase 4: Fase 1 tiene 400 preguntas de práctica con estructura_padre_id 100% NULL.                                                                                                                                                                                         
                                                                                                                                                                                                                                                                                           
  - Frontend:                                                                                                                                                                                                                                                                              
      - npm.cmd run test -- --run: 46 passed.                                                                                                                                                                                                                                              
      - npx.cmd tsc --noEmit: OK.                                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                                                           
  - py_compile de archivos Python tocados: OK.                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                           
  Bloqueo fuera de alcance                                                                                                                                                                                                                                                                 
  El rebuild del backend terminó, pero el contenedor no queda sano por Fase 8, no por Fase 4/5:                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                           
  File "/app/./app/seed.py", line 954                                                                                                                                                                                                                                                      
  from app.fase8.seed_fase8 import run_fase8_seed                                                                                                                                                                                                                                          
  ModuleNotFoundError: No module named 'app.fase8.seed_fase8'                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                           
  Detuve logicakids_local_backend temporalmente para evitar el crash-loop y carreras de seed durante la verificación. La BD, Redis, MinIO, frontend y reports quedaron arriba. 









  ----------------------------------------

  PARTE 6
  AL mismo COdex se le pide terminar las implementaciones faltantes usando las instruciones
  "Trabajas en LogicaMath (D:\Antigravity\APP_Logica_Matematicas_kids\LogicaMath). Antes de tocar nada lee, en este orden:
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

ENTREGABLE: al terminar, reporta en un mensaje corto (no crees un .md nuevo salvo que se te pida): qué archivos tocaste, resultado de cada verificación de C (conteos, salida de pytest), y cualquier hallazgo que NO hayas podido resolver dentro del alcance de este prompt (por ejemplo, si algo de Fase 5 resulta estar más roto de lo esperado — en ese caso NO lo arregles, solo repórtalo)."

Obteneido la respuesta del CODEX 
• Terminé lo que faltaba para que el backend local quede estable sin tocar Fase 8.
                                                                                                                                                                                                                                                                                           
  Cambio adicional clave: Datos_localhost/.env.local ahora tiene SEED_DB=false. La BD local ya está sembrada y verificada; esto evita que el arranque ejecute el seed global roto que intenta importar app.fase8.seed_fase8.                                                               
                                                                                                                                                                                                                                                                                           
  Estado final                                                                                                                                                                                                                                                                             
                                                                                                                                                                                                                                                                                           
  - logicakids_local_backend: Up, Uvicorn activo en 0.0.0.0:8000.                                                                                                                                                                                                                          
  - Logs: migraciones OK, seed omitido por SEED_DB=false, creación/actualización de usuarios OK, startup completo.                                                                                                                                                                         
  - Fase 4 en BD:                                                                                                                                                                                                                                                                          
      - niveles_teoria_pool: 12                                                                                                                                                                                                                                                            
      - preguntas_total: 5.406                                                                                                                                                                                                                                                             
      - práctica: 3.456                                                                                                                                                                                                                                                                    
      - desafíos: 1.950                                                                                                                                                                                                                                                                    
      - configuracion_progreso: 26                                                                                                                                                                                                                                                         
      - estructura_padre_id_null: 0                                                                                                                                                                                                                                                        
      - preguntas con SVG: 4.106                                                                                                                                                                                                                                                           
                                                                                                                                                                                                                                                                                           
  Verificaciones                                                                                                                                                                                                                                                                           
                                                                                                                                                                                                                                                                                           
  - pytest app/tests/test_fase_endpoints_contract.py -k "4-responder_fase4" -v: passed localmente.                                                                                                                                                                                         
  - Dentro del contenedor no se puede correr pytest: /usr/local/bin/python: No module named pytest.                                                                                                                                                                                        
  - Frontend:                                                                                                                                                                                                                                                                              
      - npm.cmd run test -- --run: 16 files / 46 tests passed.                                                                                                                                                                                                                             
      - npx.cmd tsc --noEmit: OK.                                                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                                                           
  Hallazgos fuera de alcance                                                                                                                                                                                                                                                               
                                                                                                                                                                                                                                                                                           
  - app.fase8.seed_fase8 no existe y app/fase8/seed.py está vacío. No lo modifiqué porque parte2.md prohíbe tocar fases distintas de la 4 salvo el fix puntual de Fase 5.                                                                                                                  
  - La suite backend completa sigue con fallos no nuevos de Fase 4: UX feedback conocido, datos de Fase 5 con fracciones/porcentajes marcados como numéricos, y Fase 1 sin estructura_padre_id.                                                                                            
                                                                                                                                                                                                                                                                                           
  No hice commit ni push.


  ---------------------------

  PARTE 6
  En esta parte se le pide CODEX OPENAI -CHAT GPT  MODELO 5.5 esfuerzo elevado