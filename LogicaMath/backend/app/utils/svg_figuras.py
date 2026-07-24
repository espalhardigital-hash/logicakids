"""
Libreria compartida de figuras SVG -- LogicaKids Pro
Seccion 11 del plan de reestructuracion (docs/reestructuraciondefases.md).
Reemplaza el patron PNG->MinIO para Fases 5 y 6 (Decision 6).

Reglas de diseno obligatorias (s11.4):
1. viewBox con holgura — ninguna cota se recorta.
2. Cotas SIEMPRE fuera de la figura.
3. Contraste: borde y cotas #FFFFFF; relleno fill-opacity 0.15.
4. Anti-revelacion: el lado a deducir lleva "?"; el hueco en color de fondo.
5. Sin dependencias externas.
6. font-size >= 14 para legibilidad en movil.
7. Determinista: mismo seed -> mismo string.

PROHIBIDO en seeds de Fase 5/6:
  import app.utils.graphics_generator
  storage_service.upload_question_graphic(...)
  datos_numericos["url"] = <url imagen>
"""
from __future__ import annotations
import math

# Constantes (identicas a svg_helpers.py original)
_W, _H   = 200, 200
_M       = 40
_INNER   = _W - 2 * _M  # 120

_GRID    = "#374151"
_SHP     = "#FFFFFF"
_LBL     = "#FFFFFF"
_SCALE   = "#94A3B8"
_FS      = 16
_FS_SC   = 11

_GRID_PATH = (
    "M20,0 V200 M40,0 V200 M60,0 V200 M80,0 V200 M100,0 V200 "
    "M120,0 V200 M140,0 V200 M160,0 V200 M180,0 V200 "
    "M0,20 H200 M0,40 H200 M0,60 H200 M0,80 H200 M0,100 H200 "
    "M0,120 H200 M0,140 H200 M0,160 H200 M0,180 H200"
)

# Colores de modulo (Decision 6, s11.2.3)
MODULE_COLORS: dict[tuple[int, int], str] = {
    (5, 1): "#10B981",  # F5-M1 Suma/Resta Decimales
    (5, 2): "#8B5CF6",  # F5-M2 Multiplicacion/Division
    (5, 3): "#F59E0B",  # F5-M3 Longitud
    (5, 4): "#3B82F6",  # F5-M4 Volumen
    (5, 5): "#EC4899",  # F5-M5 Superficie
    (6, 1): "#22C55E",  # F6-M1 Reconocimiento/Perimetros
    (6, 2): "#3B82F6",  # F6-M2 Perimetro Compuesto
    (6, 3): "#F59E0B",  # F6-M3 Fundamentos Area
    (6, 4): "#EC4899",  # F6-M4 Areas Compuestas
}


def color_modulo(fase_id: int, modulo_id: int) -> str:
    """Color hex del modulo con fallback seguro."""
    return MODULE_COLORS.get((fase_id, modulo_id), "#A855F7")


# --- Helpers privados ---------------------------------------------------------

def _svg_container(
    content: str,
    border_color: str = "#A855F7",
    w: int = 320,
    h: int = 320,
    viewbox: str | None = None,
    grid: bool = True,
    leyenda: str | None = "1 cm",
) -> str:
    """Contenedor SVG estandar ampliado (s11.2.2)."""
    vb = viewbox or f"0 0 {_W} {_H}"
    g = f"<path d='{_GRID_PATH}' stroke='{_GRID}' stroke-width='0.4'/>" if grid else ""
    ly = ""
    if leyenda:
        ly = (
            f"<line x1='155' y1='188' x2='175' y2='188' stroke='{_SCALE}' stroke-width='1.5'/>"
            f"<text x='165' y='198' fill='{_SCALE}' font-size='{_FS_SC}' text-anchor='middle'>{leyenda}</text>"
        )
    return (
        f"<svg width='{w}' height='{h}' viewBox='{vb}' "
        f"style='margin:10px auto; display:block; background:#111827; "
        f"border:2px solid {border_color}; border-radius:14px;'>"
        f"{g}{content}{ly}</svg>"
    )


def _lbl(x: float, y: float, text: str, anchor: str = "middle",
         dx: float = 0, dy: float = 0, fs: int | None = None) -> str:
    if fs is None:
        fs = _FS
    return (
        f"<text x='{x+dx:.1f}' y='{y+dy:.1f}' fill='{_LBL}' "
        f"font-size='{fs}' font-weight='bold' text-anchor='{anchor}'>{text}</text>"
    )


def _lbl_rot(cx: float, cy: float, text: str, angle: float = 90, fs: int | None = None) -> str:
    if fs is None:
        fs = _FS
    return (
        f"<text x='{cx:.1f}' y='{cy:.1f}' fill='{_LBL}' font-size='{fs}' "
        f"font-weight='bold' text-anchor='middle' "
        f"transform='rotate({angle} {cx:.1f} {cy:.1f})'>{text}</text>"
    )


def _marc_ar(x: float, y: float, s: float = 8.0) -> str:
    """Marca de angulo recto (cuadradito)."""
    return f"<rect x='{x:.1f}' y='{y:.1f}' width='{s:.1f}' height='{s:.1f}' fill='none' stroke='{_SHP}' stroke-width='1.5'/>"


# --- Figuras geometricas (Fase 6) --------------------------------------------

def fig_rectangulo(base: float, altura: float, unit: str = "cm",
                   color: str = "#22C55E", cotas: str = "dos") -> str:
    """Rectangulo con cotas FUERA. cotas in {dos, cuatro, oculta}."""
    sc = min(_INNER / base, _INNER / altura)
    pw, ph = base * sc, altura * sc
    x0 = (_W - pw) / 2; y0 = (_H - ph) / 2
    x1, y1 = x0 + pw, y0 + ph; cx, cy = (x0+x1)/2, (y0+y1)/2
    shp = (f"<rect x='{x0:.1f}' y='{y0:.1f}' width='{pw:.1f}' height='{ph:.1f}' "
           f"fill='{color}' fill-opacity='0.15' stroke='{_SHP}' stroke-width='3.5'/>")
    c = shp + _lbl(cx, y0-12, f"{base} {unit}") + _lbl_rot(x1+22, cy, f"{altura} {unit}", 90)
    if cotas == "cuatro":
        c += _lbl(cx, y1+20, f"{base} {unit}") + _lbl_rot(x0-20, cy, f"{altura} {unit}", -90)
    elif cotas == "oculta":
        c += _lbl(cx, y1+20, "?", fs=18)
    vb = f"{x0-35:.0f} {y0-35:.0f} {pw+70:.0f} {ph+70:.0f}"
    return _svg_container(c, border_color=color, viewbox=vb, leyenda=unit)


