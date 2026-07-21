## 1. Frontend: Componentes y Tipos

- [x] 1.1 Actualizar `Fase4Types.ts` para agregar `fraction_percentage` al tipo `tipo_visual`.
  - [x] *Test: Verificar que TypeScript compile correctamente sin errores de tipado.*
- [x] 1.2 Crear el componente `FractionPercentageVisualizer.tsx` interactivo con barra segmentada y caja de ecuación.
  - [x] *Test: Validar renderizado inicial del componente en un entorno aislado (o storybook/test local).*
- [x] 1.3 Integrar la mecánica de selección de números (banco de números click-to-select para llenar numerador y denominador).
  - [x] *Test: Probar interacciones de clic y validación de la fracción equivalente armada.*
- [x] 1.4 Actualizar `Fase4VisualizerEngine.tsx` para importar y renderizar `FractionPercentageVisualizer` cuando `tipo_visual === 'fraction_percentage'`.
  - [x] *Test: Comprobar que el motor inyecta el componente correcto dado el tipo visual.*
- [x] 1.5 Verificar/Actualizar `Fase4TheoryModal.tsx` para asegurar que renderice el interactivo sin problemas de parseo.
  - [x] *Test: Abrir un modal de teoría y verificar visualmente que el componente funciona dentro del modal.*

## 2. Backend: Módulo 2 y 3 (Teoría y Semillas)

- [x] 2.1 Modificar `fase4/theory_examples.py` (Módulo 2 y Módulo 3) para incorporar `tipo_visual: 'fraction_percentage'`.
  - [x] *Test: Levantar el endpoint de teoría localmente y verificar el JSON retornado.*
- [x] 2.2 Modificar `fase4/seed.py` (Módulos 2 y 3) para inyectar `tipo_visual: 'fraction_percentage'` y expandir los porcentajes disponibles.
  - [x] *Test: Forzar el seed en la BD local (`FORCE_SEED=true`) y revisar la generación de las nuevas preguntas en la tabla correspondiente.*

## 3. Análisis y Sincronización de Base de Datos

- [x] 3.1 Analizar la base de datos local vs. Desarrollo (`bd_logicakids_desarrollo`) y Producción (`bd_logicakids_producion`).
  - [x] *Test: Extraer el conteo y tipos de preguntas generadas en local y compararlo con el estado actual de las BD de desarrollo y producción para garantizar paridad (o planificar la migración).*

## 4. Despliegue Local (Docker)

- [x] 4.1 Construir y levantar los contenedores localmente usando `Datos_localhost/docker-compose.local.yml`.
  - [x] *Test: Confirmar que frontend y backend se comunican sin problemas (`localhost:3000` y `localhost:8000`).*
- [x] 4.2 Probar los flujos completos de Nivel 1 y Teoría interactuando con la base de datos local de PostgreSQL y Redis.

## 5. Sincronización y Despliegue GitHub (Desarrollo y Producción)

- [x] 5.1 Realizar commit y push de todos los cambios validados hacia la rama de **`desarrollo`** en GitHub.
- [x] 5.2 Realizar el merge, commit y push hacia la rama de **`producion`** (siguiendo aprobación explícita).
- [ ] 5.3 (Opcional, si hay acceso) Redesplegar los stacks en Portainer para Desarrollo y Producción, usando los archivos de entorno de `Datos_Desarrollo` y `Datos_Producion`.
