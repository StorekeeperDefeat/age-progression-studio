"""Face parsing mask (skin / hair / eyes / mouth) via BiSeNet ONNX."""
from __future__ import annotations

import numpy as np

SKIN_CLASSES = (1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14)
HAIR_CLASSES = (17, 18)


class MaskParser:
    def parse(self, aligned: np.ndarray) -> np.ndarray:
        h, w = aligned.shape[:2]
        # Placeholder segmentation: elliptical skin prior.
        yy, xx = np.mgrid[0:h, 0:w]
        cx, cy = w / 2, h * 0.55
        mask = (((xx - cx) / (w * 0.32)) ** 2 + ((yy - cy) / (h * 0.42)) ** 2) <= 1.0
        return mask.astype(np.uint8)