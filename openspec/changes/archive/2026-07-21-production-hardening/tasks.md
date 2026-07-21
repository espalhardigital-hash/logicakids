## 1. OpenSpec y alcance

- [x] 1.1 Crear propuesta, diseno y tareas de hardening de produccion.
- [x] 1.2 Validar la propuesta OpenSpec con la herramienta disponible del proyecto, si existe.
- [x] 1.3 Confirmar el orden de implementacion: HTML seguro primero, backend/config despues, quality gates y bundles al final.

## 2. Seguridad HTML / XSS

- [x] 2.1 Agregar dependencia de sanitizacion HTML compatible con React/Vite (e.g. dompurify).
- [x] 2.2 Crear helper central `safeHtml`/`sanitizeHtml` en frontend y conectarlo con `formatContent`.
- [x] 2.3 Reemplazar usos directos de `dangerouslySetInnerHTML` en teoria, preguntas, alternativas, simulador admin y feedback overlay.
- [x] 2.4 Validar URLs de markdown para imagenes/enlaces y bloquear `javascript:`, data URLs no permitidas y atributos inline peligrosos.
- [x] 2.5 Agregar tests unitarios para payloads XSS comunes.
- [x] 2.6 Verificar build y render basico de fases con HTML pedagogico existente.

## 3. Autenticacion segura para produccion

- [x] 3.1 Agregar configuracion de entorno para modo de sesion: cookie segura vs token legacy local.
- [x] 3.2 Hacer que login/register seteen cookie `HttpOnly`, `Secure` en produccion y `SameSite` adecuado.
- [x] 3.3 Actualizar frontend para usar `credentials: "include"` en llamadas autenticadas.
- [x] 3.4 Mantener compatibilidad local con bearer token solo bajo bandera dev.
- [x] 3.5 Agregar pruebas de login, `/users/me` y logout para ambos modos.

## 4. Backend production hardening

- [x] 4.1 Proteger o deshabilitar `/admin/system-config` en produccion mediante bandera explicita.
- [x] 4.2 Evitar devolver `DATABASE_URL` o secretos desde endpoints HTTP en produccion.
- [x] 4.3 Cambiar SQLAlchemy `echo` a `False` por defecto y hacerlo configurable para local.
- [x] 4.4 Desactivar `Base.metadata.create_all` en produccion; dejarlo solo para local/dev explicito.
- [x] 4.5 Revisar CORS para dominios exactos de produccion y desarrollo.
- [x] 4.6 Verificar arranque backend con variables locales y documentar valores Portainer.

## 5. Frontend release gates y tests

- [x] 5.1 Cambiar `LogicaMath/frontend` build a `tsc --noEmit && vite build`.
- [x] 5.2 Corregir errores TypeScript actuales hasta que `npx tsc --noEmit` pase.
- [x] 5.3 Configurar Vitest para incluir solo `*.test.ts` y `*.test.tsx`.
- [x] 5.4 Mantener Playwright separado para `*.spec.ts`.
- [x] 5.5 Reemplazar o corregir `@testing-library/react-hooks` en `useWebSocket.test.ts`.
- [x] 5.6 Revisar tests desactualizados que esperan URLs hardcoded.

## 6. Variables, repositorio y despliegue

- [x] 6.1 Unificar `VITE_API_URL` / `VITE_API_BASE_URL` y actualizar `.env.example`, Dockerfile y docs.
- [x] 6.2 Agregar ignores para `LogicaMath/frontend/playwright-report/`, `LogicaMath/frontend/test-results/` y artefactos similares.
- [x] 6.3 Documentar checklist minimo para GitHub + Portainer: env vars, migraciones, dominios, CORS, cookies y rollback.

## 7. Bundles y performance

- [x] 7.1 Registrar baseline de chunks de produccion.
- [x] 7.2 Detectar imports estaticos que impiden code splitting real.
- [x] 7.3 Separar Fabric/Three/visualizadores pesados por rutas o imports dinamicos.
- [x] 7.4 Definir budget inicial de chunks y revisar que build no crezca sin control.
