<!--
Tomo 5 — Criterios de Teoría, Ejemplos Guiados y Apoyo Visual
Estado: normativo. Validado en la Fase 4 (piloto), 2026-07-30.
-->

# Tomo 5: Criterios de Teoría, Ejemplos Guiados y Apoyo Visual — LogicaKids Pro

> **Estado:** normativo para todas las fases.
> **Origen:** reglas desarrolladas y corregidas durante la reestructuración de la Fase 4, validadas visualmente con el usuario.
>
> Complementa a: [Tomo 1 (Rector Pedagógico)](./1_Documento_Rector_Pedagogico.md) · [Tomo 3 (Frontend UX)](./3_Guia_Frontend_UX.md) · [Tomo 4 (TJS y Desafíos)](./4_Guia_TJS_Desafios.md).
> Método de aplicación: [`reestructuracionGeneralFases.md`](../reestructuracionGeneralFases.md).

---

## 1. Las dos reglas innegociables

Estas dos reglas **no se negocian por ninguna razón de contenido o layout**. Están por encima de cualquier decisión estética o pedagógica particular.

### T3 — Cero scroll vertical

Ninguna pantalla de teoría, ejemplo, explicación o pregunta puede exigir desplazamiento vertical al alumno, en ninguna fase, en ningún nivel.

Corolarios (todos aprendidos por error en la Fase 4):

1. **No** resolver el desborde con `overflow-y: auto`.
2. **No** ocultar contenido con `overflow: hidden`.
3. **No** eliminar contenido pedagógico para que quepa.
4. **Sí** dividir en pasos cuando el contenido excede el marco.

> Caso real: al corregir el diccionario del nivel, el primer intento **eliminó el diccionario** para ganar espacio. Es exactamente lo que no se debe hacer. La corrección válida fue separarlo en su propio bloque y fragmentarlo en tarjetas.

### T4 — Ventana de tamaño fijo

El marco que contiene teoría y ejemplos mantiene **las mismas dimensiones en todos los niveles y todas las fases**. Esto sostiene la consistencia de la experiencia: el alumno no debe reaprender el espacio en cada pantalla.

**Referencia calibrada:** 950 × 620 px, dimensionada para iPad 1024×768 en horizontal menos el cromo del navegador. Área útil de contenido: ~440 px.

---

## 2. Teoría por niveles

### 2.1. Principio

> **Dividir solo cuando la cantidad de información lo exige. Compactar cuando sí cabe.**

Fragmentar contenido que cabía en una sola tarjeta es tan defectuoso como cortar contenido que no cabía. Ambos extremos se cometieron en la Fase 4.

### 2.2. Reglas

1. La teoría se separa en **pasos de lectura**, no en fragmentos arbitrarios.
2. Cada flashcard contiene **una unidad de lectura completa**.
3. El **diccionario del nivel es un bloque propio**, nunca mezclado con la teoría si el conjunto no cabe.
4. Los términos del diccionario se reparten en varias tarjetas cuando son muchos, **sin eliminar ninguno**.
5. Validar visualmente el **primer nivel** antes de extender el patrón a los demás.

### 2.3. Ilustración inicial

El primer flashcard de teoría de cada nivel lleva una **ilustración contextual compacta**. Sin ella, la lectura arranca como una pared de texto abstracto, algo especialmente hostil para un alumno infantil.

Condiciones:

| Debe | No debe |
|---|---|
| Ser contextual al módulo y nivel | Usar emojis como recurso principal |
| Ser discreta y de dimensiones controladas | Depender de archivos externos (MinIO/PNG) |
| Aparecer **solo** en el primer paso | Empujar contenido fuera de la tarjeta |
| Apoyar la comprensión | Sustituir la explicación |

---

## 3. Ejemplos guiados

### 3.1. La pregunta que decide el formato

> **¿El alumno puede ver el problema, los datos y la solución como una sola unidad de aprendizaje?**

- **Sí** → una sola flashcard.
- **No** → varias flashcards, divididas por **bloques pedagógicos completos**, nunca por pasos atómicos.

### 3.2. Defectos corregidos en la Fase 4

