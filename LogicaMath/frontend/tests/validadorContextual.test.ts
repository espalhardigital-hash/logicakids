import { describe, it, expect } from 'vitest';
import { validarYCorregirParametros } from '../services/validadorContextual';

describe('validarYCorregirParametros', () => {
  it('debe corregir correctamente cuando no se admiten decimales y hay inconsistencia discreta (bucle delta)', () => {
    // Ejemplo: 3 cajas, 10 libros por caja, divisor = 9
    // Respuesta original = 3 * 10 / 9 = 3.3333333333333335 (Inconsistente)
    // Con delta = 2: 3 * (10 + 2) = 36 % 9 === 0 -> cantidadCorregida = 12, respuesta = 4
    const result = validarYCorregirParametros({
      tema: 'aritmetica',
      objeto: 'libros',
      cajas: 3,
      cantidadPorCaja: 10,
      divisor: 9
    });

    expect(result.valido).toBe(false); // Era inválido originalmente
    expect(result.parametrosCorregidos.cantidadPorCaja).toBe(9);
    expect(result.parametrosCorregidos.respuesta).toBe(3);
    expect(result.parametrosCorregidos.respuesta % 1).toBe(0); // Debe ser entero
  });

  it('debe aplicar el fallback matemático de múltiplos del divisor si el bucle delta falla en encontrar solución (delta >= 15)', () => {
    // Escenario problemático donde delta menor a 15 no resolvería la división
    // cajas = 1, cantidadPorCaja = 10, divisor = 30
    // Divisor 30, cajas 1. Bucle delta busca delta < 15:
    // 10 + delta = 10 + 1..14 = 11..24. Ninguno de estos dividido por 30 da entero.
    // 10 - delta = 10 - 1..9 = 9..1. Ninguno de estos dividido por 30 da entero.
    // Aquí el bucle delta fallará (encontrado = false).
    // Con fallback: Math.ceil(10 / 30) * 30 = 1 * 30 = 30.
    // respuesta = 1 * 30 / 30 = 1.
    const result = validarYCorregirParametros({
      tema: 'aritmetica',
      objeto: 'libros',
      cajas: 1,
      cantidadPorCaja: 10,
      divisor: 30
    });

    expect(result.valido).toBe(false);
    expect(result.parametrosCorregidos.cantidadPorCaja).toBe(30);
    expect(result.parametrosCorregidos.respuesta).toBe(1);
    expect(result.parametrosCorregidos.respuesta % 1).toBe(0);
  });

  describe('segmentacion de enunciados para dos pasos', () => {
    it('debe dividir correctamente enunciados estándar separados por punto y espacio', () => {
      const result = validarYCorregirParametros({
        tipo: 'dos_pasos',
        enunciadoTemplate: 'Esta es la primera pregunta. Esta es la segunda.'
      });

      expect(result.enunciadosSegmentados.paso1).toBe('Esta es la primera pregunta.');
      expect(result.enunciadosSegmentados.paso2).toBe('Esta es la segunda.');
    });

    it('debe segmentar enunciados con salto de línea (\\n)', () => {
      const result = validarYCorregirParametros({
        tipo: 'dos_pasos',
        enunciadoTemplate: 'Esta es la primera pregunta.\nEsta es la segunda.'
      });

      expect(result.enunciadosSegmentados.paso1).toBe('Esta es la primera pregunta.');
      expect(result.enunciadosSegmentados.paso2).toBe('Esta es la segunda.');
    });

    it('debe segmentar enunciados que terminan con signos de interrogacion (?)', () => {
      const result = validarYCorregirParametros({
        tipo: 'dos_pasos',
        enunciadoTemplate: '¿Cuántas manzanas hay? Repártelas entre 3.'
      });

      expect(result.enunciadosSegmentados.paso1).toBe('¿Cuántas manzanas hay?');
      expect(result.enunciadosSegmentados.paso2).toBe('Repártelas entre 3.');
    });

    it('debe segmentar enunciados que terminan con signos de exclamacion (!)', () => {
      const result = validarYCorregirParametros({
        tipo: 'dos_pasos',
        enunciadoTemplate: '¡Atención con el cálculo! Calcula el triple de la suma.'
      });

      expect(result.enunciadosSegmentados.paso1).toBe('¡Atención con el cálculo!');
      expect(result.enunciadosSegmentados.paso2).toBe('Calcula el triple de la suma.');
    });
  });
});
