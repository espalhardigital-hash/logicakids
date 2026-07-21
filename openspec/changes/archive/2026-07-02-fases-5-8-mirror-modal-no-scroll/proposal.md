## Why

Los modales de "Segunda Oportunidad" (Bucle Espejo) en las Fases 5, 6, 7 y 8 presentan scroll vertical cuando se cargan enunciados de preguntas anteriores muy largos. Esto rompe la directriz pedagógica del proyecto de mantener toda la información del Bucle Espejo visible en una sola pantalla sin necesidad de hacer scroll.

## What Changes

- **Ocultamiento de la pregunta anterior fallida:** El enunciado completo de la pregunta anterior que causó la equivocación desaparecerá de la sección de repaso superior del modal de espejo en las Fases 5, 6, 7 y 8.
- **Rediseño compacto del Repaso:** Rediseñar la sección de repaso de la respuesta anterior para que ocupe una barra horizontal delgada y minimalista que no requiera scroll en todas estas fases.
- **Estilos CSS Locales Libres de Scroll:** Ajustar los estilos del modal espejo y las tarjetas de las Fases 5, 6, 7 y 8 en sus respectivas hojas de estilos CSS (`Fase5Styles.css`, etc.) para bloquear la aparición de scroll mediante `overflow: hidden !important` y topes de altura (`max-height: 96vh`).

## Capabilities

### New Capabilities
- Ninguna.

### Modified Capabilities
- `phase-design-consistency`: Se generaliza el requisito de comportamiento del Bucle Espejo para establecer que **todas** las fases del sistema (Fases 4 a 8) SHALL mantener su información en una sola pantalla sin scroll, eliminando el texto del enunciado anterior en el repaso y aplicando la disposición horizontal compacta.

## Impact

- **Frontend (Fase 5):** Modificación de `Fase5MirrorModal.tsx` y `Fase5Styles.css`.
- **Frontend (Fase 6):** Modificación de `Fase6MirrorModal.tsx` y `Fase6Styles.css`.
- **Frontend (Fase 7):** Modificación de `Fase7MirrorModal.tsx` and `Fase7Styles.css`.
- **Frontend (Fase 8 & 9):** Modificación de `Fase8MirrorModal.tsx`, `Fase9MirrorModal.tsx` y `Fase8Styles.css` / `Fase9Styles.css`.
