# secure-html-rendering Specification

## Requirements

### Requirement: Sanitizacion Centralizada de HTML Dinamico
El frontend SHALL sanitizar todo HTML dinamico antes de renderizarlo con `dangerouslySetInnerHTML`, usando una allowlist centralizada de etiquetas, atributos y protocolos permitidos.

#### Scenario: Contenido pedagogico con script embebido
- **WHEN** un texto de teoria, pregunta, alternativa o feedback contiene `<script>`, manejadores inline como `onerror`, o URLs `javascript:`
- **THEN** el frontend SHALL remover o neutralizar ese contenido antes de insertarlo en el DOM.

#### Scenario: Markdown permitido con imagen o enlace seguro
- **WHEN** un contenido pedagogico incluye markdown de imagen o enlace con URL `https://` o ruta relativa permitida
- **THEN** el frontend SHALL renderizar el HTML resultante conservando solo atributos seguros.
