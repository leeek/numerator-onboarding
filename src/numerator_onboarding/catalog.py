"""Inspect table directories using file stats and Parquet footers only."""

import json
from pathlib import Path

import pyarrow.parquet as pq

from .config import data_root


def catalog_tables(root: str | Path) -> list[dict]:
    """Catalog immediate child directories containing recursive *.parquet files.

    Empty/non-Parquet directories are omitted. Schema variants describe physical
    file columns; partition keys stored only in directory names are not inferred.
    File bytes include compression, footers, and other Parquet overhead.
    Invalid/unreadable files fail the run instead of silently undercounting.
    """
    root = Path(root)
    if not root.is_dir():
        raise NotADirectoryError("Data root must be an existing directory")

    tables = []
    for directory in sorted(root.iterdir()):
        if not directory.is_dir():
            continue
        file_count = row_count = file_bytes = 0
        schemas = {}
        for path in directory.rglob("*.parquet"):
            if not path.is_file():
                continue
            # No read_table(), read(), iter_batches(), or observation access.
            with pq.ParquetFile(path) as parquet:
                row_count += parquet.metadata.num_rows
                fields = tuple(
                    (field.name, str(field.type), field.nullable)
                    for field in parquet.schema_arrow
                )
            schemas[fields] = schemas.get(fields, 0) + 1
            file_count += 1
            file_bytes += path.stat().st_size

        if file_count:
            tables.append({
                "table_name": directory.name,
                "parquet_files": file_count,
                "total_rows": row_count,
                "compressed_size_bytes": file_bytes,
                "schemas": [
                    {
                        "file_count": count,
                        "columns": [
                            {"name": name, "type": dtype, "nullable": nullable}
                            for name, dtype, nullable in fields
                        ],
                    }
                    for fields, count in sorted(schemas.items())
                ],
            })
    return tables


def main() -> None:
    try:
        result = catalog_tables(data_root())
    except Exception:
        # Backend exception messages may contain sensitive paths/partition values.
        raise SystemExit(
            "Catalog failed. Check NUMERATOR_ROOT, permissions, and Parquet validity. "
            "Details suppressed to avoid logging sensitive paths or values."
        ) from None
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
