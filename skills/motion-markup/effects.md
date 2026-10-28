# Efeitos e Máscaras Vetoriais em Python

Este documento aborda a criação de máscaras de corte, desfoque gaussiano controlado e transformações afins em canal alfa utilizando Pillow e NumPy.

## Máscara de Corte Circular (Vignette / Radar Mask)

```python
from PIL import Image, ImageDraw

def create_circular_mask(width: int, height: int, radius: int, center: tuple[int, int]) -> Image.Image:
    """
    Cria uma máscara em escala de cinza ('L') para corte circular.
    """
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    cx, cy = center
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=255)
    return mask
```

## Efeito de Brilho Perimetral (Neon Glow)

```python
from PIL import ImageFilter

def apply_glow_effect(img_rgba: Image.Image, glow_color: tuple, radius: int = 6) -> Image.Image:
    """
    Extrai o contorno alfa, aplica desfoque gaussiano e sobrepõe como camada de brilho.
    """
    alpha = img_rgba.split()[3]
    glow_mask = alpha.filter(ImageFilter.GaussianBlur(radius=radius))
    
    glow_layer = Image.new("RGBA", img_rgba.size, glow_color)
    glow_layer.putalpha(glow_mask)
    
    # Composição: brilho embaixo, elemento original por cima
    composite = Image.alpha_composite(glow_layer, img_rgba)
    return composite
```
