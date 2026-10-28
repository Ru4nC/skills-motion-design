---
name: motion-notebooks
description: Prototipagem, renderização e inspeção de animações com canal alfa em Google Colab e Jupyter Notebooks.
version: 1.0.0
---

# Motion Design em Google Colab e Jupyter Notebooks

Este documento ensina como criar, testar, prototipar e renderizar animações de Motion Design diretamente em notebooks do Google (Google Colab, Kaggle ou Jupyter local), permitindo inspeção visual instantânea de quadros estáticos e validação de transparência alfa real em células.

## 1. Configuração Headless em Uma Célula

Em ambientes Colab/Jupyter na nuvem (sem interface gráfica X11 instalada), execute o seguinte bloco de configuração inicial:

```python
# Célula 1: Instalação de dependências do sistema e fontes
!apt-get update -qq && apt-get install -y -qq ffmpeg fonts-liberation fonts-dejavu-core
!pip install -q pillow numpy

import os
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import IPython.display as ipd
```

## 2. Inspeção Rápida de Quadro Estático (Frame Check)

Para testar o layout de uma arte ou o posicionamento anti-colisão em um segundo específico $t$:

```python
# Célula 2: Renderização de quadro estático
def preview_frame(render_fn, t_sec=1.5, width=960, height=540):
    """
    Renderiza um quadro reduzido em memória e exibe na célula do notebook.
    """
    img = render_fn(t=t_sec, duration=4.0, width=width, height=height)
    return ipd.display(img)

# Exemplo de chamada:
# preview_frame(meu_motor_render, t_sec=1.2)
```

## 3. Player com Fundo Quadriculado para Canal Alfa (`InlineAlphaPreview`)

Ao renderizar um vídeo transparente `.webm` (VP9 `yuva420p`), um reprodutor comum de vídeo pode exibir fundo preto opaco. Para comprovar visualmente que o canal alfa é real, utilize o widget HTML com padrão xadrez (*checkerboard pattern* via CSS):

```python
def display_alpha_webm_inline(video_path: str, width: int = 640):
    """
    Exibe o vídeo .webm dentro da célula sob um fundo xadrez dinâmico,
    atestando a transparência real do canal alfa.
    """
    import base64
    with open(video_path, "rb") as f:
        video_b64 = base64.b64encode(f.read()).decode("utf-8")

    html_code = f"""
    <div style="
        display: inline-block;
        padding: 8px;
        border-radius: 8px;
        background: repeating-conic-gradient(#333 0% 25%, #1a1a1a 0% 50%) 50% / 20px 20px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.4);
    ">
        <video width="{width}" autoplay loop muted playsinline controls>
            <source src="data:video/webm;base64,{video_b64}" type="video/webm">
            Seu navegador não suporta reprodução de WebM.
        </video>
    </div>
    """
    return ipd.display(ipd.HTML(html_code))
```

## 4. Exportação e Download para Máquina Local ou Google Drive

Para baixar o vídeo gerado na máquina local a partir do Google Colab:

```python
# Célula 4: Download direto no Colab
try:
    from google.colab import files
    files.download("output_overlay.webm")
except ImportError:
    print("Salvo localmente em: output_overlay.webm")
```

Para persistência direta em lote no Google Drive:
```python
from google.colab import drive
drive.mount('/content/drive')
# shutil.copy("output_overlay.webm", "/content/drive/MyDrive/MotionGraphics/")
```
