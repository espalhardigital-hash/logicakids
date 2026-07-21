import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';
import type { Fase4Pregunta, Fase4AnswerResult } from './Fase4Types';
import { submitFase4Answer } from './Fase4Service';
import { CustomKeyboard } from '../common/CustomKeyboard';
import { Fase4VisualizerEngine } from './Fase4VisualizerEngine';
import './Fase4Styles.css';

const checkPositionsMatch = (current: any, target: any, tolerance: number): boolean => {
  if (!Array.isArray(current) || !Array.isArray(target)) return false;
  if (current.length !== target.length) return false;
  const matchedIndices = new Set<number>();
  for (const tgt of target) {
    let found = false;
    for (let i = 0; i < current.length; i++) {
      if (matchedIndices.has(i)) continue;
      const curr = current[i];
      if (curr.type === tgt.type) {
        const dx = Math.abs((curr.left ?? 0) - (tgt.left ?? 0));
        const dy = Math.abs((curr.top ?? 0) - (tgt.top ?? 0));
        if (dx <= tolerance && dy <= tolerance) {
          matchedIndices.add(i);
          found = true;
          break;
        }
      }
    }
    if (!found) return false;
  }
  return true;
};

interface Props {
  pregunta: Fase4Pregunta;
  moduleColor: string;
  onClose: (result?: Fase4AnswerResult) => void;
  lastCorrectAnswer?: string;
  lastQuestionEnunciado?: string;
  lastWrongAnswer?: string;
  moduloId: number;
  nivelId: number;
  selectedPolygonIds?: number[];
}

