---
name: motion-maps
description: Animações de mapas cinemáticos, retículas polares HUD, coordenadas e radares pulsantes em Python.
version: 1.0.0
---

# Mapas Cinemáticos e Retículas Cartográficas em Python

Este módulo ensina como renderizar animações de mapas e localizadores de coordenadas com estética técnica e científica sem depender de navegadores ou serviços externos.

## 1. Retícula Polar Cartográfica HUD

Em vez de renderizar mapas estáticos densos, desenhe uma janela cartográfica escura com grade polar analítica (latitude e longitude) e rótulos de coordenadas:

```python
from PIL import ImageDraw
from typing import Tuple

def draw_hud_map_grid(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    width: int,
    height: int,
    vis: float,
    accent_rgba: Tuple[int, int, int, int],
):
    # Fundo azul-escuro cartográfico
    map_bg = (6, 12, 22, int(200 * vis))
    draw.rectangle([x, y, x + width, y + height], fill=map_bg, outline=accent_rgba, width=1)

    # Linhas de latitude
    grid_alpha = int(40 * vis)
    grid_color = (accent_rgba[0], accent_rgba[1], accent_rgba[2], grid_alpha)
    
    for gy in range(y + 16, y + height, 24):
        draw.line([(x, gy), (x + width, gy)], fill=grid_color, width=1)
        
    # Linhas de longitude
    for gx in range(x + 28, x + width, 40):
        draw.line([(gx, y), (gx, y + height)], fill=grid_color, width=1)
```

## 2. Alvo de Coordenadas e Anéis de Radar Pulsantes

Para conferir dinamismo e atrair a atenção do espectador para uma coordenada geográfica ou orbital específica:

```python
import numpy as np

def draw_pulsing_radar_target(
    draw: ImageDraw.ImageDraw,
    target_x: int,
    target_y: int,
    t: float,
    vis: float,
    accent_rgba: Tuple[int, int, int, int],
    scale_f: float = 1.0,
):
    # Pulso cíclico contínuo (2.5 ciclos por segundo)
    pulse_phase = (t * 2.5) % 1.0
    r1 = max(4, int(24 * pulse_phase * scale_f))
    r1_alpha = int(220 * (1.0 - pulse_phase) * vis)
    
    # Anel de radar que se expande e desvanece
    draw.ellipse(
        [target_x - r1, target_y - r1, target_x + r1, target_y + r1],
        outline=(accent_rgba[0], accent_rgba[1], accent_rgba[2], r1_alpha),
        width=2,
    )
    
    # Ponto central brilhante fixo
    draw.ellipse(
        [target_x - 4, target_y - 4, target_x + 4, target_y + 4],
        fill=(255, 255, 255, int(255 * vis)),
    )
```
