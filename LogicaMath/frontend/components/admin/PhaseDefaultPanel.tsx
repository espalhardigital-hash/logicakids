import React from 'react';
import { RotateCcw, Star, Settings2, Target } from 'lucide-react';
import { SliderWithTooltip } from './SliderWithTooltip';
import { ConfigGridRow, ConfigGridHeader } from './ConfigGridRow';
import { ConfiguracionProgreso } from '../../types';
import { CHALLENGE_ORDER_SECCIONES, FINAL_EXAM_SECCION } from './pedagogyHelpers';

interface PhaseDefaultPanelProps {
  faseId: number;
  faseName: string;
  faseDescription: string;

  // Niveles (seccion 0): un único valor que cascada a todos los niveles de la fase.
  record: ConfiguracionProgreso | null;
  inheritedQuestionsCount: number;
  inheritedPassingScore: number;
  inheritedUseTimer: boolean;
  inheritedTimer: number;
  inheritedFeedbackType: string;
  onUpdateField: (field: keyof ConfiguracionProgreso, val: any) => void;
  onRevert: () => void;

  // Desafíos (Desafío 1/2/Final de cada módulo) + Examen Final de Fase: una fila por
  // cada uno, cada una cascadea de forma independiente a todos los módulos de la fase.
  draftModularConfigs: ConfiguracionProgreso[];
  getInheritedQuestionsCount: (isChallenge: boolean, subId: number) => number;
  getInheritedPassingScore: (isChallenge: boolean, subId: number) => number;
  getInheritedUseTimer: (isChallenge: boolean, subId: number) => boolean;
  getInheritedTimer: (isChallenge: boolean, subId: number) => number;
  onUpdateChallengeRowField: (seccion: number, operacion: string, isChallenge: boolean, subId: number, field: keyof ConfiguracionProgreso, val: any) => void;
  onRevertChallengeRow: (seccion: number, operacion: string) => void;
}

const CHALLENGE_DEFAULT_ROWS = [
  { seccion: CHALLENGE_ORDER_SECCIONES[11], subId: 11, label: 'Desafío 1 (Estándar) · todos los módulos' },
  { seccion: CHALLENGE_ORDER_SECCIONES[12], subId: 12, label: 'Desafío 2 (Avanzado) · todos los módulos' },
  { seccion: CHALLENGE_ORDER_SECCIONES[13], subId: 13, label: 'Desafío Final (Maestría) · todos los módulos' },
  { seccion: FINAL_EXAM_SECCION, subId: 99, label: '🏆 Examen Final de Fase', kind: 'final' as const },
];

