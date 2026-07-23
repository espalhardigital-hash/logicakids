// @vitest-environment jsdom
import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import SreTab from '../components/admin/SreTab';

// Mock de lucide-react
vi.mock('lucide-react', () => ({
  CheckCircle2: () => <span>CheckCircle2</span>,
  AlertTriangle: () => <span>AlertTriangle</span>,
  RefreshCw: () => <span>RefreshCw</span>,
  Server: () => <span>Server</span>,
  Shield: () => <span>Shield</span>,
  Cpu: () => <span>Cpu</span>,
  Activity: () => <span>Activity</span>,
  ListChecks: () => <span>ListChecks</span>,
  Play: () => <span>Play</span>,
  History: () => <span>History</span>,
  Sparkles: () => <span>Sparkles</span>,
}));

describe('SreTab Component (Pruebas Unitarias de Terreno)', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    vi.stubGlobal('fetch', undefined as any);
  });

  it('debe cargar métricas desde el servidor Nginx estático cuando está disponible', async () => {
    const mockSreData = {
      generated_at: new Date().toISOString(),
      environment: 'LOCAL',
      version: '1.4.2',
      summary: {
        total_tests: 41,
        passed: 41,
        failed: 0,
        skipped: 0,
        duration_seconds: 9.7,
      },
      suites: [
        { name: 'Database Connectivity', passed: true },
        { name: 'Frontend Vitest Tests', passed: true },
      ],
      note: 'Todas las compuertas pasaron.',
    };

    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => mockSreData,
    });
    vi.stubGlobal('fetch', fetchMock);

    render(<SreTab />);

    // Título principal
    expect(screen.getByText(/Principios ENG \/ SRE & Calidad/i)).toBeInTheDocument();

    // Esperar a que carguen las métricas
    await waitFor(() => {
      expect(screen.getByText('100%')).toBeInTheDocument();
    });

    expect(screen.getByText(/41 de 41 Pruebas E2E aprobadas/i)).toBeInTheDocument();
    expect(screen.getByText('Database Connectivity')).toBeInTheDocument();
  });

  it('debe activar MODO FALLBACK (BACKEND API) cuando el servidor de reportes estático falla', async () => {
    const fallbackData = {
      generated_at: new Date().toISOString(),
      environment: 'LOCAL',
      version: '1.4.2',
      is_fallback: true,
      summary: {
        total_tests: 41,
        passed: 41,
        failed: 0,
        skipped: 0,
        duration_seconds: 9.7,
      },
      suites: [
        { name: 'FastAPI Admin Routers & SRE Resilience', passed: true },
      ],
      note: 'Servido dinámicamente por la API Backend FastAPI (Modo Fallback).',
    };

    // La primera llamada a Nginx falla (404/red), la segunda llamada a /api/admin/sre/status es exitosa
    const fetchMock = vi.fn().mockImplementation((url: string) => {
      if (url.includes('9323')) {
        return Promise.reject(new Error('Network error on 9323'));
      }
      if (url.includes('/admin/sre/status')) {
        return Promise.resolve({
          ok: true,
          json: async () => fallbackData,
        });
      }
      if (url.includes('/admin/sre/history')) {
        return Promise.resolve({
          ok: true,
          json: async () => [],
        });
      }
      return Promise.reject(new Error('Unknown url'));
    });

    vi.stubGlobal('fetch', fetchMock);

    render(<SreTab />);

    // Debe mostrar la insignia MODO FALLBACK
    await waitFor(() => {
      expect(screen.getByText(/MODO FALLBACK \(BACKEND API\)/i)).toBeInTheDocument();
    });

    expect(screen.getByText('FastAPI Admin Routers & SRE Resilience')).toBeInTheDocument();
  });

  it('debe permitir ejecutar la verificación manual SRE al presionar "Ejecutar Verificación SRE"', async () => {
    const refreshedData = {
      generated_at: new Date().toISOString(),
      environment: 'LOCAL',
      version: '1.4.2',
      summary: {
        total_tests: 41,
        passed: 41,
        failed: 0,
        skipped: 0,
        duration_seconds: 8.5,
      },
      suites: [
        { name: 'Verificación Manual Ejecutada', passed: true }
      ],
      note: 'Verificación manual realizada con éxito.'
    };

    const fetchMock = vi.fn().mockImplementation((url: string, opts?: any) => {
      if (opts?.method === 'POST' && url.includes('/admin/sre/refresh')) {
        return Promise.resolve({
          ok: true,
          json: async () => ({ status: 'ok', report: refreshedData }),
        });
      }
      return Promise.resolve({
        ok: true,
        json: async () => refreshedData,
      });
    });

    vi.stubGlobal('fetch', fetchMock);

    render(<SreTab />);

    await waitFor(() => {
      expect(screen.getByText('Ejecutar Verificación SRE')).toBeInTheDocument();
    });

    const runBtn = screen.getByText('Ejecutar Verificación SRE');
    fireEvent.click(runBtn);

    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledWith(
        expect.stringContaining('/admin/sre/refresh'),
        expect.objectContaining({ method: 'POST' })
      );
    });
  });
});
