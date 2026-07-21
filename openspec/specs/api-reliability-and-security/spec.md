# api-reliability-and-security Specification

## Purpose
TBD - created by archiving change correccion-deuda-tecnica-seguridad-api. Update Purpose after archive.
## Requirements
### Requirement: Sincronización WebSocket Resiliente
El servidor backend SHALL asegurar que cualquier conexión de WebSocket establecida en el endpoint `/ws/admin-sync` que finalice o sea interrumpida por desconexiones TCP abruptas o errores inesperados, sea debidamente desconectada del gestor de conexiones (`manager.disconnect`).

#### Scenario: Desconexión TCP abrupta del socket
- **WHEN** un cliente WebSocket pierde conexión abruptamente sin enviar mensaje de cierre formal
- **THEN** el sistema SHALL capturar el error y ejecutar la limpieza en el bloque `finally`, removiendo la conexión muerta.

### Requirement: Conexión WebSocket Dinámica en Producción
El cliente frontend SHALL conectarse al endpoint de WebSocket resolviendo la URL de manera dinámica a partir del host y puerto activos en el navegador o la variable de entorno, evitando conexiones fijas a `localhost` en entornos de producción.

#### Scenario: Conexión en entorno VPS o producción remota
- **WHEN** la aplicación se carga en el dominio `https://logica.espalhar.shop`
- **THEN** el cliente WebSocket SHALL iniciar la conexión hacia `wss://logica.espalhar.shop/ws/admin-sync`.

### Requirement: Tolerancia de Fallos en Auditoría de Login
El endpoint de autenticación `/auth/login` del backend SHALL permitir el acceso a usuarios con credenciales válidas y retornar el token de seguridad incluso si la actualización de auditoría del campo `last_login` en la base de datos falla. Todo fallo asíncrono durante un rollback MUST ser registrado explícitamente en el log del sistema para no encubrir problemas de red o conexión.

#### Scenario: Fallo de conexión o bloqueo al actualizar el timestamp de login
- **WHEN** el usuario ingresa credenciales correctas pero la base de datos falla al realizar el commit de `last_login`
- **THEN** el sistema SHALL capturar el error, intentar realizar un rollback de la transacción fallida (registrando el error crítico si también falla), y retornar el Token de acceso de forma exitosa.

### Requirement: Integración de Timeouts en Solicitudes Fetch
El cliente frontend SHALL definir un límite de tiempo de espera (timeout) en sus solicitudes de comunicación HTTP genéricas hacia la API, de manera que la interfaz no permanezca bloqueada indefinidamente si el backend no responde.

#### Scenario: Backend colgado o caída temporal de red
- **WHEN** una petición fetch excede el límite de tiempo de 10 segundos
- **THEN** el cliente SHALL abortar la petición mediante `AbortController` y propagar un error controlado de timeout.

### Requirement: Carga Centralizada de Secretos
El backend SHALL leer los secretos de autenticación y claves de API de servicios externos de forma centralizada utilizando la clase `Settings`. Los scripts y servicios SHALL NOT invocar directamente al sistema operativo (ej. `os.environ.get`) para extraer contraseñas, tokens o apikeys.

#### Scenario: Inicialización de la configuración del sistema
- **WHEN** el módulo de autenticación, scripts de auditoría o análisis IA requieren secretos del entorno
- **THEN** el sistema SHALL obtenerlos exclusivamente del singleton `settings` centralizado.

### Requirement: Cancelación de Temporizadores WebSocket
El gestor de conexión WebSocket de la aplicación frontend SHALL garantizar la limpieza explícita de todo temporizador de reconexión anterior antes de agendar un nuevo reintento.

#### Scenario: Múltiples eventos de fallo y desconexión
- **WHEN** el socket sufre un `onclose` y `onerror` en rápida sucesión (múltiples llamadas)
- **THEN** el hook de react SHALL ejecutar `clearTimeout` sobre el identificador en curso antes de establecer el temporizador de 10 segundos, impidiendo fugas de memoria o ráfagas asíncronas de reconexión.
