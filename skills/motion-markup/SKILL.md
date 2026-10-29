---
name: motion-markup
description: Primitivas de renderização gráfica em memória (Pillow + NumPy), tipografia, efeitos visuais e animações matemáticas em Python.
version: 1.1.0
---

# Motion Markup e Primitivas Gráficas em Python

Este módulo fornece as regras e padrões de implementação para sintetizar elementos gráficos animados quadro a quadro diretamente em memória usando **Pillow (PIL)** e **NumPy**, sem depender de navegadores, DOM ou linguagens de estilo CSS.

O motor atende perfeitamente a dois tipos de animação:
1. **Cenas Full-Screen (100% Preenchidas)**: Infográficos completos de tela inteira, vinhetas, diagramas conceituais com gradientes escuros e fundos cinemáticos.
2. **Overlays com Canal Alfa (Camadas Transparentes)**: Elementos flutuantes, cards de telemetria e legendas sobrepostos a filmagens.

---

## 1. Inicialização do Buffer de Quadro

### Modo A: Cena 100% Preenchida (Full-Screen) com Gradiente Procedural
Para cenas completas, sintetize um gradiente cinemático contínuo com **NumPy** para máxima riqueza visual:

```python
from PIL import Image, ImageDraw
import numpy as np

def create_fullscreen_gradient_frame(
    width: int,
    height: int,
    color_top=(17, 24, 39, 255),       # Azul escuro espacial
    color_bottom=(10, 11, 14, 255),    # Obsidian profundo
) -> Image.Image:
    """Gera um fundo cinemático 100% preenchido sem canal alfa em milissegundos."""
    t_vals = np.linspace(0, 1, height)[:, None]
    r = (color_top[0] * (1 - t_vals) + color_bottom[0] * t_vals).astype(np.uint8)
    g = (color_top[1] * (1 - t_vals) + color_bottom[1] * t_vals).astype(np.uint8)
    b = (color_top[2] * (1 - t_vals) + color_bottom[2] * t_vals).astype(np.uint8)
    a = np.full((height, 1), 255, dtype=np.uint8)
    
    col = np.concatenate([r, g, b, a], axis=1)
    arr = np.repeat(col[:, None, :], width, axis=1)
    return Image.fromarray(arr, mode="RGBA")
```

### Modo B: Overlay Transparente (Canal Alfa = 0)
Para elementos flutuantes sobrepostos ao vídeo base:

```python
def create_transparent_overlay_frame(width: int, height: int) -> Image.Image:
    """Gera um buffer totalmente transparente (alpha = 0)."""
    return Image.new("RGBA", (width, height), (0, 0, 0, 0))
```

---

## 2. Loop de Renderização Quadro a Quadro

```python
def render_frame_rgba(
    width: int,
    height: int,
    time_in_sec: float,
    total_duration: float,
    data: dict,
    fullscreen: bool = True,
) -> Image.Image:
    # 1. Inicializa o fundo correspondente (100% preenchido ou transparente)
    img = create_fullscreen_gradient_frame(width, height) if fullscreen else create_transparent_overlay_frame(width, height)
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
    
    # 4. Renderiza elementos geométricos, infográficos e textuais
    # ...
    return img
```

---

## 3. Técnicas e Efeitos Cinemáticos Disponíveis

Para consultar algoritmos e implementações detalhadas de cada técnica gráfica em Python puro, consulte os tópicos:

- [Marca-Texto Orgânico (Rough Notation)](./text-highlights.md): Polígonos senoidais que simulam caneta de grifo manual e carimbos.
- [Motion Blur Direcional](./motion-blur.md): Arrasto fracionado horizontal baseado na derivada da aceleração cúbica.
- [Visualização de Áudio e Ondas](./audio-visualization.md): Osciloscópio harmônico senoidal e displays de frequência em NumPy.
- [Timing, Easing e Roll-up](./timing.md): Interpolações `easeOutExpo` ($1 - 2^{-10t}$), desaceleração elástica e contadores numéricos progressivos.
- [Sombras e Cartões Cinemáticos](./cards-and-shadows.md): Soft drop shadow concêntrico de 5 camadas, neon glow perimetral e grade analítica técnica.
- [Medição de Texto e Fontes](./measuring-text.md): Cálculo milimétrico de caixas de texto com `font.getbbox()`, anti-aliasing e fontes de sistema sem caracteres *tofu*.
- [Transições e Transformações](./transitions.md): Efeitos de dissolvência alfa, deslizamentos e manipulação de canais de cor.
- [Efeitos e Filtros Vetoriais](./effects.md): Rotações, máscaras de corte em canal alfa e transformações afins com NumPy.
