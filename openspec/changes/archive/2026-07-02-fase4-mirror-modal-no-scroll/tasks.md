## 1. Backend: Concordancia de Género

- [x] 1.1 Modificar la lógica de generación de preguntas del módulo 2 en `LogicaMath/backend/app/fase4/seed.py` para determinar dinámicamente si la colección es de género femenino.
- [x] 1.2 Ajustar los enunciados de los niveles 2 y 3 para usar artículos y preposiciones con género correcto según corresponda.

## 2. Frontend: Rediseño Compacto del Modal Espejo

- [x] 2.1 Modificar `LogicaMath/frontend/components/fase4/Fase4MirrorModal.tsx` para eliminar la visualización del enunciado largo de la pregunta anterior fallida.
- [x] 2.2 Rediseñar la sección de repaso como una franja flex horizontal minimalista que ocupe el mínimo espacio de pantalla.
- [x] 2.3 Implementar la grilla de teclado simétrica de 3x4 de la Fase 2 directamente en el modal, deshabilitando visualmente (`opacity-25` e inactividad de click) el botón de punto decimal `.`.
- [x] 2.4 Reemplazar todas las referencias de clases CSS de `.f2-` a `.f4-` en el modal e importar el archivo local de estilos `Fase4Styles.css`.

## 3. Frontend: Estilos CSS y Eliminación de Scroll

- [x] 3.1 Añadir al final de `LogicaMath/frontend/components/fase4/Fase4Styles.css` los estilos portados del modal, del input interactivo y del teclado virtual (keypad) adaptados al prefijo `.f4-`.
- [x] 3.2 Adaptar los colores de enfoque (`focused`) del input interactivo y hover del teclado para usar los tonos púrpuras propios del tema de la Fase 4.
- [x] 3.3 Asegurar mediante propiedades CSS (como `overflow: hidden`) y reducción de paddings que el modal impida y evite al 100% la aparición de scroll vertical.

## 4. Verificación y Pruebas

- [x] 4.1 Levantar el entorno de desarrollo local con Docker Compose.
- [x] 4.2 Correr el script de siembra (seed) del backend para actualizar los enunciados con género corregido en la base de datos local.
- [x] 4.3 Realizar pruebas de juego manuales en `http://localhost:3000` para comprobar la consistencia visual sin scroll del Bucle Espejo, la grilla del teclado 3x4 con punto deshabilitado y botón abajo, y la concordancia de los textos.