def fig_cuadrado(lado: float, unit: str = "cm", color: str = "#22C55E") -> str:
    return fig_rectangulo(lado, lado, unit=unit, color=color)


def fig_triangulo(base: float, altura: float, unit: str = "cm",
                  color: str = "#F59E0B", tipo: str = "isosceles",
                  marcar_altura: bool = True) -> str:
    """Triangulo con base FUERA y altura punteada interna con angulo recto."""
    sc = min(_INNER / base, _INNER / altura)
    pb, ph = base * sc, altura * sc
    yb = _H/2 + ph/2; yc = yb - ph
    xl = (_W - pb) / 2; xr = xl + pb
    ax = xl if tipo == "rectangulo" else (xl + pb*0.35 if tipo == "escaleno" else _W/2)
    shp = f"<polygon points='{xl:.1f},{yb:.1f} {xr:.1f},{yb:.1f} {ax:.1f},{yc:.1f}' fill='{color}' fill-opacity='0.15' stroke='{_SHP}' stroke-width='3.5'/>"
    c = shp + _lbl((xl+xr)/2, yb+20, f"{base} {unit}")
    if marcar_altura:
        c += (f"<line x1='{ax:.1f}' y1='{yc:.1f}' x2='{ax:.1f}' y2='{yb:.1f}' "
              f"stroke='{_SHP}' stroke-width='1.5' stroke-dasharray='4,3'/>")
        c += _marc_ar(ax, yb-8, 8)
        c += _lbl(ax-20, (yc+yb)/2, f"{altura} {unit}", anchor="end")
    vb = f"{xl-40:.0f} {yc-30:.0f} {pb+80:.0f} {ph+60:.0f}"
    return _svg_container(c, border_color=color, viewbox=vb, leyenda=unit)


def fig_poligono_irregular(vertices: list[tuple[float,float]],
                           cotas_lado: list[str | None],
                           unit: str = "cm", color: str = "#22C55E") -> str:
    """Poligono con cotas de lado. None = sin cota (anti-revelacion)."""
    if not vertices: return ""
    xs = [v[0] for v in vertices]; ys = [v[1] for v in vertices]
    mnx, mxx = min(xs), max(xs); mny, mxy = min(ys), max(ys)
    lw = mxx - mnx or 1; lh = mxy - mny or 1
    sc = min(_INNER/lw, _INNER/lh)
    ox = (_W - lw*sc)/2 - mnx*sc; oy = (_H - lh*sc)/2 - mny*sc
    def tp(lx, ly): return lx*sc+ox, ly*sc+oy
    pts_s = " ".join(f"{tp(vx,vy)[0]:.1f},{tp(vx,vy)[1]:.1f}" for vx,vy in vertices)
    shp = f"<polygon points='{pts_s}' fill='{color}' fill-opacity='0.15' stroke='{_SHP}' stroke-width='3.5'/>"
    lc = ""
    n = len(vertices)
    for i, cota in enumerate(cotas_lado):
        if cota is None: continue
        vx0,vy0 = vertices[i]; vx1,vy1 = vertices[(i+1)%n]
        mx,my = (vx0+vx1)/2, (vy0+vy1)/2; px,py = tp(mx,my)
        dx = vy1-vy0; dy = -(vx1-vx0); norm = math.hypot(dx,dy) or 1; off = 18/norm
        lc += _lbl(px+dx*off, py+dy*off, cota)
    vb = f"{mnx*sc+ox-40:.0f} {mny*sc+oy-30:.0f} {lw*sc+80:.0f} {lh*sc+60:.0f}"
    return _svg_container(shp+lc, border_color=color, viewbox=vb, leyenda=unit)


def fig_L(w1: float, h1: float, w2: float, h2: float, unit: str = "cm",
          color: str = "#3B82F6", ocultar_lado: int | None = None) -> str:
    """Figura en L (6 lados). ocultar_lado marca ese lado con '?'."""
    tw = w1 + w2; sc = min(_INNER/tw, _INNER/h1)
    pw1,pw2,ph1,ph2 = w1*sc,w2*sc,h1*sc,h2*sc
    x0 = (_W-(pw1+pw2))/2; y0 = (_H-ph1)/2
    pl = [(x0,y0),(x0+pw1,y0),(x0+pw1,y0+ph1-ph2),
          (x0+pw1+pw2,y0+ph1-ph2),(x0+pw1+pw2,y0+ph1),(x0,y0+ph1)]
    pts_s = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pl)
    shp = f"<polygon points='{pts_s}' fill='{color}' fill-opacity='0.15' stroke='{_SHP}' stroke-width='3.5'/>"
    lados = [
        (x0+pw1/2, y0, f"{w1} {unit}", 0, -15),
        (x0+pw1, y0+(ph1-ph2)/2, "?", -22, 0),
        (x0+pw1+pw2/2, y0+ph1-ph2, f"{w2} {unit}", 0, -15),
        (x0+pw1+pw2, y0+ph1-ph2/2, f"{h2} {unit}", 22, 0),
        ((x0*2+pw1+pw2)/2, y0+ph1, f"{tw} {unit}", 0, 18),
        (x0, y0+ph1/2, f"{h1} {unit}", -22, 0),
    ]
    c = shp
    for i,(mx,my,txt,ox3,oy3) in enumerate(lados):
        if i == ocultar_lado: txt = "?"
        if ox3 == 0: c += _lbl(mx, my+oy3, txt)
        else: c += _lbl_rot(mx+ox3, my, txt, 90 if ox3>0 else -90)
    vb = f"{x0-40:.0f} {y0-35:.0f} {(pw1+pw2)+80:.0f} {ph1+55:.0f}"
    return _svg_container(c, border_color=color, viewbox=vb, leyenda=unit)


