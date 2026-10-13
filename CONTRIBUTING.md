# Contributing to age-progression-studio

Thanks for helping build the AI age progression generator. This repo
targets Windows desktop, Python 3.11+, and a modular pipeline
(detect → align → identity → synthesize → export).

## Setup

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
```

## Running

```powershell
python -m age_progression_studio --input face.jpg --target-age 55 --out .\out
python -m age_progression_studio --batch .\faces --target-age 70 --headless
```

## Layout

- `age_progression_studio/app/` — bootstrap, CLI, Qt window, batch runner
- `age_progression_studio/core/` — pipeline orchestrator
- `age_progression_studio/handlers/` — detection, alignment, mask parsing
- `age_progression_studio/services/` — identity, synthesis, aging curve, export
- `age_progression_studio/models/` — registry + network blocks
- `age_progression_studio/config/` — TOML config + loader
- `age_progression_studio/utils/` — device, IO, logging, metrics

## Style

- `ruff check .` must pass.
- Type hints on public functions.
- New models go in `models/registry.py` with a matching descriptor.

## Pull requests

- One feature per PR.
- Add a test under `tests/`.
- Run `pytest -q` before pushing.