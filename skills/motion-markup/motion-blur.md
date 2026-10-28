# Motion Blur Direcional em Python

Esta técnica ensina como implementar desfoque de movimento (*motion blur*) direcional fracionado para elementos gráficos em movimento acelerado através de manipulação vetorial e matricial rápida com Pillow e NumPy.

## Princípio Físico e Matemático

O olho humano percebe arrasto óptico quando um objeto atravessa a tela em alta velocidade. No início de uma animação de entrada com interpolação cúbica ($0 \le t \le 0.35s$):

$$\text{enter\_t} = \min(1.0, t / 0.35)$$
$$\text{enter\_ease} = 1.0 - (1.0 - \text{enter\_t})^3$$

A velocidade instantânea de deslocamento é dada pela primeira derivada da curva de transição:

$$v(t) = \frac{d(\text{enter\_ease})}{dt} \propto 3 \cdot (1.0 - \text{enter\_t})^2$$

Conforme o elemento se aproxima do repouso ($\text{enter\_t} \to 1.0$), a velocidade e o arrasto caem a zero ($v \to 0$).

## Implementação com Deslocamento Fracionado

Em vez de renderizar múltiplos passes caros de convolução gaussiana global que degradariam o tempo de renderização, o motor calcula o deslocamento horizontal proporcional:

```python
def calculate_directional_motion_blur_shift(
    t: float,
    enter_ease: float,
    direction: str = "right",
    max_shift_px: float = 28.0,
    acceleration_window: float = 0.35,
) -> int:
    """
    Retorna o deslocamento em pixels a ser aplicado na coordenada X do elemento.
    """
    if t >= acceleration_window:
        return 0
    
    # Arrasto diminui conforme o card desacelera
    blur_shift = int(max_shift_px * (1.0 - enter_ease))
    return blur_shift if direction == "right" else -blur_shift
```

## Efeito de Rastro com Alpha Decrescente (Ghosting Pass)

Para animações com objetos sólidos em alta velocidade, renderize passes adicionais defasados com opacidade reduzida para criar rastro óptico:

```python
def apply_motion_blur_ghosting(img_base, draw_element_fn, t, passes=3):
    """
    Desenha réplicas translúcidas ligeiramente defasadas no eixo do movimento.
    """
    for p in range(passes, 0, -1):
        offset = int(p * 8 * (1.0 - min(1.0, t / 0.35)))
        ghost_alpha = int(40 / p)
        draw_element_fn(offset_x=offset, alpha_override=ghost_alpha)
```
