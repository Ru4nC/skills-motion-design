---
name: motion-best-practices
description: Diretrizes essenciais de arquitetura Python-First, determinismo offline, Safe Area, paleta cinemática e sincronia para Motion Design.
version: 1.0.0
---

# Motion Design Best Practices (Python-First)

Este documento estabelece os princípios arquiteturais fundamentais para criação, manutenção e auditoria de animações e Motion Design em ambientes Python-First, garantindo execução determinística, ausência de dependências web/browsers em produção e máxima qualidade estética.

## 1. Arquitetura 100% Contida e Determinística

- **Runtime Obrigatório**: Toda a suíte de animação deve ser executável estritamente a partir do interpretador Python (`.venv/bin/python`), sem invocar comandos `npx`, `npm`, `bun`, `node` ou iniciar instâncias de navegadores headless (Puppeteer, Playwright ou Chromium).
- **Zero Gravação de Frames em Disco**: O motor gráfico deve processar quadros em memória como buffers contínuos em formato `rawvideo` no espaço de cores RGBA, transmitindo os bytes diretamente via pipe (`stdin`) para o binário do FFmpeg. Gravar sequências de PNGs temporários em disco é estritamente proibido.
- **Determinismo Temporal**: Dado um timestamp $t$ ou um número de quadro $n$ e uma duração total, a função de renderização deve produzir exatamente o mesmo buffer de pixels em qualquer execução, sem depender de relógio do sistema, variáveis aleatórias não-semeadas ou rede externa.

## 2. Safe Area e Posicionamento Anti-Colisão

Todos os elementos gráficos animados devem respeitar margens de segurança perimetrais rígidas para evitar colisões com legendas dinâmicas, pontos focais de vídeo e elementos de interface dos reprodutores de vídeo:

### Formato Landscape / Long (16:9 - 1920x1080)
- **Margem de Segurança (10%)**: Mínimo de `192px` nas bordas horizontais (esquerda e direita) e `108px` nas bordas verticais (topo e rodapé).
- **Separação de Faixas**:
  - `top-right`: Posição padrão recomendada para cartões de dados, estatísticas e infográficos, liberando o quadrante inferior para legendas e o centro-esquerdo para o assunto principal do vídeo.
  - `top-left`: Utilizado para manchetes contextuais, carimbos e identificadores de fontes de notícias.
  - `bottom-left`: Reservado exclusivamente para identificadores pontuais (Lower Thirds), garantindo distância segura da faixa central inferior de legendas.

### Formato Portrait / Shorts (9:16 - 1080x1920)
- **Zona Segura Vertical Restrita**: Em vídeos verticais, todo o conteúdo informativo de motion graphics deve situar-se estritamente na faixa entre **12% e 38%** da altura total da tela ($230px \le Y \le 730px$).
- **Blindagem contra UI**: Elementos nunca devem ser posicionados nos 10% superiores (zona de títulos/cabeçalho do YouTube) nem abaixo de 40% da altura (onde botões de like, comentários, inscrição e legendas virais ocupam a visão).

## 3. Paleta Oficial Obsidian & Amber (High-Contrast Cinema)

Para conferir identidade visual cinemática de alto contraste e legibilidade imediata, adote os seguintes padrões cromáticos em espaço de cor RGBA:

| Nome da Cor | Hex / RGBA | Finalidade Narrativa |
|---|---|---|
| **Obsidian Background** | `#0A0B0E` / `(10, 11, 14, 235)` | Fundo escuro semitranslúcido de painéis e cards |
| **Dark Panel** | `#111625` / `(17, 22, 37, 240)` | Camadas secundárias de cartões e profundidade |
| **Amber Active** | `#F59E0B` / `(245, 158, 11, 255)` | Cor de destaque primária para títulos e destaques |
| **Gold Metric** | `#FFD700` / `(255, 215, 0, 255)` | Realce de dados extraordinários e métricas chave |
| **Electric Cyan** | `#06B6D4` / `(6, 182, 212, 255)` | Telemetria científica, osciloscópios e radares |
| **Crimson Alert** | `#EF4444` / `(239, 68, 68, 255)` | Carimbos confidenciais, anomalias e avisos críticos |
| **Slate Secondary** | `#94A3B8` / `(148, 163, 184, 255)` | Legendas secundárias, eixos e dados de suporte |
| **Pure White** | `#F8FAFC` / `(248, 250, 252, 255)` | Texto principal com contraste máximo |

## 4. Sincronização Temporal e Lead-in de -0.2s

- **Antecipação Natural**: Para que a mente do espectador processe a informação visual no exato instante em que a narração pronuncia uma palavra-chave ou dado numérico, a animação deve iniciar com um **Lead-in de `-0.2s`** (`start_time = max(0.0, keyword_audio_time - 0.2)`).
- **Curvas de Entrada e Saída**:
  - **Entrada (0.45s)**: Aceleração rápida com desaceleração suave utilizando interpolação cúbica (`1.0 - pow(1.0 - t, 3)`).
  - **Saída (0.40s)**: Desvanecimento com dissipação proporcional de opacidade antes do corte da cena.
- **Resolução de PTS Shift**: Animações compiladas como arquivos independentes com canal alfa devem receber o filtro `setpts=PTS-STARTPTS+{t_start}/TB` no `filter_complex` do FFmpeg para sincronizar o início de reprodução e evitar que o último frame congele em tela preta ou sobreposição indevida.
