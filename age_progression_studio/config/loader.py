"""TOML config loader with env overrides."""
from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AppConfig:
    log_level: str = "INFO"
    default_model: str = "aps-v3"
    output_dir: str = "./out"
    max_resolution: int = 1024


def load_config(path: Path) -> AppConfig:
    cfg = AppConfig()
    if path.exists():
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        for k, v in data.get("app", {}).items():
            if hasattr(cfg, k):
                setattr(cfg, k, v)
    cfg.log_level = os.environ.get("APS_LOG_LEVEL", cfg.log_level)
    cfg.output_dir = os.environ.get("APS_OUTPUT_DIR", cfg.output_dir)
    return cfg