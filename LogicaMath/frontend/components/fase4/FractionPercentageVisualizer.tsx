import React, { useState, useEffect } from 'react';

interface Props {
  percentage: number; // e.g. 25
  total: number; // e.g. 80
  color: string;
  interactive?: boolean;
  
  // Binding to parent state if the question's final answer is the fraction itself
  respuestaNum?: string;
  respuestaDen?: string;
  setRespuestaNum?: (val: string) => void;
  setRespuestaDen?: (val: string) => void;
}

export const FractionPercentageVisualizer: React.FC<Props> = ({
  percentage,
  total,
  color,
  interactive = true,
  respuestaNum = '',
  respuestaDen = '',
  setRespuestaNum,
  setRespuestaDen,
}) => {
  // Internal state for selected fraction
  const [num, setNum] = useState<number | null>(
    respuestaNum && !isNaN(Number(respuestaNum)) ? Number(respuestaNum) : null
  );
  const [den, setDen] = useState<number | null>(
    respuestaDen && !isNaN(Number(respuestaDen)) ? Number(respuestaDen) : null
  );
  const [activeSlot, setActiveSlot] = useState<'num' | 'den'>('num');
  const [isCorrect, setIsCorrect] = useState(false);

  // Available numbers for the bank (1-10)
  const numberBank = [1, 2, 3, 4, 5, 6, 8, 10];

  // Calculate target fraction values (e.g. 25% -> 1/4)
  useEffect(() => {
    if (num !== null && den !== null && den > 0) {
      const currentVal = num / den;
      const targetVal = percentage / 100;
      // Allow floating point tolerance
      const correct = Math.abs(currentVal - targetVal) < 0.001;
      setIsCorrect(correct);

      // If correct, or if we want to sync whatever they wrote, propagate up
      if (setRespuestaNum && setRespuestaDen) {
        setRespuestaNum(num.toString());
        setRespuestaDen(den.toString());
      }
    } else {
      setIsCorrect(false);
    }
  }, [num, den, percentage, setRespuestaNum, setRespuestaDen]);

  const handleNumberClick = (val: number) => {
    if (!interactive) return;

    if (activeSlot === 'num') {
      setNum(val);
      setActiveSlot('den');
    } else {
      setDen(val);
      setActiveSlot('num');
    }
  };

  const handleSlotClick = (slot: 'num' | 'den') => {
    if (!interactive) return;
    setActiveSlot(slot);
    if (slot === 'num') setNum(null);
    if (slot === 'den') setDen(null);
  };

  const segments = den || 1;
  const filledSegments = num || 0;

  return (
    <div className="flex flex-col items-center justify-center gap-6 w-full select-none font-sans">
      {/* 1D Progress Bar Visualizer */}
      <div className="w-full max-w-md flex flex-col gap-2">
        <div className="flex justify-between text-slate-400 text-xs font-black tracking-widest px-1">
          <span>0%</span>
          <span>{total} (100%)</span>
        </div>
        <div 
          className="h-12 w-full bg-slate-950 rounded-2xl flex overflow-hidden border-2 shadow-inner transition-all duration-300"
          style={{ borderColor: isCorrect ? color : 'rgba(255, 255, 255, 0.1)' }}
        >
          {Array.from({ length: segments }).map((_, i) => (
            <div
              key={i}
              className="h-full flex-1 border-r border-slate-900/60 last:border-r-0 transition-all duration-500"
              style={{
                backgroundColor: i < filledSegments ? color : 'transparent',
                opacity: i < filledSegments ? 0.85 : 0.2,
              }}
            />
          ))}
        </div>
      </div>

      {/* Equation Block */}
      <div 
        className="flex flex-col items-center p-4 sm:p-6 bg-slate-900/40 border rounded-3xl transition-all duration-500 w-full max-w-md relative"
        style={{ borderColor: isCorrect ? `${color}60` : 'rgba(255, 255, 255, 0.05)', boxShadow: isCorrect ? `0 0 25px ${color}15` : 'none' }}
      >
        <div className="flex flex-col items-center justify-center gap-4 text-white text-lg sm:text-xl font-bold w-full">
          <div className="text-slate-300 font-sans tracking-wide text-base sm:text-lg text-center whitespace-nowrap">
            {percentage && percentage > 0 ? `${percentage}% de ${total} =` : `Fracción de ${total} =`}
          </div>

          <div className="flex flex-row flex-wrap items-center justify-center gap-3 sm:gap-4">
            {/* Fraction Input Slots */}
            <div className="flex flex-col items-center gap-1">
            <button
              onClick={() => handleSlotClick('num')}
              disabled={!interactive}
              className={`w-10 h-10 sm:w-12 sm:h-12 rounded-xl flex items-center justify-center text-xl sm:text-2xl font-black transition-all ${
                activeSlot === 'num'
                  ? 'bg-slate-800 border-2 scale-105 text-white'
                  : num !== null
                  ? 'bg-slate-900 border text-slate-200'
                  : 'bg-slate-950 border border-dashed border-slate-700 text-slate-500'
              }`}
              style={{ borderColor: activeSlot === 'num' ? color : 'rgba(255, 255, 255, 0.1)' }}
            >
              {num !== null ? num : '?'}
            </button>
            <div className="w-8 sm:w-10 h-0.5 bg-slate-500 rounded-full" />
            <button
              onClick={() => handleSlotClick('den')}
              disabled={!interactive}
              className={`w-10 h-10 sm:w-12 sm:h-12 rounded-xl flex items-center justify-center text-xl sm:text-2xl font-black transition-all ${
                activeSlot === 'den'
                  ? 'bg-slate-800 border-2 scale-105 text-white'
                  : den !== null
                  ? 'bg-slate-900 border text-slate-200'
                  : 'bg-slate-950 border border-dashed border-slate-700 text-slate-500'
              }`}
              style={{ borderColor: activeSlot === 'den' ? color : 'rgba(255, 255, 255, 0.1)' }}
            >
              {den !== null ? den : '?'}
            </button>
          </div>

          <span className="text-slate-300 font-sans tracking-wide text-base sm:text-lg">
            × {total}
          </span>
          </div>
        </div>

        {/* Bloques visuales (Puntos) */}
        {den !== null && den > 0 && total % den === 0 && (
          <div className="mt-8 mb-2 w-full flex flex-wrap justify-center gap-4">
            {Array.from({ length: den }).map((_, boxIdx) => {
              const isSelected = num !== null && boxIdx < num;
              const dotsCount = total / den;
              return (
                <div 
                  key={boxIdx}
                  className="flex flex-wrap gap-1.5 p-3 rounded-xl border-2 transition-all duration-300 items-center justify-center min-w-[3rem]"
                  style={{
                    borderColor: isSelected ? color : 'rgba(255, 255, 255, 0.1)',
                    backgroundColor: isSelected ? `${color}10` : 'rgba(15, 23, 42, 0.3)',
                    boxShadow: isSelected ? `0 0 10px ${color}20` : 'none'
                  }}
                >
                  {Array.from({ length: dotsCount }).map((_, dotIdx) => (
                    <div 
                      key={dotIdx}
                      className="w-3 h-3 rounded-full transition-all duration-300"
                      style={{
                        backgroundColor: isSelected ? color : 'rgba(255, 255, 255, 0.2)'
                      }}
                    />
                  ))}
                </div>
              );
            })}
          </div>
        )}

        {/* Number Bank */}
        {interactive && (
          <div className="mt-6 flex flex-wrap gap-2 justify-center w-full">
            {numberBank.map((val) => (
              <button
                key={val}
                onClick={() => handleNumberClick(val)}
                className="w-10 h-10 rounded-xl bg-slate-900 hover:bg-slate-800 border border-white/10 text-white text-lg font-black transition-all active:scale-90"
                style={isCorrect ? { borderColor: color, color } : {}}
              >
                {val}
              </button>
            ))}
          </div>
        )}

        {isCorrect && (
          <div 
            className="absolute -top-3 -right-3 w-8 h-8 rounded-full flex items-center justify-center text-white text-lg animate-bounce"
            style={{ backgroundColor: color }}
          >
            ✓
          </div>
        )}
      </div>
    </div>
  );
};
