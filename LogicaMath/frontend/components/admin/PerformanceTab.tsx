import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Search, User, Shield, Check, Unlock, RotateCcw, 
  AlertTriangle, ChevronDown, ChevronUp, Loader2,
  CheckCircle2, CircleDot, Circle, Layers
} from 'lucide-react';
import { 
  searchAlumnos, getAlumnoProgress, overrideAlumnoProgress, overrideAlumnoProgressBulk,
  AlumnoSearchInfo
} from '../../services/storageService';
import { LevelMap } from './phaseMaps';
import { usePhaseMapContext } from './PhaseMapContext';

// ─── Helper: compute aggregate status from a list of level records ─────────────
type ProgressState = 'APROBADO' | 'EN_PROGRESO' | 'BLOQUEADO';

type OverrideItem = { fase_id: number; seccion: number; operacion: string };
type OverrideAction = 'approve' | 'unlock' | 'lock';
interface PendingOverride {
  title: string;
  warning: string;
  action: OverrideAction;
  actionKey: string;
  execute: (motivo: string) => Promise<void>;
}

const normalizeState = (raw: string | undefined | null): ProgressState => {
  if (!raw) return 'BLOQUEADO';
  const upper = raw.toUpperCase().replace(' ', '_');
  if (upper === 'APROBADO') return 'APROBADO';
  if (upper === 'EN_PROGRESO') return 'EN_PROGRESO';
  return 'BLOQUEADO';
};

function computeAggregateStatusForPhase(faseId: number, levels: LevelMap[], alumnoProgress: any[]): ProgressState {
  if (levels.length === 0) return 'BLOQUEADO';
  const states = levels.map((lvl) => {
    const prog = alumnoProgress.find(
      (p) => p.fase_id === faseId && p.seccion === lvl.seccion && p.operacion === lvl.operacion
    );
    return prog ? normalizeState(prog.estado) : 'BLOQUEADO';
  });
  if (states.every((s) => s === 'APROBADO')) return 'APROBADO';
  if (states.every((s) => s === 'BLOQUEADO')) return 'BLOQUEADO';
  return 'EN_PROGRESO';
}

// ─── Small Status Badge ────────────────────────────────────────────────────────
const StatusBadge: React.FC<{ status: string; size?: 'sm' | 'xs' }> = ({ status, size = 'xs' }) => {
  const normalized = normalizeState(status);
  const configs = {
    APROBADO: { icon: CheckCircle2, text: 'APROBADO', cls: 'bg-green-500/20 text-green-400 border-green-500/30' },
    EN_PROGRESO: { icon: CircleDot, text: 'EN PROGRESO', cls: 'bg-blue-500/20 text-blue-400 border-blue-500/30' },
    BLOQUEADO: { icon: Circle, text: 'BLOQUEADO', cls: 'bg-white/80 dark:bg-slate-800 text-slate-500 border-slate-200 dark:border-white/5' },
  };
  const config = configs[normalized] || configs.BLOQUEADO;
  const { icon: Icon, text, cls } = config;
  const textSize = size === 'sm' ? 'text-[11px]' : 'text-[10px]';
  return (
    <span className={`${textSize} font-bold px-2 py-0.5 rounded-full border flex items-center gap-1 ${cls}`}>
      <Icon size={size === 'sm' ? 11 : 9} />
      {text}
    </span>
  );
};

// ─── Bulk Action Buttons ───────────────────────────────────────────────────────
interface BulkActionButtonsProps {
  aggregateStatus: ProgressState;
  loading: boolean;
  onApprove: () => void;
  onUnlock: () => void;
  onLock: () => void;
}

