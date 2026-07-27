import DOMPurify from 'dompurify';

/**
 * Servicio para formateo, limpieza y renderizado seguro de textos del juego.
 */

/**
 * Corrige los caracteres corruptos con '?' provenientes de problemas de codificación en la base de datos.
 */
export function fixEncoding(text: string): string {
  if (!text) return text;
  
  return text
    // Signos de exclamación al inicio (si hay una exclamación al final o empieza la frase)
    .replace(/^\?([A-ZÁÉÍÓÚÑ])/g, '¡$1')
    .replace(/\b\?([A-ZÁÉÍÓÚÑ])/g, '¡$1')
    
    // Palabras específicas corruptas comunes en la aplicación
    .replace(/num\?rica/gi, 'numérica')
    .replace(/cu\?ntos/gi, 'cuántos')
    .replace(/cu\?nto/gi, 'cuánto')
    .replace(/introducci\?n/gi, 'introducción')
    .replace(/m\?ltiplos/gi, 'múltiplos')
    .replace(/m\?ltiplo/gi, 'múltiplo')
    .replace(/t\?rmino/gi, 'término')
    .replace(/definici\?n/gi, 'definición')
    .replace(/representaci\?n/gi, 'representación')
    .replace(/operaci\?n/gi, 'operación')
    .replace(/agrupaci\?n/gi, 'agrupación')
    .replace(/máx\?mas/gi, 'máximas')
    .replace(/f\?rmula/gi, 'fórmula')
    .replace(/b\?squeda/gi, 'búsqueda')
    .replace(/gr\?fica/gi, 'gráfica')
    .replace(/matem\?tica/gi, 'matemática')
    .replace(/b\?sica/gi, 'básica')
    .replace(/explicaci\?n/gi, 'explicación')
    .replace(/lecci\?n/gi, 'lección')
    .replace(/asociaci\?n/gi, 'asociación')
    .replace(/clasificaci\?n/gi, 'clasificación')
    .replace(/compr\?ndelo/gi, 'compréndelo')
    .replace(/pr\?ctica/gi, 'práctica')
    .replace(/teor\?a/gi, 'teoría')
    .replace(/desaf\?o/gi, 'desafío')
    .replace(/f\?cil/gi, 'fácil')
    .replace(/dif\?cil/gi, 'difícil')
    .replace(/r\?pido/gi, 'rápido')
    .replace(/l\?gica/gi, 'lógica');
}

/**
 * Sanitiza HTML usando DOMPurify con una allowlist estricta para prevenir XSS.
 * Incluye reparación automática de SVGs con dimensiones distorsionadas.
 */
export function sanitizeHtml(dirtyHtml: string): string {
  if (!dirtyHtml) return '';

  // Reparar SVGs distorsionados con width='320' height='320' y viewBox corto
  let processedHtml = dirtyHtml.replace(
    /<svg\s+width=['"]320['"]\s+height=['"]320['"]\s+viewBox=['"]0 68 200 64['"]/g,
    `<svg viewBox="0 68 200 64" style="margin:10px auto; display:block; width:100%; max-width:320px; height:auto; background:#111827; border:2px solid #8B5CF6; border-radius:14px;"`
  ).replace(
    /width=['"]320['"]\s+height=['"]320['"]\s+viewBox=['"]0 68 200 64['"]/g,
    `viewBox="0 68 200 64" style="margin:10px auto; display:block; width:100%; max-width:320px; height:auto; background:#111827; border:2px solid #8B5CF6; border-radius:14px;"`
  );

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
 * Helper para dangerouslySetInnerHTML que retorna un objeto sanitizado { __html: string }
 */
export function safeHtml(dirtyHtml: string): { __html: string } {
  return { __html: sanitizeHtml(dirtyHtml) };
}

/**
 * Convierte sintaxis básica de Markdown (imágenes y enlaces) a HTML.
 */
export function parseMarkdown(text: string): string {
  if (!text) return text;
  
  let html = text;
  
  // Parsear imágenes markdown: ![alt](url)
  const imgRegex = /!\[(.*?)\]\((.*?)\)/g;
  html = html.replace(imgRegex, (_match, alt, src) => {
    const cleanSrc = /^(?:https?:\/\/|\/|\.\/|data:image\/)/i.test(src.trim()) ? src.trim() : '';
    return `<img src="${cleanSrc}" alt="${alt}" class="lk-question-graphic my-4 max-w-full rounded-xl" style="display: block; margin: 16px auto; max-height: 250px; object-fit: contain;" />`;
  });
  
  // Parsear enlaces markdown: [texto](url)
  const linkRegex = /\[(.*?)\]\((.*?)\)/g;
  html = html.replace(linkRegex, (_match, linkText, url) => {
    const cleanUrl = /^(?:https?:\/\/|\/|#)/i.test(url.trim()) ? url.trim() : '#';
    return `<a href="${cleanUrl}" target="_blank" rel="noopener noreferrer" class="text-blue-400 underline hover:text-blue-350">${linkText}</a>`;
  });
  
  return html;
}

/**
 * Helper principal que limpia la codificación y formatea markdown para renderizado seguro en React.
 */
export function formatContent(text: string): string {
  if (!text) return '';
  return sanitizeHtml(parseMarkdown(fixEncoding(text)));
}

