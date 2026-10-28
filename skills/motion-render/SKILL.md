---
name: motion-render
description: Renderização em memória e streaming contínuo para FFmpeg gerando vídeos transparentes (.webm VP9 yuva420p) e stills.
version: 1.0.0
---

# Renderização em Memória e Streaming FFmpeg

Este documento fornece as diretrizes e códigos de referência para exportação de animações gráficas de alta performance sem gravação de arquivos temporários em disco, utilizando o binário do FFmpeg através de pipes padrão (`stdin`).

## 1. Streaming Direto via Pipe Stdin

Em vez de gravar milhares de arquivos PNG intermediários em disco (o que consome I/O, gera concorrência de disco e desacelera o pipeline), os bytes brutos (`rawvideo`) de cada quadro gerado pelo Pillow são enviados diretamente para a entrada padrão do processo FFmpeg.

A velocidade típica dessa abordagem é de aproximadamente **1.5s por clipe animado de 4 segundos**.

### Implementação de Referência em Python

```python
import subprocess
import numpy as np
from PIL import Image

def render_animation_to_webm(
    output_path: str,
    render_frame_fn,
    width: int = 1920,
    height: int = 1080,
    fps: int = 30,
    duration_sec: float = 4.0,
    ffmpeg_bin: str = "ffmpeg",
) -> str:
    total_frames = int(round(duration_sec * fps))

    # Comando FFmpeg otimizado para canal alfa real e alta performance
    cmd = [
        ffmpeg_bin,
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{width}x{height}",
        "-pix_fmt", "rgba",
        "-r", str(fps),
        "-i", "pipe:0",
        "-c:v", "libvpx-vp9",
        "-pix_fmt", "yuva420p",
        "-auto-alt-ref", "0",
        "-b:v", "0",
        "-crf", "28",
        "-deadline", "realtime",
        "-cpu-used", "8",
        "-an",
        output_path,
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        for f in range(total_frames):
            t = f / float(fps)
            frame_img = render_frame_fn(t=t, duration=duration_sec, width=width, height=height)
            
            # Converte a imagem PIL diretamente em buffer de bytes RGBA
            proc.stdin.write(frame_img.tobytes("raw", "RGBA"))
            
        proc.stdin.close()
        proc.wait()
    except Exception as e:
        proc.kill()
        raise RuntimeError(f"Erro durante renderização de motion: {e}")

    return output_path
```

## 2. Requisitos de Canal Alfa Real (VP9 yuva420p)

Para que o clipe `.webm` se sobreponha perfeitamente sobre a trilha base sem gerar artefatos de fundo preto:
- **Codec**: `libvpx-vp9`
- **Formato de Pixel**: `yuva420p` (o `a` designa o plano de canal alfa real de 8 bits).
- **Flag Obrigatória**: `-auto-alt-ref 0`. Esta flag impede que o codec VP9 gere quadros de referência alternativos ocultos que corrompem a interpretação de transparência em reprodutores e filtros de composição.

### Alternativa para Pós-Produção (Apple ProRes 4444)
Se o clipe precisar ser entregue para suítes de edição externas (DaVinci Resolve / Premiere Pro):
```bash
ffmpeg -f rawvideo -pix_fmt rgba -s 1920x1080 -r 30 -i pipe:0 \
  -c:v prores_ks -profile:v 4 -pix_fmt yuva444p10le output.mov
```

## 3. Renderização Determinística de Stills (Inspeção de Frames)

Para capturar um único quadro representativo (ex.: $t = 1.5s$) com transparência em disco para QA ou preview rápido:

```python
def export_still_frame(
    output_png_path: str,
    render_frame_fn,
    timestamp: float = 1.5,
    width: int = 1920,
    height: int = 1080,
) -> str:
    frame_img = render_frame_fn(t=timestamp, duration=4.0, width=width, height=height)
    frame_img.save(output_png_path, format="PNG")
    return output_png_path
```
