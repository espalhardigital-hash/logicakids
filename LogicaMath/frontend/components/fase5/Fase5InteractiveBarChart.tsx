import React, { useState } from 'react';

interface Fase5InteractiveBarChartProps {
  valA: number;
  valB: number;
  categorias?: string[];
  moduleColor: string;
}

export const Fase5InteractiveBarChart: React.FC<Fase5InteractiveBarChartProps> = ({
  valA,
  valB,
  categorias = ["Estante A", "Estante B"],
  moduleColor,
}) => {
  const [selectedBar, setSelectedBar] = useState<'A' | 'B' | null>(null);

  const labelA = categorias[0] || "Barra A";
  const labelB = categorias[1] || "Barra B";

  // Determinar la escala máxima del eje Y
  const maxVal = Math.max(valA, valB);
  // Redondear al siguiente múltiplo de 50 o 100 para que la escala sea limpia
  const yScaleMax = maxVal <= 10 ? 10 : maxVal <= 50 ? 50 : maxVal <= 100 ? 100 : Math.ceil(maxVal / 100) * 100;
  const step = yScaleMax / 5;

  // Mapear un valor a la altura en el SVG
  // El eje Y en el SVG va desde Y=20 hasta Y=160 (140px de alto)
  const getBarGeometry = (value: number, index: number) => {
    const height = (value / yScaleMax) * 140;
    const y = 160 - height;
    const x = index === 0 ? 70 : 140;
    return { x, y, width: 35, height };
  };

  const geomA = getBarGeometry(valA, 0);
  const geomB = getBarGeometry(valB, 1);

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

  // Coordenadas de la línea de guía seleccionada
  const selectedGeom = selectedBar === 'A' ? geomA : selectedBar === 'B' ? geomB : null;
  const selectedVal = selectedBar === 'A' ? valA : selectedBar === 'B' ? valB : null;

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
        <line x1={40} y1={160} x2={215} y2={160} stroke="#94a3b8" strokeWidth="2" />
        <line x1={40} y1={20} x2={40} y2={160} stroke="#94a3b8" strokeWidth="2" />

        {/* Barra A */}
        <g
          onClick={(e) => {
            e.stopPropagation();
            setSelectedBar(selectedBar === 'A' ? null : 'A');
          }}
          className="transition-all duration-200"
        >
          {/* Sombra/Halo de selección */}
          <rect
            x={geomA.x - 4}
            y={geomA.y - 4}
            width={geomA.width + 8}
            height={geomA.height + 4}
            rx="6"
            fill="#a78bfa"
            fillOpacity={selectedBar === 'A' ? 0.25 : 0}
            className="transition-all duration-200"
          />
          {/* Barra real con gradiente */}
          <rect
            x={geomA.x}
            y={geomA.y}
            width={geomA.width}
            height={geomA.height}
            rx="4"
            fill="url(#gradA)"
            stroke="#a78bfa"
            strokeWidth={selectedBar === 'A' ? 2 : 1}
            className="hover:brightness-110 transition-all duration-200"
          />
          {/* Nombre de categoría Eje X */}
          <text
            x={geomA.x + geomA.width / 2}
            y={178}
            fontFamily="Arial"
            fontSize="9"
            fontWeight="black"
            fill={selectedBar === 'A' ? "#c084fc" : "#94a3b8"}
            textAnchor="middle"
          >
            {labelA}
          </text>
        </g>

        {/* Barra B */}
        <g
          onClick={(e) => {
            e.stopPropagation();
            setSelectedBar(selectedBar === 'B' ? null : 'B');
          }}
          className="transition-all duration-200"
        >
          {/* Sombra/Halo de selección */}
          <rect
            x={geomB.x - 4}
            y={geomB.y - 4}
            width={geomB.width + 8}
            height={geomB.height + 4}
            rx="6"
            fill="#f472b6"
            fillOpacity={selectedBar === 'B' ? 0.25 : 0}
            className="transition-all duration-200"
          />
          {/* Barra real con gradiente */}
          <rect
            x={geomB.x}
            y={geomB.y}
            width={geomB.width}
            height={geomB.height}
            rx="4"
            fill="url(#gradB)"
            stroke="#f472b6"
            strokeWidth={selectedBar === 'B' ? 2 : 1}
            className="hover:brightness-110 transition-all duration-200"
          />
          {/* Nombre de categoría Eje X */}
          <text
            x={geomB.x + geomB.width / 2}
            y={178}
            fontFamily="Arial"
            fontSize="9"
            fontWeight="black"
            fill={selectedBar === 'B' ? "#f472b6" : "#94a3b8"}
            textAnchor="middle"
          >
            {labelB}
          </text>
        </g>

        {/* Línea de guía de lectura horizontal (Discontinua) */}
        {selectedGeom && (
          <line
            x1={40}
            y1={selectedGeom.y}
            x2={selectedGeom.x}
            y2={selectedGeom.y}
            stroke={selectedBar === 'A' ? "#c084fc" : "#f472b6"}
            strokeWidth="1.5"
            strokeDasharray="4 3"
            strokeOpacity="0.8"
            className="animate-pulse"
          />
        )}

        {/* Definición de gradientes premium */}
        <defs>
          <linearGradient id="gradA" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#a78bfa" />
            <stop offset="100%" stopColor="#6d28d9" />
          </linearGradient>
          <linearGradient id="gradB" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#f472b6" />
            <stop offset="100%" stopColor="#be185d" />
          </linearGradient>
        </defs>
      </svg>

      {/* Tooltip de valor seleccionado en el panel inferior */}
      <div className="flex items-center justify-between w-full mt-3 min-h-[44px]">
        {selectedGeom && selectedVal !== null ? (
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-950/80 border border-slate-800 w-full justify-center animate-fade-in">
            <span className="text-slate-400 text-[10px] font-bold uppercase tracking-wider">
              {selectedBar === 'A' ? labelA : labelB}:
            </span>
            <span
              className="font-display text-base font-black"
              style={{ color: selectedBar === 'A' ? "#c084fc" : "#f472b6" }}
            >
              {selectedVal} unidades
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
