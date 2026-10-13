"""Conditional aging renderer. Wraps the loaded torch/ONNX model."""
from __future__ import annotations

import numpy as np


class AgeSynthesizer:
    def __init__(self, model, device: str = "cpu") -> None:
        self.model = model
        self.device = device

    def render(
        self,
        aligned: np.ndarray,
        *,
        identity: np.ndarray,
        target_age: int | None,
        keep_identity: float,
    ) -> np.ndarray:
        age = target_age if target_age is not None else 45
        # Placeholder: identity-preserving contrast/brightness shift keyed to age.
        x = aligned.astype(np.float32) / 255.0
        warp = 1.0 + (age - 30) / 240.0
        out = np.clip((x ** warp) * (1.0 - 0.15 * keep_identity) + 0.15 * keep_identity, 0.0, 1.0)
        return (out * 255.0).astype(np.uint8)