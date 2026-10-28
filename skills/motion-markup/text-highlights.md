# Marca-Texto Orgânico e Grifos Manuais (Rough Notation em Python)

Esta técnica ensina como desenhar anotações e grifos de marca-texto dinâmicos (*highlights*) com imperfeições orgânicas sobre palavras ou frases em documentos e dossiês diretamente em Python.

## Princípio Matemático

Em vez de desenhar um retângulo estático e artificial, a borda do grifo é sintetizada como um polígono fechado cujas bordas superior e inferior sofrem perturbações senoidais e cossenoidais defasadas calculadas com **NumPy**:

$$y_{top}(i) = y_0 + \sin(i \cdot 0.8) \cdot A$$
$$y_{bottom}(i) = y_0 + h + \cos(i \cdot 0.7) \cdot A$$

Onde $A$ é a amplitude da imperfeição (geralmente $2.0 \times \text{scale\_factor}$) e o comprimento do grifo é animado progressivamente pela curva de avanço temporal do elemento.

## Implementação em Python (Pillow + NumPy)

```python
from typing import Tuple
from PIL import ImageDraw
import numpy as np

def draw_rough_highlight(
    draw: ImageDraw.ImageDraw,
    x0: int,
    y0: int,
    max_width: int,
    height: int,
    progress: float,
    color_rgba: Tuple[int, int, int, int],
    scale_f: float = 1.0,
):
    """
    Desenha uma faixa de marca-texto orgânica com bordas imperfeitas.
    progress: float entre 0.0 e 1.0
    color_rgba: ex: (245, 158, 11, 90) para âmbar translúcido
    """
    curr_w = int(max_width * max(0.0, min(1.0, progress)))
    if curr_w < 12:
        return

    steps = max(8, curr_w // 16)
    poly_pts = []

    # 1. Borda superior com perturbação senoidal
    for i in range(steps + 1):
        px = x0 + int(i * (curr_w / steps))
        py = y0 + int(np.sin(i * 0.8) * 2.5 * scale_f)
        poly_pts.append((px, py))

    # 2. Borda inferior retornando com perturbação cossenoidal
    for i in range(steps, -1, -1):
        px = x0 + int(i * (curr_w / steps))
        py = y0 + height + int(np.cos(i * 0.7) * 2.0 * scale_f)
        poly_pts.append((px, py))

    # 3. Preenche o polígono orgânico translúcido atrás do texto
    draw.polygon(poly_pts, fill=color_rgba)
```

## Carimbo Documental Desclassificado

Para complementar documentos e dossiês de estilo investigativo, desenhe carimbos com ângulo sutil e borda de caixa de advertência:

```python
def draw_classified_stamp(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    text: str,
    font,
    color_rgba: Tuple[int, int, int, int] = (239, 68, 68, 200),
    scale_f: float = 1.0,
):
    stamp_w = int(180 * scale_f)
    stamp_h = int(32 * scale_f)
    draw.rectangle([x, y, x + stamp_w, y + stamp_h], outline=color_rgba, width=2)
    draw.text((x + int(12 * scale_f), y + int(4 * scale_f)), text, fill=color_rgba, font=font)
```
