# Especificación de Diseño: Autocuración y Auditoría de Gráficos (Image Healing)

## 📋 Propósito
El propósito de esta especificación es regular el pipeline de auditoría automática y autocuración offline del material didáctico gráfico en el banco de preguntas escolar de las Fases 3 a 8, asegurando que el 100% de las preguntas cuenten con recursos visuales asignados en el storage y DB local.

---

## 📋 Requerimientos (ADDED Requirements)

### Requirement: Detección y Auditoría de Gráficos Faltantes
El script de inicialización de imágenes MUST escanear la base de datos de preguntas y detectar de manera inteligente todas las preguntas de las Fases 3 a 8 que carecen de imágenes y requieren material visual.

#### Scenario: Reporte correcto de imágenes faltantes
- **WHEN** el script de auditoría es ejecutado contra la base de datos local
- **THEN** calcula el listado de IDs de preguntas con imágenes ausentes y lo despliega en consola estructuradamente

### Requirement: Generación Procedimental Precisa
El sistema MUST poder generar geométricamente diagramas vectoriales para relojes analógicos, planos cartesianos, grillas de área, círculos/barras de fracciones, dados y urnas transparentes de esferas.

#### Scenario: Reloj analógico generado geométricamente
- **WHEN** una pregunta faltante de la Fase 3 requiere una hora específica (ej. "3:45")
- **THEN** el motor vectorial calcula los ángulos trigonométricos de las manecillas, renderiza el gráfico usando Pillow y guarda el archivo PNG sin distorsión visual

### Requirement: Integración con Storage MinIO y Base de Datos
El script de autocuración MUST subir los gráficos generados al bucket `logicakids` del MinIO local y actualizar el registro `datos_numericos` de la base de datos PostgreSQL con el URL correcto.

#### Scenario: Sincronización exitosa de imagen autocurada
- **WHEN** una imagen es autocurada y subida con éxito a MinIO
- **THEN** el script actualiza la columna `datos_numericos` en Postgres de modo que la clave `url` apunte al endpoint físico de MinIO, permitiendo la carga inmediata en la app

---

## 🧪 Plan de Verificación

1. **Auditoría de Banco**:
   - Comprobar que el script liste en consola las preguntas sin URL o con HTTP 404.
2. **Dibujo de Geometrías**:
   - Generar imágenes de prueba locales para los distintos tipos visuales y validar su resolución y correcta proporción visual.
3. **Integridad en MinIO**:
   - Ejecutar el script `verify_minio_integrity.py` y comprobar que todas las imágenes autocuradas respondan a peticiones S3 exitosamente.
