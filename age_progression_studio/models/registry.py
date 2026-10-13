"""Model registry: id → backend descriptor."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ModelDescriptor:
    id: str
    backend: str  # "torch" | "onnx"
    weights: Path
    resolution: int


REGISTRY: dict[str, ModelDescriptor] = {
    "aps-v3": ModelDescriptor("aps-v3", "torch", Path("weights/aps_v3.pt"), 512),
    "aps-v3-lite": ModelDescriptor("aps-v3-lite", "onnx", Path("weights/aps_v3_lite.onnx"), 256),
    "aps-v2": ModelDescriptor("aps-v2", "torch", Path("weights/aps_v2.pt"), 512),
}


def load_model(model_id: str):
    if model_id not in REGISTRY:
        raise KeyError(f"unknown model id: {model_id}")
    desc = REGISTRY[model_id]
    if not desc.weights.exists():
        return {"id": desc.id, "backend": desc.backend, "stub": True}
    return {"id": desc.id, "backend": desc.backend, "path": str(desc.weights)}