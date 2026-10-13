"""Compute backend selection."""
from __future__ import annotations

import logging

log = logging.getLogger("aps.device")


def select_device(prefer: str = "auto") -> str:
    if prefer != "auto":
        return prefer
    try:
        import torch

        if torch.cuda.is_available():
            return "cuda"
    except Exception:  # noqa: BLE001
        pass
    try:
        import torch_directml  # noqa: F401

        return "dml"
    except Exception:  # noqa: BLE001
        pass
    return "cpu"