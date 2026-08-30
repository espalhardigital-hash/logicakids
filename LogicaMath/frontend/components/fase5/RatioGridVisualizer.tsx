import React from 'react';
import type { Fase5Pregunta } from './Fase5Types';

interface Props {
  pregunta: Fase5Pregunta;
  moduleColor: string;
}

const getRatioTheme = (enunciado: string) => {
  const text = (enunciado || '').toLowerCase();
  
  if (text.includes('batido') || text.includes('frutilla') || text.includes('fruta') || text.includes('jugo') || text.includes('jarabe')) {
    return {
      labelA: 'Fruta',
      colorA: '#f43f5e', // Rosa Fresa
      labelB: text.includes('agua') ? 'Agua' : 'Leche',
      colorB: text.includes('agua') ? '#38bdf8' : '#f8fafc', // Celeste o Blanco
    };
  }
  if (text.includes('plastilina') || text.includes('slime') || text.includes('escarcha')) {
    return {
      labelA: text.includes('escarcha') ? 'Escarcha' : 'Plastilina A',
      colorA: '#c084fc', // Violeta brillante
      labelB: text.includes('líquida') || text.includes('liquida') ? 'Base' : 'Plastilina B',
      colorB: '#2dd4bf', // Turquesa
    };
  }
  if (text.includes('limon') || text.includes('limonada') || text.includes('refresco')) {
    return {
      labelA: 'Limón',
      colorA: '#fbbf24', // Amarillo
      labelB: 'Agua',
      colorB: '#60a5fa', // Azul
    };
  }
  if (text.includes('pintura') || text.includes('témpera') || text.includes('tempera') || text.includes('mural') || text.includes('verde') || text.includes('rosa')) {
    let labelA = 'Témpera A';
    let colorA = '#ef4444'; // Rojo por defecto
    let labelB = 'Témpera B';
    let colorB = '#f1f5f9'; // Blanco por defecto
    
    if (text.includes('amarilla') || text.includes('amarillo')) {
      labelA = 'Amarillo';
      colorA = '#fbbf24';
    }
    if (text.includes('azul')) {
      labelB = 'Azul';
      colorB = '#3b82f6';
    }
    if (text.includes('rojo') || text.includes('roja')) {
      labelA = 'Rojo';
      colorA = '#ef4444';
    }
    if (text.includes('blanco') || text.includes('blanca')) {
      labelB = 'Blanco';
      colorB = '#f8fafc';
    }
    return { labelA, colorA, labelB, colorB };
  }
  if (text.includes('galleta') || text.includes('harina') || text.includes('azúcar') || text.includes('azucar') || text.includes('masa')) {
    return {
      labelA: text.includes('leche') ? 'Leche' : 'Azúcar',
      colorA: '#fb923c', // Naranja suave
      labelB: 'Harina',
      colorB: '#f1f5f9', // Blanco harina
    };
  }
  if (text.includes('ficha') || text.includes('amigo') || text.includes('premio') || text.includes('punto')) {
    return {
      labelA: 'Parte A',
      colorA: '#a855f7', // Púrpura
      labelB: 'Parte B',
      colorB: '#38bdf8', // Celeste
    };
  }
  if (text.includes('arcilla')) {
    return {
      labelA: 'Agua',
      colorA: '#3b82f6',
      labelB: 'Arcilla',
      colorB: '#c2410c', // Terracota
    };
  }
  if (text.includes('cemento') || text.includes('arena')) {
    return {
      labelA: 'Cemento',
      colorA: '#475569',
      labelB: 'Arena',
      colorB: '#ca8a04',
    };
  }
  
  // Fallback amigable
  return {
    labelA: 'Ingrediente A',
    colorA: '#c084fc',
    labelB: 'Ingrediente B',
    colorB: '#34d399',
  };
};

