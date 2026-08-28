import { describe, expect, it } from 'vitest';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

describe('contrato global de scroll', () => {
  const source = readFileSync(resolve(process.cwd(), 'App.tsx'), 'utf8');

  it('permite desplazamiento solamente en mapas y selectores', () => {
    expect(source).toContain(
      "location.pathname === '/map' || location.pathname.startsWith('/welcome')",
    );
    expect(source).toContain('min-h-screen p-4 overflow-y-auto overflow-x-hidden');
  });

  it('fija las actividades al viewport sin padding exterior', () => {
    expect(source).toContain('h-dvh min-h-0 p-0 overflow-hidden');
    expect(source).toContain('max-w-none h-full min-h-0');
  });
});