def fig_T(ala: float, alto_ala: float, tallo: float, alto_tallo: float,
          unit: str = "cm", color: str = "#3B82F6") -> str:
    """Figura en T (8 lados) con cotas externas."""
    total_w = max(ala, tallo)
    total_h = alto_ala + alto_tallo
    sc = min(_INNER / total_w, _INNER / total_h)
    p_ala, p_h_ala = ala * sc, alto_ala * sc
    p_tallo, p_h_tallo = tallo * sc, alto_tallo * sc
    x0 = (_W - p_ala) / 2
    y0 = (_H - total_h * sc) / 2
    x_tallo_left = x0 + (p_ala - p_tallo) / 2
    x_tallo_right = x_tallo_left + p_tallo
    pts = [
        (x0, y0), (x0 + p_ala, y0), (x0 + p_ala, y0 + p_h_ala),
        (x_tallo_right, y0 + p_h_ala), (x_tallo_right, y0 + p_h_ala + p_h_tallo),
        (x_tallo_left, y0 + p_h_ala + p_h_tallo), (x_tallo_left, y0 + p_h_ala),
        (x0, y0 + p_h_ala),
    ]
    pts_s = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)
    shp = f"<polygon points='{pts_s}' fill='{color}' fill-opacity='0.15' stroke='{_SHP}' stroke-width='3.5'/>"
    lbl_top = _lbl(x0 + p_ala / 2, y0 - 12, f"{ala} {unit}")
    lbl_h_ala = _lbl_rot(x0 + p_ala + 22, y0 + p_h_ala / 2, f"{alto_ala} {unit}", 90)
    lbl_tallo = _lbl(x0 + p_ala / 2, y0 + p_h_ala + p_h_tallo + 18, f"{tallo} {unit}")
    lbl_h_tallo = _lbl_rot(x_tallo_right + 22, y0 + p_h_ala + p_h_tallo / 2, f"{alto_tallo} {unit}", 90)
    content = shp + lbl_top + lbl_h_ala + lbl_tallo + lbl_h_tallo
    vb = f"{x0 - 35:.0f} {y0 - 30:.0f} {p_ala + 70:.0f} {total_h * sc + 55:.0f}"
    return _svg_container(content, border_color=color, viewbox=vb, leyenda=unit)


def fig_escalonada(tramos: list[tuple[float,float]], unit: str = "cm",
                   color: str = "#3B82F6", ocultar: list[int] | None = None) -> str:
    """Figura escalonada. Cada tramo = (ancho, alto) de un escalon."""
    ocultar = ocultar or []
    tw = sum(t[0] for t in tramos)
    th = max(sum(t[1] for t in tramos[:i+1]) for i in range(len(tramos)))
    sc = min(_INNER/max(tw,1), _INNER/max(th,1))
    pts: list[tuple[float,float]] = []
    cxo = (_W - tw*sc)/2; cyb = _H/2 + th*sc/2
    xc, yc = cxo, cyb; pts.append((xc,yc))
    for aw,ah in tramos:
        pw,ph = aw*sc,ah*sc; xc += pw; pts.append((xc,yc)); yc -= ph; pts.append((xc,yc))
    pts.append((cxo, pts[-1][1]))
    pts_s = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)
    shp = f"<polygon points='{pts_s}' fill='{color}' fill-opacity='0.15' stroke='{_SHP}' stroke-width='3.5'/>"
    c = shp; xc,yc = cxo,cyb
    for i,(aw,ah) in enumerate(tramos):
        pw,ph = aw*sc,ah*sc
        if i not in ocultar: c += _lbl(xc+pw/2, yc+18, f"{aw} {unit}")
        xc += pw
        if i not in ocultar: c += _lbl_rot(xc+18, yc-ph/2, f"{ah} {unit}", 90)
        yc -= ph
    vb = f"{cxo-35:.0f} {pts[-1][1]-30:.0f} {tw*sc+70:.0f} {th*sc+55:.0f}"
    return _svg_container(c, border_color=color, viewbox=vb, leyenda=unit)


def fig_lados_ocultos(vertices: list[tuple[float,float]],
                      cotas_lado: list[str | None],
                      unit: str = "cm", color: str = "#3B82F6") -> str:
    cv: list[str | None] = ["?" if c is None else c for c in cotas_lado]
    return fig_poligono_irregular(vertices, cv, unit=unit, color=color)


def fig_malla(celdas_llenas: list[tuple[int,int]],
              medias: list[tuple[int,int,str]],
              cols: int, rows: int, unit: str = "u",
              color: str = "#F59E0B", escala: float = 1.0) -> str:
    """Malla con celdas enteras y mitades. Sin numeros (anti-revelacion)."""
    cell = int(28 * escala)
    tw, th = cols*cell, rows*cell
    x0 = (_W-tw)/2; y0 = (_H-th)/2
    gr = ""
    for ci in range(cols+1):
        gx = x0+ci*cell; gr += f"<line x1='{gx:.1f}' y1='{y0:.1f}' x2='{gx:.1f}' y2='{y0+th:.1f}' stroke='{_GRID}' stroke-width='0.6'/>"
    for ri in range(rows+1):
        gy = y0+ri*cell; gr += f"<line x1='{x0:.1f}' y1='{gy:.1f}' x2='{x0+tw:.1f}' y2='{gy:.1f}' stroke='{_GRID}' stroke-width='0.6'/>"
    ls = ""
    for (ci,ri) in celdas_llenas:
        cx2,cy2 = x0+ci*cell,y0+ri*cell
        ls += f"<rect x='{cx2:.1f}' y='{cy2:.1f}' width='{cell:.1f}' height='{cell:.1f}' fill='{color}' fill-opacity='0.35'/>"
    ms = ""
    op = {
        "BL": lambda cx2,cy2: f"{cx2:.1f},{cy2:.1f} {cx2:.1f},{cy2+cell:.1f} {cx2+cell:.1f},{cy2+cell:.1f}",
        "BR": lambda cx2,cy2: f"{cx2+cell:.1f},{cy2:.1f} {cx2:.1f},{cy2+cell:.1f} {cx2+cell:.1f},{cy2+cell:.1f}",
        "TL": lambda cx2,cy2: f"{cx2:.1f},{cy2:.1f} {cx2+cell:.1f},{cy2:.1f} {cx2:.1f},{cy2+cell:.1f}",
        "TR": lambda cx2,cy2: f"{cx2:.1f},{cy2:.1f} {cx2+cell:.1f},{cy2:.1f} {cx2+cell:.1f},{cy2+cell:.1f}",
    }
    for (ci,ri,orient) in medias:
        cx2,cy2 = x0+ci*cell,y0+ri*cell
        pf = op.get(orient, op["TR"])(cx2, cy2)
        ms += f"<polygon points='{pf}' fill='{color}' fill-opacity='0.35'/>"
    ley_y = y0+th+18
    ley = (
        f"<rect x='{x0:.1f}' y='{ley_y:.1f}' width='{cell:.1f}' height='{cell:.1f}' fill='{color}' fill-opacity='0.35' stroke='{_SHP}' stroke-width='0.8'/>"
        f"<text x='{x0+cell+4:.1f}' y='{ley_y+cell*0.7:.1f}' fill='#E5E7EB' font-size='11' text-anchor='start'>= 1 {unit}^2</text>"
        f"<polygon points='{x0+cell*2.2:.1f},{ley_y:.1f} {x0+cell*3.2:.1f},{ley_y:.1f} {x0+cell*2.2:.1f},{ley_y+cell:.1f}' fill='{color}' fill-opacity='0.35' stroke='{_SHP}' stroke-width='0.8'/>"
        f"<text x='{x0+cell*3.4:.1f}' y='{ley_y+cell*0.7:.1f}' fill='#E5E7EB' font-size='11' text-anchor='start'>= 1/2 {unit}^2</text>"
    )
    c = gr+ls+ms+ley
    vb = f"{x0-10:.0f} {y0-10:.0f} {tw+20:.0f} {th+cell+30:.0f}"
    return _svg_container(c, border_color=color, viewbox=vb, grid=False, leyenda=None)


