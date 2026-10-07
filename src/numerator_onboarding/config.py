"""Resolve data locations without touching their contents."""

import os
from pathlib import Path


def data_root() -> Path:
    """Use NUMERATOR_ROOT, or the fixture in this editable repository checkout."""
    configured = os.environ.get("NUMERATOR_ROOT")
    if configured is not None:
        if not configured.strip():
            raise ValueError("NUMERATOR_ROOT must not be empty")
        return Path(configured).expanduser()
    return Path(__file__).resolve().parents[2] / "tests" / "data" / "fake_numerator"
