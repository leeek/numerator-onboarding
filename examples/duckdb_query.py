"""Aggregate one table without materializing its observations in Python."""

import duckdb

from numerator_onboarding.config import data_root


def main() -> None:
    pattern = str(data_root() / "summarylvl_fact_table" / "**" / "*.parquet")
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
