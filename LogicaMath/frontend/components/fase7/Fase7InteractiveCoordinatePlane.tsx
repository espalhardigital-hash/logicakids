import React, { useState, useEffect, useRef } from 'react';

interface Fase7InteractiveCoordinatePlaneProps {
  initialX: number;
  initialY: number;
  targetX?: number;
  targetY?: number;
  onChange: (x: number, y: number) => void;
  moduleColor: string;
}

export const Fase7InteractiveCoordinatePlane: React.FC<Fase7InteractiveCoordinatePlaneProps> = ({
  initialX,
  initialY,
  targetX,
  targetY,
  onChange,
  moduleColor,
}) => {
  const [currentX, setCurrentX] = useState<number>(initialX);
  const [currentY, setCurrentY] = useState<number>(initialY);
  const [isDragging, setIsDragging] = useState<boolean>(false);
  const svgRef = useRef<SVGSVGElement | null>(null);

  useEffect(() => {
    setCurrentX(initialX);
    setCurrentY(initialY);
  }, [initialX, initialY]);

  // Convertir coordenadas del cliente (mouse/touch) a coordenadas del plano (0 a 6)
  const handlePointerEvent = (clientX: number, clientY: number) => {
    if (!svgRef.current) return;
    const rect = svgRef.current.getBoundingClientRect();
    
    // Obtener la posición relativa en porcentaje del SVG
    const relativeX = (clientX - rect.left) / rect.width;
    const relativeY = (clientY - rect.top) / rect.height;

    // Convertir a unidades del viewBox (0 a 210)
    const svgX = relativeX * 210;
    const svgY = relativeY * 210;

    // Convertir de coordenadas SVG a unidades del plano cartesiano (0 a 6)
    // Origen en (30, 180), espaciado de 25 píxeles por unidad
    const planeX = (svgX - 30) / 25;
    const planeY = (180 - svgY) / 25;

    // Aplicar grid snapping y limitar al rango [0, 6]
    const snapX = Math.max(0, Math.min(6, Math.round(planeX)));
    const snapY = Math.max(0, Math.min(6, Math.round(planeY)));

    if (snapX !== currentX || snapY !== currentY) {
      setCurrentX(snapX);
      setCurrentY(snapY);
      onChange(snapX, snapY);
    }
  };

  const handleMouseDown = (e: React.MouseEvent<SVGSVGElement>) => {
    setIsDragging(true);
    handlePointerEvent(e.clientX, e.clientY);
  };

  const handleMouseMove = (e: React.MouseEvent<SVGSVGElement>) => {
    if (!isDragging) return;
    handlePointerEvent(e.clientX, e.clientY);
  };

  const handleMouseUpOrLeave = () => {
    setIsDragging(false);
  };

  const handleTouchStart = (e: React.TouchEvent<SVGSVGElement>) => {
    setIsDragging(true);
    if (e.touches.length > 0) {
      handlePointerEvent(e.touches[0].clientX, e.touches[0].clientY);
    }
  };

  const handleTouchMove = (e: React.TouchEvent<SVGSVGElement>) => {
    if (!isDragging) return;
    if (e.touches.length > 0) {
      handlePointerEvent(e.touches[0].clientX, e.touches[0].clientY);
    }
  };

  const handleTouchEnd = () => {
    setIsDragging(false);
  };

  const handleReset = () => {
    setCurrentX(initialX);
    setCurrentY(initialY);
    onChange(initialX, initialY);
  };

  // Convertir coordenadas del plano a coordenadas de píxeles del SVG
  const getSvgCoords = (x: number, y: number) => {
    return {
      cx: 30 + x * 25,
      cy: 180 - y * 25,
    };
  };

  const currentPos = getSvgCoords(currentX, currentY);
  const startPos = getSvgCoords(initialX, initialY);
  const targetPos = targetX !== undefined && targetY !== undefined ? getSvgCoords(targetX, targetY) : null;

  // Generar líneas de cuadrícula
  const gridLines = [];
  for (let i = 0; i <= 6; i++) {
    const cx = 30 + i * 25;
    const cy = 180 - i * 25;

    // Líneas verticales e indicadores X
    gridLines.push(
      <line key={`v-${i}`} x1={cx} y1={20} x2={cx} y2={180} stroke="#334155" strokeWidth="1" strokeOpacity="0.5" />
    );
    gridLines.push(
      <text key={`tx-${i}`} x={cx} y={195} fontFamily="Arial" fontSize="9" fill="#94a3b8" textAnchor="middle" fontWeight="bold">
        {i}
      </text>
    );

    // Líneas horizontales e indicadores Y
    gridLines.push(
      <line key={`h-${i}`} x1={30} y1={cy} x2={180} y2={cy} stroke="#334155" strokeWidth="1" strokeOpacity="0.5" />
    );
    gridLines.push(
      <text key={`ty-${i}`} x={20} y={cy + 3} fontFamily="Arial" fontSize="9" fill="#94a3b8" textAnchor="end" fontWeight="bold">
        {i}
      </text>
    );
  }

  return (
    <div className="flex flex-col items-center w-full max-w-[340px] mx-auto p-4 bg-slate-900/60 backdrop-blur-md rounded-3xl border border-slate-700/50 shadow-2xl animate-fade-in">
      {/* Contenedor SVG Interactivo */}
      <svg
        ref={svgRef}
        viewBox="0 0 210 210"
        width="100%"
        height="100%"
        xmlns="http://www.w3.org/2000/svg"
        className="select-none cursor-pointer rounded-2xl bg-slate-950/80 border border-slate-800"
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUpOrLeave}
        onMouseLeave={handleMouseUpOrLeave}
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
      >
        {/* Cuadrícula */}
        {gridLines}

        {/* Eje X e Y */}
        <line x1={30} y1={180} x2={185} y2={180} stroke="#94a3b8" strokeWidth="2" />
        <line x1={30} y1={20} x2={30} y2={180} stroke="#94a3b8" strokeWidth="2" />
        
        {/* Flecha Eje X */}
        <path d="M 185 177 L 190 180 L 185 183 Z" fill="#94a3b8" />
        <text x="195" y="184" fontFamily="Arial" fontSize="10" fontWeight="black" fill="#94a3b8">X</text>

        {/* Flecha Eje Y */}
        <path d="M 27 20 L 30 15 L 33 20 Z" fill="#94a3b8" />
        <text x="26" y="11" fontFamily="Arial" fontSize="10" fontWeight="black" fill="#94a3b8">Y</text>

        {/* Trayectoria discontinua si se ha movido */}
        {(currentX !== initialX || currentY !== initialY) && (
          <path
            d={`M ${startPos.cx} ${startPos.cy} L ${currentPos.cx} ${startPos.cy} L ${currentPos.cx} ${currentPos.cy}`}
            fill="none"
            stroke={moduleColor}
            strokeWidth="2"
            strokeDasharray="4 4"
            strokeOpacity="0.7"
          />
        )}

        {/* Punto de Inicio (A) fijo original */}
        <circle cx={startPos.cx} cy={startPos.cy} r="5" fill="#64748b" stroke="#f8fafc" strokeWidth="1" />
        <text x={startPos.cx} y={startPos.cy - 8} fontFamily="Arial" fontSize="8" fontWeight="bold" fill="#94a3b8" textAnchor="middle">A</text>

        {/* Punto Objetivo (B) si existe y es diferente al actual */}
        {targetPos && (currentX !== targetX || currentY !== targetY) && (
          <>
            <circle cx={targetPos.cx} cy={targetPos.cy} r="6" fill="#ef4444" stroke="#f8fafc" strokeWidth="1" strokeOpacity="0.4" />
            <text x={targetPos.cx} y={targetPos.cy - 9} fontFamily="Arial" fontSize="8" fontWeight="bold" fill="#ef4444" textAnchor="middle" fillOpacity="0.6">B</text>
          </>
        )}

        {/* Punto Interactivo (Arrastrable / Seleccionado) */}
        <g className="transition-transform duration-75">
          {/* Halo pulsante de interacción */}
          <circle
            cx={currentPos.cx}
            cy={currentPos.cy}
            r="12"
            fill={moduleColor}
            fillOpacity={isDragging ? 0.35 : 0.15}
            className="animate-pulse"
          />
          <circle
            cx={currentPos.cx}
            cy={currentPos.cy}
            r="6"
            fill={moduleColor}
            stroke="#f8fafc"
            strokeWidth="1.5"
          />
          {/* Checkmark verde si coincide con el objetivo */}
          {targetX !== undefined && targetY !== undefined && currentX === targetX && currentY === targetY && (
            <path
              d={`M ${currentPos.cx - 3} ${currentPos.cy} L ${currentPos.cx - 1} ${currentPos.cy + 2} L ${currentPos.cx + 3} ${currentPos.cy - 2}`}
              fill="none"
              stroke="#22c55e"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          )}
        </g>
      </svg>

      {/* Panel de estado y reinicio */}
      <div className="flex items-center justify-between w-full mt-4">
        {/* Indicador de Coordenada */}
        <div className="flex items-center gap-2 px-4 py-2 rounded-2xl bg-slate-950/80 border border-slate-800">
          <span className="text-slate-400 text-xs font-semibold uppercase tracking-wider">Punto:</span>
          <span className="font-display text-lg font-black text-white" style={{ color: moduleColor }}>
            ({currentX}, {currentY})
          </span>
        </div>

        {/* Botón Reiniciar */}
        {(currentX !== initialX || currentY !== initialY) && (
          <button
            onClick={handleReset}
            className="px-4 py-2 rounded-2xl font-display text-xs font-bold text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 active:scale-95 transition-all border border-slate-700/50"
          >
            Reiniciar
          </button>
        )}
      </div>
    </div>
  );
};
