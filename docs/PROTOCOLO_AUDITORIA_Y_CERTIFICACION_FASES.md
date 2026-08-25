# Protocolo de Auditoría y Certificación de Fases

> **Estado:** normativo para auditorías, correcciones y publicaciones de contenido de LogicaKids.
> **Actualización:** 2026-08-25.
> **Propósito:** impedir que una fase se declare lista solo porque compila, tiene datos o posee una suite aislada en verde.

## 1. Prelación de evidencia

Este protocolo usa aprendizajes de auditorías históricas, pero ningún chat, memoria, plan antiguo o reporte de una IA constituye una instrucción vigente ni una certificación.

Ante un conflicto, prevalece este orden:

1. Solicitud actual del responsable del proyecto.
2. Documentos rectores vigentes y criterios pedagógicos/UX.
3. Comportamiento ejecutado en el entorno local: base de datos, API, pantalla y logs.
4. Pruebas automatizadas reproducibles.
5. Planes, memorias y conversaciones históricas, únicamente como contexto.

## 2. Definición de fase certificada

Una fase está certificada solo si un alumno puede completar, de inicio a fin, práctica, desafíos, teoría, correcciones y cierre sin errores de contenido, lógica, backend o UX. La evidencia debe cubrir este recorrido:

```text
generador → seed → base de datos → endpoint → interfaz → alumno
```

No es suficiente que exista un archivo, que un componente compile, ni que un seeder parezca correcto al leerlo.

## 3. Invariantes no negociables

### Pedagogía y progreso

- No existen preguntas espejo, rescates ni bypasses que acrediten progreso.
- Respuesta incorrecta = respuesta correcta + explicación paso a paso + bloqueo de lectura de 10 segundos.
- Solo un acierto real acredita dominio.
- Las variantes amplían variedad; no se sirven como reacción automática a un error.

### UX y visuales

- Cero scroll vertical en práctica, teoría, corrección, desafíos, finalización y graduación.
- El contenido extenso se divide en diapositivas; ocultar contenido con `overflow: hidden` no es paginación.
- Toda pregunta tiene `plantilla_id`, `requiere_figura` y `tipo_visual`.
- Cuando `requiere_figura=true`, el recurso debe llegar a la interfaz y mostrarse junto al enunciado.
- La figura presenta datos; nunca ejecuta el cálculo ni revela la respuesta.
- La interfaz siempre ofrece una forma real de responder: teclado, coma decimal, alternativas o interacción correspondiente.

### Integridad del banco

- Enunciado, respuesta, explicación y distractores salen de los mismos valores y fórmula.
- No hay enunciados/respuestas vacíos, placeholders, alternativas repetidas ni más de una alternativa correcta.
- Los distractores representan errores plausibles, no valores aleatorios evidentes.
- La variedad se mide por firma estructural: operación, incógnita, datos, representación y contexto; cambiar solo nombre o valor no crea un tipo nuevo.

## 4. Ciclo obligatorio de trabajo

### Paso A — Mapear antes de editar

Identificar la ruta que realmente usa el alumno, `fase_id`, módulos, niveles, seed activo, tablas afectadas, router, componentes y teoría. Buscar duplicados, rutas huérfanas, imports cruzados y fuentes de verdad paralelas.

**Salida:** mapa breve de flujo y alcance de datos que se pueden modificar.

### Paso B — Formular hipótesis y medir el estado real

Auditar la base local y la API real. Cuantificar, no describir vagamente: preguntas sin respuesta, figuras ausentes, familias nulas, alternativas inválidas, datos espejo, inconsistencias y duplicados.

**Salida:** inventario de defectos con conteo, ejemplo reproducible y causa probable.

### Paso C — Crear o ajustar el arnés de regresión

Antes de corregir, crear pruebas que fallen por el defecto detectado. Deben probar contratos de datos y casos límite, no repetir la misma lógica del generador.

**Salida:** pruebas ejecutables que diferencian el estado defectuoso del correcto.

### Paso D — Corregir la causa raíz

Cambiar el generador, seed, router, esquema o frontend que origina el defecto. Evitar parches que oculten la falla: fallbacks silenciosos, saltar preguntas, contar errores como aciertos o desactivar una ruta sin retirar su mecanismo.

