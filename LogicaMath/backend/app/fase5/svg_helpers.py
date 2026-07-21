"""
Helper para generar SVGs premium de teoría con diseño oscuro, cuadrícula y etiquetas externas.
Fondo: #111827, cuadrícula sutil #374151, figura con borde blanco sin relleno,
etiquetas FUERA con fuente grande, leyenda "1 cm" en esquina inferior derecha.
"""

# ─── Constantes de diseño ────────────────────────────────────────────────────
# Canvas interno (unidades SVG)
_W, _H = 200, 200           # tamaño total del canvas SVG interno
_M     = 40                  # margen para etiquetas (espacio fuera de la figura)
_INNER = _W - 2 * _M        # zona disponible para la figura: 120 × 120

_GRID   = "#374151"          # color de cuadrícula
_SHP    = "#FFFFFF"          # color del borde de la figura
_LBL    = "#FFFFFF"          # color de etiquetas principales
_SCALE  = "#94A3B8"          # color de la leyenda "1 cm"
_FS     = 16                 # font-size para etiquetas de medidas
_FS_SC  = 11                 # font-size para leyenda de escala

# ─── Helper de cuadrícula ─────────────────────────────────────────────────────
_GRID_PATH = (
    "M20,0 V200 M40,0 V200 M60,0 V200 M80,0 V200 M100,0 V200 "
    "M120,0 V200 M140,0 V200 M160,0 V200 M180,0 V200 "
    "M0,20 H200 M0,40 H200 M0,60 H200 M0,80 H200 M0,100 H200 "
    "M0,120 H200 M0,140 H200 M0,160 H200 M0,180 H200"
)


def _svg_container(content: str, border_color="#A855F7", w=320, h=320) -> str:
    """Envuelve el contenido SVG en el contenedor estándar de teoría."""
    return (
        f"<svg width='{w}' height='{h}' viewBox='0 0 {_W} {_H}' "
        f"style='margin:10px auto; display:block; background:#111827; "
        f"border:2px solid {border_color}; border-radius:14px;'>"
        f"  <path d='{_GRID_PATH}' stroke='{_GRID}' stroke-width='0.4'/>"
        f"{content}"
        # Leyenda "1 cm" en esquina inferior derecha
        f"  <line x1='155' y1='188' x2='175' y2='188' stroke='{_SCALE}' stroke-width='1.5'/>"
        f"  <text x='165' y='198' fill='{_SCALE}' font-size='{_FS_SC}' "
        f"    font-weight='normal' text-anchor='middle'>1 cm</text>"
        f"</svg>"
    )


def _lbl(x, y, text, anchor="middle", dx=0, dy=0, fs=None) -> str:
    """Genera una etiqueta de medida (blanca, bold)."""
    if fs is None:
        fs = _FS
    sx = x + dx
    sy = y + dy
    return (
        f"<text x='{sx}' y='{sy}' fill='{_LBL}' font-size='{fs}' "
        f"font-weight='bold' text-anchor='{anchor}'>{text}</text>"
    )


def _lbl_rot(cx, cy, text, angle=90, fs=None) -> str:
    """Etiqueta rotada (para lados verticales)."""
    if fs is None:
        fs = _FS
    return (
        f"<text x='{cx}' y='{cy}' fill='{_LBL}' font-size='{fs}' "
        f"font-weight='bold' text-anchor='middle' "
        f"transform='rotate({angle} {cx} {cy})'>{text}</text>"
    )


# ─── Figuras geométricas ─────────────────────────────────────────────────────