export const PhaseDefaultPanel: React.FC<PhaseDefaultPanelProps> = ({
  faseId, faseName, faseDescription, record,
  inheritedQuestionsCount, inheritedPassingScore, inheritedUseTimer, inheritedTimer, inheritedFeedbackType,
  onUpdateField, onRevert,
  draftModularConfigs,
  getInheritedQuestionsCount = () => 0,
  getInheritedPassingScore = () => 0,
  getInheritedUseTimer = () => false,
  getInheritedTimer = () => 0,
  onUpdateChallengeRowField, onRevertChallengeRow
}) => {
  const hasOverride = record !== null;

  const questionsCount = record?.cantidad_requerida ?? inheritedQuestionsCount;
  const passingScore = record?.porcentaje_aprobacion ?? inheritedPassingScore;
  const useTimer = record?.usa_cronometro ?? inheritedUseTimer;
  const timer = record?.tiempo_default_segundos ?? inheritedTimer;
  const feedbackType = record?.tipo_feedback ?? inheritedFeedbackType;

  const findChallengeRecord = (seccion: number) => {
    const rec = draftModularConfigs.find(c => c.fase_id === faseId && c.seccion === seccion && c.operacion === 'mixta');
    return rec && rec.activo !== false ? rec : null;
  };

  return (
    <div className="flex flex-col gap-4">
      <div className="bg-white dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-3xl p-6 flex flex-col gap-6">
        <div className="flex items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <Settings2 size={18} className="text-blue-500" />
            <div>
              <h3 className="text-base font-black text-slate-900 dark:text-white">{faseName}</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 max-w-xl">{faseDescription}</p>
            </div>
          </div>

          {hasOverride ? (
            <button
              type="button"
              onClick={onRevert}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-[11px] font-black uppercase tracking-wider bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/20 hover:bg-amber-500/20 transition-colors shrink-0"
            >
              <Star size={12} /> Regla propia · <RotateCcw size={12} /> Revertir
            </button>
          ) : (
            <span className="text-[11px] font-black uppercase tracking-wider text-slate-400 dark:text-slate-500 shrink-0">
              Heredando de Plataforma Global
            </span>
          )}
        </div>

        <p className="text-xs text-slate-500 dark:text-slate-400 -mt-3">
          Niveles (práctica libre). Se aplica a todos los niveles de todos los módulos de la fase que no tengan su propia regla.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="flex flex-col gap-5">
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <label className="text-sm text-slate-600 dark:text-slate-300 font-bold">Volumen de Ejercicios</label>
                <span className="text-base font-black text-blue-500">{questionsCount}</span>
              </div>
              <SliderWithTooltip
                value={questionsCount}
                min={10} max={120} step={5}
                onChange={(val) => onUpdateField('cantidad_requerida', val)}
                accentColor="bg-blue-500"
              />
            </div>

            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <label className="text-sm text-slate-600 dark:text-slate-300 font-bold">Porcentaje de Aprobación</label>
                <span className="text-base font-black text-green-500">{passingScore}%</span>
              </div>
              <SliderWithTooltip
                value={passingScore}
                min={50} max={100} step={5}
                onChange={(val) => onUpdateField('porcentaje_aprobacion', val)}
                accentColor="bg-green-500" unit="%"
              />
            </div>
          </div>

          <div className="bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-white/10 p-5 rounded-2xl flex flex-col gap-4">
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm text-slate-600 dark:text-slate-300 font-bold">Habilitar Cronómetro</label>
                <p className="text-[10px] text-slate-500">Límite de tiempo activo.</p>
              </div>
              <button type="button" onClick={() => onUpdateField('usa_cronometro', !useTimer)}>
                <div className={`ios-switch ${useTimer ? 'ios-switch-active' : ''}`}>
                  <div className="ios-switch-knob" />
                </div>
              </button>
            </div>

            {useTimer && (
              <div className="space-y-2 pt-3 border-t border-slate-200 dark:border-white/10">
                <div className="flex justify-between items-center">
                  <label className="text-xs text-slate-500 dark:text-slate-400 font-bold">Límite por Pregunta</label>
                  <span className="text-base font-black text-amber-500">{timer}s</span>
                </div>
                <SliderWithTooltip
                  value={timer}
                  min={3} max={3600} step={5}
                  onChange={(val) => onUpdateField('tiempo_default_segundos', val)}
                  accentColor="bg-amber-500" unit="s" isThermal
                />
              </div>
            )}

            <div className="space-y-2 pt-3 border-t border-slate-200 dark:border-white/10">
              <label className="text-xs text-slate-500 dark:text-slate-400 font-bold">Tipo de Feedback</label>
              <div className="flex gap-2">
                {(['simple', 'detallado'] as const).map((ft) => (
                  <button
                    type="button"
                    key={ft}
                    onClick={() => onUpdateField('tipo_feedback', ft)}
                    className={`flex-1 py-2 rounded-xl border text-[10px] uppercase tracking-wider font-black transition-all ${
                      feedbackType === ft
                        ? 'bg-purple-600 border-purple-500 text-white'
                        : 'bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400'
                    }`}
                  >
                    {ft === 'simple' ? 'Simple (✔/✘)' : 'Tutoría IA'}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-3xl p-6 flex flex-col gap-4">
        <div className="flex items-center gap-2">
          <Target size={18} className="text-amber-500" />
          <div>
            <h3 className="text-base font-black text-slate-900 dark:text-white">Desafíos de la fase</h3>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Cada fila cascadea de forma independiente al Desafío correspondiente de todos los módulos de la fase, y al Examen Final de Fase.
            </p>
          </div>
        </div>

        <div className="overflow-x-auto custom-scrollbar">
          <table className="w-full text-left border-collapse">
            <ConfigGridHeader />
            <tbody className="divide-y divide-slate-100 dark:divide-white/5">
              {CHALLENGE_DEFAULT_ROWS.map(row => {
                const rec = findChallengeRecord(row.seccion);
                const questionsCount = rec?.cantidad_requerida ?? getInheritedQuestionsCount(true, row.subId);
                const passingScore = rec?.porcentaje_aprobacion ?? getInheritedPassingScore(true, row.subId);
                const useTimer = rec?.usa_cronometro ?? getInheritedUseTimer(true, row.subId);
                const timer = rec?.tiempo_default_segundos ?? getInheritedTimer(true, row.subId);

                return (
                  <ConfigGridRow
                    key={row.seccion}
                    seccion={row.seccion}
                    label={row.label}
                    kind={row.kind ?? 'challenge'}
                    questionsCount={questionsCount}
                    passingScore={passingScore}
                    useTimer={useTimer}
                    timer={timer}
                    feedbackType="simple"
                    hasOwnRecord={rec !== null}
                    onChangeQuestions={(v) => onUpdateChallengeRowField(row.seccion, 'mixta', true, row.subId, 'cantidad_requerida', v)}
                    onChangePassing={(v) => onUpdateChallengeRowField(row.seccion, 'mixta', true, row.subId, 'porcentaje_aprobacion', v)}
                    onToggleTimer={() => onUpdateChallengeRowField(row.seccion, 'mixta', true, row.subId, 'usa_cronometro', !useTimer)}
                    onChangeTimer={(v) => onUpdateChallengeRowField(row.seccion, 'mixta', true, row.subId, 'tiempo_default_segundos', v)}
                    onChangeFeedback={() => {}}
                    onRevert={() => onRevertChallengeRow(row.seccion, 'mixta')}
                  />
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
