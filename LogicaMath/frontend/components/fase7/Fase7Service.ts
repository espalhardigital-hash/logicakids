/**
 * Servicio API — Fase 6: Desarrollo Numérico y Razonamiento
 * Capa de comunicación con el backend de Fase 6.
 */

import { fetchWithTimeout } from '../../services/apiHelper';
import type {
  Fase7Dashboard,
  Fase7Pregunta,
  Fase7AnswerPayload,
  Fase7AnswerResult,
  Fase7Lectura,
} from './Fase7Types';

const API_URL = import.meta.env.VITE_API_URL || '/api';

function getAuthHeaders(): HeadersInit {
  // Compatibilidad con el sistema de almacenamiento de tokens del proyecto
  const token =
    localStorage.getItem('auth_token') ||
    localStorage.getItem('token') ||
    sessionStorage.getItem('auth_token') ||
    '';
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `Error HTTP ${res.status}`);
  }
  return res.json() as Promise<T>;
}

const activeRequests = new Map<string, Promise<any>>();

async function fetchDeduplicated<T>(key: string, fetchFn: () => Promise<T>): Promise<T> {
  const existing = activeRequests.get(key);
  if (existing) {
    return existing;
  }
  const promise = fetchFn().finally(() => {
    activeRequests.delete(key);
  });
  activeRequests.set(key, promise);
  return promise;
}

// ─────────────────────────────────────────────────────────────────────────────

/**
 * Obtiene el dashboard de Fase 6 con los 5 módulos y su estado.
 */
export async function getFase7Dashboard(): Promise<Fase7Dashboard> {
  const key = 'dashboard';
  return fetchDeduplicated(key, async () => {
    const res = await fetchWithTimeout(`${API_URL}/fase7/dashboard`, {
      headers: getAuthHeaders(),
    });
    return handleResponse<Fase7Dashboard>(res);
  });
}

/**
 * Obtiene la siguiente pregunta para un módulo y nivel específicos.
 */
export async function getFase7Question(
  moduloId: number, nivelId: number, reload: boolean = false): Promise<Fase7Pregunta> {
  const key = `question-${moduloId}-${nivelId}-${reload}`;
  return fetchDeduplicated(key, async () => {
    const res = await fetchWithTimeout(
      `${API_URL}/fase7/modulo/${moduloId}/nivel/${nivelId}/pregunta?reload=${reload}`,
      { headers: getAuthHeaders() }
    );
    return handleResponse<Fase7Pregunta>(res);
  });
}

/**
 * Envía la respuesta del alumno y recibe el resultado con feedback.
 */
export async function submitFase7Answer(
  payload: Fase7AnswerPayload
): Promise<Fase7AnswerResult> {
  const res = await fetchWithTimeout(`${API_URL}/fase7/responder`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  });
  return handleResponse<Fase7AnswerResult>(res);
}

/**
 * Obtiene el contenido de lectura/teoría de un nivel.
 */
export async function getFase7Reading(
  moduloId: number, nivelId: number, reload: boolean = false): Promise<Fase7Lectura> {
  const key = `reading-${moduloId}-${nivelId}`;
  return fetchDeduplicated(key, async () => {
    const res = await fetchWithTimeout(
      `${API_URL}/fase7/lectura/${moduloId}/nivel/${nivelId}`,
      { headers: getAuthHeaders() }
    );
    return handleResponse<Fase7Lectura>(res);
  });
}

/**
 * Gradúa al alumno de Fase 6 a Fase 3 (requiere todos los módulos dominados).
 */
export async function graduateFase7(): Promise<{
  message: string;
  nueva_fase_id: number;
  nueva_fase_nombre: string;
}> {
  const res = await fetchWithTimeout(`${API_URL}/fase7/graduate`, {
    method: 'POST',
    headers: getAuthHeaders(),
  });
  return handleResponse(res);
}

