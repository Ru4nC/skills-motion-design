# Motion Design Skills

Skills de Motion Graphics para agentes autônomos orientadas à arquitetura Python-First, com renderização determinística em memória (Pillow + NumPy) e composição de overlays com canal alfa via FFmpeg.

## Language

**MotionGraphicsEngine**:
Motor Python de síntese gráfica frame a frame que renderiza animações diretamente em memória (Pillow + NumPy) e transmite buffers rawvideo RGBA via pipe para o binário do FFmpeg.
_Avoid_: Renderizador Web, Puppeteer Engine, Browser Renderer

**VideoAssembler**:
Componente de montagem responsável pela composição de trilhas na timeline sobre o vídeo base via `filter_complex` do FFmpeg.
_Avoid_: Compositor React, Player Web, Timeline Browser

**Alpha WebM Overlay**:
Vídeo transparente `.webm` codificado com VP9 (`libvpx-vp9`) em formato de pixel `yuva420p` com canal alfa real (`-auto-alt-ref 0`).
_Avoid_: PNG Sequence, Apple ProRes 4444, GIF transparente, Vídeo com croma-key verde

**PTS Shift**:
Deslocamento do Presentation Time Stamp (`setpts=PTS-STARTPTS+{t_start}/TB`) aplicado no `filter_complex` para sincronizar temporalmente overlays curtos e impedir congelamento no último quadro.
_Avoid_: Delay estático, Freeze frame manual, Trim offset

**Rawvideo RGBA Buffer**:
Buffer contínuo em memória contendo os bytes brutos dos pixels RGBA de cada quadro, transmitido diretamente ao stdin do subprocesso FFmpeg sem persistência temporária em disco.
_Avoid_: Frames intermediários em PNG, Sequência de imagens em disco, Tempfile buffer

**RoughNotation**:
Técnica de realce visual em Python que sintetiza polígonos orgânicos com perturbação senoidal (`np.sin`/`np.cos`) para simular marca-texto manual imperfeito em documentos e dossiês.
_Avoid_: Highlight retangular simples, CSS text-decoration

**EaseOutExpo**:
Função de interpolação não-linear ($1 - 2^{-10t}$) que proporciona aceleração inicial enérgica e desaceleração suave, aplicada a contadores numéricos e barras de escala.
_Avoid_: Linear interpolation, CSS cubic-bezier genérico

**DirectionalMotionBlur**:
Efeito de arrasto fracionado aplicado durante a aceleração inicial de elementos gráficos, com deslocamento proporcional à derivada da função de interpolação cúbica.
_Avoid_: Gaussian blur global, Motion blur de pós-produção

**Safe Area**:
Margem perimetral obrigatória (mínimo de 10% nas quatro bordas) para blindagem anti-colisão com legendas e controles de players de vídeo.
_Avoid_: Full bleed, Canvas livre

**InlineAlphaPreview**:
Exibição em notebooks (Colab/Jupyter) ou navegador de vídeos `.webm` sobre fundo quadriculado (*checkerboard*) via HTML5/CSS para validar a transparência real do canal alfa.
_Avoid_: Preview opaco, Fundo preto fixo
