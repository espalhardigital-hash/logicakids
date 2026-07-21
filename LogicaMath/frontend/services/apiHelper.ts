/**
 * Helper de comunicación API - LogicaKids Pro
 * Proporciona fetch con soporte de timeout y AbortController para prevenir solicitudes colgadas.
 */

export async function fetchWithTimeout(
  url: string,
  options: RequestInit = {},
  timeoutMs: number = 10000
): Promise<Response> {
  const controller = new AbortController();
  const id = setTimeout(() => {
    controller.abort();
  }, timeoutMs);

  try {
    const response = await fetch(url, {
      credentials: 'include',
      ...options,
      signal: controller.signal
    });
    clearTimeout(id);
    return response;
  } catch (error: any) {
    clearTimeout(id);
    if (error.name === 'AbortError') {
      throw new Error(`Timeout de conexión: La solicitud excedió el tiempo límite de ${timeoutMs / 1000} segundos.`);
    }
    throw error;
  }
}
