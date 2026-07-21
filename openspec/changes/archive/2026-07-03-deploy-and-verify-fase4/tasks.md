## 1. Version Control (GitHub Update)

- [x] 1.1 Sincronizar los últimos cambios locales y empujarlos a la rama `desarrollo` en GitHub.
- [x] 1.2 Cambiar a la rama `main` (producción), integrar `desarrollo`, y empujar `main` a GitHub.

## 2. Despliegue Local y Verificación de Logs

- [x] 2.1 Re-desplegar los contenedores locales usando `docker compose -f docs/Pruebas_y_Test_Unitario/docker-compose.local.yml up -d --build`.
- [x] 2.2 Inspeccionar los logs del backend y frontend local para asegurar que estén corriendo correctamente.

## 3. Pruebas y Validación (Fase 4 vs Fase 2)

- [x] 3.1 Iniciar sesión en el entorno local y realizar pruebas en la Fase 4 para corroborar la lógica de opción múltiple (interacción de confirmación/aviso de error/botón Continuar).
- [x] 3.2 Verificar que el contador de errores acumulados comience en 0 al iniciar el desafío y que no herede errores de sesiones pasadas tras fallar (early exit reset).

## 4. Documentación y Cierre

- [x] 4.1 Crear un reporte/walkthrough con los resultados de las pruebas y el estado de la VPS (contingencia por corte de conexión SSH).