**Salida:** modificación acotada y conectada al punto de entrada real.

### Paso E — Regenerar y comprobar la frontera entre capas

Re-sembrar únicamente la fase autorizada. Auditar de nuevo la BD, probar el endpoint y comprobar que el frontend consume las mismas claves generadas. Si hay recursos externos, verificar que la URL o SVG exista y sea visible.

**Salida:** mismos chequeos del Paso B sin hallazgos del defecto corregido.

### Paso F — Recorrido de alumno y cierre

Recorrer al menos una muestra representativa de práctica, cada desafío, teoría, error, corrección bloqueada y finalización. Revisar la figura en pantalla, no solo el HTML o el registro de BD.

**Salida:** evidencia de build, tests, auditoría, logs y recorrido visual.

## 5. Matriz mínima de certificación

| Área | Debe verificarse |
|---|---|
| Generador | Fórmula, valores, respuesta, explicación, distractores y variedad real |
| Seed | Punto de entrada activo, idempotencia, familias, alternativas y contrato visual |
| Base local | Conteos, vacíos, duplicados, claves, figuras requeridas y ausencia de espejo |
| API | Obtener pregunta, responder correcto/incorrecto, progreso, desafíos y errores controlados |
| Entrada | Alternativas, teclado, coma decimal y formatos de respuesta exigidos |
| Visual | Enunciado/figura coherentes, legibilidad, sin respuesta revelada, sin recorte |
| Teoría | Diapositivas completas, ejemplos y actividades contestables, sin scroll |
| Progreso | Acierto real, desbloqueo correcto, desafío y graduación |
| Operación | Tests, build, Docker, logs de arranque y documentación actualizada |

## 6. Anti-patrones que bloquean la certificación

1. Pieza creada pero no conectada al seed, router o pantalla.
2. Campo generado y descartado antes de llegar a la BD o interfaz.
3. Progreso calculado sobre familias o datos `NULL`.
4. Funcionalidad muerta: ruta, modal, endpoint o generador sin flujo activo.
5. Figura ausente, ilegible, de otro ejercicio o que muestra la respuesta.
6. Pregunta sin interfaz para ingresar el formato solicitado.
7. Enunciado imposible, magnitudes incoherentes o respuesta calculada con valores distintos.
8. Alternativas repetidas, dobles correctas o distractores pedagógicamente vacíos.
9. Copia/pega semántico entre fases: nombres, IDs, dominios, textos o CSS ajenos.
10. Prueba tautológica, que no instancia datos reales ni toca el flujo que pretende validar.
11. Reporte de éxito sin comando, salida y evidencia reproducible.

## 7. Evidencia de cierre obligatoria

Una entrega de fase debe registrar:

1. Alcance exacto y datos que se regeneraron.
2. Pruebas ejecutadas, comandos y resultado.
3. Resultado de auditoría de BD posterior a la siembra.
4. Resultado de build y estado de los contenedores locales.
5. Rutas/API comprobadas y errores esperados.
6. Muestra visual recorrida y limitaciones que no pudieron validarse.
7. Deuda restante explícita; ningún pendiente se presenta como resuelto.

## 8. Plantilla de acta de certificación

```markdown
# Certificación — Fase X

- Fecha:
- Alcance:
- Banco regenerado: sí/no; cantidad:
- Pruebas: comando + resultado
- Auditoría BD: vacíos / duplicados / figuras faltantes / espejo
- API: rutas y casos comprobados
- UX: práctica, desafíos, teoría, corrección, finalización y scroll
- Docker: build, servicios y logs
- Estado: certificada / certificada con deuda / no certificada
- Deudas o bloqueos:
```

## 9. Relación con los documentos existentes

- [`reestructuracionGeneralFases.md`](./reestructuracionGeneralFases.md) define el orden de diseño y sus gates.
- Los criterios de diseño de fase definen contenido, teoría y UX pedagógica.
- Este documento define cómo comprobar que esa intención llegó correctamente al alumno.
- Los documentos `ESTADO_IMPLEMENTACION_*` son actas de evidencia por fase, no sustituyen este protocolo.
