## ADDED Requirements

### Requirement: Reinicio de intentos y errores al iniciar sesión
El sistema backend SHALL recibir un parámetro `reload: bool` al cargar la siguiente pregunta. Si `reload` es verdadero, el backend SHALL purgar el pool asignado y los intentos de la sesión anterior del alumno, estableciendo `aciertos_acumulados` y `intentos_totales` en `0`.

#### Scenario: Reiniciar desafío de Fase 4
- **WHEN** el alumno inicia un desafío de la Fase 4 y el frontend realiza la llamada inicial con `reload=true`
- **THEN** el sistema reinicia el progreso de maestría a 0% y elimina los intentos pasados para evitar heredar errores.

### Requirement: Rediseño del flujo de confirmación en opción múltiple
El sistema frontend SHALL mostrar las opciones de alternativas en modo bloqueado (`disabled`) tras realizar una selección y requerir una confirmación explícita mediante un botón de continuar/confirmar, alineándolo con el comportamiento de la Fase 2.

#### Scenario: Avance manual tras responder
- **WHEN** el alumno selecciona una opción y presiona continuar
- **THEN** el sistema valida la respuesta y avanza al siguiente paso sin congelar la pantalla.
