# Propuesta de Producto (PRD): Autocuración de Imágenes Faltantes (Fases 3-8)

## 📋 Contexto y Motivación
En el software educativo **LogicaKids Pro**, el aprendizaje visual es fundamental para el desarrollo del razonamiento espacial, la combinatoria y el análisis gráfico en niños de primaria. Las Fases 3 a 8 incluyen temas como lectura de la hora en relojes analógicos, plano cartesiano, conteo de áreas y combinatoria con dados y urnas de colores.

Actualmente, un análisis técnico reveló que de las 3,140 preguntas que requieren apoyo visual en estas fases, **595 preguntas carecen de su respectiva imagen** en el almacenamiento de MinIO o en la base de datos local. Esto interrumpe el flujo didáctico del alumno, mostrando marcadores de imágenes rotas en el frontend.

---

## 🎯 Objetivos de Producto
1. **Población al 100%**: Lograr que el 100% de las preguntas de matemáticas del banco (Fases 3-8) tengan un recurso visual asignado y accesible.
2. **Generación Automatizada e Inteligente**: Implementar un pipeline de autocuración que lea el enunciado, interprete el gráfico requerido y lo genere.
3. **Calidad Pedagógica Premium**: Asegurar que las imágenes procedimentales y con IA cumplan con un estilo limpio, claro, colorido y atractivo para niños.
4. **Resiliencia técnica**: Guardar las imágenes directamente en el bucket `logicakids` de MinIO, asignando las URLs correctas a cada registro de pregunta en PostgreSQL.

---

## 🛠️ Requerimientos del Producto (PRD)

### 1. Auditoría del Banco de Preguntas
* El sistema debe identificar heurísticamente cuáles preguntas requieren gráficos mediante análisis de palabras clave y fase.
* Debe cruzarse cada registro contra el storage S3 local para listar las imágenes faltantes.

### 2. Generación Procedimental de Precisión
* **Relojes Analógicos (Fase 3/7)**: Generar carátulas con números del 1 al 12, manecillas de hora y minuto posicionadas con exactitud trigonométrica basada en los datos de la pregunta.
* **Plano Cartesiano (Fase 5/6)**: Renderizar grillas numeradas, ejes X/Y marcados con flechas, coordenadas graficadas y polígonos/puntos resaltados de forma nítida.
* **Fracciones y Grillas de Área (Fase 4/6)**: Dibujar círculos segmentados (pizzas), barras de fracciones divididas y coloreadas proporcionalmente, y cuadrículas con áreas sombreadas.
* **Probabilidad y Combinatoria (Fase 8)**: Dibujar dados realistas mostrando las caras indicadas, y urnas transparentes conteniendo el número exacto y color de las esferas descritas en el enunciado.

### 3. Generación Conceptual por IA
* Para imágenes que requieren conceptos abstractos o ilustraciones conceptuales (ej. *"Observa el termómetro"* o escenarios con objetos cotidianos), el sistema utilizará **Gemini Imagen 3** para generar una ilustración a medida.

### 4. Actualización del Storage y Base de Datos
* Las imágenes generadas se subirán al S3 local de MinIO en formato PNG de alta resolución.
* La URL generada (`http://localhost:9000/logicakids/graphics/...`) se inyectará en la columna `datos_numericos` de la tabla `preguntas` en Postgres.

---

## 🧪 Criterios de Aceptación
1. El script de integridad física (`verify_minio_integrity.py`) debe reportar **0 imágenes faltantes** tras completar el proceso.
2. Cada imagen debe cargar correctamente en el simulador de administrador y en la vista de juego del estudiante sin distorsión o pixelado.
