# Timing, Easing e Roll-up Numérico em Python

Esta técnica aborda a modelagem matemática de curvas de aceleração e desaceleração (*easing*), interpolação temporal e contadores numéricos progressivos (*roll-up*) em código Python determinístico.

## Curvas Canônicas de Interpolação

Elimine interpolações estritamente lineares, pois transmitem rigidez artificial. Utilize as funções matemáticas abaixo:

### 1. EaseOutExpo (Desaceleração Exponencial Rápida)
Ideal para contadores numéricos, barras de escala e revelações que precisam surgir rapidamente e pousar suavemente:

$$\text{easeOutExpo}(p) = 1.0 - 2^{-10 \cdot p}$$

```python
def ease_out_expo(progress: float) -> float:
    """Interpolação exponencial: arrancada imediata e desaceleração suave."""
    p = max(0.0, min(1.0, float(progress)))
    if p >= 0.999:
        return 1.0
    return 1.0 - pow(2.0, -10.0 * p)
```

### 2. Cubic Out (Desaceleração Cúbica Suave)
Ideal para deslocamento de cartões e opacidade de entrada:

$$\text{cubic\_out}(p) = 1.0 - (1.0 - p)^3$$

```python
def cubic_out(progress: float) -> float:
    p = max(0.0, min(1.0, float(progress)))
    return 1.0 - pow(1.0 - p, 3)
```

### 3. Smoothstep (Curva Sigmoidal Suave em S)
Excelente para transições de câmera e fades equilibrados:

$$\text{smoothstep}(p) = 3p^2 - 2p^3$$

```python
def smoothstep(progress: float) -> float:
    p = max(0.0, min(1.0, float(progress)))
    return p * p * (3.0 - 2.0 * p)
```

## Contador Numérico Progressivo (Roll-up)

Para animar números subindo (ex: `0%` a `95%`, ou anos de `1900` a `2026`), combine `ease_out_expo` com a duração do bloco de exibição:

```python
def calculate_rollup_value(
    t: float,
    start_time: float,
    duration: float,
    target_value: float,
    initial_value: float = 0.0,
) -> float:
    """
    Calcula o valor presente de um contador numérico em qualquer instante t.
    """
    if t < start_time:
        return initial_value
    
    elapsed = t - start_time
    prog_raw = min(1.0, max(0.0, elapsed / max(0.2, duration * 0.6)))
    prog_ease = ease_out_expo(prog_raw)
    
    return initial_value + (target_value - initial_value) * prog_ease
```
