import React from 'react';

interface SliderProps {
  value: number;
  min: number;
  max: number;
  step?: number;
  onChange: (val: number) => void;
  disabled?: boolean;
  accentColor: string;
  unit?: string;
  isThermal?: boolean;
}

export const SliderWithTooltip: React.FC<SliderProps> = ({
  value, min, max, step = 1, onChange, disabled = false, accentColor, unit = '', isThermal = false
}) => {
  const percentage = ((value - min) / (max - min)) * 100;

  const getThermalColor = () => {
    if (percentage < 25) return 'bg-rose-500 shadow-[0_0_15px_rgba(244,63,94,0.5)]';
    if (percentage < 50) return 'bg-orange-500 shadow-[0_0_15px_rgba(249,115,22,0.5)]';
    if (percentage < 75) return 'bg-amber-400 shadow-[0_0_15px_rgba(251,191,36,0.5)]';
    return 'bg-emerald-500 shadow-[0_0_15px_rgba(16,185,129,0.5)]';
  };

  const activeColor = isThermal ? getThermalColor() : accentColor;

  return (
    <div className="flex items-center gap-4 w-full">
      <div className="relative flex-1 group pt-2 select-none">
        <div
          className="absolute -top-3 transform -translate-x-1/2 pointer-events-none transition-all duration-100 z-10"
          style={{ left: `${percentage}%` }}
        >
          <div className="glass-panel border border-slate-300 dark:border-white/20 text-slate-900 dark:text-white font-black text-sm px-2 py-0.5 rounded shadow-xl whitespace-nowrap">
            {value}{unit}
            <div className="absolute top-full left-1/2 -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-slate-900"></div>
          </div>
        </div>

        <div className="relative w-full h-2 bg-white/80 dark:bg-slate-800/80 rounded-full overflow-hidden">
          <div
            className={`absolute top-0 left-0 h-full rounded-full transition-all duration-150 ${disabled ? 'bg-slate-600' : activeColor}`}
            style={{ width: `${percentage}%` }}
          />
          <div
            className={`absolute top-1/2 -translate-y-1/2 w-4 h-4 -ml-2 rounded-full border-2 border-white bg-white/80 dark:bg-slate-950 shadow-[0_0_8px_rgba(0,0,0,0.5)] pointer-events-none z-20 transition-transform ${disabled ? 'scale-75 opacity-55' : 'group-hover:scale-110'}`}
            style={{ left: `${percentage}%` }}
          />
        </div>

        <input
          type="range"
          min={min}
          max={max}
          step={step}
          value={value}
          onChange={(e) => onChange(parseInt(e.target.value))}
          disabled={disabled}
          className="absolute top-2 left-0 w-full h-2 opacity-0 cursor-pointer disabled:cursor-not-allowed z-30"
        />
      </div>

      <div className="relative shrink-0 flex items-center bg-white dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-xl overflow-hidden transition-all focus-within:border-blue-500/50">
        <button
          type="button"
          onClick={() => {
            let newVal = value - (step || 1);
            if (newVal < min) newVal = min;
            onChange(newVal);
          }}
          disabled={disabled || value <= min}
          className="w-8 h-9 flex items-center justify-center text-slate-500 hover:bg-slate-100 dark:hover:bg-white/10 disabled:opacity-30 transition-colors"
        >
          -
        </button>
        <input
          type="number"
          min={min}
          max={max}
          step={step}
          value={value}
          onChange={(e) => {
            if (e.target.value === '') return;
            let val = parseInt(e.target.value);
            if (isNaN(val)) return;
            if (val > max) val = max;
            onChange(val);
          }}
          onBlur={(e) => {
            let val = parseInt(e.target.value);
            if (isNaN(val) || val < min) {
              onChange(min);
            }
          }}
          disabled={disabled}
          className="w-14 bg-transparent text-center text-slate-900 dark:text-white text-sm font-black focus:outline-none disabled:opacity-50 appearance-none"
          style={{ MozAppearance: 'textfield' }}
        />
        <button
          type="button"
          onClick={() => {
            let newVal = value + (step || 1);
            if (newVal > max) newVal = max;
            onChange(newVal);
          }}
          disabled={disabled || value >= max}
          className="w-8 h-9 flex items-center justify-center text-slate-500 hover:bg-slate-100 dark:hover:bg-white/10 disabled:opacity-30 transition-colors"
        >
          +
        </button>
      </div>
    </div>
  );
};
