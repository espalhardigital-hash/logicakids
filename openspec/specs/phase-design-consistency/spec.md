# phase-design-consistency Specification

## Purpose
TBD - created by archiving change fase4-consistencia-diseno-fase2. Update Purpose after archive.
## Requirements
### Requirement: Consistencia de Apoyo Visual Contextual
El sistema SHALL mostrar únicamente recursos visuales o gráficos que correspondan estrictamente al contexto temático de la pregunta generada. En caso de que se usen colecciones discretas u objetos de contexto (como figuritas, cartas o tazos), no se MUST utilizar vasos graduados (beakers) genéricos con porcentajes o graduaciones que no se correspondan con dicho contexto. En su lugar, se SHALL utilizar representaciones que simulen la colección descrita (como diagramas de conjunto, barras o pizzas) o, en su defecto, omitir el apoyo gráfico si este no tiene relación directa y real con la pregunta.

#### Scenario: Visualización en pregunta de colecciones en Fase 4
- **WHEN** el alumno carga una pregunta sobre colecciones discretas (ej. figuritas, cartas, tazos) en la Fase 4 Módulo 2
- **THEN** la interfaz de usuario no SHALL mostrar la imagen de un vaso graduado (beaker) con líquido, y en su lugar SHALL omitir la imagen o mostrar un gráfico que sea coherente con la colección de contexto de la pregunta.

### Requirement: Estandarización de Alertas de Bucle Espejo
El componente de alerta visual del Bucle Espejo en la Fase 4 y en cualquier fase posterior del sistema SHALL utilizar exactamente el mismo texto de mensaje, estilos CSS, animaciones y comportamiento interactivo que el patrón estándar de Bucle Espejo definido y validado en la Fase 2.

#### Scenario: Activación de Bucle Espejo en Fase 4
- **WHEN** un alumno falla consecutiva o reiteradamente en la Fase 4 y se activa el Bucle Espejo
- **THEN** el sistema SHALL renderizar la alerta de Bucle Espejo con el mismo patrón textual y de diseño visual definido para la Fase 2.

