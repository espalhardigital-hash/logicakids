# Plan de Mejoras Profundas — LogicaKids Pro

> **Origen:** Auditoría Integral del Sistema y aplicación del protocolo [`razonamiento_profundo_PRO.md`](razonamiento_profundo_PRO.md)  
> **Ámbito de Aplicación:** LogicaKids Pro (Fases 1 a 8 activas; Fases 9 a 11 en construcción/revisión futura)  
> **Estado del Entorno:** Modo Pruebas Locales 100% (Infraestructura VPS preservada intacta)  

---

## 1. Resumen Ejecutivo

Este documento establece la hoja de ruta técnica para ejecutar el saneamiento de **seguridad**, **integridad de datos**, **limpieza de arquitectura** y **pruebas de no-regresión** en LogicaKids Pro.

El plan prioriza las intervenciones por **Radio de Explosión** y **Matriz de Riesgo × Esfuerzo**, garantizando que ninguna mejora técnica altere la pedagogía de los ejercicios ni degrade las funcionalidades existentes.

---

## 2. Matriz Priorizada de Intervenciones

| Fase del Plan | Objetivo Principal | Urgencia | Esfuerzo | Impacto |
| :--- | :--- | :---: | :---: | :---: |
| **Etapa 1: Seguridad (Hardening)** | Sanitización XSS en Frontend y Auth WebSocket | 🚨 Alta | Medio | Crítico |
| **Etapa 2: Arquitectura y Mapeo** | Mapa Canónico de Fases e Higiene de Docstrings | 🟠 Media | Bajo | Alto |
| **Etapa 3: Integridad de Pool (BD)** | Auditoría automatizada de preguntas y alternativas | 🟠 Media | Medio | Alto |
| **Etapa 4: Contrato y CI/CD** | Suite de Pruebas E2E en proceso para Routers | 🟡 Normal | Medio | Alto |
| **Etapa 5: Gobernanza Frontend** | Optimización de Bundle y Componentes Genéricos | 🔵 Futura | Alto | Medio |

---

## 3. Detalle de Etapas de Implementación

### Etapa 1: Hardening de Seguridad e Sanitización HTML (Corto Plazo)

#### 1.1 Helper Único de Sanitización en Frontend (`Arquetipo P`)
- **Problema:** En múltiples pantallas (`FaseGenericGameScreen.tsx`, `Fase8GameScreen.tsx`, `Fase7GameScreen.tsx`, `Fase6GameScreen.tsx`, `Fase5GameScreen.tsx`, `Fase3GameScreen.tsx`, `Fase7TheoryModal.tsx`, etc.) se renderiza HTML crudo mediante `dangerouslySetInnerHTML` sin sanitizar.
- **Acción:**
  1. Crear `LogicaMath/frontend/utils/sanitizeHtml.ts` utilizando una librería de sanitización (ej: `DOMPurify` / `sanitize-html`).
  2. Configurar una lista blanca (allowlist) de etiquetas pedagógicas: `['strong', 'em', 'b', 'i', 'sub', 'sup', 'span', 'p', 'br', 'svg', 'path', 'g']` y clases CSS seguras (ej. `keyword-highlight`).
  3. Reemplazar todos los usos directos de `dangerouslySetInnerHTML={{ __html: text }}` por `dangerouslySetInnerHTML={safePedagogicalHtml(text)}`.
- **Criterio de Aceptación:** `rg "dangerouslySetInnerHTML" LogicaMath/frontend` muestra que el 100% de las coincidencias pasan por la función de sanitización.

#### 1.2 Autenticación en WebSocket (`Arquetipo S10/O`)
- **Problema:** El endpoint `@app.websocket("/ws/admin-sync")` en `main.py` acepta cualquier conexión anónima.
- **Acción:**
  1. Extraer el token de la query string (`/ws/admin-sync?token=...`) o de la cookie de sesión durante el evento de handshake.
  2. Validar la firma JWT y expirar el socket si la autenticación falla antes de ejecutar `manager.connect(websocket)`.
