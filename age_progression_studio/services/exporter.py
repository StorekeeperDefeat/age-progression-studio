"""Export aged renders to PNG / JPEG / side-by-side comparison sheet."""
from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


class Exporter:
    def __init__(self, quality: int = 95) -> None:
        self.quality = quality

    def write(self, path: Path, image: np.ndarray) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        params = [cv2.IMWRITE_JPEG_QUALITY, self.quality] if path.suffix.lower() in {".jpg", ".jpeg"} else []
        cv2.imwrite(str(path), image, params)

    def comparison_sheet(self, before: np.ndarray, after: np.ndarray) -> np.ndarray:
        h = min(before.shape[0], after.shape[0])
        b = cv2.resize(before, (int(before.shape[1] * h / before.shape[0]), h))
        a = cv2.resize(after, (int(after.shape[1] * h / after.shape[0]), h))
        return np.concatenate([b, a], axis=1)