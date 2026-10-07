"""The teaching query must never follow an unrelated input setting."""

from pathlib import Path
import runpy

import duckdb
import pytest


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples/duckdb_query.py"


def test_example_rejects_other_input_before_connecting(monkeypatch, tmp_path):
    monkeypatch.setenv("NUMERATOR_ROOT", str(tmp_path / "not-the-fixture"))

    def forbid_connection(*args, **kwargs):
        pytest.fail("Non-fixture input must be rejected before opening DuckDB")

    monkeypatch.setattr(duckdb, "connect", forbid_connection)
    with pytest.raises(SystemExit, match="only accepts tests/data/fake_numerator"):
        runpy.run_path(str(EXAMPLE), run_name="__main__")


def test_example_aggregate(monkeypatch, capsys):
    monkeypatch.setenv("NUMERATOR_ROOT", str(ROOT / "tests/data/fake_numerator"))
    runpy.run_path(str(EXAMPLE), run_name="__main__")
    assert capsys.readouterr().out == (
        "channel | observations | total_spend\n"
        "grocery | 4 | 70.00\n"
        "online | 2 | 16.50\n"
    )
