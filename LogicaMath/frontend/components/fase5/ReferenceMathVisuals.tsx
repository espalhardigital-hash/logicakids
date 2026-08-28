import React from 'react';

type FractionStripProps = {
  numerator: number;
  denominator: number;
  factor?: number | null;
  color: string;
  equivalent?: boolean;
  objective?: string;
  expression?: string;
};

export function FractionStripVisual({ numerator, denominator, factor, color, equivalent = false, objective, expression }: FractionStripProps) {
  const safeDenominator = Math.max(1, denominator);
  const cellWidth = 240 / safeDenominator;

  return (
    <div className="w-full max-w-[300px] mx-auto" aria-label={`Tira dividida en ${safeDenominator} partes iguales`}>
      <svg viewBox="0 0 280 92" className="w-full h-[92px]" role="img">
        <text x="140" y="16" textAnchor="middle" fill="#cbd5e1" fontSize="12" fontWeight="700">
          Parte de un todo
        </text>
        <g transform="translate(20 30)">
          {Array.from({ length: safeDenominator }, (_, index) => (
            <rect
              key={index}
              x={index * cellWidth}
              y="0"
              width={cellWidth}
              height="34"
              fill={index < numerator ? color : '#182235'}
              stroke="#94a3b8"
              strokeWidth="1"
              rx="2"
            />
          ))}
        </g>
        <text x="140" y="82" textAnchor="middle" fill="#f8fafc" fontSize="16" fontWeight="800">
          {numerator}/{safeDenominator}
          {equivalent && factor ? `  × ${factor}` : ''}
        </text>
      </svg>
      {equivalent && (
        <div className="mt-1 text-center" aria-label={`Busca ${objective || 'el término solicitado'}`}>
          <p className="m-0 text-[11px] font-bold text-amber-300">Busca solo: {objective || 'el término solicitado'}</p>
          {expression && <p className="m-0 mt-1 text-sm font-black text-slate-100">{expression}</p>}
        </div>
      )}
    </div>
  );
}

type FractionTerm = {
  numerador: number | null;
  denominador: number | null;
};

type EquivalentFractionPuzzleProps = {
  left: FractionTerm;
  right: FractionTerm;
  objective?: string;
  mode?: 'equivalencia' | 'revision';
  incorrectTerm?: 'numerador' | 'denominador' | null;
  showCuts?: boolean;
  color: string;
};

function FractionNotation({ value, invalidTerm }: { value: FractionTerm; invalidTerm?: 'numerador' | 'denominador' | null }) {
  const termClass = (term: 'numerador' | 'denominador') =>
    invalidTerm === term ? 'text-red-300 line-through decoration-2' : 'text-slate-100';
  return (
    <span className="inline-grid min-w-[44px] grid-rows-2 text-center text-lg font-black leading-5" aria-label={`${value.numerador ?? 'incógnita'} sobre ${value.denominador ?? 'incógnita'}`}>
      <span className={`${termClass('numerador')} border-b-2 border-slate-400 px-1 pb-0.5`}>{value.numerador ?? '?'}</span>
      <span className={`${termClass('denominador')} px-1 pt-0.5`}>{value.denominador ?? '?'}</span>
    </span>
  );
}

function PuzzleStrip({ value, color, groupSize, unknownLabel }: { value: FractionTerm; color: string; groupSize?: number; unknownLabel: string }) {
  const denominator = value.denominador;
  if (!denominator) {
    return (
      <div className="relative flex h-11 w-full items-center justify-center rounded-lg border-2 border-dashed border-slate-500 bg-slate-900/60 text-[11px] font-bold text-slate-300">
        {unknownLabel}
      </div>
    );
  }

  return (
    <div
      className="relative grid h-11 w-full overflow-hidden rounded-lg border border-slate-500 bg-slate-950/50"
      style={{ gridTemplateColumns: `repeat(${denominator}, minmax(0, 1fr))` }}
      aria-label={`Tira dividida en ${denominator} partes${value.numerador === null ? ', con cantidad coloreada desconocida' : `, ${value.numerador} coloreadas`}`}
    >
      {Array.from({ length: denominator }, (_, index) => (
        <span
          key={index}
          className="border-l border-slate-400/70 first:border-l-0"
          style={{
            background: value.numerador !== null && index < value.numerador ? color : '#182235',
            borderLeftWidth: groupSize && index > 0 && index % groupSize === 0 ? 3 : undefined,
            borderLeftColor: groupSize && index > 0 && index % groupSize === 0 ? '#f8fafc' : undefined,
          }}
        />
      ))}
      {value.numerador === null && (
        <span className="absolute inset-0 flex items-center justify-center bg-slate-950/30 text-xl font-black text-amber-300">?</span>
      )}
    </div>
  );
}

