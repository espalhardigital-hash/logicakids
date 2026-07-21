# Checklist de Despliegue en Producción (GitHub + Portainer)

Este documento detalla la lista de verificación para el despliegue seguro en producción de LogicaKids Pro mediante GitHub y Portainer.

---

## 1. Variables de Entorno en Portainer

Asegurarse de definir las siguientes variables en la pila de producción (Stack en Portainer):

### Backend (`docker-compose_Producion.yml`)
- `ENVIRONMENT=production`
- `SESSION_MODE=cookie` (o `token` si se conecta desde clientes móviles/externos sin soporte cookie)
- `COOKIE_SECURE=True` (requiere HTTPS habilitado con certificado SSL en Traefik/Nginx)
- `COOKIE_SAMESITE=lax` (o `strict`)
- `ENABLE_SYSTEM_CONFIG_ENDPOINT=False` (bloquea la exposición de credenciales y vars de sistema)
- `SQL_ECHO=False` (desactiva logs masivos de SQL en backend)
- `SKIP_DB_ALTERATIONS=true` (evita que SQLAlchemy modifique esquemas en arranque; las migraciones se aplican con Alembic)
- `CORS_ORIGINS=https://logica.espalhar.shop,https://matematicas.espalhar.shop` (orígenes explícitos para soporte de cookies con `credentials: 'include'`)

### Frontend
- `VITE_API_URL=/api`

---

## 2. Base de Datos y Migraciones Alembic

1. **Alembic Single Source of Truth**: `Base.metadata.create_all` está deshabilitado automáticamente en produccion (`ENVIRONMENT=production` o `SKIP_DB_ALTERATIONS=true`).
2. **Ejecución de Migraciones**:
   ```bash
   docker exec -it logicakids_backend alembic upgrade head
   ```
3. **Validación de Schema**: Verificar que las tablas y columnas concuerden antes de habilitar tráfico web.

---

## 3. Seguridad y Gates de Calidad

- **XSS Sanitization**: Todos los campos con HTML dinámico (teoría, preguntas, feedback) se sanitizan con `DOMPurify` (allowlist de etiquetas `p`, `span`, `div`, `strong`, `em`, `a`, `img`, `svg`).
- **TypeScript & Build Gate**: Antes de hacer push a la rama de release, ejecutar:
  ```bash
  npm run build
  ```
  Esto ejecutará `tsc --noEmit && vite build`. Si hay algún error de tipos o compilación, la release se detendrá inmediatamente.
- **Tests Unitarios**:
  ```bash
  npm run test
  ```

---

## 4. Rollback Plan

En caso de fallo crítico post-despliegue en Portainer:
1. Revertir la imagen Docker en Portainer al tag anterior estable.
2. Si la migración de BD introdujo cambios destructivos, ejecutar downgrade en Alembic:
   ```bash
   docker exec -it logicakids_backend alembic downgrade -1
   ```
3. Reiniciar el contenedor desde la consola web de Portainer.
