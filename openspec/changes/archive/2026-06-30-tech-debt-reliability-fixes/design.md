## Context

Se ha detectado durante una auditoría preventiva que la aplicación arrastra deuda técnica respecto a los lineamientos de arquitectura en `api-reliability-and-security.md`. El frontend está expuesto a cuelgues permanentes al usar llamadas `fetch` nativas en la lógica de las Fases (Fase2 a Fase9). Los WebSockets del frontend tienen riesgos de fuga de memoria por temporizadores mal cerrados, y los scripts asíncronos del backend violaban el encapsulamiento de secretos.

## Goals / Non-Goals

**Goals:**
- Proteger al usuario de la aplicación frente a fallas de red usando el patrón de cancelación (`AbortController`) implementado en `fetchWithTimeout`.
- Evitar múltiples callbacks y memory leaks en la reconexión automática de WebSocket.
- Centralizar la gestión de variables sensibles en `settings`.
- Registrar fallas que actualmente ocurren silenciosamente en la DB.

**Non-Goals:**
- Reescribir la arquitectura completa de Fetch a librerías de terceros (e.g. Axios o React Query)
- Crear nuevas fases o lógicas didácticas
- Modificar el comportamiento de la sesión de base de datos más allá de hacer explícitos los errores

## Decisions

1. **Reemplazo con fetchWithTimeout:** Aprovechamos la envoltura ya existente en `services/apiHelper.ts`. Alternativa: Agregar AbortController en cada servicio. Elegido: `fetchWithTimeout` porque promueve la reutilización y DRY.
2. **Uso de clearTimeout:** El temporizador guardado en `useRef` será verificado y cancelado explícitamente antes de volver a ser seteado, garantizando así a lo mucho un solo reintento de conexión corriendo.
3. **Migración a config.settings:** Reemplazar explícitamente llamadas nativas del SO para la API Key de Gemini en scripts de auditoría por el pydantic `settings` para garantizar la unicidad de configuraciones.

## Risks / Trade-offs

- **[Risk]** Que las Fases superen los 10 segundos legítimamente. → **Mitigación**: Los endpoints de las Fases (traer preguntas, etc.) usualmente demoran <500ms. 10s de timeout es un rango generoso.
- **[Risk]** Interferencia al loguear los fallos de `rollback`. → **Mitigación**: Se usarán sentencias `print()` nativas y amigables para evitar añadir dependencias complejas de Logging a la clase base por ahora.
