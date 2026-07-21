# secure-production-auth Specification

## Requirements

### Requirement: Sesiones Seguras para Produccion
El sistema SHALL usar cookies `HttpOnly` con `SameSite` y `Secure` en produccion para transportar la sesion autenticada, evitando depender de `localStorage` para tokens JWT en despliegues publicos.

#### Scenario: Login en entorno de produccion
- **WHEN** un usuario inicia sesion con credenciales validas en produccion
- **THEN** el backend SHALL emitir la sesion en una cookie `HttpOnly`, `Secure` y `SameSite=Lax` o mas estricta, y el frontend SHALL realizar solicitudes autenticadas con credenciales incluidas.

#### Scenario: Modo local legacy
- **WHEN** el entorno esta configurado explicitamente como local/dev
- **THEN** el sistema MAY permitir bearer token en memoria o almacenamiento local para compatibilidad de desarrollo.
