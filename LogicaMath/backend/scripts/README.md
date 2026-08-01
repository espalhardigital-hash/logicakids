# Herramientas mantenidas del backend

Esta carpeta contiene puntos de entrada manuales. No forman parte del arranque de FastAPI, pero se conservan porque cubren operaciones repetibles, auditorías o pruebas de diagnóstico.

## Sincronización y ambientes

- `sync_db_and_minio_prod.py`: flujo canónico de sincronización de preguntas y recursos.
- `sync_helpers.py`: utilidades compartidas y cubiertas por pruebas.
- `sync_minio_vps.py`, `sync_exact_questions_to_vps.py`, `sync_questions_fast.py`: variantes operativas de sincronización.
- `sync_fases_and_config.py`, `sync_niveles_teoria_pool.py`: alineación selectiva de metadatos y teoría.
- `compare_environments.py`, `verify_minio_integrity.py`: comprobaciones entre ambientes y almacenamiento.
- `export_db_urls.py`, `export_ux_feedback.py`: exportaciones diagnósticas.

Antes de escribir en una base remota se debe seguir `RULES AGENTES/bd_minio.md` y ejecutar el modo de pre-vuelo disponible.

## Contenido y auditoría

- `apply_teacher_feedback.py`: aplica retroalimentación docente; su configuración está cubierta por pruebas.
- `audit_question_images.py`: audita imágenes de preguntas; su configuración está cubierta por pruebas.
- `audit_fase4_integrity.py`: inventario de solo lectura de configuraciones y progresos canónicos/fantasma de Fase 4; admite `--snapshot` y nunca reconcilia datos.
- `audit_all_fases_svg.py`, `audit_deep_db.py`, `audit_fase5_deep.py`, `audit_fases_5_6_7.py`, `audit_niveles_teoria.py`, `audit_theory_data.py`: diagnósticos de contenido y base.
- `seed_fase9_real.py`: seeder manual del contenido real de Fase 9.

## Pruebas manuales

- `test_local_endpoints.py`, `test_sre.py`, `test_svg_render.py`: comprobaciones manuales que requieren servicios o recursos locales.
- `verify_fase4_api_journey.py`: recorre por API los 25 bloques de Fase 4, prueba autorización, sección, doble envío y graduación. Se niega a ejecutar salvo que `DATABASE_URL` contenga `fase4_test` y elimina el usuario sintético en `finally`.

## Política de limpieza

Los parches `fix_*`, inspectores de incidentes concretos, migraciones one-shot y actualizadores que duplicaban el seed canónico fueron retirados después de verificar que no tenían consumidores. Una herramienta nueva debe indicar propósito, ambiente permitido, modo de pre-vuelo y procedimiento vigente; de lo contrario se considera temporal.
