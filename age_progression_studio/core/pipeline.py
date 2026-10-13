"""AgeProgressionPipeline — the end-to-end face aging orchestrator.

Inputs:  BGR ndarray (H,W,3) uint8, source face image.
Output:  BGR ndarray, same spatial size, age-conditioned.

Concurrency: single-threaded per instance; wrap in a pool for batch.
Memory:   peak ~1.4 GB at 1024x1024 on CUDA fp16.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass

import numpy as np

from age_progression_studio.handlers.face_detector import FaceDetector
from age_progression_studio.handlers.landmark_aligner import LandmarkAligner
from age_progression_studio.models.registry import load_model
from age_progression_studio.services.identity_encoder import IdentityEncoder
from age_progression_studio.services.age_synthesizer import AgeSynthesizer

log = logging.getLogger("aps.pipeline")


@dataclass
class PipelineConfig:
    model_id: str = "aps-v3"
    device: str = "cpu"
    keep_identity: float = 0.78
    blend_strength: float = 0.92


class AgeProgressionPipeline:
    def __init__(self, config: PipelineConfig) -> None:
        self.cfg = config
        self.detector = FaceDetector()
        self.aligner = LandmarkAligner()
        self.identity = IdentityEncoder(device=config.device)
        self.synth = AgeSynthesizer(load_model(config.model_id), device=config.device)

    @classmethod
    def from_config(cls, cfg, *, device: str, model_id: str) -> "AgeProgressionPipeline":
        return cls(PipelineConfig(model_id=model_id, device=device))

    def run(self, image: np.ndarray, *, target_age: int | None) -> np.ndarray:
        face = self.detector.detect_largest(image)
        if face is None:
            raise ValueError("no face detected")
        aligned = self.aligner.align(image, face)
        emb = self.identity.encode(aligned)
        aged = self.synth.render(
            aligned,
            identity=emb,
            target_age=target_age,
            keep_identity=self.cfg.keep_identity,
        )
        return self.aligner.unwarp(aged, face, out_size=image.shape[:2])