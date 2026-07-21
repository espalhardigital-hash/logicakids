## 1. Expandir Diccionarios de Contexto

- [x] 1.1 Ampliar la lista `NOMBRES` de 8 a 25+ nombres infantiles diversos (incluir nombres de distintas culturas latinoamericanas)
- [x] 1.2 Ampliar la lista `OBJETOS_FRACC` de 5 a 15+ objetos fraccionables (agregar: pastel, sandía, tableta, hoja de papel, bandera, ventana, tablero, mosaico, etc.)
- [x] 1.3 Ampliar la lista `COLECCIONES` de 5 a 12+ colecciones (agregar: estrellas, canicas, pegatinas, libros, conchas, botones, etc.)
- [x] 1.4 Ampliar la lista `BEBIDAS` de 4 a 10+ bebidas (agregar: vasos de leche, tazas de chocolate, limonadas, batidos, copas de helado, etc.)
- [x] 1.5 Ampliar la lista `PINTURAS` de 6 a 12+ colores de pintura y la lista `COLORES` de 5 a 10+ adjetivos de color

### Test 1: Validar diccionarios expandidos
- [x] 1.T1 Escribir script de test que importe los diccionarios de `seed.py` y verifique: `len(NOMBRES) >= 25`, `len(OBJETOS_FRACC) >= 15`, `len(COLECCIONES) >= 12`, `len(BEBIDAS) >= 10`, `len(PINTURAS) >= 12`, `len(COLORES) >= 10`
- [x] 1.T2 Verificar que no haya duplicados en ninguna lista
- [x] 1.T3 Generar 50 preguntas de muestra y confirmar que la tasa de repetición de nombres en enunciados consecutivos sea < 15%

## 2. Corregir Variantes Espejo

- [x] 2.1 Eliminar el prefijo literal `[ESPEJO]` del enunciado (línea 692 de `seed.py`: `prefix = "[ESPEJO] " if es_espejo else ""`)
- [x] 2.2 Modificar la fórmula de semilla para variantes espejo (var > 0) usando un offset primo: `seed = base_seed + var * 7919` en lugar de la semilla idéntica actual
- [x] 2.3 Agregar transformaciones lógicas por módulo para las variantes espejo:
  - Módulo 1: var=1 invierte la pregunta (pedir fracción NO pintada), var=2 cambia forma geométrica, var=3 altera denominador
  - Módulo 2: var=1 cambia a complemento, var=2 cambia colección, var=3 escala total ×2
  - Módulo 3: var=1 alterna tipo de porcentaje, var=2 cambia a gráfico de barras, var=3 cambia a promedio
  - Módulo 4: var=1 pide el otro ingrediente, var=2 escala receta, var=3 pide porcentaje de la mezcla
- [x] 2.4 Verificar que al menos 3 de las 4 variantes de cada familia produzcan respuestas correctas distintas

### Test 2: Validar variantes espejo corregidas
- [x] 2.T1 Escribir test que genere las 4 variantes de 10 familias aleatorias y confirme que ningún enunciado contiene `[ESPEJO]`
- [x] 2.T2 Confirmar que al menos 3 de 4 variantes por familia tienen `respuesta_correcta` distinta
- [x] 2.T3 Verificar que los enunciados de las 4 variantes de cada familia son textualmente diferentes (no solo el prefijo)

## 3. Ampliar Rangos Numéricos

- [x] 3.1 Expandir conjuntos de denominadores: Módulos 1-2 usar `[2, 3, 4, 5, 6, 8, 10, 12]` en vez de `[3, 4, 5, 6, 8, 10]`
- [x] 3.2 Ampliar multiplicadores de `randint(2, 10)` a `randint(2, 12)` garantizando que el total no exceda 120
- [x] 3.3 Agregar más opciones de porcentajes intuitivos en Módulo 3: incluir `75%` (dividir entre 4, multiplicar por 3) y `20%` (dividir entre 5) además de `[50, 25, 10]`
- [x] 3.4 Validar que todos los totales generados sean divisibles exactamente por su denominador (sin decimales)

### Test 3: Validar rangos numéricos ampliados
- [x] 3.T1 Generar todas las preguntas de práctica y verificar que ningún total excede 120 y que todos los resultados son enteros positivos
- [x] 3.T2 Confirmar que los denominadores `2` y `12` aparecen al menos una vez en el pool generado
- [x] 3.T3 Confirmar que porcentajes `75%` y `20%` aparecen en preguntas del Módulo 3

## 4. Mejorar Enunciados de Preguntas Interactivas

- [x] 4.1 Revisar todas las preguntas con `es_interactivo: True` del Módulo 1 y agregar contexto textual completo al enunciado (describir cuántos sectores están pintados)
- [x] 4.2 Revisar preguntas interactivas del Módulo 4 (probetas/beakers) y agregar descripción textual que explique la tarea sin depender del gráfico
- [x] 4.3 Asegurar que las preguntas de gráficos circulares (Módulo 3, nivel 2) incluyan todos los porcentajes y categorías en el texto del enunciado
- [x] 4.4 Confirmar que toda pregunta puede ser resuelta leyendo únicamente el campo `enunciado` sin ver el componente visual

