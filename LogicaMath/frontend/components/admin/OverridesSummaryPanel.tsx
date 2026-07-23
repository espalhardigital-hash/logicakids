import React, { useState } from 'react';
import { ChevronDown, ChevronUp, ListChecks, RotateCcw } from 'lucide-react';
import { ConfiguracionProgreso } from '../../types';
import { StaticPhase, findRowBySeccion } from './pedagogyHelpers';

interface OverridesSummaryPanelProps {
  draftModularConfigs: ConfiguracionProgreso[];
  staticPhases: StaticPhase[];
  onRemoveOverride: (faseId: number, seccion: number, operacion: string) => void;
  onSelectNode: (faseId: number, seccion: number, operacion: string) => void;
}

export const OverridesSummaryPanel: React.FC<OverridesSummaryPanelProps> = ({
  draftModularConfigs, staticPhases, onRemoveOverride, onSelectNode
}) => {
  const [open, setOpen] = useState(false);
  const activeOverrides = draftModularConfigs.filter(c => c.activo !== false);

  const getFriendlyName = (config: ConfiguracionProgreso) => {
    const phase = staticPhases.find(p => p.id === config.fase_id);
    if (!phase) return { phaseName: `Fase ${config.fase_id}`, sectionName: `Sección ${config.seccion}` };
    if (config.seccion === 0) return { phaseName: phase.name.split(':')[0], sectionName: 'Parámetros por defecto de Fase' };
    const found = findRowBySeccion(phase, config.seccion);
    if (!found) return { phaseName: phase.name.split(':')[0], sectionName: `Sección ${config.seccion}` };
    return { phaseName: phase.name.split(':')[0], sectionName: `${found.mod.name.split(':')[0]} - ${found.row.label}` };
  };

  return (
    <div className="bg-white dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-3xl overflow-hidden">
      <button
        type="button"
        onClick={() => setOpen(v => !v)}
        className="w-full flex items-center justify-between px-6 py-4 text-left hover:bg-slate-50 dark:hover:bg-white/5 transition-colors"
      >
        <span className="flex items-center gap-2 text-sm font-black text-slate-900 dark:text-white">
          <ListChecks size={16} className="text-blue-500" />
          Reglas especiales activas
          <span className="text-[10px] font-black px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-500">{activeOverrides.length}</span>
        </span>
        {open ? <ChevronUp size={16} className="text-slate-400" /> : <ChevronDown size={16} className="text-slate-400" />}
      </button>

      {open && (
        <div className="px-6 pb-6">
          {activeOverrides.length === 0 ? (
            <p className="text-xs text-slate-500 dark:text-slate-400 py-4 text-center">
              Sin reglas particulares. Todo el flujo pedagógico se rige por la Plataforma Global.
            </p>
          ) : (
            <div className="overflow-x-auto custom-scrollbar">
              <table className="w-full text-left border-collapse text-xs">
                <thead>
                  <tr className="border-b border-slate-200 dark:border-white/10 text-slate-400 font-bold uppercase tracking-wider">
                    <th className="pb-2">Fase</th>
                    <th className="pb-2">Módulo / Nivel</th>
                    <th className="pb-2 text-center">Ejercicios</th>
                    <th className="pb-2 text-center">Aprobación</th>
                    <th className="pb-2 text-center">Cronómetro</th>
                    <th className="pb-2 text-right">Acciones</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-white/5">
                  {activeOverrides.map((config, idx) => {
                    const { phaseName, sectionName } = getFriendlyName(config);
                    return (
                      <tr key={idx} className="hover:bg-slate-50 dark:hover:bg-white/5 transition-colors font-medium text-slate-700 dark:text-slate-300">
                        <td className="py-2.5 font-black text-slate-900 dark:text-white max-w-[120px] truncate">{phaseName}</td>
                        <td className="py-2.5 max-w-[220px] truncate">{sectionName}</td>
                        <td className="py-2.5 text-center font-bold text-blue-500">{config.cantidad_requerida}</td>
                        <td className="py-2.5 text-center font-bold text-green-500">{config.porcentaje_aprobacion}%</td>
                        <td className="py-2.5 text-center">
                          {config.usa_cronometro ? (
                            <span className="px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-500 font-bold">{config.tiempo_default_segundos ?? 12}s</span>
                          ) : (
                            <span className="text-slate-400 dark:text-slate-600">-</span>
                          )}
                        </td>
                        <td className="py-2.5 text-right">
                          <div className="flex justify-end gap-2">
                            <button
                              type="button"
                              onClick={() => onSelectNode(config.fase_id, config.seccion, config.operacion)}
                              className="px-2.5 py-1 bg-blue-500/10 hover:bg-blue-500 hover:text-white text-blue-500 rounded-lg transition-all font-bold"
                            >
                              Ver
                            </button>
                            <button
                              type="button"
                              onClick={() => onRemoveOverride(config.fase_id, config.seccion, config.operacion)}
                              title="Revertir a heredado"
                              className="p-1 text-slate-400 hover:text-amber-500 transition-colors"
                            >
                              <RotateCcw size={14} />
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
