import React, { useState } from 'react';
import { BookOpen, Trophy, ArrowDownToLine } from 'lucide-react';
import { ConfiguracionProgreso } from '../../types';
import { StaticModule, getModuleRows } from './pedagogyHelpers';
import { ConfigGridRow, ConfigGridHeader, NumberCell } from './ConfigGridRow';

interface ModuleGridPanelProps {
  faseId: number;
  mod: StaticModule;
  draftModularConfigs: ConfiguracionProgreso[];
  getInheritedQuestionsCount: (isChallenge: boolean, subId: number) => number;
  getInheritedPassingScore: (isChallenge: boolean, subId: number) => number;
  getInheritedUseTimer: (isChallenge: boolean, subId: number) => boolean;
  getInheritedFeedbackType: (isChallenge: boolean, subId: number) => string;
  getInheritedTimer: (isChallenge: boolean, subId: number) => number;
  onUpdateRowField: (seccion: number, operacion: string, isChallenge: boolean, subId: number, field: keyof ConfiguracionProgreso, val: any) => void;
  onRevertRow: (seccion: number, operacion: string) => void;
  onApplyToAll: (values: { cantidad_requerida: number; porcentaje_aprobacion: number; usa_cronometro: boolean; tiempo_default_segundos: number }) => void;
}

export const ModuleGridPanel: React.FC<ModuleGridPanelProps> = ({
  faseId, mod, draftModularConfigs,
  getInheritedQuestionsCount, getInheritedPassingScore, getInheritedUseTimer, getInheritedFeedbackType, getInheritedTimer,
  onUpdateRowField, onRevertRow, onApplyToAll
}) => {
  const rows = getModuleRows(faseId, mod);
  const isSingleRow = rows.length === 1;

  const [applyQty, setApplyQty] = useState(15);
  const [applyPct, setApplyPct] = useState(80);
  const [applyTimer, setApplyTimer] = useState(false);
  const [applyTime, setApplyTime] = useState(30);

  const findRecord = (seccion: number, operacion: string) => {
    const rec = draftModularConfigs.find(c => c.fase_id === faseId && c.seccion === seccion && c.operacion === operacion);
    return rec && rec.activo !== false ? rec : null;
  };

  return (
    <div className="bg-white dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-3xl p-6 flex flex-col gap-5">
      <div className="flex items-center gap-2">
        {mod.isFinalExam ? <Trophy size={18} className="text-amber-500" /> : <BookOpen size={18} className="text-blue-500" />}
        <div>
          <h3 className="text-base font-black text-slate-900 dark:text-white">{mod.name}</h3>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            {isSingleRow ? 'Reglas del examen final de la fase.' : 'Editá todos los niveles y desafíos del módulo. Cada fila con estrella tiene su propia regla.'}
          </p>
        </div>
      </div>

      {!isSingleRow && (
        <div className="flex flex-wrap items-center gap-3 bg-blue-500/5 border border-blue-500/20 rounded-2xl px-4 py-3">
          <span className="text-xs font-black text-blue-600 dark:text-blue-400 flex items-center gap-1.5 shrink-0">
            <ArrowDownToLine size={14} /> Aplicar a todas las filas
          </span>
          <div className="flex items-center gap-1.5">
            <label className="text-[10px] text-slate-500 font-bold">Preguntas</label>
            <NumberCell value={applyQty} min={5} max={120} step={5} onChange={setApplyQty} />
          </div>
          <div className="flex items-center gap-1.5">
            <label className="text-[10px] text-slate-500 font-bold">Aprob. %</label>
            <NumberCell value={applyPct} min={50} max={100} step={5} onChange={setApplyPct} />
          </div>
          <div className="flex items-center gap-1.5">
            <label className="text-[10px] text-slate-500 font-bold">Cronómetro</label>
            <button type="button" onClick={() => setApplyTimer(v => !v)}>
              <div className={`ios-switch ${applyTimer ? 'ios-switch-active' : ''}`}>
                <div className="ios-switch-knob" />
              </div>
            </button>
          </div>
          <div className="flex items-center gap-1.5">
            <label className="text-[10px] text-slate-500 font-bold">Tiempo s</label>
            <NumberCell value={applyTime} min={3} max={600} step={5} onChange={setApplyTime} className={!applyTimer ? 'opacity-40' : ''} />
          </div>
          <button
            type="button"
            onClick={() => onApplyToAll({ cantidad_requerida: applyQty, porcentaje_aprobacion: applyPct, usa_cronometro: applyTimer, tiempo_default_segundos: applyTime })}
            className="ml-auto px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-black transition-colors"
          >
            Aplicar a las {rows.length} filas
          </button>
        </div>
      )}

      <div className="overflow-x-auto custom-scrollbar">
        <table className="w-full text-left border-collapse">
          <ConfigGridHeader />
          <tbody className="divide-y divide-slate-100 dark:divide-white/5">
            {rows.map(row => {
              const record = findRecord(row.seccion, row.operacion);
              const questionsCount = record?.cantidad_requerida ?? getInheritedQuestionsCount(row.isChallenge, row.subId);
              const passingScore = record?.porcentaje_aprobacion ?? getInheritedPassingScore(row.isChallenge, row.subId);
              const useTimer = record?.usa_cronometro ?? getInheritedUseTimer(row.isChallenge, row.subId);
              const timer = record?.tiempo_default_segundos ?? getInheritedTimer(row.isChallenge, row.subId);
              const feedbackType = record?.tipo_feedback ?? getInheritedFeedbackType(row.isChallenge, row.subId);

              return (
                <ConfigGridRow
                  key={row.seccion}
                  seccion={row.seccion}
                  label={row.label}
                  kind={row.kind}
                  questionsCount={questionsCount}
                  passingScore={passingScore}
                  useTimer={useTimer}
                  timer={timer}
                  feedbackType={feedbackType}
                  hasOwnRecord={record !== null}
                  onChangeQuestions={(v) => onUpdateRowField(row.seccion, row.operacion, row.isChallenge, row.subId, 'cantidad_requerida', v)}
                  onChangePassing={(v) => onUpdateRowField(row.seccion, row.operacion, row.isChallenge, row.subId, 'porcentaje_aprobacion', v)}
                  onToggleTimer={() => onUpdateRowField(row.seccion, row.operacion, row.isChallenge, row.subId, 'usa_cronometro', !useTimer)}
                  onChangeTimer={(v) => onUpdateRowField(row.seccion, row.operacion, row.isChallenge, row.subId, 'tiempo_default_segundos', v)}
                  onChangeFeedback={(ft) => onUpdateRowField(row.seccion, row.operacion, row.isChallenge, row.subId, 'tipo_feedback', ft)}
                  onRevert={() => onRevertRow(row.seccion, row.operacion)}
                />
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
