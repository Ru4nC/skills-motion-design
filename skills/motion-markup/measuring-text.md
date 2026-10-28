# Medição de Texto, Bounding Boxes e Fontes em Python

Esta técnica aborda o carregamento seguro de fontes TrueType/OpenType de sistema, cálculo de dimensões milimétricas com `font.getbbox()` e prevenção de caracteres *tofu* (`□`) em UTF-8 no Pillow.

## Carregamento com Cadeia de Fallback Anti-Tofu

Para evitar que o Pillow recorra à fonte bitmap padrão de 10px em ambientes Linux/Docker, defina uma cadeia prioritária de fontes de sistema com suporte completo a caracteres latinos acentuados (`é`, `ã`, `ç`, `•`):

```python
import os
from PIL import ImageFont

FONT_CANDIDATES = [
    "/usr/share/fonts/google-droid-sans-fonts/DroidSans-Bold.ttf",
    "/usr/share/fonts/abattis-cantarell-fonts/Cantarell-Bold.otf",
    "/usr/share/fonts/adwaita-sans-fonts/AdwaitaSans-Regular.ttf",
    "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]

def load_system_font(size: int, custom_path: str = None) -> ImageFont.FreeTypeFont:
    if custom_path and os.path.exists(custom_path):
        try:
            return ImageFont.truetype(custom_path, size=size)
        except Exception:
            pass

    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size=size)
            except Exception:
                continue

    return ImageFont.load_default()
```

## Medição com `getbbox()`

Substitua chamadas legadas a `font.getsize()` (descontinuadas no Pillow moderno) pelo método `getbbox()`:

```python
def measure_text_dimensions(text: str, font) -> tuple[int, int]:
    """
    Retorna (largura, altura) exatas em pixels renderizados.
    """
    bbox = font.getbbox(text)
    # bbox retorna (left, top, right, bottom)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    return width, height
```

## Quebra Automática de Linha (Word Wrapping)

```python
def wrap_text_to_width(text: str, font, max_width_px: int) -> list[str]:
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        test_line = " ".join(current_line + [word])
        w, _ = measure_text_dimensions(test_line, font)
        if w <= max_width_px:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]

    if current_line:
        lines.append(" ".join(current_line))
    return lines
```
