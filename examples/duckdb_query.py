"""Aggregate the synthetic fixture without materializing observations in Python."""

from pathlib import Path

import duckdb

from numerator_onboarding.config import data_root


def main() -> None:
    fixture = Path(__file__).resolve().parents[1] / "tests/data/fake_numerator"
    # Compare paths without opening or resolving the configured data directory.
    # This teaching query has no partition filter and must stay synthetic-only.
    if data_root().absolute() != fixture:
        raise SystemExit(
            "This example only accepts tests/data/fake_numerator. "
            "Set NUMERATOR_ROOT=tests/data/fake_numerator from the repository root."
        )
    pattern = str(fixture / "summarylvl_fact_table" / "**" / "*.parquet")
    with duckdb.connect() as connection:
        result = connection.execute(
            """
            SELECT channel, count(*) AS observations,
                   round(sum(spend), 2) AS total_spend
            FROM read_parquet(?, hive_partitioning = true)
            GROUP BY channel
            ORDER BY channel
            """,
            [pattern],
        ).fetchall()
    print("channel | observations | total_spend")
    for channel, count, spend in result:
        print(f"{channel} | {count} | {spend:.2f}")


if __name__ == "__main__":
    main()
