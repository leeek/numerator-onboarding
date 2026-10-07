"""Generate invented observations at a fixed local fixture path; never reads data."""

from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq


ROOT = Path(__file__).resolve().parents[1] / "tests/data/fake_numerator"


def main() -> None:
    for month in (1, 2):
        tables = {
            "summarylvl_fact_table": pa.table({
                "household_id": ["fake_h001", "fake_h002", "fake_h003"],
                "spend": [12.50 + month, 8.25, 21.00],
                "channel": ["grocery", "online", "grocery"],
            }),
            "people_table": pa.table({
                "person_id": ["fake_p001", "fake_p002"],
                "household_id": ["fake_h001", "fake_h002"],
                "age_band": ["25-34", "45-54"],
            }),
            "item_table": pa.table({
                "item_id": ["fake_i001", "fake_i002"],
                "category": ["snacks", "beverages"],
            }),
        }
        for name, table in tables.items():
            path = ROOT / name / "year=2026" / f"month={month:02d}" / "part-000.parquet"
            path.parent.mkdir(parents=True, exist_ok=True)
            pq.write_table(table, path, compression="snappy", row_group_size=2)
    print("Created six synthetic Parquet files (14 rows total).")


if __name__ == "__main__":
    main()
