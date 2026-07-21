# Especificación de Error: Graduación Incorrecta en Fase 5

## 📋 Descripción del Problema
En el enrutador del backend de la Fase 5 (`backend/app/fase5/router.py`), el endpoint POST `/graduate` cuenta correctamente los progresos del alumno en la Fase 5, pero al momento de realizar la actualización del perfil del alumno y retornar la respuesta, utiliza por error los valores correspondientes a la graduación de la Fase 2 a la Fase 3. Esto causa que el estudiante retroceda en su progreso visual y lógico a la Fase 3.

---

## 🔍 Detalles Técnicos

- **Archivo Afectado**: `backend/app/fase5/router.py`
- **Función**: `graduate_fase5`
- **Ruta de la API**: `POST /api/fase5/graduate`

### Código Erróneo Actual
```python
@router.post("/graduate")
async def graduate_fase5(
    db: AsyncSession = Depends(get_db),
    alumno: Alumno = Depends(get_current_student),
):
    # ... validación de cantidad de niveles ...
    if aprobados < 26:
        raise HTTPException(
            status_code=400,
            detail=f"Debes dominar los 26 niveles de Fase 2 (14 de práctica y 12 desafíos). Llevas {aprobados}/26.",
        )

    result = await db.execute(select(Fase).where(Fase.orden == 3))
    fase3 = result.scalar_one_or_none()
    if not fase3:
        raise HTTPException(status_code=500, detail="La Fase 3 aún no ha sido configurada.")

    alumno.fase_actual_id = fase3.id
    await db.commit()

    return {
        "message": "¡Felicitaciones! ¡Has dominado la Fase 2 y avanzas a la Fase 3!",
        "nueva_fase_id": fase3.id,
        "nueva_fase_nombre": fase3.nombre,
    }
```

---

## 🛠️ Solución Propuesta

Modificar el endpoint para que consulte la Fase con orden 6 (`Fase 6`) y actualice el perfil del estudiante con dicho identificador.

### Cambio en Código (Diff)
```diff
@@ -1395,22 +1395,22 @@
     aprobados = result.scalar()
-    if aprobados < 26:
+    if aprobados < 13:  # 13 es correcto para la Fase 5 (13 niveles prácticos de semilla)
         raise HTTPException(
             status_code=400,
-            detail=f"Debes dominar los 26 niveles de Fase 2 (14 de práctica y 12 desafíos). Llevas {aprobados}/26.",
+            detail=f"Debes dominar los 13 niveles de práctica de la Fase 5. Llevas {aprobados}/13.",
         )
 
-    result = await db.execute(select(Fase).where(Fase.orden == 3))
-    fase3 = result.scalar_one_or_none()
-    if not fase3:
-        raise HTTPException(status_code=500, detail="La Fase 3 aún no ha sido configurada.")
+    result = await db.execute(select(Fase).where(Fase.orden == 6))
+    fase6 = result.scalar_one_or_none()
+    if not fase6:
+        raise HTTPException(status_code=500, detail="La Fase 6 aún no ha sido configurada.")
 
-    alumno.fase_actual_id = fase3.id
+    alumno.fase_actual_id = fase6.id
     await db.commit()
 
     return {
-        "message": "¡Felicitaciones! ¡Has dominado la Fase 2 y avanzas a la Fase 3!",
-        "nueva_fase_id": fase3.id,
-        "nueva_fase_nombre": fase3.nombre,
+        "message": "¡Felicitaciones! ¡Has dominado la Fase 5 y avanzas a la Fase 6!",
+        "nueva_fase_id": fase6.id,
+        "nueva_fase_nombre": fase6.nombre,
     }
```

---

## 📋 Requerimientos (ADDED Requirements)

### Requirement: Graduación correcta de la Fase 5
El sistema de backend MUST validar la maestría de los 13 niveles de práctica de la Fase 5 y, tras la aprobación, actualizar la fase actual del alumno a la Fase 6 (orden 6) en la base de datos.

#### Scenario: Graduación de Fase 5 exitosa
- **WHEN** un alumno con los 13 niveles dominados realiza la petición de graduación `POST /api/fase5/graduate`
- **THEN** el sistema actualiza su `fase_actual_id` al ID de la Fase 6 y retorna un mensaje de éxito indicando el avance, y se ha ajustado el mensaje de error para que no mencione "Fase 2" ni "desafíos".

---

## 🧪 Plan de Verificación

1. **Prueba Unitaria / Integración**:
   - Crear una sesión de alumno de prueba en base de datos.
   - Forzar el estado de maestría de los 13 niveles de la Fase 5 de este alumno a `APROBADO`.
   - Realizar la llamada `POST /api/fase5/graduate` con las credenciales de este alumno.
   - Validar que el response sea exitoso (HTTP 200) y que indique el avance a la Fase 6.
   - Consultar el registro de `Alumno` en base de datos y verificar que `fase_actual_id` sea el ID correspondiente a la Fase 6.
