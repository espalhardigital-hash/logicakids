import React from 'react';
import type { Fase4Pregunta } from './Fase4Types';
import { PizzaFractionVisualizer } from './PizzaFractionVisualizer';
import { BeakerVisualizer } from './BeakerVisualizer';
import { PieChartVisualizer } from './PieChartVisualizer';
import { PercentageBeaker } from './PercentageBeaker';
import { Fase4FabricVisualizer } from './Fase4FabricVisualizer';
import { Fase4NonHomogeneousPolygon } from './Fase4NonHomogeneousPolygon';
import { Fase4InteractiveBarChart } from './Fase4InteractiveBarChart';
import { ContextualPercentageVisualizer } from './ContextualPercentageVisualizer';
import { FractionPercentageVisualizer } from './FractionPercentageVisualizer';
import { RatioGridVisualizer } from './RatioGridVisualizer';

const SHAPES = ['circle', 'square', 'pentagon', 'hexagon'] as const;
// Referencia estable: evita recrear una función nueva en cada render cuando
// no se provee setVisualState (lo que forzaría un remount del canvas de Fabric.js).
const NOOP_STATE_CHANGE = (_val: any) => {};

export const getDeterministicShape = (seedText: string): 'circle' | 'square' | 'pentagon' | 'hexagon' => {
  let hash = 0;
  const safeText = seedText || '';
  for (let i = 0; i < safeText.length; i++) {
    hash = safeText.charCodeAt(i) + ((hash << 5) - hash);
  }
  const index = Math.abs(hash) % SHAPES.length;
  return SHAPES[index];
};

export const isDiscreteQuestion = (enunciado: string): boolean => {
  const lowercase = (enunciado || '').toLowerCase();
  const palabrasDiscretas = [
    'figurita', 'carta', 'manzana', 'moneda', 'tazo', 
    'galleta', 'chocolate', 'dulce', 'juguete', 'cupcake', 'caramelos'
  ];
  return palabrasDiscretas.some(palabra => lowercase.includes(palabra));
};

interface Props {
  pregunta: Fase4Pregunta;
  moduleColor: string;
  moduloId: number;
  nivelId: number;
  interactive?: boolean;
  
  // Para Pizza
  respuestaNum?: string;
  respuestaDen?: string;
  setRespuestaNum?: (val: string) => void;
  setRespuestaDen?: (val: string) => void;
  interactiveSelectedCount?: number;
  setInteractiveSelectedCount?: (val: number) => void;

  // Para Fabric/Shapes
  setVisualState?: (val: any) => void;

  // Para Polígono no homogéneo
  selectedPolygonIds?: number[];
  setSelectedPolygonIds?: React.Dispatch<React.SetStateAction<number[]>>;
  visualState?: any;
}

