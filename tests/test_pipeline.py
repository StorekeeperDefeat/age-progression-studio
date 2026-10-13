"""Smoke tests for the aging pipeline (no GPU required)."""
from __future__ import annotations

import numpy as np

from age_progression_studio.core.pipeline import AgeProgressionPipeline, PipelineConfig


def _fake_face() -> np.ndarray:
    return np.full((256, 256, 3), 180, dtype=np.uint8)


def test_pipeline_runs_end_to_end() -> None:
    pipe = AgeProgressionPipeline(PipelineConfig(device="cpu"))
    out = pipe.run(_fake_face(), target_age=60)
    assert out.shape == (256, 256, 3)
    assert out.dtype == np.uint8


def test_aging_curve_monotone() -> None:
    from age_progression_studio.services.aging_curve import AgingCurve

    a = AgingCurve.at(20)
    b = AgingCurve.at(70)
    assert b.wrinkle > a.wrinkle
    assert b.volume_loss > a.volume_loss