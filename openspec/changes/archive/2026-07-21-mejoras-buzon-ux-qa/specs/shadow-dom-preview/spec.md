## ADDED Requirements

### Requirement: Isolated DOM Preview
El sistema MUST utilizar Shadow DOM para previsualizar el fragmento de código HTML (`element_html`) dentro del panel administrador `UXFeedbackTab.tsx`, garantizando que no haya fugas de CSS globales ni colisión de clases.

#### Scenario: Visualizing a component with isolated styles
- **WHEN** el administrador expande el detalle de un reporte de UX y visualiza el campo "Elemento Seleccionado (Visual)"
- **THEN** el HTML renderizado se mantiene contenido en un Shadow Root, sin afectar el layout general del panel de control
