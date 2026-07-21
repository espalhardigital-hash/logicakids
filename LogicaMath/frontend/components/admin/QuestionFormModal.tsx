import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  X, Shield, ToggleRight, ToggleLeft, HelpCircle
} from 'lucide-react';

const TokenHighlighter: React.FC<{
  text: string;
  selectedIndices: number[];
  onChange: (indices: number[], tokens: string[]) => void;
}> = ({ text, selectedIndices, onChange }) => {
  const words = text.split(' ').filter(Boolean);

  const toggleWord = (index: number) => {
    let newIndices;
    if (selectedIndices.includes(index)) {
      newIndices = selectedIndices.filter(i => i !== index);
    } else {
      newIndices = [...selectedIndices, index].sort((a,b) => a-b);
    }
    const selectedTokens = newIndices.map(i => words[i]);
    onChange(newIndices, selectedTokens);
  };

  if (!text) return <p className="text-xs text-slate-500 italic">Escribe el enunciado primero para seleccionar tokens...</p>;

  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-center gap-2">
        <label className="text-xs font-black text-slate-500 dark:text-slate-400 uppercase">Selecciona los tokens correctos (WYSIWYG)</label>
        <div className="relative group inline-block">
          <HelpCircle size={14} className="text-slate-400 cursor-help" />
          <div className="absolute bottom-full left-0 mb-2 w-64 p-3 bg-slate-900 dark:bg-slate-700 text-white text-[11px] rounded-xl shadow-xl opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-50 leading-relaxed">
            Haz clic en las palabras del enunciado para marcarlas como términos clave de la pregunta.
            <div className="absolute top-full left-4 border-4 border-transparent border-t-slate-900 dark:border-t-slate-700"></div>
          </div>
        </div>
      </div>
      <div className="flex flex-wrap gap-1.5 p-3 bg-white/80 dark:bg-slate-950/20 border border-slate-200 dark:border-white/5 rounded-xl min-h-[50px]">
        {words.map((word, idx) => {
          const isSelected = selectedIndices.includes(idx);
          return (
            <span
              key={idx}
              onClick={() => toggleWord(idx)}
              className={`cursor-pointer px-2.5 py-1 rounded-lg text-sm font-bold transition-all shadow-sm ${isSelected ? 'bg-purple-500 text-white shadow-purple-500/30 scale-105' : 'bg-white dark:bg-white/5 text-slate-600 dark:text-slate-300 hover:bg-purple-100 dark:hover:bg-purple-900/30'}`}
            >
              {word}
            </span>
          );
        })}
      </div>
    </div>
  );
};

interface QuestionFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  editingQuestion: any;
  setEditingQuestion: React.Dispatch<React.SetStateAction<any>>;
  savingQuestion: boolean;
  onSave: (e: React.FormEvent) => void;
  showToast: (message: string, type: 'success' | 'error') => void;
}

