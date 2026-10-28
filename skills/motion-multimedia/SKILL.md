---
name: motion-multimedia
description: Extração de metadados de vídeo e áudio (dimensões, fps, duração, canais) usando FFprobe e Python puro.
version: 1.0.0
---

# Inspeção Multimídia e Metadados com FFprobe em Python

Este documento fornece funções utilitárias em Python puro para inspecionar arquivos de mídia (áudio e vídeo) utilizando o binário `ffprobe`, eliminando pacotes Node.js externos.

## 1. Inspeção de Dimensões e Taxa de Quadros (FPS)

```python
import json
import subprocess
from typing import Tuple

def get_video_properties(video_path: str, ffprobe_bin: str = "ffprobe") -> Tuple[int, int, float, float]:
    """
    Retorna (largura, altura, fps, duracao_segundos) de um arquivo de vídeo.
    """
    cmd = [
        ffprobe_bin,
        "-v", "quiet",
        "-print_format", "json",
        "-show_streams",
        "-show_format",
        video_path,
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    data = json.loads(res.stdout)

    video_stream = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
    width = int(video_stream.get("width", 1920))
    height = int(video_stream.get("height", 1080))
    
    # Converte r_frame_rate fracionário (ex.: '30/1' ou '60000/1001')
    fps_raw = video_stream.get("r_frame_rate", "30/1")
    if "/" in fps_raw:
        num, den = fps_raw.split("/")
        fps = float(num) / max(1.0, float(den))
    else:
        fps = float(fps_raw)

    duration = float(data.get("format", {}).get("duration", 0.0))
    return width, height, fps, duration
```

## 2. Inspeção Precisa de Duração de Áudio

```python
def get_audio_duration(audio_path: str, ffprobe_bin: str = "ffprobe") -> float:
    """
    Retorna a duração exata de um arquivo de áudio em segundos.
    """
    cmd = [
        ffprobe_bin,
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path,
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())
```
