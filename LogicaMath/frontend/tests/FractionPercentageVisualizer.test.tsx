import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import { FractionPercentageVisualizer } from '../components/fase5/FractionPercentageVisualizer';

describe('FractionPercentageVisualizer', () => {
  it('renders progress bar and equation correctly for percentages', () => {
    render(
      <FractionPercentageVisualizer
        percentage={25}
        total={80}
        color="#3b82f6"
        interactive={false}
      />
    );

    // Expecting 25% de 80 to be visible
    expect(screen.getByText(/25% de 80 =/i)).toBeInTheDocument();
    expect(screen.getByText(/× 80/i)).toBeInTheDocument();
  });

  it('renders fraction layout instead of percentage if percentage prop is not provided', () => {
    render(
      <FractionPercentageVisualizer
        percentage={0}
        total={20}
        color="#10b981"
        interactive={false}
      />
    );

    // Expecting Fracción de 20 to be visible
    expect(screen.getByText(/Fracción de 20 =/i)).toBeInTheDocument();
  });
});
