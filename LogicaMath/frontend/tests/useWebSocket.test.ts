import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook } from '@testing-library/react';
import { useWebSocket } from '../components/useWebSocket';

describe('useWebSocket URL resolution', () => {
  let wsConstructorSpy: any;

  beforeEach(() => {
    // La resolución por window.location es el comportamiento bajo prueba.
    // Evita que el .env.local del desarrollador anule el escenario simulado.
    vi.stubEnv('VITE_API_URL', '');

    // Mockear la clase WebSocket global
    wsConstructorSpy = vi.fn().mockImplementation(function (this: any, url: string) {
      this.url = url;
      this.addEventListener = vi.fn();
      this.removeEventListener = vi.fn();
      this.close = vi.fn();
      return this;
    });
    vi.stubGlobal('WebSocket', wsConstructorSpy);
    
    // Respaldar window.location original
    vi.stubGlobal('location', {
      protocol: 'http:',
      hostname: 'localhost',
      port: '3000',
    });
  });

  afterEach(() => {
    vi.unstubAllEnvs();
    vi.restoreAllMocks();
  });

  it('debe resolver la URL del WebSocket a ws://localhost:8000 en entorno local', () => {
    const callback = vi.fn();
    renderHook(() => useWebSocket(callback));

    // Se debió instanciar el WebSocket con la URL local calculada (port 3000 -> fallback a 8000)
    expect(wsConstructorSpy).toHaveBeenCalledWith('ws://localhost:8000/ws/admin-sync');
  });

  it('debe resolver la URL del WebSocket a wss en un entorno HTTPS de produccion', () => {
    // Simulamos que estamos en HTTPS en produccion
    vi.stubGlobal('location', {
      protocol: 'https:',
      hostname: 'logica.espalhar.shop',
      port: '',
    });

    const callback = vi.fn();
    renderHook(() => useWebSocket(callback));

    expect(wsConstructorSpy).toHaveBeenCalledWith('wss://logica.espalhar.shop/ws/admin-sync');
  });
});
