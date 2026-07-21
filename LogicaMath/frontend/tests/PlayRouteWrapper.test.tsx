import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { PlayRouteWrapper } from '../components/PlayRouteWrapper';

// Mock de GameScreen
vi.mock('../components/fase1/GameScreen', () => {
  return {
    default: (props: any) => (
      <div data-testid="mock-game-screen" data-seccion={props.seccion}>
        Mock Game Screen ({props.category} - {props.difficulty})
      </div>
    )
  };
});

describe('PlayRouteWrapper', () => {
  it('debe calcular la seccion modular correctamente y renderizar GameScreen', async () => {
    const mockNavigate = vi.fn();
    const mockEndGame = vi.fn();

    render(
      <PlayRouteWrapper
        category="addition"
        difficulty="medium"
        currentUser={{ settings: { sound: true }, fase_actual_id: 2 }}
        adminConfig={{}}
        modularConfigs={[]}
        isEvaluatorMode={false}
        handleEndGame={mockEndGame}
        navigate={mockNavigate}
      />
    );

    // Verificar que se renderiza el GameScreen mockeado usando findByTestId para esperar a Suspense
    const element = await screen.findByTestId('mock-game-screen');
    expect(element).toBeInTheDocument();
    
    // addition = 1 (modId), medium = 3 (levelId) -> seccion = 1 * 100 + 3 = 103
    expect(element.getAttribute('data-seccion')).toBe('103');
  });
});
