import React from 'react';
import { NonHomogeneousSector } from './Fase5Types';

interface Fase5NonHomogeneousPolygonProps {
  sectors: NonHomogeneousSector[];
  viewBox?: string;
  selectedIds: number[];
  onToggleSector: (id: number) => void;
  accentColor: string; // Color de acento del módulo (ej: "#A855F7")
  targetFractionText: string; // ej: "1/2" o "50%"
  onReset: () => void;
}

export const Fase5NonHomogeneousPolygon: React.FC<Fase5NonHomogeneousPolygonProps> = ({
  sectors,
  viewBox = "0 0 100 100",
  selectedIds,
  onToggleSector,
  accentColor,
  targetFractionText,
  onReset
}) => {
  // Sumar los pesos de los sectores seleccionados actualmente
  const selectedWeightSum = sectors
    .filter(s => selectedIds.includes(s.id))
    .reduce((sum, s) => sum + s.weight, 0);

  const isPercentage = targetFractionText.includes('%');

  return (
    <div className="flex flex-col items-center justify-center w-full">
      {/* Contenedor principal de la figura */}
      <div className="relative p-6 bg-slate-900/40 border border-white/5 rounded-[2.5rem] shadow-2xl flex items-center justify-center min-h-[300px] w-full max-w-md">
        <svg
          viewBox={viewBox}
          className="w-64 h-64 md:w-72 md:h-72 filter drop-shadow-[0_10px_15px_rgba(0,0,0,0.5)] select-none"
        >
          {sectors.map((sector) => {
            const isSelected = selectedIds.includes(sector.id);
            return (
              <polygon
                key={sector.id}
                points={sector.points}
                onClick={() => onToggleSector(sector.id)}
                style={{
                  fill: isSelected ? accentColor : '#27272a',
                  transition: 'fill 0.2s ease-in-out, opacity 0.2s ease-in-out'
                }}
                className="stroke-white stroke-[1.5] cursor-pointer hover:opacity-80"
              />
            );
          })}
        </svg>
      </div>

      {/* Panel inferior de control e información */}
      <div className="mt-4 flex flex-row items-center justify-between gap-4 w-full max-w-md px-4">
        {/* Pill de progreso acumulado */}
        <div 
          className="px-6 py-2 bg-slate-950/60 border border-white/10 rounded-full font-sans font-black tracking-wider text-center shadow-lg flex items-center gap-2"
        >
          <span className="text-slate-400 text-xs font-black tracking-[0.1em] uppercase">Objetivo:</span>
          <span style={{ color: accentColor }} className="text-xl font-black">
            {targetFractionText}
          </span>
        </div>

        {/* Botón de Reiniciar selección */}
        <button
          onClick={onReset}
          className="px-5 py-2 bg-zinc-800 hover:bg-zinc-700 active:scale-95 text-slate-200 text-xs font-black tracking-widest rounded-full uppercase border border-zinc-700 transition-all duration-150 cursor-pointer shadow-md"
        >
          Reiniciar
        </button>
      </div>
    </div>
  );
};

export default Fase5NonHomogeneousPolygon;
