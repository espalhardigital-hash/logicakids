/**
 * Tipos TypeScript — Fase 5: Operatoria Decimal y Conversiones
 * Espeja exactamente los schemas Pydantic del backend (fase4/schemas.py)
 */

// ─── Alternativa (Opción Múltiple — Desafíos 1 y 2) ──────────────────────────

export interface Fase4AlternativaOut {
  id: number;
  texto: string;
  orden?: number;
}

// ─── Tokens (Módulo 4 — Detective de Historias - Legado) ─────────────────────

export interface Fase4Token {
  id: number;
  texto: string;
  es_dato_relevante: boolean;
  categoria?: 'cantidad' | 'unidad' | 'operacion' | 'irrelevante';
}

// ─── Pregunta para el alumno ───────────────────────────────────────────────

export interface Fase4PasoCadenado {
  titulo: string;
  descripcion: string;
  respuesta_correcta: string;
}

export interface Fase4Pregunta {
  id?: number;
  modulo_id: number;
  nivel_id: number;
  enunciado: string;
  enunciado_seed?: string;
  tipo_pregunta:
    | 'respuesta_numerica'
    | 'multiple_opcion'
    | 'subrayado_tokens'
    | 'constructor_soluciones_chained';
  respuesta_correcta?: string;
  tiene_cronometro: boolean;
  tiempo_limite_segundos?: number;
  alternativas?: Fase4AlternativaOut[];
  payload_tokenizado?: Fase4Token[];
  pasos_encadenados?: Fase4PasoCadenado[];
  datos_numericos?: Record<string, any>;
  explicacion_referencia?: Record<string, any>;
  aciertos_acumulados?: number;
  intentos_totales?: number;
  porcentaje_actual?: number;
  cantidad_requerida?: number;
}

// ─── Respuesta del alumno ──────────────────────────────────────────────────

export interface Fase4AnswerPayload {
  modulo_id: number;
  nivel_id: number;
  pregunta_id?: number;
  enunciado_seed?: string;
  respuesta_dada?: string;
  alternativa_id?: number;
  tokens_seleccionados?: number[];
  paso_numero?: number;
  tiempo_respuesta_segundos?: number;
}

// ─── Resultado de respuesta ────────────────────────────────────────────────

export interface Fase4AnswerResult {
  es_correcta: boolean;
  respuesta_correcta?: string;
  explicacion?: Record<string, any>;
  feedback_error?: string;
  aciertos_acumulados: number;
  intentos_totales: number;
  porcentaje_actual: number;
  bloque_completado: boolean;
  fase_completada: boolean;
  // Bucle Espejo
  es_espejo: boolean;
  intentos_espejo_actuales: number;
  intentos_espejo_max: number;
  soporte_avanzado: boolean;
  // Early Exit
  early_exit?: boolean;
  errores_sesion?: number;
  max_errores_tolerados?: number;
  // Módulo 4
  tokens_correctos?: number[];
  // Módulo 5 (ahora Módulo 4 Constructor)
  paso_approved?: number;
  paso_aprobado?: number;
  valor_paso1_congelado?: string;
}

// ─── Dashboard ────────────────────────────────────────────────────────────

export interface Fase4NivelInfo {
  nivel_id: number;
  nombre: string;
  descripcion: string;
  estado: 'bloqueado' | 'en_progreso' | 'dominado';
  porcentaje: number;
  aciertos: number;
  requeridos: number;
  usa_cronometro: boolean;
}

export interface Fase4DesafioInfo {
  desafio_id: number;
  nombre: string;
  dificultad: 'estandar' | 'avanzada' | 'maestria';
  estado: 'bloqueado' | 'en_progreso' | 'dominado';
  porcentaje: number;
  aciertos: number;
  requeridos: number;
  tiempo_limite: number;
  max_errores: number;
}

export interface Fase4ModuloInfo {
  modulo_id: number;
  nombre: string;
  descripcion: string;
  icono: string;
  color: string;
  estado: 'bloqueado' | 'en_progreso' | 'dominado';
  porcentaje_global: number;
  niveles: Fase4NivelInfo[];
  desafios: Fase4DesafioInfo[];
}

export interface Fase4Dashboard {
  alumno_nombre: string;
  puntos_totales: number;
  modulos: Fase4ModuloInfo[];
  desafio_mixto_disponible: boolean;
  desafio_mixto_estado: 'bloqueado' | 'disponible' | 'completado';
}

// ─── Lectura / Teoría ─────────────────────────────────────────────────────

export interface Fase4Lectura {
  modulo_id: number;
  modulo_nombre?: string;
  nivel_id: number;
  titulo: string;
  parrafos: string[];
  diccionario?: Record<string, string>;
  ejemplos?: Array<{ 
    enunciado: string; 
    pasos?: Array<{ orden: number; texto: string }>;
    respuesta?: string;
  }>;
  interactivos?: Array<{
    enunciado?: string;
    pregunta?: string;
    pasos?: Array<{ orden: number; texto: string }>;
    respuesta: string;
    feedback_acierto: string;
    feedback_error: string;
    modo_compromiso?: boolean;
    tipo?: string;
    opciones?: Array<{ id: string; texto: string }>;
    explicacion_opciones?: Record<string, string>;
  }>;
  tip_pedagogico?: string;
}