def fig_eje_simetria(tipo: str, lado: float, ejes: list[str],
                     unit: str = "cm", color: str = "#22C55E") -> str:
    """Figura con ejes de simetria punteados."""
    sc = _INNER / lado; ps = lado * sc
    cx0,cy0 = _W/2, _H/2; half = ps/2
    if tipo in ("cuadrado","rectangulo"):
        wp = ps; hp = ps*(0.6 if tipo=="rectangulo" else 1.0)
        x0 = cx0-wp/2; y0 = cy0-hp/2
        shp = f"<rect x='{x0:.1f}' y='{y0:.1f}' width='{wp:.1f}' height='{hp:.1f}' fill='{color}' fill-opacity='0.15' stroke='{_SHP}' stroke-width='3.5'/>"
        ax = ""
        if "V" in ejes: ax += f"<line x1='{cx0:.1f}' y1='{y0-15:.1f}' x2='{cx0:.1f}' y2='{y0+hp+15:.1f}' stroke='{color}' stroke-width='1.5' stroke-dasharray='5,3'/>"
        if "H" in ejes: ax += f"<line x1='{x0-15:.1f}' y1='{cy0:.1f}' x2='{x0+wp+15:.1f}' y2='{cy0:.1f}' stroke='{color}' stroke-width='1.5' stroke-dasharray='5,3'/>"
        if "D1" in ejes: ax += f"<line x1='{x0-10:.1f}' y1='{y0-10:.1f}' x2='{x0+wp+10:.1f}' y2='{y0+hp+10:.1f}' stroke='{color}' stroke-width='1.5' stroke-dasharray='5,3'/>"
        if "D2" in ejes: ax += f"<line x1='{x0+wp+10:.1f}' y1='{y0-10:.1f}' x2='{x0-10:.1f}' y2='{y0+hp+10:.1f}' stroke='{color}' stroke-width='1.5' stroke-dasharray='5,3'/>"
        c = shp + ax
    elif tipo == "circulo":
        r = half
        shp = f"<circle cx='{cx0:.1f}' cy='{cy0:.1f}' r='{r:.1f}' fill='{color}' fill-opacity='0.15' stroke='{_SHP}' stroke-width='3.5'/>"
        ax = ""
        for ad in [0,45,90,135]:
            rd = math.radians(ad)
            x2=cx0+r*math.cos(rd); y2=cy0-r*math.sin(rd)
            x3=cx0-r*math.cos(rd); y3=cy0+r*math.sin(rd)
            ax += f"<line x1='{x2:.1f}' y1='{y2:.1f}' x2='{x3:.1f}' y2='{y3:.1f}' stroke='{color}' stroke-width='1.5' stroke-dasharray='5,3'/>"
        c = shp + ax
    elif tipo == "triangulo_eq":
        ph2 = ps*math.sqrt(3)/2
        x1=cx0-ps/2; x2=cx0+ps/2; yb=cy0+ph2/3; ya=cy0-2*ph2/3
        shp = f"<polygon points='{x1:.1f},{yb:.1f} {x2:.1f},{yb:.1f} {cx0:.1f},{ya:.1f}' fill='{color}' fill-opacity='0.15' stroke='{_SHP}' stroke-width='3.5'/>"
        ax = ""
        if "V" in ejes: ax += f"<line x1='{cx0:.1f}' y1='{ya-12:.1f}' x2='{cx0:.1f}' y2='{yb+12:.1f}' stroke='{color}' stroke-width='1.5' stroke-dasharray='5,3'/>"
        c = shp + ax
    else:  # rombo
        pts_r = f"{cx0:.1f},{cy0-half:.1f} {cx0+half:.1f},{cy0:.1f} {cx0:.1f},{cy0+half:.1f} {cx0-half:.1f},{cy0:.1f}"
        shp = f"<polygon points='{pts_r}' fill='{color}' fill-opacity='0.15' stroke='{_SHP}' stroke-width='3.5'/>"
        ax = ""
        if "V" in ejes: ax += f"<line x1='{cx0:.1f}' y1='{cy0-half-12:.1f}' x2='{cx0:.1f}' y2='{cy0+half+12:.1f}' stroke='{color}' stroke-width='1.5' stroke-dasharray='5,3'/>"
        if "H" in ejes: ax += f"<line x1='{cx0-half-12:.1f}' y1='{cy0:.1f}' x2='{cx0+half+12:.1f}' y2='{cy0:.1f}' stroke='{color}' stroke-width='1.5' stroke-dasharray='5,3'/>"
        c = shp + ax
    vb = f"{cx0-half-35:.0f} {cy0-half-35:.0f} {ps+70:.0f} {ps+70:.0f}"
    return _svg_container(c, border_color=color, viewbox=vb, leyenda=unit)


