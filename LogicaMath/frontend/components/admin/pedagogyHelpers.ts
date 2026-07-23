export interface StaticSubLevel {
  id: number;
  name: string;
}

export interface StaticChallenge {
  id: number;
  name: string;
  defaultTime: number;
  defaultQty: number;
}

export interface StaticModule {
  seccion: number;
  modulo_id?: number;
  operacion: string;
  name: string;
  levels?: StaticSubLevel[];
  challenges?: StaticChallenge[];
  isFinalExam?: boolean;
}

export interface StaticPhase {
  id: number;
  name: string;
  description: string;
  modules: StaticModule[];
}

export interface ModuleRow {
  seccion: number;
  operacion: string;
  isChallenge: boolean;
  subId: number;
  label: string;
  kind: 'level' | 'challenge' | 'final';
  defaultTime?: number;
  defaultQty?: number;
}

/**
 * Single source of truth for the seccion-id math that encodes
 * fase/módulo/nivel/desafío into ConfiguracionProgreso.seccion.
 * Fase 5+ use a wider id space (fase*1000 + modId*10 + subId for levels,
 * fase*10000 + modId*100 + subId for challenges) to avoid collisions.
 */
export const getModuleRows = (faseId: number, mod: StaticModule): ModuleRow[] => {
  if (mod.isFinalExam) {
    const ch = mod.challenges?.[0];
    return [{
      seccion: 99099,
      operacion: 'mixta',
      isChallenge: true,
      subId: ch?.id ?? 99,
      label: mod.name,
      kind: 'final',
      defaultTime: ch?.defaultTime,
      defaultQty: ch?.defaultQty,
    }];
  }

  const modId = mod.modulo_id || 1;

  const levelRows: ModuleRow[] = (mod.levels || []).map(l => ({
    seccion: faseId >= 5 ? faseId * 1000 + modId * 10 + l.id : modId * 100 + l.id,
    operacion: mod.operacion,
    isChallenge: false,
    subId: l.id,
    label: `Nivel ${l.id}: ${l.name}`,
    kind: 'level',
  }));

  const challengeRows: ModuleRow[] = (mod.challenges || []).map(c => ({
    seccion: faseId >= 5 ? faseId * 10000 + modId * 100 + c.id : modId * 1000 + c.id,
    operacion: 'mixta',
    isChallenge: true,
    subId: c.id,
    label: c.name,
    kind: 'challenge',
    defaultTime: c.defaultTime,
    defaultQty: c.defaultQty,
  }));

  return [...levelRows, ...challengeRows];
};

/**
 * Sentinel secciones for phase-wide defaults that are more granular than the
 * single "seccion 0" phase default: one slot per challenge order (Desafío 1/2/Final),
 * shared across every módulo of the phase. Negative so they never collide with a
 * real módulo/nivel/desafío seccion (those are always >= 0 per the math above).
 */
export const CHALLENGE_ORDER_SECCIONES: Record<number, number> = { 11: -11, 12: -12, 13: -13 };

/** Fixed seccion used by every phase's "Examen Final de Fase" módulo. */
export const FINAL_EXAM_SECCION = 99099;

export const findRowBySeccion = (
  phase: StaticPhase,
  seccion: number
): { mod: StaticModule; row: ModuleRow } | null => {
  for (const mod of phase.modules) {
    const rows = getModuleRows(phase.id, mod);
    const row = rows.find(r => r.seccion === seccion);
    if (row) return { mod, row };
  }
  return null;
};
