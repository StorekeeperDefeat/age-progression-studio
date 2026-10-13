"""Logging configuration for CLI + GUI runs."""
from __future__ import annotations

import logging
import os
from pathlib import Path


def configure_logging(level: str = "INFO") -> None:
    root = Path(os.environ.get("LOCALAPPDATA", ".")) / "AgeProgressionStudio" / "logs"
    root.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(root / "aps.log", encoding="utf-8")],
    )