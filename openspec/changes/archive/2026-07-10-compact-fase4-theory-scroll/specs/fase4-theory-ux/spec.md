## ADDED Requirements

### Requirement: Modal de teoría compacto sin scroll vertical
El modal de teoría de la Fase 4 SHALL compactar su contenido y dimensiones en pantallas estándar y grandes (viewport de hasta 2560x945) para evitar la aparición de scroll vertical y permitir una lectura ágil de los ejemplos ilustrados.

#### Scenario: Visualización del primer ejemplo del nivel 3
- **WHEN** el usuario ingresa a la teoría del Módulo 1, Nivel 3 de Fase 4
- **THEN** la tarjeta de teoría se ajusta compactando paddings, el tamaño de la imagen/SVG se limita a un máximo de 75px (o altura compacta), y se muestra el contenido completo de enunciado, imagen y pasos del ejemplo en pantalla sin requerir scroll vertical.

### Requirement: Parser robusto para enunciados con múltiples SVGs
La función de extracción de SVG (`extraerSvgYTexto`) MUST procesar adecuadamente enunciados que contengan más de un SVG (por ejemplo, en el caso de las equivalencias de Módulo 1 Nivel 2), extrayendo todos los SVGs o envolviéndolos correctamente para evitar romper la estructura del HTML y de los estilos en la UI.

#### Scenario: Enunciado con múltiples SVGs
- **WHEN** se analiza un ejemplo con múltiples elementos SVG y etiquetas contenedoras (como divs)
- **THEN** el parser extrae todos los elementos SVG de forma limpia, dejando el texto del enunciado libre de fragmentos de HTML rotos o etiquetas no cerradas.
