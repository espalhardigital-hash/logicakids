import React from 'react';
import type { Fase5Pregunta } from './Fase5Types';
import { PizzaFractionVisualizer } from './PizzaFractionVisualizer';
import { BeakerVisualizer } from './BeakerVisualizer';
import { PieChartVisualizer } from './PieChartVisualizer';
import { PercentageBeaker } from './PercentageBeaker';
import { Fase5FabricVisualizer } from './Fase5FabricVisualizer';
import { Fase5NonHomogeneousPolygon } from './Fase5NonHomogeneousPolygon';
import { Fase5InteractiveBarChart } from './Fase5InteractiveBarChart';
import { ContextualPercentageVisualizer } from './ContextualPercentageVisualizer';
import { FractionPercentageVisualizer } from './FractionPercentageVisualizer';
import { RatioGridVisualizer } from './RatioGridVisualizer';
import { CollectionGridVisualizer } from './CollectionGridVisualizer';
import { DataTableVisual, EquivalentFractionPuzzleVisual, FractionStripVisual, GroupCardsVisual, HundredGridVisual, RatioTableVisual } from './ReferenceMathVisuals';

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

export const getSemanticShape = (seedText: string): 'circle' | 'square' | 'pentagon' | 'hexagon' => {
  const lower = (seedText || '').toLowerCase();
  if (
    lower.includes('pizza') ||
    lower.includes('rueda') ||
    lower.includes('tarta') ||
    lower.includes('pastel circular') ||
    lower.includes('disco') ||
    lower.includes('reloj') ||
    lower.includes('pastel') ||
    lower.includes('torta')
  ) {
    return 'circle';
  }
  if (
    lower.includes('barra') ||
    lower.includes('chocolate') ||
    lower.includes('ventana') ||
    lower.includes('bandera') ||
    lower.includes('parcela') ||
    lower.includes('terreno') ||
    lower.includes('cinta') ||
    lower.includes('rectángulo') ||
    lower.includes('rectangulo') ||
    lower.includes('cuadrado') ||
    lower.includes('tabla')
  ) {
    return 'square';
  }
  if (lower.includes('pentágono') || lower.includes('pentagono')) {
    return 'pentagon';
  }
  if (lower.includes('hexágono') || lower.includes('hexagono')) {
    return 'hexagon';
  }
  return getDeterministicShape(seedText);
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
  pregunta: Fase5Pregunta;
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

export const Fase5VisualizerEngine: React.FC<Props> = ({
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
            shape={getSemanticShape(pregunta.enunciado)}
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
            <span className="text-2xl font-sans font-black tracking-wider block text-slate-200">Selecciona las partes necesarias</span>
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
    // En desafíos el nivel de ruta es 11/12/13, no el nivel pedagógico 1/2/3.
    // La representación de equivalencia se identifica por su propio contrato
    // de datos, nunca por el identificador de ruta; de otro modo una fracción
    // 2/6 caía en el dibujo por defecto de 8 sectores.
    if (pregunta.datos_numericos?.num_base !== undefined && pregunta.datos_numericos?.den_base !== undefined) {
      const num_base = pregunta.datos_numericos.num_base;
      const den_base = pregunta.datos_numericos.den_base;
      const factor = pregunta.datos_numericos.factor;
      const objetivo = pregunta.datos_numericos.objetivo_visual || 'término solicitado';
      const buscaDenominador = objetivo.toLowerCase().includes('denominador');
      return <EquivalentFractionPuzzleVisual
        left={{ numerador: num_base, denominador: den_base }}
        right={{
          numerador: buscaDenominador ? num_base * factor : null,
          denominador: buscaDenominador ? null : den_base * factor,
        }}
        objective={objetivo}
        color={moduleColor}
      />;
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
        shape={getSemanticShape(pregunta.enunciado)}
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
      <Fase5InteractiveBarChart
        valA={pregunta.datos_numericos?.val_a || 0}
        valB={pregunta.datos_numericos?.val_b || 0}
        valC={pregunta.datos_numericos?.val_c}
        categorias={pregunta.datos_numericos?.categorias}
        moduleColor={moduleColor}
      />
    );
  }

  if (tipoVisual === 'collection_grid') {
    return <CollectionGridVisualizer pregunta={pregunta} moduleColor={moduleColor} />;
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
      <Fase5FabricVisualizer
        datos_numericos={pregunta.datos_numericos}
        onStateChange={setVisualState || NOOP_STATE_CHANGE}
      />
    );
  }

  if (tipoVisual === 'non_homogeneous_polygon') {
    return (
      <Fase5NonHomogeneousPolygon
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

  if (tipoVisual === 'equivalence_strip') {
    return <EquivalentFractionPuzzleVisual
      left={pregunta.datos_numericos?.fraccion_izquierda || { numerador: null, denominador: null }}
      right={pregunta.datos_numericos?.fraccion_derecha || { numerador: null, denominador: null }}
      objective={pregunta.datos_numericos?.objetivo_visual}
      mode={pregunta.datos_numericos?.modo_visual}
      incorrectTerm={pregunta.datos_numericos?.termino_incorrecto}
      showCuts={!!pregunta.datos_numericos?.mostrar_cortes}
      color={moduleColor}
    />;
  }

  if (tipoVisual === 'fraction_strip') {
    return <FractionStripVisual
      numerator={pregunta.datos_numericos?.numerador || 0}
      denominator={pregunta.datos_numericos?.denominador || 1}
      color={moduleColor}
    />;
  }

  if (tipoVisual === 'group_cards') {
    return <GroupCardsVisual
      total={pregunta.datos_numericos?.total || 0}
      groups={pregunta.datos_numericos?.grupos || 1}
      highlighted={pregunta.datos_numericos?.grupos_destacados || 0}
      itemLabel={pregunta.datos_numericos?.etiqueta_elementos}
      color={moduleColor}
    />;
  }

  if (tipoVisual === 'hundred_grid') {
    return <HundredGridVisual
      percentage={pregunta.datos_numericos?.porcentaje || 0}
      total={pregunta.datos_numericos?.total || 0}
      color={moduleColor}
    />;
  }

  if (tipoVisual === 'data_table') {
    return <DataTableVisual
      values={pregunta.datos_numericos?.valores_tabla || []}
      labels={pregunta.datos_numericos?.etiquetas || []}
      color={moduleColor}
    />;
  }

  if (tipoVisual === 'ratio_table') {
    return <RatioTableVisual
      a={pregunta.datos_numericos?.ratio_a || 0}
      b={pregunta.datos_numericos?.ratio_b || 0}
      factor={pregunta.datos_numericos?.factor}
      total={pregunta.datos_numericos?.total}
      color={moduleColor}
    />;
  }

  console.warn(
    `Fase5VisualizerEngine: no hay visualizador para tipo_visual="${tipoVisual}" (modulo ${moduloId}, nivel ${nivelId}).`
  );
  return (
    <div className="text-center text-slate-400 text-sm italic py-8 select-none">
      Sin gráfico disponible para esta pregunta.
    </div>
  );
};
