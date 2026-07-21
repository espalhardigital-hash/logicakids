## Context

El modal espejo (segunda oportunidad) en las Fases 5, 6, 7 y 8 renderiza el enunciado largo del problema anterior fallido en el bloque de repaso superior. Esto añade una altura considerable al modal, forzando un scroll vertical no deseado en resoluciones habituales y rompiendo el estándar visual del juego. 

Al igual que en la Fase 4, se busca unificar el comportamiento de los teclados virtuales y el repaso de los modales espejo en todas las fases tomando como referencia el diseño simétrico de grilla 3x4 de la Fase 2, asegurando que toda la información relevante quepa en una sola pantalla.

## Goals / Non-Goals

**Goals:**
- Asegurar que todo el contenido del modal de segunda oportunidad en las Fases 5, 6, 7 y 8 quepa en la pantalla en una sola visualización sin scroll.
- Ocultar la pregunta anterior fallida del repaso y mostrar únicamente la respuesta errónea del alumno y la respuesta esperada en formato horizontal compacto.
- Adaptar las hojas de estilos CSS (`Fase5Styles.css`, `Fase6Styles.css`, etc.) para bloquear la aparición de scroll mediante `overflow: hidden !important` y topes de altura (`max-height: 96vh`).
- Asegurar la consistencia visual y de comportamiento del teclado en estas fases.

**Non-Goals:**
- No se modificará el comportamiento del Bucle Espejo en la Fase 2.
- No se alterará el motor lógico de evaluación del backend ni el Tutor Invisible.

## Decisions

### 1. Eliminación del enunciado de la pregunta anterior y compactación horizontal
- **Decisión:** Remover el bloque `{lastQuestionEnunciado && ...}` de la UI en `Fase5MirrorModal.tsx`, `Fase6MirrorModal.tsx`, `Fase7MirrorModal.tsx` y `Fase8MirrorModal.tsx`, y reestructurar el bloque de REPASO restante para que sea una barrita flex horizontal de altura fija mínima (~40-50px).
- **Razonamiento:** El enunciado anterior aporta poco valor pedagógico en esta pantalla rápida de segunda oportunidad y es el elemento principal que consume el espacio vertical. Al removerlo, garantizamos espacio suficiente para la nueva pregunta y el teclado.
- **Alternativas consideradas:** Mantener el enunciado pero colapsarlo en un acordeón interactivo. Se descartó porque añade interacción innecesaria y complejidad en una pantalla para niños.

### 2. Teclado Simétrico 3x4 Estándar (Consistencia de UX)
- **Decisión:** Mantener el teclado numérico virtual del estándar de la Fase 2 en las Fases 5, 6, 7 y 8, pero con las optimizaciones de espaciado y paddings necesarias para evitar el scroll. Si una fase o nivel no requiere decimales (como ciertos niveles de coordenadas o probabilidad), la tecla del punto decimal `.` se deshabilitará visual y funcionalmente, manteniendo la grilla 3x4 unificada intacta.
- **Razonamiento:** Sigue la Guía de UX del proyecto y respeta el estándar de la Fase 2. La tecla del punto decimal se mantendrá dentro de la grilla para preservar la consistencia táctil del layout de 3x4.

### 3. Estilos CSS Libres de Scroll
- **Decisión:** Modificar las definiciones de `.fX-feedback-overlay` y `.fX-mirror-modal-card` en sus respectivos archivos de estilos para bloquear la aparición de scroll mediante `overflow: hidden !important` y limitar la altura del modal card a `max-height: 96vh`.
- **Razonamiento:** Esta regla de CSS previene fallos ante re-renderizados bruscos o dispositivos móviles con pantallas extremadamente pequeñas, asegurando la consistencia estética.

## Risks / Trade-offs

- **[Risk] Mayor mantenimiento de código:** Dado que cada fase mantiene su propio modal espejo (`Fase5MirrorModal`, etc.) y sus propios estilos locales, realizar esta corrección requiere editar múltiples archivos.
  - **Mitigación:** Se seguirá una secuencia metódica de copiado y adaptación del patrón validado de la Fase 4 para asegurar una implementación rápida, limpia y sin regresiones.

## Plan de Despliegue y Migración (VPS & GitHub)

Para desplegar estos cambios y sus semillas (seeds) asociadas de forma consistente en desarrollo y producción:

### 1. Integración en GitHub
- Todos los cambios confirmados en local en la rama `desarrollo` se subirán a `origin/desarrollo`.
- Los cambios se fusionarán en la rama `main` (producción) y se subirán a `origin/main`.

### 2. Actualización de Stacks en VPS (IP: 35.222.6.7)
- **Desarrollo (Stack 28):** 
  - Se actualizará el código en `/home/rominejo/logicakids` bajo la rama `desarrollo`.
  - Se sincronizarán los archivos con el directorio del stack de Portainer: `/var/lib/docker/volumes/portainer_portainer_data/_data/compose/28/`
  - Se reconstruirán e iniciarán los contenedores: `sudo docker compose -p logicakids-desarollo up -d --build backend frontend`
- **Producción (Stack 29):**
  - Se actualizará el código en `/home/rominejo/logicakids` bajo la rama `main`.
  - Se sincronizarán los archivos con el directorio del stack de Portainer: `/var/lib/docker/volumes/portainer_portainer_data/_data/compose/29/`
  - Se reconstruirán e iniciarán los contenedores: `sudo docker compose -p matematicas-producion up -d --build backend frontend`

### 3. Siembra (Seeding) de Preguntas
- Para inyectar la concordancia gramatical corregida sin afectar variables de entorno globales en caliente, se ejecutará el script del seed en los contenedores correspondientes de la VPS:
  - Desarrollo: `sudo docker exec logicakids-desarollo-backend-1 python -m app.fase4.seed`
  - Producción: `sudo docker exec matematicas-producion-backend-1 python -m app.fase4.seed`

