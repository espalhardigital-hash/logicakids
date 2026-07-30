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