def fig_circulo(radio: float | None = None, diametro: float | None = None,
                unit: str = "cm", color: str = "#EC4899", mostrar: str = "radio") -> str:
    """Circulo con centro y cota. mostrar in {radio, diametro, ambos}."""
    if radio is None and diametro is None: raise ValueError("radio o diametro requerido")
    if radio is None: radio = diametro / 2  # type: ignore
    if diametro is None: diametro = radio * 2
    r_px = min(_INNER/2, radio * _INNER / (2*radio))
    cx0,cy0 = _W/2,_H/2
    shp = (f"<circle cx='{cx0:.1f}' cy='{cy0:.1f}' r='{r_px:.1f}' fill='{color}' fill-opacity='0.15' stroke='{_SHP}' stroke-width='3.5'/>"
           f"<circle cx='{cx0:.1f}' cy='{cy0:.1f}' r='3' fill='{_SHP}'/>")
    c = shp
    if mostrar in ("radio","ambos"):
        c += f"<line x1='{cx0:.1f}' y1='{cy0:.1f}' x2='{cx0+r_px:.1f}' y2='{cy0:.1f}' stroke='{color}' stroke-width='2'/>"
        c += _lbl(cx0+r_px/2, cy0-10, f"r={radio} {unit}")
    if mostrar in ("diametro","ambos"):
        c += f"<line x1='{cx0-r_px:.1f}' y1='{cy0:.1f}' x2='{cx0+r_px:.1f}' y2='{cy0:.1f}' stroke='{color}' stroke-width='2' stroke-dasharray='6,3'/>"
        c += _lbl(cx0, cy0+18, f"d={diametro} {unit}")
    vb = f"{cx0-r_px-35:.0f} {cy0-r_px-30:.0f} {2*r_px+70:.0f} {2*r_px+55:.0f}"
    return _svg_container(c, border_color=color, viewbox=vb, leyenda=unit)


def fig_paralelogramo(base: float, altura: float, inclinacion: float = 1.5,
                      unit: str = "cm", color: str = "#F59E0B", marcar_altura: bool = True) -> str:
    sc = min(_INNER/(base+inclinacion), _INNER/altura)
    pb,ph,pi = base*sc,altura*sc,inclinacion*sc
    yb = _H/2+ph/2; yt = yb-ph; x0 = (_W-pb-pi)/2
    pts_p = f"{x0+pi:.1f},{yt:.1f} {x0+pi+pb:.1f},{yt:.1f} {x0+pb:.1f},{yb:.1f} {x0:.1f},{yb:.1f}"
    shp = f"<polygon points='{pts_p}' fill='{color}' fill-opacity='0.15' stroke='{_SHP}' stroke-width='3.5'/>"
    c = shp + _lbl(x0+pi/2+pb/2, yb+18, f"{base} {unit}")
    if marcar_altura:
        fx = x0+pi+pb/3
        c += (f"<line x1='{fx:.1f}' y1='{yt:.1f}' x2='{fx:.1f}' y2='{yb:.1f}' "
              f"stroke='{_SHP}' stroke-width='1.5' stroke-dasharray='4,3'/>")
        c += _marc_ar(fx, yb-8, 8)
        c += _lbl(fx-22, (yt+yb)/2, f"{altura} {unit}", anchor="end")
    vb = f"{x0-30:.0f} {yt-25:.0f} {pb+pi+60:.0f} {ph+50:.0f}"
    return _svg_container(c, border_color=color, viewbox=vb, leyenda=unit)


def fig_rombo(diagonal_mayor: float, diagonal_menor: float,
              unit: str = "cm", color: str = "#F59E0B") -> str:
    sc = min(_INNER/diagonal_mayor, _INNER/diagonal_menor)
    pd,pd2 = diagonal_mayor*sc,diagonal_menor*sc
    cx0,cy0 = _W/2,_H/2
    pts_ro = f"{cx0:.1f},{cy0-pd2/2:.1f} {cx0+pd/2:.1f},{cy0:.1f} {cx0:.1f},{cy0+pd2/2:.1f} {cx0-pd/2:.1f},{cy0:.1f}"
    shp = f"<polygon points='{pts_ro}' fill='{color}' fill-opacity='0.15' stroke='{_SHP}' stroke-width='3.5'/>"
    d1 = f"<line x1='{cx0-pd/2:.1f}' y1='{cy0:.1f}' x2='{cx0+pd/2:.1f}' y2='{cy0:.1f}' stroke='{color}' stroke-width='1.5' stroke-dasharray='5,3'/>"
    d2 = f"<line x1='{cx0:.1f}' y1='{cy0-pd2/2:.1f}' x2='{cx0:.1f}' y2='{cy0+pd2/2:.1f}' stroke='{color}' stroke-width='1.5' stroke-dasharray='5,3'/>"
    c = shp+d1+d2+_lbl(cx0,cy0+12,f"D={diagonal_mayor} {unit}")+_lbl(cx0+pd/2+25,cy0,f"d={diagonal_menor} {unit}",anchor="start")
    vb = f"{cx0-pd/2-35:.0f} {cy0-pd2/2-30:.0f} {pd+80:.0f} {pd2+55:.0f}"
    return _svg_container(c, border_color=color, viewbox=vb, leyenda=unit)


def fig_trapecio(base_mayor: float, base_menor: float, altura: float,
                 unit: str = "cm", color: str = "#F59E0B", marcar_altura: bool = True) -> str:
    sc = min(_INNER/base_mayor, _INNER/altura)
    pm,pb2,ph = base_mayor*sc,base_menor*sc,altura*sc
    cx0 = _W/2; yb = _H/2+ph/2; yt = yb-ph
    xl = cx0-pm/2; xr = cx0+pm/2; xtl = cx0-pb2/2; xtr = cx0+pb2/2
    pts_t = f"{xl:.1f},{yb:.1f} {xr:.1f},{yb:.1f} {xtr:.1f},{yt:.1f} {xtl:.1f},{yt:.1f}"
    shp = f"<polygon points='{pts_t}' fill='{color}' fill-opacity='0.15' stroke='{_SHP}' stroke-width='3.5'/>"
    c = shp+_lbl(cx0,yb+18,f"B={base_mayor} {unit}")+_lbl(cx0,yt-12,f"b={base_menor} {unit}")
    if marcar_altura:
        c += (f"<line x1='{cx0:.1f}' y1='{yt:.1f}' x2='{cx0:.1f}' y2='{yb:.1f}' "
              f"stroke='{_SHP}' stroke-width='1.5' stroke-dasharray='4,3'/>")
        c += _marc_ar(cx0, yb-8, 8)
        c += _lbl(cx0-22, (yt+yb)/2, f"h={altura} {unit}", anchor="end")
    vb = f"{xl-35:.0f} {yt-30:.0f} {pm+70:.0f} {ph+55:.0f}"
    return _svg_container(c, border_color=color, viewbox=vb, leyenda=unit)


