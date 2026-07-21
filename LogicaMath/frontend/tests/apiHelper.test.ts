import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { fetchWithTimeout } from '../services/apiHelper';

describe('fetchWithTimeout', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('debe resolver la promesa si fetch responde antes del timeout', async () => {
    const mockResponse = new Response(JSON.stringify({ data: 'ok' }));
    const fetchMock = vi.fn().mockResolvedValue(mockResponse);
    vi.stubGlobal('fetch', fetchMock);

    const promise = fetchWithTimeout('http://example.com/api', {}, 5000);
    const res = await promise;
    expect(res).toBe(mockResponse);
    expect(fetchMock).toHaveBeenCalledOnce();
  });

  it('debe abortar la peticion y lanzar un error si fetch excede el tiempo configurado', async () => {
    // Mock de un fetch que simula quedar colgado indefinidamente hasta abortar
    const fetchMock = vi.fn().mockImplementation((url, options) => {
      return new Promise((resolve, reject) => {
        if (options?.signal) {
          options.signal.addEventListener('abort', () => {
            const err = new Error('The user aborted a request.');
            err.name = 'AbortError';
            reject(err);
          });
        }
      });
    });
    vi.stubGlobal('fetch', fetchMock);

    const promise = fetchWithTimeout('http://example.com/api', {}, 100);

    // Adelantar los temporizadores para disparar el timeout de AbortController
    vi.advanceTimersByTime(150);

    await expect(promise).rejects.toThrow('Timeout de conexión: La solicitud excedió el tiempo límite de 0.1 segundos.');
  });
});
