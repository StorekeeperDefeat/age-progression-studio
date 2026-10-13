"""Entry point: python -m age_progression_studio"""
from __future__ import annotations

import sys

from age_progression_studio.app.bootstrap import bootstrap


def main(argv: list[str] | None = None) -> int:
    return bootstrap(argv if argv is not None else sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())