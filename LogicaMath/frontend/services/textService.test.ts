import { describe, it, expect } from 'vitest';
import { sanitizeHtml, safeHtml, formatContent, parseMarkdown } from './textService';

describe('textService XSS and Sanitization', () => {
  it('strips script tags and inline execution handlers', () => {
    const malicious = '<script>alert("xss")</script><img src="x" onerror="alert(1)" />';
    const sanitized = sanitizeHtml(malicious);
    expect(sanitized).not.toContain('<script>');
    expect(sanitized).not.toContain('onerror');
    expect(sanitized).not.toContain('alert');
  });

  it('blocks javascript: URLs in markdown links', () => {
    const markdown = '[Click Me](javascript:alert(1))';
    const parsed = parseMarkdown(markdown);
    const sanitized = sanitizeHtml(parsed);
    expect(sanitized).not.toContain('href="javascript:');
    expect(sanitized).toContain('href="#"');
  });

  it('blocks javascript: URLs in markdown images', () => {
    const markdown = '![Alt](javascript:alert(1))';
    const parsed = parseMarkdown(markdown);
    const sanitized = sanitizeHtml(parsed);
    expect(sanitized).not.toContain('src="javascript:');
  });

  it('allows safe HTML tags and attributes', () => {
    const safe = '<p class="text-red-500"><strong>Hola</strong> <a href="https://example.com" target="_blank">Link</a></p>';
    const sanitized = sanitizeHtml(safe);
    expect(sanitized).toContain('<p class="text-red-500">');
    expect(sanitized).toContain('<strong>Hola</strong>');
    expect(sanitized).toContain('href="https://example.com"');
  });

  it('safeHtml returns an object with __html property', () => {
    const result = safeHtml('<b>Test</b>');
    expect(result).toEqual({ __html: '<b>Test</b>' });
  });

  it('formatContent fixes encoding and sanitizes markdown HTML', () => {
    const text = 'teor?a con <script>bad()</script> e imagen ![test](https://img.com/a.png)';
    const result = formatContent(text);
    expect(result).toContain('teoría');
    expect(result).not.toContain('<script>');
    expect(result).toContain('<img src="https://img.com/a.png"');
  });
});

describe('SVG figure attribute preservation', () => {
  it('preserves numeric/keyword geometry attributes on svg children', () => {
    const svg = `<svg viewBox="0 68 200 64" width="100%" height="102">` +
      `<rect x="10.0" y="67.0" width="180.0" height="66.0" fill="#3B82F6" ` +
      `fill-opacity="0.10" stroke="#FFFFFF" stroke-width="1" rx="4"></rect>` +
      `<text x="16.0" y="82.4" fill="#FFFFFF" font-size="11" ` +
      `text-anchor="start">Dinero</text></svg>`;
    const sanitized = sanitizeHtml(svg);
    expect(sanitized).toContain('viewBox="0 68 200 64"');
    expect(sanitized).toContain('x="10.0"');
    expect(sanitized).toContain('y="67.0"');
    expect(sanitized).toContain('width="180.0"');
    expect(sanitized).toContain('fill-opacity="0.10"');
    expect(sanitized).toContain('stroke-width="1"');
    expect(sanitized).toContain('rx="4"');
    expect(sanitized).toContain('font-size="11"');
    expect(sanitized).toContain('text-anchor="start"');
  });

  it('preserves points attribute on polygon shapes', () => {
    const svg = `<svg viewBox="0 0 200 200"><polygon points="10.0,190.0 190.0,190.0 100.0,20.0" ` +
      `fill="#F59E0B" fill-opacity="0.15" stroke="#FFFFFF" stroke-width="3.5"></polygon></svg>`;
    const sanitized = sanitizeHtml(svg);
    expect(sanitized).toContain('points="10.0,190.0 190.0,190.0 100.0,20.0"');
  });

  it('still blocks javascript: URLs even on svg-adjacent href/src', () => {
    const svg = `<svg><a href="javascript:alert(1)"><text x="0" y="0">click</text></a></svg>`;
    const sanitized = sanitizeHtml(svg);
    expect(sanitized).not.toContain('href="javascript:');
  });
});

