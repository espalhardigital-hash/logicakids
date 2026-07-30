import { fetchWithTimeout } from '../../services/apiHelper';
import type {
  Fase11Dashboard,
  Fase11Pregunta,
  Fase11AnswerPayload,
  Fase11AnswerResult,
  Fase11Lectura,
} from './Fase11Types';

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

export async function getFase11Dashboard(): Promise<Fase11Dashboard> {
  const key = 'dashboard-fase9';
  return fetchDeduplicated(key, async () => {
    const res = await fetchWithTimeout(`${API_URL}/fase9/dashboard`, {
      headers: getAuthHeaders(),
    });
    return handleResponse<Fase11Dashboard>(res);
  });
}

export async function getFase11Question(
  moduloId: number, nivelId: number, reload: boolean = false): Promise<Fase11Pregunta> {
  const key = `question-fase9-${moduloId}-${nivelId}-${reload}`;
  return fetchDeduplicated(key, async () => {
    const res = await fetchWithTimeout(
      `${API_URL}/fase9/modulo/${moduloId}/nivel/${nivelId}/pregunta?reload=${reload}`,
      { headers: getAuthHeaders() }
    );
    return handleResponse<Fase11Pregunta>(res);
  });
}

export async function submitFase11Answer(
  payload: Fase11AnswerPayload
): Promise<Fase11AnswerResult> {
  const res = await fetchWithTimeout(`${API_URL}/fase9/responder`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  });
  return handleResponse<Fase11AnswerResult>(res);
}

export async function closeFase11Rescate(
  moduloId: number, nivelId: number, preguntaId: number
): Promise<Fase11AnswerResult> {
  const res = await fetchWithTimeout(`${API_URL}/fase9/cerrar-rescate`, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify({ modulo_id: moduloId, nivel_id: nivelId, pregunta_id: preguntaId }),
  });
  return handleResponse<Fase11AnswerResult>(res);
}

export async function getFase11Reading(
  moduloId: number, nivelId: number, reload: boolean = false): Promise<Fase11Lectura> {
  const key = `reading-fase9-${moduloId}-${nivelId}`;
  return fetchDeduplicated(key, async () => {
    const res = await fetchWithTimeout(
      `${API_URL}/fase9/lectura/${moduloId}/nivel/${nivelId}`,
      { headers: getAuthHeaders() }
    );
    return handleResponse<Fase11Lectura>(res);
  });
}
