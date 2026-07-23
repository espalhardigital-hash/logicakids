// @vitest-environment jsdom
import React from 'react';
import { render, screen, waitFor, fireEvent, within } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import PedagogyTab from './PedagogyTab';

// Mock matchMedia for jsdom
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(), // deprecated
    removeListener: vi.fn(), // deprecated
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock services that do API calls
vi.mock('../../services/storageService', () => ({
  getAdminSettings: vi.fn().mockResolvedValue(null),
  saveAdminSettings: vi.fn().mockResolvedValue(true),
  getModularConfigs: vi.fn().mockResolvedValue([]),
  saveModularConfig: vi.fn().mockResolvedValue(true),
  createModularConfig: vi.fn().mockResolvedValue(true),
}));

describe('PedagogyTab', () => {
  it('renders the master-detail layout without crashing', async () => {
    const { container } = render(<PedagogyTab />);

    expect(await screen.findByText(/Cargando base de datos pedagógica/i)).not.toBeNull();

    await waitFor(() => {
      expect(screen.getByText(/Configuración Pedagógica/i)).not.toBeNull();
    }, { timeout: 3000 });

    // Nav tree renders the global entry and the phase list, defaulting to Fase 1's panel
    expect(screen.getByRole('button', { name: /Plataforma Global/i })).not.toBeNull();
    expect(screen.getByText(/Fase 1: Aritmética Básica/i)).not.toBeNull();

    // Fase 9 is present but locked (not yet redesigned)
    expect(screen.getByText(/^Fase 9$/)).not.toBeNull();
  });

  it('applies bulk values to every row of a module grid on "Aplicar a todas"', async () => {
    render(<PedagogyTab />);
    await waitFor(() => {
      expect(screen.getByText(/Configuración Pedagógica/i)).not.toBeNull();
    }, { timeout: 3000 });

    fireEvent.click(screen.getByRole('button', { name: /^Fase 2$/ }));
    fireEvent.click(await screen.findByRole('button', { name: /Módulo 2/i }));

    const grid = await screen.findByRole('table');
    const rowsBefore = within(grid).getAllByRole('row').slice(1); // drop header row
    expect(rowsBefore.length).toBe(7); // 4 niveles + 3 desafíos

    // None of the rows should have an own override yet
    expect(within(grid).getAllByText(/heredado/i).length).toBe(7);

    const applyButton = screen.getByRole('button', { name: /Aplicar a las 7 filas/i });
    const applyBar = applyButton.parentElement as HTMLElement;
    const applyQtyInput = within(applyBar).getAllByRole('spinbutton')[0];
    fireEvent.change(applyQtyInput, { target: { value: '33' } });

    fireEvent.click(applyButton);

    await waitFor(() => {
      const qtyInputs = within(grid).getAllByRole('spinbutton').filter((_, i) => i % 3 === 0);
      expect(qtyInputs.every(input => (input as HTMLInputElement).value === '33')).toBe(true);
    });

    // Every row now carries its own rule (revert control) instead of "heredado"
    expect(within(grid).queryAllByText(/heredado/i).length).toBe(0);
  });

  it('cascades a phase-wide "Desafío 1" default to a module that has no override of its own', async () => {
    render(<PedagogyTab />);
    await waitFor(() => {
      expect(screen.getByText(/Configuración Pedagógica/i)).not.toBeNull();
    }, { timeout: 3000 });

    fireEvent.click(screen.getByRole('button', { name: /^Fase 2$/ }));

    const challengesTable = await screen.findByRole('table');
    const d1PhaseRow = within(challengesTable).getByText(/Desafío 1 \(Estándar\)/i).closest('tr') as HTMLElement;
    const d1PhaseTimer = within(d1PhaseRow).getAllByRole('spinbutton')[2];
    fireEvent.change(d1PhaseTimer, { target: { value: '77' } });

    await waitFor(() => {
      expect((d1PhaseTimer as HTMLInputElement).value).toBe('77');
    });

    fireEvent.click(await screen.findByRole('button', { name: /^Módulo 1$/ }));

    const moduleTable = await screen.findByRole('table');
    const d1ModuleRow = within(moduleTable).getByText(/Desafío 1 \(Estándar\)/i).closest('tr') as HTMLElement;
    const d1ModuleTimer = within(d1ModuleRow).getAllByRole('spinbutton')[2];

    await waitFor(() => {
      expect((d1ModuleTimer as HTMLInputElement).value).toBe('77');
    });
  });
});
