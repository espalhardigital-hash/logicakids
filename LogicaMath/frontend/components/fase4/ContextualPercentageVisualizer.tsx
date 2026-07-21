import React from 'react';

interface Props {
  pct: number; // Porcentaje fijo de la pregunta (ej. 75)
  total: number; // Valor total de la capacidad (ej. 600)
  inputValue: string; // Lo que el alumno está escribiendo (ej. "450")
  theme: 'battery' | 'download' | 'tank';
  unit?: string; // Unidad de medida (ej. "min", "MB", "L", "USD")
  color?: string; // Color de acento
}

export const ContextualPercentageVisualizer: React.FC<Props> = ({
  pct,
  total,
  inputValue = '',
  theme,
  unit = 'min',
  color = '#10b981',
}) => {
  const numericVal = parseFloat(inputValue);
  const displayValue = isNaN(numericVal) ? '—' : numericVal.toString();

  // Determinar color de relleno según porcentaje para baterías, o usar el color de acento
  let fillColor = color;
  if (theme === 'battery') {
    if (pct <= 10) fillColor = '#ef4444'; // Rojo bajo
    else if (pct <= 20) fillColor = '#eab308'; // Amarillo/naranja bajo
    else fillColor = '#0d9488'; // Teal/verde batería estándar
  } else if (theme === 'download') {
    fillColor = '#3b82f6'; // Azul de descarga estándar
  } else if (theme === 'tank') {
    fillColor = '#0284c7'; // Azul agua para tanque
  }

  // Estilos comunes para paneles
  return (
    <div className="flex flex-col items-center justify-center w-full p-4 bg-slate-950/20 border border-white/5 rounded-[2rem] shadow-2xl">
      <div className="flex flex-row items-stretch w-full max-w-md bg-[#0b1b19] border-2 border-[#1c3d3a] rounded-2xl overflow-hidden shadow-lg min-h-[140px]">
        
        {/* PANEL IZQUIERDO: El gráfico del tema + indicador de estado */}
        <div className="flex-1 flex flex-col items-center justify-center p-4 bg-black/40 relative">
          {theme === 'battery' && (
            <div className="flex flex-col items-center w-full">
              {/* Contenedor de la batería */}
              <div className="relative w-44 h-16 border-4 border-white/30 rounded-xl p-1 flex items-center justify-start bg-black/50 shadow-inner">
                {/* Relleno de la batería */}
                <div
                  style={{
                    width: `${pct}%`,
                    backgroundColor: fillColor,
                    boxShadow: `0 0 12px ${fillColor}aa`,
                    transition: 'width 0.8s cubic-bezier(0.25, 1, 0.5, 1)',
                  }}
                  className="h-full rounded-md flex items-center justify-center relative overflow-hidden min-w-[5%]"
                >
                  <span className="text-white text-base font-black tracking-tight select-none">
                    {pct}%
                  </span>
                </div>
                {/* Cap de la batería (pestaña del polo positivo en el extremo derecho) */}
                <div className="absolute -right-3.5 top-1/2 -translate-y-1/2 w-2.5 h-6 bg-white/30 border-y-4 border-r-4 border-white/30 rounded-r-md" />
              </div>

              {/* Indicador de valor restante */}
              <div className="mt-3 flex items-center gap-2">
                <span className="px-3 py-1 bg-slate-900 border border-white/10 rounded-md text-white font-black text-sm min-w-[32px] text-center">
                  {displayValue}
                </span>
                <span className="text-slate-400 text-xs font-bold">
                  {unit} restantes
                </span>
              </div>
            </div>
          )}

          {theme === 'download' && (
            <div className="flex flex-col items-center w-full">
              {/* Contenedor de barra de descarga */}
              <div className="relative w-44 h-8 bg-slate-900 border-2 border-white/20 rounded-full overflow-hidden p-0.5 shadow-inner">
                <div
                  style={{
                    width: `${pct}%`,
                    backgroundColor: fillColor,
                    boxShadow: `0 0 10px ${fillColor}88`,
                    transition: 'width 0.8s cubic-bezier(0.25, 1, 0.5, 1)',
                  }}
                  className="h-full rounded-full flex items-center justify-center relative min-w-[5%]"
                >
                  <span className="text-white text-xs font-black select-none">
                    {pct}%
                  </span>
                </div>
              </div>

              {/* Indicador de MB descargados */}
              <div className="mt-3 flex items-center gap-2">
                <span className="px-3 py-1 bg-slate-900 border border-white/10 rounded-md text-white font-black text-sm min-w-[32px] text-center">
                  {displayValue}
                </span>
                <span className="text-slate-400 text-xs font-bold">
                  {unit} descargados
                </span>
              </div>
            </div>
          )}

          {theme === 'tank' && (
            <div className="flex flex-col items-center w-full">
              {/* Tanque de líquido vertical */}
              <div className="relative w-16 h-28 border-4 border-white/30 rounded-b-xl rounded-t-sm bg-black/40 overflow-hidden flex flex-col justify-end p-0.5 shadow-inner">
                {/* Líquido */}
                <div
                  style={{
                    height: `${pct}%`,
                    backgroundColor: fillColor,
                    boxShadow: `inset 0 4px 6px rgba(255,255,255,0.2), 0 0 15px ${fillColor}66`,
                    transition: 'height 0.8s cubic-bezier(0.25, 1, 0.5, 1)',
                  }}
                  className="w-full rounded-b-md relative min-h-[5%]"
                >
                  <div className="absolute inset-0 flex items-center justify-center">
                    <span className="text-white text-xs font-black select-none drop-shadow">
                      {pct}%
                    </span>
                  </div>
                </div>
              </div>

              {/* Indicador de volumen restante */}
              <div className="mt-3 flex items-center gap-2">
                <span className="px-3 py-1 bg-slate-900 border border-white/10 rounded-md text-white font-black text-sm min-w-[32px] text-center">
                  {displayValue}
                </span>
                <span className="text-slate-400 text-xs font-bold">
                  {unit} de líquido
                </span>
              </div>
            </div>
          )}
        </div>

        {/* PANEL DERECHO: Capacidad total / Meta */}
        <div 
          className="w-36 flex flex-col items-center justify-center p-4 border-l border-[#1c3d3a]"
          style={{ backgroundColor: `${fillColor}1a` }}
        >
          <span className="text-2xl font-black text-white tracking-tight">
            {total} <span className="text-sm font-bold text-slate-300">{unit}</span>
          </span>
          <span className="text-[10px] font-black tracking-wider text-slate-400 uppercase text-center mt-1 select-none">
            {theme === 'battery' && 'al estar lleno'}
            {theme === 'download' && 'tamaño total'}
            {theme === 'tank' && 'capacidad máxima'}
          </span>
        </div>

      </div>
    </div>
  );
};
