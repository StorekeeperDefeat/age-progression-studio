"""ArcFace identity embedding. 512-d L2-normalized."""
from __future__ import annotations

import numpy as np


class IdentityEncoder:
    def __init__(self, device: str = "cpu", dim: int = 512) -> None:
        self.device = device
        self.dim = dim

    def encode(self, aligned: np.ndarray) -> np.ndarray:
        # Placeholder: deterministic pseudo-embedding from pixel stats.
        x = aligned.astype(np.float32) / 255.0
        vec = np.concatenate([x.mean(axis=(0, 1)), x.std(axis=(0, 1)), x.mean(axis=1).ravel()[:506]])
        vec = vec[: self.dim]
        n = np.linalg.norm(vec) + 1e-8
        return (vec / n).astype(np.float32)