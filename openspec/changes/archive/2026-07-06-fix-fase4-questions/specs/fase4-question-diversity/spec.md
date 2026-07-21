## ADDED Requirements

### Requirement: Diversidad de contextos narrativos
El generador de preguntas de Fase 4 SHALL utilizar diccionarios de contexto expandidos con al menos 25 nombres, 15 objetos fraccionables, 10 colecciones, 10 bebidas, 10 pinturas y 10 colores para reducir la repetición percibida en los enunciados.

#### Scenario: Generación con vocabulario diverso
- **WHEN** el sistema genera preguntas de práctica libre para cualquier módulo de Fase 4
- **THEN** los enunciados utilizan nombres, objetos y contextos seleccionados aleatoriamente de los diccionarios expandidos
- **AND** la probabilidad de que dos preguntas consecutivas del mismo nivel usen el mismo nombre es menor al 15%

### Requirement: Variantes numéricamente distintas
Cada familia de preguntas SHALL producir 4 variantes con valores numéricos matemáticamente distintos. La variante original (var=0) y las variantes espejo (var=1,2,3) SHALL diferir en al menos uno de: denominador, numerador, total, o tipo de operación solicitada.

#### Scenario: Variante espejo con valores diferentes
- **WHEN** el generador crea la variante espejo (var > 0) de una familia de práctica
- **THEN** la semilla RNG produce valores numéricos diferentes a la variante original
- **AND** el enunciado no contiene el prefijo literal `[ESPEJO]`

#### Scenario: Variantes de la misma familia
- **WHEN** se comparan las 4 variantes de una misma familia
- **THEN** al menos 3 de las 4 variantes tienen respuestas correctas distintas

### Requirement: Rangos numéricos apropiados y ampliados
El generador SHALL utilizar rangos numéricos ampliados que mantengan la divisibilidad exacta y la dificultad apropiada para niños de 8-12 años.

#### Scenario: Denominadores ampliados en módulo de fracciones
- **WHEN** el generador selecciona denominadores para preguntas de fracciones (Módulos 1 y 2)
- **THEN** los denominadores se seleccionan de un conjunto de al menos 8 opciones que incluya `[2, 3, 4, 5, 6, 8, 10, 12]`

#### Scenario: Totales con divisibilidad garantizada
- **WHEN** el generador calcula un total para una pregunta tipo "m/n de X"
- **THEN** el total es siempre divisible exactamente por el denominador
- **AND** el resultado final es un número entero positivo

### Requirement: Enunciados autoexplicativos para preguntas interactivas
Las preguntas que incluyen componentes visuales interactivos SHALL contener un enunciado de texto completo que permita comprender y resolver el ejercicio sin depender del renderizado del componente visual.

#### Scenario: Pregunta interactiva con pizza/probeta
- **WHEN** una pregunta de práctica requiere interacción con componente visual (pizza, beaker, pie)
- **THEN** el campo `enunciado` incluye una descripción textual completa del problema
- **AND** el alumno puede deducir la respuesta correcta leyendo únicamente el enunciado

#### Scenario: Pregunta interactiva con gráfico circular
- **WHEN** una pregunta de Módulo 3 requiere interpretar un gráfico circular
- **THEN** el enunciado incluye todos los porcentajes y categorías necesarios en formato textual

### Requirement: Diversificación de desafíos del Módulo 3
Los desafíos del Módulo 3 SHALL incluir preguntas de las 4 categorías temáticas del módulo (porcentajes intuitivos, gráficos circulares, gráficos de barras, media aritmética) en lugar de alternar rígidamente entre solo dos tipos.

#### Scenario: Distribución temática en desafío de Módulo 3
- **WHEN** el generador crea las 30 preguntas de un desafío del Módulo 3
- **THEN** al menos 5 preguntas corresponden a cada una de las 4 categorías temáticas
