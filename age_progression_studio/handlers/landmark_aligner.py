"""5-point similarity alignment + inverse warp for compositing."""
from __future__ import annotations

import cv2
import numpy as np

from age_progression_studio.handlers.face_detector import FaceBox

REF_5PT = np.array(
    [[38.29, 51.69], [73.53, 51.50], [56.02, 71.73], [41.55, 92.36], [70.72, 92.20]],
    dtype=np.float32,
)


class LandmarkAligner:
    def __init__(self, out_size: int = 512) -> None:
        self.out_size = out_size
        self._last_matrix: np.ndarray | None = None

    def align(self, image: np.ndarray, box: FaceBox) -> np.ndarray:
        src = self._estimate_points(box)
        dst = REF_5PT * (self.out_size / 112.0)
        m, _ = cv2.estimateAffinePartial2D(src, dst, method=cv2.LMEDS)
        self._last_matrix = m
        return cv2.warpAffine(image, m, (self.out_size, self.out_size), flags=cv2.INTER_LINEAR)

    def unwarp(self, aged: np.ndarray, box: FaceBox, *, out_size: tuple[int, int]) -> np.ndarray:
        if self._last_matrix is None:
            return aged
        inv = cv2.invertAffineTransform(self._last_matrix)
        warped = cv2.warpAffine(aged, inv, (out_size[1], out_size[0]), flags=cv2.INTER_LINEAR)
        return warped

    @staticmethod
    def _estimate_points(box: FaceBox) -> np.ndarray:
        x1, y1, x2, y2 = box.x1, box.y1, box.x2, box.y2
        w, h = x2 - x1, y2 - y1
        return np.array(
            [
                [x1 + 0.30 * w, y1 + 0.35 * h],
                [x1 + 0.70 * w, y1 + 0.35 * h],
                [x1 + 0.50 * w, y1 + 0.55 * h],
                [x1 + 0.35 * w, y1 + 0.78 * h],
                [x1 + 0.65 * w, y1 + 0.78 * h],
            ],
            dtype=np.float32,
        )