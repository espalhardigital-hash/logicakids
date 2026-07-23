import React, { useEffect, useState } from 'react';
import { Globe, ChevronRight, ChevronDown, Layers, Trophy, Lock, Star } from 'lucide-react';

interface StaticSubLevel {
  id: number;
  name: string;
}

interface StaticChallenge {
  id: number;
  name: string;
  defaultTime: number;
  defaultQty: number;
}

interface StaticModule {
  seccion: number;
  modulo_id?: number;
  operacion: string;
  name: string;
  levels?: StaticSubLevel[];
  challenges?: StaticChallenge[];
  isFinalExam?: boolean;
}

interface StaticPhase {
  id: number;
  name: string;
  description: string;
  modules: StaticModule[];
}

interface PedagogyNavTreeProps {
  staticPhases: StaticPhase[];
  selectedPhaseId: number;
  selectedModule: StaticModule | null;
  onSelectGlobal: () => void;
  onSelectPhase: (phaseId: number) => void;
  onSelectModule: (phaseId: number, mod: StaticModule) => void;
  phaseHasChanges: (phaseId: number) => boolean;
  moduleHasChanges: (phaseId: number, mod: StaticModule) => boolean;
  moduleHasOverride: (phaseId: number, mod: StaticModule) => boolean;
  lockedPhaseId?: number;
}

export const PedagogyNavTree: React.FC<PedagogyNavTreeProps> = ({
  staticPhases, selectedPhaseId, selectedModule,
  onSelectGlobal, onSelectPhase, onSelectModule,
  phaseHasChanges, moduleHasChanges, moduleHasOverride,
  lockedPhaseId = 9
}) => {
  const [expanded, setExpanded] = useState<Set<number>>(new Set([selectedPhaseId]));

  useEffect(() => {
    setExpanded(prev => {
      if (prev.has(selectedPhaseId)) return prev;
      const next = new Set(prev);
      next.add(selectedPhaseId);
      return next;
    });
  }, [selectedPhaseId]);

  const toggleExpand = (phaseId: number) => {
    setExpanded(prev => {
      const next = new Set(prev);
      if (next.has(phaseId)) next.delete(phaseId); else next.add(phaseId);
      return next;
    });
  };

  return (
    <div className="flex flex-col gap-1 bg-white dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-3xl p-3 custom-scrollbar overflow-y-auto max-h-[75vh]">
      <button
        type="button"
        onClick={onSelectGlobal}
        className={`w-full flex items-center gap-2.5 px-3 py-2.5 rounded-xl text-sm font-bold transition-colors ${
          selectedPhaseId === 0
            ? 'bg-blue-500 text-white'
            : 'text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-white/5'
        }`}
      >
        <Globe size={16} /> Plataforma Global
      </button>

      <div className="h-px bg-slate-200 dark:bg-white/10 my-2 mx-1" />

      {staticPhases.map(phase => {
        const isLocked = phase.id === lockedPhaseId;
        const isPhaseSelected = selectedPhaseId === phase.id && !selectedModule;
        const isExpanded = expanded.has(phase.id) && !isLocked;
        const modified = !isLocked && phaseHasChanges(phase.id);

        return (
          <div key={phase.id} className="flex flex-col">
            <div
              className={`w-full flex items-center gap-1 rounded-xl transition-colors ${
                isPhaseSelected ? 'bg-blue-500 text-white' : 'text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-white/5'
              } ${isLocked ? 'opacity-50' : ''}`}
            >
              <button
                type="button"
                onClick={() => !isLocked && toggleExpand(phase.id)}
                disabled={isLocked}
                className="p-2 disabled:cursor-not-allowed"
                aria-label={isExpanded ? 'Colapsar módulos' : 'Expandir módulos'}
              >
                {isLocked ? <Lock size={14} /> : isExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
              </button>
              <button
                type="button"
                onClick={() => onSelectPhase(phase.id)}
                className="flex-1 text-left py-2 pr-3 text-sm font-bold flex items-center gap-2 disabled:cursor-not-allowed"
              >
                {phase.name.split(':')[0]}
                {modified && <span className="w-1.5 h-1.5 rounded-full bg-amber-400" />}
              </button>
            </div>

            {isExpanded && (
              <div className="flex flex-col gap-0.5 pl-7 pr-1 py-1">
                {phase.modules.map(mod => {
                  const isSelected = selectedPhaseId === phase.id && selectedModule?.name === mod.name;
                  const hasOverride = moduleHasOverride(phase.id, mod);
                  const modChanged = moduleHasChanges(phase.id, mod);
                  return (
                    <button
                      type="button"
                      key={mod.name}
                      onClick={() => onSelectModule(phase.id, mod)}
                      className={`flex items-center gap-2 px-2.5 py-1.5 rounded-lg text-xs font-bold text-left transition-colors ${
                        isSelected
                          ? 'bg-blue-500/15 text-blue-600 dark:text-blue-400'
                          : 'text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-white/5'
                      }`}
                    >
                      {mod.isFinalExam ? <Trophy size={13} className="text-amber-500 shrink-0" /> : <Layers size={13} className="shrink-0" />}
                      <span className="truncate">{mod.name.split(':')[0]}</span>
                      {modChanged && <span className="w-1.5 h-1.5 rounded-full bg-amber-400 shrink-0" />}
                      {hasOverride && <Star size={11} className="text-amber-500 shrink-0 ml-auto" />}
                    </button>
                  );
                })}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};