export function EquivalentFractionPuzzleVisual({ left, right, objective, mode = 'equivalencia', incorrectTerm, showCuts = false, color }: EquivalentFractionPuzzleProps) {
  const groupSize = left.denominador && right.denominador && right.denominador % left.denominador === 0
    ? right.denominador / left.denominador
    : undefined;
  const relation = mode === 'revision' ? '≠' : '=';

  return (
    <div className="mx-auto w-full max-w-[430px]" aria-label={`Rompecabezas de fracciones equivalentes: ${objective || 'compara las representaciones'}`}>
      <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-3">
        <div className="min-w-0 space-y-2">
          <PuzzleStrip value={left} color={color} unknownLabel="Total: ?" />
          <div className="flex justify-center"><FractionNotation value={left} /></div>
        </div>
        <span className={`text-3xl font-black ${mode === 'revision' ? 'text-red-400' : 'text-sky-400'}`} aria-label={mode === 'revision' ? 'no es equivalente' : 'es equivalente'}>{relation}</span>
        <div className={`min-w-0 space-y-2 rounded-xl ${mode === 'revision' ? 'ring-2 ring-red-500/60 ring-offset-4 ring-offset-slate-950/20' : ''}`}>
          <PuzzleStrip value={right} color={color} groupSize={groupSize} unknownLabel="Total: ?" />
          <div className="flex justify-center"><FractionNotation value={right} invalidTerm={incorrectTerm} /></div>
        </div>
      </div>
      <p className="m-0 mt-3 text-center text-[11px] font-black uppercase tracking-[0.12em] text-amber-300">
        {objective || 'Compara las dos representaciones'}
      </p>
      {showCuts && groupSize && (
        <p className="m-0 mt-1 text-center text-[10px] font-semibold text-slate-400">
          En la segunda tira, los bordes gruesos conservan las divisiones originales.
        </p>
      )}
    </div>
  );
}

export function GroupCardsVisual({ total, groups, highlighted, color, itemLabel = 'elementos' }: { total: number; groups: number; highlighted: number; color: string; itemLabel?: string }) {
  const safeGroups = Math.max(1, groups);
  const perGroup = Math.max(1, Math.floor(total / safeGroups));
  return (
    <div className="w-full max-w-[330px] mx-auto" aria-label={`${total} ${itemLabel} repartidos en ${safeGroups} grupos iguales`}>
      <p className="m-0 mb-2 text-center text-xs text-slate-300 font-bold">{total} {itemLabel} en {safeGroups} grupos iguales</p>
      <div className="grid gap-2" style={{ gridTemplateColumns: `repeat(${Math.min(safeGroups, 5)}, minmax(0, 1fr))` }}>
        {Array.from({ length: safeGroups }, (_, groupIndex) => (
          <div key={groupIndex} className="min-h-[44px] rounded-lg bg-slate-900/70 border border-slate-700/80 p-1.5">
            <div className="flex flex-wrap justify-center gap-1">
              {Array.from({ length: perGroup }, (_, dotIndex) => (
                <span
                  key={dotIndex}
                  className="h-2.5 w-2.5 rounded-full"
                  style={{ background: groupIndex < highlighted ? color : '#64748b' }}
                />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export function HundredGridVisual({ percentage, total, color }: { percentage: number; total: number; color: string }) {
  const filled = Math.max(0, Math.min(100, percentage));
  return (
    <div className="w-full max-w-[278px] mx-auto" aria-label={`Cuadrícula de cien con ${filled} partes marcadas de un total de ${total}`}>
      <div className="grid grid-cols-10 gap-[2px] rounded-xl bg-slate-950/60 p-2 border border-slate-700/70">
        {Array.from({ length: 100 }, (_, index) => (
          <span key={index} className="aspect-square rounded-[2px]" style={{ background: index < filled ? color : '#273449' }} />
        ))}
      </div>
      <p className="m-0 mt-2 text-center text-xs font-bold text-slate-300">{filled}% de {total}</p>
    </div>
  );
}

export function DataTableVisual({ values, labels, color }: { values: number[]; labels: string[]; color: string }) {
  return (
    <div className="w-full max-w-[300px] mx-auto overflow-hidden rounded-xl border border-slate-700/80">
      <table className="w-full text-sm" aria-label="Tabla de tres registros">
        <thead className="bg-slate-900 text-slate-300"><tr><th className="p-2 text-left">Registro</th><th className="p-2 text-right">Valor</th></tr></thead>
        <tbody>
          {values.map((value, index) => (
            <tr key={labels[index]} className="border-t border-slate-800 bg-slate-950/50">
              <td className="p-2 text-slate-300">{labels[index]}</td>
              <td className="p-2 text-right font-black" style={{ color }}>{value}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export function RatioTableVisual({ a, b, factor, total, color }: { a: number; b: number; factor?: number | null; total?: number; color: string }) {
  const isRepartition = Boolean(total && !factor);
  return (
    <div className="w-full max-w-[310px] mx-auto rounded-xl border border-slate-700/80 bg-slate-950/50 p-3" aria-label="Tabla de razón">
      <div className="grid grid-cols-3 gap-2 text-center text-sm">
        <span className="text-slate-400 font-bold">Componente</span><span className="text-slate-400 font-bold">A</span><span className="text-slate-400 font-bold">B</span>
        <span className="text-slate-300">Razón</span><strong style={{ color }}>{a}</strong><strong style={{ color }}>{b}</strong>
        {factor ? <><span className="text-slate-300">Escala</span><strong className="col-span-2 text-slate-100">× {factor}</strong></> : null}
        {isRepartition ? <><span className="text-slate-300">Total</span><strong className="col-span-2 text-slate-100">{total}</strong></> : null}
      </div>
      <p className="m-0 mt-2 text-center text-[11px] text-slate-400">La tabla presenta los datos; el cálculo lo haces tú.</p>
    </div>
  );
}
