/**
 * Fase5Types.ts
 * ─────────────────────────────────────────────────────────────
 * Espeja exactamente los schemas de la Fase 4 y del backend (fase5/router.py)
 */

export interface Fase5AlternativaOut {
  id: number;
  texto: string;
}

export interface NonHomogeneousSector {
  id: number;
  weight: number;
  points: string;
  label?: string;
}

export interface Fase5Pregunta {
  id: number;
  enunciado: string;
  tipo_pregunta: 'multiple_opcion' | 'respuesta_numerica';
  alternativas?: Fase5AlternativaOut[];
  tiene_cronometro: boolean;
  tiempo_limite_segundos?: number;
  datos_numericos?: {
    tipo_visual?: 'pizza' | 'thermometer' | 'pie' | 'percentage_thermometer' | 'beaker' | 'percentage_beaker' | 'non_homogeneous_polygon' | 'shapes' | 'bar_chart' | 'contextual_bar' | 'fraction_percentage' | 'ratio_grid' | 'collection_grid' | 'fraction_strip' | 'equivalence_strip' | 'group_cards' | 'hundred_grid' | 'data_table' | 'ratio_table';
    cortes?: number;
    sombreados?: number[];
    nivel?: number;
    sectors?: NonHomogeneousSector[];
    target_value?: number;
    target_fraction_text?: string;
    viewBox?: string;
    theme?: 'battery' | 'download' | 'tank';
    [key: string]: any;
  };
  respuesta_correcta?: string;
  aciertos_acumulados?: number;
  intentos_totales?: number;
  porcentaje_actual?: number;
  cantidad_requerida?: number;
}

export interface Fase5AnswerPayload {
  modulo_id: number;
  nivel_id: number;
  pregunta_id: number;
  respuesta_dada?: string;
  alternativa_id?: number;
  tiempo_respuesta_segundos: number;
}

export interface Fase5AnswerResult {
  es_correcta: boolean;
  feedback_tutor?: string;
  feedback_error?: string;
  aciertos_acumulados: number;
  intentos_totales: number;
  porcentaje_actual: number;
  bloque_completado: boolean;
  fase_completada: boolean;
  early_exit: boolean;
  respuesta_correcta: string;
  explicacion?: { pasos?: { orden: number; texto: string }[] };
  explicacion_profunda?: string;
  pausa_obligatoria_segundos: number;
}

export interface Fase5NivelInfo {
  nivel_id: number;
  nombre: string;
  estado: 'bloqueado' | 'en_progreso' | 'dominado';
  aciertos: number;
  porcentaje: number;
}

export interface Fase5DesafioInfo {
  desafio_id: number;
  nombre: string;
  estado: 'bloqueado' | 'en_progreso' | 'dominado';
  aciertos: number;
  porcentaje: number;
  dificultad: 'estandar' | 'avanzada' | 'maestria';
  tiempo_limite: number;
  max_errores: number;
}

export interface Fase5ModuloInfo {
  modulo_id: number;
  nombre: string;
  descripcion: string;
  icono: string;
  color: string;
  estado: 'bloqueado' | 'en_progreso' | 'dominado';
  porcentaje_global: number;
  niveles: Fase5NivelInfo[];
  desafios: Fase5DesafioInfo[];
}

export interface Fase5Dashboard {
  alumno_nombre: string;
  puntos_totales: number;
  desafio_mixto_disponible: boolean;
  desafio_mixto_estado: 'bloqueado' | 'en_progreso' | 'completado';
  modulos: Fase5ModuloInfo[];
}

export interface Fase5Lectura {
  modulo_id: number;
  nivel_id: number;
  titulo: string;
  parrafos: string[];
  ejemplos?: { enunciado: string; respuesta?: string; pasos?: { orden: number; texto: string }[] }[];
  tip_pedagogico?: string;
  diccionario?: Record<string, string>;
  interactivos?: { enunciado: string; respuesta: string; feedback_acierto: string; feedback_error: string }[];
}

