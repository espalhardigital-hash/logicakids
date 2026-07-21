import React from 'react';
import { ToggleRight, AlertCircle, RefreshCw } from 'lucide-react';
import { ConfiguracionProgreso } from '../../types';

interface ProgressConfigTableProps {
  draftModularConfigs: ConfiguracionProgreso[];
  staticPhases: any[];
  onRemoveOverride: (faseId: number, seccion: number, operacion: string) => void;
  onSelectNode: (faseId: number, seccion: number, operacion: string) => void;
}

export const ProgressConfigTable: React.FC<ProgressConfigTableProps> = ({
  draftModularConfigs, staticPhases, onRemoveOverride, onSelectNode
}) => {
  const activeOverrides = draftModularConfigs.filter(c => c.activo !== false);

  const getFriendlyName = (config: ConfiguracionProgreso) => {
    const phase = staticPhases.find(p => p.id === config.fase_id);
    if (!phase) return { phaseName: `Fase ${config.fase_id}`, sectionName: `Sección ${config.seccion}` };
    
    if (config.seccion === 0) {
      return { phaseName: phase.name, sectionName: 'Parámetros por defecto de Fase' };
    }

    // Search module
    for (const mod of phase.modules) {
      const modId = mod.modulo_id || 1;
      
      // Check final exam
      if (mod.isFinalExam && config.seccion === 99099) {
        return { phaseName: phase.name, sectionName: `${mod.name} (Graduación)` };
      }
      
      // Try to find matching level
      const level = mod.levels?.find((l: any) => {
        const levelSeccion = config.fase_id >= 5 
          ? config.fase_id * 1000 + modId * 10 + l.id
          : modId * 100 + l.id;
        return levelSeccion === config.seccion;
      });
      
      if (level) {
        return { phaseName: phase.name, sectionName: `${mod.name.split(':')[0]} - Nivel ${level.id}: ${level.name}` };
      }

      // Try to find matching challenge
      const challenge = mod.challenges?.find((c: any) => {
        const challengeSeccion = config.fase_id >= 5
          ? config.fase_id * 10000 + modId * 100 + c.id
          : modId * 1000 + c.id;
        return challengeSeccion === config.seccion;
      });

      if (challenge) {
        return { phaseName: phase.name, sectionName: `${mod.name.split(':')[0]} - ${challenge.name}` };
      }
    }

    return { phaseName: phase.name, sectionName: `Sección ID ${config.seccion}` };
  };

  return (
    <div className="bg-white dark:bg-white/5 backdrop-blur-2xl border border-slate-200 dark:border-white/10 p-6 lg:p-8 rounded-[2.5rem] shadow-2xl flex flex-col gap-6 w-full">
      <div>
        <h3 className="text-2xl font-black text-slate-900 dark:text-white">Resumen de Reglas Especiales</h3>
        <p className="text-slate-500 dark:text-slate-400 text-xs mt-1">
          Módulos y fases con configuraciones exclusivas activas (sobrescriben las reglas globales).
        </p>
      </div>

      {activeOverrides.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-12 text-center border-2 border-dashed border-slate-200 dark:border-white/10 rounded-3xl bg-slate-50/50 dark:bg-white/5 p-6">
          <AlertCircle className="text-slate-400 mb-3" size={32} />
          <h4 className="text-base font-bold text-slate-700 dark:text-slate-350">Heredando 100% de la Plataforma Global</h4>
          <p className="text-xs text-slate-500 max-w-sm mt-1">
            No se han definido reglas particulares de Fase o Módulo. Todo el flujo pedagógico actual se rige por los fallbacks de Plataforma Global.
          </p>
        </div>
      ) : (
        <div className="overflow-x-auto w-full custom-scrollbar">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="border-b border-slate-200 dark:border-white/10 text-slate-400 font-bold uppercase tracking-wider">
                <th className="pb-3 pl-2">Fase</th>
                <th className="pb-3">Módulo / Nivel</th>
                <th className="pb-3 text-center">Ejercicios</th>
                <th className="pb-3 text-center">Aprobación</th>
                <th className="pb-3 text-center">Cronómetro</th>
                <th className="pb-3 text-center">Feedback</th>
                <th className="pb-3 pr-2 text-right">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-white/5">
              {activeOverrides.map((config, idx) => {
                const { phaseName, sectionName } = getFriendlyName(config);
                return (
                  <tr key={idx} className="hover:bg-slate-50 dark:hover:bg-white/5 transition-colors font-medium text-slate-700 dark:text-slate-300">
                    <td className="py-4 pl-2 font-black text-slate-900 dark:text-white max-w-[150px] truncate">{phaseName.split(':')[0]}</td>
                    <td className="py-4 max-w-[250px] truncate">{sectionName}</td>
                    <td className="py-4 text-center font-bold text-blue-500">{config.cantidad_requerida}</td>
                    <td className="py-4 text-center font-bold text-green-500">{config.porcentaje_aprobacion}%</td>
                    <td className="py-4 text-center">
                      {config.usa_cronometro ? (
                        <span className="px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-500 font-bold">{config.tiempo_default_segundos || 12}s</span>
                      ) : (
                        <span className="text-slate-400 dark:text-slate-600">-</span>
                      )}
                    </td>
                    <td className="py-4 text-center capitalize">{config.tipo_feedback || 'Simple'}</td>
                    <td className="py-4 pr-2 text-right">
                      <div className="flex justify-end gap-2">
                        <button
                          type="button"
                          onClick={() => onSelectNode(config.fase_id, config.seccion, config.operacion)}
                          className="px-2.5 py-1 bg-blue-500/10 hover:bg-blue-500 hover:text-white text-blue-500 rounded-lg border border-blue-500/20 transition-all font-bold"
                        >
                          Configurar
                        </button>
                        <button
                          type="button"
                          onClick={() => onRemoveOverride(config.fase_id, config.seccion, config.operacion)}
                          className="p-1 text-slate-400 hover:text-red-500 dark:hover:text-red-400 transition-colors"
                          title="Eliminar regla y heredar del padre"
                        >
                          <ToggleRight className="text-red-500" size={20} />
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
  );
};
