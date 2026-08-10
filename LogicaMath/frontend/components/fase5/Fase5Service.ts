/**
 * Servicio API — Fase 5: Fracciones, Porcentajes y Proporciones
 * Capa de comunicación con el backend de Fase 5.
 */

import { fetchWithTimeout } from '../../services/apiHelper';
import type {
  Fase5Dashboard,
  Fase5Pregunta,
  Fase5AnswerPayload,
  Fase5AnswerResult,
  Fase5Lectura,
  Fase5CerrarRescate,
} from './Fase5Types';

const API_URL = import.meta.env.VITE_API_URL || '/api';

function getAuthHeaders(): HeadersInit {
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
 * Obtiene el dashboard de Fase 5 con sus 4 módulos y su estado.
 */
export async function getFase5Dashboard(): Promise<Fase5Dashboard> {
  const key = 'dashboard-f5';
  return fetchDeduplicated(key, async () => {
    const res = await fetchWithTimeout(`${API_URL}/fase5/dashboard`, {
      headers: getAuthHeaders(),
    });
    return handleResponse<Fase5Dashboard>(res);
  });
}

/**
 * Obtiene la siguiente pregunta para un módulo y nivel específicos.
 */
export async function getFase5Question(
  moduloId: number,
  nivelId: number,
  reload: boolean = false
): Promise<Fase5Pregunta> {
  const key = `question-f5-${moduloId}-${nivelId}-${reload}`;
  return fetchDeduplicated(key, async () => {
    const res = await fetchWithTimeout(
      `${API_URL}/fase5/modulo/${moduloId}/nivel/${nivelId}/pregunta?reload=${reload}`,
      { headers: getAuthHeaders() }
    );
    return handleResponse<Fase5Pregunta>(res);
  });
}

/**
 * Envía la respuesta del alumno y recibe el resultado con feedback.
 */
export async function submitFase5Answer(
  payload: Fase5AnswerPayload
): Promise<Fase5AnswerResult> {
  const res = await fetchWithTimeout(`${API_URL}/fase5/responder`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  });
  const data = await handleResponse<Fase5AnswerResult>(res);
  if (data && !data.feedback_tutor && data.feedback_error) {
    data.feedback_tutor = data.feedback_error;
  }
  return data;
}

/**
 * Obtiene el contenido de lectura/teoría de un nivel.
 */
export async function getFase5Reading(
  moduloId: number,
  nivelId: number
): Promise<Fase5Lectura> {
  const key = `reading-f5-${moduloId}-${nivelId}`;
  return fetchDeduplicated(key, async () => {
    const res = await fetchWithTimeout(
      `${API_URL}/fase5/lectura/${moduloId}/nivel/${nivelId}`,
      { headers: getAuthHeaders() }
    );
    return handleResponse<Fase5Lectura>(res);
  });
}

/**
 * Cierra de forma segura el bucle de rescate (Mirror Loop).
 */
export async function submitFase5CloseRescue(
  moduloId: number,
  nivelId: number,
  preguntaId: number
): Promise<Fase5CerrarRescate> {
  const res = await fetchWithTimeout(`${API_URL}/fase5/cerrar-rescate`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ modulo_id: moduloId, nivel_id: nivelId, pregunta_id: preguntaId }),
  });
  return handleResponse<Fase5CerrarRescate>(res);
}

/**
 * Gradúa al alumno de Fase 5 a Fase 6.
 */
export async function graduateFase5(): Promise<{
  message: string;
  nueva_fase_id: number;
  nueva_fase_nombre: string;
}> {
  const res = await fetchWithTimeout(`${API_URL}/fase5/graduate`, {
    method: 'POST',
    headers: getAuthHeaders(),
  });
  return handleResponse(res);
}
