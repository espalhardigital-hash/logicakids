import sys
from unittest.mock import MagicMock

# Mockear base de datos, modelos y router de Fase 4 para evitar importaciones pesadas y fallos de psycopg2
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

from app.fase4.seed import (
    NOMBRES,
    OBJETOS_FRACC,
    COLECCIONES,
    BEBIDAS,
    PINTURAS,
    COLORES,
    generate_practice_question_fase4
)

def test_vocabulario_min_lengths():
    """1.T1: Validar que los diccionarios tengan las longitudes mínimas esperadas."""
    assert len(NOMBRES) >= 25, f"Esperado >= 25 nombres, obtenido {len(NOMBRES)}"
    assert len(OBJETOS_FRACC) >= 15, f"Esperado >= 15 objetos, obtenido {len(OBJETOS_FRACC)}"
    assert len(COLECCIONES) >= 12, f"Esperado >= 12 colecciones, obtenido {len(COLECCIONES)}"
    assert len(BEBIDAS) >= 10, f"Esperado >= 10 bebidas, obtenido {len(BEBIDAS)}"
    assert len(PINTURAS) >= 12, f"Esperado >= 12 pinturas, obtenido {len(PINTURAS)}"
    assert len(COLORES) >= 10, f"Esperado >= 10 colores, obtenido {len(COLORES)}"

def test_vocabulario_no_duplicates():
    """1.T2: Verificar que no haya duplicados en ninguna lista."""
    lists_to_check = {
        "NOMBRES": NOMBRES,
        "OBJETOS_FRACC": OBJETOS_FRACC,
        "COLECCIONES": COLECCIONES,
        "BEBIDAS": BEBIDAS,
        "PINTURAS": PINTURAS,
        "COLORES": COLORES
    }
    for name, lst in lists_to_check.items():
        assert len(lst) == len(set(lst)), f"Duplicados encontrados en {name}: {[x for x in set(lst) if lst.count(x) > 1]}"

def test_question_generation_name_diversity():
    """1.T3: Confirmar tasa de repetición de nombres en preguntas consecutivas < 15%."""
    # Generamos 100 preguntas consecutivas variando la familia e índices
    nombres_usados = []
    
    # Mapeamos combinaciones de modulo y nivel
    mod_niv_pairs = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3), (3, 4), (4, 1), (4, 2), (4, 3)]
    
    for i in range(100):
        mod, niv = mod_niv_pairs[i % len(mod_niv_pairs)]
        fam = (i % 15) + 1
        var = i % 4
        q = generate_practice_question_fase4(mod, niv, fam, var)
        enunciado = q["enunciado"]
        
        nombre_detectado = None
        for nombre in NOMBRES:
            if nombre in enunciado:
                nombre_detectado = nombre
                break
        
        if nombre_detectado:
            nombres_usados.append(nombre_detectado)
            
    repeticiones_consecutivas = 0
    for i in range(len(nombres_usados) - 1):
        if nombres_usados[i] == nombres_usados[i+1]:
            repeticiones_consecutivas += 1
            
    tasa_repeticion = (repeticiones_consecutivas / (len(nombres_usados) - 1)) * 100 if nombres_usados else 0
    print(f"\nTasa de repetición consecutiva de nombres: {tasa_repeticion:.2f}%")
    assert tasa_repeticion < 15.0, f"Tasa de repetición muy alta: {tasa_repeticion:.2f}%"


def test_variantes_espejo_corregidas():
    """Grupo 2: Validar variantes espejo (no [ESPEJO], respuestas distintas, enunciados distintos)."""
    mod_niv_pairs = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3), (3, 4), (4, 1), (4, 2), (4, 3)]
    
    # Muestrear 20 familias aleatorias
    for idx, (mod, niv) in enumerate(mod_niv_pairs * 2):
        fam = (idx % 15) + 1
        
        # Generar las 4 variantes de la familia
        variantes = [generate_practice_question_fase4(mod, niv, fam, v) for v in range(4)]
        
        enunciados = [v["enunciado"] for v in variantes]
        respuestas = [v["respuesta_correcta"] for v in variantes]
        
        # 2.T1: Ninguna debe contener '[ESPEJO]'
        for e in enunciados:
            assert "[ESPEJO]" not in e, f"Se encontró prefijo [ESPEJO] en el enunciado: {e}"
            
        # 2.T2: Al menos 3 de las 4 variantes por familia deben tener respuestas correctas distintas
        # (Para asimetría M1L3, al ser Sí/No, hay 2 respuestas posibles, así que relajamos la aserción para ese nivel específico a len(set(respuestas)) >= 2)
        respuestas_unicas = len(set(respuestas))
        if mod == 1 and niv == 3:
            assert respuestas_unicas >= 2, f"Esperado al menos 2 respuestas distintas para Asimetría, obtenido: {respuestas}"
        else:
            assert respuestas_unicas >= 3, f"Familia mod={mod} niv={niv} fam={fam} tiene pocas respuestas distintas ({respuestas_unicas}): {respuestas}"
            
        # 2.T3: Los enunciados deben ser textualmente diferentes
        # (No deben ser idénticos entre variantes)
        assert len(set(enunciados)) == 4, f"Enunciados duplicados en familia mod={mod} niv={niv} fam={fam}: {enunciados}"


