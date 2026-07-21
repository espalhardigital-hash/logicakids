import { describe, it, expect } from 'vitest';
import Fase4GameScreen from '../components/fase4/Fase4GameScreen';

const isDiscreteQuestion = (enunciado: string): boolean => {
  const lowercase = (enunciado || '').toLowerCase();
  const palabrasDiscretas = [
    'figurita', 'carta', 'manzana', 'moneda', 'tazo', 
    'galleta', 'chocolate', 'dulce', 'juguete', 'cupcake', 'caramelos'
  ];
  return palabrasDiscretas.some(palabra => lowercase.includes(palabra));
};

describe('isDiscreteQuestion', () => {
  it('debe detectar correctamente colecciones discretas', () => {
    expect(isDiscreteQuestion('Sofía tenía 40 figuritas. Regaló 6/10 del total a sus amigos. ¿Cuántos figuritas le QUEDAN a Sofía?')).toBe(true);
    expect(isDiscreteQuestion('Mateo tiene 30 cartas. Regala 1/3. ¿Cuántas cartas le quedan?')).toBe(true);
    expect(isDiscreteQuestion('Un cofre contiene 15 monedas de oro.')).toBe(true);
    expect(isDiscreteQuestion('Tengo 8 tazos en mi bolsillo.')).toBe(true);
  });

  it('debe retornar false para conceptos continuos, de volumen o pizzas', () => {
    expect(isDiscreteQuestion('Un tanque tiene 50 litros de agua.')).toBe(false);
    expect(isDiscreteQuestion('Un círculo está dividido en 5 partes iguales.')).toBe(false);
    expect(isDiscreteQuestion('Sofía necesita colorear la pizza para formar 3/4.')).toBe(false);
  });
});
