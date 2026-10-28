---
name: motion-interactivity
description: Parametrização declarativa via JSON e controle temporal de keyframes para animações em Python.
version: 1.0.0
---

# Parametrização Declarativa e Interatividade em Python

Este módulo aborda o desacoplamento entre a arte gráfica e os dados de entrada através de esquemas declarativos JSON, permitindo que roteiros e agentes configurem parâmetros visuais sem alterar o código de desenho.

## 1. Contrato Declarativo JSON

Toda animação deve ser configurável através de um dicionário serializável:

```json
{
  "type": "stat",
  "start_sec": 12.4,
  "duration_sec": 4.2,
  "position": "top-right",
  "accent_color": "#F59E0B",
  "data": {
    "title": "TAXA DE EXPANSÃO",
    "value": 73.2,
    "suffix": " km/s/Mpc",
    "description": "Medição confirmada pelo telescópio espacial Hubble."
  }
}
```

## 2. Validação e Consumo em Python

```python
from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class MotionItemSpec:
    graphic_type: str
    start_sec: float
    duration_sec: float
    position: str = "top-right"
    accent_color: str = "#F59E0B"
    data: Dict[str, Any] = None

    @classmethod
    def from_dict(cls, payload: dict) -> "MotionItemSpec":
        return cls(
            graphic_type=payload.get("type", "fact"),
            start_sec=float(payload.get("start_sec", 0.0)),
            duration_sec=float(payload.get("duration_sec", 4.0)),
            position=payload.get("position", "top-right"),
            accent_color=payload.get("accent_color", "#F59E0B"),
            data=payload.get("data") or {},
        )
```