### Test 4: Validar enunciados autoexplicativos
- [x] 4.T1 Filtrar todas las preguntas con `es_interactivo: True` y verificar que el campo `enunciado` contiene al menos 20 palabras (no es genérico vacío)
- [x] 4.T2 Verificar que las preguntas interactivas de Módulo 3 (gráficos circulares) incluyen todos los valores porcentuales en el texto del enunciado
- [x] 4.T3 Verificar que las preguntas interactivas de Módulo 4 (beaker) mencionan las cantidades de ambos ingredientes en el enunciado

## 5. Diversificar Desafíos del Módulo 3

- [x] 5.1 Modificar `generate_challenge_question_fase4()` para Módulo 3: en vez de alternar solo entre porcentajes (idx par) y promedios (idx impar), distribuir las 30 preguntas en 4 categorías: porcentajes intuitivos, gráficos circulares, gráficos de barras, media aritmética
- [x] 5.2 Implementar generadores de preguntas de desafío para gráficos circulares y barras (actualmente ausentes en la función de desafío)
- [x] 5.3 Asegurar que cada categoría tenga al menos 5 preguntas de las 30 totales por desafío
 
### Test 5: Validar diversificación de desafíos M3
- [x] 5.T1 Generar las 30 preguntas de cada desafío del Módulo 3 y clasificarlas por categoría temática
- [x] 5.T2 Confirmar que cada una de las 4 categorías tiene al menos 5 preguntas por desafío
- [x] 5.T3 Verificar que los enunciados de gráficos circulares y barras en desafíos incluyen datos completos para resolver sin visual
 
## 6. Mejorar Distractores de Múltiple Opción
 
- [x] 6.1 Agregar más `errores_previstos` por módulo en `generate_challenge_question_fase4()` para que las alternativas incorrectas reflejen errores pedagógicos reales (ej: confundir numerador con denominador, olvidar el paso de división, calcular el complemento en vez de la fracción pedida)
- [x] 6.2 Asegurar que al menos 2 de los 3 distractores tengan feedback correctivo específico (no el genérico "Esa alternativa es incorrecta")
 
### Test 6: Validar distractores mejorados
- [x] 6.T1 Generar las preguntas de desafío 11 y 12 (múltiple opción) y verificar que al menos 2 de los 3 distractores tienen un `feedback_error` específico (no genérico)
- [x] 6.T2 Verificar que ningún distractor tiene el mismo valor que la respuesta correcta

## 7. Verificación Local y Re-seed

- [x] 7.1 Ejecutar `run_fase4_seed()` en entorno local Docker y verificar que no haya errores de inserción
- [x] 7.2 Consultar la base de datos para confirmar el conteo total de preguntas generadas (~780 práctica + ~360 desafío = ~1140 preguntas)
- [x] 7.3 Ejecutar un script de auditoría que muestree 20 familias aleatorias y confirme que las 4 variantes tienen respuestas distintas
- [x] 7.4 Verificar que ningún enunciado generado contenga el prefijo `[ESPEJO]`

## 8. Actualizar Repositorio GitHub (Rama Desarrollo)

- [x] 8.1 Revisar todos los archivos modificados con `git diff` para confirmar que los cambios son correctos
- [x] 8.2 Hacer `git add` de los archivos modificados en la rama `desarrollo`
- [x] 8.3 Hacer `git commit` con mensaje descriptivo (ej: `fix(fase4): diversificar generador de preguntas`)
- [x] 8.4 Hacer `git push` a la rama `desarrollo` en GitHub

## 9. Redespliegue en VPS de Desarrollo y Verificación

- [x] 9.1 Conectar por SSH a la VPS (`rominejo@34.9.51.225`) y en el directorio del entorno de Desarrollo hacer `git pull` de la rama `desarrollo`
- [x] 9.2 Ejecutar el comando para reiniciar el contenedor de backend de desarrollo o correr el script de seed de Fase 4 en el backend de desarrollo
- [x] 9.3 Leer los logs del backend de desarrollo para confirmar que el seed finalizó con éxito ("Fase 4 seeded successfully!")

## 10. Despliegue en VPS de Producción y Re-seed de Producción

- [x] 10.1 Integrar los cambios de la rama `desarrollo` a la rama de producción (`produccion` o `main` según corresponda) en el repositorio de GitHub
- [x] 10.2 Conectar por SSH a la VPS y en el directorio del entorno de Producción (`Datos_Producion`) hacer `git pull` de la rama de producción
- [x] 10.3 Reiniciar el contenedor de backend de producción mediante Portainer o vía comando `docker compose -p` correspondiente
- [x] 10.4 Ejecutar el script de seed para la base de datos de producción (`logicakids_producion`) a través del contenedor de producción
- [x] 10.5 Leer los logs del backend de producción y comprobar que el proceso de seed de Fase 4 finalizó con éxito sin errores
- [x] 10.6 Conectarse a la base de datos de producción para comprobar que las preguntas se inyectaron de forma correcta y diversa
