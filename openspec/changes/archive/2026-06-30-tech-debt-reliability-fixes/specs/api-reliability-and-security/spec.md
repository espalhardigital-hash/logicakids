## MODIFIED Requirements

### Requirement: Tolerancia de Fallos en Auditoría de Login
El endpoint de autenticación `/auth/login` del backend SHALL permitir el acceso a usuarios con credenciales válidas y retornar el token de seguridad incluso si la actualización de auditoría del campo `last_login` en la base de datos falla. Todo fallo asíncrono durante un rollback MUST ser registrado explícitamente en el log del sistema para no encubrir problemas de red o conexión.

#### Scenario: Fallo de conexión o bloqueo al actualizar el timestamp de login
- **WHEN** el usuario ingresa credenciales correctas pero la base de datos falla al realizar el commit de `last_login`
- **THEN** el sistema SHALL capturar el error, intentar realizar un rollback de la transacción fallida (registrando el error crítico si también falla), y retornar el Token de acceso de forma exitosa.

### Requirement: Carga Centralizada de Secretos
El backend SHALL leer los secretos de autenticación y claves de API de servicios externos de forma centralizada utilizando la clase `Settings`. Los scripts y servicios SHALL NOT invocar directamente al sistema operativo (ej. `os.environ.get`) para extraer contraseñas, tokens o apikeys.

#### Scenario: Inicialización de la configuración del sistema
- **WHEN** el módulo de autenticación, scripts de auditoría o análisis IA requieren secretos del entorno
- **THEN** el sistema SHALL obtenerlos exclusivamente del singleton `settings` centralizado.

## ADDED Requirements

### Requirement: Cancelación de Temporizadores WebSocket
El gestor de conexión WebSocket de la aplicación frontend SHALL garantizar la limpieza explícita de todo temporizador de reconexión anterior antes de agendar un nuevo reintento.

#### Scenario: Múltiples eventos de fallo y desconexión
- **WHEN** el socket sufre un `onclose` y `onerror` en rápida sucesión (múltiples llamadas)
- **THEN** el hook de react SHALL ejecutar `clearTimeout` sobre el identificador en curso antes de establecer el temporizador de 10 segundos, impidiendo fugas de memoria o ráfagas asíncronas de reconexión.
