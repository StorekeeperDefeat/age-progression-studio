"""Identity-preservation + perceptual metrics for QA."""
from __future__ import annotations

import numpy as np


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    na, nb = np.linalg.norm(a) + 1e-8, np.linalg.norm(b) + 1e-8
    return float(np.dot(a, b) / (na * nb))


def psnr(a: np.ndarray, b: np.ndarray) -> float:
    mse = float(np.mean((a.astype(np.float64) - b.astype(np.float64)) ** 2))
    if mse == 0:
        return float("inf")
    return 10.0 * np.log10((255.0 ** 2) / mse)