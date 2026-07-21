## Context

La herramienta "Buzón de Mejorías UX & QA" se utiliza para agilizar el reporte de problemas visuales y proponer mejoras (UX) desde la interfaz de juego hacia el Panel de Administrador. Actualmente, el flujo requiere que el evaluador tome capturas de forma manual (subiéndolas o pegándolas). Asimismo, la visualización de elementos HTML en el panel administrador utiliza `dangerouslySetInnerHTML` lo que provoca fuga de estilos CSS y conflictos visuales. Finalmente, el agente IA u otros desarrolladores carecen de contexto sobre el estado reactivo que generó el error y la relación exacta con imágenes guardadas en MinIO no siempre es suficientemente explícita para la IA.

## Goals / Non-Goals

**Goals:**
- Automatizar la captura de pantalla usando `html2canvas` en el instante del reporte.
- Utilizar Shadow DOM para aislar la previsualización del HTML interceptado.
- Serializar el estado crítico de la aplicación en React y adjuntarlo al payload (`app_state`).
- Refinar `getUniqueSelector` para garantizar rutas unívocas.
- Asegurar URLs directas e inequívocas al almacenamiento de MinIO.

**Non-Goals:**
- No se migrará el esquema completo de base de datos, solo se ajustará el guardado del `app_state` (JSON).
- No se implementará grabación de video (ej. rrweb) en esta iteración.
- No se construirán integraciones con plataformas externas (Jira/GitHub) todavía.

## Decisions

1. **Captura Automática (html2canvas):** 
   - *Decisión:* Al hacer clic en un elemento en modo inspección, el componente `UXFeedbackOverlay` invocará `html2canvas(document.body, { windowWidth, windowHeight, scale: 1 })` en segundo plano. La imagen se subirá automáticamente y devolverá la URL al modal sin que el usuario deba intervenir.
   - *Alternativa considerada:* API experimental genérica del navegador. *Rechazada* por problemas de compatibilidad y por requerir múltiples permisos del usuario.

2. **Aislamiento Visual con Shadow DOM:**
   - *Decisión:* En el componente `UXFeedbackTab.tsx` (Admin Panel), se creará un componente envoltorio que use `attachShadow({ mode: 'open' })`. Dentro del shadow root se inyectarán las clases base (como una referencia estática a `index.css`) y el HTML capturado, previniendo que los estilos del admin panel interfieran.
   - *Alternativa:* Usar un `<iframe>` base64. *Rechazada* porque es más pesado y complicado de dimensionar automáticamente frente a un Shadow Root nativo.

3. **Captura del Estado de la Aplicación (App State):**
   - *Decisión:* Ampliar la firma de la captura. Se capturarán variables relevantes que estén al alcance en el overlay (Puntaje actual, Respuestas previas) si se exportan a un nivel global (ej. `window.__GAME_STATE__` si estuviese expuesto) o se pasarán por Props hacia el `UXFeedbackOverlay`. El Backend almacenará esto dentro de la columna JSON `app_state`.

4. **Enlaces Absolutos a MinIO:**
   - *Decisión:* Refactorizar el endpoint `upload_feedback_screenshot` en el Backend y `storage.py` para asegurar que siempre devuelva la URL absoluta apuntando al clúster de MinIO (`MINIO_EXTERNAL_ENDPOINT`). Esto garantiza que los LLMs como Antigravity accedan a la imagen sin depender de contextos relativos (`/evaluador/...`).

5. **Mejora del Selector DOM (`getUniqueSelector`):**
   - *Decisión:* Se cambiará la heurística de `nth-of-type` por `nth-child` calculada iterativamente sobre todos los hermanos directos del nodo. Además, se incluirán atributos `[data-testid]` si están presentes, lo que otorgará la máxima resiliencia.

## Risks / Trade-offs

- **Rendimiento de html2canvas:** 
  - *Riesgo:* `html2canvas` puede ser lento y bloquear el hilo principal durante fracciones de segundo.
  - *Mitigación:* Mostrar un *loading spinner* inmediato al hacer clic en el DOM antes de que aparezca el modal de feedback, ofreciendo retroalimentación visual al usuario.
- **Complejidad del Shadow DOM:**
  - *Riesgo:* Algunos estilos inyectados globalmente (CSS Variables de Tailwind o variables propias del `:root`) no traspasarán el límite del Shadow DOM.
  - *Mitigación:* Se inyectará un `<style>` dentro del shadow root que importe los tokens globales básicos del proyecto.
