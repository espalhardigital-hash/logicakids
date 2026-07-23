import React from 'react';
import { Globe } from 'lucide-react';
import { SliderWithTooltip } from './SliderWithTooltip';
import { PedagogyConfig } from '../../types';

interface GlobalConfigPanelProps {
  draftGlobalConfig: PedagogyConfig;
  updateGlobalField: (section: 'practica_libre' | 'desafios', field: string, val: any) => void;
}

export const GlobalConfigPanel: React.FC<GlobalConfigPanelProps> = ({ draftGlobalConfig, updateGlobalField }) => {
  return (
    <div className="bg-white dark:bg-white/5 border border-slate-200 dark:border-white/10 rounded-3xl p-6 flex flex-col gap-6">
      <div className="flex items-center gap-2">
        <Globe size={18} className="text-blue-500" />
        <div>
          <h3 className="text-base font-black text-slate-900 dark:text-white">Fallback de plataforma</h3>
          <p className="text-xs text-slate-500 dark:text-slate-400">Valores base que usa todo el sistema cuando una fase o módulo no tiene reglas propias.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        {/* PRÁCTICA LIBRE */}
        <div className="bg-slate-50 dark:bg-slate-950/40 border border-slate-200 dark:border-white/5 p-6 rounded-2xl flex flex-col gap-5">
          <h4 className="text-sm font-black text-slate-900 dark:text-white flex items-center gap-2 border-b border-slate-200 dark:border-white/5 pb-2">
            <div className="w-2.5 h-2.5 rounded-full bg-blue-500" />
            Práctica Libre (Niveles 1 a 10)
          </h4>

          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <label className="text-xs text-slate-600 dark:text-slate-300 font-bold">Volumen de Ejercicios</label>
              <span className="text-sm font-black text-blue-500">{draftGlobalConfig.practica_libre.cantidad_requerida}</span>
            </div>
            <SliderWithTooltip
              value={draftGlobalConfig.practica_libre.cantidad_requerida}
              min={5} max={60} step={1}
              onChange={(val) => updateGlobalField('practica_libre', 'cantidad_requerida', val)}
              accentColor="bg-blue-500"
            />
          </div>

          <div className="space-y-2 pt-2 border-t border-slate-200 dark:border-white/5">
            <div className="flex justify-between items-center">
              <label className="text-xs text-slate-600 dark:text-slate-300 font-bold">Porcentaje Mínimo Aprobación</label>
              <span className="text-sm font-black text-green-500">{draftGlobalConfig.practica_libre.porcentaje_aprobacion}%</span>
            </div>
            <SliderWithTooltip
              value={draftGlobalConfig.practica_libre.porcentaje_aprobacion}
              min={50} max={100} step={5}
              onChange={(val) => updateGlobalField('practica_libre', 'porcentaje_aprobacion', val)}
              accentColor="bg-green-500" unit="%"
            />
          </div>

          <div className="grid grid-cols-2 gap-4 pt-2 border-t border-slate-200 dark:border-white/5">
            <div className="flex flex-col gap-3">
              <div className="flex items-center justify-between">
                <label className="text-xs text-slate-600 dark:text-slate-300 font-bold">Cronómetro</label>
                <button
                  type="button"
                  onClick={() => updateGlobalField('practica_libre', 'usa_cronometro', !draftGlobalConfig.practica_libre.usa_cronometro)}
                >
                  <div className={`ios-switch ${draftGlobalConfig.practica_libre.usa_cronometro ? 'ios-switch-active' : ''}`}>
                    <div className="ios-switch-knob" />
                  </div>
                </button>
              </div>
              {draftGlobalConfig.practica_libre.usa_cronometro && (
                <div className="space-y-1 bg-white dark:bg-white/5 p-2.5 rounded-xl border border-slate-200 dark:border-white/10">
                  <div className="flex justify-between items-center">
                    <label className="text-[10px] text-slate-600 dark:text-slate-300 font-bold">Límite</label>
                    <span className="text-xs font-black text-blue-500">{draftGlobalConfig.practica_libre.tiempo_default_segundos}s</span>
                  </div>
                  <SliderWithTooltip
                    value={draftGlobalConfig.practica_libre.tiempo_default_segundos}
                    min={3} max={60}
                    onChange={(val) => updateGlobalField('practica_libre', 'tiempo_default_segundos', val)}
                    accentColor="bg-blue-500" unit="s" isThermal
                  />
                </div>
              )}
            </div>

            <div className="flex flex-col gap-1.5">
              <label className="text-xs text-slate-600 dark:text-slate-300 font-bold">Feedback</label>
              {(['simple', 'detallado'] as const).map((ft) => (
                <button
                  type="button"
                  key={ft}
                  onClick={() => updateGlobalField('practica_libre', 'tipo_feedback', ft)}
                  className={`py-2 rounded-lg text-[10px] uppercase tracking-wider font-black border transition-all ${
                    draftGlobalConfig.practica_libre.tipo_feedback === ft
                      ? 'bg-blue-600 border-blue-500 text-white'
                      : 'bg-white dark:bg-slate-800 border-slate-200 dark:border-white/5 text-slate-500 dark:text-slate-400'
                  }`}
                >
                  {ft === 'simple' ? 'Simple (✔/✘)' : 'Tutoría IA'}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* DESAFÍOS */}
        <div className="bg-slate-50 dark:bg-slate-950/40 border border-slate-200 dark:border-white/5 p-6 rounded-2xl flex flex-col gap-5">
          <h4 className="text-sm font-black text-slate-900 dark:text-white flex items-center gap-2 border-b border-slate-200 dark:border-white/5 pb-2">
            <div className="w-2.5 h-2.5 rounded-full bg-purple-500" />
            Zona de Desafíos (Niveles 11 a 13)
          </h4>

          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <label className="text-xs text-slate-600 dark:text-slate-300 font-bold">Volumen de Ejercicios</label>
              <span className="text-sm font-black text-purple-500">{draftGlobalConfig.desafios.cantidad_requerida}</span>
            </div>
            <SliderWithTooltip
              value={draftGlobalConfig.desafios.cantidad_requerida}
              min={5} max={60} step={1}
              onChange={(val) => updateGlobalField('desafios', 'cantidad_requerida', val)}
              accentColor="bg-purple-500"
            />
          </div>

          <div className="space-y-2 pt-2 border-t border-slate-200 dark:border-white/5">
            <div className="flex justify-between items-center">
              <label className="text-xs text-slate-600 dark:text-slate-300 font-bold">Porcentaje Mínimo Aprobación</label>
              <span className="text-sm font-black text-green-500">{draftGlobalConfig.desafios.porcentaje_aprobacion}%</span>
            </div>
            <SliderWithTooltip
              value={draftGlobalConfig.desafios.porcentaje_aprobacion}
              min={50} max={100} step={5}
              onChange={(val) => updateGlobalField('desafios', 'porcentaje_aprobacion', val)}
              accentColor="bg-green-500" unit="%"
            />
          </div>

          <div className="grid grid-cols-2 gap-4 pt-2 border-t border-slate-200 dark:border-white/5">
            <div className="flex flex-col gap-3">
              <div className="flex items-center justify-between">
                <label className="text-xs text-slate-600 dark:text-slate-300 font-bold">Cronómetro</label>
                <button
                  type="button"
                  onClick={() => updateGlobalField('desafios', 'usa_cronometro', !draftGlobalConfig.desafios.usa_cronometro)}
                >
                  <div className={`ios-switch ${draftGlobalConfig.desafios.usa_cronometro ? 'ios-switch-active' : ''}`}>
                    <div className="ios-switch-knob" />
                  </div>
                </button>
              </div>

              <div className="space-y-2" style={{ opacity: draftGlobalConfig.desafios.usa_cronometro ? 1 : 0.3, transition: 'opacity 0.2s' }}>
                <div className="space-y-1 bg-white dark:bg-white/5 p-2 rounded-xl border border-slate-200 dark:border-white/10">
                  <div className="flex justify-between items-center">
                    <span className="text-[9px] font-bold text-slate-600 dark:text-slate-300">Desafío 1</span>
                    <span className="text-[11px] font-black text-purple-500">{draftGlobalConfig.desafios.tiempo_default_segundos_11}s</span>
                  </div>
                  <SliderWithTooltip
                    value={draftGlobalConfig.desafios.tiempo_default_segundos_11}
                    min={10} max={200}
                    disabled={!draftGlobalConfig.desafios.usa_cronometro}
                    onChange={(val) => updateGlobalField('desafios', 'tiempo_default_segundos_11', val)}
                    accentColor="bg-purple-500" unit="s" isThermal
                  />
                </div>
                <div className="space-y-1 bg-white dark:bg-white/5 p-2 rounded-xl border border-slate-200 dark:border-white/10">
                  <div className="flex justify-between items-center">
                    <span className="text-[9px] font-bold text-slate-600 dark:text-slate-300">Desafío 2</span>
                    <span className="text-[11px] font-black text-purple-500">{draftGlobalConfig.desafios.tiempo_default_segundos_12}s</span>
                  </div>
                  <SliderWithTooltip
                    value={draftGlobalConfig.desafios.tiempo_default_segundos_12}
                    min={10} max={200}
                    disabled={!draftGlobalConfig.desafios.usa_cronometro}
                    onChange={(val) => updateGlobalField('desafios', 'tiempo_default_segundos_12', val)}
                    accentColor="bg-purple-500" unit="s" isThermal
                  />
                </div>
                <div className="space-y-1 bg-white dark:bg-white/5 p-2 rounded-xl border border-slate-200 dark:border-white/10">
                  <div className="flex justify-between items-center">
                    <span className="text-[9px] font-bold text-slate-600 dark:text-slate-300">Desafío Final</span>
                    <span className="text-[11px] font-black text-purple-500">{draftGlobalConfig.desafios.tiempo_default_segundos_13}s</span>
                  </div>
                  <SliderWithTooltip
                    value={draftGlobalConfig.desafios.tiempo_default_segundos_13}
                    min={10} max={200}
                    disabled={!draftGlobalConfig.desafios.usa_cronometro}
                    onChange={(val) => updateGlobalField('desafios', 'tiempo_default_segundos_13', val)}
                    accentColor="bg-purple-500" unit="s" isThermal
                  />
                </div>
              </div>
            </div>

            <div className="flex flex-col gap-1.5">
              <label className="text-xs text-slate-600 dark:text-slate-300 font-bold">Feedback</label>
              {(['simple', 'detallado'] as const).map((ft) => (
                <button
                  type="button"
                  key={ft}
                  onClick={() => updateGlobalField('desafios', 'tipo_feedback', ft)}
                  className={`py-2 rounded-lg text-[10px] uppercase tracking-wider font-black border transition-all ${
                    draftGlobalConfig.desafios.tipo_feedback === ft
                      ? 'bg-purple-600 border-purple-500 text-white'
                      : 'bg-white dark:bg-slate-800 border-slate-200 dark:border-white/5 text-slate-500 dark:text-slate-400'
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
  );
};
