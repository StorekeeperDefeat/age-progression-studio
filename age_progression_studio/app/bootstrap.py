"""Runtime bootstrap.

Responsibilities:
  - Parse CLI args (--input, --target-age, --model, --device, --out).
  - Resolve config from config/default.toml + env overrides.
  - Select compute backend (CUDA / DirectML / CPU).
  - Launch either the Qt desktop window or a headless batch run.

Side effects: initializes torch device, loads model registry, writes
logs to %LOCALAPPDATA%\\AgeProgressionStudio\\logs.
"""
from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

from age_progression_studio.config.loader import load_config
from age_progression_studio.core.pipeline import AgeProgressionPipeline
from age_progression_studio.utils.device import select_device
from age_progression_studio.utils.logging_setup import configure_logging


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="age-progression-studio",
        description="AI age progression generator (desktop).",
    )
    p.add_argument("--input", type=Path, required=False, help="Source face image.")
    p.add_argument("--target-age", type=int, default=None, help="Target age 1..90.")
    p.add_argument("--model", default="aps-v3", help="Model id from registry.")
    p.add_argument("--device", default="auto", choices=["auto", "cuda", "dml", "cpu"])
    p.add_argument("--out", type=Path, default=Path("./out"))
    p.add_argument("--batch", type=Path, default=None, help="Folder of inputs.")
    p.add_argument("--headless", action="store_true")
    return p


def bootstrap(argv: list[str]) -> int:
    args = _build_parser().parse_args(argv)
    cfg = load_config(Path.cwd() / "config" / "default.toml")
    configure_logging(cfg.log_level)

    log = logging.getLogger("aps.bootstrap")
    device = select_device(args.device)
    log.info("device=%s model=%s target_age=%s", device, args.model, args.target_age)

    pipeline = AgeProgressionPipeline.from_config(cfg, device=device, model_id=args.model)

    if args.headless or args.input is None:
        from age_progression_studio.app.batch_runner import run_batch
        return run_batch(pipeline, args)

    from age_progression_studio.app.window import launch_window
    return launch_window(pipeline, args)