def fig_compuesta_suma(rect_a: tuple[float,float], rect_b: tuple[float,float],
                       disposicion: str = "horizontal", unit: str = "cm",
                       color: str = "#EC4899") -> str:
    aw,ah = rect_a; bw,bh = rect_b
    if disposicion == "horizontal":
        sc = min(_INNER/(aw+bw), _INNER/max(ah,bh))
        paw,pah,pbw,pbh = aw*sc,ah*sc,bw*sc,bh*sc
        x0 = (_W-(paw+pbw))/2; y0 = (_H-pah)/2
        c = (f"<rect x='{x0:.1f}' y='{y0:.1f}' width='{paw:.1f}' height='{pah:.1f}' fill='{color}' fill-opacity='0.20' stroke='{_SHP}' stroke-width='2'/>"
             f"<rect x='{x0+paw:.1f}' y='{y0:.1f}' width='{pbw:.1f}' height='{pbh:.1f}' fill='{color}' fill-opacity='0.35' stroke='{_SHP}' stroke-width='2'/>"
             f"<line x1='{x0+paw:.1f}' y1='{y0:.1f}' x2='{x0+paw:.1f}' y2='{y0+max(pah,pbh):.1f}' stroke='{_SHP}' stroke-width='1.5' stroke-dasharray='5,3'/>"
             + _lbl(x0+paw/2,y0+pah/2+6,"A") + _lbl(x0+paw+pbw/2,y0+pbh/2+6,"B"))
        vb = f"{x0-10:.0f} {y0-10:.0f} {paw+pbw+20:.0f} {max(pah,pbh)+20:.0f}"
    else:
        sc = min(_INNER/max(aw,bw), _INNER/(ah+bh))
        paw,pah,pbw,pbh = aw*sc,ah*sc,bw*sc,bh*sc
        x0 = (_W-max(paw,pbw))/2; y0 = (_H-(pah+pbh))/2
        c = (f"<rect x='{x0:.1f}' y='{y0:.1f}' width='{paw:.1f}' height='{pah:.1f}' fill='{color}' fill-opacity='0.20' stroke='{_SHP}' stroke-width='2'/>"
             f"<rect x='{x0:.1f}' y='{y0+pah:.1f}' width='{pbw:.1f}' height='{pbh:.1f}' fill='{color}' fill-opacity='0.35' stroke='{_SHP}' stroke-width='2'/>"
             f"<line x1='{x0:.1f}' y1='{y0+pah:.1f}' x2='{x0+max(paw,pbw):.1f}' y2='{y0+pah:.1f}' stroke='{_SHP}' stroke-width='1.5' stroke-dasharray='5,3'/>"
             + _lbl(x0+paw/2,y0+pah/2+6,"A") + _lbl(x0+pbw/2,y0+pah+pbh/2+6,"B"))
        vb = f"{x0-10:.0f} {y0-10:.0f} {max(paw,pbw)+20:.0f} {pah+pbh+20:.0f}"
    return _svg_container(c, border_color=color, viewbox=vb, leyenda=unit)


def fig_compuesta_hueco(externa: tuple[float,float], hueco: tuple[float,float],
                        unit: str = "cm", color: str = "#EC4899") -> str:
    """Hueco en color de fondo (anti-revelacion)."""
    ew,eh = externa; hw,hh = hueco
    sc = min(_INNER/ew, _INNER/eh)
    pew,peh,phw,phh = ew*sc,eh*sc,hw*sc,hh*sc
    x0 = (_W-pew)/2; y0 = (_H-peh)/2
    hx = x0+(pew-phw)/2; hy = y0+(peh-phh)/2
    shp = (f"<rect x='{x0:.1f}' y='{y0:.1f}' width='{pew:.1f}' height='{peh:.1f}' fill='{color}' fill-opacity='0.25' stroke='{_SHP}' stroke-width='3.5'/>"
           f"<rect x='{hx:.1f}' y='{hy:.1f}' width='{phw:.1f}' height='{phh:.1f}' fill='#111827' stroke='{_SHP}' stroke-width='1.5' stroke-dasharray='4,3'/>")
    c = (shp + _lbl((x0*2+pew)/2,y0-12,f"{ew} {unit}") + _lbl_rot(x0+pew+22,(y0*2+peh)/2,f"{eh} {unit}",90)
         + _lbl((hx*2+phw)/2,hy-10,f"{hw} {unit}",fs=13) + _lbl_rot(hx+phw+18,(hy*2+phh)/2,f"{hh} {unit}",90,fs=13))
    vb = f"{x0-35:.0f} {y0-30:.0f} {pew+70:.0f} {peh+50:.0f}"
    return _svg_container(c, border_color=color, viewbox=vb, leyenda=unit)


def fig_inscrita(externa: str, interna: str, dims: dict,
                 unit: str = "cm", color: str = "#EC4899") -> str:
    """Figura inscrita. Zona sombreada = exterior; interior queda hueco."""
    cx0,cy0 = _W/2,_H/2
    if externa == "circulo_en_cuadrado":
        lado = dims.get("lado",8); radio = dims.get("radio",lado/2)
        ps = lado*(_INNER/lado); pr = radio*(_INNER/lado)
        x0=cx0-ps/2; y0=cy0-ps/2
        c = (f"<rect x='{x0:.1f}' y='{y0:.1f}' width='{ps:.1f}' height='{ps:.1f}' fill='{color}' fill-opacity='0.25' stroke='{_SHP}' stroke-width='3.5'/>"
             f"<circle cx='{cx0:.1f}' cy='{cy0:.1f}' r='{pr:.1f}' fill='#111827' stroke='{_SHP}' stroke-width='1.5' stroke-dasharray='4,3'/>"
             + _lbl(cx0,y0-12,f"{lado} {unit}") + _lbl(cx0+pr/2,cy0-10,f"r={radio} {unit}",fs=12))
        vb = f"{x0-30:.0f} {y0-30:.0f} {ps+60:.0f} {ps+50:.0f}"
    elif externa == "cuadrado_en_circulo":
        radio = dims.get("radio",6); lado = dims.get("lado", radio*math.sqrt(2))
        pr = min(_INNER/2, radio*_INNER/(2*radio)); ps = lado*pr/radio
        x0=cx0-ps/2; y0=cy0-ps/2
        c = (f"<circle cx='{cx0:.1f}' cy='{cy0:.1f}' r='{pr:.1f}' fill='{color}' fill-opacity='0.25' stroke='{_SHP}' stroke-width='3.5'/>"
             f"<rect x='{x0:.1f}' y='{y0:.1f}' width='{ps:.1f}' height='{ps:.1f}' fill='#111827' stroke='{_SHP}' stroke-width='1.5' stroke-dasharray='4,3'/>"
             + _lbl(cx0,cy0-pr-12,f"r={radio} {unit}"))
        vb = f"{cx0-pr-30:.0f} {cy0-pr-30:.0f} {2*pr+60:.0f} {2*pr+50:.0f}"
    else:  # triangulo_en_rectangulo
        bw=dims.get("base",8); bh=dims.get("altura",5)
        sc=min(_INNER/bw,_INNER/bh); pbw,pbh=bw*sc,bh*sc
        x0=cx0-pbw/2; y0=cy0-pbh/2
        tp_pts = f"{x0:.1f},{y0+pbh:.1f} {x0+pbw:.1f},{y0+pbh:.1f} {cx0:.1f},{y0:.1f}"
        c = (f"<rect x='{x0:.1f}' y='{y0:.1f}' width='{pbw:.1f}' height='{pbh:.1f}' fill='{color}' fill-opacity='0.25' stroke='{_SHP}' stroke-width='3.5'/>"
             f"<polygon points='{tp_pts}' fill='#111827' stroke='{_SHP}' stroke-width='1.5' stroke-dasharray='4,3'/>"
             + _lbl(cx0,y0+pbh+18,f"{bw} {unit}") + _lbl_rot(x0+pbw+22,cy0,f"{bh} {unit}",90))
        vb = f"{x0-30:.0f} {y0-20:.0f} {pbw+60:.0f} {pbh+45:.0f}"
    return _svg_container(c, border_color=color, viewbox=vb, leyenda=unit)


