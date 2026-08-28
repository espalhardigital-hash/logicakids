import React from 'react';
import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import { CustomKeyboard } from '../components/common/CustomKeyboard';

describe('accesibilidad del teclado numérico', () => {
  it('nombra los controles que solo muestran iconos', () => {
    render(
      <CustomKeyboard
        onNumberPress={vi.fn()}
        onDelete={vi.fn()}
        onSubmit={vi.fn()}
        allowDecimal
      />,
    );

    expect(screen.getByRole('button', { name: 'Borrar último dígito' })).toBeTruthy();
    expect(screen.getByRole('button', { name: 'Separador decimal' })).toBeTruthy();
    expect(screen.getByRole('button', { name: 'Confirmar respuesta' })).toBeTruthy();
  });
});
