import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Plus, Trash2, Save, FileText, Loader2, X, 
  Settings, ChevronUp, ChevronDown, Award
} from 'lucide-react';

interface TheoryEditorProps {
  theory: any;
  setTheory: React.Dispatch<React.SetStateAction<any>>;
  loadingTheory: boolean;
  savingTheory: boolean;
  onSave: () => Promise<void>;
  mgrFaseId: number;
  mgrModuloId: number;
  mgrLevelId: number;
  PHASE_MAPS: any[];
  showConfirm: (title: string, message: string, onConfirm: () => void) => void;
  showToast: (message: string, type: 'success' | 'error') => void;
}

export const TheoryEditor: React.FC<TheoryEditorProps> = ({
  theory,
  setTheory,
  loadingTheory,
  savingTheory,
  onSave,
  mgrFaseId,
  mgrModuloId,
  mgrLevelId,
  PHASE_MAPS,
  showConfirm,
  showToast
}) => {
  // Collapse sections states
  const [expandTheoryCore, setExpandTheoryCore] = useState(true);
  const [expandGlosario, setExpandGlosario] = useState(true);
  const [expandEjemplos, setExpandEjemplos] = useState(true);

  // Interactive Exercises editing helpers
  const handleAddInteractive = () => {
    const newInteractives = [...(theory?.interactivos || [])];
    newInteractives.push({
      enunciado: "Nuevo Ejercicio",
      pasos: [
        { orden: 1, texto: "Paso 1 del ejercicio" }
      ],
      respuesta: "",
      feedback_acierto: "¡Excelente!",
      feedback_error: "Inténtalo de nuevo."
    });
    setTheory((prev: any) => ({ ...prev, interactivos: newInteractives }));
  };

  const handleDeleteInteractive = (idx: number) => {
    showConfirm(
      "Eliminar Ejercicio Interactivo",
      "¿Estás seguro de que deseas eliminar este ejercicio interactivo de la teoría?",
      () => {
        const newInteractives = (theory?.interactivos || []).filter((_: any, i: number) => i !== idx);
        setTheory((prev: any) => ({ ...prev, interactivos: newInteractives }));
        showToast("Ejercicio removido de la teoría.", "success");
      }
    );
  };

  const handleUpdateInteractive = (idx: number, field: string, value: any) => {
    const newInteractives = [...(theory?.interactivos || [])];
    newInteractives[idx] = {
      ...newInteractives[idx],
      [field]: value
    };
    setTheory((prev: any) => ({ ...prev, interactivos: newInteractives }));
  };

  const handleAddInteractiveStep = (intIdx: number) => {
    const newInteractives = [...(theory?.interactivos || [])];
    const steps = [...(newInteractives[intIdx].pasos || [])];
    steps.push({ orden: steps.length + 1, texto: "Siguiente paso" });
    newInteractives[intIdx] = {
      ...newInteractives[intIdx],
      pasos: steps
    };
    setTheory((prev: any) => ({ ...prev, interactivos: newInteractives }));
  };

  const handleUpdateInteractiveStepText = (intIdx: number, stepIdx: number, value: string) => {
    const newInteractives = [...(theory?.interactivos || [])];
    const steps = [...(newInteractives[intIdx]?.pasos || [])];
    if (steps[stepIdx]) {
      steps[stepIdx] = {
        ...steps[stepIdx],
        texto: value
      };
      newInteractives[intIdx] = {
        ...newInteractives[intIdx],
        pasos: steps
      };
      setTheory((prev: any) => ({ ...prev, interactivos: newInteractives }));
    }
  };

  const handleDeleteInteractiveStep = (intIdx: number, stepIdx: number) => {
    const newInteractives = [...(theory?.interactivos || [])];
    const steps = (newInteractives[intIdx]?.pasos || []).filter((_: any, i: number) => i !== stepIdx)
      .map((s: any, idx: number) => ({ ...s, orden: idx + 1 }));
    newInteractives[intIdx] = {
      ...newInteractives[intIdx],
      pasos: steps
    };
    setTheory((prev: any) => ({ ...prev, interactivos: newInteractives }));
  };

  const activePhase = PHASE_MAPS.find(p => p.id === mgrFaseId);
  const activeModule = activePhase?.modules?.find((m: any) => m.id === mgrModuloId);
  const activeLevel = (activeModule?.levels || activePhase?.levels || []).find((l: any) => l.id === mgrLevelId);

  return (
    <div className="flex flex-col gap-6">
      {/* Global theory save action panel */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 glass-panel border border-slate-200 dark:border-white/5 p-4 rounded-2xl">
        <span className="text-sm font-black text-slate-600 dark:text-slate-300">
          Estás editando la teoría de: <span className="text-purple-400">{activePhase?.name.split(':')[0]} / {activeLevel?.name}</span>
        </span>
        <button
          onClick={onSave}
          disabled={loadingTheory || savingTheory}
          className="px-5 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 disabled:opacity-40 text-sm font-black flex items-center gap-1.5 shadow-md shadow-purple-900/10 active:scale-95 transition-all cursor-pointer self-end sm:self-center"
        >
          {savingTheory ? <Loader2 size={14} className="animate-spin" /> : <Save size={14} />}
          Guardar Cambios de Teoría
        </button>
      </div>

      {loadingTheory ? (
        <div className="flex flex-col gap-6 animate-pulse">
          <div className="bg-white dark:bg-white/5 backdrop-blur-2xl border border-slate-200 dark:border-white/10 rounded-[2.2rem] shadow-2xl p-6 flex flex-col gap-4">
            <div className="h-6 w-1/3 bg-slate-200 dark:bg-white/10 rounded-full"></div>
            <div className="pt-4 border-t border-slate-200 dark:border-white/5 flex flex-col gap-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex flex-col gap-4">
                  <div className="h-12 bg-slate-200 dark:bg-white/10 rounded-xl w-full"></div>
                  <div className="h-24 bg-slate-200 dark:bg-white/10 rounded-xl w-full"></div>
                </div>
                <div className="flex flex-col gap-4">
                  <div className="h-40 bg-slate-200 dark:bg-white/10 rounded-xl w-full"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="flex flex-col gap-6">
          
          {/* SECTION 1: CORE THEORY FIELDS */}
          <div className="bg-white dark:bg-white/5 backdrop-blur-2xl border border-slate-200 dark:border-white/10 rounded-[2.2rem] shadow-2xl p-6 flex flex-col gap-4">
            <div 
              onClick={() => setExpandTheoryCore(!expandTheoryCore)}
              className="flex justify-between items-center cursor-pointer select-none group"
            >
              <h4 className="text-base font-black text-slate-600 dark:text-slate-300 group-hover:text-purple-400 transition-colors flex items-center gap-2">
                <FileText size={18} className="text-purple-400" />
                1. Información de Teoría Principal
              </h4>
              {expandTheoryCore ? <ChevronUp size={20} className="text-slate-500 dark:text-slate-400" /> : <ChevronDown size={20} className="text-slate-500 dark:text-slate-400" />}
            </div>

            <AnimatePresence initial={false}>
              {expandTheoryCore && (
                <motion.div
                  key="theory-core-body"
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.25 }}
                  className="overflow-hidden"
                >
                  <div className="pt-4 border-t border-slate-200 dark:border-white/5 flex flex-col gap-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="flex flex-col gap-4">
                        <div className="flex flex-col gap-1.5">
                          <label className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase">Título de Teoría</label>
                          <input
                            type="text"
                            value={theory?.titulo || ""}
                            onChange={(e) => setTheory((prev: any) => ({ ...prev, titulo: e.target.value }))}
                            className="bg-white/80 dark:bg-slate-950/60 border border-slate-200 dark:border-white/10 rounded-xl p-3 text-sm font-bold text-slate-900 dark:text-white focus:outline-none focus:border-purple-500/50"
                          />
                        </div>
                        
                        <div className="flex flex-col gap-1.5">
                          <label className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase">Texto Descubrimiento</label>
                          <textarea
                            rows={4}
                            value={theory?.texto_descubrimiento || ""}
                            onChange={(e) => setTheory((prev: any) => ({ ...prev, texto_descubrimiento: e.target.value }))}
                            className="bg-white/80 dark:bg-slate-950/60 border border-slate-200 dark:border-white/10 rounded-xl p-3 text-sm font-bold text-slate-900 dark:text-white focus:outline-none focus:border-purple-500/50 resize-none"
                          />
                        </div>
                      </div>

                      <div className="flex flex-col gap-4">
                        <div className="flex flex-col gap-1.5">
                          <label className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase">Tip Pedagógico / Advertencia</label>
                          <textarea
                            rows={7}
                            value={theory?.advertencia || ""}
                            onChange={(e) => setTheory((prev: any) => ({ ...prev, advertencia: e.target.value }))}
                            className="bg-white/80 dark:bg-slate-950/60 border border-slate-200 dark:border-white/10 rounded-xl p-3 text-sm font-bold text-slate-900 dark:text-white focus:outline-none focus:border-purple-500/50 resize-none"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* SECTION 2: GLOSSARY / DICTIONARY */}
          <div className="bg-white dark:bg-white/5 backdrop-blur-2xl border border-slate-200 dark:border-white/10 rounded-[2.2rem] shadow-2xl p-6 flex flex-col gap-4">
            <div 
              onClick={() => setExpandGlosario(!expandGlosario)}
              className="flex justify-between items-center cursor-pointer select-none group"
            >
              <h4 className="text-base font-black text-slate-600 dark:text-slate-300 group-hover:text-purple-400 transition-colors flex items-center gap-2">
                <Settings size={18} className="text-purple-400" />
                2. Glosario / Vocabulario del Nivel
              </h4>
              <div className="flex items-center gap-3">
                {expandGlosario && (
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      const newDict = { ...(theory?.diccionario || {}) };
                      let suffix = 1;
                      while (newDict[`Nuevo Término ${suffix}`]) suffix++;
                      newDict[`Nuevo Término ${suffix}`] = "Definición del término.";
                      setTheory((prev: any) => ({ ...prev, diccionario: newDict }));
                    }}
                    className="px-3 py-1.5 bg-purple-600/20 hover:bg-purple-600 text-purple-400 hover:text-slate-900 dark:text-white rounded-lg border border-purple-500/30 text-xs font-bold flex items-center gap-1 transition-all cursor-pointer"
                  >
                    <Plus size={12} /> Agregar Término
                  </button>
                )}
                {expandGlosario ? <ChevronUp size={20} className="text-slate-500 dark:text-slate-400" /> : <ChevronDown size={20} className="text-slate-500 dark:text-slate-400" />}
              </div>
            </div>

            <AnimatePresence initial={false}>
              {expandGlosario && (
                <motion.div
                  key="theory-glosario-body"
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.25 }}
                  className="overflow-hidden"
                >
                  <div className="pt-4 border-t border-slate-200 dark:border-white/5 flex flex-col gap-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      {Object.entries(theory?.diccionario || {}).map(([term, def]: [string, any], dIdx) => (
                        <div key={dIdx} className="flex gap-2 bg-white/80 dark:bg-slate-950/20 border border-slate-200 dark:border-white/5 p-3 rounded-xl items-start">
                          <div className="flex-1 flex flex-col gap-1.5">
                            <input
                              type="text"
                              placeholder="Término"
                              value={term}
                              onChange={(e) => {
                                const newKey = e.target.value;
                                if (!newKey) return;
                                const newDict: Record<string, any> = {};
                                for (const [k, v] of Object.entries(theory.diccionario)) {
                                  if (k === term) {
                                    newDict[newKey] = v;
                                  } else {
                                    newDict[k] = v;
                                  }
                                }
                                setTheory((prev: any) => ({ ...prev, diccionario: newDict }));
                              }}
                              className="bg-white/80 dark:bg-slate-950 border border-slate-200 dark:border-white/5 rounded-lg p-2 text-xs font-black text-purple-300 focus:outline-none focus:border-purple-500/50"
                            />
                            <textarea
                              rows={2}
                              placeholder="Definición"
                              value={def}
                              onChange={(e) => {
                                const newDict = { ...(theory.diccionario || {}) };
                                newDict[term] = e.target.value;
                                setTheory((prev: any) => ({ ...prev, diccionario: newDict }));
                              }}
                              className="bg-white/80 dark:bg-slate-950 border border-slate-200 dark:border-white/5 rounded-lg p-2 text-xs text-slate-900 dark:text-white focus:outline-none focus:border-purple-500/50 resize-none"
                            />
                          </div>
                          <button
                            type="button"
                            onClick={() => {
                              const newDict = { ...(theory.diccionario || {}) };
                              delete newDict[term];
                              setTheory((prev: any) => ({ ...prev, diccionario: newDict }));
                            }}
                            className="p-2 bg-red-500/10 hover:bg-red-500 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white rounded-lg transition-colors cursor-pointer"
                          >
                            <Trash2 size={12} />
                          </button>
                        </div>
                      ))}
                      {Object.keys(theory?.diccionario || {}).length === 0 && (
                        <div className="flex flex-col items-center justify-center py-8 text-center md:col-span-2 border-2 border-dashed border-slate-200 dark:border-white/10 rounded-2xl bg-slate-50/50 dark:bg-white/5">
                          <div className="p-3 bg-slate-100 dark:bg-white/5 rounded-full mb-3">
                            <FileText size={24} className="text-slate-400" />
                          </div>
                          <p className="text-sm font-black text-slate-500 dark:text-slate-400">Glosario Vacío</p>
                          <p className="text-xs text-slate-400 font-medium mt-1">No hay términos definidos. Haz clic en "Agregar Término" para empezar.</p>
                        </div>
                      )}
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* SECTION 3: EXAMPLES & INTERACTIVE EXERCISES */}
          <div className="bg-white dark:bg-white/5 backdrop-blur-2xl border border-slate-200 dark:border-white/10 rounded-[2.2rem] shadow-2xl p-6 flex flex-col gap-4">
            <div 
              onClick={() => setExpandEjemplos(!expandEjemplos)}
              className="flex justify-between items-center cursor-pointer select-none group"
            >
              <h4 className="text-base font-black text-slate-600 dark:text-slate-300 group-hover:text-purple-400 transition-colors flex items-center gap-2">
                <Award size={18} className="text-purple-400" />
                3. Secuencia Didáctica (Ejemplos y Ejercicios)
              </h4>
              {expandEjemplos ? <ChevronUp size={20} className="text-slate-500 dark:text-slate-400" /> : <ChevronDown size={20} className="text-slate-500 dark:text-slate-400" />}
            </div>

            <AnimatePresence initial={false}>
              {expandEjemplos && (
                <motion.div
                  key="theory-ejemplos-body"
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.25 }}
                  className="overflow-hidden"
                >
                  <div className="pt-4 border-t border-slate-200 dark:border-white/5 flex flex-col gap-6">
                    
                    {/* SUB-SECTION 3A: EXAMPLES */}
                    <div className="flex flex-col gap-4 glass-panel/20 border border-slate-200 dark:border-white/5 p-4 rounded-3xl">
                      <div className="flex justify-between items-center border-b border-slate-200 dark:border-white/5 pb-2">
                        <h5 className="text-sm font-black text-slate-500 dark:text-slate-400 uppercase tracking-widest">
                          3A. Ejemplos del Nivel (Explicativos / Guiados)
                        </h5>
                        <button
                          type="button"
                          onClick={() => {
                            const newExamples = [...(theory?.ejemplos || [])];
                            newExamples.push({
                              enunciado: "Nuevo Ejemplo",
                              pasos: [
                                { orden: 1, texto: "Paso 1 del ejemplo" }
                              ]
                            });
                            setTheory((prev: any) => ({ ...prev, ejemplos: newExamples }));
                          }}
                          className="px-3 py-1 bg-purple-600/20 hover:bg-purple-600 text-purple-400 hover:text-slate-900 dark:text-white rounded-lg border border-purple-500/30 text-xs font-bold flex items-center gap-1 transition-all cursor-pointer"
                        >
                          <Plus size={10} /> Agregar Ejemplo
                        </button>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {(theory?.ejemplos || []).map((ex: any, eIdx: number) => (
                          <div key={eIdx} className="bg-white/80 dark:bg-slate-950/20 border border-slate-200 dark:border-white/5 p-4 rounded-2xl flex flex-col gap-3 relative">
                            <div className="flex justify-between items-center">
                              <span className="text-xs font-black text-purple-400">Ejemplo #{eIdx + 1}</span>
                              <button
                                type="button"
                                onClick={() => {
                                  const newExamples = (theory.ejemplos || []).filter((_: any, i: number) => i !== eIdx);
                                  setTheory((prev: any) => ({ ...prev, ejemplos: newExamples }));
                                }}
                                className="p-1.5 bg-red-500/10 hover:bg-red-500 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white rounded-lg transition-colors cursor-pointer"
                              >
                                <Trash2 size={12} />
                              </button>
                            </div>

                            <div className="flex flex-col gap-1.5">
                              <label className="text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase">Enunciado del Ejemplo</label>
                              <input
                                type="text"
                                value={ex.enunciado || ""}
                                onChange={(e) => {
                                  const newExamples = [...theory.ejemplos];
                                  newExamples[eIdx] = { ...ex, enunciado: e.target.value };
                                  setTheory((prev: any) => ({ ...prev, ejemplos: newExamples }));
                                }}
                                className="bg-white/80 dark:bg-slate-950 border border-slate-200 dark:border-white/5 rounded-lg p-2.5 text-xs text-slate-900 dark:text-white focus:outline-none focus:border-purple-500/50"
                              />
                            </div>

                            <div className="flex flex-col gap-2 bg-white/80 dark:bg-slate-950/40 p-3 rounded-xl border border-slate-200 dark:border-white/5">
                              <div className="flex justify-between items-center">
                                <label className="text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase">Pasos del Ejemplo</label>
                                <button
                                  type="button"
                                  onClick={() => {
                                    const newExamples = [...theory.ejemplos];
                                    const steps = [...(ex.pasos || [])];
                                    steps.push({ orden: steps.length + 1, texto: "Siguiente paso" });
                                    newExamples[eIdx] = { ...ex, pasos: steps };
                                    setTheory((prev: any) => ({ ...prev, ejemplos: newExamples }));
                                  }}
                                  className="px-2 py-0.5 bg-purple-500/10 hover:bg-purple-500 hover:text-slate-900 dark:text-white text-purple-400 rounded text-[9px] font-bold flex items-center gap-0.5 border border-purple-500/20 cursor-pointer"
                                >
                                  <Plus size={8} /> Añadir Paso
                                </button>
                              </div>

                              <div className="flex flex-col gap-2">
                                {(ex.pasos || []).map((step: any, sIdx: number) => (
                                  <div key={sIdx} className="flex gap-2 items-center">
                                    <span className="text-xs font-bold text-slate-500">{step.orden}</span>
                                    <input
                                      type="text"
                                      value={step.texto || ""}
                                      onChange={(e) => {
                                        const newExamples = [...theory.ejemplos];
                                        const steps = [...ex.pasos];
                                        steps[sIdx] = { ...step, texto: e.target.value };
                                        newExamples[eIdx] = { ...ex, pasos: steps };
                                        setTheory((prev: any) => ({ ...prev, ejemplos: newExamples }));
                                      }}
                                      className="flex-1 bg-white/80 dark:bg-slate-950 border border-slate-200 dark:border-white/5 rounded-lg p-2 text-xs text-slate-900 dark:text-white focus:outline-none focus:border-purple-500/50"
                                    />
                                    <button
                                      type="button"
                                      onClick={() => {
                                        const newExamples = [...theory.ejemplos];
                                        const steps = ex.pasos.filter((_: any, i: number) => i !== sIdx)
                                          .map((s: any, idx: number) => ({ ...s, orden: idx + 1 }));
                                        newExamples[eIdx] = { ...ex, pasos: steps };
                                        setTheory((prev: any) => ({ ...prev, ejemplos: newExamples }));
                                      }}
                                      className="p-1.5 hover:bg-red-500/20 text-slate-500 dark:text-slate-400 hover:text-red-400 rounded-lg transition-colors cursor-pointer"
                                    >
                                      <X size={10} />
                                    </button>
                                  </div>
                                ))}
                                {(ex.pasos || []).length === 0 && (
                                  <div className="flex flex-col gap-1">
                                    <span className="text-[9px] text-slate-500 italic">No hay pasos, se usará la respuesta legacy directa:</span>
                                    <input
                                      type="text"
                                      placeholder="Respuesta directa (ej: 18)"
                                      value={ex.respuesta || ""}
                                      onChange={(e) => {
                                        const newExamples = [...theory.ejemplos];
                                        newExamples[eIdx] = { ...ex, respuesta: e.target.value };
                                        setTheory((prev: any) => ({ ...prev, ejemplos: newExamples }));
                                      }}
                                      className="bg-white/80 dark:bg-slate-950 border border-slate-200 dark:border-white/5 rounded-lg p-2 text-xs text-slate-900 dark:text-white focus:outline-none"
                                    />
                                  </div>
                                )}
                              </div>
                            </div>
                          </div>
                        ))}
                        {(theory?.ejemplos || []).length === 0 && (
                          <div className="flex flex-col items-center justify-center py-8 text-center md:col-span-2 border-2 border-dashed border-slate-200 dark:border-white/10 rounded-2xl bg-slate-50/50 dark:bg-white/5">
                            <div className="p-3 bg-purple-500/10 rounded-full mb-3">
                              <Award size={24} className="text-purple-400" />
                            </div>
                            <p className="text-sm font-black text-slate-500 dark:text-slate-400">Sin Ejemplos Guiados</p>
                            <p className="text-xs text-slate-400 font-medium mt-1">Aún no has agregado ejemplos explicativos para este nivel.</p>
                          </div>
                        )}
                      </div>
                    </div>

                    {/* SUB-SECTION 3B: INTERACTIVES */}
                    <div className="flex flex-col gap-4 glass-panel/20 border border-slate-200 dark:border-white/5 p-4 rounded-3xl">
                      <div className="flex justify-between items-center border-b border-slate-200 dark:border-white/5 pb-2">
                        <h5 className="text-sm font-black text-slate-500 dark:text-slate-400 uppercase tracking-widest flex items-center gap-2">
                          3B. Ejercicios Interactivos del Alumno (Secuencia de Evocación)
                        </h5>
                        <button
                          type="button"
                          onClick={handleAddInteractive}
                          className="px-3 py-1 bg-purple-600/20 hover:bg-purple-600 text-purple-400 hover:text-slate-900 dark:text-white rounded-lg border border-purple-500/30 text-xs font-bold flex items-center gap-1 transition-all cursor-pointer"
                        >
                          <Plus size={10} /> Agregar Ejercicio
                        </button>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {(theory?.interactivos || []).map((ex: any, iIdx: number) => (
                          <div key={iIdx} className="bg-white/80 dark:bg-slate-950/20 border border-slate-200 dark:border-white/5 p-4 rounded-2xl flex flex-col gap-3 relative">
                            <div className="flex justify-between items-center">
                              <span className="text-xs font-black text-purple-400">Ejercicio Interactivo #{iIdx + 1}</span>
                              <button
                                type="button"
                                onClick={() => handleDeleteInteractive(iIdx)}
                                className="p-1.5 bg-red-500/10 hover:bg-red-500 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white rounded-lg transition-colors cursor-pointer"
                              >
                                <Trash2 size={12} />
                              </button>
                            </div>

                            <div className="flex flex-col gap-1.5">
                              <label className="text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase">Enunciado del Ejercicio</label>
                              <input
                                type="text"
                                value={ex.enunciado || ""}
                                onChange={(e) => handleUpdateInteractive(iIdx, "enunciado", e.target.value)}
                                className="bg-white/80 dark:bg-slate-950 border border-slate-200 dark:border-white/5 rounded-lg p-2.5 text-xs text-slate-900 dark:text-white focus:outline-none focus:border-purple-500/50"
                              />
                            </div>

                            <div className="flex flex-col gap-1.5">
                              <label className="text-[10px] font-bold text-green-400 uppercase">Respuesta Correcta Esperada</label>
                              <input
                                type="text"
                                placeholder="Ej: 16"
                                value={ex.respuesta || ""}
                                onChange={(e) => handleUpdateInteractive(iIdx, "respuesta", e.target.value)}
                                className="bg-white/80 dark:bg-slate-950 border border-slate-200 dark:border-white/5 rounded-lg p-2.5 text-xs text-slate-900 dark:text-white focus:outline-none focus:border-purple-500/50"
                              />
                            </div>

                            <div className="flex flex-col gap-2 bg-white/80 dark:bg-slate-950/40 p-3 rounded-xl border border-slate-200 dark:border-white/5">
                              <div className="flex justify-between items-center">
                                <label className="text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase">Pasos Resolutivos</label>
                                <button
                                  type="button"
                                  onClick={() => handleAddInteractiveStep(iIdx)}
                                  className="px-2 py-0.5 bg-purple-500/10 hover:bg-purple-500 hover:text-slate-900 dark:text-white text-purple-400 rounded text-[9px] font-bold flex items-center gap-0.5 border border-purple-500/20 cursor-pointer"
                                >
                                  <Plus size={8} /> Añadir Paso
                                </button>
                              </div>

                              <div className="flex flex-col gap-2">
                                {(ex.pasos || []).map((step: any, sIdx: number) => (
                                  <div key={sIdx} className="flex gap-2 items-center">
                                    <span className="text-xs font-bold text-slate-500">{step.orden}</span>
                                    <input
                                      type="text"
                                      value={step.texto || ""}
                                      onChange={(e) => handleUpdateInteractiveStepText(iIdx, sIdx, e.target.value)}
                                      className="flex-1 bg-white/80 dark:bg-slate-950 border border-slate-200 dark:border-white/5 rounded-lg p-2 text-xs text-slate-900 dark:text-white focus:outline-none focus:border-purple-500/50"
                                    />
                                    <button
                                      type="button"
                                      onClick={() => handleDeleteInteractiveStep(iIdx, sIdx)}
                                      className="p-1.5 hover:bg-red-500/20 text-slate-500 dark:text-slate-400 hover:text-red-400 rounded-lg transition-colors cursor-pointer"
                                    >
                                      <X size={10} />
                                    </button>
                                  </div>
                                ))}
                              </div>
                            </div>

                            <div className="flex flex-col gap-2 bg-white/80 dark:bg-slate-950/40 p-3 rounded-xl border border-slate-200 dark:border-white/5">
                              <div className="flex flex-col gap-1">
                                <label className="text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase">Feedback al Acertar</label>
                                <input
                                  type="text"
                                  placeholder="Ej: ¡Excelente! 8 x 2 = 16"
                                  value={ex.feedback_acierto || ""}
                                  onChange={(e) => handleUpdateInteractive(iIdx, "feedback_acierto", e.target.value)}
                                  className="bg-white/80 dark:bg-slate-950 border border-slate-200 dark:border-white/5 rounded-lg p-2 text-xs text-slate-900 dark:text-white focus:outline-none focus:border-purple-500/50"
                                />
                              </div>
                              <div className="flex flex-col gap-1">
                                <label className="text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase">Feedback al Fallar</label>
                                <input
                                  type="text"
                                  placeholder="Ej: 'El doble' es multiplicar por 2"
                                  value={ex.feedback_error || ""}
                                  onChange={(e) => handleUpdateInteractive(iIdx, "feedback_error", e.target.value)}
                                  className="bg-white/80 dark:bg-slate-950 border border-slate-200 dark:border-white/5 rounded-lg p-2 text-xs text-slate-900 dark:text-white focus:outline-none focus:border-purple-500/50"
                                />
                              </div>
                            </div>
                          </div>
                        ))}
                        {(theory?.interactivos || []).length === 0 && (
                          <div className="flex flex-col items-center justify-center py-8 text-center md:col-span-2 border-2 border-dashed border-slate-200 dark:border-white/10 rounded-2xl bg-slate-50/50 dark:bg-white/5">
                            <div className="p-3 bg-blue-500/10 rounded-full mb-3">
                              <Settings size={24} className="text-blue-400" />
                            </div>
                            <p className="text-sm font-black text-slate-500 dark:text-slate-400">Sin Ejercicios Interactivos</p>
                            <p className="text-xs text-slate-400 font-medium mt-1">Añade ejercicios para que el estudiante practique lo aprendido.</p>
                          </div>
                        )}
                      </div>
                    </div>

                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

        </div>
      )}
    </div>
  );
};
