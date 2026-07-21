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
