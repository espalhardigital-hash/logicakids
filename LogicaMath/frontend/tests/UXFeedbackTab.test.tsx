// @vitest-environment jsdom
import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { UXFeedbackTab } from '../components/admin/UXFeedbackTab';

// Mock de lucide-react para evitar problemas en el entorno de pruebas de JSDOM
vi.mock('lucide-react', () => ({
  ShieldAlert: () => <span>ShieldAlert</span>,
  CheckCircle: () => <span>CheckCircle</span>,
  Clock: () => <span>Clock</span>,
  Trash2: () => <span>Trash2</span>,
  Filter: () => <span>Filter</span>,
  Code: () => <span>Code</span>,
}));

// Mock del storage de token
vi.mock('../../services/authService', () => ({
  getStoredToken: () => 'mock-token',
}));

describe('UXFeedbackTab Component', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('debe renderizar cargando al inicio y luego el buzón de feedbacks', async () => {
    const mockFeedbacks = [
      {
        id: 1,
        fase: 4,
        modulo_id: 1,
        nivel_id: 1,
        dom_selector: 'div.f4-pizza',
        comentario: 'Corregir colores de la pizza',
        tipo: 'bug_visual',
        prioridad: 'alta',
        estado: 'pendiente',
        fecha_creacion: new Date().toISOString(),
      }
    ];

    // Mock del fetch global
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => mockFeedbacks,
    });
    vi.stubGlobal('fetch', fetchMock);

    render(<UXFeedbackTab />);

    // Comprobar que muestra el título del buzón
    expect(screen.getByText('Buzón de Mejorías UX & QA')).toBeInTheDocument();

    // Esperar a que cargue la información del feedback
    await waitFor(() => {
      expect(screen.getByText('Corregir colores de la pizza')).toBeInTheDocument();
    });

    expect(screen.getAllByText('Fase 4').length).toBeGreaterThan(0);
    expect(screen.getByText('div.f4-pizza')).toBeInTheDocument();
  });

  it('debe mostrar mensaje si el listado está vacío', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => [],
    });
    vi.stubGlobal('fetch', fetchMock);

    render(<UXFeedbackTab />);

    await waitFor(() => {
      expect(screen.getByText('No se encontraron anotaciones de UX con los filtros seleccionados.')).toBeInTheDocument();
    });
  });
});
