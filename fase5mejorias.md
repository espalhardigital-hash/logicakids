# Fase 5 — Diagnóstico y Plan de Mejoras (Geometría Plana y Medidas)

> **Documento de handoff técnico.** Escrito para que otro agente/LLM (o el mismo, en otra sesión) pueda implementar los cambios sin contexto previo de esta conversación. Incluye evidencia de código (archivo + línea), causa raíz, solución propuesta con snippets, impacto en base de datos, impacto en MinIO/storage, y el procedimiento exacto para aplicar los cambios en el entorno **local**.
>
> Fecha del diagnóstico: 2026-07-21. Rama activa: `desarrollo`. Entorno de referencia: **Local** (`Datos_localhost/` + `docker-compose.local.yml`), no VPS.
>
> **Regla de oro para quien implemente esto:** todos los cambios de contenido de Fase 5 viven en **código Python que siembra la base de datos** (no son archivos JSON sueltos). No basta con editar texto: hay que tocar `seed.py`/`theory_examples.py`, **subir la versión de seed**, y **re-sembrar** la base de datos local para que el cambio se refleje en la app. Todo esto se explica en la sección 6.

---

## 0. Índice

1. [Resumen ejecutivo](#1-resumen-ejecutivo)
2. [Arquitectura relevante de Fase 5](#2-arquitectura-relevante-de-fase-5)
3. [Problemas encontrados (con evidencia)](#3-problemas-encontrados-con-evidencia)
4. [Soluciones propuestas (detalladas, con código)](#4-soluciones-propuestas-detalladas-con-código)
5. [Impacto y consideraciones de Base de Datos](#5-impacto-y-consideraciones-de-base-de-datos)
6. [Impacto y consideraciones de MinIO / Storage](#6-impacto-y-consideraciones-de-minio--storage)
7. [Plan de implementación paso a paso](#7-plan-de-implementación-paso-a-paso)
8. [Plan de pruebas / validación](#8-plan-de-pruebas--validación)
9. [Reglas y restricciones que debe respetar quien implemente](#9-reglas-y-restricciones-que-debe-respetar-quien-implemente)
10. [Apéndice A — Inventario completo de figuras faltantes por nivel](#apéndice-a--inventario-completo-de-figuras-faltantes-por-nivel)
11. [Apéndice B — Catálogo de funciones de `svg_helpers.py` listas para usar](#apéndice-b--catálogo-de-funciones-de-svg_helperspy-listas-para-usar)

---

## 1. Resumen ejecutivo

La Fase 5 ("Geometría Plana y Medidas") tiene 4 módulos y 13 niveles de práctica libre (+ 3 desafíos por módulo = 25 secciones evaluables + 1 desafío mixto). Cada nivel de práctica libre tiene una pantalla de **teoría** (`Fase5TheoryModal.tsx`) con 3 bloques:

1. **Intro** (texto + diccionario)
2. **Ejemplos guiados** (`ejemplos`) — muestran problema resuelto paso a paso
3. **Interactivos** ("¡Tu turno!", `interactivos`) — el alumno resuelve un ejercicio similar antes de pasar a la práctica libre real

**Hallazgo principal:** los **Ejemplos guiados tienen figura en el 100% de los casos (52/52)**, pero los **Interactivos solo tienen figura en 3 de 39 casos (7.7%)** — 36 ejercicios "¡Tu turno!" son puro texto. Esto rompe la continuidad pedagógica: el niño ve una figura rica explicando el concepto y, un paso después, se le pide resolver "a ciegas" sin apoyo visual. Este es el defecto que el usuario reportó como "ausencia de figuras" (la imagen que motivó este análisis correspondía justamente a un Ejemplo Guiado que sí tiene figura — el problema está un paso más adelante, en el interactivo).

**Causa raíz técnica:** existe un archivo `LogicaMath/backend/app/fase5/svg_helpers.py` con 8 funciones ya construidas para generar figuras SVG parametrizadas (rectángulo, cuadrado, triángulo, forma en L, polígono con etiquetas, rectángulo sombreado, etc.) pero **nunca se importa ni se usa en ningún lugar del código**. Es una pieza de infraestructura terminada y no conectada.

Además de este hallazgo central, se identificaron 8 problemas secundarios (inconsistencia de tema visual, errores geométricos puntuales, tipografía pequeña, falta de cotas en imágenes de rejilla, ausencia de enseñanza de Pitágoras antes de exigirlo, diccionario pedagógico escueto, y una **fuga de almacenamiento en MinIO** en cada re-siembra).

Este documento detalla los 9 problemas, propone solución concreta para cada uno, y da el procedimiento exacto de base de datos y MinIO para que el cambio impacte en el entorno local.

---

## 2. Arquitectura relevante de Fase 5

### 2.1 Flujo de datos (teoría)

```
seed.py (seed_teoria_niveles)
  └─> INSERT en tabla niveles_teoria_pool (modelo NivelTeoria, JSONB: ejemplos, interactivos, diccionario)
        └─> GET /fase5/lectura/{modulo_id}/nivel/{nivel_id}  (router.py:438-472)
              └─> Fase5ContenidoLectura (schemas.py:233-242)
                    └─> Fase5TheoryModal.tsx (frontend, renderiza ejemplos/interactivos)
```

### 2.2 Flujo de datos (práctica / preguntas)

```
seed.py (seed_practica_pool, seed_preguntas_desafios)
  └─> _gen_fase5_pool() -> _gen_fase5_pool_raw()  (genera enunciado + figura + alternativas)
        └─> graphics_generator.py (genera PNG) -> storage_service.upload_question_graphic() -> MinIO / fallback local
        └─> INSERT en tabla preguntas (modelo Pregunta, campo datos_numericos.url)
              └─> GET /fase5/modulo/{id}/nivel/{id}/pregunta (router.py:479-...)
                    └─> Fase5GameScreen.tsx (renderiza <img src={datos_numericos.url}>)
```

### 2.3 Archivos involucrados (mapa completo)

| Archivo | Rol |
|---|---|
| `LogicaMath/backend/app/fase5/seed.py` | Siembra `NivelTeoria` (teoría + interactivos) y `Pregunta` (pool de práctica/desafíos). **Archivo principal a editar.** |
| `LogicaMath/backend/app/fase5/theory_examples.py` | Contiene `obtener_ejemplos_expandidos_fase5(modulo_id, nivel_id)` — los 52 "Ejemplos guiados" con SVG ya embebido (referencia de estilo correcto). |
| `LogicaMath/backend/app/fase5/svg_helpers.py` | 8 funciones constructoras de SVG, **no usadas actualmente**. Ver Apéndice B. |
| `LogicaMath/backend/app/utils/graphics_generator.py` | Genera imágenes PNG (Pillow) para preguntas de práctica (rectángulos con cotas, figuras en rejilla, figuras rectilíneas). Usa `storage_service.upload_question_graphic()`. |
| `LogicaMath/backend/app/core/storage.py` | `StorageService` — sube a MinIO (S3-compatible) o hace fallback a filesystem local si MinIO no está disponible. |
| `LogicaMath/backend/app/fase5/router.py` | Endpoints: dashboard, lectura/teoría, obtener pregunta, responder, graduar. |
| `LogicaMath/backend/app/fase5/schemas.py` | Pydantic schemas (contratos API). |
| `LogicaMath/backend/app/fase2/models.py` | Define el modelo SQLAlchemy `NivelTeoria` (tabla `niveles_teoria_pool`) — **reutilizado por Fase 5** (no tiene modelo propio). |
| `LogicaMath/backend/app/models/pregunta.py` | Modelo SQLAlchemy `Pregunta` / `Alternativa` (tabla `preguntas`, `alternativas`) — genérico para todas las fases. |
| `LogicaMath/backend/app/seed.py` | Orquestador raíz: contiene `SEED_VERSIONS["fase_5"]` (versión actual: `"20260720_v6"`) y `should_seed_phase()` / `update_seed_version()`. |
| `LogicaMath/frontend/components/fase5/Fase5TheoryModal.tsx` | Renderiza teoría (intro, ejemplos, interactivos, tip). |
| `LogicaMath/frontend/components/fase5/Fase5Types.ts` | Tipos TS que espejan los schemas Pydantic. |
| `LogicaMath/frontend/components/fase5/Fase5GameScreen.tsx` | Renderiza preguntas de práctica/desafío (líneas 1302-1378: `datos_numericos.tipo_visual === 'imagen'` → `<img>`). |
| `Datos_localhost/docker-compose.local.yml` | Stack local: Postgres (5433), Redis (6380), MinIO (9100 API / 9101 consola), backend (8000), frontend (3000). Bucket MinIO local: `logicakids`. |

### 2.4 Modelo de datos relevante

**`NivelTeoria`** (`app/fase2/models.py:54-80`, tabla `niveles_teoria_pool`):
```python
fase_id, modulo_id, nivel_id, titulo,
texto_descubrimiento: Text,
diccionario: JSONB,       # {"Término": "Definición"}
advertencia: Text,        # el "tip pedagógico"
ejemplos: JSONB,          # lista de ejemplos guiados
interactivos: JSONB,      # lista de ejercicios "¡Tu turno!"  <-- foco de la mejora
```

**`Pregunta`** (`app/models/pregunta.py:8-117`, tabla `preguntas`):
```python
fase_id, seccion, operacion, tipo_pregunta,
enunciado: Text,
respuesta_correcta: String,
datos_numericos: JSONB,        # {"tipo_visual": "imagen", "url": "..."} o {"pasos": [...]}
errores_previstos: JSONB,      # feedback pedagógico por error común
explicacion_paso_a_paso: JSONB,
estructura_padre_id: String,   # agrupa "familias" de preguntas (para Bucle Espejo)
```

**Forma esperada de un `interactivo`** (según `Fase5Types.ts:157-164` y consumo en `Fase5TheoryModal.tsx:282-398`):
```ts
{
  enunciado?: string;   // o "pregunta" (legado) — puede contener HTML embebido, incl. <svg>
  pasos?: Array<{ orden: number; texto: string }>;  // opcional: si un paso contiene "= ?", se renderiza como input numérico
  respuesta: string;
  feedback_acierto: string;
  feedback_error: string;
}
```
Importante: el campo que hoy usan los 39 interactivos es `"pregunta"` (legado, sin `pasos`), lo cual dispara la rama `!int.pasos` en `Fase5TheoryModal.tsx:364-386` (un solo input de texto genérico). El campo `pregunta` **sí admite HTML/SVG embebido** (así lo demuestran los 3 interactivos de M1 Nivel 1 en `seed.py:82-115`) — por eso la solución no requiere cambios de frontend, solo agregar el SVG al string de `"pregunta"` en los 36 interactivos restantes.

---

## 3. Problemas encontrados (con evidencia)

### Problema 1 — 36/39 interactivos sin figura (CRÍTICO, el reportado por el usuario)

- **Evidencia:** `LogicaMath/backend/app/fase5/seed.py`, función `seed_teoria_niveles()`, líneas 68-277. Cada nivel define una lista `interactivos` de 3 (o en algunos casos más) ejercicios. Solo el Módulo 1 / Nivel 1 (líneas 80-116) incluye `<svg>` en el campo `"pregunta"`. Los otros 12 niveles (líneas 125-129, 138-142, 152-156, 165-169, 178-182, 192-196, 205-209, 218-222, 231-235, 245-249, 258-262, 271-275) son texto plano.
- **Impacto UX:** el alumno ve figura en "Ejemplos guiados" y luego pierde el apoyo visual justo cuando debe practicar solo. Rompe el andamiaje pedagógico (scaffolding) que la propia app promete (ver `docs/DISENO DE FASES/fase5.md`, sección de feedback pedagógico).
- **Causa raíz:** `svg_helpers.py` fue construido (8 funciones, 252 líneas) pero nunca conectado — 0 imports en todo el repo (`grep -r "svg_helpers" --include=*.py` → sin resultados fuera del propio archivo).

### Problema 2 — Inconsistencia de tema visual (oscuro vs. claro)

- **Evidencia:**
  - `theory_examples.py` (Ejemplos guiados): fondo `#111827` (oscuro), texto `#FFF`, acentos `#A855F7` / `#EC4899` / `#10B981`.
  - `svg_helpers.py` (`_svg_container`, líneas 29-42): también fondo oscuro `#111827`, coherente con lo anterior.
  - `seed.py` (SVGs inline de preguntas de práctica, ej. líneas 461-469, 495-502, 783-791, etc.) y `graphics_generator.py` (PNG con `Image.new("RGBA", ..., (255,255,255,255))`, fondo **blanco**): tema claro.
- **Impacto:** el alumno pasa de pantallas oscuras (teoría) a pantallas blancas (práctica) dentro del mismo flujo de aprendizaje — inconsistencia de marca y carga cognitiva innecesaria.

### Problema 3 — Error geométrico/terminológico: "estrella" que es un pentágono irregular

- **Evidencia:** `theory_examples.py:108-121` (Módulo 1, Nivel 2, ejemplo 3). Enunciado: *"Una estrella geométrica tiene 5 lados iguales y cada uno mide 1 cm"*. El SVG (`polygon points='70,15 110,45 95,90 45,90 30,45'`) dibuja un **pentágono irregular** (los lados NO son visualmente iguales, y no tiene puntas de estrella). Contradice el propio enunciado.
- **Impacto:** enseña una figura incorrectamente etiquetada; puede confundir al alumno sobre qué es una estrella geométrica vs. un pentágono.

### Problema 4 — Mezcla de unidades ("unidades" narrativas vs. "cm" en la figura)

- **Evidencia:** `seed.py:406-410` — las plantillas de enunciado narrativo dicen *"los lados miden {a} y {b} {unidad}"* donde `unidad` es aleatorio (cm/m), pero en `theory_examples.py` (Módulo 1 Nivel 1) los ejemplos guiados dicen *"lados de 3 y 4 unidades"* en el enunciado y luego el SVG rotula "3 cm" / "4 cm" — es decir, el mismo concepto se nombra "unidades" (abstracto) en un lugar y "cm" (concreto) en otro, sin que quede claro para el niño si son sinónimos.
- **Impacto:** menor, pero genera fricción de comprensión en los niveles iniciales (justamente donde se construye la base conceptual).

### Problema 5 — Tipografía demasiado pequeña en varias figuras

- **Evidencia:** `theory_examples.py` M1L2 (font-size 11, líneas 79-84, 96-99, 111-115, 127-130), M3 casi todas las figuras (font-size 8-9, líneas 411-412, 442-443, 456-457, 531-532, 545-546, 571-572), M4L1 (font-size 8, líneas 673-679). En una pantalla infantil a resolución típica (1280×800 o superior), 8-11px de font-size en un SVG con `viewBox` pequeño es prácticamente ilegible sin zoom.
- **Impacto:** accesibilidad/legibilidad para el público objetivo (niños).

### Problema 6 — Imágenes de rejilla sin cotas (dimension labels)

- **Evidencia:** `seed.py` múltiples llamadas a `generate_grid_shape_image(vertices, grid_size=..., fill_color=..., outline_color=...)` (ej. líneas 397-399, 610-613) **sin pasar el parámetro `labels`**. La función (`graphics_generator.py:333-393`) soporta `labels` para dibujar cotas con `_draw_dimension_line`, pero como nunca se pasa, las imágenes de rejilla solo muestran la leyenda genérica "Área = 1 u² / Cuadrado escala" (líneas 385-388) sin medidas explícitas de la figura.
- **Impacto:** en preguntas de **perímetro** que usan la variante `"grid"`, el alumno ve una figura en cuadrícula pero sin poder leer las medidas de los lados directamente en la imagen — debe inferirlas contando celdas, lo cual es válido pedagógicamente para *conteo* pero no para los enunciados que piden "observa los lados marcados".

### Problema 7 — Pitágoras exigido en la práctica sin enseñarse en la teoría (M4 Nivel 2)

- **Evidencia:** `seed.py:1105-1136` (`_gen_fase5_pool_raw`, módulo 4 nivel 2, caso 4) genera preguntas usando ternas pitagóricas (3,4,5 / 6,8,10 / 5,12,13) exigiendo calcular la diagonal vía `a² + b² = c²`. Sin embargo, `texto_descubrimiento` de M4 Nivel 2 (`seed.py:253-263`) y los 4 ejemplos guiados correspondientes (`theory_examples.py:729-786`) **solo explican que "la diagonal es la medida más larga"**, sin mencionar el teorema de Pitágoras ni mostrar un ejemplo numérico resuelto con la fórmula.
- **Impacto:** el alumno puede recibir en práctica una pregunta que requiere una fórmula (Pitágoras) que la teoría del mismo nivel nunca introdujo — salto pedagógico no cubierto.

### Problema 8 — Diccionario pedagógico muy escueto (1 término por nivel)

- **Evidencia:** los 13 niveles en `seed.py` (`seed_teoria_niveles`) definen `"diccionario"` con **exactamente 1 entrada** cada uno (excepto M1L3 y M4L3 que tienen 2). Ejemplo: M1L1 solo define `"Perímetro"`; no define "Borde", "Contorno", "Lado" ni "Arista" pese a que estos términos aparecen en el texto y en las preguntas.
- **Impacto:** el "Diccionario del Nivel" (sección visible en `Fase5TheoryModal.tsx:214-226`) queda subutilizado como herramienta de refuerzo léxico.

### Problema 9 — Fuga de almacenamiento en MinIO en cada re-siembra (hallazgo de infraestructura)

- **Evidencia:** `seed.py`, función `clear_fase5_data()` (líneas 44-66), purga **únicamente filas de PostgreSQL** (`Pregunta`, `Alternativa`, `Intento`, etc.) mediante `DELETE FROM ...`. En ningún punto se leen las URLs de imágenes (`datos_numericos.url`) de las preguntas que se van a borrar para invocar `storage_service.delete_file(url)` (definido y funcional en `app/core/storage.py:144-208`). Cada vez que se sube la versión de seed (`SEED_VERSIONS["fase_5"]`) y se re-siembra, **se generan nuevas imágenes en MinIO con nuevos nombres (UUID)**, pero las imágenes de la siembra anterior **quedan huérfanas en el bucket** (`logicakids` en local), ya que solo el registro en Postgres que apuntaba a ellas fue borrado.
- **Impacto:** crecimiento indefinido del bucket MinIO local (y de producción) con archivos ya no referenciados por ninguna fila de la BD. No rompe la app, pero es deuda técnica de almacenamiento que conviene corregir junto con esta ronda de mejoras, ya que el plan de trabajo (Problema 1-2) implica **al menos una re-siembra completa** de Fase 5.

---

## 4. Soluciones propuestas (detalladas, con código)

### Solución 1 — Conectar `svg_helpers.py` a los 36 interactivos sin figura

**Paso A. Import en `seed.py`:**
```python
from app.fase5.svg_helpers import (
    svg_rect, svg_square, svg_triangle_equilateral,
    svg_rect_all_labels, svg_l_shape, svg_polygon_labeled,
    svg_shaded_rect,
)
```

**Paso B. Por cada interactivo, generar el SVG correspondiente y concatenarlo al campo `"pregunta"` con `<br/>` como separador** (mismo patrón que ya usan los 3 interactivos de M1L1, `seed.py:82-115`).

Ejemplo concreto — Módulo 1, Nivel 2 (Suma de magnitudes), interactivo 1 (`seed.py:126`, hoy):
```python
{"pregunta": "Una figura tiene cuatro lados que miden: 2 cm, 3 cm, 2 cm y 3 cm. Perímetro:", "respuesta": "10", ...}
```
Propuesta (usando `svg_rect_all_labels`, que ya dibuja las 4 etiquetas por fuera — exactamente lo que este ejercicio necesita):
```python
{
    "pregunta": (
        "Una figura tiene cuatro lados que miden: 2 cm, 3 cm, 2 cm y 3 cm. Perímetro:<br/>"
        + svg_rect_all_labels(3, 2, unit="cm", border="#F59E0B")
    ),
    "respuesta": "10",
    "feedback_acierto": "¡Correcto!",
    "feedback_error": "Suma: 2+3+2+3."
}
```
> Nota: `svg_rect_all_labels(w_u, h_u, ...)` rotula "arriba/abajo" con `w_u` y "izquierda/derecha" con `h_u` — ambas veces el mismo valor por lado paralelo (igual que un rectángulo real). Para esta pregunta con lados 2-3-2-3, basta `svg_rect_all_labels(3, 2, ...)`.

**Patrón de asignación función → tipo de ejercicio** (ver detalle completo en Apéndice A):

| Módulo.Nivel | Función `svg_helpers` recomendada | Justificación |
|---|---|---|
| M1.L2 (suma magnitudes) | `svg_rect_all_labels` / `svg_polygon_labeled` | Necesita ver todos los lados rotulados, no solo 2 |
| M1.L3 (conversión lineal) | `svg_rect` (con doble unidad en texto, no en la figura) | Figura simple; la conversión es aritmética, no geométrica |
| M2.L1 (área confinada) | `svg_shaded_rect` | Ya calcula y muestra `w×h=área` dentro de la figura |
| M2.L2 (fusión triangular) | Nueva mini-función `svg_grid_half_units` (ver Solución 1-C) | `svg_helpers` no tiene aún un constructor de "enteros + mitades"; hay que añadirlo |
| M2.L3 (estimación irregular) | Reutilizar `generate_irregular_grid_shape_image` (ya existe, vía PNG) o extender `svg_helpers` con grid irregular | Mismo patrón que preguntas de práctica |
| M3.L1 (descomposición) | `svg_l_shape` | Ya construida específicamente para figuras en L |
| M3.L2 (Tangram/conservación) | `svg_polygon_labeled` con 2 figuras lado a lado | Conservación de área: mostrar "antes" y "después" |
| M3.L3 (áreas sombreadas) | `svg_shaded_rect` + rectángulo interior sin relleno (hueco) | Necesita extenderse: agregar parámetro de "hueco interior" |
| M3.L4 (simetría) | `svg_polygon_labeled` + líneas discontinuas de eje | Reutilizar el patrón ya usado en preguntas de práctica (`seed.py:812-822`, `figs_data`) |
| M4.L1 (escala gráfica) | Nueva mini-función de "barra de escala" (ver Solución 1-C) | No existe aún en `svg_helpers` |
| M4.L2 (diagonal/Pitágoras) | `svg_rect` + línea diagonal (extender función o nueva `svg_rect_diagonal`) | Necesario para visualizar la hipotenusa |
| M4.L3 (conversión m²↔cm²) | `svg_rect_all_labels` con doble anotación (u1 y u2) | Mostrar el cuadrado de 1 unidad y su equivalencia |

**Paso C. Extender `svg_helpers.py` con 3 funciones nuevas** (no existen aún, se necesitan para cubrir M2.L2, M4.L1, M4.L2):

```python
# --- Añadir a svg_helpers.py ---

def svg_grid_halves(enteros: int, mitades: int, unit="cm", border="#3B82F6") -> str:
    """Rejilla con cuadrados enteros (rect) + triángulos mitad, para M2.L2 (fusión de sectores)."""
    cols = min(enteros + mitades, 6)
    cell = _INNER / cols if cols else _INNER
    # ... (dibuja `enteros` rects + `mitades` polygons triangulares en grid,
    #      reutilizando el mismo patrón ya usado en seed.py líneas 644-678, pero
    #      centralizado aquí para no duplicar código entre teoría e interactivos)
    ...
    return _svg_container(shape, border_color=border)


def svg_scale_bar(u_val: int, scale: int, unit="cm", border="#F59E0B") -> str:
    """Barra de escala gráfica tipo mapa, para M4.L1."""
    ...
    return _svg_container(shape, border_color=border)


def svg_rect_diagonal(w_u: int, h_u: int, diag_label: str = "?", unit="cm", border="#EC4899") -> str:
    """Rectángulo con diagonal resaltada (para enseñar/practicar Pitágoras), para M4.L2."""
    ...
    return _svg_container(shape, border_color=border)
```

> **Nota de implementación:** el cuerpo exacto de estas 3 funciones debe seguir el mismo patrón geométrico (escalado a `_INNER`, centrado en `_W/_H`, etiquetas con `_lbl`/`_lbl_rot`) que las funciones existentes en `svg_helpers.py:70-252`. Se recomienda copiar el bloque SVG ya usado en `seed.py` para preguntas de práctica equivalentes (M2 fusión: líneas 644-678; M4 escala: líneas 1047-1061; M4 diagonal/Pitágoras: líneas 1111-1122) y refactorizarlo como función reutilizable, en vez de escribir SVG desde cero. Esto además **elimina duplicación de código** entre `seed.py` (preguntas de práctica) y los nuevos interactivos de teoría.

### Solución 2 — Unificar tema visual (adoptar tema oscuro de `svg_helpers.py` en todo)

- **Backend (preguntas de práctica):** en `graphics_generator.py`, cambiar la paleta por defecto de `generate_clean_shape_image`, `generate_grid_shape_image`, `generate_irregular_grid_shape_image`, `generate_rectilinear_shape_image` de fondo blanco (`(255,255,255,255)`) a fondo oscuro (`(17,24,39,255)` = `#111827`, igual que `svg_helpers.py`), con `outline_color` por defecto en blanco/gris claro en vez de negro.
- **Backend (SVG inline en `seed.py`):** todos los `<svg ... style='...background:#FFFFFF...'>` (hay ~15 ocurrencias, ej. líneas 461-469, 495-502, 514-521, 533-540, 783-791, 897-903, 931-941, 1010-1018, 1049-1061, 1081-1088, etc.) deben migrar a `background:#111827` y `stroke='#FFFFFF'`/texto blanco, en vez de `#1E293B` sobre blanco.
- **Recomendación de implementación:** dado el volumen (~15 bloques SVG inline + 4 funciones de generación PNG), conviene:
  1. Definir una única paleta en un módulo compartido, p.ej. `app/fase5/theme.py`:
     ```python
     FASE5_BG = "#111827"
     FASE5_GRID = "#374151"
     FASE5_TEXT = "#FFFFFF"
     FASE5_SCALE_LABEL = "#94A3B8"
     ```
  2. Reemplazar los literales de color hardcodeados en `seed.py` y `graphics_generator.py` por estas constantes.
  3. Esto es **más invasivo** que la Solución 1 — se recomienda hacerlo en una segunda pasada, después de validar que la Solución 1 (figuras en interactivos) funciona correctamente.

### Solución 3 — Corregir la "estrella" de M1.L2 ejemplo 3

**Archivo:** `theory_examples.py:108-121`. Dos alternativas:

- **Opción A (recomendada, mínimo esfuerzo):** cambiar el enunciado para que coincida con la figura real: *"Un pentágono irregular tiene 5 lados y cada uno mide 1 cm"* (eliminar la palabra "estrella" y "iguales" ya que el polígono dibujado no es regular).
- **Opción B (más trabajo, más correcto pedagógicamente):** redibujar el SVG como una **estrella de 5 puntas real** (polígono estrellado, 10 vértices alternando radio externo/interno) para que coincida con el enunciado original. Usar esta fórmula para los 10 puntos:
  ```python
  import math
  def star_points(cx, cy, r_out, r_in, n=5):
      points = []
      for i in range(n * 2):
          r = r_out if i % 2 == 0 else r_in
          angle = math.pi / n * i - math.pi / 2
          points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
      return points
  ```
  Se recomienda la **Opción A** por ser más rápida y no introducir un nuevo tipo de figura (estrella de 5 puntas) que no se reutiliza en ningún otro lugar de la fase.

### Solución 4 — Unificar "unidades" vs "cm"

- **Regla propuesta:** en los **Ejemplos guiados de M1.L1** (los únicos que usan la palabra "unidades" de forma abstracta), cambiar el enunciado para incluir la unidad concreta desde el inicio, ya que la figura siempre la muestra. Ejemplo (`theory_examples.py:25`):
  - Antes: `"Un rectángulo tiene lados de 3 y 4 unidades. ¿Cuál es su perímetro?"`
  - Después: `"Un rectángulo tiene lados de 3 cm y 4 cm. ¿Cuál es su perímetro en cm?"`
- Aplicar el mismo criterio a los 4 ejemplos de M1.L1 (líneas 11-72) y a los interactivos de M1.L1 (líneas 82-115), que ya tienen esta inconsistencia parcial.

### Solución 5 — Aumentar tipografía mínima

- **Regla propuesta:** establecer `font-size` mínimo de **16px** para etiquetas de medida y **13px** para texto secundario/leyenda, en todos los SVG de Fase 5 (tanto `theory_examples.py` como los inline de `seed.py`).
- Archivos/líneas a corregir (buscar `font-size='8'`, `font-size='9'`, `font-size='10'`, `font-size='11'` y subir a 16 mínimo):
  - `theory_examples.py`: líneas 79-84 (M1L2), 96-99, 111-115 (M1L2), 411-412, 442-443, 456-457 (M3L1), 487-488 (M3L2), 531-532, 545-546 (M3L3), 673-679, 697-701 (M4L1).
  - `seed.py`: líneas 673-679, 697-701 (barras de escala M4L1, font-size 8).
- **Método recomendado:** grep-replace controlado, verificando visualmente cada cambio porque algunos `viewBox` son pequeños y podrían requerir también agrandar el `viewBox` para que el texto más grande no se salga del contenedor.

### Solución 6 — Agregar cotas a imágenes de rejilla

- **Archivo:** `graphics_generator.py`, función `generate_grid_shape_image` (líneas 333-393) — **ya soporta** el parámetro `labels` (línea 333, 376-378), solo falta que los llamadores en `seed.py` lo usen.
- **Cambio en `seed.py`:** en las llamadas a `generate_grid_shape_image(vertices, grid_size=..., fill_color=..., outline_color=...)` (variante `"grid"` de M1.L1 y M2.L1, líneas ~397 y ~610), agregar el diccionario `labels`:
  ```python
  vertices = [(1, 1), (1 + a, 1), (1 + a, 1 + b), (1, 1 + b)]
  labels = {
      (0, 1): f"{a} m",   # lado superior (vértice 0 -> 1)
      (1, 2): f"{b} m",   # lado derecho (vértice 1 -> 2)
  }
  img_bytes = generate_grid_shape_image(vertices, grid_size=(...), fill_color=..., outline_color=..., labels=labels)
  ```
  > La clave de `labels` es una tupla `(idx_vertice_origen, idx_vertice_destino)` según el orden de `vertices` (ver `graphics_generator.py:371-378`). Solo hace falta rotular 2 lados (los no-paralelos) ya que en un rectángulo los opuestos miden igual.
- **Importante:** como esto cambia el contenido visual de las imágenes, **hay que incrementar el sufijo de versión en el nombre de archivo** (ej. `f"grid_p_{a}_{b}_v2.png"` → `"_v3.png"`) para evitar servir desde caché del navegador o CDN una imagen vieja con la misma URL lógica pero distinto contenido esperado. Ver sección 6.2.

### Solución 7 — Enseñar Pitágoras antes de exigirlo (M4.L2)

- **Archivo:** `seed.py`, función `seed_teoria_niveles()`, entrada `{"modulo_id": 4, "nivel_id": 2, ...}` (líneas 251-263).
- **Cambio propuesto en `texto_descubrimiento`:** añadir un párrafo con la fórmula y un ejemplo numérico resuelto:
  ```python
  "texto_descubrimiento": (
      "Cuando compramos una pantalla de televisión, de celular o tablet, nos dicen su tamaño en pulgadas... "
      "¡Pero esa medida no es el ancho ni el alto! El tamaño de las pantallas siempre se mide en línea recta "
      "cruzando desde una esquina hasta la esquina contraria. ¡Eso es la diagonal!\n"
      "¿Sabías que existe una fórmula mágica para calcular la diagonal sin medirla directamente? "
      "Se llama el Teorema de Pitágoras: si conocemos la base y la altura de un rectángulo, "
      "la diagonal al cuadrado es igual a la suma de la base al cuadrado más la altura al cuadrado "
      "(diagonal² = base² + altura²). Por ejemplo, si la base mide 3 y la altura mide 4: "
      "3² + 4² = 9 + 16 = 25, y la raíz cuadrada de 25 es 5. ¡La diagonal mide 5!"
  ),
  ```
- **Agregar un 5.° ejemplo guiado** en `theory_examples.py` bajo la clave `(4, 2)` que resuelva paso a paso un caso de Pitágoras completo (ya existe uno similar en la práctica, `seed.py:1105-1136` — reutilizar la misma terna 3-4-5 con figura `svg_rect_diagonal` de la Solución 1-C).
- **Agregar término al diccionario:** `"Teorema de Pitágoras": "En un triángulo rectángulo, el cuadrado de la hipotenusa (lado más largo) es igual a la suma de los cuadrados de los otros dos lados."`

### Solución 8 — Ampliar diccionario pedagógico (2-3 términos por nivel)

Propuesta concreta de términos adicionales por nivel (a agregar en el `"diccionario"` de cada entrada de `seed_teoria_niveles()`):

| Nivel | Términos actuales | Términos a agregar |
|---|---|---|
| M1.L1 | Perímetro | + "Lado", "Contorno" |
| M1.L2 | Lado (Arista) | + "Polígono", "Cuadrilátero" |
| M1.L3 | 1 m, 1 km | + "Unidad de longitud", "Escalera de conversión" |
| M2.L1 | Área | + "Unidad cuadrada", "Base y altura" |
| M2.L2 | Fusión de áreas | + "Diagonal de un cuadrado", "Triángulo rectángulo" |
| M2.L3 | Área irregular | + "Aproximación", "Estimación" |
| M3.L1 | Descomponer | + "Figura compuesta", "Superposición" |
| M3.L2 | Conservación del área | + "Tangram", "Congruencia" |
| M3.L3 | Resta geométrica | + "Área sombreada", "Figura hueca" |
| M3.L4 | Eje de simetría | + "Simetría axial", "Reflejo/Espejo" |
| M4.L1 | Escala gráfica | + "Distancia real", "Proporción" |
| M4.L2 | Diagonal | + "Teorema de Pitágoras" (ver Solución 7), "Hipotenusa" |
| M4.L3 | Metro cuadrado (m²) | + "Centímetro cuadrado (cm²)", "Decímetro cuadrado (dm²)" |

### Solución 9 — Corregir la fuga de almacenamiento en MinIO

**Archivo:** `seed.py`, función `clear_fase5_data()` (líneas 44-66).

**Cambio propuesto:** antes de borrar las filas de `Pregunta`, recolectar las URLs de imágenes referenciadas en `datos_numericos.url` y llamar a `storage_service.delete_file()` para cada una:

```python
from app.core.storage import storage_service

async def clear_fase5_data(session: AsyncSession):
    print("Purging existing Fase 5 data for a clean overwrite...")
    result = await session.execute(select(Pregunta.id, Pregunta.datos_numericos).where(Pregunta.fase_id == FASE5_ID))
    rows = result.all()
    pregunta_ids_list = [r[0] for r in rows]

    # --- NUEVO: limpiar imágenes huérfanas en MinIO antes de borrar las filas ---
    urls_a_borrar = [
        r[1]["url"] for r in rows
        if r[1] and isinstance(r[1], dict) and r[1].get("url")
    ]
    for url in urls_a_borrar:
        await storage_service.delete_file(url)
    print(f"MinIO: {len(urls_a_borrar)} imágenes huérfanas eliminadas antes de re-sembrar.")
    # --- fin bloque nuevo ---

    if pregunta_ids_list:
        await session.execute(delete(Alternativa).where(Alternativa.pregunta_id.in_(pregunta_ids_list)))
        ... # (resto del código sin cambios)
```

> **Nota de rendimiento:** `storage_service.delete_file()` es async pero internamente usa `asyncio.to_thread` para la llamada boto3 síncrona — con ~1600 preguntas sembradas (120 × 13 niveles + 30 × 3 desafíos × 4 módulos), esto puede tardar varios segundos extra en el re-seed. Es aceptable para un proceso de siembra (no es una ruta caliente de producción), pero conviene loguear progreso si se quiere prolijidad.
>
> **Nota de alcance:** esta fuga existe también potencialmente en otras fases con generación de imágenes (fase 1, 2, etc., si usan el mismo patrón) — **este documento se limita a Fase 5** por ser el foco del pedido, pero vale la pena señalarlo como hallazgo transversal para una futura revisión.

---

## 5. Impacto y consideraciones de Base de Datos

### 5.1 Naturaleza de los "datos" de Fase 5

A diferencia de otras fases (3-8) que usan un archivo estático de frontend (`faseMetadata.ts`), **Fase 5 es 100% dinámica desde PostgreSQL**: tanto la teoría (`niveles_teoria_pool`) como las preguntas (`preguntas`, `alternativas`) se generan por código Python (`seed.py`) y se insertan en la base de datos. **No existen archivos JSON de contenido editables directamente** — todo pasa por re-ejecutar el script de siembra.

### 5.2 Mecanismo de versión de seed (`SEED_VERSIONS`)

Ubicado en `LogicaMath/backend/app/seed.py:27-38`:
```python
SEED_VERSIONS = {
    ...
    "fase_5": "20260720_v6",
    ...
}
```

`should_seed_phase(session, "fase_5", 5)` (línea 702) compara esta versión contra el valor guardado en la tabla `platform_settings` (clave `database_seed_versions`). **Si coinciden, el re-seed se salta silenciosamente** (no hace nada). Por lo tanto:

> **Regla obligatoria:** cualquier cambio de contenido en `seed.py`/`theory_examples.py`/`svg_helpers.py` para Fase 5 **debe ir acompañado de subir el string de versión**, p. ej. `"fase_5": "20260722_v7"`, o el cambio nunca se aplicará a la base de datos aunque el código esté correcto.

### 5.3 Qué se borra al re-sembrar (`clear_fase5_data`)

`clear_fase5_data()` (`seed.py:44-66`) borra, en cascada, **todos los datos de alumnos relacionados con Fase 5**:
- `Alternativa` (de preguntas de Fase 5)
- `IntentoPaso` / `IntentoPregunta` (de preguntas de Fase 5, incluye Módulo 4 Constructor)
- `Intento` (todos los intentos de alumnos en Fase 5)
- `PoolAsignadoAlumno` (asignaciones de pool por alumno)
- `Pregunta` (todo el banco de preguntas de Fase 5)
- `ConfiguracionProgreso` (configuración de niveles/desafíos)
- `NivelTeoria` (teoría/interactivos de Fase 5)

**Esto significa que el progreso de cualquier alumno de prueba en Fase 5 se pierde en cada re-seed.** Es aceptable en el entorno **local** de desarrollo (datos de prueba), pero **jamás debe ejecutarse contra producción** sin coordinación explícita y aviso — ver sección 9.

### 5.4 Cómo ejecutar el re-seed en local

**Opción A — automático al levantar el backend:** el backend local llama a la rutina de seeding general al arrancar (revisar `main.py` / evento de `startup` — no incluido en el análisis de este documento, pero es el patrón estándar de la app). Si `docker compose -f docker-compose.local.yml up -d --build` reinicia el contenedor `backend` después de subir la versión en `SEED_VERSIONS`, el seed de Fase 5 correrá automáticamente.

**Opción B — manual, dentro del contenedor backend:**
```bash
docker exec -it logicakids_local_backend python -m app.fase5.seed
```
(`seed.py` tiene `if __name__ == "__main__": asyncio.run(run_fase5_seed())` en la línea 1369-1370). Nota: `run_fase5_seed()` (línea 1346) también llama internamente a `should_seed_phase`, así que **igual requiere haber subido la versión primero**, o no hará nada.

### 5.5 Índices y consultas relevantes que no deben romperse

`Pregunta` tiene índices GIN sobre `datos_numericos`, `errores_previstos`, `palabras_clave` (`app/models/pregunta.py:107-116`). Los cambios propuestos en este documento **solo agregan claves nuevas a estos JSONB** (p. ej. `labels` para cotas, nuevos campos en `errores_previstos`), no cambian su tipo ni estructura raíz — no se requieren migraciones de Alembic ni cambios de índice.

---

## 6. Impacto y consideraciones de MinIO / Storage

### 6.1 Cómo funciona hoy

`StorageService` (`app/core/storage.py`) es **tolerante a fallos**: intenta subir a MinIO (S3-compatible) vía `boto3`; si falla (`ClientError`, `EndpointConnectionError`) o no está configurado, cae automáticamente a filesystem local (`app/static/graphics/`, servido como archivos estáticos por FastAPI). Esto significa que **incluso sin MinIO corriendo, el seed de Fase 5 no falla** — las imágenes simplemente se guardan en disco dentro del contenedor backend.

### 6.2 Entorno local — configuración exacta

De `Datos_localhost/docker-compose.local.yml`:
- MinIO API: `localhost:9100` (dentro de la red docker: `http://minio:9000`)
- Consola web MinIO: `localhost:9101` (usuario `logicakids_minio_admin`, contraseña en el compose)
- Bucket auto-creado por el servicio `minio-setup`: **`logicakids`**, con política `anonymous set download` (lectura pública, escritura solo autenticada) — esto permite que las URLs de imágenes generadas sean accesibles directamente por el frontend sin autenticación.
- Las variables `S3_ACCESS_KEY`, `S3_SECRET_KEY`, `S3_ENDPOINT_URL`, `S3_BUCKET_NAME`, `S3_PUBLIC_URL` deben estar seteadas en `.env.local` (no versionado, solo lectura para el agente) apuntando a este stack local.

### 6.3 Caché en memoria de URLs durante el seed

`seed.py` mantiene un diccionario `_graphic_url_cache: Dict[str, str] = {}` (línea 42) que evita regenerar/resubir la misma imagen si ya se generó en la misma corrida de seed (basado en una `cache_key` que codifica dimensiones + unidad). **Este caché es solo en memoria del proceso** — no persiste entre corridas. Cada re-seed completo genera un set completamente nuevo de imágenes con nuevos UUIDs (ver `storage_service.upload_question_graphic`, que siempre genera `uuid.uuid4().hex`), de ahí la fuga descrita en el Problema 9 / Solución 9.

### 6.4 Convención de versión en nombre de archivo

Se observa un patrón manual en `seed.py` donde el nombre lógico del archivo lleva un sufijo de versión (`_v2.png`, `_v3.png`) que el desarrollador incrementa manualmente cuando cambia la lógica de generación de una imagen (ver p. ej. `f"clean_p_{a}_{b}_v2.png"` en línea 390). **Esto es una convención de cache-busting manual**, no automática. Quien implemente la Solución 6 (cotas en imágenes de rejilla) o la Solución 2 (tema oscuro) **debe recordar incrementar estos sufijos** en cada `cache_key`/nombre de archivo modificado, para que el cambio visual se refleje (de lo contrario, si por alguna razón el bucket ya tuviera una imagen con esa clave — poco probable dado que el UUID siempre es nuevo, pero el *filename lógico* pasado a `upload_question_graphic` sí se reutiliza como parte del path informativo — conviene mantener la convención existente).

### 6.5 Recomendación arquitectónica: NO usar MinIO para las figuras de los Interactivos

Para la **Solución 1** (figuras en interactivos de teoría), se recomienda explícitamente **usar SVG inline** (vía `svg_helpers.py`, como ya hacen los Ejemplos guiados) y **no** generar PNG vía `graphics_generator.py` + subida a MinIO. Razones:
1. **Consistencia:** los 52 Ejemplos guiados ya son 100% SVG inline — mantener el mismo patrón para los interactivos evita mezclar dos tecnologías de renderizado dentro de la misma pantalla de teoría.
2. **Costo cero de almacenamiento:** SVG inline vive dentro del JSONB de `NivelTeoria` (13 filas, tamaño despreciable) — no genera objetos nuevos en MinIO, no contribuye a la fuga del Problema 9, no depende de que MinIO esté disponible/accesible.
3. **Rendimiento:** sin round-trip de red para cargar una imagen — el SVG se renderiza inmediatamente como parte del HTML ya entregado por la API.
4. **Theming:** un SVG inline puede heredar `currentColor` / clases CSS del frontend si se desea evolucionar el tema más adelante; un PNG generado en el backend queda "congelado" con los colores que tenía al momento de generarse.

MinIO sigue siendo **necesario y correcto** para las preguntas de **práctica libre y desafíos** (pool de 120+30×3×4 preguntas por módulo), donde la generación paramétrica de imágenes con Pillow (`graphics_generator.py`) es la única forma práctica de tener miles de variantes únicas sin explotar el tamaño del JSONB con SVG repetido. Ahí sí aplican las Soluciones 2 (tema) y 6 (cotas) y la corrección de fuga (Solución 9).

---

## 7. Plan de implementación paso a paso

> Orden recomendado: de menor a mayor riesgo/alcance, con checkpoints de verificación entre pasos.

### Fase A — Preparación (no toca contenido aún)
1. Confirmar que el stack local está arriba: `docker compose -f Datos_localhost/docker-compose.local.yml ps` (postgres, redis, minio, minio-setup, backend, frontend healthy).
2. Backup opcional de la BD local antes de empezar (por si se quiere comparar antes/después): `docker exec logicakids_local_db pg_dump -U logicakids_local_user logicakids_local > backup_pre_fase5_mejoras.sql`.

### Fase B — Solución 9 primero (evitar agravar la fuga de MinIO con los próximos re-seeds)
3. Implementar la limpieza de MinIO en `clear_fase5_data()` (Solución 9).
4. **No subir versión de seed todavía** — este cambio no altera contenido, solo higiene de storage; se probará junto con el primer re-seed real del paso 6.

### Fase C — Solución 1 (figura en los 36 interactivos) — PRIORIDAD 1
5. Extender `svg_helpers.py` con las 3 funciones nuevas (`svg_grid_halves`, `svg_scale_bar`, `svg_rect_diagonal`) — Solución 1-C.
6. Editar `seed.py` función `seed_teoria_niveles()`: agregar el import de `svg_helpers` y modificar los 36 interactivos (uno por uno, siguiendo el Apéndice A) para incluir `<br/>` + llamada a la función SVG correspondiente en el campo `"pregunta"`.
7. Aplicar también, de paso, las Soluciones 3, 4, 7 y 8 (correcciones de contenido) ya que se está editando el mismo bloque de código.
8. Subir versión: `SEED_VERSIONS["fase_5"] = "20260722_v7"` (o fecha real de implementación) en `app/seed.py`.
9. Re-sembrar: reiniciar el contenedor backend local (`docker compose -f docker-compose.local.yml restart backend`) o ejecutar manualmente `docker exec -it logicakids_local_backend python -m app.fase5.seed`.
10. **Checkpoint de verificación** (ver sección 8) antes de continuar.

### Fase D — Solución 6 (cotas en imágenes de rejilla) y Solución 5 (tipografía)
11. Editar `seed.py` (llamadas a `generate_grid_shape_image`) para pasar `labels`.
12. Incrementar sufijos de versión en los `cache_key`/nombres de archivo afectados (Solución 6.4).
13. Aumentar `font-size` en los bloques identificados en Solución 5 (`theory_examples.py` y `seed.py`).
14. Subir versión de seed nuevamente, re-sembrar, verificar.

### Fase E — Solución 2 (tema visual unificado) — mayor alcance, hacer al final
15. Crear `app/fase5/theme.py` con constantes de color.
16. Reemplazar paleta en `graphics_generator.py` (4 funciones de generación de imagen) y en los ~15 bloques SVG inline de `seed.py`.
17. Subir versión de seed, re-sembrar, verificar visualmente **todas** las pantallas de práctica (no solo teoría) para confirmar legibilidad sobre fondo oscuro.

### Fase F — Cierre
18. Ejecutar suite de tests existente (`fase5.test.ts` en frontend, y cualquier test de backend relacionado) para confirmar que no se rompió nada estructural.
19. Documentar en el changelog interno (si existe) o dejar nota en memoria del agente sobre la nueva versión de seed aplicada.

---

## 8. Plan de pruebas / validación

Para cada uno de los 13 niveles de Fase 5, después de re-sembrar:

1. **Vía API directa (rápido, sin UI):**
   ```bash
   curl http://localhost:8000/api/fase5/lectura/1/nivel/1
   ```
   Verificar que la respuesta JSON incluya, para cada elemento de `interactivos[]`, un campo `"pregunta"` que contenga la subcadena `<svg`.

2. **Vía navegador (validación visual real):**
   - Iniciar sesión como alumno de prueba en `http://localhost:3000`.
   - Navegar a Fase 5 → cada módulo → cada nivel → abrir la teoría → avanzar hasta el paso "¡Tu turno!" y confirmar que la figura se renderiza correctamente (sin overflow, sin `viewBox` roto, texto legible).
   - Confirmar que el `<svg>` no rompe el layout del contenedor `.f5-interactive-box` (revisar especialmente los niveles con figuras más grandes, como M3.L2 Tangram con 2 figuras lado a lado).

3. **Regresión de práctica libre:** entrar a un nivel de práctica libre (no teoría) y confirmar que las preguntas con imagen (`datos_numericos.tipo_visual === 'imagen'`) siguen cargando correctamente desde MinIO (`http://localhost:9100/logicakids/graphics/...`) — validar que la Solución 9 no rompió el flujo normal de subida.

4. **Validación de MinIO tras Solución 9:** antes y después de un re-seed, comparar el conteo de objetos en el bucket:
   ```bash
   docker exec logicakids_local_minio mc ls --recursive localminio/logicakids/graphics | wc -l
   ```
   Debería mantenerse estable (no crecer indefinidamente) tras sucesivos re-seeds, en vez de acumular imágenes huérfanas.

5. **Tests automatizados existentes:** correr `LogicaMath/frontend/components/fase5/fase5.test.ts` (Vitest) y cualquier test de Playwright relevante en `tests/*fase5*.spec.ts` si existen, para detectar regresiones de render.

---

## 9. Reglas y restricciones que debe respetar quien implemente

Estas reglas ya rigen el repositorio (ver memoria del proyecto) y aplican integralmente a este trabajo:

- **No hacer commit ni push automático** al repositorio remoto (`espalhardigital-hash/logicakids.git`) salvo pedido explícito y expreso del usuario en el momento.
- **Operar exclusivamente sobre la rama `desarrollo`**. Nunca tocar `main` (producción) sin pedido explícito.
- **Nunca ejecutar el re-seed de Fase 5 (`clear_fase5_data` + `run_fase5_seed`) contra la base de datos de Producción o Desarrollo remoto** — todo el trabajo de este documento asume el entorno **Local** (`Datos_localhost/`, Postgres puerto 5433, MinIO 9100/9101). Si en algún momento se requiere aplicar esto a Desarrollo o Producción, debe ser un paso explícito y coordinado aparte, avisando que **se perderá el progreso de todos los alumnos en Fase 5** en ese entorno.
- **Archivos `.env` son de solo lectura** — nunca escribir/modificar `.env`, `.env.local`, etc. Si hace falta un valor de configuración nuevo, preguntar al usuario o usar un `.env.local.example` de referencia sin tocar el real.
- **No hacer refactors preventivos** más allá de lo que estas soluciones requieren (p. ej., no reestructurar todas las fases para compartir código común "ya que estamos" — eso está fuera de alcance de este documento).
- Antes de dar por completada cualquier fase del plan (sección 7), **verificar visualmente en el navegador** (no solo que el código compile) — esta es una mejora de UX/contenido visual, y una regresión de layout solo se detecta mirando la pantalla renderizada.

---

## Apéndice A — Inventario completo de figuras faltantes por nivel

| # | Módulo.Nivel | Nombre del nivel | Interactivos sin figura | Función `svg_helpers` sugerida |
|---|---|---|---|---|
| 1 | M1.L1 | Conteo directo | 0 de 3 (✅ ya tiene) | — (ya resuelto, referencia de patrón) |
| 2 | M1.L2 | Suma de magnitudes | 3 de 3 | `svg_rect_all_labels`, `svg_polygon_labeled` (cuadrilátero irregular) |
| 3 | M1.L3 | Conversión lineal | 3 de 3 | `svg_rect` (simple, foco en conversión numérica) |
| 4 | M2.L1 | Conteo confinado (área) | 3 de 3 | `svg_shaded_rect` |
| 5 | M2.L2 | Fusión de sectores triangulares | 3 de 3 | `svg_grid_halves` (nueva) |
| 6 | M2.L3 | Estimación de áreas irregulares | 4 de 4 | `svg_grid_halves` (nueva) reutilizada a mayor escala |
| 7 | M3.L1 | Descomposición estructural | 3 de 3 | `svg_l_shape` |
| 8 | M3.L2 | Conservación de área (Tangram) | 4 de 4 | `svg_polygon_labeled` (par de figuras) |
| 9 | M3.L3 | Áreas sombreadas (resta geométrica) | 4 de 4 | `svg_shaded_rect` extendida con hueco interior |
| 10 | M3.L4 | Ejes de simetría | 4 de 4 | `svg_polygon_labeled` + líneas de eje (reutilizar `figs_data` de `seed.py:812-822`) |
| 11 | M4.L1 | Escala gráfica | 3 de 3 | `svg_scale_bar` (nueva) |
| 12 | M4.L2 | Diagonal / Pantallas (Pitágoras) | 3 de 3 | `svg_rect_diagonal` (nueva) |
| 13 | M4.L3 | Conversión de superficie (m²↔cm²) | 3 de 3 | `svg_rect_all_labels` con doble anotación de unidad |

**Total interactivos:** 39. **Con figura hoy:** 3. **A corregir:** 36.

---

## Apéndice B — Catálogo de funciones de `svg_helpers.py` listas para usar

Ubicación: `LogicaMath/backend/app/fase5/svg_helpers.py`. Todas devuelven un `str` con el `<svg>...</svg>` completo, ya envuelto en `_svg_container` (fondo oscuro, cuadrícula sutil, leyenda "1 cm").

| Función | Firma | Uso típico |
|---|---|---|
| `svg_rect` | `(w_u, h_u, unit="cm", border="#A855F7")` | Rectángulo simple, etiqueta arriba + derecha |
| `svg_square` | `(side_u, unit="cm", border="#A855F7")` | Cuadrado (llama a `svg_rect` con w=h) |
| `svg_triangle_equilateral` | `(side_u, unit="cm", border="#A855F7")` | Triángulo equilátero, 3 lados etiquetados |
| `svg_rect_all_labels` | `(w_u, h_u, unit="cm", border="#F59E0B")` | Rectángulo con las 4 etiquetas (arriba/abajo/izq/der) |
| `svg_l_shape` | `(w1_u, h1_u, w2_u, h2_u, unit="cm", border="#F59E0B")` | Figura en L con 3 etiquetas representativas |
| `svg_polygon_labeled` | `(points_unit, labels, unit="cm", border="#A855F7")` | Polígono arbitrario con etiquetas custom en puntos lógicos |
| `svg_shaded_rect` | `(w_u, h_u, unit="cm²", fill="#EC4899", border="#EC4899")` | Rectángulo relleno con `w×h=área` calculado dentro |

**Funciones nuevas a agregar (Solución 1-C):** `svg_grid_halves`, `svg_scale_bar`, `svg_rect_diagonal` — ver especificación de firma y propósito en la Solución 1-C de la sección 4.

---

*Fin del documento. Cualquier duda de implementación debe resolverse releyendo el archivo fuente citado (archivo + línea) antes de asumir comportamiento — este documento resume el estado del código al 2026-07-21, que puede haber cambiado desde entonces.*
