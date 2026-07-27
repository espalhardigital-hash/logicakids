"""
Script de Prueba de Renderizado de HTML/SVG
"""

import re

def fix_svg_html(dirty_html):
    if not dirty_html:
        return dirty_html
    
    # 1. Reparar SVGs con viewBox 200x64 (tablas de montos decimales)
    cleaned = re.sub(
        r'<svg[^>]*viewBox=["\']0 (?:68|57) 200 (?:64|86)["\'][^>]*>',
        r'<svg viewBox="0 68 200 64" width="100%" height="102" style="margin:10px auto; display:block; width:100%; max-width:320px; height:102px; min-height:102px; aspect-ratio:200/64; background:#111827; border:2px solid #8B5CF6; border-radius:14px;">',
        dirty_html,
        flags=re.IGNORECASE
    )

    # 2. Reparar cualquier otro SVG sin height explícito
    cleaned = re.sub(
        r'<svg(?![^>]*\bheight=)([^>]*)>',
        r'<svg height="150" style="min-height:100px;" \1>',
        cleaned,
        flags=re.IGNORECASE
    )
    
    return cleaned

sample_enunciado = "Thiago reúne montos en la nota fiscal del almuerzo.<br/><svg viewBox='0 68 200 64' style='margin:10px auto; display:block; width:100%; max-width:320px; height:auto; background:#111827; border:2px solid #8B5CF6; border-radius:14px;'><rect x='10.0' y='78.0' width='180.0' height='44.0' fill='#8B5CF6' fill-opacity='0.10' stroke='#FFFFFF' stroke-width='1' rx='4'/><text x='16.0' y='93.4' fill='#FFFFFF' font-size='11' text-anchor='start'>Monto 1</text><text x='145.0' y='93.4' fill='#8B5CF6' font-size='11' font-weight='bold' text-anchor='middle'>R$ 11,78</text></svg><br/>¿Qué operación calcula el total acumulado?"

print("ORIGINAL:\n", sample_enunciado[:180])
print("\nFIXED:\n", fix_svg_html(sample_enunciado)[:250])
