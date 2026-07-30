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

const MAX_THEORY_CHARACTERS_PER_SLIDE = 560;
const MAX_EXAMPLE_WEIGHT_PER_SLIDE = 780;

const formatFase4Content = (text: string) => {
  const normalizedText = text
    .replace(/\$\s*ightarrow\$/g, '→')
    .replace(/\$\\\\rightarrow\$/g, '→');

  return formatContent(normalizedText);
};

const groupTheoryParagraphs = (paragraphs: string[]) => {
  const nonEmptyParagraphs = paragraphs.filter(Boolean);
  const [intro, ...procedure] = nonEmptyParagraphs;
  const groups: string[][] = [];
  let currentGroup: string[] = [];
  let currentLength = 0;

  procedure.forEach((paragraph) => {
    const nextLength = currentLength + paragraph.length;
    if (currentGroup.length > 0 && nextLength > MAX_THEORY_CHARACTERS_PER_SLIDE) {
      groups.push(currentGroup);
      currentGroup = [paragraph];
      currentLength = paragraph.length;
      return;
    }

    currentGroup.push(paragraph);
    currentLength = nextLength;
  });

  if (currentGroup.length > 0) groups.push(currentGroup);

  return { intro, groups };
};

const getPlainTextWeight = (text = '') => (
  text
    .replace(/<svg[\s\S]*?<\/svg>/g, '')
    .replace(/<[^>]*>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .length
);

const getExampleQuestionWeight = (text = '') => {
  const hasSvg = /<svg[\s\S]*?<\/svg>/.test(text);
  return getPlainTextWeight(text) + (hasSvg ? 260 : 110);
};

const getExampleStepWeight = (step: any) => {
  const optionWeight = Array.isArray(step?.opciones)
    ? step.opciones.reduce((total: number, option: any) => {
      const optionText = typeof option === 'string' ? option : option?.texto || '';
      return total + getPlainTextWeight(optionText) + 28;
    }, 0)
    : 0;

  return getPlainTextWeight(step?.texto || '') + optionWeight + 55;
};

const buildCompactExampleSlides = (
  example: any,
  exampleIndex: number,
  totalExamples: number
) => {
  const steps = Array.isArray(example?.pasos) ? example.pasos : [];
  const chunks: Array<{
    type: string;
    data: {
      example: any;
      exampleIndex: number;
      totalExamples: number;
      includePrompt: boolean;
      pasos: any[];
      partIndex: number;
      totalParts: number;
      isFinalPart: boolean;
    };
  }> = [];

  if (steps.length === 0) return chunks;

  let includePrompt = true;
  let currentSteps: any[] = [];
  let currentWeight = getExampleQuestionWeight(example.enunciado || '');

  const flushChunk = () => {
    if (currentSteps.length === 0) return;
    chunks.push({
      type: 'example-compact',
      data: {
        example,
        exampleIndex,
        totalExamples,
        includePrompt,
        pasos: currentSteps,
        partIndex: 0,
        totalParts: 0,
        isFinalPart: false
      }
    });
    includePrompt = false;
    currentSteps = [];
    currentWeight = 0;
  };

  steps.forEach((step) => {
    const stepWeight = getExampleStepWeight(step);
    if (currentSteps.length > 0 && currentWeight + stepWeight > MAX_EXAMPLE_WEIGHT_PER_SLIDE) {
      flushChunk();
    }

    currentSteps.push(step);
    currentWeight += stepWeight;
  });

  flushChunk();

  return chunks.map((chunk, index) => ({
    ...chunk,
    data: {
      ...chunk.data,
      partIndex: index,
      totalParts: chunks.length,
      isFinalPart: index === chunks.length - 1
    }
  }));
};

type TheoryIllustrationKind = 'stack' | 'positions' | 'division' | 'ladder';

interface TheoryIllustrationConfig {
  kind: TheoryIllustrationKind;
  label: string;
  note: string;
  rows?: string[];
  steps?: string[];
  units?: string[];
  direction?: 'down' | 'up' | 'mixed';
}

const THEORY_ILLUSTRATIONS: Record<string, TheoryIllustrationConfig> = {
  '1-1': {
    kind: 'stack',
    label: 'Comas en la misma columna',
    rows: ['12,40', '+ 3,05', '15,45'],
    note: 'La coma baja por una linea vertical.'
  },
  '1-2': {
    kind: 'stack',
    label: 'Ceros auxiliares',
    rows: ['10,00', '- 3,45', ' 6,55'],
    note: 'Los ceros llenan casilleros antes de restar.'
  },
  '1-3': {
    kind: 'stack',
    label: 'Dinero ordenado',
    rows: ['50,00', '-18,75', '31,25'],
    note: 'Primero se ordena el gasto, despues el vuelto.'
  },
  '2-1': {
    kind: 'positions',
    label: 'Una posicion decimal',
    steps: ['42 x 3', '126', '12,6'],
    note: 'El producto recupera 1 lugar decimal.'
  },
  '2-2': {
    kind: 'positions',
    label: 'Dos posiciones decimales',
    steps: ['215 x 4', '860', '8,60'],
    note: 'Se cuentan 2 lugares desde la derecha.'
  },
  '2-3': {
    kind: 'positions',
    label: 'Suma de posiciones',
    steps: ['15 x 3', '45', '0,45'],
    note: '1 lugar + 1 lugar = 2 lugares decimales.'
  },
  '3-1': {
    kind: 'division',
    label: 'La coma cruza al cociente',
    steps: ['8,4 / 2', '4,2'],
    note: 'Al bajar decimales, la coma aparece arriba.'
  },
  '3-2': {
    kind: 'division',
    label: 'Hasta las centesimas',
    steps: ['12,48 / 4', '3,12'],
    note: 'Se sigue dividiendo cifra por cifra.'
  },
  '3-3': {
    kind: 'division',
    label: 'Divisor entero y contexto',
    steps: ['6 / 1,5', '60 / 15', '4'],
    note: 'Primero mueve la coma; luego decide segun el problema.'
  },
  '4-1': {
    kind: 'ladder',
    label: 'Bajar aumenta la cantidad',
    units: ['km', 'm', 'cm', 'mm'],
    direction: 'down',
    note: 'Cada escalon hacia abajo multiplica por 10.'
  },
  '4-2': {
    kind: 'ladder',
    label: 'Subir reduce la cantidad',
    units: ['mm', 'cm', 'm', 'km'],
    direction: 'up',
    note: 'Cada escalon hacia arriba divide entre 10.'
  },
  '4-3': {
    kind: 'ladder',
    label: 'Una unidad comun',
    units: ['L', 'mL', 'g', 'kg'],
    direction: 'mixed',
    note: 'Convierte primero; despues compara o calcula.'
  }
};

const Fase4TheoryIllustration: React.FC<{
  moduloId: number;
  nivelId: number;
  moduleColor: string;
}> = ({ moduloId, nivelId, moduleColor }) => {
  const config = THEORY_ILLUSTRATIONS[`${moduloId}-${nivelId}`];
  if (!config) return null;

  return (
    <div
      className={`f4-theory-illustration f4-theory-illustration-${config.kind}`}
      style={{ ['--f4-illustration-color' as string]: moduleColor }}
      aria-hidden="true"
    >
      <div className="f4-illustration-label">{config.label}</div>

      {config.kind === 'stack' && (
        <div className="f4-illustration-stack">
          {config.rows?.map((row, idx) => (
            <div key={`${row}-${idx}`} className={`f4-stack-row ${idx === (config.rows?.length || 0) - 1 ? 'result' : ''}`}>
              {row}
            </div>
          ))}
          <div className="f4-stack-comma-guide" />
        </div>
      )}

      {config.kind === 'positions' && (
        <div className="f4-position-flow">
          {config.steps?.map((step, idx) => (
            <React.Fragment key={`${step}-${idx}`}>
              <span className={idx === (config.steps?.length || 0) - 1 ? 'final' : ''}>{step}</span>
              {idx < (config.steps?.length || 0) - 1 && <span className="f4-flow-arrow">&rarr;</span>}
            </React.Fragment>
          ))}
        </div>
      )}

      {config.kind === 'division' && (
        <div className="f4-division-flow">
          {config.steps?.map((step, idx) => (
            <React.Fragment key={`${step}-${idx}`}>
              <span className={idx === (config.steps?.length || 0) - 1 ? 'final' : ''}>{step}</span>
              {idx < (config.steps?.length || 0) - 1 && <span className="f4-flow-arrow">&rarr;</span>}
            </React.Fragment>
          ))}
        </div>
      )}

      {config.kind === 'ladder' && (
        <div className={`f4-unit-ladder ${config.direction || 'down'}`}>
          {config.units?.map((unit, idx) => (
            <span key={`${unit}-${idx}`} className="f4-unit-step">{unit}</span>
          ))}
        </div>
      )}

      <div className="f4-illustration-note">{config.note}</div>
    </div>
  );
};

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
    const s: { type: string; data: any; centered?: boolean }[] = [];
    const dictionaryEntries = Object.entries(readingData.diccionario || {});
    const { intro, groups } = groupTheoryParagraphs(readingData.parrafos);

    if (intro) {
      s.push({ type: 'intro', data: [intro], centered: true });
    }
    groups.forEach((group) => s.push({ type: 'intro', data: group }));
    if (!intro && groups.length === 0) {
      s.push({ type: 'intro', data: null });
    }

    if (dictionaryEntries.length > 0) {
      const chunks = chunkArray(dictionaryEntries, 4);
      chunks.forEach(c => s.push({ type: 'dictionary', data: c }));
    }
    
    if (readingData.ejemplos && readingData.ejemplos.length > 0) {
      const totalExamples = readingData.ejemplos.length;
      readingData.ejemplos.forEach((example, exampleIndex) => {
        if (example.pasos?.length) {
          const compactSlides = buildCompactExampleSlides(example, exampleIndex, totalExamples);
          compactSlides.forEach((compactSlide) => s.push(compactSlide));
          return;
        }

        s.push({ type: 'examples', data: [example], exampleIndex, totalExamples } as any);
      });
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
    const currentSlideData = slides[currentStep] as any;

    if (currentType === 'example-compact') {
      return {
        label: `Ejemplo ${currentSlideData.data.exampleIndex + 1} de ${currentSlideData.data.totalExamples}`
      };
    }

    if (currentType === 'examples' && currentSlideData.exampleIndex !== undefined) {
      return {
        label: `Ejemplo ${currentSlideData.exampleIndex + 1} de ${currentSlideData.totalExamples}`
      };
    }
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
                className={`f4-flashcard-content ${currentSlide.centered ? 'centered-theory' : ''}`}
              >
                {currentSlide.centered && (
                  <Fase4TheoryIllustration
                    moduloId={readingData.modulo_id}
                    nivelId={readingData.nivel_id}
                    moduleColor={moduleColor}
                  />
                )}

                {(currentSlide.data || readingData.parrafos).map((p: string, idx: number) => (
                  <p key={idx} className="f4-reading-p" dangerouslySetInnerHTML={{ __html: formatFase4Content(p) }} />
                ))}

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
                        <div className="f4-dict-term" style={{ color: moduleColor }} dangerouslySetInnerHTML={{ __html: formatFase4Content(termino) }} />
                        <div className="f4-dict-def" dangerouslySetInnerHTML={{ __html: formatFase4Content(definicion) }} />
                      </div>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}

            {currentSlide?.type === 'example-compact' && (
              <motion.div
                key={`example-compact-${currentStep}`}
                custom={direction}
                variants={variants}
                initial="enter"
                animate="center"
                exit="exit"
                transition={{ duration: 0.3 }}
                className="f4-flashcard-content"
              >
                <div className="f4-reading-examples compact-example">
                  <div className={`f4-example-box compact-example-card ${currentSlide.data.includePrompt ? '' : 'without-prompt'}`}>
                    {currentSlide.data.includePrompt && (
                      <div
                        className="f4-ex-q f4-ex-q-compact"
                        dangerouslySetInnerHTML={{ __html: formatFase4Content(currentSlide.data.example.enunciado) }}
                      />
                    )}

                    <div className="f4-compact-example-steps">
                      {currentSlide.data.pasos.map((paso: any) => {
                        const isLastStep = currentSlide.data.isFinalPart && paso === currentSlide.data.pasos[currentSlide.data.pasos.length - 1];
                        return (
                          <div
                            key={paso.orden}
                            className={`f4-ex-step compact-step ${isLastStep ? 'result-step' : ''}`}
                          >
                            <span className="f4-ex-step-num">{paso.orden}</span>
                            <span className="f4-compact-step-body">
                              <span dangerouslySetInnerHTML={{ __html: formatFase4Content(paso.texto) }} />
                              {Array.isArray(paso.opciones) && paso.opciones.length > 0 && (
                                <span className="f4-step-options">
                                  {paso.opciones.map((option: any, optionIndex: number) => {
                                    const optionText = typeof option === 'string' ? option : option?.texto || '';
                                    const optionId = typeof option === 'string' ? String.fromCharCode(65 + optionIndex) : option?.id || String.fromCharCode(65 + optionIndex);
                                    return (
                                      <span key={`${paso.orden}-${optionId}`} className="f4-step-option">
                                        <strong>{optionId}</strong>
                                        <span dangerouslySetInnerHTML={{ __html: formatFase4Content(optionText) }} />
                                      </span>
                                    );
                                  })}
                                </span>
                              )}
                            </span>
                          </div>
                        );
                      })}
                    </div>

                    {currentSlide.data.isFinalPart && (
                      <div className="f4-example-solved-mark" aria-label="Ejemplo resuelto">
                        <CheckCircle size={16} />
                        <span>Resuelto</span>
                      </div>
                    )}
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
                    {currentSlide.data.map((ex: any, idx: number) => (
                      <div key={idx} className="f4-example-box">
                        <div className="f4-ex-q" dangerouslySetInnerHTML={{ __html: formatFase4Content(ex.enunciado) }} />
                        {ex.pasos ? (
                          <div className="f4-ex-steps">
                            {ex.pasos.map((paso: any) => (
                              <div key={paso.orden} className="f4-ex-step">
                                <span className="f4-ex-step-num">{paso.orden}</span>
                                <span dangerouslySetInnerHTML={{ __html: formatFase4Content(paso.texto) }} />
                              </div>
                            ))}
                          </div>
                        ) : (
                           <div className="f4-ex-legacy">→ <span style={{ color: moduleColor }} dangerouslySetInnerHTML={{ __html: formatFase4Content(ex.respuesta) }} /></div>
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
