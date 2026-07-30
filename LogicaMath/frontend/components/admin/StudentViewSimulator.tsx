import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  BookOpen, Target, Award, ArrowRight, ArrowLeft, 
  FastForward, CheckCircle, XCircle, Smartphone, Info,
  Maximize, Minimize
} from 'lucide-react';
import { TeacherCommentBox } from './TeacherCommentBox';
import { safeHtml, sanitizeHtml } from '../../services/textService';

interface StudentViewSimulatorProps {
  theory: any;
  questions: any[];
  mgrFaseId: number;
  mgrModuloId: number;
  mgrLevelId: number;
  showToast: (message: string, type: 'success' | 'error') => void;
}

export const StudentViewSimulator: React.FC<StudentViewSimulatorProps> = ({
  theory,
  questions = [],
  mgrFaseId,
  mgrModuloId,
  mgrLevelId,
  showToast
}) => {
  // Navigation inside the simulator
  const [simTab, setSimTab] = useState<'theory' | 'guided' | 'free'>('theory');
  
  // Interactive theory states
  const [theoryStep, setTheoryStep] = useState(0);
  const [theoryAnswers, setTheoryAnswers] = useState<Record<number, string>>({});
  const [theoryFeedback, setTheoryFeedback] = useState<Record<number, { isCorrect: boolean; message: string }>>({});

  // Question navigation states
  const [guidedIdx, setGuidedIdx] = useState(0);
  const [freeIdx, setFreeIdx] = useState(0);
  
  // Free play state
  const [freeAnswer, setFreeAnswer] = useState('');
  const [freeFeedback, setFreeFeedback] = useState<{ isCorrect: boolean; message: string } | null>(null);

  // Fullscreen state
  const [isExpanded, setIsExpanded] = useState(false);

  // ResizeObserver simulation for canvas aspects
  const containerRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState({ width: 640, height: 480 });

  useEffect(() => {
    if (!containerRef.current) return;
    const observer = new ResizeObserver((entries) => {
      for (let entry of entries) {
        setDimensions({
          width: entry.contentRect.width,
          height: entry.contentRect.height
        });
      }
    });
    observer.observe(containerRef.current);
    return () => observer.disconnect();
  }, []);

  // Reset indices when level selectors change
  useEffect(() => {
    setTheoryStep(0);
    setTheoryAnswers({});
    setTheoryFeedback({});
    setGuidedIdx(0);
    setFreeIdx(0);
    setFreeAnswer('');
    setFreeFeedback(null);
  }, [mgrFaseId, mgrModuloId, mgrLevelId]);

  // Calculations for theory slides
  const slides = React.useMemo(() => {
    const s: { type: string; data: any }[] = [];
    if (!theory) return s;
    s.push({ type: 'intro', data: null });
    
    if (theory.ejemplos && theory.ejemplos.length > 0) {
      theory.ejemplos.forEach((ex: any, idx: number) => {
        s.push({ type: 'example', data: { ...ex, index: idx } });
      });
    }

    if (theory.interactivos && theory.interactivos.length > 0) {
      theory.interactivos.forEach((int: any, idx: number) => {
        s.push({ type: 'interactive', data: { ...int, index: idx } });
      });
    }

    if (theory.advertencia) {
      s.push({ type: 'tip', data: theory.advertencia });
    }

    return s;
  }, [theory]);

  // Handle skip function (avoids answering blocks)
  const handleSkipQuestion = () => {
    if (simTab === 'guided') {
      if (questions.length === 0) return;
      setGuidedIdx(prev => (prev + 1) % questions.length);
      showToast('Omitido: Avanzando a la siguiente pregunta guiada.', 'success');
    } else if (simTab === 'free') {
      if (questions.length === 0) return;
      setFreeIdx(prev => (prev + 1) % questions.length);
      setFreeAnswer('');
      setFreeFeedback(null);
      showToast('Omitido: Avanzando a la siguiente pregunta libre.', 'success');
    } else {
      if (theoryStep < slides.length - 1) {
        setTheoryStep(prev => prev + 1);
        showToast('Omitido: Avanzando de sección de teoría.', 'success');
      }
    }
  };

  const handleVerifyTheory = (idx: number, correctRes: string, msgOk: string, msgErr: string) => {
    const val = theoryAnswers[idx]?.trim();
    if (!val) return;
    
    const normalize = (text: string) => 
      text.toLowerCase()
          .normalize("NFD")
          .replace(/[\u0300-\u036f]/g, "")
          .replace(/\s+/g, '')
          .replace(/,/g, '.')
          .replace(/%/g, '');

    if (normalize(val) === normalize(correctRes)) {
      setTheoryFeedback(prev => ({ ...prev, [idx]: { isCorrect: true, message: msgOk || '¡Excelente!' } }));
    } else {
      setTheoryFeedback(prev => ({ ...prev, [idx]: { isCorrect: false, message: msgErr || 'Inténtalo de nuevo.' } }));
    }
  };

  const handleVerifyFree = (correctRes: string) => {
    const val = freeAnswer.trim();
    if (!val) return;
    
    const normalize = (text: string) => 
      text.toLowerCase()
          .normalize("NFD")
          .replace(/[\u0300-\u036f]/g, "")
          .replace(/\s+/g, '')
          .replace(/,/g, '.')
          .replace(/%/g, '');

    if (normalize(val) === normalize(correctRes)) {
      setFreeFeedback({ isCorrect: true, message: '¡Fabuloso! Tu respuesta es correcta.' });
    } else {
      setFreeFeedback({ isCorrect: false, message: 'Respuesta incorrecta. ¡Analiza e intenta de nuevo!' });
    }
  };

  const activeQuestion = questions[simTab === 'guided' ? guidedIdx : freeIdx] || null;

  return (
    <div className="flex flex-col gap-6 w-full">
      {/* Selector de sub-pestañas del simulador */}
      <div className="flex justify-between items-center bg-white/5 border border-white/10 rounded-2xl p-2 gap-2">
        <div className="flex gap-2">
          <button
            onClick={() => setSimTab('theory')}
            className={`px-4 py-2 text-xs font-black rounded-xl flex items-center gap-1.5 transition-all cursor-pointer ${simTab === 'theory' ? 'bg-purple-600 text-white' : 'text-slate-400 hover:bg-white/5'}`}
          >
            <BookOpen size={14} />
            1. Teoría
          </button>
          <button
            onClick={() => setSimTab('guided')}
            className={`px-4 py-2 text-xs font-black rounded-xl flex items-center gap-1.5 transition-all cursor-pointer ${simTab === 'guided' ? 'bg-blue-600 text-white' : 'text-slate-400 hover:bg-white/5'}`}
          >
            <Target size={14} />
            2. Preguntas Guiadas
          </button>
          <button
            onClick={() => setSimTab('free')}
            className={`px-4 py-2 text-xs font-black rounded-xl flex items-center gap-1.5 transition-all cursor-pointer ${simTab === 'free' ? 'bg-green-600 text-white' : 'text-slate-400 hover:bg-white/5'}`}
          >
            <Award size={14} />
            3. Prueba Libre
          </button>
        </div>

        {/* Botón de Skip especial para Docentes */}
        <div className="flex gap-2">
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="px-4 py-2 bg-slate-700/50 hover:bg-slate-600 text-white text-xs font-black rounded-xl flex items-center gap-1.5 transition-all active:scale-95 cursor-pointer shadow-md border border-slate-600"
            title="Pantalla Completa"
          >
            {isExpanded ? <Minimize size={14} /> : <Maximize size={14} />}
            {isExpanded ? 'Reducir' : 'Expandir'}
          </button>
          <button
            onClick={handleSkipQuestion}
            className="px-4 py-2 bg-yellow-600/20 hover:bg-yellow-600 border border-yellow-500/30 hover:text-black text-yellow-400 text-xs font-black rounded-xl flex items-center gap-1.5 transition-all active:scale-95 cursor-pointer shadow-md"
            title="Avanzar sin responder (Exclusivo Administrador)"
          >
            <FastForward size={14} />
            Omitir / Avanzar
          </button>
        </div>
      </div>

      {/* Simulador de Pantalla de Alumno con Aspect Ratio Fijo de Tablet */}
      <div className={`w-full flex justify-center ${isExpanded ? 'fixed inset-0 z-[100] bg-black/90 backdrop-blur-sm p-4 md:p-10' : ''}`}>
        <div className={`relative w-full ${isExpanded ? 'max-w-6xl h-full' : 'max-w-[800px] aspect-[4/3]'} bg-slate-950 border-[16px] border-slate-900 rounded-[2.5rem] shadow-2xl overflow-hidden flex flex-col flex-shrink-0 transition-all duration-300`}>
          
          {/* Cámara frontal del iPad simulada */}
          <div className="absolute top-2 left-1/2 -translate-x-1/2 w-3 h-3 bg-slate-800 rounded-full z-50"></div>

          {/* Área de Visualización Reactiva */}
          <div 
            ref={containerRef} 
            className="flex-1 w-full overflow-y-auto custom-scrollbar p-6 bg-slate-900 text-white flex flex-col justify-between"
            style={{ fontSize: dimensions.width < 500 ? '12px' : '14px' }}
          >
            <AnimatePresence mode="wait">
              {/* VISTA 1: TEORÍA */}
              {simTab === 'theory' && theory && (
                <motion.div
                  key={`sim-theory-${theoryStep}`}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  className="flex-1 flex flex-col justify-between h-full min-h-[300px]"
                >
                  <div className="flex-1 flex flex-col gap-4">
                    {/* Header */}
                    <div className="border-b border-white/5 pb-2">
                      <span className="text-[10px] text-purple-400 font-bold uppercase tracking-widest">
                        Fase {mgrFaseId} • Nivel {mgrLevelId}
                      </span>
                      <h3 className="text-lg font-black text-white flex items-center gap-1.5 mt-0.5">
                        ✨ {theory.titulo || 'Teoría del Nivel'}
                      </h3>
                    </div>

                    {/* Intro slide */}
                    {slides[theoryStep]?.type === 'intro' && (
                      <div className="flex flex-col gap-3">
                        <div 
                          className="text-xs text-slate-300 leading-relaxed font-medium rendered-html-content"
                          dangerouslySetInnerHTML={safeHtml(theory.texto_descubrimiento || 'Sin descripción disponible.')}
                        />
                        
                        {theory.diccionario && Object.keys(theory.diccionario).length > 0 && (
                          <div className="mt-2 bg-white/5 border border-white/10 rounded-xl p-4">
                            <h4 className="text-xs font-black text-purple-300 uppercase tracking-wider mb-2">📖 Glosario:</h4>
                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                              {Object.entries(theory.diccionario).map(([k, v]: [string, any], idx) => (
                                <div key={idx} className="bg-slate-950/40 p-2 rounded-lg border border-white/5">
                                  <strong className="text-xs text-purple-400 block">{k}</strong>
                                  <span className="text-[10px] text-slate-400 font-medium">{v}</span>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}

                    {/* Example slide */}
                    {slides[theoryStep]?.type === 'example' && (
                      <div className="flex flex-col gap-3">
                        <span className="text-xs font-bold text-slate-400">EJEMPLO GUIADO {slides[theoryStep].data.index + 1}:</span>
                        <div className="bg-white/5 border border-white/10 rounded-xl p-4 flex flex-col gap-3">
                          <div 
                            className="text-xs font-bold text-purple-300 rendered-html-content"
                            dangerouslySetInnerHTML={safeHtml(slides[theoryStep].data.enunciado)}
                          />
                          {slides[theoryStep].data.pasos ? (
                            <div className="flex flex-col gap-2 bg-slate-950/30 p-3 rounded-lg border border-white/5">
                              {slides[theoryStep].data.pasos.map((p: any) => (
                                <div key={p.orden} className="flex gap-2 text-[11px] font-semibold text-slate-300 items-start">
                                  <span className="bg-purple-500/20 text-purple-300 px-1.5 rounded flex-shrink-0">{p.orden}</span>
                                  <div dangerouslySetInnerHTML={safeHtml(p.texto)} className="rendered-html-content" />
                                </div>
                              ))}
                            </div>
                          ) : (
                            <div className="text-xs text-green-400 font-bold flex gap-1">
                              <span>Respuesta:</span> 
                              <span dangerouslySetInnerHTML={safeHtml(slides[theoryStep].data.respuesta)} className="rendered-html-content" />
                            </div>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Interactive slide */}
                    {slides[theoryStep]?.type === 'interactive' && (
                      <div className="flex flex-col gap-3">
                        <span className="text-xs font-bold text-slate-400">EJERCICIO PRÁCTICO {slides[theoryStep].data.index + 1}:</span>
                        <div className="bg-white/5 border border-white/10 rounded-xl p-4 flex flex-col gap-3">
                          <div 
                            className="text-xs font-bold text-blue-300 rendered-html-content"
                            dangerouslySetInnerHTML={safeHtml(slides[theoryStep].data.enunciado)}
                          />
                          
                          {/* Pasos resolutivos */}
                          <div className="flex flex-col gap-2">
                            {slides[theoryStep].data.pasos?.map((p: any) => {
                              const isInput = p.texto.includes("= ?");
                              const globIdx = slides[theoryStep].data.index;
                              if (isInput) {
                                const parts = p.texto.split("= ?");
                                return (
                                  <div key={p.orden} className="flex flex-col sm:flex-row sm:items-center gap-2 text-xs">
                                    <div dangerouslySetInnerHTML={safeHtml(parts[0] + ' =')} className="rendered-html-content" />
                                    <div className="flex gap-1">
                                      <input 
                                        type="text"
                                        value={theoryAnswers[globIdx] || ''}
                                        onChange={(e) => setTheoryAnswers(prev => ({ ...prev, [globIdx]: e.target.value }))}
                                        className="bg-slate-950 border border-white/10 rounded px-2 py-1 text-xs text-white w-20 focus:outline-none focus:border-purple-500"
                                      />
                                      <button 
                                        onClick={() => handleVerifyTheory(globIdx, slides[theoryStep].data.respuesta, slides[theoryStep].data.feedback_acierto, slides[theoryStep].data.feedback_error)}
                                        className="bg-purple-600 px-2 py-1 rounded text-[10px] font-bold hover:bg-purple-500 transition-colors"
                                      >
                                        Validar
                                      </button>
                                    </div>
                                  </div>
                                );
                              }
                              return (
                                <div 
                                  key={p.orden} 
                                  className="text-[11px] text-slate-400 rendered-html-content"
                                  dangerouslySetInnerHTML={safeHtml(p.texto)}
                                />
                              );
                            })}
                          </div>

                          {theoryFeedback[slides[theoryStep].data.index] && (
                            <div className={`flex items-center gap-2 p-2 rounded-lg text-xs ${theoryFeedback[slides[theoryStep].data.index].isCorrect ? 'bg-green-500/10 text-green-400' : 'bg-red-500/10 text-red-400'}`}>
                              {theoryFeedback[slides[theoryStep].data.index].isCorrect ? <CheckCircle size={14} /> : <XCircle size={14} />}
                              <span>{theoryFeedback[slides[theoryStep].data.index].message}</span>
                            </div>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Tip slide */}
                    {slides[theoryStep]?.type === 'tip' && (
                      <div className="flex flex-col gap-4 text-center items-center py-6">
                        <div className="bg-yellow-500/10 border border-yellow-500/20 text-yellow-400 rounded-xl p-4 max-w-md">
                          <h4 className="text-xs font-black uppercase tracking-wider mb-1">💡 Advertencia / Tip:</h4>
                          <div 
                            className="text-[11px] font-medium leading-relaxed rendered-html-content"
                            dangerouslySetInnerHTML={safeHtml(slides[theoryStep].data)}
                          />
                        </div>
                        <div className="mt-4 text-lg">🚀 ¡Todo listo para empezar la práctica!</div>
                      </div>
                    )}
                  </div>

                  {/* Navigation controls footer */}
                  <div className="flex justify-between items-center border-t border-white/5 pt-4 mt-6">
                    <button
                      onClick={() => setTheoryStep(prev => Math.max(0, prev - 1))}
                      disabled={theoryStep === 0}
                      className="px-3 py-1.5 bg-white/5 hover:bg-white/10 disabled:opacity-30 rounded-lg text-[10px] font-bold flex items-center gap-1.5 cursor-pointer"
                    >
                      <ArrowLeft size={12} /> Atrás
                    </button>
                    <span className="text-[10px] text-slate-500 font-bold">Paso {theoryStep + 1} de {slides.length}</span>
                    <button
                      onClick={() => setTheoryStep(prev => Math.min(slides.length - 1, prev + 1))}
                      disabled={theoryStep === slides.length - 1}
                      className="px-3 py-1.5 bg-purple-600 hover:bg-purple-500 disabled:opacity-30 rounded-lg text-[10px] font-bold flex items-center gap-1.5 cursor-pointer"
                    >
                      Siguiente <ArrowRight size={12} />
                    </button>
                  </div>
                </motion.div>
              )}

              {/* VISTA 2: PREGUNTAS GUIADAS */}
              {simTab === 'guided' && (
                <motion.div
                  key={`sim-guided-${guidedIdx}`}
                  initial={{ opacity: 0, scale: 0.98 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.98 }}
                  className="flex-1 flex flex-col justify-between h-full min-h-[300px]"
                >
                  {questions.length === 0 ? (
                    <div className="flex-1 flex flex-col items-center justify-center text-center text-slate-500 py-10">
                      <Info size={32} className="mb-2 text-slate-600" />
                      <p className="text-xs font-bold">No hay preguntas cargadas en este nivel.</p>
                    </div>
                  ) : (
                    <div className="flex-1 flex flex-col justify-between">
                      <div className="flex flex-col gap-4">
                        <div className="border-b border-white/5 pb-2 flex justify-between items-center">
                          <span className="text-[10px] text-blue-400 font-bold uppercase tracking-widest">
                            Pregunta Guiada {guidedIdx + 1} de {questions.length}
                          </span>
                          <span className="text-[9px] bg-white/10 px-2 py-0.5 rounded-full font-bold uppercase text-slate-300">
                            {activeQuestion?.tipo_pregunta === 'multiple_opcion' ? 'Opción Múltiple' : 'Numérica'}
                          </span>
                        </div>

                        {/* Enunciado */}
                        <div className="bg-slate-900 border border-white/5 p-4 rounded-xl">
                          <div 
                            className="text-sm font-black leading-relaxed text-white rendered-html-content"
                            dangerouslySetInnerHTML={safeHtml(activeQuestion?.enunciado || '')}
                          />

                          {/* Imagen de Soporte */}
                          {activeQuestion?.datos_numericos?.url && (
                            <div className="mt-3 flex justify-center w-full max-h-[160px] overflow-hidden rounded-lg bg-black/40 border border-white/5 p-2">
                              <img 
                                src={activeQuestion.datos_numericos.url} 
                                alt="Visual support"
                                className="object-contain max-h-[140px] aspect-[16/9]"
                                onError={(e) => {
                                  (e.target as HTMLImageElement).src = ''; 
                                  showToast('Advertencia: URL de gráfico rota o inaccesible en MinIO.', 'error');
                                }}
                              />
                            </div>
                          )}
                        </div>

                        {/* Visual tutor feedback simulation */}
                        <div className="bg-blue-600/10 border border-blue-500/20 text-blue-300 rounded-xl p-3 text-[11px] leading-relaxed font-semibold">
                          ℹ️ En modo guiado, se analizan los errores cognitivos del alumno y se le da feedback inmediato si falla alguna alternativa.
                        </div>

                        {/* Options list */}
                        {activeQuestion?.tipo_pregunta === 'multiple_opcion' && activeQuestion.alternativas ? (
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-2">
                            {activeQuestion.alternativas.map((alt: any, idx: number) => (
                              <button
                                key={idx}
                                onClick={() => {
                                  if (alt.es_correcta) {
                                    showToast('¡Correcto! Opción acertada.', 'success');
                                  } else {
                                    showToast(`Error (${alt.tipo_error || 'general'}): ${alt.feedback_error || 'Inténtalo de nuevo.'}`, 'error');
                                  }
                                }}
                                className={`p-3 rounded-xl border text-left text-xs font-bold transition-all hover:scale-[1.01] cursor-pointer ${
                                  alt.es_correcta 
                                    ? 'bg-green-600/10 border-green-500/20 hover:bg-green-600/20 text-green-300' 
                                    : 'bg-white/5 border-white/10 hover:bg-white/10 text-slate-300'
                                }`}
                              >
                                <span dangerouslySetInnerHTML={safeHtml(alt.texto)} className="rendered-html-content block" />
                              </button>
                            ))}
                          </div>
                        ) : (
                          <div className="mt-2 flex flex-col gap-2">
                            <span className="text-[10px] text-slate-400 font-bold uppercase">Escribe tu respuesta numérica:</span>
                            <div className="flex gap-2">
                              <input 
                                type="text"
                                placeholder={`Correcta: ${activeQuestion?.respuesta_correcta}`}
                                className="bg-slate-950 border border-white/10 rounded-xl px-3 py-2 text-xs text-white focus:outline-none w-48"
                                disabled
                              />
                              <button 
                                onClick={() => showToast('En modo libre se evalúa el resultado completo.', 'success')}
                                className="bg-blue-600 hover:bg-blue-500 text-xs font-black px-4 py-2 rounded-xl transition-colors cursor-pointer"
                              >
                                Evaluar
                              </button>
                            </div>
                          </div>
                        )}
                      </div>

                      {/* Selector footer */}
                      <div className="flex justify-between items-center border-t border-white/5 pt-4 mt-6">
                        <button
                          onClick={() => setGuidedIdx(prev => Math.max(0, prev - 1))}
                          disabled={guidedIdx === 0}
                          className="px-3 py-1.5 bg-white/5 hover:bg-white/10 disabled:opacity-30 rounded-lg text-[10px] font-bold flex items-center gap-1.5 cursor-pointer"
                        >
                          <ArrowLeft size={12} /> Anterior
                        </button>
                        <button
                          onClick={() => setGuidedIdx(prev => Math.min(questions.length - 1, prev + 1))}
                          disabled={guidedIdx === questions.length - 1}
                          className="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 disabled:opacity-30 rounded-lg text-[10px] font-bold flex items-center gap-1.5 cursor-pointer"
                        >
                          Siguiente <ArrowRight size={12} />
                        </button>
                      </div>
                    </div>
                  )}
                </motion.div>
              )}

              {/* VISTA 3: PRUEBA LIBRE */}
              {simTab === 'free' && (
                <motion.div
                  key={`sim-free-${freeIdx}`}
                  initial={{ opacity: 0, scale: 0.98 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.98 }}
                  className="flex-1 flex flex-col justify-between h-full min-h-[300px]"
                >
                  {questions.length === 0 ? (
                    <div className="flex-1 flex flex-col items-center justify-center text-center text-slate-500 py-10">
                      <Info size={32} className="mb-2 text-slate-600" />
                      <p className="text-xs font-bold">No hay preguntas cargadas en este nivel.</p>
                    </div>
                  ) : (
                    <div className="flex-1 flex flex-col justify-between">
                      <div className="flex flex-col gap-4">
                        <div className="border-b border-white/5 pb-2 flex justify-between items-center">
                          <span className="text-[10px] text-green-400 font-bold uppercase tracking-widest">
                            Pregunta Libre {freeIdx + 1} de {questions.length}
                          </span>
                          <span className="text-[9px] bg-white/10 px-2 py-0.5 rounded-full font-bold uppercase text-slate-300">
                            {activeQuestion?.tipo_pregunta === 'multiple_opcion' ? 'Opción Múltiple' : 'Numérica'}
                          </span>
                        </div>

                        {/* Enunciado */}
                        <div className="bg-slate-900 border border-white/5 p-4 rounded-xl">
                          <div 
                            className="text-sm font-black leading-relaxed text-white rendered-html-content"
                            dangerouslySetInnerHTML={safeHtml(activeQuestion?.enunciado || '')}
                          />

                          {/* Imagen de Soporte */}
                          {activeQuestion?.datos_numericos?.url && (
                            <div className="mt-3 flex justify-center w-full max-h-[160px] overflow-hidden rounded-lg bg-black/40 border border-white/5 p-2">
                              <img 
                                src={activeQuestion.datos_numericos.url} 
                                alt="Visual support"
                                className="object-contain max-h-[140px] aspect-[16/9]"
                                onError={(e) => {
                                  (e.target as HTMLImageElement).src = ''; 
                                }}
                              />
                            </div>
                          )}
                        </div>

                        {/* Options list */}
                        {activeQuestion?.tipo_pregunta === 'multiple_opcion' && activeQuestion.alternativas ? (
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-2">
                            {activeQuestion.alternativas.map((alt: any, idx: number) => (
                              <button
                                key={idx}
                                onClick={() => handleVerifyFree(alt.texto)}
                                className={`p-3 rounded-xl border text-left text-xs font-bold transition-all hover:bg-white/5 cursor-pointer ${
                                  freeAnswer === alt.texto
                                    ? 'bg-purple-600/20 border-purple-500 text-purple-300'
                                    : 'bg-white/5 border-white/10 text-slate-300'
                                }`}
                              >
                                <span dangerouslySetInnerHTML={safeHtml(alt.texto)} className="rendered-html-content block" />
                              </button>
                            ))}
                          </div>
                        ) : (
                          <div className="mt-2 flex flex-col gap-2">
                            <span className="text-[10px] text-slate-400 font-bold uppercase">Escribe tu respuesta correcta:</span>
                            <div className="flex gap-2">
                              <input 
                                type="text"
                                placeholder="Escribe aquí tu respuesta numérica..."
                                value={freeAnswer}
                                onChange={(e) => setFreeAnswer(e.target.value)}
                                className="bg-slate-950 border border-white/10 rounded-xl px-3 py-2 text-xs text-white focus:outline-none w-48 font-bold"
                              />
                              <button 
                                onClick={() => handleVerifyFree(activeQuestion?.respuesta_correcta)}
                                className="bg-green-600 hover:bg-green-500 text-xs font-black px-4 py-2 rounded-xl transition-colors cursor-pointer"
                              >
                                Verificar
                              </button>
                            </div>
                          </div>
                        )}

                        {freeFeedback && (
                          <div className={`flex items-center gap-2 p-2.5 rounded-lg text-xs mt-2 ${freeFeedback.isCorrect ? 'bg-green-500/10 text-green-400 border border-green-500/20' : 'bg-red-500/10 text-red-400 border border-red-500/20'}`}>
                            {freeFeedback.isCorrect ? <CheckCircle size={14} /> : <XCircle size={14} />}
                            <span className="font-bold">{freeFeedback.message}</span>
                          </div>
                        )}
                      </div>

                      {/* Selector footer */}
                      <div className="flex justify-between items-center border-t border-white/5 pt-4 mt-6">
                        <button
                          onClick={() => {
                            setFreeIdx(prev => Math.max(0, prev - 1));
                            setFreeAnswer('');
                            setFreeFeedback(null);
                          }}
                          disabled={freeIdx === 0}
                          className="px-3 py-1.5 bg-white/5 hover:bg-white/10 disabled:opacity-30 rounded-lg text-[10px] font-bold flex items-center gap-1.5 cursor-pointer"
                        >
                          <ArrowLeft size={12} /> Anterior
                        </button>
                        <button
                          onClick={() => {
                            setFreeIdx(prev => Math.min(questions.length - 1, prev + 1));
                            setFreeAnswer('');
                            setFreeFeedback(null);
                          }}
                          disabled={freeIdx === questions.length - 1}
                          className="px-3 py-1.5 bg-green-600 hover:bg-green-500 disabled:opacity-30 rounded-lg text-[10px] font-bold flex items-center gap-1.5 cursor-pointer"
                        >
                          Siguiente <ArrowRight size={12} />
                        </button>
                      </div>
                    </div>
                  )}
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>

      {/* Caja de Comentarios del Docente contextualizada */}
      <TeacherCommentBox
        faseId={mgrFaseId}
        seccionId={
          // Calculate section ID format from active question or layout level config
          activeQuestion?.seccion || 
          ((PHASE_MAPS as any[]).find(p => p.id === mgrFaseId)?.modules?.find((m: any) => m.id === mgrModuloId)?.levels || (PHASE_MAPS as any[]).find(p => p.id === mgrFaseId)?.levels || [])[0]?.seccion || 
          101
        }
        preguntaId={simTab !== 'theory' ? activeQuestion?.id : null}
        tipo={simTab === 'theory' ? 'teoria' : 'pregunta'}
        showToast={showToast}
      />
    </div>
  );
};

// Mock map of phases for stand-alone layout tests if context is absent
const PHASE_MAPS = [
  { id: 1, name: "Fase 1: Primeros Pasos" },
  { id: 2, name: "Fase 2: Multiplicación" },
  { id: 3, name: "Fase 3: Geometría e Imágenes" },
  { id: 4, name: "Fase 4: Operatoria Decimal y Conversiones" },
  { id: 5, name: "Fase 5: Fracciones, Porcentajes y Proporciones" },
  { id: 6, name: "Fase 6: Volúmenes y Escalas" },
  { id: 7, name: "Fase 7: Tiempo y Planos" },
  { id: 8, name: "Fase 8: Probabilidad y Arreglos" }
];
