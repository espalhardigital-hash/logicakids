import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BookOpen, CheckCircle, XCircle, ArrowRight, ArrowLeft, LogOut, Sparkles } from 'lucide-react';
import { Fase5Lectura } from './Fase5Types';
import { formatContent, fixEncoding } from '../../services/textService';
import { PizzaFractionVisualizer } from './PizzaFractionVisualizer';
import { PieChartVisualizer } from './PieChartVisualizer';
import { FractionPercentageVisualizer } from './FractionPercentageVisualizer';
import './Fase5Styles.css';

interface Fase5TheoryModalProps {
  readingData: Fase5Lectura;
  moduleColor: string;
  onClose: () => void;
  onAbort?: () => void;
  isInitialReading?: boolean;
  isEvaluatorMode?: boolean;
}

const MODULE_NAMES: Record<number, string> = {
  1: 'La Fracción Visual',
  2: 'Fracción de Cantidad',
  3: 'Porcentajes Rápidos y Promedios',
  4: 'Razón y Mezclas',
};

const SHAPES = ['circle', 'square', 'pentagon', 'hexagon'] as const;

const getDeterministicShape = (seedText: string): 'circle' | 'square' | 'pentagon' | 'hexagon' => {
  let hash = 0;
  for (let i = 0; i < seedText.length; i++) {
    hash = seedText.charCodeAt(i) + ((hash << 5) - hash);
  }
  const index = Math.abs(hash) % SHAPES.length;
  return SHAPES[index];
};

const getFractionForPercentage = (pct: number) => {
  if (pct === 50) return { slices: 2, sombreados: [0] };
  if (pct === 25) return { slices: 4, sombreados: [0] };
  if (pct === 75) return { slices: 4, sombreados: [0, 1, 2] };
  
  for (let den = 2; den <= 20; den++) {
    const val = (pct * den) / 100;
    if (Number.isInteger(val)) {
      return { slices: den, sombreados: Array.from({ length: val }, (_, i) => i) };
    }
  }
  
  const den = 10;
  const num = Math.round((pct * den) / 100);
  return { slices: den, sombreados: Array.from({ length: num }, (_, i) => i) };
};

const stripHtmlAndComments = (html: string): string => {
  if (!html) return '';
  // Remover comentarios de HTML/SVG
  let clean = html.replace(/<!--[\s\S]*?-->/g, '');
  // Remover todas las etiquetas HTML/SVG
  clean = clean.replace(/<[^>]*>?/gm, '');
  return clean;
};

const extraerSvgYTexto = (html: string) => {
  if (!html) return { svg: null, texto: '' };
  
  // Si contiene múltiples SVGs o tiene un diseño flexible contenedor, no extraemos el SVG
  // para preservar la maquetación original del enunciado.
  const svgMatches = html.match(/<svg[\s\S]*?<\/svg>/g);
  if (svgMatches && svgMatches.length > 1) {
    return { svg: null, texto: html };
  }
  
  if (html.includes('display:flex') || html.includes('display: flex')) {
    return { svg: null, texto: html };
  }

  const svgMatch = html.match(/<svg[\s\S]*?<\/svg>/);
  if (svgMatch) {
    const svg = svgMatch[0];
    const texto = html.replace(/<svg[\s\S]*?<\/svg>/, '').replace(/<br\s*\/?>\s*$/, '').trim();
    return { svg, texto };
  }
  return { svg: null, texto: html };
};


