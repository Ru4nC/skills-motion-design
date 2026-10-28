---
name: motion-captions
description: Geração e formatação de legendas dinâmicas virais (Bebas Neue #FFFF00, contorno grosso, 3 palavras/cue) em Python.
version: 1.0.0
---

# Legendas Dinâmicas Virais e Tipografia em Python

Este módulo fornece os padrões para geração, estilização e queima de legendas dinâmicas de alto engajamento visual para vídeos verticais (Shorts/Reels/TikTok) e horizontais (Longs), inspiradas nos formatos virais modernos.

## 1. Regra das 3 Palavras por Cue (Ritmo de Leitura Rápido)

- **Máximo de 3 palavras por tela**: O espectador não deve ler um parágrafo estático; as palavras devem surgir dinamicamente no ritmo da locução.
- **Tipografia em Caixa Alta (Uppercase)**: Todo o texto deve ser capitalizado em maiúsculas (`.upper()`).
- **Família Tipográfica de Impacto**: Famílias condensadas fortes, preferencialmente **Bebas Neue** ou **Cantarell ExtraBold**.

## 2. Parâmetros Visuais de Alto Contraste

| Parâmetro | Valor Padrão | Justificativa |
|---|---|---|
| **Cor da Fonte** | `#FFFF00` (Amarelo Puro) | Máxima retenção ocular e destaque instantâneo |
| **Contorno (Outline)** | `#000000`, largura `8px` | Separação física nítida contra qualquer cor de fundo |
| **Sombra Projetada** | `#000000`, blur `12px`, opacidade `0.95` | Profundidade adicional e leitura estável |
| **Alinhamento** | Centro horizontal, inferior vertical | Zona padrão de leitura ergonômica |

## 3. Posicionamento Seguro por Formato

- **Em Shorts (9:16)**: As legendas devem ser ancoradas na faixa de `70%` a `80%` da altura da tela, logo acima dos títulos do player móvel do YouTube e abaixo do ponto focal visual.
- **Em Longs (16:9)**: As legendas ficam ancoradas na margem inferior (`margin_v = 90px`), liberando o topo e a direita para overlays de dados (`motion-markup`).
