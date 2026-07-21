import math
import io
import random
from PIL import Image, ImageDraw, ImageFont

def get_font(size: int):
    """Intenta cargar una fuente limpia, si no, usa la por defecto."""
    try:
        font_names = [
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", # Docker container path
            "arial.ttf", 
            "DejaVuSans-Bold.ttf", 
            "LiberationSans-Bold.ttf"
        ]
        for name in font_names:
            try:
                return ImageFont.truetype(name, size)
            except IOError:
                continue
        return ImageFont.load_default()
    except Exception:
        return ImageFont.load_default()

def draw_antialiased_circle(draw: ImageDraw.Draw, xy, fill=None, outline=None, width=1):
    """Dibuja un círculo suave usando el método de elipse."""
    draw.ellipse(xy, fill=fill, outline=outline, width=width)

def _draw_dimension_line(img: Image.Image, draw: ImageDraw.Draw, p1: tuple, p2: tuple, label: str, offset: float, font, color=(30, 30, 30, 255)):
    """Dibuja flechas bidireccionales paralelas a un segmento con texto centrado."""
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    if length == 0: return
    ux, uy = dx / length, dy / length
    nx, ny = -uy, ux # normal points to the left of p1->p2
    
    l1x, l1y = x1 + nx * offset, y1 + ny * offset
    l2x, l2y = x2 + nx * offset, y2 + ny * offset
    
    draw.line([l1x, l1y, l2x, l2y], fill=color, width=2)
    
    arrow_len = 8
    draw.polygon([
        (l1x, l1y),
        (l1x + ux * arrow_len + nx * arrow_len/2, l1y + uy * arrow_len + ny * arrow_len/2),
        (l1x + ux * arrow_len - nx * arrow_len/2, l1y + uy * arrow_len - ny * arrow_len/2)
    ], fill=color)
    draw.polygon([
        (l2x, l2y),
        (l2x - ux * arrow_len + nx * arrow_len/2, l2y - uy * arrow_len + ny * arrow_len/2),
        (l2x - ux * arrow_len - nx * arrow_len/2, l2y - uy * arrow_len - ny * arrow_len/2)
    ], fill=color)
    
    # Guide lines
    draw.line([x1 + nx * 2, y1 + ny * 2, l1x - nx * 2, l1y - ny * 2], fill=color, width=1)
    draw.line([x2 + nx * 2, y2 + ny * 2, l2x - nx * 2, l2y - ny * 2], fill=color, width=1)

    mx, my = (l1x + l2x) / 2, (l1y + l2y) / 2
    angle = math.degrees(math.atan2(dy, dx))
    
    if angle > 90 or angle < -89:
        angle += 180
        nx, ny = -nx, -ny
        
    try:
        bbox = draw.textbbox((0, 0), label, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
    except AttributeError:
        tw, th = draw.textsize(label, font=font)
        
    txt_img = Image.new('RGBA', (int(tw) + 4, int(th) + 4), (255, 255, 255, 0))
    txt_draw = ImageDraw.Draw(txt_img)
    txt_draw.text((2, 2), label, fill=color, font=font)
    
    txt_rotated = txt_img.rotate(-angle, expand=True, resample=Image.Resampling.BICUBIC)
    
    tx = int(mx + nx * 40 - txt_rotated.width / 2)
    ty = int(my + ny * 40 - txt_rotated.height / 2)
    img.paste(txt_rotated, (tx, ty), txt_rotated)

def generate_clean_shape_image(shape_type: str, dimensions: dict, unit_label: str = "cm", fill_color=(224, 247, 250, 180), outline_color=(30, 30, 30, 255)) -> bytes:
    """Genera polígonos con cotas externas tipo ingeniería sobre fondo blanco. Figura grande, legible y premium."""
    # --- Canvas setup ---
    IMG_SIZE  = 1200          # canvas cuadrado grande para máxima nitidez
    MARGIN    = 180           # espacio lateral amplio para las cotas
    DRAW_AREA = IMG_SIZE - 2 * MARGIN   # zona disponible para la figura

    img  = Image.new("RGBA", (IMG_SIZE, IMG_SIZE), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = get_font(100)        # fuente MUY grande para que se lea sin zoom

    cx, cy = IMG_SIZE / 2, IMG_SIZE / 2

    # --- Definición de puntos lógicos y cotas para cada tipo ---
    pts           = []
    lines_to_draw = []
    OFFSET = 80  # separación de la línea de cota a la figura

    if shape_type == "rectangle":
        w = dimensions.get("base", 6)
        h = dimensions.get("height", 4)
        pts = [(0, 0), (0, h), (w, h), (w, 0)]
        lines_to_draw.append(((0, h), (w, h), f"{w} {unit_label}", OFFSET))   # base (abajo)
        lines_to_draw.append(((0, 0), (0, h), f"{h} {unit_label}", OFFSET))   # altura (izquierda)

    elif shape_type == "square":
        s = dimensions.get("side", 5)
        pts = [(0, 0), (0, s), (s, s), (s, 0)]
        lines_to_draw.append(((0, s), (s, s), f"{s} {unit_label}", OFFSET))
        lines_to_draw.append(((0, 0), (0, s), f"{s} {unit_label}", OFFSET))

    elif shape_type == "triangle":
        b = dimensions.get("base", 5)
        h = dimensions.get("height", 4)
        c = dimensions.get("hypotenuse", round(math.hypot(b, h), 1))
        pts = [(0, 0), (0, h), (b, h)]
        lines_to_draw.append(((0, h), (b, h), f"{b} {unit_label}", OFFSET))
        lines_to_draw.append(((0, 0), (0, h), f"{h} {unit_label}", OFFSET))
        lines_to_draw.append(((b, h), (0, 0), f"{c} {unit_label}", OFFSET))

    elif shape_type == "trapezoid":
        top    = dimensions.get("top", 4)
        bottom = dimensions.get("bottom", 8)
        h      = dimensions.get("height", 5)
        side   = dimensions.get("side", round(math.hypot((bottom-top)/2, h), 1))
        ox     = (bottom - top) / 2
        pts = [(ox, 0), (0, h), (bottom, h), (ox + top, 0)]
        lines_to_draw.append(((ox + top, 0), (ox, 0),       f"{top} {unit_label}",    OFFSET))
        lines_to_draw.append(((0, h),        (bottom, h),   f"{bottom} {unit_label}", OFFSET))
        lines_to_draw.append(((bottom, h),   (ox + top, 0), f"{side} {unit_label}",   OFFSET))
        lines_to_draw.append(((ox, 0),       (0, h),        f"{side} {unit_label}",   OFFSET))

    elif shape_type == "l_shape":
        w1 = dimensions.get("w1", 3)
        h1 = dimensions.get("h1", 6)
        w2 = dimensions.get("w2", 5)
        h2 = dimensions.get("h2", 2)
        pts = [(0, 0), (0, h1), (w1+w2, h1), (w1+w2, h1-h2), (w1, h1-h2), (w1, 0)]
        lines_to_draw.append(((0, 0),       (0, h1),       f"{h1} {unit_label}",    OFFSET))
        lines_to_draw.append(((0, h1),      (w1+w2, h1),   f"{w1+w2} {unit_label}", OFFSET))
        lines_to_draw.append(((w1+w2, h1),  (w1+w2, h1-h2),f"{h2} {unit_label}",   OFFSET))
        lines_to_draw.append(((w1+w2, h1-h2),(w1, h1-h2),  f"{w2} {unit_label}",   OFFSET))
        lines_to_draw.append(((w1, h1-h2),  (w1, 0),       f"{h1-h2} {unit_label}", OFFSET))
        lines_to_draw.append(((w1, 0),      (0, 0),        f"{w1} {unit_label}",    OFFSET))
    else:
        pts = [(0, 0), (0, 5), (5, 5), (5, 0)]

    # --- Escala: la figura ocupa DRAW_AREA dentro del margen ---
    min_x = min(p[0] for p in pts)
    max_x = max(p[0] for p in pts)
    min_y = min(p[1] for p in pts)
    max_y = max(p[1] for p in pts)
    logic_w = max_x - min_x
    logic_h = max_y - min_y

    scale = min(DRAW_AREA / max(logic_w, 0.001),
                DRAW_AREA / max(logic_h, 0.001))

    def to_px(lx, ly):
        px = cx + (lx - min_x - logic_w / 2) * scale
        py = cy + (ly - min_y - logic_h / 2) * scale
        return (px, py)

    # --- Dibujo de la figura ---
    physical_pts = [to_px(lx, ly) for lx, ly in pts]
    draw.polygon(physical_pts, fill=fill_color, outline=outline_color, width=5)

    # --- Cotas externas ---
    for p1_log, p2_log, label, offset in lines_to_draw:
        p1 = to_px(*p1_log)
        p2 = to_px(*p2_log)
        _draw_dimension_line(img, draw, p1, p2, label, offset, font, outline_color)

    # --- Exportar a 700×700 (máxima legibilidad) ---
    img_resized = img.resize((700, 700), Image.Resampling.LANCZOS)
    output = io.BytesIO()
    img_resized.save(output, format="PNG")
    return output.getvalue()



def _generate_random_staircase(rng: random.Random, grid_w: int, grid_h: int, target_area: int):
    """Genera una forma conexa irregular y calcula su perímetro."""
    start_c, start_r = grid_w // 2, grid_h // 2
    cells = set([(start_c, start_r)])
    
    while len(cells) < target_area:
        adjacent = set()
        for c, r in cells:
            for dc, dr in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nc, nr = c + dc, r + dr
                if 0 <= nc < grid_w and 0 <= nr < grid_h:
                    if (nc, nr) not in cells:
                        adjacent.add((nc, nr))
        if not adjacent:
            break
        cells.add(rng.choice(list(adjacent)))
        
    perimeter = 0
    for c, r in cells:
        for dc, dr in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if (c + dc, r + dr) not in cells:
                perimeter += 1
                
    min_c = min(c for c, r in cells)
    max_c = max(c for c, r in cells)
    min_r = min(r for c, r in cells)
    max_r = max(r for c, r in cells)
    
    offset_c = (grid_w - (max_c - min_c + 1)) // 2 - min_c
    offset_r = (grid_h - (max_r - min_r + 1)) // 2 - min_r
    
    centered_cells = [(c + offset_c, r + offset_r) for c, r in cells]
    return centered_cells, perimeter

def generate_irregular_grid_shape_image(cells: list, grid_size: tuple = (10, 10), fill_color=(255, 182, 193, 180), outline_color=(60, 60, 60, 255)) -> bytes:
    """Dibuja formas escalonadas o irregulares pintando celdas en cuadrícula."""
    size = 800
    img = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    left_margin = 60
    top_margin = 60
    grid_w = 680
    grid_h = 680
    
    cols, rows = grid_size
    cell_w = grid_w / cols
    cell_h = grid_h / rows
    
    def to_pixel(gx, gy):
        return (int(left_margin + gx * cell_w), int(top_margin + gy * cell_h))

    grid_line_color = (200, 200, 200, 120)
    for c in range(cols + 1):
        x1, y1 = to_pixel(c, 0)
        x2, y2 = to_pixel(c, rows)
        draw.line([x1, y1, x2, y2], fill=grid_line_color, width=2)
        
    for r in range(rows + 1):
        x1, y1 = to_pixel(0, r)
        x2, y2 = to_pixel(cols, r)
        draw.line([x1, y1, x2, y2], fill=grid_line_color, width=2)

    cells_set = set(cells)
    for c, r in cells:
        px1, py1 = to_pixel(c, r)
        px2, py2 = to_pixel(c + 1, r + 1)
        draw.rectangle([px1, py1, px2, py2], fill=fill_color)
        
    for c, r in cells:
        px1, py1 = to_pixel(c, r)
        px2, py2 = to_pixel(c + 1, r + 1)
        if (c, r - 1) not in cells_set:
            draw.line([px1, py1, px2, py1], fill=outline_color, width=3)
        if (c, r + 1) not in cells_set:
            draw.line([px1, py2, px2, py2], fill=outline_color, width=3)
        if (c - 1, r) not in cells_set:
            draw.line([px1, py1, px1, py2], fill=outline_color, width=3)
        if (c + 1, r) not in cells_set:
            draw.line([px2, py1, px2, py2], fill=outline_color, width=3)

    x1, y1 = to_pixel(0, 0)
    x2, y2 = to_pixel(cols, rows)
    draw.rectangle([x1, y1, x2, y2], outline=(60, 60, 60, 255), width=2)

    img_resized = img.resize((400, 400), Image.Resampling.LANCZOS)
    output = io.BytesIO()
    img_resized.save(output, format="PNG")
    return output.getvalue()

def _build_step_shape(rng: random.Random, unit_label="cm"):
    """Helper for generating a rectilinear step shape (L inverted or 2-step stair)."""
    w1 = rng.randint(2, 6)
    w2 = rng.randint(2, 6)
    h1 = rng.randint(2, 6)
    h2 = rng.randint(2, 6)
    
    segments = [
        (0, h1+h2, w1+w2, h1+h2, f"{w1+w2} {unit_label}"), # bottom
        (w1+w2, h1+h2, w1+w2, h2, f"{h1} {unit_label}"), # right bottom
        (w1+w2, h2, w1, h2, f"{w2} {unit_label}"), # middle top
        (w1, h2, w1, 0, f"{h2} {unit_label}"), # right top
        (w1, 0, 0, 0, f"{w1} {unit_label}"), # top
        (0, 0, 0, h1+h2, f"{h1+h2} {unit_label}") # left
    ]
    perimeter = 2*(w1+w2) + 2*(h1+h2)
    return segments, perimeter

def generate_rectilinear_shape_image(segments: list, fill_color=(224, 247, 250, 180), outline_color=(30, 30, 30, 255)) -> bytes:
    """Genera figuras rectilíneas compuestas con cotas en cada borde."""
    size = 800
    img = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = get_font(42)

    pts = []
    for x1, y1, x2, y2, label in segments:
        pts.append((x1, y1))
        
    min_x = min(p[0] for p in pts)
    max_x = max(p[0] for p in pts)
    min_y = min(p[1] for p in pts)
    max_y = max(p[1] for p in pts)
    
    logic_w = max_x - min_x
    logic_h = max_y - min_y
    
    scale = min(450 / max(logic_w, 1), 450 / max(logic_h, 1))
    cx, cy = size / 2, size / 2
    
    def to_px(lx, ly):
        px = cx + (lx - min_x - logic_w/2) * scale
        py = cy + (ly - min_y - logic_h/2) * scale
        return (px, py)
        
    physical_pts = [to_px(lx, ly) for lx, ly in pts]
    draw.polygon(physical_pts, fill=fill_color, outline=outline_color, width=3)
    
    for x1, y1, x2, y2, label in segments:
        if not label: continue
        p1 = to_px(x1, y1)
        p2 = to_px(x2, y2)
        _draw_dimension_line(img, draw, p1, p2, label, 40, font, outline_color)
        
    img_resized = img.resize((400, 400), Image.Resampling.LANCZOS)
    output = io.BytesIO()
    img_resized.save(output, format="PNG")
    return output.getvalue()

def generate_grid_shape_image(vertices: list, grid_size: tuple = (10, 10), fill_color=(224, 247, 250, 180), outline_color=(30, 30, 30, 255), labels=None) -> bytes:
    """Dibuja una cuadrícula matemática con un polígono relleno y una leyenda de escala."""
    size = 800
    img = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = get_font(36)

    left_margin = 60
    top_margin = 60
    grid_w = 520
    grid_h = 520
    
    cols, rows = grid_size
    cell_w = grid_w / cols
    cell_h = grid_h / rows
    
    def to_pixel(gx, gy):
        return (int(left_margin + gx * cell_w), int(top_margin + gy * cell_h))

    grid_line_color = (200, 200, 200, 100)
    for c in range(cols + 1):
        x1, y1 = to_pixel(c, 0)
        x2, y2 = to_pixel(c, rows)
        draw.line([x1, y1, x2, y2], fill=grid_line_color, width=2)
        
    for r in range(rows + 1):
        x1, y1 = to_pixel(0, r)
        x2, y2 = to_pixel(cols, r)
        draw.line([x1, y1, x2, y2], fill=grid_line_color, width=2)
        
    border_color = (150, 150, 150, 200)
    x1, y1 = to_pixel(0, 0)
    x2, y2 = to_pixel(cols, rows)
    draw.rectangle([x1, y1, x2, y2], outline=border_color, width=2)

    if len(vertices) >= 3:
        px_vertices = [to_pixel(vx, vy) for vx, vy in vertices]
        draw.polygon(px_vertices, fill=fill_color)
        for idx in range(len(px_vertices)):
            v1 = px_vertices[idx]
            v2 = px_vertices[(idx + 1) % len(px_vertices)]
            draw.line([v1[0], v1[1], v2[0], v2[1]], fill=outline_color, width=3)
            
            if labels and (idx, (idx+1)%len(px_vertices)) in labels:
                label = labels[(idx, (idx+1)%len(px_vertices))]
                _draw_dimension_line(img, draw, v1, v2, label, 30, font, outline_color)

    legend_x = 600
    legend_y = 200
    sq_size = 60
    draw.rectangle([legend_x, legend_y, legend_x + sq_size, legend_y + sq_size], fill=fill_color, outline=outline_color, width=2)
    
    label_text1 = "Área = 1 u²"
    label_text2 = "Cuadrado escala"
    draw.text((legend_x - 15, legend_y + sq_size + 15), label_text1, fill=(30, 30, 30, 255), font=font)
    draw.text((legend_x - 35, legend_y + sq_size + 65), label_text2, fill=(80, 80, 80, 255), font=get_font(26))

    img_resized = img.resize((400, 400), Image.Resampling.LANCZOS)
    output = io.BytesIO()
    img_resized.save(output, format="PNG")
    return output.getvalue()

def generate_clock_image(hour: int, minute: int) -> bytes:
    size = 600
    img = Image.new("RGBA", (size, size), (30, 41, 59, 0))
    draw = ImageDraw.Draw(img)

    center = size // 2
    radius = int(center * 0.85)

    draw.ellipse([center - radius, center - radius, center + radius, center + radius], fill=(15, 23, 42, 255), outline=(56, 189, 248, 255), width=8)
    draw.ellipse([center - radius + 8, center - radius + 8, center + radius - 8, center + radius - 8], outline=(56, 189, 248, 40), width=4)

    font = get_font(40)
    for m in range(60):
        angle = math.radians(6 * m - 90)
        is_hour = (m % 5 == 0)
        tick_length = 24 if is_hour else 10
        tick_width = 4 if is_hour else 2
        tick_color = (255, 255, 255, 220) if is_hour else (100, 116, 139, 150)
        x1 = center + (radius - 12 - tick_length) * math.cos(angle)
        y1 = center + (radius - 12 - tick_length) * math.sin(angle)
        x2 = center + (radius - 12) * math.cos(angle)
        y2 = center + (radius - 12) * math.sin(angle)
        draw.line([x1, y1, x2, y2], fill=tick_color, width=tick_width)

    for h in range(1, 13):
        angle = math.radians(30 * h - 90)
        dist = radius - 55
        nx = center + dist * math.cos(angle)
        ny = center + dist * math.sin(angle)
        text = str(h)
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
        except AttributeError:
            tw, th = draw.textsize(text, font=font)
        draw.text((nx - tw // 2, ny - th // 2 - 4), text, fill=(248, 250, 252, 255), font=font)

    hour_angle = math.radians(30 * (hour % 12 + minute / 60.0) - 90)
    minute_angle = math.radians(6 * minute - 90)

    hour_len = int(radius * 0.52)
    hx = center + hour_len * math.cos(hour_angle)
    hy = center + hour_len * math.sin(hour_angle)
    draw.line([center, center, hx, hy], fill=(56, 189, 248, 255), width=12)

    minute_len = int(radius * 0.76)
    mx = center + minute_len * math.cos(minute_angle)
    my = center + minute_len * math.sin(minute_angle)
    draw.line([center, center, mx, my], fill=(249, 115, 22, 255), width=8)

    draw.ellipse([center - 12, center - 12, center + 12, center + 12], fill=(255, 255, 255, 255), outline=(15, 23, 42, 255), width=3)
    draw.ellipse([center - 4, center - 4, center + 4, center + 4], fill=(249, 115, 22, 255))

    img_resized = img.resize((300, 300), Image.Resampling.LANCZOS)
    output = io.BytesIO()
    img_resized.save(output, format="PNG")
    return output.getvalue()

def generate_cartesian_plane_image(points: list) -> bytes:
    size = 800
    img = Image.new("RGBA", (size, size), (30, 41, 59, 0))
    draw = ImageDraw.Draw(img)

    margin = 80
    grid_area = size - 2 * margin
    min_val, max_val = -1, 7
    units = max_val - min_val
    cell_size = grid_area / units
    
    def to_pixel(x, y):
        px = margin + (x - min_val) * cell_size
        py = margin + (max_val - y) * cell_size
        return int(px), int(py)

    grid_color = (71, 85, 105, 100)
    for i in range(units + 1):
        val = min_val + i
        x1, y1 = to_pixel(val, min_val)
        x2, y2 = to_pixel(val, max_val)
        draw.line([x1, y1, x2, y2], fill=grid_color, width=2)
        x1_h, y1_h = to_pixel(min_val, val)
        x2_h, y2_h = to_pixel(max_val, val)
        draw.line([x1_h, y1_h, x2_h, y2_h], fill=grid_color, width=2)

    axis_color = (248, 250, 252, 220)
    x0, y0_min = to_pixel(0, min_val)
    _, y0_max = to_pixel(0, max_val)
    draw.line([x0, y0_min, x0, y0_max], fill=axis_color, width=5)
    draw.polygon([x0, y0_max - 15, x0 - 10, y0_max, x0 + 10, y0_max], fill=axis_color)
    
    x0_min, y0 = to_pixel(min_val, 0)
    x0_max, _ = to_pixel(max_val, 0)
    draw.line([x0_min, y0, x0_max, y0], fill=axis_color, width=5)
    draw.polygon([x0_max + 15, y0, x0_max, y0 - 10, x0_max, y0 + 10], fill=axis_color)

    font = get_font(22)
    for val in range(min_val, max_val + 1):
        if val == 0:
            x, y = to_pixel(0, 0)
            draw.text((x - 20, y + 10), "0", fill=(226, 232, 240, 255), font=font)
            continue
        x, y = to_pixel(val, 0)
        text_x = str(val)
        try:
            bbox = draw.textbbox((0, 0), text_x, font=font)
            tw = bbox[2] - bbox[0]
        except AttributeError:
            tw, _ = draw.textsize(text_x, font=font)
        draw.text((x - tw // 2, y + 10), text_x, fill=(203, 213, 225, 255), font=font)
        
        x, y = to_pixel(0, val)
        text_y = str(val)
        try:
            bbox = draw.textbbox((0, 0), text_y, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
        except AttributeError:
            tw, th = draw.textsize(text_y, font=font)
        draw.text((x - tw - 12, y - th // 2), text_y, fill=(203, 213, 225, 255), font=font)

    label_font = get_font(28)
    ex_x, ex_y = to_pixel(max_val, 0)
    draw.text((ex_x + 25, ex_y - 12), "X", fill=(56, 189, 248, 255), font=label_font)
    ey_x, ey_y = to_pixel(0, max_val)
    draw.text((ey_x - 12, ey_y - 35), "Y", fill=(56, 189, 248, 255), font=label_font)

    point_font = get_font(24)
    for p in points:
        px = p["x"]
        py = p["y"]
        label = p.get("label", "")
        cx, cy = to_pixel(px, py)
        cx_0, cy_0 = to_pixel(px, 0)
        draw.line([cx, cy, cx_0, cy_0], fill=(203, 213, 225, 120), width=2)
        cx_y0, cy_y0 = to_pixel(0, py)
        draw.line([cx, cy, cx_y0, cy_y0], fill=(203, 213, 225, 120), width=2)
        dot_r = 10
        draw.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill=(249, 115, 22, 255), outline=(255, 255, 255, 255), width=2)
        label_text = f"{label}({px},{py})" if label else f"({px},{py})"
        draw.text((cx + 14, cy - 30), label_text, fill=(255, 255, 255, 255), font=point_font)

    img_resized = img.resize((400, 400), Image.Resampling.LANCZOS)
    output = io.BytesIO()
    img_resized.save(output, format="PNG")
    return output.getvalue()

def generate_isometric_cubes_image(cubes: list) -> bytes:
    width, height = 800, 600
    img = Image.new("RGBA", (width, height), (30, 41, 59, 0))
    draw = ImageDraw.Draw(img)

    block_size = 45
    cos30 = math.cos(math.radians(30))
    sin30 = math.sin(math.radians(30))
    w_iso = block_size * cos30
    h_iso = block_size * sin30
    block_h = block_size
    origin_x = width // 2
    origin_y = height // 2 + 100

    def get_iso_coords(x, y, z):
        px = origin_x + (x - y) * w_iso
        py = origin_y + (x + y) * h_iso - z * block_h
        return px, py

    sorted_cubes = sorted(cubes, key=lambda c: (c[2], c[0], c[1]))

    for x, y, z in sorted_cubes:
        cx, cy = get_iso_coords(x, y, z)
        top_pts = [(cx, cy - h_iso), (cx + w_iso, cy), (cx, cy + h_iso), (cx - w_iso, cy)]
        left_pts = [(cx - w_iso, cy), (cx, cy + h_iso), (cx, cy + h_iso + block_h), (cx - w_iso, cy + block_h)]
        right_pts = [(cx, cy + h_iso), (cx + w_iso, cy), (cx + w_iso, cy + block_h), (cx, cy + h_iso + block_h)]

        top_fill = (241, 245, 249, 255)
        right_fill = (148, 163, 184, 255)
        left_fill = (71, 85, 105, 255)
        outline_color = (15, 23, 42, 255)
        outline_width = 3

        draw.polygon(top_pts, fill=top_fill)
        draw.polygon(left_pts, fill=left_fill)
        draw.polygon(right_pts, fill=right_fill)
        draw.polygon(top_pts, outline=outline_color, width=outline_width)
        draw.polygon(left_pts, outline=outline_color, width=outline_width)
        draw.polygon(right_pts, outline=outline_color, width=outline_width)

    img_resized = img.resize((400, 300), Image.Resampling.LANCZOS)
    output = io.BytesIO()
    img_resized.save(output, format="PNG")
    return output.getvalue()

def generate_thermometer_image(temp: float) -> bytes:
    width, height = 300, 800
    img = Image.new("RGBA", (width, height), (30, 41, 59, 0))
    draw = ImageDraw.Draw(img)
    
    tube_w = 30
    bulb_r = 55
    center_x = width // 2
    bulb_y = height - 120
    tube_top = 100
    tube_bottom = bulb_y - 20
    
    draw.ellipse([center_x - bulb_r, bulb_y - bulb_r, center_x + bulb_r, bulb_y + bulb_r], fill=(15, 23, 42, 255), outline=(148, 163, 184, 255), width=6)
    draw.rectangle([center_x - tube_w, tube_top, center_x + tube_w, tube_bottom], fill=(15, 23, 42, 255), outline=(148, 163, 184, 255), width=6)
    draw.ellipse([center_x - tube_w, tube_top - tube_w, center_x + tube_w, tube_top + tube_w], fill=(15, 23, 42, 255), outline=(148, 163, 184, 255), width=6)
    draw.rectangle([center_x - tube_w + 3, tube_top + 1, center_x + tube_w - 3, tube_bottom - 1], fill=(15, 23, 42, 255))
    draw.ellipse([center_x - tube_w + 3, tube_top - tube_w + 3, center_x + tube_w - 3, tube_top + tube_w - 3], fill=(15, 23, 42, 255))
    draw.rectangle([center_x - tube_w + 6, tube_bottom - 10, center_x + tube_w - 6, bulb_y - 10], fill=(15, 23, 42, 255))

    min_temp, max_temp = -20, 50
    temp_range = max_temp - min_temp
    pixel_range = tube_bottom - tube_top - 40
    
    def temp_to_y(t):
        pct = (t - min_temp) / temp_range
        return tube_bottom - 20 - pct * pixel_range

    font = get_font(26)
    for t in range(min_temp, max_temp + 1, 10):
        ty = temp_to_y(t)
        draw.line([center_x + tube_w, ty, center_x + tube_w + 20, ty], fill=(203, 213, 225, 200), width=3)
        draw.text((center_x + tube_w + 30, ty - 15), f"{t}°C", fill=(248, 250, 252, 255), font=font)

    in_bulb_r = bulb_r - 8
    draw.ellipse([center_x - in_bulb_r, bulb_y - in_bulb_r, center_x + in_bulb_r, bulb_y + in_bulb_r], fill=(239, 68, 68, 255))
    
    level_y = temp_to_y(temp)
    level_y = max(tube_top + 10, min(tube_bottom + 10, level_y))
    in_tube_w = tube_w - 8
    draw.rectangle([center_x - in_tube_w, level_y, center_x + in_tube_w, bulb_y], fill=(239, 68, 68, 255))
    draw.ellipse([center_x - 25, bulb_y - 25, center_x - 5, bulb_y - 5], fill=(255, 255, 255, 100))

    img_resized = img.resize((150, 400), Image.Resampling.LANCZOS)
    output = io.BytesIO()
    img_resized.save(output, format="PNG")
    return output.getvalue()
