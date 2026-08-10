"""
Test de verificación para la Etapa 4: Exactitud Matemática y Concordancia Semántica.
Verifica que el compositor de Fase 5 no genere decimales periódicos no enteros en promedios (M3N3)
ni en mezclas (M4N3), y que se respete la concordancia gramatical y de magnitudes.
"""

import random
import pytest
from app.fase5.compositor_fase5 import CompositorFase5


def test_m3n3_promedios_siempre_enteros():
    """BUG-20: M3N3 promedios debe producir resultados enteros en 100 de 100 muestras."""
    comp = CompositorFase5()
    for fam in range(12):
        for var in range(10):
            seed_val = 300000 + fam * 10 + var
            data = comp.componer_pregunta_practica(modulo_id=3, nivel_id=3, fam_idx=fam, var_idx=var, seed_val=seed_val)
            resultado = data["resultado_num"]
            assert float(resultado).is_integer(), f"M3N3 produjo decimal no entero: {resultado} en {data['enunciado']}"


def test_m4n3_porcentaje_mezclas_siempre_entero():
    """BUG-21: M4N3 mezclas debe producir resultados enteros en 100 de 100 muestras."""
    comp = CompositorFase5()
    for fam in range(12):
        for var in range(10):
            seed_val = 400000 + fam * 10 + var
            data = comp.componer_pregunta_practica(modulo_id=4, nivel_id=3, fam_idx=fam, var_idx=var, seed_val=seed_val)
            resultado = data["resultado_num"]
            assert float(resultado).is_integer(), f"M4N3 produjo decimal no entero: {resultado} en {data['enunciado']}"


def test_preguntas_no_monetarias_son_enteras():
    """BUG-22: Ninguna pregunta de conteo u objetos debe tener respuesta decimal."""
    comp = CompositorFase5()
    for m in (1, 2, 3, 4):
        for n in (1, 2, 3):
            for fam in range(5):
                for var in range(4):
                    seed_val = m * 10000 + n * 1000 + fam * 10 + var
                    data = comp.componer_pregunta_practica(m, n, fam, var, seed_val)
                    res = data["resultado_num"]
                    escenario_id = data["escenario_id"]
                    if "dinero" not in escenario_id and "precio" not in escenario_id:
                        assert float(res).is_integer(), f"Pregunta no monetaria M{m}N{n} ({escenario_id}) dio decimal: {res}"