def svg_rect(w_u, h_u, unit="cm", border="#A855F7") -> str:
    """
    Rectángulo con etiquetas fuera: ancho arriba, alto a la derecha (rotado).
    w_u, h_u: dimensiones lógicas en unidades 'unit'.
    La figura ocupa la zona interior (dentro del margen _M).
    Escala: se ajusta para que la figura llene la zona interna proporcionalmente.
    """
    # Escala para que la figura quepa en _INNER × _INNER
    scale = min(_INNER / w_u, _INNER / h_u)
    # Tamaño en px del canvas
    pw = w_u * scale
    ph = h_u * scale
    # Centrar en el canvas (teniendo en cuenta el margen)
    x0 = (_W - pw) / 2
    y0 = (_H - ph) / 2
    x1, y1 = x0 + pw, y0 + ph

    cx = (x0 + x1) / 2   # centro horizontal
    cy = (y0 + y1) / 2   # centro vertical

    shape = (
        f"<rect x='{x0:.1f}' y='{y0:.1f}' width='{pw:.1f}' height='{ph:.1f}' "
        f"fill='transparent' stroke='{_SHP}' stroke-width='3.5'/>"
    )
    # Etiqueta ancho: centrada ARRIBA de la figura
    top_lbl    = _lbl(cx, y0 - 8, f"{w_u} {unit}")
    # Etiqueta alto: a la DERECHA, rotada 90° (texto legible de abajo a arriba)
    right_lbl  = _lbl_rot(x1 + 22, cy, f"{h_u} {unit}", angle=90)

    return _svg_container(shape + top_lbl + right_lbl, border_color=border)


def svg_square(side_u, unit="cm", border="#A855F7") -> str:
    """Cuadrado con etiqueta arriba y a la derecha (rotada)."""
    return svg_rect(side_u, side_u, unit=unit, border=border)


def svg_triangle_equilateral(side_u, unit="cm", border="#A855F7") -> str:
    """Triángulo equilátero. Etiquetas en cada lado, FUERA de la figura."""
    import math
    scale = min(_INNER / side_u, _INNER / (side_u * 0.866))
    ps = side_u * scale                      # lado en pixels
    ph = ps * math.sqrt(3) / 2              # altura en pixels

    # Centrar
    cx = _W / 2
    cy = _H / 2
    x1 = cx - ps / 2;  y1 = cy + ph / 3     # esquina inf-izquierda
    x2 = cx + ps / 2;  y2 = cy + ph / 3     # esquina inf-derecha
    x3 = cx;           y3 = cy - 2 * ph / 3  # cima

    shape = (
        f"<polygon points='{x1:.1f},{y1:.1f} {x2:.1f},{y2:.1f} {x3:.1f},{y3:.1f}' "
        f"fill='transparent' stroke='{_SHP}' stroke-width='3.5'/>"
    )
    # Base (abajo)
    base_lbl  = _lbl(cx, y1 + 18, f"{side_u} {unit}")
    # Lado izquierdo (fuera, a la izquierda)
    lx = (x1 + x3) / 2 - 20;  ly = (y1 + y3) / 2
    left_lbl  = _lbl(lx, ly, f"{side_u} {unit}", anchor="end")
    # Lado derecho (fuera, a la derecha)
    rx = (x2 + x3) / 2 + 20;  ry = (y2 + y3) / 2
    right_lbl = _lbl(rx, ry, f"{side_u} {unit}", anchor="start")

    return _svg_container(shape + base_lbl + left_lbl + right_lbl, border_color=border)


def svg_rect_all_labels(w_u, h_u, unit="cm", border="#F59E0B") -> str:
    """
    Rectángulo con las 4 etiquetas FUERA (arriba, abajo, izquierda, derecha).
    Útil para mostrar todos los lados explícitamente.
    """
    scale = min(_INNER / w_u, _INNER / h_u)
    pw = w_u * scale
    ph = h_u * scale
    x0 = (_W - pw) / 2
    y0 = (_H - ph) / 2
    x1, y1 = x0 + pw, y0 + ph
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2

    shape = (
        f"<rect x='{x0:.1f}' y='{y0:.1f}' width='{pw:.1f}' height='{ph:.1f}' "
        f"fill='transparent' stroke='{_SHP}' stroke-width='3.5'/>"
    )
    top_lbl    = _lbl(cx, y0 - 8, f"{w_u} {unit}")
    bottom_lbl = _lbl(cx, y1 + 20, f"{w_u} {unit}")
    left_lbl   = _lbl_rot(x0 - 20, cy, f"{h_u} {unit}", angle=-90)
    right_lbl  = _lbl_rot(x1 + 20, cy, f"{h_u} {unit}", angle=90)

    return _svg_container(shape + top_lbl + bottom_lbl + left_lbl + right_lbl, border_color=border)


