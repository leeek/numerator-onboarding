# Numerator onboarding on Great Lakes

A small metadata-first Python exercise for University of Michigan faculty and
researchers. Local development uses invented data only; no real Numerator data
is included or needed. Requires Python 3.10 or newer.

## Setup and verification

From the repository root:

```sh
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
export NUMERATOR_ROOT="$PWD/tests/data/fake_numerator"
python -m pytest
numerator-catalog
python examples/duckdb_query.py
```

With `NUMERATOR_ROOT` unset, the editable checkout defaults to the same synthetic
fixture. An explicitly empty variable is rejected. For a non-editable installation,
set `NUMERATOR_ROOT` explicitly: fixtures are not packaged in the wheel.

## Exercise 1: inspect before querying

Run `numerator-catalog` (equivalently `python -m numerator_onboarding.catalog`).
Its JSON output reports each table's name, recursive `.parquet` file count, total
rows, compressed file bytes, and column names/types/nullability. Every immediate
child directory containing Parquet files is a table; documentation and empty
directories are skipped. All matching files are counted, so use a stable dataset
without duplicate or staging files.

Row counts come from Parquet footer metadata, with no observation scan or pandas
load. Size is the sum of file lengths, including compressed data and Parquet
overhead, not filesystem allocation blocks or uncompressed memory size. All files
are inspected, so metadata work still takes time on large trees. Invalid or
unreadable files fail the run instead of producing a partial catalog.

Each distinct physical schema is reported with its file count; inspect variations
before writing queries. Directory-only Hive partition keys such as `year` and
`month` are not physical columns and are not included in the catalog. Arrow schema
annotations are omitted. The catalog prints schema information, never row values
or file paths.

The fixture has three tables, each with two nested `year=2026/month=...` partitions:

| Table | Files | Rows |
| --- | ---: | ---: |
| item_table | 2 | 4 |
| people_table | 2 | 4 |
| summarylvl_fact_table | 2 | 6 |

These names and columns illustrate structure, not Numerator's actual schema or
business semantics. Rebuild the six Snappy-compressed files with
`python scripts/make_fake_data.py`. The generator writes only to the fixed fixture
directory and ignores `NUMERATOR_ROOT`.

## Exercise 2: a small DuckDB aggregate

`python examples/duckdb_query.py` reads the synthetic summary table with DuckDB,
groups by channel, and returns only the aggregate rows to Python:

```text
channel | observations | total_spend
grocery | 4 | 70.00
online | 2 | 16.50
```

DuckDB recognizes Hive directory partitions. Unlike the catalog, this query scans
selected column data. A small result or a `LIMIT` does not guarantee a small scan.
Before adapting it to real data, inspect the actual schema and add appropriate
partition filters. The illustrative `channel` and `spend` fields are not promised
to exist in the real tables.

## Working with real data

Real data stays on `greatlakes.arc-ts.umich.edu`. On Great Lakes, in the checked-out
repository with dependencies available, the same catalog supports:

```sh
NUMERATOR_ROOT=/nfs/turbo/bus-kbaldata/Numerator python -m numerator_onboarding.catalog
```

The known top-level directories are `summarylvl_fact_table`, `people_table`,
`static_table`, `itemlvl_fact_table`, `item_table`, `people_attributes_table`,
`people_history_table`, `banner_table`, and `0-Data_Description_and_Schemas`.
The catalog discovers tables rather than hardcoding this list.

- **Never commit Numerator data. Never copy raw Numerator observations into this repo.**
- Develop against synthetic data locally. Do not mount, download, or access real
  Numerator data during local development.
- Do not print household/person identifiers in logs, notebooks, or error reports.
  Do not save row-level extracts here. Review aggregates before sharing them.
- Run large real-data scans on allocated Great Lakes compute nodes, **not login
  nodes**. For a large metadata crawl, use a compute allocation as well.
- `.gitignore` blocks common data formats but cannot enforce these rules. Its
  fixture exception is for generated synthetic data only. Review staged files.

Implementation lives in `src/numerator_onboarding/`; tests always select the
synthetic fixture or temporary data explicitly, even if `NUMERATOR_ROOT` points
elsewhere. No pandas dependency is used.
