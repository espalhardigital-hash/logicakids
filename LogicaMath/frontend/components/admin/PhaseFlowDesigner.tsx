import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Layers, Settings, ChevronUp, ChevronDown, Target } from 'lucide-react';
import { ConfiguracionProgreso } from '../../types';

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

interface PhaseFlowDesignerProps {
  selectedPhaseId: number;
  selectedModule: StaticModule | null;
  selectPhase: (phaseId: number) => void;
  selectModule: (phaseId: number, mod: StaticModule) => void;
  expandedCategories: Record<string, boolean>;
  toggleCategory: (cat: string) => void;
  draftModularConfigs: ConfiguracionProgreso[];
  isPhaseModified: (phaseId: number) => boolean;
  isModuleModified: (phaseId: number, seccion: number, operacion: string) => boolean;
  
  // Sub-navigation inside module
  selectedSubLevelId: number | null;
  setSelectedSubLevelId: (lvlId: number | null) => void;
  isSelectedChallenge: boolean;
  setIsSelectedChallenge: (isCh: boolean) => void;
  
  staticPhases: StaticPhase[];
}

export const PhaseFlowDesigner: React.FC<PhaseFlowDesignerProps> = ({
  selectedPhaseId, selectedModule, selectPhase, selectModule,
  expandedCategories, toggleCategory, draftModularConfigs,
  isPhaseModified, isModuleModified,
  selectedSubLevelId, setSelectedSubLevelId, isSelectedChallenge, setIsSelectedChallenge,
  staticPhases
}) => {
  const activePhase = staticPhases.find(p => p.id === selectedPhaseId);

  const basicas = activePhase?.modules.filter(m => !m.isFinalExam && ['suma', 'resta'].includes(m.operacion)) || [];
  const avanzadas = activePhase?.modules.filter(m => !m.isFinalExam && ['multiplicacion', 'division'].includes(m.operacion)) || [];
  const desafios = activePhase?.modules.filter(m => !m.isFinalExam && !['suma', 'resta', 'multiplicacion', 'division'].includes(m.operacion)) || [];
  const finalExam = activePhase?.modules.filter(m => m.isFinalExam) || [];

  const checkModuleIsModifiedLocal = (mod: StaticModule) => {
    const modId = mod.modulo_id || 1;
    const levelIds = mod.levels?.map(l => l.id) || [];
    const challengeIds = mod.challenges?.map(c => c.id) || [];
    for (const lid of levelIds) {
      if (isModuleModified(selectedPhaseId, modId * 100 + lid, mod.operacion)) return true;
    }
    for (const cid of challengeIds) {
      if (isModuleModified(selectedPhaseId, modId * 1000 + cid, 'mixta')) return true;
    }
    return false;
  };

  const checkModuleHasActiveOverride = (mod: StaticModule) => {
    const modId = mod.modulo_id || 1;
    return draftModularConfigs.some(
      c => c.fase_id === selectedPhaseId && 
           (Math.floor(c.seccion / 100) === modId || Math.floor(c.seccion / 1000) === modId) &&
           c.activo !== false
    );
  };

  const renderCategory = (id: string, title: string, iconColor: string, mods: StaticModule[]) => {
    if (mods.length === 0) return null;
    const isExpanded = expandedCategories[id] !== false;
    
    return (
      <div key={id} className="bg-white/50 dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-2xl overflow-hidden shadow-sm">
        <button 
          type="button"
          onClick={() => toggleCategory(id)}
          className="w-full flex justify-between items-center px-5 py-4 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors"
        >
          <div className="flex items-center gap-3">
            <div className={`p-2 rounded-lg ${iconColor}`}>
              <Layers size={18} />
            </div>
            <div className="text-left">
              <h4 className="text-sm font-bold text-slate-900 dark:text-white">{title}</h4>
              <p className="text-xs text-slate-500 dark:text-slate-400">{mods.length} operaciones disponibles</p>
            </div>
          </div>
          {isExpanded ? <ChevronUp size={20} className="text-slate-400" /> : <ChevronDown size={20} className="text-slate-400" />}
        </button>

        <AnimatePresence initial={false}>
          {isExpanded && (
            <motion.div 
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="border-t border-slate-200 dark:border-white/5"
            >
              <div className="p-4 flex gap-3 flex-wrap">
                {mods.map(mod => {
                  const isModModified = checkModuleIsModifiedLocal(mod);
                  const hasOverride = checkModuleHasActiveOverride(mod);

                  return (
                    <button 
                      type="button"
                      key={mod.name}
                      onClick={() => selectModule(selectedPhaseId, mod)}
                      className={`px-5 py-2.5 rounded-xl font-black text-xs border transition-all flex items-center gap-2 ${
                        selectedModule?.name === mod.name
                          ? 'bg-blue-500 text-white border-blue-500 shadow-md shadow-blue-500/20' 
                          : 'bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700/80'
                      }`}
                    >
                      <Layers size={14} /> {mod.name.split(':')[0]}
                      {isModModified && <div className="w-2 h-2 rounded-full bg-amber-400 animate-pulse ml-1" />}
                      {hasOverride && (
                        <span
                          className={`text-[10px] px-1.5 py-0.5 rounded-full ml-1 cursor-help flex items-center justify-center ${
                            selectedModule?.name === mod.name ? 'bg-white/20' : 'bg-amber-500/20 text-amber-500 border border-amber-500/20'
                          }`}
                          title="Módulo con configuración propia"
                        >
                          ⭐
                        </span>
                      )}
                    </button>
                  );
                })}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    );
  };

  return (
    <div className="flex flex-col gap-5 bg-white/50 dark:bg-slate-900/40 backdrop-blur-2xl border border-slate-200 dark:border-white/10 p-5 rounded-[2.5rem] shadow-xl">
      {/* Level 2: Phases (Horizontal Scroll) */}
      <div className="flex items-center gap-3 overflow-x-auto custom-scrollbar pb-2 px-1">
        {staticPhases.map(phase => {
          const hasDraftChanges = isPhaseModified(phase.id);
          return (
            <button 
              type="button"
              key={phase.id}
              onClick={() => selectPhase(phase.id)}
              className={`shrink-0 px-6 py-3 rounded-full font-black text-sm border transition-all flex items-center gap-2 ${
                selectedPhaseId === phase.id 
                  ? 'bg-blue-500 text-white border-blue-500 shadow-md shadow-blue-500/20' 
                  : 'bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700/80'
              }`}
            >
              {phase.name.split(':')[0]}
              {hasDraftChanges && (
                <div className="w-2.5 h-2.5 rounded-full bg-amber-400 animate-pulse shadow-[0_0_8px_rgba(251,191,36,0.8)]" />
              )}
            </button>
          );
        })}
      </div>

      <div className="w-full h-px bg-slate-200 dark:bg-white/10" />

      {/* Level 3: Modules (Categorized Accordions) */}
      <div className="flex flex-col gap-4 px-1">
        <button 
          type="button"
          onClick={() => selectPhase(selectedPhaseId)}
          className={`w-fit px-5 py-2.5 rounded-xl font-black text-xs border transition-all flex items-center gap-2 ${
            !selectedModule
              ? 'bg-amber-500 text-white border-amber-500 shadow-md shadow-amber-500/20' 
              : 'bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700/80'
          }`}
        >
          <Settings size={14} /> General (Fase {selectedPhaseId})
        </button>

        {renderCategory('basicas', 'Operaciones Básicas', 'bg-blue-500/10 text-blue-500', basicas)}
        {renderCategory('avanzadas', 'Operaciones Avanzadas', 'bg-purple-500/10 text-purple-500', avanzadas)}
        {renderCategory('desafios', 'Módulos Temáticos', 'bg-amber-500/10 text-amber-500', desafios)}
        {renderCategory('final_exam', '🏆 Examen Final de Fase', 'bg-red-500/10 text-red-500', finalExam)}
      </div>

      {/* Sub-item Selector for Fase 2 & 3 */}
      {selectedModule && selectedPhaseId > 1 && (
        <div className="flex flex-col gap-3 bg-white/80 dark:bg-slate-950/40 p-5 rounded-3xl border border-slate-200 dark:border-white/5 mt-4 shadow-inner">
          <label className="text-[11px] font-black text-slate-500 dark:text-slate-400 uppercase tracking-widest pl-1">Explorar Niveles y Desafíos del Módulo</label>
          <div className="flex flex-wrap gap-2">
            {/* Levels */}
            {selectedModule.levels?.map((lvl) => (
              <button
                type="button"
                key={`lvl-${lvl.id}`}
                onClick={() => { setSelectedSubLevelId(lvl.id); setIsSelectedChallenge(false); }}
                className={`px-4 py-2 rounded-2xl text-sm font-bold border transition-all ${
                  !isSelectedChallenge && selectedSubLevelId === lvl.id
                    ? 'bg-blue-600 border-blue-500 text-white font-black shadow-md shadow-blue-500/20'
                    : 'bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white hover:bg-slate-50'
                }`}
              >
                Nivel {lvl.id}: {lvl.name}
              </button>
            ))}
            {/* Challenges */}
            {selectedModule.challenges?.map((ch) => (
              <button
                type="button"
                key={`ch-${ch.id}`}
                onClick={() => { setSelectedSubLevelId(ch.id); setIsSelectedChallenge(true); }}
                className={`px-4 py-2 rounded-2xl text-sm font-bold border transition-all flex items-center gap-1.5 ${
                  isSelectedChallenge && selectedSubLevelId === ch.id
                    ? 'bg-amber-600 border-amber-500 text-white font-black shadow-md shadow-amber-500/20'
                    : 'bg-amber-50 dark:bg-amber-900/20 border-amber-200 dark:border-amber-500/30 text-amber-700 dark:text-amber-400 hover:bg-amber-100'
                }`}
              >
                <Target size={14} /> {ch.name}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