- **Criterio de Aceptación:** Solicitudes de conexión WS sin token reciben rechazo 401/403.

---

### Etapa 2: Alineación Arquitectónica y Congelamiento de Mapeos (Medio Plazo)

#### 2.1 Congelamiento del Mapa Canónico de IDs (`Recomendación R1`)
- **Problema:** Descalce entre carpetas de backend (`app/fase8`), nombres de componentes frontend (`Fase7GameScreen`), rutas API y `fase_id` en la BD.
- **Acción:**
  1. Crear `docs/MAPA_CANONICO_FASES.md` detallando la correspondencia exacta:
     * `fase_id` (Base de Datos)
     * Ruta Backend (`app/faseN/`)
     * Prefijo API (`/api/faseN/`)
     * Componente Frontend (`components/faseN/`)
     * Módulo Pedagógico Rector
  2. Prohibir renumeraciones automáticas de `fase_id` en migraciones de base de datos.

#### 2.2 Higiene de Docstrings y Copy-Paste (`Arquetipo H`)
- **Problema:** Docstrings heredados de Fase 2 en `fase6/schemas.py`, `fase6/router.py`, `fase5/schemas.py`, y `is_money = (modulo_id == 3)` en `fase11/router.py`.
- **Acción:**
  1. Actualizar los comentarios docstrings para reflejar fielmente el nombre y número de la fase actual.
  2. Normalizar `is_money = False` en fases que no gestionan transacciones monetarias.

---

### Etapa 3: Integridad de Pool de Preguntas en Base de Datos (Medio Plazo)

#### 3.1 Pruebas de Integridad de Opciones y Respuestas (`Arquetipos B, E, F`)
- **Acción:**
  Crear un script de auditoría periódica (`LogicaMath/backend/app/tests/test_pool_integrity.py`) que ejecute consultas SQL de verificación:
  - **Preguntas de opción múltiple sin alternativas:** Detectar mediante `LEFT JOIN` preguntas `MULTIPLE_OPCION` con 0 filas en `alternativas`.
  - **Respuestas numéricas con texto:** Verificar que preguntas `RESPUESTA_NUMERICA` contengan únicamente valores numéricos parseables.
  - **Cardinalidad de Familias (`estructura_padre_id`):** Garantizar que ninguna sección de práctica mantenga `estructura_padre_id` en NULL para evitar bloqueos en el cálculo de maestría.

---

### Etapa 4: Pruebas Automáticas y Contratos API (Medio Plazo)

#### 4.1 Test de Contrato E2E por Fase (`Recomendación R4`)
- **Acción:**
  1. Crear un harness de prueba en Python que instancie la base de datos de pruebas locales.
  2. Simular ejecuciones de `responder_faseN` enviando payloads de respuestas correctas e incorrectas.
  3. Validar que la respuesta contenga los campos esperados por el frontend y que el estado progrese de `EN_PROGRESO` a `APROBADO` al 100%.

---

## 4. Matriz de No-Regresión (Checklist PRO §P8)

Antes de declarar completada cualquiera de las etapas de este plan, se deberán verificar las siguientes invariantes:

- [ ] **Compilación limpia:** `npx tsc --noEmit` en frontend sin errores de tipo.
- [ ] **Sintaxis backend:** `python -m py_compile` sin errores de sintaxis en FastAPI.
- [ ] **Sin fugas de secretos:** Ninguna variable `.env`, `SECRET_KEY` o credencial expuesta en logs o diffs.
- [ ] **Verificación de caminos colaterales:** Probar tanto el camino feliz (respuesta correcta) como el de error (respuesta incorrecta/reloj agotado).
- [ ] **Preservación de datos locales:** No alterar esquemas en `Datos_Producion/` ni `Datos_Desarrollo/`.

---

## 5. Próximos Pasos Recomendados

1. **Revisar y Aprobar este Plan:** Confirmar el alcance y las prioridades propuestas.
2. **Ejecución por Etapas:** Comenzar con la **Etapa 1 (Hardening de Seguridad)** debido a su impacto directo en la solidez del sistema.