export const RatioGridVisualizer: React.FC<Props> = ({ pregunta, moduleColor }) => {
  const data = pregunta.datos_numericos || {};
  // El backend entrega ratio_a/ratio_b. Conservamos val_a/val_b solo para
  // preguntas antiguas mientras se reconstruye el banco local.
  const ratioA = Math.max(1, Number(data.ratio_a ?? data.val_a ?? 1));
  const ratioB = Math.max(1, Number(data.ratio_b ?? data.val_b ?? 1));
  const factor = Number(data.factor || 1);
  const { labelA, colorA, labelB, colorB } = getRatioTheme(pregunta.enunciado);

  const baseA = ratioA;
  const baseB = ratioB;
  const hasScaledRecipe = factor > 1;

  const renderBlocks = (countA: number, countB: number) => {
    const total = countA + countB;
    return (
      <div className="flex flex-wrap gap-2 justify-center max-w-[220px] p-2 bg-slate-950/60 rounded-xl border border-slate-800 min-h-[60px] items-center">
        {Array.from({ length: countA }).map((_, i) => (
          <div
            key={`a-${i}`}
            className="w-5 h-5 rounded-md shadow-md shadow-black/20 border border-white/10 animate-bounce"
            style={{ 
              backgroundColor: colorA,
              animationDelay: `${i * 100}ms`,
              animationDuration: '2s'
            }}
          />
        ))}
        {Array.from({ length: countB }).map((_, i) => (
          <div
            key={`b-${i}`}
            className="w-5 h-5 rounded-md shadow-md shadow-black/20 border border-white/10 animate-bounce"
            style={{ 
              backgroundColor: colorB,
              animationDelay: `${(countA + i) * 100}ms`,
              animationDuration: '2s'
            }}
          />
        ))}
      </div>
    );
  };

  return (
    <div className="flex flex-col items-center w-full max-w-[555px] mx-auto mt-4 p-4 bg-slate-900/60 backdrop-blur-md rounded-2xl border border-slate-700/50 shadow-lg select-none">
      <div className="flex justify-around items-stretch w-full gap-4">
        {/* Receta Base */}
        <div className="flex flex-col items-center gap-2 flex-1">
          <span style={{ color: moduleColor }} className="text-xs font-black uppercase tracking-wider">
            Razón ({baseA}:{baseB})
          </span>
          {renderBlocks(baseA, baseB)}
        </div>

        {/* Separador */}
        {hasScaledRecipe && <div className="flex items-center justify-center text-3xl font-black text-slate-600">➔</div>}

        {/* Objetivo proporcional: se conserva la incógnita, nunca se dibuja
            el resultado que el estudiante debe obtener. */}
        {hasScaledRecipe && <div className="flex flex-col items-center justify-center gap-3 flex-1 rounded-xl border border-purple-400/25 bg-purple-500/5 p-4">
          <span className="text-xs font-black uppercase tracking-wider text-purple-300">
            Escalar ×{factor}
          </span>
          <span className="text-sm font-black text-slate-100">{labelA}: {baseA} × {factor} = ?</span>
          <span className="text-sm font-black text-slate-100">{labelB}: {baseB} × {factor} = ?</span>
          <span className="text-[10px] font-bold text-slate-400">Calcula la cantidad solicitada.</span>
        </div>}
      </div>

      {/* Leyenda explicativa al pie */}
      <div className="flex justify-center gap-6 mt-4 pt-3 border-t border-slate-800/80 w-full text-[10px] font-bold text-slate-400">
        <div className="flex items-center gap-1.5">
          <div className="w-3.5 h-3.5 rounded-sm border border-white/5" style={{ backgroundColor: colorA }} />
          <span>{labelA}: {baseA}</span>
        </div>
        <div className="flex items-center gap-1.5">
          <div className="w-3.5 h-3.5 rounded-sm border border-white/5" style={{ backgroundColor: colorB }} />
          <span>{labelB}: {baseB}</span>
        </div>
      </div>
    </div>
  );
};
