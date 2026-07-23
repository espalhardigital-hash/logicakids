import React from 'react';
import { Target, BookOpen, Trophy, RotateCcw, Star } from 'lucide-react';

export const NumberCell: React.FC<{ value: number; min: number; max: number; step?: number; onChange: (v: number) => void; className?: string }> = ({
  value, min, max, step = 1, onChange, className = ''
}) => (
  <input
    type="number"
    value={value}
    min={min}
    max={max}
    step={step}
    onChange={(e) => {
      if (e.target.value === '') return;
      let val = parseInt(e.target.value);
      if (isNaN(val)) return;
      if (val > max) val = max;
      if (val < min) val = min;
      onChange(val);
    }}
    className={`w-16 text-center bg-white dark:bg-slate-900 border border-slate-200 dark:border-white/10 rounded-lg py-1.5 text-sm font-black text-slate-900 dark:text-white focus:outline-none focus:border-blue-500/50 ${className}`}
  />
);

interface ConfigGridRowProps {
  seccion: number;
  label: string;
  kind: 'level' | 'challenge' | 'final';
  questionsCount: number;
  passingScore: number;
  useTimer: boolean;
  timer: number;
  feedbackType: string;
  hasOwnRecord: boolean;
  onChangeQuestions: (v: number) => void;
  onChangePassing: (v: number) => void;
  onToggleTimer: () => void;
  onChangeTimer: (v: number) => void;
  onChangeFeedback: (ft: 'simple' | 'detallado') => void;
  onRevert: () => void;
}

export const ConfigGridRow: React.FC<ConfigGridRowProps> = ({
  label, kind, questionsCount, passingScore, useTimer, timer, feedbackType, hasOwnRecord,
  onChangeQuestions, onChangePassing, onToggleTimer, onChangeTimer, onChangeFeedback, onRevert
}) => {
  const Icon = kind === 'level' ? BookOpen : kind === 'final' ? Trophy : Target;
  const iconColor = kind === 'level' ? 'text-blue-500' : 'text-amber-500';

  return (
    <tr className="hover:bg-slate-50 dark:hover:bg-white/5 transition-colors">
      <td className="py-2.5 pl-2">
        <span className="flex items-center gap-2 text-xs font-bold text-slate-700 dark:text-slate-200">
          <Icon size={13} className={`${iconColor} shrink-0`} />
          {label}
        </span>
      </td>
      <td className="text-center">
        <NumberCell value={questionsCount} min={5} max={120} step={5} onChange={onChangeQuestions} />
      </td>
      <td className="text-center">
        <NumberCell value={passingScore} min={50} max={100} step={5} onChange={onChangePassing} />
      </td>
      <td className="text-center">
        <button type="button" onClick={onToggleTimer}>
          <div className={`ios-switch ${useTimer ? 'ios-switch-active' : ''}`}>
            <div className="ios-switch-knob" />
          </div>
        </button>
      </td>
      <td className="text-center">
        <NumberCell value={timer} min={3} max={600} step={5} className={!useTimer ? 'opacity-40' : ''} onChange={onChangeTimer} />
      </td>
      <td className="text-center">
        {kind === 'level' ? (
          <div className="inline-flex rounded-lg overflow-hidden border border-slate-200 dark:border-white/10">
            {(['simple', 'detallado'] as const).map(ft => (
              <button
                type="button"
                key={ft}
                onClick={() => onChangeFeedback(ft)}
                className={`px-2 py-1 text-[10px] font-black uppercase transition-colors ${
                  feedbackType === ft ? 'bg-purple-600 text-white' : 'bg-white dark:bg-slate-900 text-slate-500 dark:text-slate-400'
                }`}
              >
                {ft === 'simple' ? 'S' : 'IA'}
              </button>
            ))}
          </div>
        ) : (
          <span className="text-slate-300 dark:text-slate-600 text-xs">—</span>
        )}
      </td>
      <td className="text-right pr-2">
        {hasOwnRecord ? (
          <button
            type="button"
            onClick={onRevert}
            title="Revertir a la regla heredada"
            className="inline-flex items-center gap-1 text-[10px] font-black text-amber-600 dark:text-amber-400 hover:text-amber-500"
          >
            <Star size={12} /> <RotateCcw size={12} />
          </button>
        ) : (
          <span className="text-[10px] text-slate-300 dark:text-slate-600">heredado</span>
        )}
      </td>
    </tr>
  );
};

export const ConfigGridHeader: React.FC = () => (
  <thead>
    <tr className="text-[10px] uppercase tracking-wider text-slate-400 font-black">
      <th className="pb-2 pl-2 text-left">Nivel / Desafío</th>
      <th className="pb-2 text-center">Preguntas</th>
      <th className="pb-2 text-center">Aprob. %</th>
      <th className="pb-2 text-center">Cronómetro</th>
      <th className="pb-2 text-center">Tiempo (s)</th>
      <th className="pb-2 text-center">Feedback</th>
      <th className="pb-2 pr-2 text-right">Regla</th>
    </tr>
  </thead>
);
