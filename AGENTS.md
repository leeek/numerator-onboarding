# Repository rules

- For setup help, read README.md first. Use the project's `.venv/bin/python`, reproduce failures with synthetic inputs, and diagnose the failing layer (allocation, interpreter, dependencies, proxy, or authentication) before changing architecture. Never request authentication tokens or print credential files.
- Before real-data work on Great Lakes, confirm the hostname and Slurm job match an active compute allocation. In browser VS Code, "Work locally" means the remote Great Lakes workspace. Do not delegate data access to a cloud environment.
- Develop locally against synthetic data only. Never access the real Numerator data from local development.
- Never commit Numerator data or copy raw Numerator observations into this repository, including examples, test output, notebooks, and logs.
- Never print household/person identifiers or observation values in logs. Use schemas and aggregate results for onboarding.
- The sole committed data exception is the tiny, generated synthetic fixture under `tests/data/fake_numerator/`. Never place real data there. Git ignore rules are not a security boundary.
- Real data stays on Great Lakes at `/nfs/turbo/bus-kbaldata/Numerator`. Large scans must run on allocated compute nodes, not login nodes.
- Configure input through `NUMERATOR_ROOT`; tests must explicitly select synthetic or temporary inputs and ignore any production environment setting.
- Keep the catalog metadata-only: use Parquet footers for row counts, and never load observations into pandas or Arrow tables to catalog them.
- Keep ordinary Python and a small dependency set. After changes run `.venv/bin/python -m pytest` and the synthetic catalog with `NUMERATOR_ROOT=tests/data/fake_numerator`.