| Defecto | Corrección |
|---|---|
| Ejemplos que mostraban enunciado y datos, **pero no la solución** | El ejemplo guiado debe llegar hasta la resolución |
| Una flashcard por cada paso, habiendo espacio de sobra | Compactar cuando cabe |
| Encabezados redundantes (`Ejemplos guiados`, `Parte 1 de varias`) | Eliminados: la etiqueta superior ya lo indica |
| Indicador interno de parte, sin información real | Eliminado |
| Tablas y figuras con bordes y colores que robaban espacio | Ver §4 |

### 3.3. Cierre del ejemplo

Al final se muestra una **marca discreta de problema resuelto**. Comunica cierre sin exceso visual.

### 3.4. TJS dentro de ejemplos guiados

Se mantiene **un solo TJS** en el bloque de ejemplos guiados, y debe estar **explicado**, no presentado de forma pasiva. Un TJS que el alumno solo observa sin entender el criterio de decisión no enseña nada. Ver Tomo 4.

---

## 4. Limpieza visual de figuras, tablas y recuadros

### 4.1. Principio

> **Una figura pedagógica debe competir lo menos posible con el contenido matemático.**

### 4.2. Prueba de justificación

Antes de añadir un borde, color o marco, debe responder **sí** a alguna de estas:

1. ¿Ayuda a entender?
2. ¿Organiza información?
3. ¿Guía la mirada?
4. ¿Evita confusión?

Si no cumple ninguna función clara, **se elimina**.

### 4.3. Reglas aplicadas

1. Sin bordes decorativos alrededor de figuras y tablas.
2. Color de texto interno unificado con el del enunciado, manteniendo contraste.
3. Sin colores llamativos (morado, rosa) compitiendo con el enunciado.
4. Un borde decorativo **puede leerse como elemento interactivo** — razón adicional para retirarlo.

---

## 5. Apoyo visual SVG en preguntas

### 5.1. Regla anti-revelación *(crítica)*

> **La figura presenta los datos del problema. Jamás ejecuta el procedimiento ni muestra el resultado.**

Prohibido explícitamente:

1. Flechas que resuelvan la conversión u operación.
2. El resultado dentro del SVG.
3. Cualquier marca que insinúe la respuesta correcta.

### 5.2. Reglas técnicas

| Regla | Detalle |
|---|---|
| SVG **inline** | Sin dependencia de MinIO ni de PNG externos |
| Altura controlada | ≤ 140 px en desafíos; dentro del presupuesto visual en teoría |
| Legibilidad | Una figura diminuta no apoya: o se ve bien, o no va |
| Sin texto cortado | Verificar que el SVG no recorte etiquetas |
| Consistencia por flujo | Mismo criterio en práctica, desafío, teoría y corrección bloqueada |

### 5.3. Figura recurrente de fase

Cuando una fase usa una figura característica (en la Fase 4, la escalera métrica), esa figura se trata como **componente pedagógico**, no como adorno:

1. Debe verse bien **en todos los contextos** donde aparece.
2. No debe aparecer diminuta.
3. No debe repetirse si en ese contexto no ayuda.
4. No debe rodearse de marcos decorativos.

> ⚠️ **Riesgo conocido:** el SVG del proyecto ya falló una vez — DOMPurify borraba atributos geométricos y las figuras salían vacías. Está corregido, pero **ampliar el uso amplía la superficie de ese riesgo**: incluir SVG explícitamente en las pruebas.

---

## 6. Coherencia lógica de los enunciados

Un alumno debe fallar por su razonamiento matemático, **nunca por un defecto del enunciado**. Esto es justicia pedagógica.

### 6.1. Barrido obligatorio antes de cerrar una fase

1. ¿Todos los datos pueden **coexistir** en la historia?
2. ¿La pregunta corresponde con la operación esperada?
3. ¿Hay distractores que **parecen datos útiles**?
4. ¿El resultado esperado es **posible** en el contexto?
5. ¿El alumno puede resolver sin explicación externa?

> Caso real: el alumno tenía un monto inicial, los gastos **superaban** ese monto, y aun así se preguntaba cuánto le sobró. Situación imposible.

### 6.2. Coherencia semántica y de unidades

> **No se pueden sumar peras con manzanas.**

