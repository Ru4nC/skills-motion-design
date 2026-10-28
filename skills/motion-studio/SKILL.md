---
name: motion-studio
description: Paridade visual entre o motor Python e Canvas 2D em navegador, inspeção offline com ffplay e exportação de stills.
version: 1.0.0
---

# Motion Studio: Paridade Canvas 2D e Inspeção Offline

Este módulo define os requisitos de paridade matemática e visual entre o motor de renderização Python (`Pillow` + `NumPy`) e artefatos de visualização web em Canvas HTML5 (`motion_studio.html`), além de orientar a inspeção ágil de animações com `ffplay` e stills estáticos.

## 1. Contrato de Paridade `window.renderAutomationFrame`

Para permitir que desenvolvedores e interfaces web inspecionem animações sem necessidade de rodar o FFmpeg para cada alteração de estilo, o visualizador HTML5 expõe uma função global com assinatura idêntica à do motor Python:

```javascript
window.renderAutomationFrame = function(templateName, sceneData, localeData, timeInSeconds, totalDuration) {
    const canvas = document.getElementById("motionCanvas");
    const ctx = canvas.getContext("2d");
    
    // 1. Limpa canvas transparente
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // 2. Safe Area perimetral de 10%
    const mx = canvas.width * 0.10;
    const my = canvas.height * 0.10;
    
    // 3. Aplica exatamente as mesmas curvas matemáticas do Python
    const enter_t = Math.min(1.0, timeInSeconds / 0.45);
    const enter_ease = 1.0 - Math.pow(1.0 - enter_t, 3);
    
    // 4. Desenha elementos gráficos correspondentes
    // ...
};
```

## 2. Inspeção Rápida de Vídeos Transparentes com `ffplay`

Para inspecionar um clipe `.webm` gerado localmente em alta taxa de quadros e verificar a integridade da transparência antes de aplicar no montador:

```bash
# Executa visualização do clipe com fundo transparente
ffplay -autoexit -v quiet output_overlay.webm
```

## 3. Auditoria Visual Automatizada (Visual Regression QA)

Gere dois stills de comparação no frame de estabilização máxima ($t = 1.5s$) para atestar que o resultado do Pillow no backend coincide perfeitamente com a especificação visual acordada:

```python
def verify_visual_parity(still_a_path: str, still_b_path: str, tolerance_rms: float = 2.0) -> bool:
    """
    Compara duas imagens RGBA calculando o erro quadrático médio (RMS).
    """
    import numpy as np
    from PIL import Image
    
    arr_a = np.array(Image.open(still_a_path).convert("RGBA"), dtype=np.float32)
    arr_b = np.array(Image.open(still_b_path).convert("RGBA"), dtype=np.float32)
    
    rms = np.sqrt(np.mean((arr_a - arr_b) ** 2))
    return rms <= tolerance_rms
```
