"""Headless batch driver for folder-mode processing."""
from __future__ import annotations

import logging
from pathlib import Path

from age_progression_studio.core.pipeline import AgeProgressionPipeline
from age_progression_studio.utils.image_io import load_image, save_image

log = logging.getLogger("aps.batch")

SUPPORTED = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


def run_batch(pipeline: AgeProgressionPipeline, args) -> int:
    src = args.batch or args.input
    if src is None:
        log.error("no input or batch path provided")
        return 2

    out_dir: Path = args.out
    out_dir.mkdir(parents=True, exist_ok=True)

    files = [src] if src.is_file() else sorted(p for p in src.iterdir() if p.suffix.lower() in SUPPORTED)
    ok, fail = 0, 0
    for f in files:
        try:
            img = load_image(f)
            result = pipeline.run(img, target_age=args.target_age)
            save_image(out_dir / f"{f.stem}_age{args.target_age or 'auto'}.png", result)
            ok += 1
        except Exception as exc:  # noqa: BLE001
            log.warning("failed %s: %s", f, exc)
            fail += 1
    log.info("batch done ok=%d fail=%d", ok, fail)
    return 0 if fail == 0 else 1