def svg_l_shape(w1_u, h1_u, w2_u, h2_u, unit="cm", border="#F59E0B") -> str:
    """Forma en L con etiquetas fuera de cada lado."""
    total_w = w1_u + w2_u
    total_h = h1_u
    scale = min(_INNER / total_w, _INNER / total_h)

    pw1 = w1_u * scale;  ph1 = h1_u * scale
    pw2 = w2_u * scale;  ph2 = h2_u * scale

    x0 = (_W - (pw1 + pw2)) / 2
    y0 = (_H - ph1) / 2

    # Puntos de la L (empieza arriba-izquierda, sentido horario)
    pts = [
        (x0,           y0),
        (x0,           y0 + ph1),
        (x0 + pw1 + pw2, y0 + ph1),
        (x0 + pw1 + pw2, y0 + ph1 - ph2),
        (x0 + pw1,     y0 + ph1 - ph2),
        (x0 + pw1,     y0),
    ]
    pts_str = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)
    shape = f"<polygon points='{pts_str}' fill='transparent' stroke='{_SHP}' stroke-width='3.5'/>"

    # Etiquetas representativas (solo 3 para no saturar)
    total_cx = (x0 + x0 + pw1 + pw2) / 2
    top_lbl    = _lbl(total_cx, y0 - 8, f"{total_w} {unit}")                     # ancho total arriba
    left_lbl   = _lbl_rot(x0 - 20, y0 + ph1/2, f"{h1_u} {unit}", angle=-90)     # alto total izquierda
    inner_lbl  = _lbl_rot(x0 + pw1 + pw2 + 20, y0 + ph1 - ph2/2, f"{h2_u} {unit}", angle=90)  # alto escalón

    return _svg_container(shape + top_lbl + left_lbl + inner_lbl, border_color=border)


def svg_polygon_labeled(points_unit, labels, unit="cm", border="#A855F7") -> str:
    """
    Polígono arbitrario. 
    points_unit: lista de (x,y) en unidades lógicas.
    labels: lista de (x,y, texto) en UNIDADES LÓGICAS (se escalarán).
    """
    import math
    if not points_unit:
        return ""

    xs = [p[0] for p in points_unit]
    ys = [p[1] for p in points_unit]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    lw = max_x - min_x or 1
    lh = max_y - min_y or 1

    scale = min(_INNER / lw, _INNER / lh)
    ox = (_W - lw * scale) / 2 - min_x * scale
    oy = (_H - lh * scale) / 2 - min_y * scale

    def tp(lx, ly):
        return lx * scale + ox, ly * scale + oy

    pts_str = " ".join(f"{tp(px,py)[0]:.1f},{tp(px,py)[1]:.1f}" for px, py in points_unit)
    shape = f"<polygon points='{pts_str}' fill='transparent' stroke='{_SHP}' stroke-width='3.5'/>"

    lbl_content = ""
    for lx, ly, txt in labels:
        px, py = tp(lx, ly)
        lbl_content += _lbl(px, py, txt)

    return _svg_container(shape + lbl_content, border_color=border)


def svg_shaded_rect(w_u, h_u, unit="cm²", fill="#EC4899", border="#EC4899") -> str:
    """Rectángulo relleno para área, con dimensiones fuera y etiqueta de área dentro."""
    scale = min(_INNER / w_u, _INNER / h_u)
    pw = w_u * scale
    ph = h_u * scale
    x0 = (_W - pw) / 2
    y0 = (_H - ph) / 2
    x1, y1 = x0 + pw, y0 + ph
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2

    shape = (
        f"<rect x='{x0:.1f}' y='{y0:.1f}' width='{pw:.1f}' height='{ph:.1f}' "
        f"fill='{fill}' fill-opacity='0.35' stroke='{fill}' stroke-width='3'/>"
        f"<text x='{cx:.1f}' y='{cy+6:.1f}' fill='#FFF' font-size='{_FS}' "
        f"font-weight='bold' text-anchor='middle'>{w_u}×{h_u}={w_u*h_u}</text>"
    )
    top_lbl   = _lbl(cx, y0 - 8, f"{w_u}")
    right_lbl = _lbl_rot(x1 + 22, cy, f"{h_u}", angle=90)

    return _svg_container(shape + top_lbl + right_lbl, border_color=border)

