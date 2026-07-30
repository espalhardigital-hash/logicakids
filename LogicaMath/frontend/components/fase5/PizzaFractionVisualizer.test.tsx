import React from 'react';
import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import { PizzaFractionVisualizer } from './PizzaFractionVisualizer';

describe('PizzaFractionVisualizer', () => {
  it('debería renderizarse con el tamaño size por defecto de 200', () => {
    const { container } = render(
      <PizzaFractionVisualizer slices={8} />
    );
    const svg = container.querySelector('svg');
    expect(svg).toBeDefined();
    expect(svg?.getAttribute('width')).toBe('200');
    expect(svg?.getAttribute('height')).toBe('200');
  });

  it('debería respetar la propiedad size personalizada', () => {
    const { container } = render(
      <PizzaFractionVisualizer slices={8} size={110} />
    );
    const svg = container.querySelector('svg');
    expect(svg).toBeDefined();
    expect(svg?.getAttribute('width')).toBe('110');
    expect(svg?.getAttribute('height')).toBe('110');
  });
});
