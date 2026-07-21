import React from 'react';
import { Clock, HelpCircle, ShieldAlert, ToggleLeft, ToggleRight } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { PedagogyConfig, ConfiguracionProgreso } from '../../types';

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

const SliderWithTooltip: React.FC<SliderProps> = ({ 
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

interface ConfigFormProps {
  type: 'global' | 'phase' | 'module';
  title: string;
  description: string;
  draftGlobalConfig: PedagogyConfig;
  updateGlobalField: (section: 'practica_libre' | 'desafios', field: string, val: any) => void;
  
  // Phase & Module Specific overrides
  activeOverrideRecord: ConfiguracionProgreso | null | undefined;
  toggleOverride: (enable: boolean) => void;
  updateOverrideField: (field: keyof ConfiguracionProgreso, val: any) => void;
  
  // Context info
  isSelectedChallenge?: boolean;
  selectedSubLevelId?: number | null;
  getInheritedQuestionsCount: () => number;
  getInheritedPassingScore: () => number;
  getInheritedUseTimer: () => boolean;
  getInheritedFeedbackType: () => string;
  getInheritedTimerForLevel: (levelKey: any) => number;
}

export const ConfigForm: React.FC<ConfigFormProps> = ({
  type, title, description, draftGlobalConfig, updateGlobalField,
  activeOverrideRecord, toggleOverride, updateOverrideField,
  isSelectedChallenge = false, selectedSubLevelId = null,
  getInheritedQuestionsCount, getInheritedPassingScore, getInheritedUseTimer,
  getInheritedFeedbackType, getInheritedTimerForLevel
}) => {
  const hasOverride = activeOverrideRecord !== null && activeOverrideRecord !== undefined;

  if (type === 'global') {
    return (
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
        {/* SECCIÓN 1: PRÁCTICA LIBRE */}
        <div className="bg-white/80 dark:bg-slate-950/40 border border-slate-200 dark:border-white/5 p-8 rounded-3xl flex flex-col gap-6 shadow-inner">
          <h4 className="text-xl font-black text-slate-900 dark:text-white flex items-center gap-3 border-b border-slate-200 dark:border-white/5 pb-3">
            <div className="w-3 h-3 rounded-full bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.6)]" />
            Práctica Libre (Niveles 1 a 10)
          </h4>

          <div className="flex flex-col gap-6">
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <label className="text-sm text-slate-600 dark:text-slate-300 font-bold">Volumen de Ejercicios</label>
                <span className="text-base font-black text-blue-500 bg-blue-500/10 px-3 py-1 rounded-xl border border-blue-500/20 text-center shadow-sm">
                  {draftGlobalConfig.practica_libre.cantidad_requerida} Ejercicios
                </span>
              </div>
              <SliderWithTooltip
                value={draftGlobalConfig.practica_libre.cantidad_requerida}
                min={5} max={60} step={1}
                onChange={(val) => updateGlobalField('practica_libre', 'cantidad_requerida', val)}
                accentColor="bg-blue-500"
              />
            </div>

            <div className="space-y-3 pt-3 border-t border-slate-200 dark:border-white/5">
              <div className="flex justify-between items-center">
                <label className="text-sm text-slate-600 dark:text-slate-300 font-bold">Porcentaje Mínimo Aprobación</label>
                <span className="text-base font-black text-green-500 bg-green-500/10 px-3 py-1 rounded-xl border border-green-500/20 text-center shadow-sm">
                  {draftGlobalConfig.practica_libre.porcentaje_aprobacion}%
                </span>
              </div>
              <SliderWithTooltip
                value={draftGlobalConfig.practica_libre.porcentaje_aprobacion}
                min={50} max={100} step={5}
                onChange={(val) => updateGlobalField('practica_libre', 'porcentaje_aprobacion', val)}
                accentColor="bg-green-500" unit="%"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-3 border-t border-slate-200 dark:border-white/5">
              <div className="flex flex-col gap-4">
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm text-slate-600 dark:text-slate-300 font-bold">Uso de Cronómetro</label>
                    <p className="text-[10px] text-slate-500">Tiempo por pregunta.</p>
                  </div>
                  <button 
                    type="button"
                    onClick={() => updateGlobalField('practica_libre', 'usa_cronometro', !draftGlobalConfig.practica_libre.usa_cronometro)} 
                    className="transition-all hover:scale-105"
                  >
                    <div className={`ios-switch ${draftGlobalConfig.practica_libre.usa_cronometro ? 'ios-switch-active' : ''}`}>
                      <div className="ios-switch-knob" />
                    </div>
                  </button>
                </div>
                {draftGlobalConfig.practica_libre.usa_cronometro && (
                  <div className="space-y-2 bg-slate-50 dark:bg-white/5 p-3 rounded-2xl border border-slate-200 dark:border-white/10">
                    <div className="flex justify-between items-center mb-2">
                      <label className="text-[11px] text-slate-600 dark:text-slate-300 font-bold">Límite</label>
                      <span className="text-sm font-black text-blue-500">{draftGlobalConfig.practica_libre.tiempo_default_segundos}s</span>
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

              <div className="flex flex-col gap-2">
                <label className="text-sm text-slate-600 dark:text-slate-300 font-bold">Feedback Pedagógico</label>
                <div className="flex flex-col gap-2 mt-1">
                  {['simple', 'detallado'].map((ft) => (
                    <button
                      type="button"
                      key={ft}
                      onClick={() => updateGlobalField('practica_libre', 'tipo_feedback', ft)}
                      className={`py-2.5 rounded-xl text-[11px] uppercase tracking-wider font-black border transition-all ${
                        draftGlobalConfig.practica_libre.tipo_feedback === ft
                          ? 'bg-blue-600 border-blue-500 text-white shadow-md shadow-blue-500/20'
                          : 'glass-panel border-slate-200 dark:border-white/5 text-slate-500 dark:text-slate-400 hover:text-slate-600 dark:text-slate-300'
                      }`}
                    >
                      {ft === 'simple' ? 'Simple (✔/✘)' : 'Detallado (Tutoría IA)'}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* SECCIÓN 2: DESAFÍOS */}
        <div className="bg-white/80 dark:bg-slate-950/40 border border-slate-200 dark:border-white/5 p-8 rounded-3xl flex flex-col gap-6 shadow-inner">
          <h4 className="text-xl font-black text-slate-900 dark:text-white flex items-center gap-3 border-b border-slate-200 dark:border-white/5 pb-3">
            <div className="w-3 h-3 rounded-full bg-purple-500 shadow-[0_0_8px_rgba(168,85,247,0.6)] animate-pulse" />
            Zona de Desafíos (Niveles 11 a 13)
          </h4>

          <div className="flex flex-col gap-6">
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <label className="text-sm text-slate-600 dark:text-slate-300 font-bold">Volumen de Ejercicios</label>
                <span className="text-base font-black text-purple-500 bg-purple-500/10 px-3 py-1 rounded-xl border border-purple-500/20 text-center shadow-sm">
                  {draftGlobalConfig.desafios.cantidad_requerida} Ejercicios
                </span>
              </div>
              <SliderWithTooltip
                value={draftGlobalConfig.desafios.cantidad_requerida}
                min={5} max={60} step={1}
                onChange={(val) => updateGlobalField('desafios', 'cantidad_requerida', val)}
                accentColor="bg-purple-500"
              />
            </div>

            <div className="space-y-3 pt-3 border-t border-slate-200 dark:border-white/5">
              <div className="flex justify-between items-center">
                <label className="text-sm text-slate-600 dark:text-slate-300 font-bold">Porcentaje Mínimo Aprobación</label>
                <span className="text-base font-black text-green-500 bg-green-500/10 px-3 py-1 rounded-xl border border-green-500/20 text-center shadow-sm">
                  {draftGlobalConfig.desafios.porcentaje_aprobacion}%
                </span>
              </div>
              <SliderWithTooltip
                value={draftGlobalConfig.desafios.porcentaje_aprobacion}
                min={50} max={100} step={5}
                onChange={(val) => updateGlobalField('desafios', 'porcentaje_aprobacion', val)}
                accentColor="bg-green-500" unit="%"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-3 border-t border-slate-200 dark:border-white/5">
              <div className="flex flex-col gap-4">
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm text-slate-600 dark:text-slate-300 font-bold">Uso de Cronómetro</label>
                    <p className="text-[10px] text-slate-500">Para toda la evaluación.</p>
                  </div>
                  <button 
                    type="button"
                    onClick={() => updateGlobalField('desafios', 'usa_cronometro', !draftGlobalConfig.desafios.usa_cronometro)} 
                    className="transition-all hover:scale-105"
                  >
                    <div className={`ios-switch ${draftGlobalConfig.desafios.usa_cronometro ? 'ios-switch-active' : ''}`}>
                      <div className="ios-switch-knob" />
                    </div>
                  </button>
                </div>

                <div className="space-y-4" style={{ opacity: draftGlobalConfig.desafios.usa_cronometro ? 1 : 0.3, transition: 'opacity 0.2s' }}>
                  <div className="space-y-1 bg-slate-50 dark:bg-white/5 p-3 rounded-2xl border border-slate-200 dark:border-white/10">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-[10px] font-bold text-slate-600 dark:text-slate-300 font-bold">Desafío 1</span>
                      <span className="text-xs font-black text-purple-500">{draftGlobalConfig.desafios.tiempo_default_segundos_11}s</span>
                    </div>
                    <SliderWithTooltip
                      value={draftGlobalConfig.desafios.tiempo_default_segundos_11}
                      min={10} max={200}
                      disabled={!draftGlobalConfig.desafios.usa_cronometro}
                      onChange={(val) => updateGlobalField('desafios', 'tiempo_default_segundos_11', val)}
                      accentColor="bg-purple-500" unit="s" isThermal
                    />
                  </div>

                  <div className="space-y-1 bg-slate-50 dark:bg-white/5 p-3 rounded-2xl border border-slate-200 dark:border-white/10">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-[10px] font-bold text-slate-600 dark:text-slate-300 font-bold">Desafío 2</span>
                      <span className="text-xs font-black text-purple-500">{draftGlobalConfig.desafios.tiempo_default_segundos_12}s</span>
                    </div>
                    <SliderWithTooltip
                      value={draftGlobalConfig.desafios.tiempo_default_segundos_12}
                      min={10} max={200}
                      disabled={!draftGlobalConfig.desafios.usa_cronometro}
                      onChange={(val) => updateGlobalField('desafios', 'tiempo_default_segundos_12', val)}
                      accentColor="bg-purple-500" unit="s" isThermal
                    />
                  </div>

                  <div className="space-y-1 bg-slate-50 dark:bg-white/5 p-3 rounded-2xl border border-slate-200 dark:border-white/10">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-[10px] font-bold text-slate-600 dark:text-slate-300 font-bold">Desafío Final</span>
                      <span className="text-xs font-black text-purple-500">{draftGlobalConfig.desafios.tiempo_default_segundos_13}s</span>
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

              <div className="flex flex-col gap-2">
                <label className="text-sm text-slate-600 dark:text-slate-300 font-bold">Feedback Pedagógico</label>
                <div className="flex flex-col gap-2 mt-1">
                  {['simple', 'detallado'].map((ft) => (
                    <button
                      type="button"
                      key={ft}
                      onClick={() => updateGlobalField('desafios', 'tipo_feedback', ft)}
                      className={`py-2.5 rounded-xl text-[11px] uppercase tracking-wider font-black border transition-all ${
                        draftGlobalConfig.desafios.tipo_feedback === ft
                          ? 'bg-purple-600 border-purple-500 text-white shadow-md shadow-purple-500/20'
                          : 'glass-panel border-slate-200 dark:border-white/5 text-slate-500 dark:text-slate-400 hover:text-slate-600 dark:text-slate-300'
                      }`}
                    >
                      {ft === 'simple' ? 'Simple (✔/✘)' : 'Detallado (Tutoría IA)'}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Phase and Module forms
  return (
    <div className="bg-white dark:bg-white/5 backdrop-blur-2xl border border-slate-200 dark:border-white/10 p-8 rounded-[2.5rem] shadow-2xl flex flex-col gap-8 w-full relative">
      <div className="flex justify-between items-start z-30">
        <div>
          <div className={`inline-flex items-center gap-2 text-[10px] font-black uppercase tracking-widest px-3 py-1 rounded-full border ${
            type === 'phase' ? 'text-blue-400 bg-blue-500/10 border-blue-500/20' : 'text-amber-500 bg-amber-500/10 border-amber-500/20'
          }`}>
            {type === 'phase' ? 'Parámetros por Defecto de Fase' : 'Configuración de Módulo'}
          </div>
          <h3 className="text-3xl font-black text-slate-900 dark:text-white mt-3">{title}</h3>
          <p className="text-slate-500 dark:text-slate-400 text-sm mt-1 max-w-2xl">{description}</p>
        </div>

        <div className="flex flex-col items-end gap-2 bg-slate-50 dark:bg-slate-900/50 p-4 rounded-2xl border border-slate-200 dark:border-white/10 shadow-sm">
          <label className="text-[10px] font-black text-slate-500 dark:text-slate-400 uppercase tracking-wider">
            {type === 'phase' ? 'Sobrescribir Global' : 'Sobrescribir Padre'}
          </label>
          <button 
            type="button"
            onClick={() => toggleOverride(!hasOverride)}
            className="transition-all hover:scale-105"
          >
            {hasOverride ? (
              <ToggleRight size={38} className={type === 'phase' ? "text-blue-500" : "text-amber-500"} />
            ) : (
              <ToggleLeft size={38} className="text-slate-400" />
            )}
          </button>
        </div>
      </div>

      <div className="relative overflow-hidden rounded-3xl min-h-[350px]">
        <AnimatePresence>
          {!hasOverride && (
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="absolute inset-0 bg-white/60 dark:bg-slate-950/70 backdrop-blur-md z-[55] flex flex-col items-center justify-center p-8 text-center"
            >
              <ShieldAlert className={type === 'phase' ? "text-blue-500 mb-4" : "text-amber-500 mb-4"} size={48} strokeWidth={1.5} />
              <h4 className="text-2xl font-black text-slate-900 dark:text-white mb-2">
                Heredando de {type === 'phase' ? 'Límites Globales' : 'Parámetros de Fase'}
              </h4>
              <p className="text-sm text-slate-600 dark:text-slate-300 max-w-md font-medium leading-relaxed">
                Esta sección está utilizando las reglas heredadas. Activa el botón de sobrescritura superior si deseas definir límites exclusivos para este nivel.
              </p>
            </motion.div>
          )}
        </AnimatePresence>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 p-4 bg-white/80 dark:bg-slate-950/40 border border-slate-200 dark:border-white/5 rounded-3xl h-full shadow-inner">
          <div className="flex flex-col gap-8">
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <label className="text-sm lg:text-base text-slate-600 dark:text-slate-300 font-bold">Volumen de Ejercicios</label>
                <span className="text-lg font-black text-blue-500 bg-blue-500/10 px-4 py-1 rounded-xl border border-blue-500/20 shadow-sm">
                  {activeOverrideRecord?.cantidad_requerida ?? getInheritedQuestionsCount()}
                </span>
              </div>
              <SliderWithTooltip
                value={activeOverrideRecord?.cantidad_requerida ?? getInheritedQuestionsCount()}
                min={type === 'module' ? 5 : 10} max={120} step={5}
                disabled={!hasOverride}
                onChange={(val) => updateOverrideField('cantidad_requerida', val)}
                accentColor="bg-blue-500"
              />
            </div>

            <div className="space-y-4 pt-6 border-t border-slate-200 dark:border-white/5">
              <div className="flex justify-between items-center">
                <label className="text-sm lg:text-base text-slate-600 dark:text-slate-300 font-bold">Porcentaje de Aprobación</label>
                <span className="text-lg font-black text-green-500 bg-green-500/10 px-4 py-1 rounded-xl border border-green-500/20 shadow-sm">
                  {activeOverrideRecord?.porcentaje_aprobacion ?? getInheritedPassingScore()}%
                </span>
              </div>
              <SliderWithTooltip
                value={activeOverrideRecord?.porcentaje_aprobacion ?? getInheritedPassingScore()}
                min={50} max={100} step={5}
                disabled={!hasOverride}
                onChange={(val) => updateOverrideField('porcentaje_aprobacion', val)}
                accentColor="bg-green-500" unit="%"
              />
            </div>
          </div>

          <div className="bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-white/10 p-6 rounded-3xl flex flex-col gap-6 shadow-sm">
            {type === 'module' && !isSelectedChallenge && (
              <div className="space-y-4 mb-4">
                <label className="text-sm text-slate-600 dark:text-slate-300 font-bold flex items-center gap-2">
                  <HelpCircle size={18} className="text-purple-500" /> Tipo de Feedback Pedagógico
                </label>
                <div className="flex gap-3">
                  {['simple', 'detallado'].map((ft) => (
                    <button
                      type="button"
                      key={ft}
                      onClick={() => updateOverrideField('tipo_feedback', ft)}
                      disabled={!hasOverride}
                      className={`flex-1 py-3 rounded-2xl border text-xs uppercase tracking-wider font-black transition-all ${
                        (activeOverrideRecord?.tipo_feedback ?? getInheritedFeedbackType()) === ft
                          ? 'bg-purple-600 border-purple-500 text-white shadow-md shadow-purple-500/20'
                          : 'bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 text-slate-500 dark:text-slate-400'
                      }`}
                    >
                      {ft === 'simple' ? 'Simple (✔/✘)' : 'Tutoría IA'}
                    </button>
                  ))}
                </div>
              </div>
            )}

            <div className={`space-y-4 ${type === 'phase' ? 'mt-auto' : ''}`}>
              <div className="flex items-center justify-between">
                <div>
                  <label className="text-sm text-slate-600 dark:text-slate-300 font-bold">Habilitar Cronómetro</label>
                  <p className="text-[10px] text-slate-500">Límite de tiempo activo.</p>
                </div>
                <button 
                  type="button"
                  onClick={() => updateOverrideField('usa_cronometro', !(activeOverrideRecord?.usa_cronometro ?? getInheritedUseTimer()))}
                  disabled={!hasOverride}
                  className="transition-all hover:scale-105 disabled:opacity-30"
                >
                  <div className={`ios-switch ${(activeOverrideRecord?.usa_cronometro ?? getInheritedUseTimer()) ? 'ios-switch-active' : ''}`}>
                    <div className="ios-switch-knob" />
                  </div>
                </button>
              </div>

              {(activeOverrideRecord?.usa_cronometro ?? getInheritedUseTimer()) && (
                <div className="space-y-3 pt-4 border-t border-slate-200 dark:border-white/10">
                  <div className="flex justify-between items-center">
                    <label className="text-xs text-slate-500 dark:text-slate-400 font-bold">Límite por Pregunta</label>
                    <span className="text-lg font-black text-amber-500">
                      {activeOverrideRecord?.tiempo_default_segundos ?? getInheritedTimerForLevel('medium')}s
                    </span>
                  </div>
                  <SliderWithTooltip
                    value={activeOverrideRecord?.tiempo_default_segundos ?? getInheritedTimerForLevel('medium')}
                    min={3} max={type === 'phase' ? 3600 : 600} step={5}
                    disabled={!hasOverride}
                    onChange={(val) => updateOverrideField('tiempo_default_segundos', val)}
                    accentColor="bg-amber-500" unit="s" isThermal
                  />
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