export const QuestionFormModal: React.FC<QuestionFormModalProps> = ({
  isOpen,
  onClose,
  editingQuestion,
  setEditingQuestion,
  savingQuestion,
  onSave,
  showToast
}) => {
  if (!isOpen || !editingQuestion) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
        <motion.div
          initial={{ scale: 0.95, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.95, opacity: 0 }}
          className="glass-panel border border-slate-200 dark:border-white/10 w-full max-w-xl rounded-[2.2rem] p-8 shadow-2xl flex flex-col gap-6 max-h-[90vh] overflow-y-auto custom-scrollbar text-slate-900 dark:text-white select-none"
        >
          <div className="flex justify-between items-center border-b border-slate-200 dark:border-white/5 pb-4">
            <h4 className="text-xl font-black flex items-center gap-2">
              <Shield size={20} className="text-blue-400" />
              {editingQuestion.id ? 'Editar Pregunta' : 'Nueva Pregunta'}
            </h4>
            <button 
              onClick={onClose}
              className="p-1 hover:bg-slate-200 dark:hover:bg-slate-100 dark:bg-white/10 rounded-lg text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white transition-all cursor-pointer"
            >
              <X size={20} />
            </button>
          </div>

          <form onSubmit={onSave} className="flex flex-col gap-5">
            
            {/* Enunciado */}
            <div className="flex flex-col gap-2">
              <label className="text-xs font-black text-slate-500 dark:text-slate-400 uppercase">Enunciado / Pregunta</label>
              <input
                type="text"
                required
                value={editingQuestion.enunciado}
                onChange={(e) => setEditingQuestion((prev: any) => ({ ...prev, enunciado: e.target.value }))}
                className="w-full bg-white/80 dark:bg-slate-950 border border-slate-200 dark:border-white/10 rounded-xl p-3.5 text-sm font-bold text-slate-900 dark:text-white focus:outline-none focus:border-blue-500/50"
              />
            </div>

            {/* Respuesta Correcta */}
            <div className="flex flex-col gap-2">
              <label className="text-xs font-black text-slate-500 dark:text-slate-400 uppercase">Respuesta Correcta</label>
              <input
                type="text"
                required
                value={editingQuestion.respuesta_correcta}
                onChange={(e) => setEditingQuestion((prev: any) => ({ ...prev, respuesta_correcta: e.target.value }))}
                className="w-full bg-white/80 dark:bg-slate-950 border border-slate-200 dark:border-white/10 rounded-xl p-3.5 text-sm font-bold text-slate-900 dark:text-white focus:outline-none focus:border-blue-500/50"
              />
            </div>

            {/* Tipo de pregunta & Requiere subrayado */}
            <div className="grid grid-cols-2 gap-4">
              <div className="flex flex-col gap-2">
                <label className="text-xs font-black text-slate-500 dark:text-slate-400 uppercase">Tipo de Interfaz</label>
                <select
                  value={editingQuestion.tipo_pregunta}
                  onChange={(e) => setEditingQuestion((prev: any) => ({ ...prev, tipo_pregunta: e.target.value }))}
                  className="bg-white/80 dark:bg-slate-950 border border-slate-200 dark:border-white/10 rounded-xl p-3 text-sm font-bold text-slate-900 dark:text-white focus:outline-none focus:border-blue-500/50"
                >
                  <option value="multiple_opcion">Opción Múltiple</option>
                  <option value="respuesta_numerica">Respuesta Numérica</option>
                </select>
              </div>

              <div className="flex items-center justify-between bg-white/80 dark:bg-slate-950/40 border border-slate-200 dark:border-white/5 p-3 rounded-xl self-end h-[46px]">
                <span className="text-xs font-black text-slate-500 dark:text-slate-400 uppercase">Requiere Subrayado</span>
                <button
                  type="button"
                  onClick={() => setEditingQuestion((prev: any) => ({ ...prev, requiere_subrayado: !prev.requiere_subrayado }))}
                  className="hover:scale-105 transition-transform cursor-pointer"
                >
                  {editingQuestion.requiere_subrayado ? (
                    <ToggleRight size={32} className="text-blue-400" />
                  ) : (
                    <ToggleLeft size={32} className="text-slate-600" />
                  )}
                </button>
              </div>
            </div>

            {/* Token Highlighter for Subrayado */}
            {editingQuestion.requiere_subrayado && (
              <TokenHighlighter 
                text={editingQuestion.enunciado}
                selectedIndices={editingQuestion.tokens_correctos_indices || []}
                onChange={(indices, tokens) => {
                  setEditingQuestion((prev: any) => ({
                    ...prev,
                    tokens_correctos_indices: indices,
                    tokens_correctos: tokens,
                    // Automatically update respuesta_correcta to match selected tokens
                    respuesta_correcta: tokens.join(' ')
                  }));
                }}
              />
            )}

            {/* Alternatives editor (only if Multiple Choice) */}
            {editingQuestion.tipo_pregunta === "multiple_opcion" && (
              <div className="flex flex-col gap-3 border-t border-slate-200 dark:border-white/5 pt-3">
                <label className="text-xs font-black text-slate-500 dark:text-slate-400 uppercase">Alternativas del Nivel (Opción Múltiple)</label>
                
                {editingQuestion.alternativas.map((alt: any, idx: number) => (
                  <div key={idx} className="flex flex-col gap-2 bg-white/80 dark:bg-slate-950/20 border border-slate-200 dark:border-white/5 p-3 rounded-xl">
                    <div className="flex items-center gap-3">
                      <span className="text-sm font-black text-slate-500 w-5 text-center">#{idx + 1}</span>
                      <input
                        type="text"
                        required
                        placeholder={`Texto de la opción ${idx + 1}`}
                        value={alt.texto}
                        onChange={(e) => {
                          const newAlts = [...editingQuestion.alternativas];
                          newAlts[idx] = { ...alt, texto: e.target.value };
                          let updateCorrectObj: any = {};
                          if (alt.es_correcta) {
                            updateCorrectObj.respuesta_correcta = e.target.value;
                          }
                          setEditingQuestion((prev: any) => ({
                            ...prev,
                            alternativas: newAlts,
                            ...updateCorrectObj
                          }));
                        }}
                        className="flex-1 bg-white/80 dark:bg-slate-950 border border-slate-200 dark:border-white/5 rounded-lg p-2.5 text-sm text-slate-900 dark:text-white focus:outline-none focus:border-blue-500/50"
                      />
                      <button
                        type="button"
                        onClick={() => {
                          const newAlts = editingQuestion.alternativas.map((a: any, i: number) => ({
                            ...a,
                            es_correcta: i === idx,
                            tipo_error: i === idx ? null : a.tipo_error,
                            feedback_error: i === idx ? null : a.feedback_error
                          }));
                          setEditingQuestion((prev: any) => ({
                            ...prev,
                            alternativas: newAlts,
                            respuesta_correcta: alt.texto
                          }));
                        }}
                        className={`px-3 py-1.5 rounded-lg text-xs font-black border transition-all cursor-pointer ${
                          alt.es_correcta 
                            ? 'bg-green-500/20 border-green-500/40 text-green-400' 
                            : 'bg-white dark:bg-white/5 border-slate-200 dark:border-white/10 text-slate-500 hover:text-slate-600 dark:text-slate-300'
                        }`}
                      >
                        {alt.es_correcta ? 'Correcta' : 'Hacer Correcta'}
                      </button>
                    </div>
                    
                    {!alt.es_correcta && (
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pl-8 border-t border-slate-200 dark:border-white/5 pt-2 mt-1">
                        <div className="flex flex-col gap-1.5">
                          <label className="text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase">Tipo de Error Cognitivo</label>
                          <select
                            value={alt.tipo_error || ""}
                            onChange={(e) => {
                              const newAlts = [...editingQuestion.alternativas];
                              newAlts[idx] = { ...alt, tipo_error: e.target.value || null };
                              setEditingQuestion((prev: any) => ({ ...prev, alternativas: newAlts }));
                            }}
                            className="bg-white/80 dark:bg-slate-950 border border-slate-200 dark:border-white/5 rounded-lg p-2 text-xs text-slate-900 dark:text-white focus:outline-none focus:border-blue-500/50"
                          >
                            <option value="">-- Sin Tipo de Error --</option>
                            <option value="calculo">Cálculo</option>
                            <option value="lectura">Lectura</option>
                            <option value="atencion">Atención</option>
                            <option value="operacion_incorrecta">Operación Incorrecta</option>
                            <option value="no_identifica_datos">No Identifica Datos</option>
                            <option value="problema_incompleto">Problema Incompleto</option>
                            <option value="tabuada">Tabuada</option>
                            <option value="division">División</option>
                            <option value="valor_posicional">Valor Posicional</option>
                            <option value="troco">Troco</option>
                            <option value="inferencia">Inferencia</option>
                          </select>
                        </div>
                        <div className="flex flex-col gap-1.5">
                          <label className="text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase">Feedback Pedagógico del Error</label>
                          <input
                            type="text"
                            placeholder="Ej: Recuerda sumar las decenas primero"
                            value={alt.feedback_error || ""}
                            onChange={(e) => {
                              const newAlts = [...editingQuestion.alternativas];
                              newAlts[idx] = { ...alt, feedback_error: e.target.value };
                              setEditingQuestion((prev: any) => ({ ...prev, alternativas: newAlts }));
                            }}
                            className="bg-white/80 dark:bg-slate-950 border border-slate-200 dark:border-white/5 rounded-lg p-2 text-xs text-slate-900 dark:text-white focus:outline-none focus:border-blue-500/50"
                          />
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* Submit / Cancel Buttons */}
            <div className="flex justify-end gap-3 mt-4 border-t border-slate-200 dark:border-white/5 pt-4">
              <button
                type="button"
                onClick={onClose}
                className="px-5 py-2.5 bg-slate-200 dark:bg-white/10 hover:bg-slate-300 dark:hover:bg-white/20 rounded-xl text-sm font-black text-slate-700 dark:text-white transition-all cursor-pointer"
              >
                Cancelar
              </button>
              <button
                type="submit"
                disabled={savingQuestion}
                className="px-5 py-2.5 bg-blue-600 hover:bg-blue-500 disabled:opacity-40 rounded-xl text-sm font-black text-white shadow-md shadow-blue-900/10 active:scale-95 transition-all flex items-center gap-1.5 cursor-pointer"
              >
                {savingQuestion && <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>}
                {editingQuestion.id ? 'Actualizar Pregunta' : 'Crear Pregunta'}
              </button>
            </div>
          </form>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};
