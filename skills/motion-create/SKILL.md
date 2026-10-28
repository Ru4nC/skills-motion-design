---
name: motion-create
description: Scaffolding e estrutura recomendada para criação de novos módulos de Motion Design em Python.
version: 1.0.0
---

# Scaffolding de Módulos de Motion Design em Python

Este documento apresenta o template estrutural padronizado para criar um novo módulo de Motion Design ou um novo template de animação em Python.

## Estrutura Canônica de um Módulo

```python
"""
Módulo de Animação: MeuElementoAnimado
Responsável por renderizar infografias animadas determinísticas em memória.
"""

from typing import Dict, Any, Tuple
from PIL import Image, ImageDraw, ImageFont
import numpy as np

class CustomMotionTemplate:
    def __init__(self, width: int = 1920, height: int = 1080):
        self.width = width
        self.height = height

    def render_frame(
        self,
        t: float,
        duration: float,
        data: Dict[str, Any],
    ) -> Image.Image:
        """
        Gera um quadro individual no timestamp t (em segundos).
        """
        w, h = self.width, self.height
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img, "RGBA")

        # 1. Margens de segurança (10%)
        mx, my = int(w * 0.10), int(h * 0.10)

        # 2. Curvas de entrada e saída
        enter_t = min(1.0, t / 0.45)
        enter_ease = 1.0 - pow(1.0 - enter_t, 3)
        exit_t = min(1.0, max(0.0, (duration - t) / 0.40))
        exit_ease = 1.0 - pow(1.0 - exit_t, 3)
        vis = max(0.05, min(enter_ease, exit_ease))

        # 3. Desenho de elementos gráficos
        # ...

        return img
```
