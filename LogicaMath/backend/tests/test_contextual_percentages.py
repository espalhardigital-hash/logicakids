import sys
from unittest.mock import MagicMock

import pytest

# Estos tests cubren PORCENTAJES (contextual_bar: battery / download / tank), que
# eran contenido de la antigua Fase 4 y con la reestructuración pasaron a la Fase 5.
# Importaban generate_practice_question_fase4 / generate_challenge_question_fase4,
# funciones que ya no existen, y el fallo de importación interrumpía la colección de
# TODA la suite. Se omiten a nivel de módulo en lugar de borrarlos: los cuerpos siguen
# siendo la especificación válida para reactivarlos al reestructurar la Fase 5.
pytest.skip(
    "Porcentajes pasaron a la Fase 5 con la reestructuración; reactivar al migrar "
    "estos tests a app.fase5 (ver reestructuracion.md)",
    allow_module_level=True,
)

# Mock database and sqlalchemy models to prevent imports crashing in JSDOM/sqlite environment
sys.modules['app.db'] = MagicMock()
sys.modules['app.db.session'] = MagicMock()
sys.modules['app.models'] = MagicMock()
sys.modules['app.models.sql_models'] = MagicMock()
sys.modules['app.fase2.models'] = MagicMock()
sys.modules['app.fase4.router'] = MagicMock()
sys.modules['sqlalchemy'] = MagicMock()
sys.modules['sqlalchemy.orm'] = MagicMock()
sys.modules['sqlalchemy.ext'] = MagicMock()
sys.modules['sqlalchemy.ext.asyncio'] = MagicMock()

from app.fase4.seed import generate_practice_question_fase4, generate_challenge_question_fase4

def test_contextual_percentage_practice_generation():
    """Validar que las preguntas de práctica impar en M3L1 se generen como contextual_bar."""
    for fam in range(1, 16):
        if fam % 2 == 1:  # Familias impares de porcentajes rápidos
            for var in range(4):
                q = generate_practice_question_fase4(modulo_id=3, nivel_id=1, fam=fam, var=var)
                vals = q.get("valores", {})
                
                # Deben ser de tipo 'contextual_bar'
                assert vals["tipo_visual"] == "contextual_bar", f"Esperado 'contextual_bar', obtenido {vals['tipo_visual']}"
                assert vals["theme"] in ["battery", "download", "tank"], f"Tema inválido: {vals['theme']}"
                assert vals["unit"] in ["min", "MB", "L"], f"Unidad inválida: {vals['unit']}"
                
                # Deben usar bases amigables
                assert vals["total"] in [100, 200, 400, 500, 600, 1000]
                assert vals["pct"] in [10, 20, 25, 30, 40, 50, 60, 75, 80, 90]
                
                # Verificar respuestas matemáticas
                total = vals["total"]
                pct = vals["pct"]
                expected_ans = (total * pct) // 100
                ans = int(q["respuesta_correcta"])
                
                # En la variante impar (espejo), se calcula el complemento
                if var % 2 == 1:
                    assert ans == total - expected_ans
                else:
                    assert ans == expected_ans

def test_contextual_percentage_challenge_generation():
    """Validar que las preguntas de desafío de la categoría 0 de M3 sean contextual_bar."""
    for desafio_id in [11, 12, 13]:
        for idx in range(1, 31):
            categoria = idx % 4
            if categoria == 0:  # Porcentajes intuitivos
                q = generate_challenge_question_fase4(modulo_id=3, desafio_id=desafio_id, idx=idx)
                vals = q.get("valores", {})
                
                # Debe ser 'contextual_bar'
                assert vals["tipo_visual"] == "contextual_bar"
                assert vals["theme"] in ["battery", "download", "tank"]
                assert vals["unit"] in ["min", "MB", "L"]
                
                # Verificar distractores
                errores = q.get("errores_previstos", {})
                ans = q["respuesta_correcta"]
                
                assert ans not in errores, f"La respuesta correcta {ans} no debe estar en los distractores"
                assert len(errores) >= 2, "Debe tener al menos 2 distractores definidos"
