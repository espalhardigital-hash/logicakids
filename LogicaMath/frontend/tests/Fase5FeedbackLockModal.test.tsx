import React from 'react';
import { act, fireEvent, render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { Fase5FeedbackLockModal } from '../components/fase5/Fase5FeedbackLockModal';
import type { Fase5AnswerResult } from '../components/fase5/Fase5Types';

const incorrectResult: Fase5AnswerResult = {
  es_correcta: false,
  respuesta_correcta: '12',
  feedback_error: 'Multiplica ambos términos por el mismo factor.',
  aciertos_acumulados: 0,
  intentos_totales: 1,
  porcentaje_actual: 0,
  bloque_completado: false,
  fase_completada: false,
  early_exit: false,
  pausa_obligatoria_segundos: 10,
  explicacion: {
    pasos: [
      { orden: 1, texto: 'Identifica el denominador 6.' },
      { orden: 2, texto: 'Usa el factor 2.' },
      { orden: 3, texto: 'Multiplica 6 × 2.' },
      { orden: 4, texto: 'El denominador es 12.' },
    ],
  },
};

describe('Fase5FeedbackLockModal', () => {
  afterEach(() => vi.useRealTimers());

  it('bloquea continuar durante 10 segundos y exige leer todas las páginas', () => {
    vi.useFakeTimers();
    const onContinue = vi.fn();
    render(<Fase5FeedbackLockModal resultado={incorrectResult} moduleColor="#8b5cf6" onContinue={onContinue} />);

    const continueButton = screen.getByRole('button', { name: 'Continuar' });
    expect(screen.getByText(/la respuesta correcta es/i)).toHaveTextContent('12');
    expect(screen.getByText(/lee la solución: 10 s/i)).toBeInTheDocument();
    expect(continueButton).toBeDisabled();

    for (let second = 0; second < 10; second += 1) {
      act(() => vi.advanceTimersByTime(1_000));
    }
    expect(screen.getByText(/ya puedes continuar/i)).toBeInTheDocument();
    expect(continueButton).toBeDisabled();

    fireEvent.click(screen.getByRole('button', { name: 'Siguiente' }));
    expect(screen.getByText('El denominador es 12.')).toBeInTheDocument();
    expect(continueButton).toBeEnabled();
    fireEvent.click(continueButton);
    expect(onContinue).toHaveBeenCalledTimes(1);
  });
});
