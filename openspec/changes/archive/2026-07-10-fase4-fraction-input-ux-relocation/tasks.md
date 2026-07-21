## 1. Modificación de Fase4GameScreen.tsx

- [x] 1.1 Quitar el bloque condicional de inputs manuales (`showFractionInput`) de la columna derecha de inputs interactivos.
- [x] 1.2 Agregar el bloque condicional de inputs manuales (`showFractionInput`) en la columna izquierda dentro del componente de tarjeta visual (justo debajo del párrafo del enunciado).
- [x] 1.3 Asegurar que los inputs interactúen correctamente con el teclado numérico (`CustomKeyboard`) y que no se pierdan referencias de focos activos (`activeInputField`).
- [x] 1.4 Modificar el botón Confirmar del modo interactivo (línea 1381) reduciendo tipografía, paddings, esquinas redondeadas, ancho máximo e icono circular de check.
- [x] 1.5 Modificar el botón Confirmar de formas geométricas / polígono asimétrico (línea 1479) reduciendo tipografía, paddings, esquinas redondeadas e icono circular de check.
- [x] 1.6 Modificar el botón Confirmar de opción múltiple (línea 1522) reduciendo tipografía, paddings, esquinas redondeadas, ancho máximo e icono circular de check.

## 2. Ajustes de Estilos CSS

- [x] 2.1 Ajustar márgenes verticales y paddings para `.f4-fraction-input-box` en `Fase4Styles.css` cuando se encuentra dentro de la tarjeta.
- [x] 2.2 Optimizar el centrado y responsividad del input simple para que no sobrecargue la tarjeta de la izquierda.

## 3. Pruebas y Verificación

- [x] 3.1 Construir el frontend de desarrollo local para aplicar los cambios.
- [x] 3.2 Verificar visualmente que la caja de entrada de fracción y número entero aparezca abajo del enunciado en la izquierda.
- [x] 3.3 Comprobar la usabilidad con el teclado numérico a la derecha, y verificar que no hay desbordamiento en la resolución `2560x945`.
- [x] 3.4 Verificar visualmente que los tres botones "CONFIRMAR" de la Fase 4 tengan dimensiones compactas, estilizadas y ergonómicas.
