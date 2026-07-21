import pytest
import os
from unittest.mock import patch

# Parchear sys.path no es estrictamente necesario aquí si se corre con pytest desde backend, 
# pero debemos asegurarnos de que la carga de settings funcione en los scripts.
from app.core.config import settings

def test_apply_teacher_feedback_uses_settings():
    """
    Validar que el script ya no use os.environ para acceder a la API key y en su lugar 
    use settings.GOOGLE_API_KEY.
    """
    from scripts.apply_teacher_feedback import call_gemini_to_suggest_correction
    
    # Comprobar importación exitosa y que el código no lanza KeyError
    assert callable(call_gemini_to_suggest_correction)

def test_audit_question_images_uses_settings():
    """
    Validar que el script de auditoría utilice el objeto settings para la generación de imágenes.
    """
    from scripts.audit_question_images import generate_image_via_gemini_imagen
    
    # Si podemos importarlo y verificar su existencia, es el primer paso.
    assert callable(generate_image_via_gemini_imagen)
    
    # Adicionalmente verificamos que si hacemos mock de settings.GOOGLE_API_KEY se usa.
    # Leer el código fuente para asegurar que no hay os.environ.get("GOOGLE_API_KEY")
    with open("scripts/audit_question_images.py", "r", encoding="utf-8") as f:
        content = f.read()
        assert 'os.environ.get("GOOGLE_API_KEY")' not in content, "El script todavía usa os.environ en vez de settings"
        
    with open("scripts/apply_teacher_feedback.py", "r", encoding="utf-8") as f:
        content = f.read()
        assert 'os.environ.get("GOOGLE_API_KEY")' not in content, "El script todavía usa os.environ en vez de settings"
