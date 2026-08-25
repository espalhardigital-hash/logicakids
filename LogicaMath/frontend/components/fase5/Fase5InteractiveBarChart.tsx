import React, { useState } from 'react';

interface Fase5InteractiveBarChartProps {
  valA: number;
  valB: number;
  valC?: number;
  categorias?: string[];
  moduleColor: string;
}

export const Fase5InteractiveBarChart: React.FC<Fase5InteractiveBarChartProps> = ({
  valA,
  valB,
  valC,
  categorias = ["Estante A", "Estante B"],
  moduleColor,
}) => {
  const [selectedBar, setSelectedBar] = useState<number | null>(null);

  const values = valC === undefined ? [valA, valB] : [valA, valB, valC];
  const labels = values.map((_, index) => categorias[index] || `Dato ${index + 1}`);
  const colors = ['#a78bfa', '#f472b6', '#38bdf8'];

  // Determinar la escala máxima del eje Y
  const maxVal = Math.max(...values);
  // Redondear al siguiente múltiplo de 50 o 100 para que la escala sea limpia
  const yScaleMax = maxVal <= 10 ? 10 : maxVal <= 50 ? 50 : maxVal <= 100 ? 100 : Math.ceil(maxVal / 100) * 100;
  const step = yScaleMax / 5;

  // Mapear un valor a la altura en el SVG
  // El eje Y en el SVG va desde Y=20 hasta Y=160 (140px de alto)
  const getBarGeometry = (value: number, index: number) => {
    const height = (value / yScaleMax) * 140;
    const y = 160 - height;
    const x = values.length === 3 ? 58 + index * 54 : 70 + index * 70;
    return { x, y, width: 35, height };
  };

  const geometries = values.map(getBarGeometry);

  // Líneas de cuadrícula horizontales
  const gridLines = [];
  for (let i = 0; i <= 5; i++) {
    const val = i * step;
    const y = 160 - (val / yScaleMax) * 140;
    gridLines.push(
      <g key={`grid-${i}`}>
        {/* Línea horizontal */}
        <line x1={40} y1={y} x2={210} y2={y} stroke="#334155" strokeWidth="1" strokeOpacity="0.4" strokeDasharray={i === 0 ? "none" : "3 3"} />
        {/* Etiqueta del valor en el eje Y */}
        <text x={30} y={y + 3} fontFamily="Arial" fontSize="9" fontWeight="bold" fill="#94a3b8" textAnchor="end">
          {val}
        </text>
      </g>
    );
  }

  return (
    <div className="flex flex-col items-center w-full max-w-[340px] mx-auto p-4 bg-slate-900/60 backdrop-blur-md rounded-3xl border border-slate-700/50 shadow-2xl animate-fade-in">
      <div className="text-center mb-2">
        <span className="text-slate-400 text-xs font-bold uppercase tracking-widest">Visualizador de Datos</span>
      </div>

      {/* Contenedor SVG del Gráfico de Barras */}
      <svg
        viewBox="0 0 240 200"
        width="100%"
        height="100%"
        xmlns="http://www.w3.org/2000/svg"
        className="select-none cursor-pointer rounded-2xl bg-slate-950/80 border border-slate-800 p-2"
        onClick={() => setSelectedBar(null)}
      >
        {/* Cuadrícula Horizontal */}
        {gridLines}

        {/* Ejes principales */}
        <line x1={40} y1={160} x2={220} y2={160} stroke="#94a3b8" strokeWidth="2" />
        <line x1={40} y1={20} x2={40} y2={160} stroke="#94a3b8" strokeWidth="2" />

        {geometries.map((geom, index) => <g key={labels[index]} onClick={(event) => { event.stopPropagation(); setSelectedBar(selectedBar === index ? null : index); }} className="transition-all duration-200">
          <rect x={geom.x - 4} y={geom.y - 4} width={geom.width + 8} height={geom.height + 4} rx="6" fill={colors[index]} fillOpacity={selectedBar === index ? 0.25 : 0} />
          <rect x={geom.x} y={geom.y} width={geom.width} height={geom.height} rx="4" fill={colors[index]} fillOpacity="0.9" stroke={colors[index]} strokeWidth={selectedBar === index ? 2 : 1} className="hover:brightness-110 transition-all duration-200" />
          <text x={geom.x + geom.width / 2} y={178} fontFamily="Arial" fontSize="9" fontWeight="black" fill={selectedBar === index ? colors[index] : "#94a3b8"} textAnchor="middle">{labels[index]}</text>
        </g>)}

        {/* Línea de guía de lectura horizontal (Discontinua) */}
        {selectedBar !== null && (
          <line
            x1={40}
            y1={geometries[selectedBar].y}
            x2={geometries[selectedBar].x}
            y2={geometries[selectedBar].y}
            stroke={colors[selectedBar]}
            strokeWidth="1.5"
            strokeDasharray="4 3"
            strokeOpacity="0.8"
            className="animate-pulse"
          />
        )}

      </svg>

      {/* Tooltip de valor seleccionado en el panel inferior */}
      <div className="flex items-center justify-between w-full mt-3 min-h-[44px]">
        {selectedBar !== null ? (
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-950/80 border border-slate-800 w-full justify-center animate-fade-in">
            <span className="text-slate-400 text-[10px] font-bold uppercase tracking-wider">
              {labels[selectedBar]}:
            </span>
            <span
              className="font-display text-base font-black"
              style={{ color: colors[selectedBar] }}
            >
              {values[selectedBar]} unidades
            </span>
          </div>
        ) : (
          <div className="text-center text-slate-500 text-xs w-full py-2">
            Haz clic en una barra para leer su valor exacto
          </div>
        )}
      </div>
    </div>
  );
};
