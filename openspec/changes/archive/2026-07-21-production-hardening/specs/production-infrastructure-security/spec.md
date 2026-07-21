## ADDED Requirements

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
