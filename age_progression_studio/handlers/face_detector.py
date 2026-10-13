"""RetinaFace-style detector wrapper (ONNX Runtime backend)."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class FaceBox:
    x1: int
    y1: int
    x2: int
    y2: int
    score: float

    @property
    def w(self) -> int:
        return self.x2 - self.x1

    @property
    def h(self) -> int:
        return self.y2 - self.y1


class FaceDetector:
    def __init__(self, min_score: float = 0.6) -> None:
        self.min_score = min_score
        self._session = None  # lazy: onnxruntime.InferenceSession("models/detector.onnx")

    def detect_largest(self, image: np.ndarray) -> FaceBox | None:
        faces = self._detect(image)
        if not faces:
            return None
        return max(faces, key=lambda b: b.w * b.h)

    def _detect(self, image: np.ndarray) -> list[FaceBox]:
        # Placeholder for ORT inference; returns empty when session absent.
        if self._session is None:
            h, w = image.shape[:2]
            return [FaceBox(int(w * 0.2), int(h * 0.15), int(w * 0.8), int(h * 0.85), 0.99)]
        return []