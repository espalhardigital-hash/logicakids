"""
app/fase5/svg_helpers.py (shim temporal de re-exportación)
============================================================
Toda la lógica de generación de figuras SVG vive ahora en app.utils.svg_figuras
según la Sección 11 del plan de reestructuración (docs/reestructuraciondefases.md).
"""
from app.utils.svg_figuras import *  # noqa: F401,F403