Dos ejes, no uno:

1. **Magnitud** — una plantilla de dinero jamás recibe un escenario de longitud. Debe **fallar en la siembra**, no adaptarse.
2. **Escala física** — la magnitud sola es insuficiente. `longitud` abarca el grosor de una moneda y una maratón. Sin un eje de escala (`micro` / `objeto` / `distancia`) se generó: *"recorrió un trayecto en la pila de monedas de 1,57 km"*.

### 6.3. Escala pedagógica de los valores

Los operandos deben vivir en el rango realista de su unidad de partida. Convertir `1,22 cm → m` da `0,0122`, que al redondear se destruye en `0,01`. La forma correcta es `122 cm → 1,22 m`.

### 6.4. Presentación numérica

1. **Coma decimal** en todo enunciado, opción, explicación y tabla. Nunca punto.
2. Enteros sin decimales de relleno: `450 cm`, no `450,00 cm`.
3. Contracciones del español correctas: `del`, no `de el`.
4. Sin *placeholders* crudos: si aparece `{unidad}` en pantalla, hay un campo sin formatear.

---

## 7. Distractores en opción múltiple

Un distractor debe **encarnar un error que un alumno comete de verdad**, no ser ruido:

| Distractor | Error que representa |
|---|---|
| Operación invertida | Confundir el sentido del problema |
| Coma desplazada un lugar | Error estructural del dominio decimal |
| Un operando sin usar | Lectura incompleta del enunciado |

**Regla de plausibilidad:** un distractor 100 veces mayor o menor que la respuesta se descarta de un vistazo y **no mide nada**. Debe ser plausible para ser útil.

**Regla de feedback honesto:** el mensaje debe describir el error **realmente cometido**. En una conversión métrica, *"repartir en partes iguales es dividir"* es una explicación falsa; lo correcto es hablar de recorrer la escalera métrica al revés.

---

## 8. Ecosistema de flujos

Todo cambio de UX se rastrea **por flujo, no por componente**. El mismo contenido reaparece en:

1. Pantalla principal de práctica
2. Batería de práctica libre
3. Corrección obligatoria tras error
4. Desafíos de módulo (D1 / D2 / DF)
5. Desafío mixto (DM)
6. Finalización y graduación
7. Vistas admin / preview

> Si se corrige solo una vista, el alumno sigue viendo el defecto en otra. La misma pregunta no puede verse correcta en un lugar y rota en otro.

---

## 9. Identidad visible de la fase

Cuando una fase se renumera o intercambia, **no basta con cambiar backend y ruta**. Auditar la identidad completa:

- [ ] Encabezados y badges
- [ ] Pantalla de bienvenida
- [ ] Flujo de juego
- [ ] Mensajes de progreso y graduación
- [ ] Modal de teoría
- [ ] Mapas administrativos (`phaseMaps.ts`, `faseMetadata.ts`)
- [ ] Seeders y sus mensajes de consola
- [ ] Cabeceras de archivos (`Service.ts`, `Types.ts`)
- [ ] Scripts auxiliares y documentos

> La fuente de verdad del nombre es la tabla `fases` y el router de la fase — nunca un metadato duplicado en el frontend.

---

## 10. Checklist de cierre visual de una fase

Una fase **no se cierra porque "se ve mejor"**. Se cierra con evidencia:

- [ ] Cero scroll vertical verificado **visualmente**, no inferido del código
- [ ] Cero contenido cortado en todos los niveles
- [ ] Teoría legible con diccionario completo
- [ ] Ejemplos guiados con resolución visible
- [ ] Figuras legibles, sin revelar respuesta
- [ ] Sin bordes decorativos injustificados
- [ ] Enunciados sin contradicción lógica
- [ ] Coma decimal y contracciones correctas en todo el contenido
- [ ] Mismo criterio aplicado en los 7 flujos de §8
- [ ] Identidad visible coherente (§9)
- [ ] Suite frontend + `tsc --noEmit` en verde
- [ ] Conteos verificados contra la **base de datos real**

---

## 11. Cierre

> **Una buena implementación pedagógica no consiste en mostrar más información, sino en mostrar la información justa, completa y en el momento correcto.**
