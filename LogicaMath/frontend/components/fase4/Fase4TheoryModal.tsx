import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BookOpen, CheckCircle, XCircle, ArrowRight, ArrowLeft, LogOut } from 'lucide-react';
import { Fase4Lectura } from './Fase4Types';
import { formatContent, fixEncoding } from '../../services/textService';
import { getAvatarUrl } from '../../services/storageService';
import './Fase4Styles.css';

interface Fase4TheoryModalProps {
  readingData: Fase4Lectura;
  moduleColor: string;
  onClose: () => void;
  onAbort?: () => void;
  userAvatar?: string;
  isInitialReading?: boolean;
  isEvaluatorMode?: boolean;
}

export const Fase4TheoryModal: React.FC<Fase4TheoryModalProps> = ({
  readingData,
  moduleColor,
  onClose,
  onAbort,
  userAvatar,
  isInitialReading = true,
  isEvaluatorMode
}) => {
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [feedback, setFeedback] = useState<Record<number, { isCorrect: boolean; message: string }>>({});

  const chunkArray = (arr: any[], size: number) => {
    if (!arr || arr.length === 0) return [];
    const chunks = [];
    for (let i = 0; i < arr.length; i += size) {
      chunks.push(arr.slice(i, i + size));
    }
    return chunks;
  };

  const slides = useMemo(() => {
    const s: { type: string; data: any }[] = [];
    const isModuleOne = readingData.modulo_id === 1;
    const dictionaryEntries = Object.entries(readingData.diccionario || {});

    s.push({ type: 'intro', data: null });

    if (isModuleOne && dictionaryEntries.length > 0) {
      const chunks = chunkArray(dictionaryEntries, 2);
      chunks.forEach(c => s.push({ type: 'dictionary', data: c }));
    }
    
    if (readingData.ejemplos && readingData.ejemplos.length > 0) {
      const chunks = chunkArray(readingData.ejemplos, 1);
      chunks.forEach(c => s.push({ type: 'examples', data: c }));
    } else {
      s.push({ type: 'examples', data: [] });
    }

    if (readingData.interactivos && readingData.interactivos.length > 0) {
      const withIndex = readingData.interactivos.map((item, index) => ({ ...item, globalIndex: index }));
      const chunks = chunkArray(withIndex, 1);
      chunks.forEach(c => s.push({ type: 'interactives', data: c }));
    }

    if (readingData.tip_pedagogico) {
      s.push({ type: 'tip', data: readingData.tip_pedagogico });
    }

    return s;
  }, [readingData]);

  const totalSteps = slides.length;
  const currentSlide = slides[currentStep];

  const blockInfo = useMemo(() => {
    if (!slides || slides.length === 0) return { label: 'Teoría 1 de 1' };
    const currentType = slides[currentStep]?.type;
    const sameTypeSlides = slides.filter(s => s.type === currentType);
    const indexInType = sameTypeSlides.findIndex(s => s === slides[currentStep]) + 1;
    const totalInType = sameTypeSlides.length;

    let typeName = 'Teoría';
    if (currentType === 'examples') typeName = 'Ejemplo';
    else if (currentType === 'dictionary') typeName = 'Diccionario';
    else if (currentType === 'interactives') typeName = 'Tu turno';
    else if (currentType === 'tip') typeName = 'Consejo';

    return { label: `${typeName} ${indexInType} de ${totalInType}` };
  }, [slides, currentStep]);

  const handleAnswerChange = (idx: number, val: string) => {
    setAnswers(prev => ({ ...prev, [idx]: val }));
    setFeedback(prev => {
      const newFb = { ...prev };
      delete newFb[idx];
      return newFb;
    });
  };

  const handleVerify = (idx: number, correctRes: string, msgOk: string, msgErr: string) => {
    const val = answers[idx]?.trim();
    if (!val) return;
    
    const normalize = (text: string) => 
      text.toLowerCase()
          .normalize("NFD")
          .replace(/[\u0300-\u036f]/g, "")
          .replace(/\s+/g, '')
          .replace(/,/g, '.')
          .replace(/%/g, '');

    if (normalize(val) === normalize(correctRes)) {
      setFeedback(prev => ({ ...prev, [idx]: { isCorrect: true, message: msgOk } }));
    } else {
      setFeedback(prev => ({ ...prev, [idx]: { isCorrect: false, message: msgErr } }));
    }
  };

  const canGoNext = useMemo(() => {
    if (isEvaluatorMode) return true;
    if (currentSlide?.type !== 'interactives') return true;
    const items = currentSlide.data;
    for (let i = 0; i < items.length; i++) {
      const globalIdx = items[i].globalIndex;
      const item = items[i];
      // Regla C2.3: Si es modo compromiso sin consecuencia, basta con haber interactuado.
      // NO exige acierto para habilitar el avance al siguiente paso.
      if (item.modo_compromiso || item.tipo === 'eleccion_guiada') {
        if (!feedback[globalIdx] && !answers[globalIdx]) return false;
      } else {
        if (!feedback[globalIdx] || !feedback[globalIdx].isCorrect) return false;
      }
    }
    return true;
  }, [currentSlide, feedback, answers, isEvaluatorMode]);

  const variants = {
    enter: (direction: number) => ({
      x: direction > 0 ? 50 : -50,
      opacity: 0
    }),
    center: {
      zIndex: 1,
      x: 0,
      opacity: 1
    },
    exit: (direction: number) => ({
      zIndex: 0,
      x: direction < 0 ? 50 : -50,
      opacity: 0
    })
  };

  const [direction, setDirection] = useState(0);

  const goToStep = (newStep: number) => {
    setDirection(newStep > currentStep ? 1 : -1);
    setCurrentStep(newStep);
  };

  return (
    <div className="f4-reading-overlay">
      <motion.div 
        initial={{ scale: 0.9, y: 20, opacity: 0 }}
        animate={{ scale: 1, y: 0, opacity: 1 }}
        exit={{ scale: 0.9, y: 20, opacity: 0 }}
        className="f4-reading-card flashcard-mode"
      >
        <div className="f4-reading-header">
          <div className="f4-reading-icon" style={{ backgroundColor: `${moduleColor}22`, color: moduleColor, flexShrink: 0 }}>
            <BookOpen size={24} />
          </div>
          <div style={{ flex: 1 }}>
            <div style={{
              fontSize: '0.8rem',
              fontWeight: 800,
              textTransform: 'uppercase',
              color: moduleColor,
              letterSpacing: '1.2px',
              marginBottom: '2px'
            }}>
              {readingData.fase_nombre || 'Operatoria Decimal y Conversiones'} • Módulo {readingData.modulo_id}: {readingData.modulo_nombre || `Módulo ${readingData.modulo_id}`} • Nivel {readingData.nivel_id}
            </div>
            <h2 style={{ display: 'flex', alignItems: 'center', gap: '12px', margin: 0, fontSize: '1.4rem', fontWeight: 800 }}>
               ✨ {fixEncoding(readingData.titulo)}
            </h2>
          </div>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flexShrink: 0 }}>
            {onAbort && (
              <button 
                onClick={onAbort}
                title={isInitialReading ? "Salir del nivel" : "Cerrar Teoría"}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  background: 'rgba(239, 68, 68, 0.12)',
                  border: '1px solid rgba(239, 68, 68, 0.3)',
                  color: '#ef4444',
                  padding: '8px',
                  borderRadius: '50%',
                  cursor: 'pointer',
                  width: '36px',
                  height: '36px',
                  transition: 'all 0.2s ease'
                }}
                className="f4-abort-btn"
              >
                <LogOut size={16} />
              </button>
            )}
            <div className="f4-step-indicator" style={{ marginTop: 0 }}>
              {blockInfo.label}
            </div>
          </div>
        </div>
        
        <div className="f4-reading-body flashcard-body">
          <AnimatePresence mode="wait" custom={direction}>
            {currentSlide?.type === 'intro' && (
              <motion.div
                key="intro"
                custom={direction}
                variants={variants}
                initial="enter"
                animate="center"
                exit="exit"
                transition={{ duration: 0.3 }}
                className="f4-flashcard-content"
              >
                {readingData.parrafos.map((p, idx) => (
                  <p key={idx} className="f4-reading-p" dangerouslySetInnerHTML={{ __html: formatContent(p) }} />
                ))}

                {readingData.modulo_id !== 1 && readingData.diccionario && Object.keys(readingData.diccionario).length > 0 && (
                  <div className="f4-reading-dictionary">
                    <h3>📖 EL DICCIONARIO DEL NIVEL:</h3>
                    <div className="f4-dict-grid">
                      {Object.entries(readingData.diccionario).map(([termino, definicion], idx) => (
                        <div key={idx} className="f4-dict-card" style={{ borderColor: `${moduleColor}55` }}>
                          <div className="f4-dict-term" style={{ color: moduleColor }} dangerouslySetInnerHTML={{ __html: formatContent(termino) }} />
                          <div className="f4-dict-def" dangerouslySetInnerHTML={{ __html: formatContent(definicion as string) }} />
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </motion.div>
            )}

            {currentSlide?.type === 'dictionary' && (
              <motion.div
                key={`dictionary-${currentStep}`}
                custom={direction}
                variants={variants}
                initial="enter"
                animate="center"
                exit="exit"
                transition={{ duration: 0.3 }}
                className="f4-flashcard-content"
              >
                <div className="f4-reading-dictionary standalone">
                  <h3>📖 EL DICCIONARIO DEL NIVEL:</h3>
                  <div className="f4-dict-grid">
                    {currentSlide.data.map(([termino, definicion]: [string, string], idx: number) => (
                      <div key={`${termino}-${idx}`} className="f4-dict-card" style={{ borderColor: `${moduleColor}55` }}>
                        <div className="f4-dict-term" style={{ color: moduleColor }} dangerouslySetInnerHTML={{ __html: formatContent(termino) }} />
                        <div className="f4-dict-def" dangerouslySetInnerHTML={{ __html: formatContent(definicion) }} />
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}

            {currentSlide?.type === 'examples' && (
              <motion.div
                key={`examples-${currentStep}`}
                custom={direction}
                variants={variants}
                initial="enter"
                animate="center"
                exit="exit"
                transition={{ duration: 0.3 }}
                className="f4-flashcard-content"
              >
                {currentSlide.data.length > 0 ? (
                  <div className="f4-reading-examples">
                    <h3>EJEMPLOS GUIADOS:</h3>
                    {currentSlide.data.map((ex: any, idx: number) => (
                      <div key={idx} className="f4-example-box">
                        <div className="f4-ex-q" dangerouslySetInnerHTML={{ __html: formatContent(ex.enunciado) }} />
                        {ex.pasos ? (
                          <div className="f4-ex-steps">
                            {ex.pasos.map((paso: any) => (
                              <div key={paso.orden} className="f4-ex-step">
                                <span className="f4-ex-step-num">{paso.orden}</span>
                                <span dangerouslySetInnerHTML={{ __html: formatContent(paso.texto) }} />
                              </div>
                            ))}
                          </div>
                        ) : (
                           <div className="f4-ex-legacy">→ <span style={{ color: moduleColor }} dangerouslySetInnerHTML={{ __html: formatContent(ex.respuesta) }} /></div>
                        )}
                      </div>
                    ))}
                  </div>

                ) : (
                  <div className="f4-reading-p">No hay ejemplos para este nivel. Avanza al siguiente paso.</div>
                )}
              </motion.div>
            )}

            {currentSlide?.type === 'interactives' && (
              <motion.div
                key={`interactives-${currentStep}`}
                custom={direction}
                variants={variants}
                initial="enter"
                animate="center"
                exit="exit"
                transition={{ duration: 0.3 }}
                className="f4-flashcard-content"
              >
                <div className="f4-reading-interactive">
                  <h3>¡Tu turno! Completa los ejercicios:</h3>
                  {currentSlide.data.map((int: any, localIdx: number) => {
                    const idx = int.globalIndex;
                    const qText = int.enunciado || int.pregunta;
                    const isCorrect = feedback[idx]?.isCorrect;
                    const isLocked = localIdx > 0 && !feedback[currentSlide.data[localIdx - 1].globalIndex]?.isCorrect;
                    
                    return (
                      <div 
                        key={idx} 
                        className={`f4-interactive-box ${isCorrect ? 'correct' : ''} ${feedback[idx] && !isCorrect ? 'error' : ''}`}
                        style={isLocked ? { position: 'relative', overflow: 'hidden', minHeight: '110px' } : {}}
                      >
                        <div 
                          className="f4-int-q"
                          style={isLocked ? { filter: 'blur(5px)', opacity: 0.3, pointerEvents: 'none', userSelect: 'none' } : {}}
                          dangerouslySetInnerHTML={{ __html: qText }}
                        />
                        
                        {isLocked ? (
                          <div style={{
                            position: 'absolute',
                            inset: 0,
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            justifyContent: 'center',
                            backgroundColor: 'rgba(19, 25, 41, 0.85)',
                            zIndex: 10,
                            borderRadius: '12px',
                            gap: '8px',
                            border: '1px dashed rgba(255, 255, 255, 0.15)'
                          }}>
                            <span style={{ fontSize: '1.4rem' }}>🔒</span>
                            <span style={{ fontSize: '0.85rem', color: '#8a9bbf', fontWeight: 650 }}>
                              Completa el ejercicio anterior para desbloquear
                            </span>
                          </div>
                        ) : (
                          <>
                            {int.pasos && (
                              <div className="f4-ex-steps">
                                {int.pasos.map((paso: any) => {
                                  const isInputPaso = paso.texto.includes("= ?");
                                  if (isInputPaso) {
                                    const parts = paso.texto.split("= ?");
                                    return (
                                      <div key={paso.orden} className="f4-ex-step input-step">
                                        <span className="f4-ex-step-num">{paso.orden}</span>
                                        <span>{parts[0]} = </span>
                                        <div className="f4-int-input-group">
                                          <input 
                                            type="number" 
                                            className="f4-int-input"
                                            value={answers[idx] || ''}
                                            onChange={(e) => handleAnswerChange(idx, e.target.value)}
                                            disabled={isCorrect}
                                            onKeyDown={(e) => {
                                              if (e.key === 'Enter') handleVerify(idx, int.respuesta, int.feedback_acierto, int.feedback_error);
                                            }}
                                          />
                                          {!isCorrect && (
                                            <button 
                                              className="f4-int-verify"
                                              style={{ backgroundColor: moduleColor }}
                                              onClick={() => handleVerify(idx, int.respuesta, int.feedback_acierto, int.feedback_error)}
                                            >
                                              Verificar
                                            </button>
                                          )}
                                        </div>
                                      </div>
                                    );
                                  }
                                  return (
                                    <div key={paso.orden} className="f4-ex-step">
                                      <span className="f4-ex-step-num">{paso.orden}</span>
                                      <span>{paso.texto}</span>
                                    </div>
                                  );
                                })}
                              </div>
                            )}
                            {int.opciones && int.opciones.length > 0 ? (
                              <div className="f4-choice-step-container mt-3">
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3">
                                  {int.opciones.map((opt: any) => {
                                    const isSelected = answers[idx] === opt.id || answers[idx] === opt.texto;
                                    const isOptCorrect = opt.id === int.respuesta || opt.texto === int.respuesta;
                                    const hasChosen = !!answers[idx];
                                    return (
                                      <button
                                        key={opt.id}
                                        disabled={hasChosen && (int.modo_compromiso || int.tipo === 'eleccion_guiada')}
                                        onClick={() => {
                                          handleAnswerChange(idx, opt.id);
                                          const isRight = opt.id === int.respuesta || opt.texto === int.respuesta;
                                          setFeedback(prev => ({
                                            ...prev,
                                            [idx]: {
                                              isCorrect: isRight,
                                              message: isRight ? int.feedback_acierto : int.feedback_error
                                            }
                                          }));
                                        }}
                                        className={`p-3 rounded-xl border text-left transition-all font-semibold ${
                                          isSelected
                                            ? (isOptCorrect ? 'bg-green-500/20 border-green-500 text-green-300' : 'bg-red-500/20 border-red-500 text-red-300')
                                            : (hasChosen && isOptCorrect ? 'bg-green-500/10 border-green-500/50 text-green-200' : 'bg-white/5 border-white/10 text-white hover:bg-white/10')
                                        }`}
                                      >
                                        {opt.texto}
                                      </button>
                                    );
                                  })}
                                </div>
                                {answers[idx] && (
                                  <div className="f4-revelation-card p-4 rounded-xl bg-white/5 border border-white/10 mt-3">
                                    <div className="font-bold text-sm text-yellow-400 mb-2 flex items-center gap-2">
                                      <span>💡 Explicación pedagógica de la revelación:</span>
                                    </div>
                                    {int.explicacion_opciones ? (
                                      <div className="flex flex-col gap-2 text-xs text-white/90">
                                        {Object.entries(int.explicacion_opciones).map(([k, exp]: [string, any]) => (
                                          <div key={k} className="p-2 rounded bg-black/20 border border-white/5">
                                            <strong style={{ color: moduleColor }}>{k}:</strong> {exp}
                                          </div>
                                        ))}
                                      </div>
                                    ) : (
                                      <div className="text-sm text-white/90">
                                        {feedback[idx]?.message || int.feedback_acierto}
                                      </div>
                                    )}
                                  </div>
                                )}
                              </div>
                            ) : (
                              <>
                                {!int.pasos && (
                                  <div className="f4-int-input-group legacy">
                                    <input 
                                      type="text" 
                                      className="f4-int-input"
                                      value={answers[idx] || ''}
                                      onChange={(e) => handleAnswerChange(idx, e.target.value)}
                                      disabled={isCorrect}
                                      onKeyDown={(e) => {
                                        if (e.key === 'Enter') handleVerify(idx, int.respuesta, int.feedback_acierto, int.feedback_error);
                                      }}
                                    />
                                    {!isCorrect && (
                                      <button 
                                        className="f4-int-verify"
                                        style={{ backgroundColor: moduleColor }}
                                        onClick={() => handleVerify(idx, int.respuesta, int.feedback_acierto, int.feedback_error)}
                                      >
                                        Verificar
                                      </button>
                                    )}
                                  </div>
                                )}
                              </>
                            )}
                            
                            {feedback[idx] && !int.opciones && (
                              <div className={`f4-int-feedback ${feedback[idx].isCorrect ? 'success' : 'error'}`}>
                                {feedback[idx].isCorrect ? <CheckCircle size={18} /> : <XCircle size={18} />}
                                <span>{feedback[idx].message}</span>
                              </div>
                            )}
                          </>
                        )}
                      </div>
                    );
                  })}
                </div>
              </motion.div>
            )}

            {currentSlide?.type === 'tip' && (
              <motion.div
                key="tip"
                custom={direction}
                variants={variants}
                initial="enter"
                animate="center"
                exit="exit"
                transition={{ duration: 0.3 }}
                className="f4-flashcard-content"
              >
                <div className="f4-reading-tip highlighted">
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px', color: '#f59e0b', fontWeight: 800, fontSize: '1.05rem' }}>
                    <span style={{ fontSize: '1.25rem' }}>⚠️</span>
                    <span>¡CONSEJO IMPORTANTE!</span>
                  </div>
                  <div style={{ fontSize: '1.05rem', color: '#fffbeb', lineHeight: 1.5 }}>
                    {currentSlide.data}
                  </div>
                </div>

                <div className="f4-ready-container">
                  <motion.div 
                    className="f4-ready-rocket"
                    animate={{ 
                      y: [0, -15, 0],
                      rotate: [0, 5, -5, 0]
                    }}
                    transition={{ 
                      duration: 3, 
                      repeat: Infinity,
                      ease: "easeInOut"
                    }}
                  >
                    🚀
                  </motion.div>
                  <div className="f4-ready-msg">
                    ¡Excelente trabajo!<br />
                    Estás listo para la práctica libre.
                  </div>
                  <div className="f4-ready-stars">
                    {[...Array(5)].map((_, i) => (
                      <motion.span 
                        key={i}
                        className="f4-ready-star"
                        animate={{ opacity: [0.2, 1, 0.2], scale: [1, 1.2, 1] }}
                        transition={{ duration: 2 + i * 0.5, repeat: Infinity }}
                      >
                        ✨
                      </motion.span>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
        
        <div className="f4-reading-footer">
          <button 
            className="f4-nav-btn" 
            disabled={currentStep === 0}
            onClick={() => goToStep(currentStep - 1)}
          >
            <ArrowLeft size={18} /> Atrás
          </button>
          
          {currentStep < totalSteps - 1 ? (
            <button 
              className="f4-nav-btn primary" 
              style={{ backgroundColor: moduleColor, opacity: canGoNext ? 1 : 0.5 }}
              disabled={!canGoNext}
              onClick={() => goToStep(currentStep + 1)}
            >
              Siguiente <ArrowRight size={18} />
            </button>
          ) : (
            <button 
              className="f4-reading-close-btn"
              style={{ background: `linear-gradient(135deg, ${moduleColor}cc, ${moduleColor})` }}
              onClick={onClose}
            >
              ¡Entendido, empezar!
            </button>
          )}
        </div>
      </motion.div>
    </div>
  );
};