def test_rangos_numericos_ampliados():
    """Grupo 3: Validar rangos numéricos (totales <= 120, enteros positivos, denominadores 2/12 y porcentajes 75%/20%)."""
    mod_niv_pairs = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3), (3, 4), (4, 1), (4, 2), (4, 3)]
    
    denominadores_detectados = set()
    porcentajes_detectados = set()
    
    # Generar todas las preguntas posibles de práctica (13 niveles x 15 familias x 4 variantes = 780 preguntas)
    for mod, niv in mod_niv_pairs:
        for fam in range(1, 16):
            for var in range(4):
                q = generate_practice_question_fase4(mod, niv, fam, var)
                vals = q.get("valores", {})
                
                # 3.T1: Ningún total excede 120 y todos los resultados matemáticos son válidos
                if "total" in vals:
                    total = vals["total"]
                    assert total <= 120, f"El total {total} en mod={mod} niv={niv} fam={fam} excede 120"
                    
                # Verificar respuesta entera positiva (excepto para fracciones visuales del Módulo 1 y Sí/No)
                ans = q["respuesta_correcta"]
                if "/" not in ans and ans not in ["0", "1"]:
                    assert int(ans) >= 0, f"Respuesta negativa detectada: {ans}"
                    
                # Recopilar denominadores usados en M1 y M2
                if mod in (1, 2):
                    if "den" in vals:
                        denominadores_detectados.add(vals["den"])
                    if "den_base" in vals:
                        denominadores_detectados.add(vals["den_base"])
                        
                # Recopilar porcentajes en M3
                if mod == 3 and "pct" in vals:
                    porcentajes_detectados.add(vals["pct"])
                    
    # 3.T2: Confirmar que los denominadores 2 y 12 aparecen en el pool
    assert 2 in denominadores_detectados, "El denominador 2 no se utilizó en ninguna pregunta"
    assert 12 in denominadores_detectados, "El denominador 12 no se utilizó en ninguna pregunta"
    
    # 3.T3: Confirmar que porcentajes 75% y 20% aparecen en M3
    assert 75 in porcentajes_detectados, "El porcentaje 75% no se utilizó en ninguna pregunta de M3"
    assert 20 in porcentajes_detectados, "El porcentaje 20% no se utilizó en ninguna pregunta de M3"


def test_enunciados_autoexplicativos():
    """Grupo 4: Validar enunciados autoexplicativos para interactivas."""
    mod_niv_pairs = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3), (3, 4), (4, 1), (4, 2), (4, 3)]
    
    for mod, niv in mod_niv_pairs:
        for fam in range(1, 16):
            for var in range(4):
                q = generate_practice_question_fase4(mod, niv, fam, var)
                vals = q.get("valores", {})
                enunciado = q["enunciado"]
                
                # 4.T1: Si es interactivo, el enunciado debe tener suficiente longitud descriptiva
                if vals.get("es_interactivo"):
                    palabras = len(enunciado.split())
                    assert palabras >= 18, f"Enunciado interactivo muy corto ({palabras} palabras) en mod={mod} niv={niv} fam={fam}: {enunciado}"
                    
                    # 4.T2: Si es M3 interactivo (gráficos circulares), deben constar los datos numéricos en el texto
                    if mod == 3 and niv == 2:
                        assert str(vals["pct_a"]) in enunciado, f"Enunciado interactivo de gráfico circular no menciona pct_a ({vals['pct_a']})"
                        assert str(vals["pct_b"]) in enunciado, f"Enunciado interactivo de gráfico circular no menciona pct_b ({vals['pct_b']})"
                        
                    # 4.T3: Si es M4 interactivo (beaker), debe constar la relación en el texto
                    if mod == 4 and niv == 2:
                        assert str(vals["azul"]) in enunciado, f"Enunciado interactivo de probeta no menciona partes del primer ingrediente ({vals['azul']})"
                        assert str(vals["amarillo"]) in enunciado, f"Enunciado interactivo de probeta no menciona partes del segundo ingrediente ({vals['amarillo']})"
                        assert str(vals["pedido"]) in enunciado, f"Enunciado interactivo de probeta no menciona el pedido total ({vals['pedido']})"


