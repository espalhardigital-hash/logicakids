// @vitest-environment jsdom
import { describe, it, expect } from 'vitest';
import { getUniqueSelector } from '../components/common/UXFeedbackOverlay';

describe('getUniqueSelector', () => {
  it('debe devolver el ID del elemento si existe', () => {
    const div = document.createElement('div');
    div.id = 'mi-boton-especial';
    document.body.appendChild(div);

    const selector = getUniqueSelector(div);
    expect(selector).toBe('#mi-boton-especial');

    document.body.removeChild(div);
  });

  it('debe construir un selector semántico con clases de LógicaKids', () => {
    const parent = document.createElement('main');
    parent.className = 'f4-screen-wrapper';
    
    const child = document.createElement('div');
    child.className = 'f4-pizza-visualizer active';
    
    parent.appendChild(child);
    document.body.appendChild(parent);

    const selector = getUniqueSelector(child);
    expect(selector).toBe('main.f4-screen-wrapper > div.f4-pizza-visualizer');

    document.body.removeChild(parent);
  });

  it('debe usar data-component si está definido', () => {
    const card = document.createElement('div');
    card.setAttribute('data-component', 'Fase4TheoryModal');
    document.body.appendChild(card);

    const selector = getUniqueSelector(card);
    expect(selector).toBe('[data-component="Fase4TheoryModal"]');

    document.body.removeChild(card);
  });

  it('debe subir automáticamente al contenedor semántico de UI si se cliquea un texto interno', () => {
    const modal = document.createElement('div');
    modal.className = 'fase4-theory-modal';

    const card = document.createElement('div');
    card.className = 'theory-card';

    const span = document.createElement('span');
    span.textContent = 'Texto explicativo del nivel';

    card.appendChild(span);
    modal.appendChild(card);
    document.body.appendChild(modal);

    const selector = getUniqueSelector(span);
    expect(selector).toContain('div.fase4-theory-modal > div.theory-card > span');

    document.body.removeChild(modal);
  });
});