export const Fase4VisualizerEngine: React.FC<Props> = ({
  pregunta,
  moduleColor,
  moduloId,
  nivelId,
  interactive = false,
  
  respuestaNum = '',
  respuestaDen = '',
  setRespuestaNum,
  setRespuestaDen,
  interactiveSelectedCount = 0,
  setInteractiveSelectedCount,

  setVisualState,

  selectedPolygonIds = [],
  setSelectedPolygonIds,
  visualState,
}) => {
  const isFractionAnswer = (pregunta.respuesta_correcta ?? '').includes('/');
  const tipoVisual = pregunta.datos_numericos?.tipo_visual;
  const isVisualMultipleChoice = pregunta.alternativas?.some(alt => alt.texto.includes('<svg'));

  if (isVisualMultipleChoice) {
    return null;
  }

  if (interactive) {
    // Modo interactivo (Generalmente pizza o pie chart interactivo)
    if (tipoVisual === 'pizza') {
      return (
        <>
          <PizzaFractionVisualizer
            slices={pregunta.datos_numericos?.cortes || 8}
            initialSombreados={pregunta.datos_numericos?.sombreados || []}
            interactive={true}
            hideText={true}
            onChange={(selectedCount) => {
              setRespuestaNum?.(selectedCount.toString());
              setRespuestaDen?.((pregunta.datos_numericos?.cortes || 8).toString());
              setInteractiveSelectedCount?.(selectedCount);
            }}
            color={moduleColor}
            shape={getDeterministicShape(pregunta.enunciado)}
          />

          <div 
            className="mt-4 px-6 py-2 bg-slate-950/60 border border-purple-500/20 rounded-full font-sans font-black tracking-widest text-center shadow-lg"
            style={{ minWidth: '100px' }}
          >
            <span style={{ color: moduleColor }} className="text-2xl font-black">
              {interactiveSelectedCount}
            </span>
            <span className="text-slate-400 text-xl font-bold mx-2">/</span>
            <span className="text-slate-200 text-2xl font-black">
              {pregunta.datos_numericos?.cortes || 8}
            </span>
          </div>

          <div className="mt-6 text-center">
            <span className="text-slate-400 text-xs font-black tracking-[0.2em] block mb-2">
              SOMBREA EXACTAMENTE LA FRACCIÓN:
            </span>
            <span 
              style={{ color: moduleColor, textShadow: `0 0 15px ${moduleColor}60` }} 
              className="text-4xl font-sans font-black tracking-wider block"
            >
              {pregunta.respuesta_correcta}
            </span>
          </div>
        </>
      );
    }

    if (tipoVisual === 'pie') {
      return (
        <>
          <PieChartVisualizer
            pctA={pregunta.datos_numericos?.pct_a || 40}
            pctB={pregunta.datos_numericos?.pct_b || 35}
            pctC={pregunta.datos_numericos?.pct_c || 25}
            categorias={pregunta.datos_numericos?.categorias || ['Rojas', 'Verdes', 'Uvas']}
            interactive={true}
            onChange={(value) => {
              setRespuestaNum?.(value.toString());
            }}
            color={moduleColor}
          />
          <div className="mt-6 text-center">
            <span className="text-slate-400 text-xs font-black tracking-[0.2em] block mb-2">
              PORCENTAJE SELECCIONADO:
            </span>
            <span 
              style={{ color: moduleColor, textShadow: `0 0 15px ${moduleColor}60` }} 
              className="text-4xl font-sans font-black tracking-wider block"
            >
              {respuestaNum ? `${respuestaNum}%` : '?'}
            </span>
          </div>
        </>
      );
    }
  }

  // Modo estándar/repaso o no interactivo
  if (tipoVisual === 'pizza') {
    if (moduloId === 1 && nivelId === 2 && pregunta.datos_numericos?.num_base !== undefined) {
      const num_base = pregunta.datos_numericos.num_base;
      const den_base = pregunta.datos_numericos.den_base;
      const factor = pregunta.datos_numericos.factor;
      const num_eq = num_base * factor;
      const den_eq = den_base * factor;
      const shape = getDeterministicShape(pregunta.enunciado);
      return (
        <div className="flex items-center justify-center gap-6 my-4 scale-[0.9] origin-top">
          <div className="flex flex-col items-center">
            <PizzaFractionVisualizer
              slices={den_base}
              initialSombreados={Array.from({ length: num_base }, (_, i) => i)}
              interactive={false}
              hideText={true}
              color={moduleColor}
              shape={shape}
            />
            <span className="text-slate-300 font-black text-lg">{num_base}/{den_base}</span>
          </div>
          <div className="text-4xl font-black text-purple-400" style={{ color: moduleColor }}>=</div>
          <div className="flex flex-col items-center">
            <PizzaFractionVisualizer
              slices={den_eq}
              initialSombreados={Array.from({ length: num_eq }, (_, i) => i)}
              interactive={false}
              hideText={true}
              color={moduleColor}
              shape={shape}
            />
            <span className="text-slate-300 font-black text-lg">{num_eq}/{den_eq}</span>
          </div>
        </div>
      );
    }

    return (
      <PizzaFractionVisualizer
        slices={pregunta.datos_numericos?.cortes || 8}
        initialSombreados={pregunta.datos_numericos?.sombreados || []}
        interactive={!!pregunta.datos_numericos?.es_interactivo}
        onChange={(selectedCount) => {
          setRespuestaNum?.(selectedCount.toString());
          setRespuestaDen?.((pregunta.datos_numericos?.cortes || 8).toString());
          setInteractiveSelectedCount?.(selectedCount);
        }}
        color={moduleColor}
        shape={getDeterministicShape(pregunta.enunciado)}
      />
    );
  }

  if (tipoVisual === 'thermometer' || tipoVisual === 'beaker') {
    if (isDiscreteQuestion(pregunta.enunciado)) {
      return (
        <div className="text-center font-display text-7xl my-8 animate-pulse select-none">
          📦
        </div>
      );
    }

    return (
      <BeakerVisualizer
        divisions={pregunta.datos_numericos?.cortes || 5}
        initialLevel={pregunta.datos_numericos?.nivel || 0}
        interactive={!!pregunta.datos_numericos?.es_interactivo}
        onChange={(selectedLevel) => {
          if (isFractionAnswer) {
            setRespuestaNum?.(selectedLevel.toString());
            setRespuestaDen?.((pregunta.datos_numericos?.cortes || 5).toString());
          } else {
            setRespuestaNum?.(selectedLevel.toString());
          }
          setInteractiveSelectedCount?.(selectedLevel);
        }}
        color={moduleColor}
        type={tipoVisual === 'thermometer' ? 'thermometer' : 'beaker'}
      />
    );
  }

  if (tipoVisual === 'bar_chart') {
    return (
      <Fase4InteractiveBarChart
        valA={pregunta.datos_numericos?.val_a || 0}
        valB={pregunta.datos_numericos?.val_b || 0}
        categorias={pregunta.datos_numericos?.categorias}
        moduleColor={moduleColor}
      />
    );
  }

  if (tipoVisual === 'pie') {
    return (
      <PieChartVisualizer
        pctA={pregunta.datos_numericos?.pct_a || 40}
        pctB={pregunta.datos_numericos?.pct_b || 35}
        pctC={pregunta.datos_numericos?.pct_c || 25}
        categorias={pregunta.datos_numericos?.categorias || ['Rojas', 'Verdes', 'Uvas']}
        interactive={!!pregunta.datos_numericos?.es_interactivo}
        onChange={(value) => {
          setRespuestaNum?.(value.toString());
        }}
        color={moduleColor}
      />
    );
  }

  if (tipoVisual === 'percentage_thermometer' || tipoVisual === 'percentage_beaker') {
    return (
      <PercentageBeaker
        inputValue={respuestaNum}
        total={pregunta.datos_numericos?.total || 100}
        color={moduleColor}
        type={tipoVisual === 'percentage_thermometer' ? 'thermometer' : 'beaker'}
      />
    );
  }

  if (tipoVisual === 'contextual_bar') {
    const pct = pregunta.datos_numericos?.pct || 0;
    const total = pregunta.datos_numericos?.total || 100;
    const theme = pregunta.datos_numericos?.theme || 'battery';
    const unit = pregunta.datos_numericos?.unit || 'min';
    
    return (
      <div className="flex flex-col items-center gap-4 w-full">
        <ContextualPercentageVisualizer
          pct={pct}
          total={total}
          inputValue={respuestaNum}
          theme={theme}
          unit={unit}
          color={moduleColor}
        />
        
        {/* Caja de ecuación para conectar la visualización con la fórmula abstracta */}
        <div className="mt-2 px-6 py-3 bg-slate-900/60 border border-white/10 rounded-2xl flex items-center justify-center gap-3 shadow-lg min-w-[200px]">
          <span className="text-lg font-bold text-slate-300 font-sans select-none">
            {pct}% de {total} =
          </span>
          <span className="px-4 py-1.5 bg-slate-950 border border-white/10 rounded-xl text-white font-black text-2xl min-w-[64px] text-center font-display">
            {respuestaNum || '?'}
          </span>
        </div>
      </div>
    );
  }

  if (tipoVisual === 'fraction_percentage') {
    const pct = pregunta.datos_numericos?.pct || 0;
    const total = pregunta.datos_numericos?.total || 100;
    // El backend siembra el numerador/denominador objetivo reales en 'nivel'/'cortes'
    // (para preguntas de fracción simple 'pct' queda en 0 solo para controlar el
    // texto mostrado, así que el chequeo de acierto debe usar estos valores exactos
    // en vez de derivar el objetivo desde 'pct').
    const targetNum = pregunta.datos_numericos?.nivel;
    const targetDen = pregunta.datos_numericos?.cortes;

    return (
      <FractionPercentageVisualizer
        percentage={pct}
        total={total}
        targetNum={targetNum}
        targetDen={targetDen}
        color={moduleColor}
        interactive={interactive || !!pregunta.datos_numericos?.es_interactivo}
        respuestaNum={respuestaNum}
        respuestaDen={respuestaDen}
        setRespuestaNum={setRespuestaNum}
        setRespuestaDen={setRespuestaDen}
      />
    );
  }

  if (tipoVisual === 'shapes') {
    return (
      <Fase4FabricVisualizer
        datos_numericos={pregunta.datos_numericos}
        onStateChange={setVisualState || NOOP_STATE_CHANGE}
      />
    );
  }

  if (tipoVisual === 'non_homogeneous_polygon') {
    return (
      <Fase4NonHomogeneousPolygon
        sectors={pregunta.datos_numericos?.sectors || []}
        viewBox={pregunta.datos_numericos?.viewBox}
        selectedIds={selectedPolygonIds}
        onToggleSector={(id) => {
          if (setSelectedPolygonIds) {
            setSelectedPolygonIds(prev => 
              prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
            );
          }
        }}
        accentColor={moduleColor}
        targetFractionText={pregunta.datos_numericos?.target_fraction_text || pregunta.respuesta_correcta || ''}
        onReset={() => setSelectedPolygonIds?.([])}
      />
    );
  }

  if (tipoVisual === 'ratio_grid') {
    return (
      <RatioGridVisualizer
        pregunta={pregunta}
        moduleColor={moduleColor}
      />
    );
  }

  console.warn(
    `Fase4VisualizerEngine: no hay visualizador para tipo_visual="${tipoVisual}" (modulo ${moduloId}, nivel ${nivelId}).`
  );
  return (
    <div className="text-center text-slate-400 text-sm italic py-8 select-none">
      Sin gráfico disponible para esta pregunta.
    </div>
  );
};
