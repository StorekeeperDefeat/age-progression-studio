"""Metric sanity checks."""
from __future__ import annotations

import numpy as np

from age_progression_studio.utils.metrics import cosine, psnr


def test_cosine_identity() -> None:
    v = np.array([1.0, 2.0, 3.0], dtype=np.float32)
    assert abs(cosine(v, v) - 1.0) < 1e-6


def test_psnr_identical() -> None:
    x = np.zeros((8, 8, 3), dtype=np.uint8)
    assert psnr(x, x) == float("inf")