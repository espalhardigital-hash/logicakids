"""
Test de integridad numérica y coherencia semántica para la Fase 4.
Garantiza que el 100% del pool generado de la Fase 4 produzca únicamente:
- Resultados numéricos exactos (enteros o decimales finitos con máximo 2 cifras decimales).
- Ausencia de números periódicos (ej. 1,5701...).
- Ausencia de marcadores sin formatear.
"""

import pytest
from app.fase4.compositor_fase4 import CompositorFase4

def test_fase4_precision_y_sin_periodicos():
    compositor = CompositorFase4()
    total_evaluadas = 0

    for modulo_id in range(1, 5):
        for nivel_id in range(1, 4):
            for fam_idx in range(72):
                for var_idx in range(4):
                    seed_val = 1000 + modulo_id * 100 + nivel_id * 10 + fam_idx * 4 + var_idx
                    q = compositor.componer_pregunta_practica(
                        modulo_id=modulo_id,
                        nivel_id=nivel_id,
                        fam_idx=fam_idx,
                        var_idx=var_idx,
                        seed_val=seed_val,
                    )
                    
                    resultado_num = q["resultado_num"]
                    # 1. El resultado numérico debe ser exacto a 2 decimales
                    assert abs(resultado_num - round(resultado_num, 2)) < 1e-6, (
                        f"Pregunta {q['plantilla_id']} produjo resultado no exacto/periódico: {resultado_num}"
                    )
                    
                    # 2. La respuesta correcta formateada no debe tener más de 2 decimales tras la coma
                    resp_str = q["respuesta_correcta"].replace(',', '.')
                    if '.' in resp_str:
                        partes = resp_str.split('.')
                        assert len(partes[1]) <= 2, (
                            f"Respuesta {q['respuesta_correcta']} supera 2 decimales en {q['plantilla_id']}"
                        )
                    
                    # 3. El enunciado no debe tener placeholders crudos
                    enunciado = q["enunciado"]
                    assert "{" not in enunciado and "}" not in enunciado, (
                        f"Enunciado contiene placeholders crudos: {enunciado}"
                    )
                    
                    total_evaluadas += 1

    assert total_evaluadas == 3456
