## Why

Esta propuesta corrige múltiples hallazgos en la API y el cliente frontend de la aplicación. Estos problemas comprometen el rendimiento, la robustez de las conexiones, la seguridad frente a CORS y la tolerancia a fallos en la persistencia de auditorías de acceso de usuario. Adicionalmente, se elimina la url hardcoded de localhost en los WebSockets para permitir su funcionamiento nativo en producción.

## What Changes

- **Integración de timeouts en fetch (Frontend):** Añadir tiempos de espera a las peticiones HTTP del frontend para evitar bloqueos por respuestas colgadas.
- **Robustez de WebSocket en backend (Backend):** Utilizar un bloque `finally:` para asegurar que las conexiones muertas se desconecten siempre.
- **Tolerancia a fallos en last_login (Backend):** Envolver el commit de actualización del campo `last_login` en un try/except para evitar que fallos de auditoría de BD bloqueen el login de usuarios válidos.
- **Dinamización de WebSocket en producción (Frontend):** Construir dinámicamente la URL del WebSocket del administrador según el host y protocolo de la ventana actual.
- **Eliminación de renderizados y desmontajes repetitivos (Frontend):** Reemplazar la IIFE inline del router `/play` por un wrapper para optimizar el rendimiento y evitar reconstrucción del estado de `GameScreen`.
- **CORS restrictivo por entornos (Backend):** Habilitar orígenes estrictos en producción.
- **Carga de secretos unificada (Backend):** Reemplazar el uso de `os.getenv` por settings unificados en `auth.py` y `ai_service.py`.

## Capabilities

### New Capabilities

- `api-reliability-and-security`: Definición de reglas de resiliencia para la sincronización push (WebSocket), comunicación fetch tolerante a fallos, seguridad en orígenes CORS y configuraciones unificadas en backend y frontend.

### Modified Capabilities

## Impact

- **Backend:** `LogicaMath/backend/app/main.py`, `LogicaMath/backend/app/routers/auth_users.py`, `LogicaMath/backend/app/auth.py` y `LogicaMath/backend/app/services/ai_service.py`.
- **Frontend:** `LogicaMath/frontend/App.tsx`, `LogicaMath/frontend/components/useWebSocket.ts`, y helpers comunes de servicios en el frontend.