def svg_grid_halves(enteros: int, mitades: int, unit="cm", border="#3B82F6") -> str:
    """Rejilla con cuadrados enteros (rect) + triángulos mitad, para M2.L2 (fusión de sectores)."""
    cols = min(enteros + mitades, 6)
    if cols == 0:
        return ""
    cs = _INNER / cols
    rows = (enteros + mitades + cols - 1) // cols
    cx = _M + (_INNER - cols * cs) / 2
    cy = _M + (_INNER - rows * cs) / 2

    shape = ""
    col_i = 0
    row_i = 0
    for _ in range(enteros):
        if col_i >= cols:
            col_i = 0
            row_i += 1
        x = cx + col_i * cs
        y = cy + row_i * cs
        shape += f"<rect x='{x:.1f}' y='{y:.1f}' width='{cs:.1f}' height='{cs:.1f}' fill='#BAE6FD' stroke='{_SHP}' stroke-width='1'/>"
        col_i += 1
    for _ in range(mitades):
        if col_i >= cols:
            col_i = 0
            row_i += 1
        x = cx + col_i * cs
        y = cy + row_i * cs
        shape += f"<polygon points='{x:.1f},{y:.1f} {x+cs:.1f},{y:.1f} {x+cs:.1f},{y+cs:.1f}' fill='#FCA5A5' stroke='{_SHP}' stroke-width='1'/>"
        col_i += 1

    return _svg_container(shape, border_color=border)

def svg_scale_bar(u_val: int, scale: int, unit="cm", border="#F59E0B") -> str:
    """Barra de escala gráfica tipo mapa, para M4.L1."""
    bar_w = _INNER * 0.8
    shape = (
        f"<rect x='{_M:.1f}' y='{_M:.1f}' width='{_INNER:.1f}' height='{_INNER:.1f}' fill='#475569' fill-opacity='0.4' rx='6'/>"
        f"<line x1='{_M+10:.1f}' y1='{_H/2:.1f}' x2='{_M+10+bar_w:.1f}' y2='{_H/2:.1f}' stroke='{_SHP}' stroke-width='3' stroke-linecap='round'/>"
        f"<line x1='{_M+10:.1f}' y1='{_H/2-10:.1f}' x2='{_M+10:.1f}' y2='{_H/2+10:.1f}' stroke='{_SHP}' stroke-width='2'/>"
        f"<line x1='{_M+10+bar_w:.1f}' y1='{_H/2-10:.1f}' x2='{_M+10+bar_w:.1f}' y2='{_H/2+10:.1f}' stroke='{_SHP}' stroke-width='2'/>"
    )
    lbl = _lbl(_M + 10 + bar_w/2, _H/2 - 12, f"{u_val} {unit}", fs=18)
    return _svg_container(shape + lbl, border_color=border)

def svg_rect_diagonal(w_u: int, h_u: int, diag_label: str = "?", unit="cm", border="#EC4899") -> str:
    """Rectángulo con diagonal resaltada (para enseñar/practicar Pitágoras), para M4.L2."""
    scale_fac = min(_INNER / w_u, _INNER / h_u)
    pw = w_u * scale_fac
    ph = h_u * scale_fac
    x0 = (_W - pw) / 2
    y0 = (_H - ph) / 2
    x1, y1 = x0 + pw, y0 + ph
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2
    
    shape = (
        f"<rect x='{x0:.1f}' y='{y0:.1f}' width='{pw:.1f}' height='{ph:.1f}' fill='#1E40AF' fill-opacity='0.5' stroke='{_SHP}' stroke-width='2'/>"
        f"<line x1='{x0:.1f}' y1='{y0:.1f}' x2='{x1:.1f}' y2='{y1:.1f}' stroke='#F59E0B' stroke-width='3' stroke-dasharray='5,3'/>"
    )
    
    bottom_lbl = _lbl(cx, y1 + 18, f"{w_u} {unit}")
    left_lbl   = _lbl_rot(x0 - 20, cy, f"{h_u} {unit}", angle=-90)
    
    import math
    angle = math.degrees(math.atan2(y1 - y0, x1 - x0))
    diag_lbl   = _lbl_rot(cx + 8, cy - 8, diag_label, angle=angle, fs=16)

    return _svg_container(shape + bottom_lbl + left_lbl + diag_lbl, border_color=border)

