#!/usr/bin/env python3
"""
Gera os ativos visuais (GIFs animados e stills) para demonstração no README.md e no Showcase Notebook.
Executável via Python com Pillow + NumPy + FFmpeg.
"""

import os
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parent.parent
DEMO_DIR = REPO_ROOT / "assets" / "demo"
DEMO_DIR.mkdir(parents=True, exist_ok=True)


def load_font(size: int):
    candidates = [
        "/usr/share/fonts/google-droid-sans-fonts/DroidSans-Bold.ttf",
        "/usr/share/fonts/abattis-cantarell-fonts/Cantarell-Bold.otf",
        "/usr/share/fonts/adwaita-sans-fonts/AdwaitaSans-Regular.ttf",
        "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size=size)
            except Exception:
                continue
    return ImageFont.load_default()


def render_fullscreen_explainer_frame(t: float, dur: float, w: int, h: int) -> Image.Image:
    # 1. Gradiente de tela cheia
    t_vals = np.linspace(0, 1, h)[:, None]
    r = (15 * (1 - t_vals) + 8 * t_vals).astype(np.uint8)
    g = (22 * (1 - t_vals) + 10 * t_vals).astype(np.uint8)
    b = (36 * (1 - t_vals) + 14 * t_vals).astype(np.uint8)
    a = np.full((h, 1), 255, dtype=np.uint8)
    arr = np.repeat(np.concatenate([r, g, b, a], axis=1)[:, None, :], w, axis=1)
    img = Image.fromarray(arr, mode="RGBA")
    draw = ImageDraw.Draw(img, "RGBA")

    # Easing
    enter_t = min(1.0, t / 0.5)
    ease = 1.0 - pow(1.0 - enter_t, 3)
    p_roll = min(1.0, max(0.0, t / (dur * 0.7)))
    ease_roll = 1.0 if p_roll >= 0.999 else (1.0 - pow(2.0, -10.0 * p_roll))

    font_title = load_font(int(22 * (w / 720.0)))
    font_val = load_font(int(36 * (w / 720.0)))
    font_sub = load_font(int(14 * (w / 720.0)))

    # Grade técnica analítica
    for gx in range(40, w, 60):
        draw.line([(gx, 30), (gx, h - 30)], fill=(30, 42, 60, 80), width=1)

    # Card central com sombra
    card_w = int(w * 0.75 * ease)
    card_h = int(h * 0.58)
    x0 = (w - int(w * 0.75)) // 2
    y0 = int(h * 0.22)

    if card_w > 20:
        draw.rounded_rectangle([x0, y0, x0 + card_w, y0 + card_h], radius=10, fill=(17, 24, 39, 230), outline=(245, 158, 11, int(200 * ease)), width=2)
        
        # Conteúdo
        curr_km = int(384400 * ease_roll)
        draw.text((x0 + 24, y0 + 20), "TELEMETRIA DE MISSÃO ORBITAL", fill=(245, 158, 11, int(255 * ease)), font=font_title)
        draw.text((x0 + 24, y0 + 60), f"{curr_km:,} KM".replace(",", "."), fill=(248, 250, 252, int(255 * ease)), font=font_val)
        draw.text((x0 + 24, y0 + 120), "APOGEU // TRAJETÓRIA TRANSLUNAR CONFIRMADA", fill=(148, 163, 184, int(230 * ease)), font=font_sub)

        # Barra de escala
        bar_w = int((card_w - 48) * ease_roll)
        if bar_w > 4:
            draw.rectangle([x0 + 24, y0 + 150, x0 + 24 + bar_w, y0 + 162], fill=(6, 182, 212, 240))

    return img


def render_dossier_frame(t: float, dur: float, w: int, h: int) -> Image.Image:
    # Fundo xadrez sutil para destacar a janela documental
    img = Image.new("RGBA", (w, h), (12, 14, 18, 255))
    draw = ImageDraw.Draw(img, "RGBA")

    enter_t = min(1.0, t / 0.45)
    ease = 1.0 - pow(1.0 - enter_t, 3)
    p_hl = min(1.0, max(0.0, (t - 0.2) / 0.8))
    ease_hl = 1.0 if p_hl >= 0.999 else (1.0 - pow(2.0, -10.0 * p_hl))

    font_badge = load_font(int(14 * (w / 720.0)))
    font_quote = load_font(int(20 * (w / 720.0)))
    font_stamp = load_font(int(14 * (w / 720.0)))

    card_w = int(w * 0.85)
    card_h = int(h * 0.65)
    x0 = (w - card_w) // 2
    y0 = (h - card_h) // 2

    # Card estilo dossiê escuro
    draw.rounded_rectangle([x0, y0, x0 + card_w, y0 + card_h], radius=8, fill=(18, 20, 24, 245), outline=(245, 158, 11, int(180 * ease)), width=1)

    draw.text((x0 + 28, y0 + 24), "REGISTRO CLASSIFICADO // ARQUIVO 1977", fill=(245, 158, 11, int(255 * ease)), font=font_badge)

    # Carimbo vermelho
    stamp_x = x0 + card_w - 180
    stamp_y = y0 + 20
    draw.rectangle([stamp_x, stamp_y, stamp_x + 150, stamp_y + 28], outline=(239, 68, 68, int(220 * ease)), width=2)
    draw.text((stamp_x + 12, stamp_y + 6), "DESCLASSIFICADO", fill=(239, 68, 68, int(220 * ease)), font=font_stamp)

    # Grifo orgânico Rough Notation
    quote_text = "SINAL WOW! REGISTRADO EM 1420.456 MHz"
    text_y = y0 + 80
    hl_w = int(len(quote_text) * 11 * (w / 720.0) * ease_hl)

    if hl_w > 12:
        steps = max(8, hl_w // 14)
        poly = []
        for i in range(steps + 1):
            px = x0 + 26 + int(i * (hl_w / steps))
            py = text_y + int(np.sin(i * 0.8) * 2.5)
            poly.append((px, py))
        for i in range(steps, -1, -1):
            px = x0 + 26 + int(i * (hl_w / steps))
            py = text_y + 32 + int(np.cos(i * 0.7) * 2.0)
            poly.append((px, py))
        draw.polygon(poly, fill=(245, 158, 11, int(110 * ease)))

    draw.text((x0 + 28, text_y + 2), quote_text, fill=(248, 250, 252, int(255 * ease)), font=font_quote)
    draw.text((x0 + 28, y0 + 140), "ORIGEM: CONSTELAÇÃO DE SAGITÁRIO // DURAÇÃO: 72s", fill=(148, 163, 184, int(200 * ease)), font=font_badge)

    return img


def render_hud_overlay_frame(t: float, dur: float, w: int, h: int) -> Image.Image:
    # Fundo com padrão quadriculado xadrez para evidenciar o canal alfa
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    
    # Desenha fundo xadrez transparente simulado
    check_size = 20
    for cy in range(0, h, check_size):
        for cx in range(0, w, check_size):
            color = (32, 32, 36, 255) if ((cx // check_size) + (cy // check_size)) % 2 == 0 else (18, 18, 22, 255)
            img.paste(color, [cx, cy, cx + check_size, cy + check_size])

    draw = ImageDraw.Draw(img, "RGBA")

    # Card HUD Translúcido sobre o xadrez
    enter_t = min(1.0, t / 0.45)
    ease = 1.0 - pow(1.0 - enter_t, 3)

    font_badge = load_font(int(14 * (w / 720.0)))
    font_val = load_font(int(22 * (w / 720.0)))

    card_w = int(w * 0.78)
    card_h = int(h * 0.60)
    x0 = (w - card_w) // 2
    y0 = (h - card_h) // 2

    # Card com canal alfa real sobre o xadrez
    panel_bg = (8, 14, 24, int(215 * ease))
    accent_cyan = (6, 182, 212, int(255 * ease))
    draw.rounded_rectangle([x0, y0, x0 + card_w, y0 + card_h], radius=10, fill=panel_bg, outline=accent_cyan, width=2)

    draw.text((x0 + 24, y0 + 18), "HUD ESPECTRAL // FREQUÊNCIA HARMONICA", fill=accent_cyan, font=font_badge)

    # Osciloscópio dinâmico
    osc_w = card_w - 48
    osc_h = 70
    center_y = y0 + 75
    pts = []
    num_samples = 60
    for i in range(num_samples + 1):
        rel_x = i / float(num_samples)
        px = x0 + 24 + int(rel_x * osc_w)
        env = np.sin(rel_x * np.pi)
        w1 = np.sin(rel_x * 14.0 + t * 5.0) * 18.0
        w2 = np.sin(rel_x * 28.0 - t * 8.0) * 9.0
        py = center_y + int((w1 + w2) * env * ease)
        pts.append((px, py))

    draw.line([(x0 + 24, center_y), (x0 + 24 + osc_w, center_y)], fill=(6, 182, 212, int(60 * ease)), width=1)
    for j in range(len(pts) - 1):
        draw.line([pts[j], pts[j + 1]], fill=accent_cyan, width=2)

    draw.text((x0 + 24, y0 + 130), "STATUS: SINAL MODULADO // CARGA: 100%", fill=(148, 163, 184, int(220 * ease)), font=font_badge)

    return img


def generate_gif(render_fn, output_path: str, w=640, h=360, fps=15, duration=2.5):
    frames = []
    total_frames = int(fps * duration)
    for i in range(total_frames):
        t = i / float(fps)
        img = render_fn(t, duration, w, h)
        frames.append(img.convert("RGB"))

    # Salva como GIF animado em loop
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / fps),
        loop=0,
        optimize=True,
    )
    print(f"Salvo: {output_path}")


if __name__ == "__main__":
    print("Gerando ativos visuais animados...")
    generate_gif(render_fullscreen_explainer_frame, str(DEMO_DIR / "fullscreen_explainer.gif"))
    generate_gif(render_dossier_frame, str(DEMO_DIR / "dossier_rough_notation.gif"))
    generate_gif(render_hud_overlay_frame, str(DEMO_DIR / "transparent_hud_overlay.gif"))
    print("Concluído!")
