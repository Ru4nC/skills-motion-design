# Transições de Opacidade e Transformações Matriciais em Python

Esta técnica aborda transições de corte, fades graduais com canal alfa e deslizamentos direcionais utilizando operações matriciais do **NumPy** e métodos de manipulação de canais do **Pillow**.

## Crossfade de Opacidade com Canal Alfa

Para transicionar elementos com precisão matemática em formato RGBA:

```python
from PIL import Image
import numpy as np

def apply_alpha_fade(img: Image.Image, opacity: float) -> Image.Image:
    """
    Multiplica o canal alfa existente pelo fator de opacidade (0.0 a 1.0).
    """
    arr = np.array(img, dtype=np.float32)
    alpha_scale = max(0.0, min(1.0, float(opacity)))
    arr[:, :, 3] = arr[:, :, 3] * alpha_scale
    return Image.fromarray(arr.astype(np.uint8), mode="RGBA")
```

## Wipe de Cortina Horizontal com NumPy

```python
def apply_horizontal_wipe(img: Image.Image, progress: float) -> Image.Image:
    """
    Revela a imagem da esquerda para a direita de acordo com o progresso (0.0 a 1.0).
    """
    arr = np.array(img)
    w = img.width
    cutoff = int(w * max(0.0, min(1.0, progress)))
    
    # Zera o canal alfa além do ponto de corte
    arr[:, cutoff:, 3] = 0
    return Image.fromarray(arr, mode="RGBA")
```