export const Fase5TheoryModal: React.FC<Fase5TheoryModalProps> = ({
  readingData,
  moduleColor,
  onClose,
  onAbort,
  isInitialReading = true,
  isEvaluatorMode = false
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

  const paginateParagraphs = (paragraphs: string[]) => paragraphs.flatMap((paragraph) => {
    if (paragraph.length <= 420) return [paragraph];
    const sentences = paragraph.match(/[^.!?]+[.!?]+(?:\s|$)|[^.!?]+$/g) || [paragraph];
    const pages: string[] = [];
    let current = '';
    for (const sentence of sentences) {
      if (current && current.length + sentence.length > 420) {
        pages.push(current.trim());
        current = sentence;
      } else {
        current += sentence;
      }
    }
    if (current.trim()) pages.push(current.trim());
    return pages;
  });

  const renderInteractiveBarChart = (globalIdx: number) => {
    const valA = 100;
    const valB = 150;
    const valC = 50;

    const hMax = 180;
    const getScaleY = (val: number) => 100 - (val / hMax) * 80;

    const yA = getScaleY(valA);
    const yB = getScaleY(valB);
    const yC = getScaleY(valC);

    const hA = 100 - yA;
    const hB = 100 - yB;
    const hC = 100 - yC;

    let opacityA = 1;
    let opacityB = 1;
    let opacityC = 1;
    
    if (globalIdx === 1) {
      opacityA = 0.3;
    }

    return (
      <div className="flex flex-col items-center w-full max-w-[370px] mx-auto mt-4 p-3 bg-slate-900/60 backdrop-blur-md rounded-2xl border border-slate-700/50 shadow-lg">
        <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-2">Gráfico de Barras de Referencia</span>
        <svg viewBox="0 0 240 120" className="w-full h-auto bg-slate-950/80 rounded-xl border border-slate-800 p-1">
          {[0, 50, 100, 150].map((val) => {
            const y = getScaleY(val);
            return (
              <g key={val}>
                <line x1={35} y1={y} x2={220} y2={y} stroke="#334155" strokeWidth="1" strokeOpacity="0.4" strokeDasharray={val === 0 ? "none" : "3 3"} />
                <text x={28} y={y + 3} fontFamily="Arial" fontSize="9" fontWeight="bold" fill="#94a3b8" textAnchor="end">{val}</text>
              </g>
            );
          })}

          <line x1={35} y1={100} x2={225} y2={100} stroke="#94a3b8" strokeWidth="1.5" />
          <line x1={35} y1={20} x2={35} y2={100} stroke="#94a3b8" strokeWidth="1.5" />

          <g opacity={opacityA} className="transition-all duration-300">
            <rect x={60} y={yA} width={25} height={hA} rx={3} fill="url(#gradIntA)" stroke="#a78bfa" strokeWidth={1} />
            <text x={72.5} y={yA - 4} fontFamily="Arial" fontSize="9" fontWeight="black" fill="#c084fc" textAnchor="middle">{valA}</text>
            <text x={72.5} y={112} fontFamily="Arial" fontSize="9" fontWeight="black" fill="#94a3b8" textAnchor="middle">A</text>
          </g>

          <g opacity={opacityB} className="transition-all duration-300">
            <rect x={110} y={yB} width={25} height={hB} rx={3} fill="url(#gradIntB)" stroke="#10b981" strokeWidth={1} />
            <text x={122.5} y={yB - 4} fontFamily="Arial" fontSize="9" fontWeight="black" fill="#34d399" textAnchor="middle">{valB}</text>
            <text x={122.5} y={112} fontFamily="Arial" fontSize="9" fontWeight="black" fill="#94a3b8" textAnchor="middle">B</text>
          </g>

          <g opacity={opacityC} className="transition-all duration-300">
            <rect x={160} y={yC} width={25} height={hC} rx={3} fill="url(#gradIntC)" stroke="#f59e0b" strokeWidth={1} />
            <text x={172.5} y={yC - 4} fontFamily="Arial" fontSize="9" fontWeight="black" fill="#fbbf24" textAnchor="middle">{valC}</text>
            <text x={172.5} y={112} fontFamily="Arial" fontSize="9" fontWeight="black" fill="#94a3b8" textAnchor="middle">C</text>
          </g>

          {globalIdx === 1 && (
            <g className="animate-pulse">
              <line x1={172.5} y1={yC} x2={122.5} y2={yC} stroke="#fbbf24" strokeWidth="1" strokeDasharray="3 2" strokeOpacity="0.7" />
              <line x1={140} y1={yB} x2={140} y2={yC} stroke="#ff007f" strokeWidth="1.5" />
              <polygon points={`137,${yB + 3} 140,${yB} 143,${yB + 3}`} fill="#ff007f" />
              <polygon points={`137,${yC - 3} 140,${yC} 143,${yC - 3}`} fill="#ff007f" />
              <rect x={144} y={(yB + yC) / 2 - 6} width={22} height={12} rx={2} fill="#ff007f" />
              <text x={155} y={(yB + yC) / 2 + 3} fontFamily="Arial" fontSize="8" fontWeight="bold" fill="#FFF" textAnchor="middle">100</text>
            </g>
          )}

          {globalIdx === 2 && (
            <g className="animate-pulse">
              <line x1={35} y1={yB} x2={220} y2={yB} stroke="#10b981" strokeWidth="1" strokeDasharray="4 2" strokeOpacity="0.6" />
              <rect x={60} y={yB} width={25} height={hC} rx={2} fill="none" stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="3 2" />
              <text x={72.5} y={yB + hC / 2 + 3} fontFamily="Arial" fontSize="8" fontWeight="bold" fill="#fbbf24" textAnchor="middle">+50</text>
              <text x={95} y={yB + 10} fontFamily="Arial" fontSize="9" fontWeight="bold" fill="#34d399">A + C = B</text>
            </g>
          )}

          <defs>
            <linearGradient id="gradIntA" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#a78bfa" />
              <stop offset="100%" stopColor="#6d28d9" />
            </linearGradient>
            <linearGradient id="gradIntB" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#10b981" />
              <stop offset="100%" stopColor="#047857" />
            </linearGradient>
            <linearGradient id="gradIntC" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#f59e0b" />
              <stop offset="100%" stopColor="#b45309" />
            </linearGradient>
          </defs>
        </svg>
      </div>
    );
  };

  const renderAverageInteractiveChart = (globalIdx: number) => {
    let values = [4, 8, 12];
    let labels = ['A', 'B', 'C'];
    let average = 8;

    if (globalIdx === 1) {
      values = [10, 20];
      labels = ['Amigo 1', 'Amigo 2'];
      average = 15;
    } else if (globalIdx === 2) {
      values = [6, 6, 12];
      labels = ['Día 1', 'Día 2', 'Día 3'];
      average = 8;
    }

    const maxVal = Math.max(...values);
    const yScaleMax = maxVal + 4;
    const getScaleY = (val: number) => 100 - (val / yScaleMax) * 80;

    const yAvg = getScaleY(average);

    return (
      <div className="flex flex-col items-center w-full max-w-[555px] mx-auto mt-4 p-3 bg-slate-900/60 backdrop-blur-md rounded-2xl border border-slate-700/50 shadow-lg">
        <svg viewBox="0 0 240 130" className="w-full h-auto bg-slate-950/80 rounded-xl border border-slate-800 p-1">
          {[0, Math.round(average), Math.round(yScaleMax - 2)].map((val) => {
            const y = getScaleY(val);
            return (
              <g key={val}>
                <line x1={35} y1={y} x2={220} y2={y} stroke="#334155" strokeWidth="1" strokeOpacity="0.4" strokeDasharray={val === 0 ? "none" : "3 3"} />
                <text x={28} y={y + 3} fontFamily="Arial" fontSize="9" fontWeight="bold" fill="#94a3b8" textAnchor="end">{val}</text>
              </g>
            );
          })}

          <line x1={35} y1={100} x2={225} y2={100} stroke="#94a3b8" strokeWidth="1.5" />
          <line x1={35} y1={20} x2={35} y2={100} stroke="#94a3b8" strokeWidth="1.5" />

          {values.map((val, idx) => {
            const width = 20;
            const spacing = values.length === 2 ? 60 : 45;
            const startX = values.length === 2 ? 70 : 55;
            const x = startX + idx * spacing;
            const y = getScaleY(val);
            const height = 100 - y;
            
            const fillGradient = idx === 0 ? 'url(#gradIntA)' : idx === 1 ? 'url(#gradIntB)' : 'url(#gradIntC)';
            const strokeColor = idx === 0 ? '#a78bfa' : idx === 1 ? '#10b981' : '#f59e0b';

            return (
              <g key={idx}>
                {Array.from({ length: val }).map((_, blockIdx) => {
                  const blockHeight = height / val;
                  const blockY = 100 - (blockIdx + 1) * blockHeight;
                  return (
                    <rect
                      key={blockIdx}
                      x={x}
                      y={blockY + 0.5}
                      width={width}
                      height={blockHeight - 1}
                      rx={1}
                      fill={fillGradient}
                      stroke={strokeColor}
                      strokeWidth={0.5}
                    />
                  );
                })}
                <text x={x + width / 2} y={y - 4} fontFamily="Arial" fontSize="9" fontWeight="black" fill={strokeColor} textAnchor="middle">{val}</text>
                <text x={x + width / 2} y={112} fontFamily="Arial" fontSize="9" fontWeight="black" fill="#94a3b8" textAnchor="middle">{labels[idx]}</text>
              </g>
            );
          })}



          <defs>
            <linearGradient id="gradIntA" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#a78bfa" />
              <stop offset="100%" stopColor="#6d28d9" />
            </linearGradient>
            <linearGradient id="gradIntB" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#10b981" />
              <stop offset="100%" stopColor="#047857" />
            </linearGradient>
            <linearGradient id="gradIntC" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#f59e0b" />
              <stop offset="100%" stopColor="#b45309" />
            </linearGradient>
          </defs>
        </svg>
      </div>
    );
  };

  const slides = useMemo(() => {
    const s: { type: string; data: any; exampleIndex?: number; totalExamples?: number }[] = [];
    const parrafosRaw = readingData.parrafos || [];
    const sepIdx = parrafosRaw.indexOf('---');
    
    let parrafosParte1 = [...parrafosRaw];
    let parrafosParte2: string[] = [];
    
    if (sepIdx !== -1) {
      parrafosParte1 = parrafosRaw.slice(0, sepIdx);
      parrafosParte2 = parrafosRaw.slice(sepIdx + 1);
    }
    
    const ejemplosRaw = readingData.ejemplos || [];
    const ejemploChunks = chunkArray(ejemplosRaw, 1);
    
    // Cada pantalla contiene una pieza de lectura acotada. Nunca se oculta
    // texto debajo del borde ni se exige desplazamiento vertical.
    paginateParagraphs(parrafosParte1).forEach((paragraph) => {
      s.push({ type: 'intro', data: { parrafos: [paragraph], mostrarDiccionario: false } });
    });

    const dictionaryEntries = Object.entries(readingData.diccionario || {});
    chunkArray(dictionaryEntries, 3).forEach((entries) => {
      s.push({ type: 'intro', data: { parrafos: [], mostrarDiccionario: true, diccionario: Object.fromEntries(entries) } });
    });
    
    // Cada ejemplo en su propia slide independiente (Regla T3: Cero scroll vertical)
    ejemploChunks.forEach((chunk, index) => {
      s.push({ 
        type: 'examples', 
        data: chunk,
        exampleIndex: index + 1,
        totalExamples: ejemplosRaw.length
      });
    });
    
    // Slide 3: Teoría Parte 2 (Si existe, sin diccionario)
    paginateParagraphs(parrafosParte2).forEach((paragraph) => {
      s.push({ type: 'intro', data: { parrafos: [paragraph], mostrarDiccionario: false } });
    });

    // Interactivos prácticos SOLO SI TIENEN CONTENIDO REAL (enunciado/pregunta y respuesta definida)
    if (readingData.interactivos && readingData.interactivos.length > 0) {
      const validInteractivos = readingData.interactivos.filter(
        (item: any) => (item.enunciado || item.pregunta) && (item.respuesta !== undefined)
      );
      if (validInteractivos.length > 0) {
        const withIndex = validInteractivos.map((item: any, index: number) => ({ ...item, globalIndex: index }));
        const chunks = chunkArray(withIndex, 1);
        chunks.forEach((c: any) => s.push({ type: 'interactives', data: c }));
      }
    }

    if (readingData.tip_pedagogico) {
      s.push({ type: 'tip', data: readingData.tip_pedagogico });
    }

    return s;
  }, [readingData]);

  const totalSteps = slides.length;
  const currentSlide = slides[currentStep];

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
      if (!feedback[globalIdx] || !feedback[globalIdx].isCorrect) return false;
    }
    return true;
  }, [currentSlide, feedback, isEvaluatorMode]);

  const [direction, setDirection] = useState(0);

  const goToStep = (newStep: number) => {
    setDirection(newStep > currentStep ? 1 : -1);
    setCurrentStep(newStep);
  };

  const variants = {
    enter: (direction: number) => ({
      x: direction > 0 ? 100 : -100,
      opacity: 0
    }),
    center: {
      zIndex: 1,
      x: 0,
      opacity: 1
    },
    exit: (direction: number) => ({
      zIndex: 0,
      x: direction < 0 ? 100 : -100,
      opacity: 0
    })
  };

  return (
    <div className="f5-reading-overlay">
      <motion.div 
        initial={{ scale: 0.95, y: 20, opacity: 0 }}
        animate={{ scale: 1, y: 0, opacity: 1 }}
        exit={{ scale: 0.95, y: 20, opacity: 0 }}
        transition={{ type: "spring", duration: 0.5 }}
        className="f5-reading-card"
        style={{ '--neon-accent-color': moduleColor } as React.CSSProperties}
      >
        {/* Header */}
        <div className="f5-reading-header">
          <div className="f5-reading-icon" style={{ backgroundColor: `${moduleColor}18`, color: moduleColor }}>
            <BookOpen size={22} />
          </div>
          <div className="f5-reading-header-content">
            <div className="f5-reading-badge" style={{ color: moduleColor }}>
              MÓDULO {readingData.modulo_id}: {MODULE_NAMES[readingData.modulo_id] || 'Fracciones'} • NIVEL {readingData.nivel_id}
            </div>
            <h2 className="f5-reading-title">
               💡 {fixEncoding(readingData.titulo)}
            </h2>
          </div>
          
          <div className="f5-reading-header-controls">
            {onAbort && (
              <button 
                onClick={onAbort}
                title={isInitialReading ? "Salir del nivel" : "Cerrar Teoría"}
                className="f5-abort-btn"
              >
                <LogOut size={16} />
              </button>
            )}
            <div className="f5-step-indicator">
              Paso {currentStep + 1} de {totalSteps}
            </div>
          </div>
        </div>
        
        {/* Body */}
        <div className="f5-reading-body">
          <AnimatePresence mode="wait" custom={direction}>
            {currentSlide?.type === 'intro' && (
              <motion.div
                key={`intro-${currentStep}`}
                custom={direction}
                variants={variants}
                initial="enter"
                animate="center"
                exit="exit"
                transition={{ duration: 0.25 }}
                className="f5-flashcard-content"
              >
                {(currentSlide.data?.parrafos || readingData.parrafos || []).map((p: string, idx: number) => (
                  <p key={idx} className="f5-reading-p" dangerouslySetInnerHTML={{ __html: formatContent(p) }} />
                ))}

                {(currentSlide.data === null || currentSlide.data?.mostrarDiccionario) && (currentSlide.data?.diccionario || readingData.diccionario) && Object.keys(currentSlide.data?.diccionario || readingData.diccionario).length > 0 && (
                  <div className="f5-reading-dictionary">
                    <h3>🔍 DICCIONARIO MATEMÁTICO:</h3>
                    <div className="f5-dict-grid">
                      {Object.entries(currentSlide.data?.diccionario || readingData.diccionario).map(([termino, definicion], idx) => (
                        <div key={idx} className="f5-dict-card" style={{ borderColor: `${moduleColor}33` }}>
                          <div className="f5-dict-term" style={{ color: moduleColor }} dangerouslySetInnerHTML={{ __html: formatContent(termino) }} />
                          <div className="f5-dict-def" dangerouslySetInnerHTML={{ __html: formatContent(definicion as string) }} />
                        </div>
                      ))}
                    </div>
                  </div>
                )}
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
                transition={{ duration: 0.25 }}
                className="f5-flashcard-content"
              >
                {currentSlide.data.length > 0 ? (
                  <div className="f5-reading-examples">
                    <h3>📐 EJEMPLO ILUSTRADO {(currentSlide as any).exampleIndex ? `(${(currentSlide as any).exampleIndex} de ${(currentSlide as any).totalExamples})` : ''}:</h3>
                    {currentSlide.data.map((ex: any, idx: number) => {
                      let fractionVisualizer = null;
                      let hideEnunciadoSvg = false;
                      if (readingData.modulo_id === 1) {
                         const textToSearch = ex.enunciado + " " + (ex.pasos ? ex.pasos.map((p: any) => p.texto).join(" ") : "") + " " + (ex.respuesta || "");
                         const matches = Array.from(textToSearch.matchAll(/(\d+)\/(\d+)/g));
                         const uniqueFractions: { num: number; den: number }[] = [];
                         const seen = new Set<string>();
                         
                         for (const match of matches) {
                            const num = parseInt(match[1], 10);
                            const den = parseInt(match[2], 10);
                            const key = `${num}/${den}`;
                            if (!seen.has(key) && num <= den && den <= 20) {
                               seen.add(key);
                               uniqueFractions.push({ num, den });
                            }
                         }
                         
                         const shape = getDeterministicShape(ex.enunciado);
                         
                         if (uniqueFractions.length >= 2) {
                            // Equivalency mode: side-by-side with an "=" sign
                            fractionVisualizer = (
                               <div className="flex items-center justify-center gap-4 my-2 scale-[0.8] origin-top">
                                  <div className="flex flex-col items-center">
                                     <PizzaFractionVisualizer slices={uniqueFractions[0].den} initialSombreados={Array.from({ length: uniqueFractions[0].num }, (_, i) => i)} color={moduleColor} interactive={false} hideText={true} shape={shape} size={90} />
                                     <span className="text-slate-300 font-black text-lg">{uniqueFractions[0].num}/{uniqueFractions[0].den}</span>
                                  </div>
                                  <div className="text-4xl font-black text-purple-400" style={{ color: moduleColor }}>=</div>
                                  <div className="flex flex-col items-center">
                                     <PizzaFractionVisualizer slices={uniqueFractions[1].den} initialSombreados={Array.from({ length: uniqueFractions[1].num }, (_, i) => i)} color={moduleColor} interactive={false} hideText={true} shape={shape} size={90} />
                                     <span className="text-slate-300 font-black text-lg">{uniqueFractions[1].num}/{uniqueFractions[1].den}</span>
                                  </div>
                               </div>
                            );
                         } else if (uniqueFractions.length === 1) {
                            fractionVisualizer = (
                               <div className="flex flex-col items-center justify-center my-2 scale-[0.8] origin-top">
                                  <PizzaFractionVisualizer slices={uniqueFractions[0].den} initialSombreados={Array.from({ length: uniqueFractions[0].num }, (_, i) => i)} color={moduleColor} interactive={false} hideText={true} shape={shape} size={90} />
                                  <span className="text-slate-300 font-black text-lg">{uniqueFractions[0].num}/{uniqueFractions[0].den}</span>
                                </div>
                            );
                         }
                      } else if (readingData.modulo_id === 2) {
                         const cleanEnunciado = ex.enunciado.replace(/<[^>]*>?/gm, '');
                         const fractionMatch = cleanEnunciado.match(/(\d+)\/(\d+)/);
                         const allNumbers = cleanEnunciado.match(/\b(\d+)\b/g);
                         
                         let num = 0, den = 0, qty = 0;
                         if (fractionMatch) {
                            num = parseInt(fractionMatch[1], 10);
                            den = parseInt(fractionMatch[2], 10);
                            
                            if (allNumbers) {
                               const numbers = allNumbers.map((n: string) => parseInt(n, 10));
                               const foundQty = numbers.find((n: number) => n !== num && n !== den && n % den === 0);
                               if (foundQty) {
                                 qty = foundQty;
                               } else {
                                 const anyNum = numbers.find((n: number) => n !== num && n !== den);
                                 if (anyNum) qty = anyNum;
                               }
                            }
                         }
                         
                         if (num > 0 && den > 0 && qty > 0) {
                            fractionVisualizer = (
                               <div className="flex flex-col items-center justify-center my-2 scale-[0.8] origin-top w-full">
                                  <FractionPercentageVisualizer
                                     percentage={0}
                                     total={qty}
                                     color={moduleColor}
                                     interactive={false}
                                     respuestaNum={num.toString()}
                                     respuestaDen={den.toString()}
                                  />
                               </div>
                            );
                         }
                      } else if (readingData.modulo_id === 3) {
                         const isRemaining = ex.enunciado.toLowerCase().includes('resto') && 
                                             (ex.enunciado.toLowerCase().includes('¿qué porcentaje') || ex.enunciado.toLowerCase().includes('qué porcentaje'));
                         
                         if (isRemaining) {
                            hideEnunciadoSvg = true;
                            const cleanEnunciado = ex.enunciado.replace(/<[^>]*>/g, ' ');
                            const matches = Array.from(cleanEnunciado.matchAll(/(\d+)%\s+(?:prefiere\s+|son\s+)?([a-z\u00E0-\u00FC]+)/gi));
                            
                            let pctA = 40, pctB = 35, pctC = 25;
                            let catA = 'Fútbol', catB = 'Básquet', catC = 'Vóley';
                            
                            if (matches.length >= 2) {
                               pctA = parseInt(matches[0][1], 10);
                               catA = matches[0][2].charAt(0).toUpperCase() + matches[0][2].slice(1);
                               
                               pctB = parseInt(matches[1][1], 10);
                               catB = matches[1][2].charAt(0).toUpperCase() + matches[1][2].slice(1);
                               
                               pctC = 100 - pctA - pctB;
                            }
                            
                            const restoMatch = cleanEnunciado.match(/resto\s+([a-z\u00E0-\u00FC]+)/i);
                            if (restoMatch) {
                               catC = restoMatch[1].charAt(0).toUpperCase() + restoMatch[1].slice(1);
                            }
                            
                            fractionVisualizer = (
                               <div className="flex flex-col items-center justify-center my-2 scale-[0.9] origin-top w-full mb-4">
                                  <PieChartVisualizer
                                     pctA={pctA}
                                     pctB={pctB}
                                     pctC={pctC}
                                     categorias={[catA, catB, catC]}
                                     interactive={false}
                                     color={moduleColor}
                                  />
                                  <div 
                                    className="mt-4 flex items-center justify-center gap-2 px-3 py-2 bg-slate-900/40 border border-white/10 rounded-xl text-white text-base font-black font-sans relative"
                                    style={{ borderColor: `${moduleColor}40`, boxShadow: `0 0 15px ${moduleColor}10` }}
                                  >
                                    {/* Checkmark de completado/teoría */}
                                    <div 
                                      className="absolute -top-3 -right-3 w-8 h-8 rounded-full flex items-center justify-center text-white text-lg animate-bounce shadow-lg"
                                      style={{ backgroundColor: '#F97316' }}
                                    >
                                      ✓
                                    </div>
                                    <span>100%</span>
                                    <span className="text-slate-500">-</span>
                                    <span style={{ color: '#A855F7' }}>{pctA}%</span>
                                    <span className="text-slate-500">-</span>
                                    <span style={{ color: '#7C3AED' }}>{pctB}%</span>
                                    <span className="text-slate-500">=</span>
                                    <span style={{ color: '#10B981' }}>{pctC}%</span>
                                  </div>
                               </div>
                            );
                         } else {
                            const cleanEnunciado = stripHtmlAndComments(ex.enunciado || '');
                            const cleanRespuesta = stripHtmlAndComments(ex.respuesta || '');
                            const cleanText = cleanEnunciado + " " + cleanRespuesta;
                            const match = cleanText.match(/(\d+)%/);
                            const allNumbers = cleanEnunciado.match(/\b(\d+)\b/g);
                            if (match) {
                               const pct = parseInt(match[1], 10);
                               let total = 100;
                               if (allNumbers) {
                                  const numbers = allNumbers.map((n: string) => parseInt(n, 10));
                                  const foundTotal = numbers.find((n: number) => n !== pct && n > 0);
                                  if (foundTotal) total = foundTotal;
                               }
                               const { slices, sombreados } = getFractionForPercentage(pct);
                               const num = sombreados.length;
                               const den = slices;
                               
                               fractionVisualizer = (
                                  <div className="flex flex-col items-center justify-center my-2 scale-[0.8] origin-top w-full">
                                     <FractionPercentageVisualizer
                                        percentage={pct}
                                        total={total}
                                        color={moduleColor}
                                        interactive={false}
                                        respuestaNum={num.toString()}
                                        respuestaDen={den.toString()}
                                     />
                                  </div>
                               );
                            }
                         }
                      }
                      
                      const { svg: exSvg, texto: exTexto } = extraerSvgYTexto(ex.enunciado);
                      const finalHideEnunciadoSvg = hideEnunciadoSvg || !!fractionVisualizer;
                      const tieneVisuals = !!fractionVisualizer || (!!exSvg && !finalHideEnunciadoSvg);
                      
                      return (
                        <div key={idx} className="f5-example-box" style={{ borderLeftColor: moduleColor }}>
                          {tieneVisuals ? (
                            <div className="f5-example-box-layout flex-col items-stretch">
                              <div className="f5-example-details">
                                <div className="f5-ex-q" dangerouslySetInnerHTML={{ __html: exTexto }} />
                                {ex.pasos ? (
                                  <div className="f5-ex-steps">
                                    {ex.pasos.map((paso: any) => (
                                      <div key={paso.orden} className="f5-ex-step">
                                        <span className="f5-ex-step-num" style={{ color: moduleColor, backgroundColor: `${moduleColor}12` }}>{paso.orden}</span>
                                        <span className="f5-ex-step-text" dangerouslySetInnerHTML={{ __html: paso.texto }} />
                                      </div>
                                    ))}
                                  </div>
                                ) : (
                                   <div className="f5-ex-legacy">Respuesta → <span style={{ color: moduleColor, fontWeight: 800 }} dangerouslySetInnerHTML={{ __html: ex.respuesta }} /></div>
                                )}
                              </div>
                              <div className="f5-example-visuals-row mt-4">
                                {fractionVisualizer}
                                {exSvg && !finalHideEnunciadoSvg && <div dangerouslySetInnerHTML={{ __html: exSvg }} />}
                              </div>
                            </div>
                          ) : (
                            <>
                              <div className="f5-ex-q" dangerouslySetInnerHTML={{ __html: formatContent(ex.enunciado) }} />
                              {ex.pasos ? (
                                <div className="f5-ex-steps">
                                  {ex.pasos.map((paso: any) => (
                                    <div key={paso.orden} className="f5-ex-step">
                                      <span className="f5-ex-step-num" style={{ color: moduleColor, backgroundColor: `${moduleColor}12` }}>{paso.orden}</span>
                                      <span className="f5-ex-step-text" dangerouslySetInnerHTML={{ __html: formatContent(paso.texto) }} />
                                    </div>
                                  ))}
                                </div>
                              ) : (
                                 <div className="f5-ex-legacy">Respuesta → <span style={{ color: moduleColor, fontWeight: 800 }} dangerouslySetInnerHTML={{ __html: formatContent(ex.respuesta) }} /></div>
                              )}
                            </>
                          )}
                        </div>
                      );
                    })}
                  </div>
                ) : (
                  <div className="f5-reading-p text-center opacity-70">
                    Sigue adelante para repasar conceptos prácticos e interactivos.
                  </div>
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
                transition={{ duration: 0.25 }}
                className="f5-flashcard-content"
              >
                <div className="f5-reading-interactive">
                  <h3>🎯 ENTRENAMIENTO RÁPIDO: Completa para avanzar</h3>
                  {currentSlide.data.map((int: any, localIdx: number) => {
                    const idx = int.globalIndex;
                    const qText = int.enunciado || int.pregunta;
                    const isCorrect = feedback[idx]?.isCorrect;
                    const isLocked = localIdx > 0 && !feedback[currentSlide.data[localIdx - 1].globalIndex]?.isCorrect;
                    
                    return (
                      <div 
                        key={idx} 
                        className={`f5-interactive-box ${isCorrect ? 'correct' : ''} ${feedback[idx] && !isCorrect ? 'error' : ''}`}
                        style={isLocked ? { position: 'relative', overflow: 'hidden', minHeight: '110px' } : {}}
                      >
                        <div 
                          className="f5-int-q"
                          style={isLocked ? { filter: 'blur(5px)', opacity: 0.3, pointerEvents: 'none', userSelect: 'none' } : {}}
                        >
                          {qText}
                        </div>
                        
                        {isLocked ? (
                          <div className="f5-interactive-locked-overlay">
                            <span>🔒</span>
                            <span>Completa el ejercicio anterior para desbloquear</span>
                          </div>
                        ) : (
                          <>
                            {int.pasos && (
                              <div className="f5-ex-steps">
                                {int.pasos.map((paso: any) => {
                                  const isInputPaso = paso.texto.includes("= ?");
                                  if (isInputPaso) {
                                    const parts = paso.texto.split("= ?");
                                    return (
                                      <div key={paso.orden} className="f5-ex-step input-step">
                                        <span className="f5-ex-step-num" style={{ color: moduleColor, backgroundColor: `${moduleColor}12` }}>{paso.orden}</span>
                                        <span className="f5-ex-step-text">{parts[0]} = </span>
                                        <div className="f5-int-input-group">
                                          <input 
                                            type="text" 
                                            className="f5-int-input"
                                            value={answers[idx] || ''}
                                            onChange={(e) => handleAnswerChange(idx, e.target.value)}
                                            disabled={isCorrect}
                                            onKeyDown={(e) => {
                                              if (e.key === 'Enter') handleVerify(idx, int.respuesta, int.feedback_acierto, int.feedback_error);
                                            }}
                                            autoComplete="off"
                                          />
                                          {!isCorrect && (
                                            <button 
                                              className="f5-int-verify"
                                              style={{ background: moduleColor }}
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
                                    <div key={paso.orden} className="f5-ex-step">
                                      <span className="f5-ex-step-num" style={{ color: moduleColor, backgroundColor: `${moduleColor}12` }}>{paso.orden}</span>
                                      <span className="f5-ex-step-text">{paso.texto}</span>
                                    </div>
                                  );
                                })}
                              </div>
                            )}
                            {!int.pasos && (
                              <div className="f5-int-input-group legacy">
                                <input 
                                  type="text" 
                                  className="f5-int-input"
                                  value={answers[idx] || ''}
                                  onChange={(e) => handleAnswerChange(idx, e.target.value)}
                                  disabled={isCorrect}
                                  onKeyDown={(e) => {
                                    if (e.key === 'Enter') handleVerify(idx, int.respuesta, int.feedback_acierto, int.feedback_error);
                                  }}
                                  autoComplete="off"
                                />
                                {!isCorrect && (
                                  <button 
                                    className="f5-int-verify"
                                    style={{ background: moduleColor }}
                                    onClick={() => handleVerify(idx, int.respuesta, int.feedback_acierto, int.feedback_error)}
                                  >
                                    Verificar
                                  </button>
                                )}
                              </div>
                            )}
                            
                            {feedback[idx] && (
                              <div className={`f5-int-feedback ${feedback[idx].isCorrect ? 'success' : 'error'}`}>
                                {feedback[idx].isCorrect ? <CheckCircle size={18} /> : <XCircle size={18} />}
                                <span>{feedback[idx].message}</span>
                              </div>
                            )}

                            {readingData.modulo_id === 3 && readingData.nivel_id === 3 && (
                              renderInteractiveBarChart(idx)
                            )}

                            {readingData.modulo_id === 3 && readingData.nivel_id === 4 && (
                              renderAverageInteractiveChart(idx)
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
                transition={{ duration: 0.25 }}
                className="f5-flashcard-content"
              >
                <div className="f5-reading-tip highlighted">
                  <div className="f5-tip-title-box">
                    <span style={{ fontSize: '1.25rem' }}>⚠️</span>
                    <span>¡ANÁLISIS DE MISIÓN ADVERSA!</span>
                  </div>
                  <div className="f5-tip-text">
                    {currentSlide.data}
                  </div>
                </div>

                <div className="f5-ready-container">
                  <motion.div 
                    className="f5-ready-rocket"
                    animate={{ 
                      y: [0, -12, 0],
                      rotate: [0, 4, -4, 0]
                    }}
                    transition={{ 
                      duration: 3, 
                      repeat: Infinity,
                      ease: "easeInOut"
                    }}
                  >
                    🚀
                  </motion.div>
                  <div className="f5-ready-msg">
                    ¡Excelente preparación!<br />
                    El sistema de fracciones está listo. ¡Es hora de jugar!
                  </div>
                  <div className="f5-ready-stars">
                    {[...Array(5)].map((_, i) => (
                      <motion.span 
                        key={i}
                        className="f5-ready-star"
                        animate={{ opacity: [0.2, 1, 0.2], scale: [1, 1.2, 1] }}
                        transition={{ duration: 1.8 + i * 0.4, repeat: Infinity }}
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
        
        <div className="f5-reading-footer">
          <button 
            className="f5-nav-btn" 
            disabled={currentStep === 0}
            onClick={() => goToStep(currentStep - 1)}
          >
            <ArrowLeft size={18} /> Atrás
          </button>
          
          {isEvaluatorMode && (
            <button
              className="f5-nav-btn evaluator-skip-theory"
              style={{ background: '#eab308', color: '#fff', border: 'none', borderRadius: '12px', padding: '10px 18px', fontWeight: 800, fontSize: '0.8rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px', marginLeft: 'auto', marginRight: '10px' }}
              onClick={onClose}
              title="Avanzar directamente a la práctica (Modo Evaluador)"
            >
              <span>Avanzar a Práctica ⏭️</span>
            </button>
          )}
          
          {currentStep < totalSteps - 1 ? (
            <button 
              className="f5-nav-btn primary" 
              style={{ background: moduleColor, opacity: canGoNext ? 1 : 0.5, marginLeft: isEvaluatorMode ? '0' : 'auto' }}
              disabled={!canGoNext}
              onClick={() => goToStep(currentStep + 1)}
            >
              Siguiente <ArrowRight size={18} />
            </button>
          ) : (
            <button 
              className="f5-reading-close-btn"
              style={{ background: `linear-gradient(135deg, ${moduleColor}cc, ${moduleColor})`, marginLeft: isEvaluatorMode ? '0' : 'auto' }}
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
