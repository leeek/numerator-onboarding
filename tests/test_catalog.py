from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from numerator_onboarding.catalog import catalog_tables, main
from numerator_onboarding.config import data_root


FIXTURE = Path(__file__).parent / "data/fake_numerator"


def test_synthetic_catalog_uses_metadata(monkeypatch):
    def forbid_scan(*args, **kwargs):
        pytest.fail("Catalog must not scan observations")

    monkeypatch.setattr(pq, "read_table", forbid_scan)
    monkeypatch.setattr(pq.ParquetFile, "read", forbid_scan)
    monkeypatch.setattr(pq.ParquetFile, "read_row_group", forbid_scan)
    monkeypatch.setattr(pq.ParquetFile, "read_row_groups", forbid_scan)
    monkeypatch.setattr(pq.ParquetFile, "iter_batches", forbid_scan)
    tables = catalog_tables(FIXTURE)
    assert [t["table_name"] for t in tables] == [
        "item_table", "people_table", "summarylvl_fact_table"
    ]
    assert [t["total_rows"] for t in tables] == [4, 4, 6]
    for table in tables:
        assert table["parquet_files"] == 2
        files = list((FIXTURE / table["table_name"]).rglob("*.parquet"))
        assert table["compressed_size_bytes"] == sum(p.stat().st_size for p in files)
        assert table["schemas"][0]["file_count"] == 2
    assert tables[-1]["schemas"][0]["columns"] == [
        {"name": "household_id", "type": "string", "nullable": True},
        {"name": "spend", "type": "double", "nullable": True},
        {"name": "channel", "type": "string", "nullable": True},
    ]


def test_fixture_is_snappy():
    for path in FIXTURE.rglob("*.parquet"):
        metadata = pq.read_metadata(path)
        for index in range(metadata.num_row_groups):
            group = metadata.row_group(index)
            assert all(group.column(i).compression == "SNAPPY" for i in range(group.num_columns))


def test_schema_variations_empty_files_and_non_data_directories(tmp_path):
    table_dir = tmp_path / "table" / "partition=one"
    table_dir.mkdir(parents=True)
    (tmp_path / "0-Data_Description_and_Schemas").mkdir()
    (table_dir / "notes.txt").write_text("Not a data file")
    pq.write_table(pa.table({"value": [1, 2, 3]}), table_dir / "a.parquet", row_group_size=1)
    pq.write_table(pa.table({"label": pa.array([], type=pa.string())}), table_dir / "b.parquet")
    result = catalog_tables(tmp_path)
    assert len(result) == 1
    assert result[0]["parquet_files"] == 2
    assert result[0]["total_rows"] == 3
    assert len(result[0]["schemas"]) == 2
    assert {s["columns"][0]["type"] for s in result[0]["schemas"]} == {"int64", "string"}


def test_empty_root(tmp_path):
    assert catalog_tables(tmp_path) == []


def test_missing_root(tmp_path):
    with pytest.raises(NotADirectoryError):
        catalog_tables(tmp_path / "missing")


def test_invalid_parquet_fails_without_logging_values(tmp_path, monkeypatch, capsys):
    directory = tmp_path / "table" / "person_id=private_value"
    directory.mkdir(parents=True)
    (directory / "bad.parquet").write_text("invalid file")
    monkeypatch.setenv("NUMERATOR_ROOT", str(tmp_path))
    with pytest.raises(SystemExit) as error:
        main()
    assert "Catalog failed" in str(error.value)
    assert "private_value" not in str(error.value)
    assert capsys.readouterr().out == ""


def test_data_root(monkeypatch, tmp_path):
    monkeypatch.delenv("NUMERATOR_ROOT", raising=False)
    assert data_root() == FIXTURE.resolve()
    monkeypatch.setenv("NUMERATOR_ROOT", str(tmp_path))
    assert data_root() == tmp_path
    monkeypatch.setenv("NUMERATOR_ROOT", "")
    with pytest.raises(ValueError):
        data_root()


def test_cli_uses_selected_fixture(monkeypatch, capsys):
    import json

    monkeypatch.setenv("NUMERATOR_ROOT", str(FIXTURE))
    main()
    output = capsys.readouterr().out
    assert len(json.loads(output)) == 3
    assert "fake_h001" not in output
    assert "fake_p001" not in output
