## 1. Conexiones de API y Contratos (Backend & Frontend)

- [x] 1.1 Modificar el endpoint de WebSocket `/ws/admin-sync` en `backend/app/main.py` para utilizar un bloque `finally:` que asegure `manager.disconnect(websocket)`.
- [x] 1.2 **Test de Verificación 1.1:** Escribir y ejecutar un script de test unitario en Python que simule una desconexión abrupta de WebSocket y valide que el socket se remueve de la lista de conexiones activas.
- [x] 1.3 Modificar el router de login en `backend/app/routers/auth_users.py` envolviendo la actualización de `last_login` en un try/except con rollback de base de datos.
- [x] 1.4 **Test de Verificación 1.3:** Escribir y ejecutar un test en Python que simule un fallo de base de datos durante el commit de `last_login` y verifique que la autenticación del usuario aún tiene éxito y retorna el Token.
- [x] 1.5 Crear el helper `fetchWithTimeout` en `frontend/services/apiHelper.ts` (o similar) e integrarlo en `frontend/services/authService.ts`.
- [x] 1.6 **Test de Verificación 1.5:** Escribir un test unitario en Vitest que simule una petición colgada y compruebe que se cancela por timeout tras el tiempo configurado.

## 2. WebSocket Dinámico y Wrapper de Renderizado (Frontend)

- [x] 2.1 Modificar `frontend/components/useWebSocket.ts` para dinamizar el cálculo de la URL de conexión de WebSocket basándose en el host y protocolo actuales.
- [x] 2.2 **Test de Verificación 2.1:** Escribir un test de Vitest que verifique que la función calcula la URL correcta bajo entornos de localhost y de producción remota HTTPS (wss).
- [x] 2.3 Crear `PlayRouteWrapper` en `frontend/App.tsx` y reemplazar la IIFE inline del router `/play` por este componente envoltura.
- [x] 2.4 **Test de Verificación 2.3:** Compilar el frontend y correr un test de renderizado básico para asegurar que `PlayRouteWrapper` se renderiza de forma consistente sin desmontajes.

## 3. Centralización de Secretos y Configuración (Backend)

- [x] 3.1 Actualizar `backend/app/auth.py` y `backend/app/services/ai_service.py` sustituyendo las llamadas directas de `os.getenv` por el singleton `settings`.
- [x] 3.2 **Test de Verificación 3.1:** Compilar el backend y verificar que no existan errores de importación de variables de entorno ni fallos en la inicialización del servidor.
