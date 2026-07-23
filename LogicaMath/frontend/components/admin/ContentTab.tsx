import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  FileText, Settings, Shield, ChevronRight, ToggleRight, ToggleLeft, BookOpen
} from 'lucide-react';
import { 
  deletePregunta, createPregunta, updatePregunta,
  saveNivelTeoria 
} from '../../services/storageService';
import { usePhaseMapContext } from './PhaseMapContext';
import { useAdminContent } from './useAdminContent';

// Import subcomponents
import { TheoryEditor } from './TheoryEditor';
import { QuestionTable } from './QuestionTable';
import { QuestionFormModal } from './QuestionFormModal';
import { StudentViewSimulator } from './StudentViewSimulator';

interface ContentTabProps {
  showAlert?: (title: string, message: string, type?: 'info' | 'success' | 'error') => void;
  showConfirm?: (title: string, message: string, onConfirm: () => void) => void;
}

const ContentTab: React.FC<ContentTabProps> = ({ showAlert, showConfirm: showConfirmProp }) => {
  const { phaseMaps: PHASE_MAPS } = usePhaseMapContext();
  
  // Sub-tabs: theory editor, question bank list, or student flow simulator
  const [activeSubTab, setActiveSubTab] = useState<'theory' | 'questions' | 'simulator'>('theory');

  // Hook for Content Logic and API synchronization
  const {
    mgrFaseId, setMgrFaseId,
    mgrModuloId, setMgrModuloId,
    mgrLevelId, setMgrLevelId,
    questions, setQuestions,
    theory, setTheory,
    loading: loadingQuestions
  } = useAdminContent();

  const loadingTheory = loadingQuestions;
  const [savingTheory, setSavingTheory] = useState(false);

  // Question Pagination & Filter State
  const [questionsPerPage, setQuestionsPerPage] = useState<number>(10);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [questionSearchQuery, setQuestionSearchQuery] = useState<string>('');

  // Modal / Form State for Question modifications
  const [editingQuestion, setEditingQuestion] = useState<any | null>(null);
  const [showQuestionModal, setShowQuestionModal] = useState(false);
  const [savingQuestion, setSavingQuestion] = useState(false);

  // Unified notifications using global app modals or fallback window dialogs
  const showToast = (message: string, type: 'success' | 'error' = 'success') => {
    if (showAlert) {
      showAlert(type === 'success' ? 'Éxito' : 'Error', message, type === 'success' ? 'success' : 'error');
    }
  };

  const showConfirm = (title: string, message: string, onConfirm: () => void) => {
    if (showConfirmProp) {
      showConfirmProp(title, message, onConfirm);
    } else if (window.confirm(message)) {
      onConfirm();
    }
  };

  // Reset pagination filters when level coordinates change
  useEffect(() => {
    setCurrentPage(1);
    setQuestionSearchQuery('');
  }, [mgrFaseId, mgrModuloId, mgrLevelId]);

  // Persist selectors to local storage for administration ease
  useEffect(() => {
    localStorage.setItem('admin_content_fase', String(mgrFaseId));
    localStorage.setItem('admin_content_modulo', String(mgrModuloId));
  }, [mgrFaseId, mgrModuloId]);

  // Save Theory changes to the database
  const handleSaveTheory = async () => {
    if (!theory) return;
    setSavingTheory(true);
    try {
      await saveNivelTeoria(theory);
      showToast("¡Teoría guardada exitosamente!", "success");
    } catch (e) {
      console.error(e);
      showToast("Error al guardar la teoría.", "error");
    } finally {
      setSavingTheory(false);
    }
  };

  // Delete a question from the bank
  const handleDeleteQuestion = async (qId: number) => {
    showConfirm(
      "Eliminar Pregunta",
      "¿Estás seguro de que deseas eliminar esta pregunta? Esta acción no se puede deshacer.",
      async () => {
        try {
          await deletePregunta(qId);
          setQuestions(prev => prev.filter(q => q.id !== qId));
          showToast("Pregunta eliminada exitosamente.", "success");
        } catch (e) {
          console.error(e);
          showToast("Error al eliminar la pregunta.", "error");
        }
      }
    );
  };

  // Save changes from QuestionFormModal
  const handleSaveQuestion = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingQuestion) return;

    // Validations
    if (!editingQuestion.enunciado || !editingQuestion.enunciado.trim()) {
      showToast("El enunciado principal no puede estar vacío.", "error");
      return;
    }

    if (editingQuestion.tipo_pregunta === "multiple_opcion") {
      if (!editingQuestion.alternativas || editingQuestion.alternativas.length < 2) {
        showToast("Debes proporcionar al menos 2 alternativas.", "error");
        return;
      }
      const hasEmptyAlts = editingQuestion.alternativas.some((a: any) => !a.texto || !a.texto.trim());
      if (hasEmptyAlts) {
        showToast("Todas las alternativas deben contener texto.", "error");
        return;
      }
      const correctAlts = editingQuestion.alternativas.filter((a: any) => a.es_correcta);
      if (correctAlts.length === 0) {
        showToast("Debe haber al menos una alternativa marcada como correcta.", "error");
        return;
      }
      if (!editingQuestion.respuesta_correcta || !editingQuestion.respuesta_correcta.trim()) {
        editingQuestion.respuesta_correcta = correctAlts[0].texto;
      }
    } else if (editingQuestion.requiere_subrayado) {
       if (!editingQuestion.tokens_correctos_indices || editingQuestion.tokens_correctos_indices.length === 0) {
         showToast("En el modo de selección, debes subrayar al menos una palabra.", "error");
         return;
       }
    } else {
       if (!editingQuestion.respuesta_correcta || !editingQuestion.respuesta_correcta.trim()) {
         showToast("El campo de respuesta correcta no puede estar vacío.", "error");
         return;
       }
    }

    setSavingQuestion(true);

    const phase = PHASE_MAPS.find(p => p.id === mgrFaseId);
    const mod = phase?.modules.find(m => m.id === mgrModuloId);
    const lvl = mod?.levels.find(l => l.id === mgrLevelId) || phase?.levels?.find(l => l.id === mgrLevelId);
    if (!lvl) return;

    const payload = {
      ...editingQuestion,
      fase_id: mgrFaseId,
      seccion: lvl.seccion,
      operacion: lvl.operacion
    };

    try {
      if (editingQuestion.id) {
        const updated = await updatePregunta(editingQuestion.id, payload);
        setQuestions(prev => prev.map(q => q.id === editingQuestion.id ? updated : q));
        showToast("Pregunta actualizada exitosamente.", "success");
      } else {
        const created = await createPregunta(payload);
        setQuestions(prev => [...prev, created]);
        showToast("Pregunta creada exitosamente.", "success");
      }
      setShowQuestionModal(false);
      setEditingQuestion(null);
    } catch (err) {
      console.error(err);
      showToast("Error al guardar la pregunta.", "error");
    } finally {
      setSavingQuestion(false);
    }
  };

  const openNewQuestionModal = () => {
    setEditingQuestion({
      enunciado: "",
      respuesta_correcta: "",
      tipo_pregunta: "multiple_opcion",
      requiere_subrayado: false,
      tokens_correctos_indices: [],
      tokens_correctos: [],
      explicacion_paso_a_paso: null,
      alternativas: [
        { texto: "", es_correcta: true, orden: 1 },
        { texto: "", es_correcta: false, orden: 2 },
        { texto: "", es_correcta: false, orden: 3 },
        { texto: "", es_correcta: false, orden: 4 }
      ]
    });
    setShowQuestionModal(true);
  };

  const openEditQuestionModal = (q: any) => {
    const alts = q.alternativas && q.alternativas.length > 0 
      ? JSON.parse(JSON.stringify(q.alternativas)) 
      : [
          { texto: "", es_correcta: true, orden: 1 },
          { texto: "", es_correcta: false, orden: 2 },
          { texto: "", es_correcta: false, orden: 3 },
          { texto: "", es_correcta: false, orden: 4 }
        ];
    setEditingQuestion({
      id: q.id,
      enunciado: q.enunciado,
      respuesta_correcta: q.respuesta_correcta,
      tipo_pregunta: q.tipo_pregunta || "multiple_opcion",
      requiere_subrayado: q.requiere_subrayado || false,
      tokens_correctos_indices: q.tokens_correctos_indices || [],
      tokens_correctos: q.tokens_correctos || [],
      explicacion_paso_a_paso: q.explicacion_paso_a_paso ? JSON.parse(JSON.stringify(q.explicacion_paso_a_paso)) : null,
      alternativas: alts
    });
    setShowQuestionModal(true);
  };

  const activePhase = PHASE_MAPS.find(p => p.id === mgrFaseId);
  const activeModule = activePhase?.modules?.find(m => m.id === mgrModuloId);
  const activeLevelList = activeModule?.levels || activePhase?.levels || [];
  const activeLevel = activeLevelList.find(l => l.id === mgrLevelId);

  return (
    <div className="w-full flex flex-col gap-6 text-slate-900 dark:text-white select-none">
      
      {/* Top Header Panel */}
      <div className="flex items-center justify-between bg-white dark:bg-white/5 backdrop-blur-2xl border border-slate-200 dark:border-white/10 rounded-[2.2rem] shadow-2xl p-6">
        <div>
          <h2 className="text-3xl font-bold text-slate-900 dark:text-[#f3f4f6] flex items-center gap-3">
            <div className="p-2.5 bg-[#007AFF]/20 rounded-2xl border border-[#007AFF]/30">
              <BookOpen className="text-[#007AFF]" size={24} />
            </div>
            Banco de Preguntas y Teoría
          </h2>
          <p className="text-slate-500 dark:text-[#8E8E93] text-sm mt-1 font-medium">
            Administra las preguntas del plan de estudios, el material teórico y simula la experiencia del alumno.
          </p>
        </div>
        <div>
          <button 
            onClick={() => document.documentElement.classList.toggle('dark')}
            className="glass-button flex items-center gap-2 text-sm"
          >
            <ToggleRight className="hidden dark:block text-blue-400" size={20} />
            <ToggleLeft className="block dark:hidden text-slate-400" size={20} />
            Tema
          </button>
        </div>
      </div>

      {/* Tabs Selector Bar */}
      <div className="flex flex-wrap border-b border-slate-200 dark:border-white/10 w-full gap-2 md:gap-4 glass-panel p-2 rounded-t-[1.5rem] border-t border-x">
        <button
          onClick={() => setActiveSubTab('theory')}
          className={`pb-3 pt-2 px-6 font-black text-base relative transition-all cursor-pointer ${
            activeSubTab === 'theory' 
              ? 'text-slate-900 dark:text-white font-extrabold' 
              : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white hover:bg-white dark:bg-white/5 rounded-xl'
          }`}
        >
          {activeSubTab === 'theory' && (
            <motion.div 
              layoutId="activeSubTab-pill" 
              className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-600 to-purple-600 shadow-[0_0_15px_rgba(37,99,235,0.6)] rounded-full"
              transition={{ type: "spring", stiffness: 350, damping: 28 }}
            />
          )}
          <span className="flex items-center gap-2">
            <FileText size={16} />
            Contenido Teórico
          </span>
        </button>
        <button
          onClick={() => setActiveSubTab('questions')}
          className={`pb-3 pt-2 px-6 font-black text-base relative transition-all cursor-pointer ${
            activeSubTab === 'questions' 
              ? 'text-slate-900 dark:text-white font-extrabold' 
              : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white hover:bg-white dark:bg-white/5 rounded-xl'
          }`}
        >
          {activeSubTab === 'questions' && (
            <motion.div 
              layoutId="activeSubTab-pill" 
              className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-600 to-purple-600 shadow-[0_0_15px_rgba(37,99,235,0.6)] rounded-full"
              transition={{ type: "spring", stiffness: 350, damping: 28 }}
            />
          )}
          <span className="flex items-center gap-2">
            <Settings size={16} />
            Banco de Preguntas
          </span>
        </button>
        <button
          onClick={() => setActiveSubTab('simulator')}
          className={`pb-3 pt-2 px-6 font-black text-base relative transition-all cursor-pointer ${
            activeSubTab === 'simulator' 
              ? 'text-slate-900 dark:text-white font-extrabold' 
              : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:text-white hover:bg-white dark:bg-white/5 rounded-xl'
          }`}
        >
          {activeSubTab === 'simulator' && (
            <motion.div 
              layoutId="activeSubTab-pill" 
              className="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-600 to-purple-600 shadow-[0_0_15px_rgba(37,99,235,0.6)] rounded-full"
              transition={{ type: "spring", stiffness: 350, damping: 28 }}
            />
          )}
          <span className="flex items-center gap-2">
            <Shield size={16} />
            Simulador de Alumno
          </span>
        </button>
      </div>

      {/* Main Layout Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start">
        
        {/* Left Column: Selectors */}
        <div className="lg:col-span-1 bg-white dark:bg-white/5 backdrop-blur-2xl border border-slate-200 dark:border-white/10 rounded-[2.2rem] shadow-2xl p-5 flex flex-col gap-5">
          <h3 className="text-xs font-bold text-slate-500 dark:text-[#8E8E93] uppercase tracking-wider px-2">Selector de Nivel</h3>
          
          {/* Phase selector */}
          <div className="flex flex-col gap-2">
            <label className="text-xs font-black text-slate-500 uppercase tracking-wider px-2">Fase</label>
            <select
              value={mgrFaseId}
              onChange={(e) => {
                const fid = parseInt(e.target.value);
                setMgrFaseId(fid);
                const phase = PHASE_MAPS.find(p => p.id === fid);
                if (phase?.modules && phase.modules.length > 0) {
                  setMgrModuloId(phase.modules[0].id);
                  setMgrLevelId(phase.modules[0].levels[0]?.id || 1);
                } else if (phase?.levels && phase.levels.length > 0) {
                  setMgrModuloId(0);
                  setMgrLevelId(phase.levels[0].id);
                } else {
                  setMgrModuloId(1);
                  setMgrLevelId(1);
                }
              }}
              className="bg-white/80 dark:bg-slate-950 border border-slate-200 dark:border-white/10 rounded-xl p-3 text-sm font-bold text-slate-900 dark:text-white focus:outline-none focus:border-blue-500/50 cursor-pointer"
            >
              {PHASE_MAPS.map(p => (
                <option key={p.id} value={p.id} className="text-slate-900 bg-white dark:text-white dark:bg-slate-900">{p.name.split(':')[0]}</option>
              ))}
            </select>
          </div>

          {/* Module selector */}
          {activePhase?.modules && activePhase.modules.length > 0 && (
            <div className="flex flex-col gap-2">
              <label className="text-xs font-black text-slate-500 uppercase tracking-wider px-2">Módulo</label>
              <select
                value={mgrModuloId}
                onChange={(e) => {
                  const mid = parseInt(e.target.value);
                  setMgrModuloId(mid);
                  const levels = activePhase.modules.find(m => m.id === mid)?.levels || [];
                  setMgrLevelId(levels[0]?.id || 1);
                }}
                className="bg-white/80 dark:bg-slate-950 border border-slate-200 dark:border-white/10 rounded-xl p-3 text-sm font-bold text-slate-900 dark:text-white focus:outline-none focus:border-blue-500/50 cursor-pointer"
              >
                {activePhase.modules.map(m => (
                  <option key={m.id} value={m.id} className="text-slate-900 bg-white dark:text-white dark:bg-slate-900">{m.name}</option>
                ))}
              </select>
            </div>
          )}

          {/* Level selector */}
          <div className="flex flex-col gap-2">
            <label className="text-xs font-black text-slate-500 uppercase tracking-wider px-2">Nivel / Desafío</label>
            <select
              value={mgrLevelId}
              onChange={(e) => setMgrLevelId(parseInt(e.target.value))}
              className="bg-white/80 dark:bg-slate-950 border border-slate-200 dark:border-white/10 rounded-xl p-3 text-sm font-bold text-slate-900 dark:text-white focus:outline-none focus:border-blue-500/50 cursor-pointer"
            >
              {activeLevelList.map(l => (
                <option key={l.id} value={l.id} className="text-slate-900 bg-white dark:text-white dark:bg-slate-900">
                  {l.isChallenge ? 'Desafío' : 'Nivel'} {l.id}: {l.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Right Column: Dynamic Tabs Content */}
        <div className="lg:col-span-3 flex flex-col gap-6">

          {/* Breadcrumb Navigation */}
          <nav className="flex items-center gap-1.5 text-[12px] text-slate-500 dark:text-slate-400 font-medium px-1">
            <span className="text-slate-700 dark:text-slate-300">Administración</span>
            <ChevronRight size={12} />
            <span className="text-slate-700 dark:text-slate-300">
              {activePhase?.name?.split(':')[0] || `Fase ${mgrFaseId}`}
            </span>
            {activeModule && (
              <>
                <ChevronRight size={12} />
                <span className="text-slate-700 dark:text-slate-300">
                  {activeModule.name?.split(':')[0] || `Módulo ${mgrModuloId}`}
                </span>
              </>
            )}
            <ChevronRight size={12} />
            <span className="text-blue-500 dark:text-blue-400 font-bold">
              {activeLevel?.isChallenge ? 'Desafío' : 'Nivel'} {mgrLevelId}
            </span>
          </nav>

          <AnimatePresence mode="wait">
            
            {/* TAB A: THEORY / CONCEPTS EDITOR */}
            {activeSubTab === 'theory' && (
              <motion.div
                key="theory-tab"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.2 }}
              >
                <TheoryEditor
                  theory={theory}
                  setTheory={setTheory}
                  loadingTheory={loadingTheory}
                  savingTheory={savingTheory}
                  onSave={handleSaveTheory}
                  mgrFaseId={mgrFaseId}
                  mgrModuloId={mgrModuloId}
                  mgrLevelId={mgrLevelId}
                  PHASE_MAPS={PHASE_MAPS}
                  showConfirm={showConfirm}
                  showToast={showToast}
                />
              </motion.div>
            )}

            {/* TAB B: QUESTIONS LIST & PAGINATION */}
            {activeSubTab === 'questions' && (
              <motion.div
                key="questions-tab"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.2 }}
              >
                <QuestionTable
                  questions={questions}
                  loadingQuestions={loadingQuestions}
                  onOpenAddModal={openNewQuestionModal}
                  onOpenEditModal={openEditQuestionModal}
                  onDeleteQuestion={handleDeleteQuestion}
                  questionsPerPage={questionsPerPage}
                  setQuestionsPerPage={setQuestionsPerPage}
                  currentPage={currentPage}
                  setCurrentPage={setCurrentPage}
                  searchQuery={questionSearchQuery}
                  setSearchQuery={setQuestionSearchQuery}
                />
              </motion.div>
            )}

            {/* TAB C: STUDENT VIEW SIMULATOR */}
            {activeSubTab === 'simulator' && (
              <motion.div
                key="simulator-tab"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.2 }}
              >
                <StudentViewSimulator
                  theory={theory}
                  questions={questions}
                  mgrFaseId={mgrFaseId}
                  mgrModuloId={mgrModuloId}
                  mgrLevelId={mgrLevelId}
                  showToast={showToast}
                />
              </motion.div>
            )}

          </AnimatePresence>
        </div>
      </div>

      {/* QUESTION EDIT/CREATE FORM MODAL */}
      <QuestionFormModal
        isOpen={showQuestionModal}
        onClose={() => { setShowQuestionModal(false); setEditingQuestion(null); }}
        editingQuestion={editingQuestion}
        setEditingQuestion={setEditingQuestion}
        savingQuestion={savingQuestion}
        onSave={handleSaveQuestion}
        showToast={showToast}
      />

    </div>
  );
};

export default ContentTab;
