---
name: motion-render
description: Renderização em memória e streaming contínuo para FFmpeg gerando cenas de tela cheia (.mp4 H.264) ou overlays transparentes (.webm VP9 yuva420p).
version: 1.1.0
---

# Renderização em Memória e Streaming FFmpeg

Este documento fornece as diretrizes e códigos de referência para exportação de animações gráficas de alta performance sem gravação de arquivos temporários em disco, utilizando o binário do FFmpeg através de pipes padrão (`stdin`).

O motor suporta dois modos fundamentais de entrega visual:
1. **Cenas de Tela Cheia 100% Preenchidas (Full-Screen Standalone Scenes)**: Telas completas (infográficos explicativos, diagramas conceituais, title cards, vinhetas de capítulo) exportadas diretamente como `.mp4` (H.264 `yuv420p`) para compor a trilha principal de vídeo.
2. **Overlays Transparentes com Canal Alfa (Alpha Layer Overlays)**: Elementos flutuantes (telemetria HUD, estatísticas, grifos e lower thirds) exportados como `.webm` (VP9 `yuva420p`) para sobreposição sobre b-roll ou filmagens reais.

---

## 1. Modo Full-Screen: Cenas 100% Preenchidas (.mp4 H.264)

Para animações que ocupam toda a tela (1920x1080 ou 1080x1920) com fundo sólido, gradientes procedurais ou infografia densa:

```python
import subprocess
from PIL import Image

def render_fullscreen_scene_to_mp4(
    output_path: str,
    render_frame_fn,
    width: int = 1920,
    height: int = 1080,
    fps: int = 30,
    duration_sec: float = 5.0,
    ffmpeg_bin: str = "ffmpeg",
) -> str:
    """
    Renderiza uma cena 100% preenchida diretamente como vídeo MP4 H.264 broadcast-quality.
    Velocidade: ~1.2s para 5 segundos de animação em 1080p.
    """
    total_frames = int(round(duration_sec * fps))

    cmd = [
        ffmpeg_bin,
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{width}x{height}",
        "-pix_fmt", "rgba",
        "-r", str(fps),
        "-i", "pipe:0",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-crf", "18",
        "-an",
        output_path,
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        for f in range(total_frames):
            t = f / float(fps)
            frame_img = render_frame_fn(t=t, duration=duration_sec, width=width, height=height)
            proc.stdin.write(frame_img.tobytes("raw", "RGBA"))
            
        proc.stdin.close()
        proc.wait()
    except Exception as e:
        proc.kill()
        raise RuntimeError(f"Erro na renderização full-screen: {e}")

    return output_path
```

---

## 2. Modo Overlay: Clipes Transparentes com Canal Alfa (.webm VP9)

Quando a animação precisa sobrepor um vídeo de fundo, utilizamos o codec VP9 com formato de pixel `yuva420p`:

```python
def render_transparent_overlay_to_webm(
    output_path: str,
    render_frame_fn,
    width: int = 1920,
    height: int = 1080,
    fps: int = 30,
    duration_sec: float = 4.0,
    ffmpeg_bin: str = "ffmpeg",
) -> str:
    """
    Renderiza um overlay com fundo transparente (canal alfa real) via pipe direto para o FFmpeg.
    """
    total_frames = int(round(duration_sec * fps))

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
            proc.stdin.write(frame_img.tobytes("raw", "RGBA"))
            
        proc.stdin.close()
        proc.wait()
    except Exception as e:
        proc.kill()
        raise RuntimeError(f"Erro na renderização transparente: {e}")

    return output_path
```

### Requisitos do Canal Alfa Real
- **Formato de Pixel**: `yuva420p` (o `a` designa o plano alfa de transparência).
- **Flag Obrigatória**: `-auto-alt-ref 0` (impede quadros de referência alternativos ocultos que corrompem o canal alfa).
- **Pós-Produção Externa**: Para DaVinci Resolve ou Premiere, substitua por Apple ProRes 4444 (`-c:v prores_ks -profile:v 4 -pix_fmt yuva444p10le output.mov`).

---

## 3. Renderização Determinística de Stills (Inspeção e Miniaturas)

Para capturar um único quadro representativo (ex.: $t = 1.5s$) tanto de uma cena cheia quanto de um overlay com transparência:

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
