import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Clock3, Lightbulb } from 'lucide-react';
import type { Fase7AnswerResult } from './Fase7Types';

interface Props {
  resultado: Fase7AnswerResult;
  moduleColor: string;
  onContinue: () => void;
}

/** Corrección obligatoria, paginada y sin desplazamiento vertical tras un error. */
export const Fase7FeedbackLockModal: React.FC<Props> = ({ resultado, moduleColor, onContinue }) => {
  const [secondsLeft, setSecondsLeft] = useState(resultado.pausa_obligatoria_segundos || 10);
  const [stepPage, setStepPage] = useState(0);
  const steps = resultado.explicacion?.pasos ?? [];
  const stepsPerPage = 3;
  const totalStepPages = Math.max(1, Math.ceil(steps.length / stepsPerPage));
  const visibleSteps = steps.slice(stepPage * stepsPerPage, (stepPage + 1) * stepsPerPage);

  useEffect(() => {
    if (secondsLeft <= 0) return;
    const timer = window.setTimeout(() => setSecondsLeft((current) => current - 1), 1000);
    return () => window.clearTimeout(timer);
  }, [secondsLeft]);

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="f6-feedback-overlay" style={{ zIndex: 1200 }} role="dialog" aria-modal="true" aria-labelledby="fase7-feedback-title">
      <motion.section initial={{ scale: 0.96, y: 16 }} animate={{ scale: 1, y: 0 }} className="f6-feedback-card glass-card" style={{ maxWidth: '620px', width: '92%', padding: '28px', borderTop: `6px solid ${moduleColor}` }}>
        <div className="flex items-center gap-3 mb-4"><Lightbulb size={30} style={{ color: moduleColor }} aria-hidden="true" /><div><h2 id="fase7-feedback-title" className="text-xl font-black text-white">Veamos cómo se resolvía</h2><p className="text-sm text-slate-300">La respuesta correcta es <strong className="text-white">{resultado.respuesta_correcta}</strong>.</p></div></div>
        {steps.length > 0 ? <ol className="space-y-2 mb-5">{visibleSteps.map((step: any, index: number) => <li key={step.orden ?? index} className="flex gap-2 text-sm leading-5 text-slate-100"><span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full text-xs font-black text-slate-950" style={{ background: moduleColor }}>{step.orden ?? index + 1}</span><span>{step.texto}</span></li>)}</ol> : <p className="mb-5 text-sm leading-5 text-slate-100">{resultado.explicacion_profunda || resultado.feedback_error}</p>}
        {totalStepPages > 1 && <div className="mb-5 flex items-center justify-between gap-3"><span className="text-xs font-bold text-slate-400">Paso explicado {stepPage + 1} de {totalStepPages}</span><div className="flex gap-2"><button type="button" disabled={stepPage === 0} onClick={() => setStepPage((page) => page - 1)} className="rounded-lg border border-white/15 px-3 py-1.5 text-xs font-bold text-white disabled:opacity-30">Atrás</button><button type="button" disabled={stepPage === totalStepPages - 1} onClick={() => setStepPage((page) => page + 1)} className="rounded-lg border border-white/15 px-3 py-1.5 text-xs font-bold text-white disabled:opacity-30">Siguiente</button></div></div>}
        <div className="flex items-center justify-between gap-3 rounded-xl bg-slate-950/60 px-4 py-3"><span className="flex items-center gap-2 text-xs font-bold uppercase tracking-wide text-slate-300"><Clock3 size={16} aria-hidden="true" />{secondsLeft <= 0 ? 'Ya puedes continuar' : `Lee la solución: ${secondsLeft} s`}</span><button type="button" disabled={secondsLeft > 0 || stepPage < totalStepPages - 1} onClick={onContinue} className="rounded-xl px-4 py-2 text-sm font-black text-white transition disabled:cursor-not-allowed disabled:opacity-40" style={{ background: moduleColor }}>Continuar</button></div>
      </motion.section>
    </motion.div>
  );
};