const BulkActionButtons: React.FC<BulkActionButtonsProps> = ({
  aggregateStatus, loading, onApprove, onUnlock, onLock
}) => {
  if (loading) return <Loader2 size={14} className="animate-spin text-blue-400" />;
  return (
    <div className="flex items-center gap-1" onClick={(e) => e.stopPropagation()}>
      {aggregateStatus === 'BLOQUEADO' && (
        <button
          onClick={onUnlock}
          title="Liberar todo"
          className="px-3 py-1.5 rounded-lg bg-blue-600/20 hover:bg-blue-600 border border-blue-500/30 text-[13px] font-medium text-blue-400 hover:text-slate-900 dark:text-white transition-all flex items-center gap-1 cursor-pointer min-h-[32px]"
        >
          <Unlock size={13} /> Liberar
        </button>
      )}
      {aggregateStatus !== 'APROBADO' && (
        <button
          onClick={onApprove}
          title="Aprobar todo"
          className="px-3 py-1.5 rounded-lg bg-green-600/20 hover:bg-green-600 border border-green-500/30 text-[13px] font-medium text-green-400 hover:text-slate-900 dark:text-white transition-all flex items-center gap-1 cursor-pointer min-h-[32px]"
        >
          <Check size={13} /> Aprobar
        </button>
      )}
      {aggregateStatus !== 'BLOQUEADO' && (
        <button
          onClick={onLock}
          title="Restablecer todo"
          className="px-3 py-1.5 rounded-lg bg-red-500/10 hover:bg-red-500 border border-red-500/20 hover:border-red-500 text-[13px] font-medium text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white transition-all flex items-center gap-1 cursor-pointer min-h-[32px]"
        >
          <RotateCcw size={13} /> Restablecer
        </button>
      )}
    </div>
  );
};

// ─── Main Component ────────────────────────────────────────────────────────────
interface PerformanceTabProps {
  showConfirm?: (title: string, message: string, onConfirm: () => void) => void;
  showAlert?: (title: string, message: string, type?: 'info' | 'success' | 'error') => void;
}