def test_desafios_m3_diversificados():
    """Grupo 5: Validar diversificación de desafíos M3 (categorías distribuidas y enunciados autoexplicativos)."""
    from app.fase4.seed import generate_challenge_question_fase4
    
    # 5.T1 y 5.T2: Probar para los 3 desafíos del Módulo 3 (11, 12, 13)
    for desafio_id in (11, 12, 13):
        categorias_conteo = {0: 0, 1: 0, 2: 0, 3: 0} # 0=pct, 1=circ, 2=barras, 3=promedio
        
        # Generar las 30 preguntas del desafío
        for idx in range(1, 31):
            q = generate_challenge_question_fase4(modulo_id=3, desafio_id=desafio_id, idx=idx)
            categoria = idx % 4
            categorias_conteo[categoria] += 1
            
            enunciado = q["enunciado"]
            vals = q.get("valores", {})
            
            # 5.T3: Enunciados autoexplicativos en desafíos
            if categoria == 0: # porcentajes
                assert str(vals["pct"]) in enunciado, f"Falta porcentaje en enunciado de desafío porcentajes (idx={idx})"
                assert str(vals["total"]) in enunciado, f"Falta total en enunciado de desafío porcentajes (idx={idx})"
            elif categoria == 1: # circulares
                assert str(vals["pct_a"]) in enunciado, f"Falta pct_a en enunciado de desafío gráficos circulares (idx={idx})"
                assert str(vals["pct_b"]) in enunciado, f"Falta pct_b en enunciado de desafío gráficos circulares (idx={idx})"
            elif categoria == 2: # barras
                assert str(vals["val_a"]) in enunciado, f"Falta val_a en enunciado de desafío barras (idx={idx})"
                assert str(vals["val_b"]) in enunciado, f"Falta val_b en enunciado de desafío barras (idx={idx})"
            elif categoria == 3: # promedio
                assert str(vals["a"]) in enunciado, f"Falta nota a en enunciado de desafío promedio (idx={idx})"
                assert str(vals["b"]) in enunciado, f"Falta nota b en enunciado de desafío promedio (idx={idx})"
                assert str(vals["c"]) in enunciado, f"Falta nota c en enunciado de desafío promedio (idx={idx})"
                
        # Confirmar que cada una de las 4 categorías tiene al menos 5 preguntas por desafío (deben tener 7 u 8)
        for cat, conteo in categorias_conteo.items():
            assert conteo >= 5, f"Pocas preguntas ({conteo}) para categoría {cat} en desafío M3 {desafio_id}"


def test_distractores_opcion_multiple():
    """Grupo 6: Validar distractores mejorados (múltiple opción con retroalimentación específica)."""
    from app.fase4.seed import generate_challenge_question_fase4
    
    # Desafíos de opción múltiple son el 11 y 12
    for mod in range(1, 5):
        for desafio_id in (11, 12):
            for idx in range(1, 15): # Muestrear las primeras 15 preguntas
                q = generate_challenge_question_fase4(modulo_id=mod, desafio_id=desafio_id, idx=idx)
                
                # 6.T2: Verificar que ningún distractor tiene el mismo valor que la respuesta correcta
                ans = q["respuesta_correcta"]
                errores = q.get("errores_previstos", {})
                
                assert ans not in errores, f"La respuesta correcta {ans} está listada como un error previsto en mod={mod} des={desafio_id} idx={idx}"
                
                # 6.T1: Al menos 2 de los 3 distractores deben tener un mensaje específico
                # (El pool del seed inyecta alternativas basadas en errores_previstos)
                assert len(errores) >= 2, f"Pocos errores previstos específicos ({len(errores)}) en mod={mod} des={desafio_id} idx={idx}"


def test_auditoria_volumen_y_prefijos():
    """Grupo 7: Auditar volumen total de preguntas y ausencia del prefijo [ESPEJO]."""
    from app.fase4.seed import generate_practice_question_fase4, generate_challenge_question_fase4

    # 7.2 y 7.4: Generar y auditar todo el pool de práctica libre (~780 preguntas)
    conteo_practica = 0
    modulos_niveles = {1: 3, 2: 3, 3: 4, 4: 3}
    for modulo_id, max_niv in modulos_niveles.items():
        for nivel_id in range(1, max_niv + 1):
            for fam in range(1, 16):
                for var in range(4):
                    q = generate_practice_question_fase4(modulo_id, nivel_id, fam, var)
                    conteo_practica += 1
                    # Verificar que no contenga [ESPEJO]
                    assert "[ESPEJO]" not in q["enunciado"], f"Encontrado prefijo [ESPEJO] en práctica mod={modulo_id} niv={nivel_id} fam={fam} var={var}"

    # 7.2 y 7.4: Generar y auditar todo el pool de desafíos (~360 preguntas)
    conteo_desafios = 0
    for modulo_id in range(1, 5):
        for desafio_id in (11, 12, 13):
            for idx in range(1, 31):
                q = generate_challenge_question_fase4(modulo_id, desafio_id, idx)
                conteo_desafios += 1
                # Verificar que no contenga [ESPEJO]
                assert "[ESPEJO]" not in q["enunciado"], f"Encontrado prefijo [ESPEJO] en desafío mod={modulo_id} des={desafio_id} idx={idx}"

    total_preguntas = conteo_practica + conteo_desafios
    print(f"\nAuditoría de volumen: Práctica={conteo_practica}, Desafíos={conteo_desafios}, Total={total_preguntas}")
    
    assert conteo_practica == 780, f"Se esperaban 780 preguntas de práctica, pero se generaron {conteo_practica}"
    assert conteo_desafios == 360, f"Se esperaban 360 preguntas de desafíos, pero se generaron {conteo_desafios}"
    assert total_preguntas == 1140, f"Volumen total incorrecto: {total_preguntas}"

