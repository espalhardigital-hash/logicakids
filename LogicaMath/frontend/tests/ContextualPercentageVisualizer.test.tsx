import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { ContextualPercentageVisualizer } from '../components/fase4/ContextualPercentageVisualizer';
import { Fase4VisualizerEngine } from '../components/fase4/Fase4VisualizerEngine';
import type { Fase4Pregunta } from '../components/fase4/Fase4Types';

describe('ContextualPercentageVisualizer Component', () => {
  it('debe renderizar correctamente el tema de bateria', () => {
    render(
      <ContextualPercentageVisualizer
        pct={75}
        total={600}
        inputValue=""
        theme="battery"
        unit="min"
      />
    );

    // Debe mostrar la capacidad total
    expect(screen.getByText('600')).toBeInTheDocument();
    expect(screen.getByText('min')).toBeInTheDocument();
    expect(screen.getByText('al estar lleno')).toBeInTheDocument();
    
    // Debe mostrar el porcentaje
    expect(screen.getByText('75%')).toBeInTheDocument();
    
    // Al estar vacía la respuesta, debe mostrar el placeholder
    expect(screen.getByText('—')).toBeInTheDocument();
    expect(screen.getByText(/restantes/)).toBeInTheDocument();
  });

  it('debe renderizar correctamente el valor ingresado por el usuario', () => {
    render(
      <ContextualPercentageVisualizer
        pct={50}
        total={200}
        inputValue="100"
        theme="download"
        unit="MB"
      />
    );

    expect(screen.getByText('50%')).toBeInTheDocument();
    expect(screen.getByText('100')).toBeInTheDocument();
    expect(screen.getByText(/descargados/)).toBeInTheDocument();
    expect(screen.getByText(/tamaño total/)).toBeInTheDocument();
  });
});

describe('Fase4VisualizerEngine Integration with contextual_bar', () => {
  it('debe renderizar la visualizacion contextual y la caja de ecuacion', () => {
    const mockPregunta: Fase4Pregunta = {
      id: 1,
      enunciado: '¿Cuántos minutos quedan?',
      tipo_pregunta: 'multiple_opcion',
      tiene_cronometro: false,
      datos_numericos: {
        tipo_visual: 'contextual_bar',
        theme: 'battery',
        pct: 25,
        total: 400,
        unit: 'min',
      },
    };

    render(
      <Fase4VisualizerEngine
        pregunta={mockPregunta}
        moduleColor="#10b981"
        moduloId={3}
        nivelId={1}
        respuestaNum="100"
      />
    );

    // Debe mostrar el porcentaje y total en la caja de ecuación
    expect(screen.getByText('25% de 400 =')).toBeInTheDocument();
    
    // 100 aparece dos veces (en la batería y en la caja de ecuación)
    const elements = screen.getAllByText('100');
    expect(elements.length).toBe(2);
  });
});
