# Python Motion Design: Arquitetura, Técnicas e Guia de Referência

Este documento é uma fonte de conhecimento unificada e estruturada sobre a suíte **Python Motion Design Agent Skills**, ideal para consulta técnica e processamento em ferramentas de análise como Google NotebookLM.

---

## 1. Visão Geral da Arquitetura

O ecossistema **Python Motion Design** foi concebido sob a premissa de eliminar dependências de navegadores headless (Chromium/Puppeteer), linguagens web e servidores complexos.

- **Linguagem**: Python 3.10+
- **Motor Gráfico**: Pillow (PIL) para rasterização de alta fidelidade e tipografia + NumPy para transformações matriciais, interpolações e ondas harmônicas.
- **Renderização**: 100% em memória, com streaming de quadros `rawvideo` no espaço de cores `RGBA` diretamente para a entrada padrão (`stdin`) do binário FFmpeg.
- **Velocidade**: ~1.2s a 1.5s por clipe de 4 segundos.
- **Determinismo**: Animações puramente matemáticas orientadas pelo tempo $t$, sem desvios de relógio do sistema ou dependência de rede.

---

## 2. Modos de Operação

### Modo A: Cenas Full-Screen (100% Preenchidas)
- **Formato**: `.mp4` codificado com `libx264` em espaço de cor `yuv420p` (`-preset fast -crf 18`).
- **Aplicações**: Infográficos explicativos completos, telas de capítulo, diagramas conceituais densos e vinhetas com fundos em gradientes procedurais contínuos.

### Modo B: Overlays Transparentes com Canal Alfa
- **Formato**: `.webm` codificado com `libvpx-vp9` em espaço de cor `yuva420p` com a flag obrigatória `-auto-alt-ref 0`.
- **Aplicações**: Telemetria flutuante, cartões HUD científicos, marcas de texto dinâmicas, lower thirds e contadores sobrepostos à filmagem base.
- **Sincronia Temporal (PTS Shift)**: Ajuste milimétrico de apresentação temporal via `filter_complex`:
  $$\text{PTS}_{novo} = \text{PTS} - \text{STARTPTS} + \frac{t_{start}}{\text{TB}}$$
  Impedindo que clipes curtos congelem no último quadro antes de sua janela de exibição.

---

## 3. Técnicas Visuais e Fórmulas Matemáticas

1. **Desaceleração Exponencial (EaseOutExpo)**:
   $$\text{prog} = 1.0 - 2^{-10 \cdot t}$$
   Utilizada em contadores numéricos (*roll-up*) e barras de progresso para arrancada inicial vigorosa e parada suave.
2. **Motion Blur Direcional**:
   $$v(t) \propto 3 \cdot (1 - \text{enter\_t})^2$$
   Aplica deslocamento horizontal proporcional à velocidade da curva cúbica durante a janela inicial de aceleração ($t < 0.35s$).
3. **Marca-Texto Orgânico (Rough Notation)**:
   Polígonos com bordas perturbadas senoidalmente:
   $$y_{top} = y_0 + \sin(i \cdot 0.8) \cdot A, \quad y_{bottom} = y_0 + h + \cos(i \cdot 0.7) \cdot A$$
4. **Osciloscópios Harmônicos**:
   Superposição de ondas senoidais multi-frequência moduladas no tempo $t$ com envelope de borda atenuado nas extremidades.
5. **Soft Drop Shadows**:
   5 camadas concêntricas com raio crescente e opacidade decrescente exponencialmente.

---

## 4. Catálogo das 11 Skills Oficiais

1. `motion-best-practices`: Filosofia Python-First, Safe Area (10% em 1080p e 12%-38% em Shorts) e Paleta Obsidian & Amber.
2. `motion-markup`: Primitivas gráficas em memória (Pillow + NumPy) e artigos técnicos de efeitos.
3. `motion-render`: Streaming via pipe para FFmpeg gerando `.mp4` Full-Screen e `.webm` transparente.
4. `motion-composition`: Montagem na timeline via `filter_complex`, PTS Shift e regras acústicas EBU R128.
5. `motion-notebooks`: Prototipagem e player com transparência xadrez em Google Colab / Jupyter.
6. `motion-maps`: Retículas cartográficas HUD polares e radares pulsantes.
7. `motion-captions`: Legendas virais condensadas amarelas (#FFFF00) com contorno preto grosso.
8. `motion-studio`: Paridade visual com Canvas 2D HTML5 e inspeção offline rápida.
9. `motion-multimedia`: Extração de dimensões e metadados via FFprobe em Python puro.
10. `motion-create`: Scaffolding estrutural de novos módulos.
11. `motion-interactivity`: Parametrização declarativa via esquemas JSON.
