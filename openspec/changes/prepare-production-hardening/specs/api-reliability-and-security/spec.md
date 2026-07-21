## ADDED Requirements

### Requirement: Sanitizacion Centralizada de HTML Dinamico
El frontend SHALL sanitizar todo HTML dinamico antes de renderizarlo con `dangerouslySetInnerHTML`, usando una allowlist centralizada de etiquetas, atributos y protocolos permitidos.

#### Scenario: Contenido pedagogico con script embebido
- **WHEN** un texto de teoria, pregunta, alternativa o feedback contiene `<script>`, manejadores inline como `onerror`, o URLs `javascript:`
- **THEN** el frontend SHALL remover o neutralizar ese contenido antes de insertarlo en el DOM.

#### Scenario: Markdown permitido con imagen o enlace seguro
- **WHEN** un contenido pedagogico incluye markdown de imagen o enlace con URL `https://` o ruta relativa permitida
- **THEN** el frontend SHALL renderizar el HTML resultante conservando solo atributos seguros.

### Requirement: Sesiones Seguras para Produccion
El sistema SHALL usar cookies `HttpOnly` con `SameSite` y `Secure` en produccion para transportar la sesion autenticada, evitando depender de `localStorage` para tokens JWT en despliegues publicos.

#### Scenario: Login en entorno de produccion
- **WHEN** un usuario inicia sesion con credenciales validas en produccion
- **THEN** el backend SHALL emitir la sesion en una cookie `HttpOnly`, `Secure` y `SameSite=Lax` o mas estricta, y el frontend SHALL realizar solicitudes autenticadas con credenciales incluidas.

#### Scenario: Modo local legacy
- **WHEN** el entorno esta configurado explicitamente como local/dev
- **THEN** el sistema MAY permitir bearer token en memoria o almacenamiento local para compatibilidad de desarrollo.

### Requirement: Endpoint de Configuracion del Sistema Restringido
El backend SHALL deshabilitar o restringir `/admin/system-config` en produccion para impedir lectura o escritura de secretos y configuracion de infraestructura desde HTTP.

#### Scenario: Solicitud a system-config en produccion
- **WHEN** un administrador llama `/admin/system-config` en produccion
- **THEN** el backend SHALL rechazar la operacion sin devolver `DATABASE_URL` ni otros secretos.

#### Scenario: Solicitud a system-config en desarrollo local
- **WHEN** el entorno local habilita explicitamente `ENABLE_SYSTEM_CONFIG_ENDPOINT=true`
- **THEN** el backend MAY permitir la operacion para facilitar desarrollo, manteniendo auditoria y sin exponerla por defecto.

### Requirement: Alembic como Fuente Unica de Schema en Produccion
El backend SHALL usar Alembic como mecanismo de migracion de schema en produccion y SHALL NOT ejecutar `Base.metadata.create_all` de forma implicita durante el lifespan de la aplicacion.

#### Scenario: Arranque del backend en produccion
- **WHEN** la aplicacion inicia en produccion
- **THEN** el schema SHALL estar gestionado por migraciones Alembic y no por creacion automatica de tablas desde modelos ORM.

### Requirement: Logging SQL Seguro por Defecto
El backend SHALL configurar SQLAlchemy con `echo=False` por defecto, permitiendo logs SQL verbosos solo mediante una bandera explicita de desarrollo.

#### Scenario: Arranque en produccion
- **WHEN** el backend crea el engine de SQLAlchemy en produccion
- **THEN** las consultas SQL no SHALL imprimirse automaticamente en logs de aplicacion.

### Requirement: CORS Restrictivo en Produccion
El backend SHALL limitar CORS a origenes explicitos en produccion y SHALL rejectar configuraciones comodin cuando se usan credenciales.

#### Scenario: Dominio no autorizado llama la API
- **WHEN** un origen no incluido en `ALLOWED_ORIGINS` llama a la API de produccion
- **THEN** el backend SHALL negar la solicitud CORS.
