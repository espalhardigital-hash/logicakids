import DOMPurify from 'dompurify';

/**
 * Corrige errores de codificación comunes en caracteres en español.
 */
export function fixEncoding(str: string): string {
  if (!str) return '';
  return str
    .replace(/teor\?a/gi, 'teoría')
    .replace(/operaci\?n/gi, 'operación')
    .replace(/fracci\?n/gi, 'fracción')
    .replace(/posici\?n/gi, 'posición')
    .replace(/opci\?n/gi, 'opción')
    .replace(/geometr\?a/gi, 'geometría')
    .replace(/cu\?nto/gi, 'cuánto')
    .replace(/qu\? /gi, 'qué ')
    .replace(/m\?s/gi, 'más');
}

/**
 * Convierte sintaxis markdown básica (negrita, itálica, imágenes, links) a HTML.
 */
export function parseMarkdown(text: string): string {
  if (!text) return '';

  let html = text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/!\[(.*?)\]\((.*?)\)/g, '<img src="$2" alt="$1" class="max-w-full h-auto rounded-lg my-2" />')
    .replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer" class="text-indigo-400 underline">$1</a>');

  return html;
}

/**
 * Formatea un texto solucionando codificación, parseando markdown y sanitizándolo.
 */
export function formatContent(text: string): string {
  if (!text) return '';
  const fixed = fixEncoding(text);
  const parsed = parseMarkdown(fixed);
  return sanitizeHtml(parsed);
}

/**
 * Sanitiza HTML usando DOMPurify con una allowlist estricta para prevenir XSS.
 * Incluye reparación automática y dinámica de SVGs para evitar colapso visual (height: 0px).
 */
export function sanitizeHtml(dirtyHtml: string): string {
  if (!dirtyHtml) return '';

  // Transformación dinámica de etiquetas SVG para reemplazar height:auto por dimensiones intrínsecas y aspect-ratio
  let processedHtml = dirtyHtml.replace(/<svg\s+([^>]*)>/gi, (match, attrs) => {
    // Si ya contiene height explícito en px (que no sea auto), dejarlo o asegurar min-height
    if (attrs.includes('height=') && !attrs.includes('height:auto') && !attrs.includes('height: auto')) {
      return match;
    }

    // Extraer viewBox
    const vbMatch = attrs.match(/viewBox=["']([0-9.\-\s]+)["']/i);
    let calcWidth = 320;
    let calcHeight = 200;
    let aspectRatioStr = "16/9";

    if (vbMatch) {
      const parts = vbMatch[1].split(/\s+/).map(Number);
      if (parts.length === 4) {
        const vbW = parts[2];
        const vbH = parts[3];
        if (vbW > 0 && vbH > 0) {
          if (vbW === 200 && (vbH === 64 || vbH === 86)) {
            calcHeight = 102;
            aspectRatioStr = "200/64";
          } else if (vbW === vbH) {
            calcWidth = 260;
            calcHeight = 260;
            aspectRatioStr = "1/1";
          } else {
            aspectRatioStr = `${Math.round(vbW)}/${Math.round(vbH)}`;
            calcHeight = Math.max(180, Math.round((calcWidth * vbH) / vbW));
          }
        }
      }
    }

    const vbAttr = vbMatch ? `viewBox="${vbMatch[1]}"` : '';
    const borderColor = attrs.includes('F59E0B') ? '#F59E0B' : (attrs.includes('10B981') ? '#10B981' : '#8B5CF6');

    return `<svg ${vbAttr} width="100%" height="${calcHeight}" style="margin:10px auto; display:block; width:100%; max-width:${calcWidth}px; height:${calcHeight}px; min-height:${calcHeight}px; aspect-ratio:${aspectRatioStr}; background:#111827; border:2px solid ${borderColor}; border-radius:14px;">`;
  });

  return DOMPurify.sanitize(processedHtml, {
    ALLOWED_TAGS: [
      'p', 'span', 'div', 'strong', 'em', 'b', 'i', 'u', 's', 'strike',
      'a', 'img', 'br', 'hr', 'ul', 'ol', 'li', 'sub', 'sup', 'code', 'pre',
      'table', 'thead', 'tbody', 'tr', 'th', 'td',
      'svg', 'path', 'circle', 'rect', 'line', 'polyline', 'polygon', 'text', 'g'
    ],
    ALLOWED_ATTR: [
      'class', 'style', 'src', 'alt', 'href', 'target', 'rel', 'title',
      'width', 'height', 'viewBox', 'd', 'fill', 'stroke', 'stroke-width',
      'stroke-linecap', 'stroke-linejoin', 'cx', 'cy', 'r', 'x', 'y', 'x1', 'y1', 'x2', 'y2',
      'fill-opacity', 'stroke-opacity', 'rx', 'ry', 'font-size', 'font-weight', 'text-anchor',
      'dominant-baseline', 'alignment-baseline', 'transform', 'preserveAspectRatio'
    ],
    ALLOWED_URI_REGEXP: /^(?:(?:https?|mailto):|\/|#|data:image\/(?:png|jpeg|webp|gif|svg\+xml);base64,)/i,
    ADD_ATTR: ['target'],
    FORBID_TAGS: ['script', 'style', 'iframe', 'object', 'embed', 'form', 'input', 'button'],
    FORBID_ATTR: ['onerror', 'onload', 'onclick', 'onmouseover', 'onfocus', 'onblur']
  });
}

/**
 * Retorna un objeto compatible con dangerouslySetInnerHTML={{ __html: safeHtml(...) }}
 */
export function safeHtml(dirtyHtml: string): { __html: string } {
  return { __html: sanitizeHtml(dirtyHtml) };
}