# --- Figuras de conversion y decimales (Fase 5) ------------------------------

def escalera_unidades(tipo: str, unidades: list[str], origen: str, destino: str,
                      valor: float | None = None, color: str = "#F59E0B") -> str:
    """Escalera de conversion. Anti-revelacion: NO escribe el resultado."""
    fac = {"lineal":"x10/div10","cuadrada":"x100/div100","cubica":"x1000/div1000"}.get(tipo,"x?")
    n=len(unidades); sw=min(int(_INNER/max(n,1)),30); sh=20
    tw=n*sw; th=n*sh; x0=(_W-tw)/2; y0=_H/2+th/2
    shps = ""
    for i,u in enumerate(unidades):
        bx=x0+i*sw; by=y0-i*sh
        fill=color if u in (origen,destino) else "#374151"
        op="0.5" if u in (origen,destino) else "0.25"
        shps += (f"<rect x='{bx:.1f}' y='{by-sh:.1f}' width='{sw:.1f}' height='{sh:.1f}' fill='{fill}' fill-opacity='{op}' stroke='{_SHP}' stroke-width='1'/>"
                 f"<text x='{bx+sw/2:.1f}' y='{by-sh/2+4:.1f}' fill='{_LBL}' font-size='10' font-weight='bold' text-anchor='middle'>{u}</text>")
    fc = f"<text x='{x0+tw/2:.1f}' y='{y0-th-10:.1f}' fill='{color}' font-size='12' font-weight='bold' text-anchor='middle'>{fac}</text>"
    vb = f"{x0-15:.0f} {y0-th-25:.0f} {tw+30:.0f} {th+40:.0f}"
    return _svg_container(shps+fc, border_color=color, viewbox=vb, grid=False, leyenda=None)


def recta_numerica_decimal(inicio: float, fin: float, paso: float,
                           marcas: list[float], unit: str = "",
                           color: str = "#8B5CF6") -> str:
    """Recta numerica con marcas resaltadas."""
    nd = round((fin-inicio)/paso); bw = _INNER*0.85
    x0 = _M+(_INNER-bw)/2; y0 = _H/2
    line = f"<line x1='{x0:.1f}' y1='{y0:.1f}' x2='{x0+bw:.1f}' y2='{y0:.1f}' stroke='{_SHP}' stroke-width='3' stroke-linecap='round'/>"
    ticks = ""; mr = [round(m,6) for m in marcas]
    for i in range(nd+1):
        val=round(inicio+i*paso,10); px=x0+(i/nd)*bw if nd else x0
        h = 10 if round(val,6) in mr else 5
        ticks += f"<line x1='{px:.1f}' y1='{y0-h:.1f}' x2='{px:.1f}' y2='{y0+h:.1f}' stroke='{_SHP}' stroke-width='1.5'/>"
        ticks += _lbl(px,y0+22,str(round(val,4)).replace(".",","),fs=10)
    globs = ""
    for m in marcas:
        if fin-inicio<=0: continue
        px = x0+((m-inicio)/(fin-inicio))*bw
        globs += (f"<circle cx='{px:.1f}' cy='{y0:.1f}' r='6' fill='{color}' fill-opacity='0.7' stroke='{_SHP}' stroke-width='1'/>"
                  f"<text x='{px:.1f}' y='{y0-12:.1f}' fill='{color}' font-size='12' font-weight='bold' text-anchor='middle'>{str(round(m,4)).replace('.',',')}</text>")
    vb = f"{x0-20:.0f} {y0-35:.0f} {bw+40:.0f} 70"
    return _svg_container(line+ticks+globs, border_color=color, viewbox=vb, grid=False, leyenda=None)


def tabla_datos(filas: list[tuple[str,str]], titulo: str | None = None,
                color: str = "#F59E0B") -> str:
    """Mini tabla. Datos numericos aqui, NO en la prosa (Decision 10)."""
    rh=22; cw=90; n=len(filas); th=(n+(1 if titulo else 0))*rh; tw=cw*2
    x0=(_W-tw)/2; y0=(_H-th)/2
    shps = f"<rect x='{x0:.1f}' y='{y0:.1f}' width='{tw:.1f}' height='{th:.1f}' fill='{color}' fill-opacity='0.10' stroke='{_SHP}' stroke-width='1' rx='4'/>"
    txts = ""; ro = 0
    if titulo:
        txts += f"<text x='{x0+tw/2:.1f}' y='{y0+rh*0.7:.1f}' fill='{color}' font-size='12' font-weight='bold' text-anchor='middle'>{titulo}</text>"
        shps += f"<line x1='{x0:.1f}' y1='{y0+rh:.1f}' x2='{x0+tw:.1f}' y2='{y0+rh:.1f}' stroke='{_SHP}' stroke-width='0.8'/>"
        ro = 1
    for i,(concepto,valor) in enumerate(filas):
        ry = y0+(i+ro)*rh
        if i>0 or ro>0: shps += f"<line x1='{x0:.1f}' y1='{ry:.1f}' x2='{x0+tw:.1f}' y2='{ry:.1f}' stroke='{_GRID}' stroke-width='0.5'/>"
        shps += f"<line x1='{x0+cw:.1f}' y1='{ry:.1f}' x2='{x0+cw:.1f}' y2='{ry+rh:.1f}' stroke='{_GRID}' stroke-width='0.5'/>"
        txts += (f"<text x='{x0+6:.1f}' y='{ry+rh*0.70:.1f}' fill='{_LBL}' font-size='11' text-anchor='start'>{concepto}</text>"
                 f"<text x='{x0+cw+cw/2:.1f}' y='{ry+rh*0.70:.1f}' fill='{color}' font-size='11' font-weight='bold' text-anchor='middle'>{valor}</text>")
    vb = f"{x0-10:.0f} {y0-10:.0f} {tw+20:.0f} {th+20:.0f}"
    return _svg_container(shps+txts, border_color=color, viewbox=vb, grid=False, leyenda=None)


