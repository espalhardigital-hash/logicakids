## MODIFIED Requirements

### Requirement: Renderizado condicional de visualizadores por tipo_visual
El componente `Fase4GameScreen.tsx` DEBE soportar el renderizado condicional del nuevo tipo visual `non_homogeneous_polygon` además de los tipos existentes (`pizza`, `thermometer`, `beaker`, `pie`, `percentage_thermometer`, `percentage_beaker`, `shapes`).

#### Scenario: Renderizado de pregunta con tipo_visual non_homogeneous_polygon
- **WHEN** se carga una pregunta cuyo `datos_numericos.tipo_visual` es `"non_homogeneous_polygon"`
- **THEN** el sistema DEBE renderizar el componente `Fase4NonHomogeneousPolygon` en el área visual izquierda, pasando los `sectors`, `viewBox` y `target_fraction_text` como props
- **AND** DEBE mostrar el enunciado en español debajo de la figura SVG
- **AND** DEBE mostrar un indicador de progreso que muestre la fracción seleccionada actualmente (suma de pesos de sectores coloreados) vs. la fracción objetivo

#### Scenario: Envío de respuesta para non_homogeneous_polygon
- **WHEN** el alumno presiona "CONFIRMAR" con sectores seleccionados
- **THEN** el frontend DEBE enviar `respuesta_dada` con los IDs de los sectores coloreados separados por coma (ej: `"1,3,5"`) al endpoint `/responder`

#### Scenario: Tipos visuales existentes no afectados
- **WHEN** se carga una pregunta con `tipo_visual` existente (ej: `"pizza"`, `"thermometer"`)
- **THEN** el renderizado DEBE funcionar exactamente igual que antes, sin cambios de comportamiento
