"""Age-conditioning curve utilities (monotone wrinkle/volume schedules)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgingCurve:
    wrinkle: float
    volume_loss: float
    pigment: float

    @staticmethod
    def at(age: int) -> "AgingCurve":
        a = max(1, min(90, age))
        t = (a - 1) / 89.0
        return AgingCurve(
            wrinkle=min(1.0, t ** 1.6),
            volume_loss=min(1.0, 0.9 * t ** 1.3),
            pigment=min(1.0, 0.5 * t + 0.1),
        )