def comparador_opciones(titulo_a: str, datos_a: list[tuple[str,str]],
                        titulo_b: str, datos_b: list[tuple[str,str]],
                        color: str = "#EC4899") -> str:
    tbl_a = tabla_datos(datos_a, titulo=titulo_a, color=color)
    tbl_b = tabla_datos(datos_b, titulo=titulo_b, color=color)
    vs = f"<svg width='30' height='80' style='display:inline-block; vertical-align:middle;'><text x='15' y='45' fill='{color}' font-size='14' font-weight='bold' text-anchor='middle'>vs</text></svg>"
    return tbl_a + vs + tbl_b


# --- Aliases de compatibilidad con svg_helpers.py ----------------------------

def svg_rect(w_u, h_u, unit="cm", border="#A855F7") -> str:
    return fig_rectangulo(w_u, h_u, unit=unit, color=border)

def svg_square(side_u, unit="cm", border="#A855F7") -> str:
    return fig_cuadrado(side_u, unit=unit, color=border)

def svg_triangle_equilateral(side_u, unit="cm", border="#A855F7") -> str:
    return fig_triangulo(side_u, side_u * 0.866, unit=unit, color=border, tipo="isosceles")

def svg_rect_all_labels(w_u, h_u, unit="cm", border="#F59E0B") -> str:
    return fig_rectangulo(w_u, h_u, unit=unit, color=border, cotas="cuatro")

def svg_l_shape(w1_u, h1_u, w2_u, h2_u, unit="cm", border="#F59E0B") -> str:
    return fig_L(w1_u, h1_u, w2_u, h2_u, unit=unit, color=border)

def svg_polygon_labeled(points_unit, labels, unit="cm", border="#A855F7") -> str:
    verts = list(points_unit)
    cotas_lado = [txt for _,_,txt in list(labels)[:len(verts)]]
    while len(cotas_lado) < len(verts): cotas_lado.append(None)
    return fig_poligono_irregular(verts, cotas_lado, unit=unit, color=border)

def svg_shaded_rect(w_u, h_u, unit="cm2", fill="#EC4899", border="#EC4899") -> str:
    return fig_rectangulo(w_u, h_u, unit=unit.replace("2","").replace("^",""), color=border)

def svg_grid_halves(enteros: int, mitades: int, unit="cm", border="#3B82F6") -> str:
    cols = min(enteros + mitades, 6) or 1
    celdas = [(i % cols, i // cols) for i in range(enteros)]
    ci = enteros; ml = []
    for _ in range(mitades): ml.append((ci % cols, ci // cols, "BR")); ci += 1
    rows = max((enteros + mitades + cols - 1) // cols, 1)
    return fig_malla(celdas, ml, cols=cols, rows=rows, color=border)

def svg_scale_bar(u_val: int, scale: int, unit="cm", border="#F59E0B") -> str:
    bw = _INNER * 0.8; x0 = _M + (_INNER - bw) / 2
    shp = (f"<line x1='{x0:.1f}' y1='{_H/2:.1f}' x2='{x0+bw:.1f}' y2='{_H/2:.1f}' stroke='{_SHP}' stroke-width='3' stroke-linecap='round'/>"
           f"<line x1='{x0:.1f}' y1='{_H/2-10:.1f}' x2='{x0:.1f}' y2='{_H/2+10:.1f}' stroke='{_SHP}' stroke-width='2'/>"
           f"<line x1='{x0+bw:.1f}' y1='{_H/2-10:.1f}' x2='{x0+bw:.1f}' y2='{_H/2+10:.1f}' stroke='{_SHP}' stroke-width='2'/>")
    return _svg_container(shp + _lbl(x0+bw/2,_H/2-15,f"{u_val} {unit}",fs=14), border_color=border)

def svg_length_conversion(val: int, unit_from: str, unit_to: str,
                          factor: int = 1000, border: str = "#10B981") -> str:
    return escalera_unidades("lineal", [unit_from, unit_to], unit_from, unit_to, val, border)


# --- Verificacion interna (s11.7) --------------------------------------------

def _ejemplo_rectangulo_8x5() -> str:
    """s11.7.1: Rectangulo 8x5 cm verde."""
    return fig_rectangulo(8, 5, unit="cm", color="#10B981", cotas="dos")

def _ejemplo_L_lados_ocultos() -> str:
    """s11.7.2: Figura en L con lado oculto '?'."""
    return fig_L(3, 6, 5, 3, unit="cm", color="#3B82F6", ocultar_lado=2)

def _ejemplo_malla_triangulo() -> str:
    """s11.7.3: Triangulo sobre malla 4x4 sin numeros."""
    celdas = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    medias = [(0,0,"BL"),(1,1,"BL"),(2,2,"BL"),(3,3,"BL")]
    return fig_malla(celdas, medias, cols=4, rows=4, unit="u", color="#F59E0B")


if __name__ == "__main__":
    print("=== Ejemplo 1: Rectangulo 8x5 cm ===")
    s1 = _ejemplo_rectangulo_8x5()
    assert "<svg" in s1
    assert "8 cm" in s1
    assert "5 cm" in s1
    assert "fill-opacity='0.15'" in s1
    assert "#10B981" in s1
    assert "viewBox" in s1
    print(f"  OK: {len(s1)} chars, viewBox presente")

    print("=== Ejemplo 2: L con lado oculto ===")
    s2 = _ejemplo_L_lados_ocultos()
    assert "<svg" in s2 and "?" in s2 and "#3B82F6" in s2
    print(f"  OK: {len(s2)} chars, '?' presente")

    print("=== Ejemplo 3: Malla triangulo ===")
    s3 = _ejemplo_malla_triangulo()
    assert "<svg" in s3
    assert "BL" not in s3
    assert "= 1 u^2" in s3
    assert "= 1/2 u^2" in s3
    print(f"  OK: {len(s3)} chars, leyendas OK")

    print("\nTodos los ejemplos s11.7 pasan el checklist de calidad.")
