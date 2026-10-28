# Visualização de Áudio e Osciloscópios Harmônicos em Python

Esta técnica ensina como sintetizar gráficos de osciloscópio de frequência, ondas sonoras e telemetria analítica com visual científico de alta precisão utilizando NumPy e Pillow.

## Princípio Matemático

Um osciloscópio estético não necessita de FFT computacionalmente pesada para gráficos conceituais: ele pode ser sintetizado através da superposição de ondas harmônicas senoidais com frequências e fases moduladas no tempo $t$:

$$y(x, t) = y_{center} + \sum_{k=1}^{3} A_k \cdot \sin(f_k \cdot x + \omega_k \cdot t)$$

Onde:
- $A_k$ é a amplitude da harmônica $k$
- $f_k$ é a frequência espacial
- $\omega_k$ é a velocidade angular de oscilação temporal

## Implementação em Python com NumPy

```python
from typing import Tuple
from PIL import ImageDraw
import numpy as np

def draw_harmonic_waveform(
    draw: ImageDraw.ImageDraw,
    x0: int,
    y0: int,
    width: int,
    height: int,
    t: float,
    accent_rgba: Tuple[int, int, int, int] = (6, 182, 212, 255),
    scale_f: float = 1.0,
):
    """
    Desenha um osciloscópio cinemático verde/ciano com onda harmônica viva.
    """
    center_y = y0 + height // 2
    pts = []
    
    # Amostra pontos horizontalmente ao longo da janela do osciloscópio
    num_samples = max(40, width // 4)
    for i in range(num_samples + 1):
        rel_x = i / float(num_samples)
        px = x0 + int(rel_x * width)
        
        # Envelope de borda: atenua amplitude nas extremidades para encostar suave no eixo central
        envelope = np.sin(rel_x * np.pi)
        
        # Superposição harmônica
        w1 = np.sin(rel_x * 12.0 + t * 4.0) * 16.0
        w2 = np.sin(rel_x * 24.0 - t * 6.5) * 8.0
        w3 = np.cos(rel_x * 6.0 + t * 2.0) * 6.0
        
        total_amp = (w1 + w2 + w3) * envelope * scale_f
        py = center_y + int(total_amp)
        pts.append((px, py))

    # Desenha linha de fundo atenuada (eixo central)
    draw.line([(x0, center_y), (x0 + width, center_y)], fill=(accent_rgba[0], accent_rgba[1], accent_rgba[2], 50), width=1)

    # Desenha a curva do osciloscópio com espessura anti-aliased
    for j in range(len(pts) - 1):
        draw.line([pts[j], pts[j + 1]], fill=accent_rgba, width=max(2, int(2 * scale_f)))
```
