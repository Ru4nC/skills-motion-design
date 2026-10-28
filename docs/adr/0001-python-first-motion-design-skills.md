# 0001: Arquitetura Python-First de Motion Design

## Contexto
Sistemas de geração automatizada de vídeo frequentemente recorrem a runtimes baseados em navegadores headless (Chromium, Node.js), que impõem sobrecarga de memória, inicialização lenta e dependências de pacotes complexas em produção.

## Decisão
Adotamos uma arquitetura estritamente **Python-First** (100% contida em ambiente Python, determinística e offline) para Motion Design:
1. **Motor Gráfico em Memória**: Geração de quadros diretamente em memória com Pillow + NumPy como buffers rawvideo RGBA.
2. **Streaming via Pipe**: Transmissão contínua para o FFmpeg (codec VP9 em `yuva420p` com canal alfa real e `-auto-alt-ref 0`) sem arquivos PNG temporários em disco.
3. **Composição na Timeline**: Sobreposição via `filter_complex` com ajuste temporal de apresentação (PTS Shift: `setpts=PTS-STARTPTS+{t_start}/TB`).
4. **Técnicas Cinemáticas Nativas**: Implementação direta em Python de marca-texto orgânico, motion blur direcional, osciloscópios e interpolações matemáticas.
5. **Prototipagem em Notebooks**: Suporte nativo a Google Colab e Jupyter com visualização inline de canal alfa sobre fundo quadriculado.

## Consequências
- Execução ultra-rápida (~1.5s por clipe de animação) e determinística.
- Zero dependência externa de navegadores ou Node.js.
- Conjunto universal de Agent Skills para agentes de codificação em IA.
