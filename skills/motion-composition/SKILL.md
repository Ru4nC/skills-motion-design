---
name: motion-composition
description: Composição de overlays na timeline via filter_complex do FFmpeg, ajuste de apresentação (PTS Shift) e sincronia temporal.
version: 1.0.0
---

# Composição de Linha do Tempo e Sincronia Temporal (PTS Shift)

Este módulo documenta a esteira de pós-composição em que os clipes de animação transparentes (`.webm` VP9 `yuva420p`) são sobrepostos cirurgicamente sobre a trilha base de vídeo através do filtro `filter_complex` do **FFmpeg**, garantindo sincronia temporal milimétrica e ausência de travamentos.

## 1. O Problema do Congelamento de Quadros (Por que o PTS Shift é Obrigatório)

Quando múltiplos clipes de vídeo são combinados no FFmpeg:
- Se você aplicar apenas o filtro `overlay=enable='between(t, t_start, t_end)'` em um clipe de overlay curto (ex.: 4 segundos) que deve aparecer aos $12.0s$ do vídeo:
  - O clipe de overlay começa a decodificar no tempo zero ($t = 0$).
  - Aos $4.0s$ ele atinge o final do arquivo (**EOF**).
  - Quando a timeline atinge $12.0s$ (o momento em que ele deveria ser exibido), o clipe já está no último frame congelado ou simplesmente exibe tela preta.

### A Fórmula Matemática do PTS Shift
Para que o clipe overlay permaneça inativo no tempo zero e inicie o primeiro quadro exatamente no segundo $t_{start}$:

$$\text{PTS}_{novo} = \text{PTS} - \text{STARTPTS} + \frac{t_{start}}{\text{TB}}$$

No FFmpeg:
```
[1:v]setpts=PTS-STARTPTS+12.00/TB[ov1];
[base][ov1]overlay=0:0:eof_action=pass:enable='between(t,12.00,16.00)'[v_out]
```

## 2. Construção Programática do Comando `filter_complex` em Python

Abaixo está o padrão arquitetural utilizado pelo montador de vídeo para encadear $N$ overlays sobre o vídeo base:

```python
from typing import List, Dict, Any

def build_overlay_filter_complex_cmd(
    base_video_path: str,
    overlays: List[Dict[str, Any]],
    output_video_path: str,
    ffmpeg_bin: str = "ffmpeg",
) -> List[str]:
    """
    Constrói a chamada de linha de comando do FFmpeg para estampar overlays na timeline.
    overlays: lista de dicts com {'path': str, 't_start': float, 't_end': float}
    """
    cmd = [ffmpeg_bin, "-y", "-i", base_video_path]
    
    # 1. Adiciona cada arquivo .webm como input individual
    for ov in overlays:
        cmd.extend(["-i", ov["path"]])
        
    filter_chains = []
    last_stream = "[0:v]"
    
    # 2. Constrói o grafo de filtros
    for idx, ov in enumerate(overlays, start=1):
        t_start = f"{ov['t_start']:.3f}"
        t_end = f"{ov['t_end']:.3f}"
        
        # Aplica o PTS Shift para deslocar o início do vídeo transparente
        pts_stream = f"[ov{idx}]"
        filter_chains.append(f"[{idx}:v]setpts=PTS-STARTPTS+{t_start}/TB{pts_stream}")
        
        # Faz o overlay sobre a trilha base acumulada
        next_stream = f"[v{idx}]"
        filter_chains.append(
            f"{last_stream}{pts_stream}overlay=0:0:eof_action=pass:enable='between(t,{t_start},{t_end})'{next_stream}"
        )
        last_stream = next_stream

    filter_complex_str = ";".join(filter_chains)
    
    cmd.extend([
        "-filter_complex", filter_complex_str,
        "-map", last_stream,
        "-map", "0:a?",
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "fast",
        "-c:a", "copy",
        output_video_path
    ])
    
    return cmd
```

## 3. Lead-in Temporal de Antecipação (-0.2s)

Ao calcular o `t_start` com base na posição da palavra-chave no roteiro ou no alinhamento de fala:

```python
def calculate_lead_in_start_time(keyword_audio_second: float) -> float:
    """
    Subtrai 200ms da fala para que a animação entre em movimento quando a palavra é ouvida.
    """
    return max(0.0, keyword_audio_second - 0.20)
```

## 4. Conformidade Acústica de SFX (EBU R128)

Qualquer pontuação de áudio (micro-woosh de entrada) associada à animação:
- Nunca deve ser mixada de forma intrusiva sobre a voz principal.
- Deve passar obrigatoriamente pela etapa final de masterização EBU R128 (`loudnorm=I=-14.0:TP=-1.5:LRA=7`), garantindo que o pico real interamostral final respeite `True Peak <= -1.0 dBTP`.
