# Sombras Suaves, Cartões Cinemáticos e Grade Analítica em Python

Esta técnica ensina como desenhar cartões de alta legibilidade com sombras projetadas suaves (*soft drop shadows*) de 5 camadas, contornos com brilho (*neon glow*) e grades técnicas analíticas em Pillow.

## Sombra Projetada Suave de 5 Camadas (Soft Drop Shadow)

Para destacar cartões semânticos contra qualquer fundo de vídeo (inclusive cenas claras ou explosões estelares), sintetize 5 retângulos concêntricos com expansão gradativa de raio e decaimento exponencial de opacidade:

```python
from typing import Tuple
from PIL import ImageDraw

def draw_soft_shadow(
    draw: ImageDraw.ImageDraw,
    x0: int,
    y0: int,
    card_w: int,
    card_h: int,
    vis: float = 1.0,
    layers: int = 5,
    blur_spread: int = 4,
):
    """
    Desenha uma sombra difusa de 5 camadas concêntricas atrás do card.
    """
    for i in range(layers, 0, -1):
        pad = i * blur_spread
        # Opacidade decai conforme afasta do centro
        shadow_alpha = int((18 / (i * 0.8)) * vis)
        shadow_color = (0, 0, 0, shadow_alpha)
        draw.rounded_rectangle(
            [x0 - pad, y0 - pad + (i * 2), x0 + card_w + pad, y0 + card_h + pad + (i * 2)],
            radius=max(6, 14 + pad // 2),
            fill=shadow_color,
        )
```

## Painel com Neon Glow e Borda Animada (Stroke Draw)

Nos primeiros instantes da animação ($t < 0.35s$), o perímetro do cartão é desenhado progressivamente (*stroke draw*) antes de revelar o preenchimento:

```python
def draw_cinematic_card_panel(
    draw: ImageDraw.ImageDraw,
    x0: int,
    y0: int,
    card_w: int,
    card_h: int,
    panel_bg: Tuple[int, int, int, int],
    accent_rgba: Tuple[int, int, int, int],
    vis: float,
    stroke_progress: float = 1.0,
    corner_radius: int = 12,
):
    # 1. Desenha a sombra projetada
    draw_soft_shadow(draw, x0, y0, card_w, card_h, vis=vis)

    # 2. Preenchimento do painel escuro
    draw.rounded_rectangle(
        [x0, y0, x0 + card_w, y0 + card_h],
        radius=corner_radius,
        fill=panel_bg,
    )

    # 3. Grade analítica técnica sutil no interior do card
    grid_alpha = int(14 * vis)
    for gx in range(x0 + 20, x0 + card_w, 36):
        draw.line([(gx, y0 + 10), (gx, y0 + card_h - 10)], fill=(accent_rgba[0], accent_rgba[1], accent_rgba[2], grid_alpha), width=1)

    # 4. Borda com contorno perimetral e neon glow
    if stroke_progress > 0.05:
        outline_alpha = int(accent_rgba[3] * min(1.0, stroke_progress))
        draw.rounded_rectangle(
            [x0, y0, x0 + card_w, y0 + card_h],
            radius=corner_radius,
            outline=(accent_rgba[0], accent_rgba[1], accent_rgba[2], outline_alpha),
            width=2,
        )
```
