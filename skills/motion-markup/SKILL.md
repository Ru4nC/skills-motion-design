---
name: motion-markup
description: Primitivas de renderização gráfica em memória (Pillow + NumPy), tipografia, efeitos visuais e animações matemáticas em Python.
version: 1.0.0
---

# Motion Markup e Primitivas Gráficas em Python

Este módulo fornece as regras e padrões de implementação para sintetizar elementos gráficos animados quadro a quadro diretamente em memória usando **Pillow (PIL)** e **NumPy**, sem depender de navegadores, DOM ou linguagens de estilo CSS.

## 1. Loop Fundamental de Renderização de Quadros

Toda animação em Python opera sobre uma função determinística que recebe o instante de tempo em segundos $t$, a duração total e os dados do elemento, retornando uma imagem `PIL.Image` em formato `RGBA`:

```python
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def render_frame_rgba(
    width: int,
    height: int,
    time_in_sec: float,
    total_duration: float,
    data: dict,
) -> Image.Image:
    # 1. Cria buffer transparente de fundo (alpha = 0)
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    
    # 2. Respeita 10% de Safe Area perimetral
    mx = int(width * 0.10)
    my = int(height * 0.10)
    
    # 3. Calcula curvas de entrada e saída
    t = max(0.0, min(total_duration, time_in_sec))
    enter_t = min(1.0, t / 0.45)
    enter_ease = 1.0 - pow(1.0 - enter_t, 3)  # cubic_out
    exit_t = min(1.0, max(0.0, (total_duration - t) / 0.40))
    exit_ease = 1.0 - pow(1.0 - exit_t, 3)
    vis = max(0.05, min(enter_ease, exit_ease))
    
    # 4. Renderiza elementos geométricos e textuais
    # ...
    return img
```

## 2. Técnicas e Efeitos Cinemáticos Disponíveis

Para consultar algoritmos e implementações detalhadas de cada técnica gráfica em Python puro, consulte os tópicos:

- [Marca-Texto Orgânico (Rough Notation)](./text-highlights.md): Polígonos senoidais que simulam caneta de grifo manual e carimbos.
- [Motion Blur Direcional](./motion-blur.md): Arrasto fracionado horizontal baseado na derivada da aceleração cúbica.
- [Visualização de Áudio e Ondas](./audio-visualization.md): Osciloscópio harmônico senoidal e displays de frequência em NumPy.
- [Timing, Easing e Roll-up](./timing.md): Interpolações `easeOutExpo` ($1 - 2^{-10t}$), desaceleração elástica e contadores numéricos progressivos.
- [Sombras e Cartões Cinemáticos](./cards-and-shadows.md): Soft drop shadow concêntrico de 5 camadas, neon glow perimetral e grade analítica técnica.
- [Medição de Texto e Fontes](./measuring-text.md): Cálculo milimétrico de caixas de texto com `font.getbbox()`, anti-aliasing e fontes de sistema sem caracteres *tofu*.
- [Transições e Transformações](./transitions.md): Efeitos de dissolvência alfa, deslizamentos e manipulação de canais de cor.
- [Efeitos e Filtros Vetoriais](./effects.md): Rotações, máscaras de corte em canal alfa e transformações afins com NumPy.
