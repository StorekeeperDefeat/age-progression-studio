"""Reusable network blocks (ResBlock, AdaIN, SPADE) for the aging generator."""
from __future__ import annotations

try:
    import torch
    import torch.nn as nn
except ImportError:  # torch optional at import-time
    torch = None  # type: ignore
    nn = object  # type: ignore


if torch is not None:

    class AdaIN(nn.Module):
        """Adaptive instance norm: modulates features by an age/identity code."""

        def __init__(self, channels: int, code_dim: int) -> None:
            super().__init__()
            self.norm = nn.InstanceNorm2d(channels, affine=False)
            self.to_scale = nn.Linear(code_dim, channels)
            self.to_bias = nn.Linear(code_dim, channels)

        def forward(self, x, code):
            s = self.to_scale(code).view(-1, x.shape[1], 1, 1)
            b = self.to_bias(code).view(-1, x.shape[1], 1, 1)
            return self.norm(x) * (1 + s) + b

    class ResBlock(nn.Module):
        def __init__(self, ch: int) -> None:
            super().__init__()
            self.body = nn.Sequential(
                nn.Conv2d(ch, ch, 3, padding=1),
                nn.SiLU(inplace=True),
                nn.Conv2d(ch, ch, 3, padding=1),
            )

        def forward(self, x):
            return x + self.body(x)