const PerformanceTab: React.FC<PerformanceTabProps> = ({ showConfirm, showAlert }) => {
  const { phaseMaps: PHASE_MAPS } = usePhaseMapContext();
  // Search & Alumnos states
  const [searchQuery, setSearchQuery] = useState('');
  const [loadingSearch, setLoadingSearch] = useState(false);
  const [alumnos, setAlumnos] = useState<AlumnoSearchInfo[]>([]);
  const [selectedAlumno, setSelectedAlumno] = useState<AlumnoSearchInfo | null>(null);
  
  // Progress states
  const [alumnoProgress, setAlumnoProgress] = useState<any[]>([]);
  const [loadingProgress, setLoadingProgress] = useState(false);
  const [selectedFaseId, setSelectedFaseId] = useState<number>(1);
  const [activeModuleId, setActiveModuleId] = useState<Record<number, number>>({});

  // Action tracking: "level-{faseId}-{seccion}-{op}" | "module-{faseId}-{modId}" | "fase-{faseId}"
  const [actionInProgress, setActionInProgress] = useState<string | null>(null);

  // Override confirmation modal (Protocolo de Auditoría §6.3): motivo obligatorio + advertencia de cascada
  const [pendingOverride, setPendingOverride] = useState<PendingOverride | null>(null);
  const [overrideMotivo, setOverrideMotivo] = useState('');
  const [overrideSubmitting, setOverrideSubmitting] = useState(false);

  // Conjunto retrógado: todos los niveles de la fase en orden hasta (e incluyendo) el objetivo.
  // El orden canónico solo vive en el phase-map del frontend; el backend ejecuta lo que se le envía.
  const computeRetroSet = (faseId: number, seccion: number, operacion: string): OverrideItem[] => {
    const phase = PHASE_MAPS.find((p) => p.id === faseId);
    if (!phase) return [{ fase_id: faseId, seccion, operacion }];
    const flat: OverrideItem[] = [];
    for (const mod of phase.modules) {
      for (const lvl of mod.levels) {
        flat.push({ fase_id: faseId, seccion: lvl.seccion, operacion: lvl.operacion });
        if (lvl.seccion === seccion && lvl.operacion === operacion) return flat;
      }
    }
    return flat.length ? flat : [{ fase_id: faseId, seccion, operacion }];
  };

  // Load all students on mount (UX-4)
  useEffect(() => {
    const loadAllAlumnos = async () => {
      setLoadingSearch(true);
      try {
        const res = await searchAlumnos('');
        setAlumnos(res?.data || []);
      } catch (e) {
        console.error(e);
      } finally {
        setLoadingSearch(false);
      }
    };
    loadAllAlumnos();
  }, []);

  // Search trigger on input change
  useEffect(() => {
    if (searchQuery.trim() === '') return; // Skip on empty, we already loaded all
    const delayDebounceFn = setTimeout(() => {
      handleSearch();
    }, 400);
    return () => clearTimeout(delayDebounceFn);
  }, [searchQuery]);

  const handleSearch = async () => {
    setLoadingSearch(true);
    try {
      const res = await searchAlumnos(searchQuery);
      setAlumnos(res?.data || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingSearch(false);
    }
  };

  const fetchProgress = async (alumnoId: number) => {
    setLoadingProgress(true);
    try {
      const res = await getAlumnoProgress(alumnoId);
      setAlumnoProgress(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingProgress(false);
    }
  };

  const handleSelectAlumno = (alumno: AlumnoSearchInfo) => {
    setSelectedAlumno(alumno);
    fetchProgress(alumno.alumno_id);
    setSelectedFaseId(alumno.fase_actual_id || 1);
    
    // Set first module as active for each phase
    const defaultModules: Record<number, number> = {};
    PHASE_MAPS.forEach((phase) => {
      if (phase.modules.length > 0) {
        defaultModules[phase.id] = phase.modules[0].id;
      }
    });
    setActiveModuleId(defaultModules);
  };

  const ACTION_VERB: Record<OverrideAction, string> = {
    approve: 'Aprobar', unlock: 'Liberar', lock: 'Restablecer / Bloquear',
  };

  const runOverride = async (actionKey: string, fn: () => Promise<void>) => {
    setActionInProgress(actionKey);
    try {
      await fn();
      if (selectedAlumno) await fetchProgress(selectedAlumno.alumno_id);
    } catch (e: any) {
      console.error(e);
      const msg = e?.message || 'Error al aplicar la acción de override.';
      if (showAlert) showAlert('Error', msg, 'error');
      else alert(msg);
    } finally {
      setActionInProgress(null);
    }
  };

  // ── Single-level override ──────────────────────────────────────────────────
  const handleApplyOverride = (
    faseId: number, seccion: number, operacion: string, action: OverrideAction
  ) => {
    if (!selectedAlumno) return;
    const alumnoId = selectedAlumno.alumno_id;
    const actionKey = `level-${faseId}-${seccion}-${operacion}`;
    if (action === 'approve') {
      const retro = computeRetroSet(faseId, seccion, operacion);
      const anteriores = Math.max(retro.length - 1, 0);
      setPendingOverride({
        title: `${ACTION_VERB[action]} nivel`,
        warning: `Aprobación Retrógada: se declararán APROBADOS este nivel y los ${anteriores} nivel(es) anterior(es) de la Fase ${faseId}, para mantener la consistencia lineal del progreso.`,
        action, actionKey,
        execute: (motivo) => runOverride(actionKey, () =>
          overrideAlumnoProgressBulk(alumnoId, { items: retro, action: 'approve', motivo, expand_phase: false }).then(() => {})),
      });
    } else {
      setPendingOverride({
        title: `${ACTION_VERB[action]} nivel`,
        warning: action === 'lock'
          ? 'Esta acción regresará el nivel a BLOQUEADO y reiniciará su progreso a cero.'
          : 'Esta acción liberará el nivel (EN_PROGRESO) sin exigir completar los niveles previos.',
        action, actionKey,
        execute: (motivo) => runOverride(actionKey, () =>
          overrideAlumnoProgress(alumnoId, { fase_id: faseId, seccion, operacion, action, motivo }).then(() => {})),
      });
    }
  };

  // ── Module-level bulk override ─────────────────────────────────────────────
  const handleModuleBulk = (
    faseId: number, modId: number, levels: LevelMap[], action: OverrideAction
  ) => {
    if (!selectedAlumno) return;
    const alumnoId = selectedAlumno.alumno_id;
    const actionKey = `module-${faseId}-${modId}`;
    const items = levels.map((lvl) => ({ fase_id: faseId, seccion: lvl.seccion, operacion: lvl.operacion }));
    setPendingOverride({
      title: `${ACTION_VERB[action]} módulo completo`,
      warning: `Se aplicará '${ACTION_VERB[action]}' a los ${items.length} nivel(es) del módulo.` +
        (action === 'approve' ? ' Los niveles quedarán APROBADOS.' : ''),
      action, actionKey,
      execute: (motivo) => runOverride(actionKey, () =>
        overrideAlumnoProgressBulk(alumnoId, { items, action, motivo, expand_phase: false }).then(() => {})),
    });
  };

  // ── Phase-level bulk override ──────────────────────────────────────────────
  const handleFaseBulk = (
    faseId: number, allLevels: LevelMap[], action: OverrideAction
  ) => {
    if (!selectedAlumno) return;
    const alumnoId = selectedAlumno.alumno_id;
    const actionKey = `fase-${faseId}`;
    const items = allLevels.map((lvl) => ({ fase_id: faseId, seccion: lvl.seccion, operacion: lvl.operacion }));
    setPendingOverride({
      title: `${ACTION_VERB[action]} Fase ${faseId} completa`,
      warning: `Se aplicará '${ACTION_VERB[action]}' a TODA la Fase ${faseId} (${items.length} niveles del mapa` +
        (action === 'approve' ? ', más cualquier bloque activo adicional no mapeado).' : ').'),
      action, actionKey,
      execute: (motivo) => runOverride(actionKey, () =>
        overrideAlumnoProgressBulk(alumnoId, { items, action, motivo, expand_phase: action === 'approve' }).then(() => {})),
    });
  };

  // ── Render ─────────────────────────────────────────────────────────────────
  return (
    <div className="w-full flex flex-col gap-6 text-slate-900 dark:text-white select-none">
      
      {/* Top Header Panel */}
      <div className="flex flex-col md:flex-row md:items-center justify-between bg-white dark:bg-white/5 backdrop-blur-2xl border border-slate-200 dark:border-white/10 p-6 rounded-[2.2rem] shadow-2xl">
        <div className="w-full">
          <h2 className="text-3xl font-black text-slate-900 dark:text-white flex items-center gap-3">
            <div className="p-2.5 bg-red-500/20 rounded-2xl border border-red-500/30">
              <Shield className="text-red-400" size={24} />
            </div>
            Rendimiento Estudiantil Avanzado
          </h2>
          <p className="text-slate-500 dark:text-slate-400 text-sm mt-1">
            Busca un alumno para gestionar su avance. Usa los controles de Fase y Módulo para acciones masivas.
          </p>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        
        {/* Left Column: Student search */}
        <div className="lg:col-span-1 bg-white dark:bg-white/5 backdrop-blur-2xl border border-slate-200 dark:border-white/10 p-5 rounded-[2.2rem] shadow-2xl flex flex-col gap-4">
          <h3 className="text-base font-black text-slate-500 dark:text-slate-400 uppercase tracking-widest px-2">Buscador de Alumnos</h3>
          
          <div className="relative">
            <Search size={18} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" />
            <input
              type="text"
              placeholder="Buscar por nombre o email..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-white/80 dark:bg-slate-950/60 border border-slate-200 dark:border-white/10 rounded-2xl py-3.5 pl-12 pr-4 text-base font-bold placeholder-slate-500 text-slate-900 dark:text-white focus:outline-none focus:border-blue-500/50 transition-colors"
            />
          </div>

          <div className="flex flex-col gap-2 max-h-[50vh] overflow-y-auto pr-1 custom-scrollbar">
            {loadingSearch && (
              <div className="flex items-center justify-center py-10">
                <Loader2 className="text-blue-500 animate-spin" size={24} />
              </div>
            )}
            {!loadingSearch && alumnos.length === 0 && searchQuery.trim() !== '' && (
              <p className="text-sm text-slate-500 text-center py-10">No se encontraron alumnos.</p>
            )}
            {!loadingSearch && alumnos.length === 0 && searchQuery.trim() === '' && (
              <p className="text-sm text-slate-500 text-center py-10">No hay alumnos registrados aún.</p>
            )}
            {alumnos.map((a) => {
              const isSelected = selectedAlumno?.id === a.id;
              return (
                <button
                  key={a.id}
                  onClick={() => handleSelectAlumno(a)}
                  className={`w-full text-left p-4 rounded-2xl border transition-all flex flex-col gap-1 cursor-pointer ${
                    isSelected 
                      ? 'bg-blue-600/20 text-slate-900 dark:text-white border-blue-500/40 shadow-inner' 
                      : 'bg-white dark:bg-white/5 border-slate-200 dark:border-white/5 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-100 dark:bg-white/10'
                  }`}
                >
                  <span className="text-sm font-black">{a.alumno_nombre}</span>
                  <span className="text-xs text-slate-500 font-bold">{a.email}</span>
                  <span className="text-[10px] bg-white/80 dark:bg-slate-800 text-slate-500 dark:text-slate-400 px-2 py-0.5 rounded-full border border-slate-200 dark:border-white/5 self-start mt-1 font-bold">
                    Fase Actual: {a.fase_actual_id}
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Right Column: Detailed progress */}
        <div className="lg:col-span-2 flex flex-col gap-6">
          {!selectedAlumno ? (
            <div className="bg-white dark:bg-white/5 backdrop-blur-2xl border border-slate-200 dark:border-white/10 p-12 rounded-[2.2rem] shadow-2xl flex flex-col items-center justify-center text-center min-h-[40vh]">
              <User size={48} className="text-slate-600 mb-4" />
              <h4 className="text-base font-black text-slate-600 dark:text-slate-300">Ningún Alumno Seleccionado</h4>
              <p className="text-sm text-slate-500 max-w-xs mt-1">
                Selecciona un alumno de la lista de la izquierda para ver su rendimiento académico detallado y gestionar sus permisos de fase.
              </p>
            </div>
          ) : (
            <div className="bg-white dark:bg-white/5 backdrop-blur-2xl border border-slate-200 dark:border-white/10 p-8 rounded-[2.2rem] shadow-2xl flex flex-col gap-6">
              
              {/* Student profile card */}
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white/80 dark:bg-slate-950/40 p-5 rounded-3xl border border-slate-200 dark:border-white/5">
                <div className="flex items-center gap-4">
                  <div className="p-3 bg-blue-500/20 rounded-2xl border border-blue-500/30">
                    <User className="text-blue-400" size={24} />
                  </div>
                  <div>
                    <h4 className="text-xl font-black text-slate-900 dark:text-white">{selectedAlumno.alumno_nombre}</h4>
                    <p className="text-sm text-slate-500 font-bold">{selectedAlumno.email}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="glass-panel border border-slate-200 dark:border-white/10 px-4 py-2 rounded-xl text-center">
                    <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider block">Fase Actual</span>
                    <span className="text-base font-black text-blue-400">Fase {selectedAlumno.fase_actual_id}</span>
                  </div>
                  <div className="glass-panel border border-slate-200 dark:border-white/10 px-4 py-2 rounded-xl text-center">
                    <span className="text-[10px] text-slate-500 font-bold uppercase tracking-wider block">Estado</span>
                    <span className="text-base font-black text-green-400">{selectedAlumno.estado}</span>
                  </div>
                </div>
              </div>

              {/* Progress Drilldown */}
              <div className="flex flex-col gap-4 border-t border-slate-200 dark:border-white/5 pt-4">
                <h4 className="text-base font-black text-slate-500 dark:text-slate-400 uppercase tracking-widest px-1">Progreso y Control de Maestría</h4>

                {loadingProgress ? (
                  <div className="flex items-center justify-center py-20">
                    <Loader2 className="text-blue-500 animate-spin" size={32} />
                  </div>
                ) : (
                  <div className="flex flex-col gap-5">
                    {/* Horizontal Phase Tabs */}
                    <div className="flex overflow-x-auto custom-scrollbar pb-2 gap-2">
                      {PHASE_MAPS.map((phase) => {
                        const allFaseLevels = phase.modules.flatMap((m) => m.levels);
                        const faseStatus = computeAggregateStatusForPhase(phase.id, allFaseLevels, alumnoProgress);
                        const isSelected = selectedFaseId === phase.id;
                        
                        return (
                          <button
                            key={phase.id}
                            onClick={() => setSelectedFaseId(phase.id)}
                            className={`shrink-0 flex items-center gap-2 px-4 py-2.5 rounded-2xl border transition-all ${
                              isSelected 
                                ? 'bg-blue-600 text-white border-blue-500 shadow-[0_5px_15px_rgba(37,99,235,0.3)]' 
                                : 'bg-white dark:bg-white/5 border-slate-200 dark:border-white/5 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/10'
                            }`}
                          >
                            <span className={`text-sm font-black whitespace-nowrap ${isSelected ? 'text-white' : ''}`}>Fase {phase.id}</span>
                            {!isSelected && <StatusBadge status={faseStatus} size="xs" />}
                          </button>
                        );
                      })}
                    </div>

                    {/* Active Phase Content */}
                    {(PHASE_MAPS || []).filter(p => p.id === selectedFaseId).map((phase) => {
                      const allFaseLevels = phase.modules.flatMap((m) => m.levels);
                      const faseStatus = computeAggregateStatusForPhase(phase.id, allFaseLevels, alumnoProgress);
                      const faseBulkKey = `fase-${phase.id}`;
                      const faseBulkLoading = actionInProgress === faseBulkKey;

                      return (
                        <div key={phase.id} className="rounded-3xl border border-slate-200 dark:border-white/5 bg-white/80 dark:bg-slate-950/20 overflow-hidden flex flex-col">
                          
                          {/* Phase Header for Bulk Actions */}
                          <div className="flex justify-between items-center p-4 glass-panel border-b border-slate-200 dark:border-white/5 bg-slate-50 dark:bg-slate-900/50">
                            <div className="flex items-center gap-3">
                              <Layers size={18} className="text-blue-500" />
                              <span className="text-base font-black text-slate-900 dark:text-white">{phase.name}</span>
                              <StatusBadge status={faseStatus} size="sm" />
                            </div>
                            <BulkActionButtons
                              aggregateStatus={faseStatus}
                              loading={faseBulkLoading}
                              onApprove={() => handleFaseBulk(phase.id, allFaseLevels, 'approve')}
                              onUnlock={() => handleFaseBulk(phase.id, allFaseLevels, 'unlock')}
                              onLock={() => handleFaseBulk(phase.id, allFaseLevels, 'lock')}
                            />
                          </div>

                          {/* Modules Horizontal Tabs */}
                          <div className="flex overflow-x-auto custom-scrollbar border-b border-slate-200 dark:border-white/5 bg-slate-50/50 dark:bg-slate-900/20">
                            {phase.modules.map((mod) => {
                              const isActive = activeModuleId[phase.id] === mod.id;
                              const modStatus = computeAggregateStatusForPhase(phase.id, mod.levels, alumnoProgress);
                              return (
                                <button
                                  key={mod.id}
                                  onClick={() => setActiveModuleId(prev => ({ ...prev, [phase.id]: mod.id }))}
                                  className={`shrink-0 flex items-center gap-2 px-4 py-3 border-b-2 transition-all cursor-pointer ${
                                    isActive 
                                      ? 'border-blue-500 bg-white dark:bg-white/5 text-blue-600 dark:text-blue-400' 
                                      : 'border-transparent text-slate-500 hover:text-slate-700 dark:hover:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/5'
                                  }`}
                                >
                                  <h5 className="text-xs font-black truncate">{mod.name}</h5>
                                  <StatusBadge status={modStatus} size="xs" />
                                </button>
                              );
                            })}
                          </div>

                          <div className="p-4 flex flex-col gap-4">
                            {(phase.modules || []).filter(m => m.id === activeModuleId[phase.id]).map((mod) => {
                              const modStatus = computeAggregateStatusForPhase(phase.id, mod.levels, alumnoProgress);
                              const moduleBulkKey = `module-${phase.id}-${mod.id}`;
                              const moduleBulkLoading = actionInProgress === moduleBulkKey;

                              return (
                                <div key={mod.id} className="bg-white/80 dark:bg-slate-950/40 rounded-2xl border border-slate-200 dark:border-white/5 overflow-hidden">
                                  
                                  {/* Module header actions */}
                                  <div className="flex items-center justify-between p-3 glass-panel/30 border-b border-slate-200 dark:border-white/5">
                                    <div className="flex items-center gap-2 flex-1 min-w-0">
                                      <h5 className="text-sm font-black text-slate-600 dark:text-slate-300 truncate">Niveles del {mod.name}</h5>
                                    </div>
                                    <div className="ml-2 shrink-0">
                                      <BulkActionButtons
                                        aggregateStatus={modStatus}
                                        loading={moduleBulkLoading}
                                        onApprove={() => handleModuleBulk(phase.id, mod.id, mod.levels, 'approve')}
                                        onUnlock={() => handleModuleBulk(phase.id, mod.id, mod.levels, 'unlock')}
                                        onLock={() => handleModuleBulk(phase.id, mod.id, mod.levels, 'lock')}
                                      />
                                    </div>
                                  </div>

                                  {/* Individual levels */}
                                  <div className="p-3 flex flex-col gap-2">
                                    {mod.levels.map((lvl) => {
                                        const prog = alumnoProgress.find(
                                          (p) => p.fase_id === phase.id && p.seccion === lvl.seccion && p.operacion === lvl.operacion
                                        );
                                        const state = normalizeState(prog ? prog.estado : 'BLOQUEADO');
                                        const pct = prog ? prog.porcentaje_actual : 0;
                                        const isApprovedByAdmin = prog ? prog.aprobado_por_admin : false;
                                        const actionKey = `level-${phase.id}-${lvl.seccion}-${lvl.operacion}`;
                                        const loadingThis = actionInProgress === actionKey;

                                        return (
                                          <div
                                            key={lvl.id}
                                            className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-3 glass-panel/20 border border-slate-200 dark:border-white/5 rounded-xl"
                                          >
                                            {/* Level metadata */}
                                            <div className="flex-1 min-w-0">
                                              <div className="flex items-center gap-2">
                                                <span className={`text-xs font-black ${lvl.isChallenge ? 'text-amber-400' : 'text-slate-600 dark:text-slate-300'}`}>
                                                  {lvl.isChallenge ? 'Desafío' : 'Nivel'} {lvl.id}: {lvl.name}
                                                </span>
                                                {isApprovedByAdmin && (
                                                  <span className="text-[9px] bg-amber-500/20 border border-amber-500/30 text-amber-300 px-1.5 py-0.5 rounded-full font-black flex items-center gap-1">
                                                    <AlertTriangle size={10} /> Aprobado por Admin
                                                  </span>
                                                )}
                                              </div>
                                              <div className="flex items-center gap-2 mt-1">
                                                <StatusBadge status={state} />
                                                {state !== 'BLOQUEADO' && (
                                                  <>
                                                    <span className="text-xs text-slate-500 font-bold">{pct}% Aciertos</span>
                                                    {/* Progress bar (UX-5) */}
                                                    <div className="w-20 h-1.5 bg-slate-200 dark:bg-slate-700 rounded-full overflow-hidden">
                                                      <div
                                                        className={`h-full rounded-full transition-all ${
                                                          pct >= 80 ? 'bg-green-500' :
                                                          pct >= 60 ? 'bg-blue-500' :
                                                          pct >= 40 ? 'bg-amber-500' :
                                                          'bg-red-500'
                                                        }`}
                                                        style={{ width: `${Math.min(pct, 100)}%` }}
                                                      />
                                                    </div>
                                                  </>
                                                )}
                                                {prog && prog.ultimos_errores && prog.ultimos_errores.length > 0 && (
                                                  <div className="flex gap-1 ml-2">
                                                    {prog.ultimos_errores.map((err: any, idx: number) => (
                                                      <span key={idx} className="text-[9px] bg-red-500/10 border border-red-500/20 text-red-400 px-1.5 py-0.5 rounded flex items-center gap-1 font-bold">
                                                        <AlertTriangle size={8} /> {err.tipo} ({err.count})
                                                      </span>
                                                    ))}
                                                  </div>
                                                )}
                                              </div>
                                            </div>

                                            {/* Individual controls */}
                                            <div className="flex items-center gap-1.5 self-end sm:self-center">
                                              {loadingThis ? (
                                                <Loader2 size={16} className="animate-spin text-blue-400 mr-4" />
                                              ) : (
                                                <>
                                                  {state === 'BLOQUEADO' && (
                                                    <button
                                                      onClick={() => handleApplyOverride(phase.id, lvl.seccion, lvl.operacion, 'unlock')}
                                                      className="px-3 py-1.5 rounded-lg bg-blue-600/20 hover:bg-blue-600 border border-blue-500/30 text-[13px] font-medium text-blue-400 hover:text-slate-900 dark:text-white transition-all flex items-center gap-1 cursor-pointer min-h-[32px]"
                                                    >
                                                      <Unlock size={13} /> Liberar
                                                    </button>
                                                  )}
                                                  {state !== 'APROBADO' && (
                                                    <button
                                                      onClick={() => handleApplyOverride(phase.id, lvl.seccion, lvl.operacion, 'approve')}
                                                      className="px-3 py-1.5 rounded-lg bg-green-600/20 hover:bg-green-600 border border-green-500/30 text-[13px] font-medium text-green-400 hover:text-slate-900 dark:text-white transition-all flex items-center gap-1 cursor-pointer min-h-[32px]"
                                                    >
                                                      <Check size={13} /> Aprobar (90%)
                                                    </button>
                                                  )}
                                                  {state !== 'BLOQUEADO' && (
                                                    <button
                                                      onClick={() => handleApplyOverride(phase.id, lvl.seccion, lvl.operacion, 'lock')}
                                                      className="px-3 py-1.5 rounded-lg bg-red-500/10 hover:bg-red-500 border border-red-500/20 hover:border-red-500 text-[13px] font-medium text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white transition-all flex items-center gap-1 cursor-pointer min-h-[32px]"
                                                    >
                                                      <RotateCcw size={13} /> Restablecer
                                                    </button>
                                                  )}
                                                </>
                                              )}
                                            </div>
                                          </div>
                                        );
                                      })}
                                    </div>
                                </div>
                              );
                            })}
                          </div>

                        </div>
                      );
                    })}
                  </div>
                )}
              </div>

            </div>
          )}
        </div>

      </div>

      {/* Modal de Confirmación de Override (Protocolo de Auditoría §6.3) */}
      {pendingOverride && (
        <div
          className="fixed inset-0 z-[100] flex items-center justify-center p-4 backdrop-blur-sm bg-slate-900/60"
          onClick={() => { if (!overrideSubmitting) { setPendingOverride(null); setOverrideMotivo(''); } }}
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.96 }}
            animate={{ opacity: 1, scale: 1 }}
            onClick={(e) => e.stopPropagation()}
            className="w-full max-w-lg bg-white dark:bg-slate-900 border border-slate-200 dark:border-white/10 rounded-3xl shadow-2xl p-6 flex flex-col gap-4"
          >
            <div className="flex items-center gap-3">
              <div className="p-2.5 bg-amber-500/20 rounded-2xl border border-amber-500/30">
                <AlertTriangle className="text-amber-400" size={22} />
              </div>
              <h3 className="text-xl font-black text-slate-900 dark:text-white">{pendingOverride.title}</h3>
            </div>
            <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-600 dark:text-amber-300 text-sm leading-relaxed">
              {pendingOverride.warning}
            </div>
            <div className="flex flex-col gap-1.5">
              <label className="text-xs font-black text-slate-500 dark:text-slate-400 uppercase">
                Motivo pedagógico (obligatorio, mín. 10 caracteres)
              </label>
              <textarea
                value={overrideMotivo}
                onChange={(e) => setOverrideMotivo(e.target.value)}
                onKeyDown={(e) => {
                  if ((e.key === 'Enter' && !e.shiftKey) || (e.key === 'Enter' && e.ctrlKey)) {
                    e.preventDefault();
                    if (overrideMotivo.trim().length >= 10 && !overrideSubmitting && pendingOverride) {
                      const p = pendingOverride;
                      setOverrideSubmitting(true);
                      p.execute(overrideMotivo.trim()).finally(() => {
                        setOverrideSubmitting(false);
                        setPendingOverride(null);
                        setOverrideMotivo('');
                      });
                    }
                  }
                }}
                rows={3}
                autoFocus
                placeholder="Ej: Estudiante avanzado de 5º grado, demuestra dominio inicial."
                className="w-full bg-white/80 dark:bg-slate-950 border border-slate-200 dark:border-white/10 rounded-xl p-3 text-sm text-slate-900 dark:text-white focus:outline-none focus:border-blue-500/50 resize-none"
              />
              <span className={`text-[11px] font-bold ${overrideMotivo.trim().length >= 10 ? 'text-emerald-500' : 'text-slate-400'}`}>
                {overrideMotivo.trim().length}/10
              </span>
            </div>
            <div className="flex items-center justify-end gap-3 pt-1">
              <button
                type="button"
                disabled={overrideSubmitting}
                onClick={() => { setPendingOverride(null); setOverrideMotivo(''); }}
                className="px-4 py-2 rounded-xl text-sm font-bold text-slate-500 hover:text-slate-700 dark:hover:text-white transition-colors disabled:opacity-40"
              >
                Cancelar
              </button>
              <button
                type="button"
                disabled={overrideMotivo.trim().length < 10 || overrideSubmitting}
                onClick={async () => {
                  const p = pendingOverride;
                  setOverrideSubmitting(true);
                  try {
                    await p.execute(overrideMotivo.trim());
                  } finally {
                    setOverrideSubmitting(false);
                    setPendingOverride(null);
                    setOverrideMotivo('');
                  }
                }}
                className="px-5 py-2 rounded-xl text-sm font-black text-white bg-red-600 hover:bg-red-500 disabled:opacity-40 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
              >
                {overrideSubmitting ? <Loader2 size={16} className="animate-spin" /> : null}
                Confirmar Intervención
              </button>
            </div>
          </motion.div>
        </div>
      )}

    </div>
  );
};

export default PerformanceTab;
