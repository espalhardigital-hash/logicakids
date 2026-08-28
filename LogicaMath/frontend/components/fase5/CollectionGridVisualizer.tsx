import React from 'react';
import type { Fase5Pregunta } from './Fase5Types';

interface Props {
  pregunta: Fase5Pregunta;
  moduleColor: string;
}

/** Representa una cantidad como grupos iguales; no reutiliza la pizza para
 * problemas de fracción de una colección. */
export const CollectionGridVisualizer: React.FC<Props> = ({ pregunta, moduleColor }) => {
  const data = pregunta.datos_numericos || {};
  const total = Math.max(1, Number(data.total || 0));
  const groups = Math.max(1, Number(data.grupos || data.b || 1));
  const itemLabel = String(data.etiqueta_elementos || 'elementos');
  const perGroup = Math.max(1, Math.floor(total / groups));
  const visibleGroups = Math.min(groups, 10);
  const itemLimit = 12;

  return (
    <figure className="w-full max-w-[560px] mx-auto rounded-3xl border border-sky-300/20 bg-slate-900/70 p-4 shadow-xl" aria-label={`Colección de ${total} ${itemLabel} agrupada en ${groups} grupos iguales`}>
      <figcaption className="mb-3 text-center text-xs font-black uppercase tracking-[0.18em] text-slate-300">
        {total} {itemLabel} en {groups} grupos iguales
      </figcaption>
      <div className="grid gap-2" style={{ gridTemplateColumns: `repeat(${Math.min(visibleGroups, 5)}, minmax(0, 1fr))` }}>
        {Array.from({ length: visibleGroups }, (_, groupIndex) => (
          <div key={groupIndex} className="rounded-2xl border border-white/10 bg-slate-950/55 p-2">
            <div className="mb-1 text-center text-[10px] font-bold text-slate-400">Grupo {groupIndex + 1}</div>
            <div className="flex flex-wrap justify-center gap-1">
              {Array.from({ length: Math.min(perGroup, itemLimit) }, (_, itemIndex) => (
                <span key={itemIndex} className="h-3.5 w-3.5 rounded-full border border-white/30" style={{ backgroundColor: moduleColor }} />
              ))}
              {perGroup > itemLimit && <span className="text-xs font-black text-slate-300">+{perGroup - itemLimit}</span>}
            </div>
          </div>
        ))}
      </div>
      {groups > visibleGroups && <p className="mt-3 text-center text-xs font-semibold text-slate-400">La colección continúa con grupos del mismo tamaño.</p>}
    </figure>
  );
};
