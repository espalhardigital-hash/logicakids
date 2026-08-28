import React from 'react';
import { describe, expect, it } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { Fase5VisualizerEngine } from '../components/fase5/Fase5VisualizerEngine';
import type { Fase5Pregunta } from '../components/fase5/Fase5Types';

const baseQuestion = (tipo_visual: NonNullable<Fase5Pregunta['datos_numericos']>['tipo_visual'], datos: Record<string, unknown>): Fase5Pregunta => ({
  id: 99,
  enunciado: 'Pregunta de referencia',
  tipo_pregunta: 'respuesta_numerica',
  tiene_cronometro: false,
  datos_numericos: { tipo_visual, ...datos },
});

describe('ReferenceMathVisuals', () => {
  it('plantea una equivalencia con término faltante sin mostrar la multiplicación', () => {
    render(<Fase5VisualizerEngine pregunta={baseQuestion('equivalence_strip', {
      fraccion_izquierda: { numerador: 2, denominador: 5 },
      fraccion_derecha: { numerador: null, denominador: 15 },
      objetivo_visual: 'completa el numerador equivalente',
      modo_visual: 'equivalencia',
    })} moduleColor="#ec4899" moduloId={1} nivelId={2} />);
    expect(screen.getByLabelText('2 sobre 5')).toBeInTheDocument();
    expect(screen.getByLabelText('incógnita sobre 15')).toBeInTheDocument();
    expect(screen.getByText(/completa el numerador equivalente/i)).toBeInTheDocument();
    expect(screen.queryByText(/2 × 3/)).not.toBeInTheDocument();
    expect(screen.queryByText('6')).not.toBeInTheDocument();
  });

  it('no dibuja una fracción final completa cuando solo se pide el denominador', () => {
    const { container } = render(<Fase5VisualizerEngine pregunta={baseQuestion('pizza', {
      num_base: 4,
      den_base: 6,
      factor: 2,
      objetivo_visual: 'denominador equivalente',
      expresion_visual: '6 × 2 = ?',
    })} moduleColor="#8b5cf6" moduloId={1} nivelId={2} />);

    expect(screen.getByLabelText('4 sobre 6')).toBeInTheDocument();
    expect(screen.getByLabelText('8 sobre incógnita')).toBeInTheDocument();
    expect(screen.getByText(/denominador equivalente/i)).toBeInTheDocument();
    expect(screen.queryByText('6 × 2 = ?')).not.toBeInTheDocument();
    expect(screen.queryByText('8/12')).not.toBeInTheDocument();
    expect(container.querySelectorAll('svg')).toHaveLength(0);
  });

  it('marca una propuesta falsa y no la presenta como equivalencia válida', () => {
    render(<Fase5VisualizerEngine pregunta={baseQuestion('equivalence_strip', {
      fraccion_izquierda: { numerador: 2, denominador: 5 },
      fraccion_derecha: { numerador: 7, denominador: 15 },
      objetivo_visual: 'corrige el numerador marcado',
      modo_visual: 'revision',
      termino_incorrecto: 'numerador',
    })} moduleColor="#ec4899" moduloId={1} nivelId={2} />);
    expect(screen.getByLabelText('no es equivalente')).toHaveTextContent('≠');
    expect(screen.getByText('7')).toHaveClass('line-through');
  });

  it('muestra datos de porcentaje y razón sin revelar el resultado calculado', () => {
    const { rerender } = render(<Fase5VisualizerEngine pregunta={baseQuestion('hundred_grid', { porcentaje: 25, total: 80 })} moduleColor="#ec4899" moduloId={3} nivelId={1} />);
    expect(screen.getByText('25% de 80')).toBeInTheDocument();
    expect(screen.queryByText('20')).not.toBeInTheDocument();

    rerender(<Fase5VisualizerEngine pregunta={baseQuestion('ratio_table', { ratio_a: 2, ratio_b: 3, factor: 4 })} moduleColor="#ec4899" moduloId={4} nivelId={1} />);
    expect(screen.getByText('× 4')).toBeInTheDocument();
    expect(screen.queryByText('8')).not.toBeInTheDocument();
  });

  it('nombra la colección con el objeto real del enunciado', () => {
    render(<Fase5VisualizerEngine pregunta={baseQuestion('group_cards', {
      total: 20,
      grupos: 4,
      grupos_destacados: 1,
      etiqueta_elementos: 'estudiantes',
    })} moduleColor="#a855f7" moduloId={2} nivelId={1} />);

    expect(screen.getByText('20 estudiantes en 4 grupos iguales')).toBeInTheDocument();
    expect(screen.queryByText(/20 elementos/)).not.toBeInTheDocument();
  });

  it('no revela los componentes escalados de una razón', () => {
    render(<Fase5VisualizerEngine pregunta={baseQuestion('ratio_grid', {
      ratio_a: 2,
      ratio_b: 5,
      factor: 4,
    })} moduleColor="#10b981" moduloId={4} nivelId={1} />);

    expect(screen.getByText('Ingrediente A: 2 × 4 = ?')).toBeInTheDocument();
    expect(screen.getByText('Ingrediente B: 5 × 4 = ?')).toBeInTheDocument();
    expect(screen.queryByText(/8:20/)).not.toBeInTheDocument();
    expect(screen.queryByText(/→ 8/)).not.toBeInTheDocument();
  });
});
