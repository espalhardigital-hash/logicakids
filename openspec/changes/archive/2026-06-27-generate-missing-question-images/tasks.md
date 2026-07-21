## 1. Preparación y Configuración del Entorno

- [x] 1.1 Validar que los contenedores docker locales estén arriba y que MinIO local sea accesible.
- [x] 1.2 Confirmar que las variables de entorno de MinIO estén configuradas en `docs/Pruebas_y_Test_Unitario/.env.local`.

## 2. Ejecución de Autocuración (Auto-Healing)

- [x] 2.1 Ejecutar el script `backend/scripts/audit_question_images.py` indicando que autocure y genere las 595 imágenes faltantes de las Fases 3 a 8.
- [x] 2.2 Monitorear la consola del script para confirmar la generación de relojes, fracciones, dados, planos cartesianos y urnas de colores de forma secuencial.
- [x] 2.3 Validar que el script no lance excepciones de red o base de datos y que complete el ciclo exitosamente.

## 3. Verificación de Integridad Física en MinIO y DB

- [x] 3.1 Ejecutar el script de diagnóstico `backend/scripts/verify_minio_integrity.py` una vez finalizada la autocuración.
- [x] 3.2 Confirmar que el conteo de imágenes faltantes se reduzca a **0** (o sea, 100% de imágenes existentes en MinIO).
- [x] 3.3 Verificar visualmente en el simulador del administrador que las imágenes generadas se rendericen de forma correcta y premium.