export const Fase4MirrorModal: React.FC<Props> = ({
  pregunta,
  moduleColor,
  onClose,
  lastCorrectAnswer,
  lastWrongAnswer,
  moduloId,
  nivelId,
  selectedPolygonIds,
}) => {
  // Solo mostrar explicación visual si es polígono Y NO es una pregunta espejo.
  // La explicación se abre con el botón "¿Por qué?" tras respuesta correcta.
  // Las preguntas espejo de polígono deben pasar al flujo interactivo de abajo.
  const isPolygonExplanation = pregunta.datos_numericos?.tipo_visual === 'non_homogeneous_polygon'
    && !pregunta.datos_numericos?.es_espejo;

  if (isPolygonExplanation) {
    const sectors = pregunta.datos_numericos?.sectors || [];
    const viewBox = pregunta.datos_numericos?.viewBox || "0 0 100 100";
    const targetText = pregunta.datos_numericos?.target_fraction_text || pregunta.respuesta_correcta || "";
    
    const activeIds = selectedPolygonIds && selectedPolygonIds.length > 0
      ? selectedPolygonIds
      : sectors.map(s => s.id);

    const isPercentage = targetText.includes('%');
    let textoExplicativo = "";
    if (isPercentage) {
      textoExplicativo = `Al consolidar las piezas coloreadas, podemos ver que cubren exactamente el ${targetText} de la superficie total de la figura.`;
    } else {
      textoExplicativo = `Al consolidar las piezas coloreadas, podemos ver que representan exactamente la fracción ${targetText} de la figura entera.`;
    }

    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="f4-feedback-overlay mirror-modal-overlay"
        style={{ zIndex: 1100 }}
      >
        <motion.div
          initial={{ scale: 0.9, y: 20 }}
          animate={{ scale: 1, y: 0 }}
          className="f4-mirror-modal-card glass-card"
          style={{
            maxWidth: '850px',
            width: '95%',
            display: 'flex',
            flexDirection: 'column',
            gap: '20px',
            padding: '32px',
            border: `2px solid ${moduleColor}40`,
            position: 'relative',
          }}
        >
          <button
            className="absolute top-4 right-4 p-2 text-white/40 hover:text-white transition-colors"
            onClick={() => onClose()}
          >
            <X size={24} />
          </button>

          <div className="flex flex-col items-center text-center">
            <div
              className="px-4 py-1.5 rounded-full text-xs font-black uppercase tracking-widest mb-2"
              style={{ background: `${moduleColor}30`, color: moduleColor }}
            >
              Explicación Visual
            </div>
            <h2 className="text-xl md:text-2xl font-black text-white mb-2 leading-tight">
              ¿Por qué es {targetText}?
            </h2>
            <p className="text-sm text-slate-400 max-w-lg mb-6">
              Observa cómo las piezas que seleccionaste se pueden agrupar o consolidar para formar la fracción solicitada de manera exacta.
            </p>
          </div>

          {/* Figuras Lado a Lado */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center justify-center w-full my-2">
            {/* 1. Figura Original */}
            <div className="flex flex-col items-center gap-3">
              <span className="text-xs font-bold text-slate-400 tracking-wider uppercase">Tus Piezas Seleccionadas</span>
              <div className="p-4 bg-slate-950/40 border border-white/5 rounded-2xl flex items-center justify-center min-h-[220px] w-full">
                <svg viewBox={viewBox} className="w-48 h-48 filter drop-shadow-md">
                  {sectors.map((sector) => {
                    const isSelected = activeIds.includes(sector.id);
                    return (
                      <polygon
                        key={sector.id}
                        points={sector.points}
                        style={{
                          fill: isSelected ? moduleColor : '#27272a',
                        }}
                        className="stroke-white stroke-[1.5]"
                      />
                    );
                  })}
                </svg>
              </div>
            </div>

            {/* 2. Figura Simplificada (Bordes desvanecidos) */}
            <div className="flex flex-col items-center gap-3">
              <span className="text-xs font-bold text-slate-400 tracking-wider uppercase">Vista Simplificada</span>
              <div className="p-4 bg-slate-950/40 border border-white/5 rounded-2xl flex items-center justify-center min-h-[220px] w-full">
                <svg viewBox={viewBox} className="w-48 h-48 filter drop-shadow-md">
                  {sectors.map((sector) => {
                    const isSelected = activeIds.includes(sector.id);
                    return (
                      <polygon
                        key={sector.id}
                        points={sector.points}
                        style={{
                          fill: isSelected ? moduleColor : '#27272a',
                          stroke: isSelected ? moduleColor : '#ffffff',
                          strokeWidth: 1.5
                        }}
                        className="transition-all duration-300"
                      />
                    );
                  })}
                </svg>
              </div>
            </div>
          </div>

          <div className="bg-white/5 border border-white/5 rounded-2xl p-4 text-center mt-2">
            <p className="text-slate-200 text-sm md:text-base font-medium leading-relaxed">
              {textoExplicativo}
            </p>
          </div>

          <button
            onClick={() => onClose()}
            className="w-full py-4 rounded-2xl bg-emerald-500 hover:bg-emerald-600 text-white font-black text-lg transition-all duration-150 cursor-pointer shadow-lg mt-4 active:scale-[0.98]"
          >
            Entendido
          </button>
        </motion.div>
      </motion.div>
    );
  }

  const [respuestaNum, setRespuestaNum] = useState('');
  const [respuestaDen, setRespuestaDen] = useState('');
  const [activeInputField, setActiveInputField] = useState<'num' | 'den'>('num');
  const [interactiveSelectedCount, setInteractiveSelectedCount] = useState<number>(0);
  const [visualState, setVisualState] = useState<any>(null);
  const [localSelectedPolygonIds, setLocalSelectedPolygonIds] = useState<number[]>([]);
  const [selectedAltId, setSelectedAltId] = useState<number | null>(null);

  const [feedback, setFeedback] = useState<{
    visible: boolean;
    esCorrecta: boolean;
    resultado?: Fase4AnswerResult;
  }>({ visible: false, esCorrecta: false });
  const [shaking, setShaking] = useState(false);

  const isFractionAnswer = (pregunta.respuesta_correcta ?? '').includes('/');
  const showFractionInput = isFractionAnswer;

  useEffect(() => {
    setRespuestaNum('');
    setRespuestaDen('');
    setActiveInputField('num');
    setFeedback({ visible: false, esCorrecta: false });
    setShaking(false);
    setInteractiveSelectedCount(0);
    setVisualState(null);
    setLocalSelectedPolygonIds(selectedPolygonIds || []);
    setSelectedAltId(null);
  }, [pregunta.id, selectedPolygonIds]);

  const handleNumberPress = (num: string) => {
    if (feedback.visible) return;
    if (showFractionInput) {
      if (activeInputField === 'num') {
        setRespuestaNum(prev => prev.length < 5 ? prev + num : prev);
      } else {
        setRespuestaDen(prev => prev.length < 5 ? prev + num : prev);
      }
    } else {
      setRespuestaNum(prev => prev.length < 10 ? prev + num : prev);
    }
  };

  const handleBackspace = () => {
    if (feedback.visible) return;
    if (showFractionInput) {
      if (activeInputField === 'num') {
        setRespuestaNum(prev => prev.slice(0, -1));
      } else {
        setRespuestaDen(prev => prev.slice(0, -1));
      }
    } else {
      setRespuestaNum(prev => prev.slice(0, -1));
    }
  };

  const handleSubmit = async (customAnswer?: string) => {
    let finalAnswer = '';
    let alternativaId: number | undefined = undefined;
    
    const isInteractivePizza = pregunta.datos_numericos?.tipo_visual === 'pizza' && !!pregunta.datos_numericos?.es_interactivo;
    const isInteractiveShapes = pregunta.datos_numericos?.tipo_visual === 'shapes';
    const isInteractivePolygon = pregunta.datos_numericos?.tipo_visual === 'non_homogeneous_polygon';

    if (pregunta.tipo_pregunta === 'multiple_opcion' && pregunta.alternativas) {
      if (selectedAltId !== null) {
        alternativaId = selectedAltId;
        const match = pregunta.alternativas.find(alt => alt.id === selectedAltId);
        if (match) finalAnswer = match.texto;
      }
    } else if (isInteractivePolygon) {
      finalAnswer = localSelectedPolygonIds.join(',');
    } else if (isInteractiveShapes) {
      try {
        const targetState = JSON.parse(pregunta.respuesta_correcta || '[]');
        const tolerance = 15;
        const isMatch = checkPositionsMatch(visualState, targetState, tolerance);
        finalAnswer = isMatch ? pregunta.respuesta_correcta : JSON.stringify(visualState);
      } catch (e) {
        finalAnswer = JSON.stringify(visualState || '');
      }
    } else if (isInteractivePizza) {
      const numVal = respuestaNum.trim();
      const denVal = respuestaDen.trim();
      if (numVal && denVal) {
        finalAnswer = `${numVal}/${denVal}`;
      } else {
        finalAnswer = `${interactiveSelectedCount}/${pregunta.datos_numericos?.cortes || 8}`;
      }
    } else if (showFractionInput) {
      const numVal = respuestaNum.trim();
      const denVal = respuestaDen.trim();
      if (numVal && denVal) {
        finalAnswer = `${numVal}/${denVal}`;
      } else {
        finalAnswer = numVal;
      }
    } else {
      finalAnswer = respuestaNum;
    }

    if (customAnswer !== undefined) {
      finalAnswer = customAnswer;
    }

    if ((pregunta.tipo_pregunta !== 'multiple_opcion' && !finalAnswer.trim()) || feedback.visible) return;
    if (pregunta.tipo_pregunta === 'multiple_opcion' && selectedAltId === null && customAnswer === undefined) return;

    try {
      const result = await submitFase4Answer({
        modulo_id: moduloId,
        nivel_id: nivelId,
        pregunta_id: pregunta.id,
        respuesta_dada: finalAnswer.trim() || undefined,
        alternativa_id: alternativaId,
        tiempo_respuesta_segundos: 0,
      });

      if (result.es_correcta) {
        setFeedback({ visible: true, esCorrecta: true, resultado: result });
        setTimeout(() => onClose(result), 1500);
      } else {
        setShaking(true);
        setTimeout(() => setShaking(false), 450);
        setFeedback({ visible: true, esCorrecta: false, resultado: result });
        if (result.fase_completada || result.bloque_completado) {
          setTimeout(() => onClose(result), 1500);
        }
      }
    } catch (e) {
      console.error('[Fase4MirrorModal] Error al enviar respuesta:', e);
    }
  };

  useEffect(() => {
    if (feedback.visible && !feedback.esCorrecta) {
      const timer = setTimeout(() => {
        onClose(feedback.resultado);
      }, 2000);
      return () => clearTimeout(timer);
    }
  }, [feedback, onClose]);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="f4-feedback-overlay mirror-modal-overlay"
      style={{ zIndex: 1100 }}
    >
      <motion.div
        initial={{ scale: 0.9, y: 20 }}
        animate={{ scale: 1, y: 0 }}
        className="f4-mirror-modal-card glass-card"
        style={{
          maxWidth: '900px',
          width: '95%',
          display: 'flex',
          flexDirection: 'column',
          gap: '16px',
          padding: '24px',
          border: `2px solid ${moduleColor}40`,
          position: 'relative',
        }}
      >
        <button
          className="absolute top-4 right-4 p-2 text-white/40 hover:text-white transition-colors"
          onClick={() => onClose()}
        >
          <X size={24} />
        </button>

        {/* Header: patrón estándar Fase 2 — ¡SEGUNDA OPORTUNIDAD! */}
        <div className="flex items-center gap-4 mb-1">
          <div
            className="px-3 py-1 rounded-full text-xs font-black uppercase tracking-widest"
            style={{ background: `${moduleColor}30`, color: moduleColor }}
          >
            ¡SEGUNDA OPORTUNIDAD!
          </div>
          <div className="text-white/40 text-xs font-bold">
            Vamos a repasar juntos el concepto
          </div>
        </div>

        {/* Repaso minimalista en barra horizontal compacta sin el enunciado de la pregunta anterior */}
        {lastCorrectAnswer && (
          <div className="bg-green-500/10 border border-green-500/20 px-4 py-2.5 rounded-2xl mb-1 flex items-center justify-between text-xs sm:text-sm flex-wrap gap-2">
            <div className="flex items-center gap-2">
              <span className="text-green-500 font-black tracking-wider text-[10px] uppercase bg-green-500/15 px-2 py-0.5 rounded">REPASO</span>
              {lastWrongAnswer && (
                <span className="text-white/50">
                  Respondiste: <span className="text-red-400 font-bold line-through ml-1">{lastWrongAnswer}</span>
                </span>
              )}
            </div>
            <span className="text-white">
              La respuesta correcta era: <strong className="text-green-400 font-bold text-sm sm:text-base ml-1">{lastCorrectAnswer}</strong>
            </span>
          </div>
        )}

        {/* Layout: enunciado + teclado numérico (Adaptativo según tipo de pregunta) */}
        {(() => {
          const isInteractiveVisual = pregunta.datos_numericos?.tipo_visual === 'shapes' || pregunta.datos_numericos?.tipo_visual === 'non_homogeneous_polygon';
          const isMultipleChoice = pregunta.tipo_pregunta === 'multiple_opcion' && pregunta.alternativas;

          if (isInteractiveVisual) {
            return (
              <div className="flex flex-col items-center justify-center w-full">
                <motion.div
                  animate={shaking ? { x: [-8, 8, -6, 6, -4, 4, 0] } : {}}
                  className="bg-white/5 border border-white/10 rounded-[2rem] p-6 w-full max-w-[620px] flex flex-col items-center"
                >
                  <h2 
                    className="text-center text-lg md:text-xl font-bold text-white mb-6 leading-tight max-w-[90%]"
                    dangerouslySetInnerHTML={{ __html: (pregunta.enunciado || '').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }}
                  />
                  
                  <div className="flex justify-center mb-6 w-full max-h-[320px] md:max-h-[380px] overflow-hidden origin-top scale-100">
                    <Fase4VisualizerEngine
                      pregunta={pregunta}
                      moduleColor={moduleColor}
                      moduloId={moduloId}
                      nivelId={nivelId}
                      interactive={!!pregunta.datos_numericos?.es_interactivo}
                      respuestaNum={respuestaNum}
                      respuestaDen={respuestaDen}
                      setRespuestaNum={setRespuestaNum}
                      setRespuestaDen={setRespuestaDen}
                      interactiveSelectedCount={interactiveSelectedCount}
                      setInteractiveSelectedCount={setInteractiveSelectedCount}
                      setVisualState={setVisualState}
                      selectedPolygonIds={localSelectedPolygonIds}
                      setSelectedPolygonIds={setLocalSelectedPolygonIds}
                      visualState={visualState}
                    />
                  </div>

                  {/* Botón de Confirmación para interactivas */}
                  <button
                    onClick={() => handleSubmit()}
                    className="group relative flex items-center justify-center gap-4 w-full max-w-[280px] py-4 px-6 text-white font-sans font-black text-xl rounded-2xl border-2 border-white/10 transform active:scale-[0.95] transition-all duration-150 cursor-pointer overflow-hidden mt-4"
                    style={{
                      background: feedback.visible 
                        ? (feedback.esCorrecta ? '#10B981' : '#EF4444') 
                        : `linear-gradient(135deg, ${moduleColor}cc, ${moduleColor})`,
                      boxShadow: feedback.visible 
                        ? (feedback.esCorrecta ? '0 8px 20px rgba(16, 185, 129, 0.3)' : '0 8px 20px rgba(239, 68, 68, 0.3)') 
                        : `0 8px 20px rgba(168, 85, 247, 0.3)`
                    }}
                  >
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 ease-out" />
                    <span>{feedback.visible ? (feedback.esCorrecta ? 'Continuar →' : 'Activando repaso...') : 'CONFIRMAR'}</span>
                    <div className="flex items-center justify-center w-8 h-8 rounded-full border-2 border-white bg-transparent flex-shrink-0">
                      <span className="text-white text-base font-black">
                        {feedback.visible ? (feedback.esCorrecta ? '→' : '...') : '✓'}
                      </span>
                    </div>
                  </button>
                </motion.div>
              </div>
            );
          }

          if (isMultipleChoice) {
            const isVisualMultipleChoice = pregunta.alternativas!.some(alt => alt.texto.includes('<svg'));
            return (
              <div className="flex flex-col items-center justify-center w-full">
                <motion.div
                  animate={shaking ? { x: [-8, 8, -6, 6, -4, 4, 0] } : {}}
                  className="bg-white/5 border border-white/10 rounded-[2rem] p-6 w-full max-w-[620px] flex flex-col items-center"
                >
                  <h2 
                    className="text-center text-lg md:text-xl font-bold text-white mb-6 leading-tight max-w-[90%]"
                    dangerouslySetInnerHTML={{ __html: (pregunta.enunciado || '').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }}
                  />

                  <div className={isVisualMultipleChoice ? "grid grid-cols-2 gap-4 w-full mb-6" : "w-full space-y-4 mb-6"}>
                    {pregunta.alternativas!.map(alt => (
                      <button
                        key={alt.id}
                        onClick={() => setSelectedAltId(alt.id)}
                        disabled={feedback.visible}
                        className={`w-full py-5 px-6 bg-white/5 hover:bg-white/10 border rounded-2xl font-black text-xl text-white transition-all cursor-pointer flex items-center justify-center ${
                          isVisualMultipleChoice ? 'text-center' : 'text-left'
                        } ${
                          selectedAltId === alt.id 
                            ? 'border-purple-500 bg-purple-500/20 shadow-[0_0_15px_rgba(168,85,247,0.3)]' 
                            : 'border-white/10 hover:border-purple-500/30 active:scale-[0.98]'
                        }`}
                        dangerouslySetInnerHTML={{ __html: alt.texto }}
                      />
                    ))}
                  </div>

                  {/* Botón de Confirmación para opción múltiple */}
                  <button
                    onClick={() => handleSubmit()}
                    disabled={!feedback.visible && selectedAltId === null}
                    className="group relative flex items-center justify-center gap-4 w-full max-w-[280px] py-4 px-6 text-white font-sans font-black text-xl rounded-2xl border-2 border-white/10 transform active:scale-[0.95] transition-all duration-150 cursor-pointer overflow-hidden disabled:opacity-50 disabled:cursor-not-allowed"
                    style={{
                      background: feedback.visible 
                        ? (feedback.esCorrecta ? '#10B981' : '#EF4444') 
                        : `linear-gradient(135deg, ${moduleColor}cc, ${moduleColor})`,
                      boxShadow: feedback.visible 
                        ? (feedback.esCorrecta ? '0 8px 20px rgba(16, 185, 129, 0.3)' : '0 8px 20px rgba(239, 68, 68, 0.3)') 
                        : (selectedAltId !== null ? `0 8px 20px rgba(168, 85, 247, 0.3)` : 'none')
                    }}
                  >
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 ease-out" />
                    <span>{feedback.visible ? (feedback.esCorrecta ? 'Continuar →' : 'Activando repaso...') : 'CONFIRMAR'}</span>
                    <div className="flex items-center justify-center w-8 h-8 rounded-full border-2 border-white bg-transparent flex-shrink-0">
                      <span className="text-white text-base font-black">
                        {feedback.visible ? (feedback.esCorrecta ? '→' : '...') : '✓'}
                      </span>
                    </div>
                  </button>
                </motion.div>
              </div>
            );
          }

          // Modo Estándar: Layout de Dos Columnas (Keypad e Inputs numéricos)
          return (
            <div className="flex flex-col md:flex-row gap-6 items-center w-full">
              <div className="flex-1 w-full">
                <motion.div
                  animate={shaking ? { x: [-8, 8, -6, 6, -4, 4, 0] } : {}}
                  className="bg-white/5 border border-white/10 rounded-[2rem] p-6"
                >
                  <h2 
                    className="text-center text-lg md:text-xl font-bold text-white mb-6 leading-tight max-w-[90%] mx-auto"
                    dangerouslySetInnerHTML={{ __html: (pregunta.enunciado || '').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') }}
                  />

                  {pregunta.datos_numericos?.tipo_visual && (
                    <div className="flex justify-center mb-6 max-h-[220px] overflow-hidden origin-top scale-[0.85]">
                      <Fase4VisualizerEngine
                        pregunta={pregunta}
                        moduleColor={moduleColor}
                        moduloId={moduloId}
                        nivelId={nivelId}
                        interactive={!!pregunta.datos_numericos?.es_interactivo}
                        respuestaNum={respuestaNum}
                        respuestaDen={respuestaDen}
                        setRespuestaNum={setRespuestaNum}
                        setRespuestaDen={setRespuestaDen}
                        interactiveSelectedCount={interactiveSelectedCount}
                        setInteractiveSelectedCount={setInteractiveSelectedCount}
                        setVisualState={setVisualState}
                        selectedPolygonIds={localSelectedPolygonIds}
                        setSelectedPolygonIds={setLocalSelectedPolygonIds}
                        visualState={visualState}
                      />
                    </div>
                  )}

                  {showFractionInput ? (
                    <div className="f4-fraction-input-box justify-center my-4 scale-110 origin-center">
                      <div 
                        className={`f4-fraction-field-wrap num ${activeInputField === 'num' ? 'active' : ''}`}
                        onClick={() => !feedback.visible && setActiveInputField('num')}
                      >
                        <span className="f4-fraction-label-indicator">NUMERADOR</span>
                        <div className="f4-fraction-digit-box text-3xl md:text-4xl">
                          {feedback.visible
                            ? feedback.esCorrecta
                              ? (feedback.resultado?.respuesta_correcta?.split('/')?.[0] || respuestaNum)
                              : respuestaNum || '?'
                            : respuestaNum || '?'}
                        </div>
                      </div>
                      <div className="f4-fraction-line-divider" />
                      <div 
                        className={`f4-fraction-field-wrap den ${activeInputField === 'den' ? 'active' : ''}`}
                        onClick={() => !feedback.visible && setActiveInputField('den')}
                      >
                        <span className="f4-fraction-label-indicator">DENOMINADOR</span>
                        <div className="f4-fraction-digit-box text-3xl md:text-4xl">
                          {feedback.visible
                            ? feedback.esCorrecta
                              ? (feedback.resultado?.respuesta_correcta?.split('/')?.[1] || respuestaDen)
                              : respuestaDen || '?'
                            : respuestaDen || '?'}
                        </div>
                      </div>
                      {feedback.visible && (
                        <div className="f4-input-status-elements ml-4">
                          {feedback.esCorrecta ? (
                            <div className="f4-status-badge correct">
                              <svg className="f4-status-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round">
                                <polyline points="20 6 9 17 4 12" />
                              </svg>
                            </div>
                          ) : (
                            <>
                              <span className="f4-era-pill">
                                Era: {feedback.resultado?.respuesta_correcta}
                              </span>
                              <div className="f4-status-badge incorrect">
                                <svg className="f4-status-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round">
                                  <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
                                </svg>
                              </div>
                            </>
                          )}
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="f4-numeric-input-wrap mb-2">
                      <div
                        className={`f4-custom-input-box ${
                          feedback.visible
                            ? feedback.esCorrecta
                              ? 'correct'
                              : 'incorrect'
                            : 'focused'
                        }`}
                      >
                        <span className="f4-input-value-text text-3xl md:text-4xl">
                          {feedback.visible
                            ? feedback.esCorrecta
                              ? feedback.resultado?.respuesta_correcta || respuestaNum
                              : respuestaNum || '?'
                            : respuestaNum || '?'}
                        </span>
                        {feedback.visible && (
                          <div className="f4-input-status-elements">
                            {feedback.esCorrecta ? (
                              <div className="f4-status-badge correct">
                                <svg className="f4-status-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round">
                                  <polyline points="20 6 9 17 4 12" />
                                </svg>
                              </div>
                            ) : (
                              <>
                                <span className="f4-era-pill">
                                  Era: {feedback.resultado?.respuesta_correcta}
                                </span>
                                <div className="f4-status-badge incorrect">
                                  <svg className="f4-status-icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round">
                                    <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
                                  </svg>
                                </div>
                              </>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Botón de reintentar removido: la transición es automática después de 2 segundos */}
                  <AnimatePresence>
                    {feedback.visible && !feedback.esCorrecta && (
                      <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0 }}
                        className="w-full mt-3 p-3.5 rounded-2xl bg-white/5 text-white/70 text-center font-medium text-sm"
                      >
                        Activando siguiente variante...
                      </motion.div>
                    )}
                  </AnimatePresence>
                </motion.div>
              </div>

              {/* Teclado numérico — Grilla simétrica 3x4 del Estándar Fase 2 */}
              <div className="w-[300px] shrink-0">
                <CustomKeyboard
                  onNumberPress={handleNumberPress}
                  onDelete={handleBackspace}
                  onSubmit={handleSubmit}
                  disabled={feedback.visible}
                  submitDisabled={showFractionInput ? (!respuestaNum.trim() || !respuestaDen.trim()) : !respuestaNum.trim()}
                />
              </div>
            </div>
          );
        })()}
      </motion.div>
    </motion.div>
  );
};
