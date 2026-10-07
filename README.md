# Numerator onboarding on Great Lakes

A small metadata-first Python exercise for University of Michigan faculty and
researchers. Local development uses invented data only; no real Numerator data
is included or needed. Requires Python 3.10 or newer.

## Prerequisites: accounts and data access

Before starting the Great Lakes setup, have the following ready:

- **Your U-M uniqname and Great Lakes access.** You will use your U-M login and
  MFA to sign in to the cluster and Open OnDemand. Obtain Great Lakes access
  through your department or U-M ARC if you do not already have it.
- **Your authorized Slurm account.** This is the allocation/billing account used
  to request compute time, not your login name. Ask your department or U-M ARC
  which account you should use. For example, Kevin's uniqname is `kvnlee` and his
  Slurm account is `kvnlee0` (a zero appended to the uniqname). This is an example,
  not a naming rule: confirm your assigned account rather than guessing it or
  using the instructor's account.
- **Numerator data access.** Open the
  [Ross Research Computing datasets page](https://rossrc.bus.umich.edu/databases.html),
  find **Numerator** under **Other Datasets**, and click **Request access to Numerator**.
  This permission is separate from Great Lakes access and access to this public
  repository. You can complete setup and the synthetic exercises while waiting
  for approval; real-data work requires that access to be granted.
- **A GitHub account.** Sign in before creating your own project from the template.
  If you do not have an account, create one first. You can browse this guide and
  clone the public starter for practice without signing in.

## Start here: let an assistant help with setup

You do not need to understand every shell command before starting. The suggested
route is to have a desktop assistant work through this guide with you, then use
Codex inside Great Lakes browser VS Code for everyday research. The explicit
commands below remain available for checking what happened and diagnosing failures.

1. Install and sign in to the **ChatGPT desktop app** on your Mac or Windows PC.
   Select **Codex** (or ChatGPT **Work**), and use **This computer** for the task.
2. Open **Plugins → Computer Use** and install/enable it. Follow its permission
   prompts. In **Settings → Computer use**, connect Google Chrome using the
   offered browser-extension setup. Availability depends on your account and region.
3. In Chrome, sign in to **GitHub** and **Great Lakes Open OnDemand**. Have your
   own Slurm account name ready, as explained in the prerequisites above.
4. Start a desktop task with `@Chrome` and paste the prompt below. You can provide
   this repository's URL without first downloading or cloning anything yourself.
5. Stay available for passwords, U-M MFA, ChatGPT sign-in, and permission prompts.
   Once setup passes its checks, continue research in the Codex sidebar of the
   Great Lakes browser editor.

Copy this prompt, replacing the two placeholders:

> @Chrome Help me set up https://github.com/leeek/numerator-onboarding on University
> of Michigan Great Lakes. Read its README.md and AGENTS.md first. My uniqname is
> YOUR_UNIQNAME and my authorized Slurm account is YOUR_SLURM_ACCOUNT. I am an
> empirical researcher, not a software engineer. Inspect what is already installed
> and complete the setup steps you can; explain briefly what each stage does.
> Use browser VS Code through Open OnDemand with 12 hours, 2 cores, and 8 GB.
> Help me create a private copy using the GitHub template, or start with the public
> starter for practice if Git authentication would delay setup. Keep Python work
> on an allocated compute node and use synthetic data only during setup. Do not
> access real Numerator data, overwrite existing work, or change account-security
> settings automatically. Let me handle authentication and required approvals.
> Finish by checking the node/job, Python environment, tests, synthetic catalog,
> and Codex command execution. Show me how to reconnect and stop the allocation.

This is guided assistance, not a guaranteed unattended installer. If Computer Use
is unavailable, use the manual instructions below and ask your assistant to explain
one step or error at a time. A regular web chat does not have access to your local
signed-in browser merely because you share this URL.

See OpenAI's [Computer Use setup](https://learn.chatgpt.com/docs/computer-use) and
[desktop/browser task guide](https://learn.chatgpt.com/use-cases/use-your-computer-with-codex).

## Create your own project

This is a public GitHub template. **Sign in to GitHub first** (create a free
GitHub account if you do not have one), then return to
[this repository](https://github.com/leeek/numerator-onboarding). To start your own
research project, click **Use this template → Create a new repository**, give your project a name, and
choose **Private**. Then clone your new repository onto Great Lakes
using its **Code → HTTPS** URL in the clone command below. This makes an independent
starting copy; later starter updates are not applied automatically. If you choose
a different project name, use that folder name everywhere below, including in
the setup file. Keep research
data outside Git, even in a private repository.

For a first practice session, cloning the starter directly is sufficient. You do
not need to create a fork or learn how to synchronize one to run the exercises.

## Manual setup: overview

If using the assistant above, let it work through these steps with you; this is
also the reference for doing setup yourself. Complete **One-time cluster checkout and Python environment**
below, then use **Great Lakes browser VS Code** for everyday work. Local practice
is optional. The initial SSH setup creates files and an environment; daily work
uses the browser and does not require configuring Remote-SSH.

## One-time cluster checkout and Python environment

If transferring changes from an existing local checkout, commit and push the code
you intend to run. Check `git status --short` and `git diff --cached` first. A new
user can start by cloning without making any commits.
Replace `YOUR_UNIQNAME` and `YOUR_SLURM_ACCOUNT` below with your own values. The
Slurm account is an allocation/billing account, not necessarily your uniqname.

On your laptop, in a terminal:

```sh
ssh YOUR_UNIQNAME@greatlakes.arc-ts.umich.edu
```

Complete password/MFA authentication yourself. On the Great Lakes login node,
clone once. The public starter requires no GitHub login. A private template copy
requires your own GitHub authentication, separate from your U-M login; GitHub
account passwords do not work for Git HTTPS authentication. Use an existing
authenticated Git setup or ask Codex to help configure it without sharing tokens.
For a first practice session, use this public clone command:

```sh
git clone https://github.com/leeek/numerator-onboarding.git
cd numerator-onboarding
git log -1 --oneline
```

For later sessions, use `cd ~/numerator-onboarding` and `git pull --ff-only`
instead. Stop if Git reports conflicting local changes; do not reset them away.
Check that the commit matches the one you intended to transfer.

Request a 12-hour interactive allocation:

```sh
salloc --account=YOUR_SLURM_ACCOUNT --partition=standard --nodes=1 --ntasks=1 --cpus-per-task=2 --mem=8G --time=12:00:00
hostname
echo "$SLURM_JOB_ID"
squeue -u "$USER"
```

Wait for the allocation to start. Great Lakes' `salloc` normally places the shell
on a compute node. Confirm the hostname matches your job's node, not `gl-login*`.
If the shell remains on a login node after allocation, use `srun --pty bash -l`
and check again. The resources above are a starting point for development and
metadata work, not a recommendation for full data scans. Keep the session open;
12 hours is the allocation limit, not a guarantee against connection loss or
shell idle timeouts. Exit when finished so the allocation can be released.

On the allocated compute node, create a separate Linux environment once; never
copy the laptop's `.venv` to Great Lakes:

```sh
cd ~/numerator-onboarding
module load python/3.12.1
python3 --version  # Expect Python 3.12.x
python3 -m venv .venv
source .venv/bin/activate
source /etc/profile.d/http_proxy.sh
python -m pip install -e '.[dev]'
NUMERATOR_ROOT=tests/data/fake_numerator python -m pytest
NUMERATOR_ROOT=tests/data/fake_numerator python -m numerator_onboarding.catalog
NUMERATOR_ROOT=tests/data/fake_numerator python examples/duckdb_query.py
```

Once verification succeeds, create the setup file in the browser workflow below,
then exit this one-time interactive shell to release its allocation.

On subsequent terminal sessions, load the same Python module and activate `.venv` again.
The tested module is `python/3.12.1`; use it consistently when creating and
activating the environment.
If installation cannot reach the package index from the compute node, follow
ITS's documented proxy setup (`source /etc/profile.d/http_proxy.sh`) and retry.

**Why an explicit Python version?** `module load python` selects the cluster's
current default, which can change. The guide uses `python/3.12.1` because that
exact setup passed the environment, package, and browser-editor checks. Python
3.13.2 is a reasonable candidate, but has not been validated for this workflow;
being the default does not itself make it more robust. If changing versions,
create a separate environment, use the same explicit module in the editor setup
file, and rerun the synthetic checks. Loading another module does not upgrade an
existing `.venv`. Keep the working environment until the replacement passes.

## Great Lakes browser VS Code: daily workflow

The recommended editor is **Visual Studio Code through Great Lakes Open OnDemand**,
with the official Codex extension running in the same compute allocation. Your
browser is the interface; Python and Codex's commands run on Great Lakes. Local
work remains synthetic-only. First create the cluster checkout and environment
using the explicit one-time commands above.

1. Create `~/numerator-ood-setup.sh` on Great Lakes using a text editor. Its contents
   should be the following (replace the environment path and use the same Python
   module that created your environment):

   ```sh
   source /etc/profile.d/http_proxy.sh
   module load python/3.12.1
   source /home/YOUR_UNIQNAME/numerator-onboarding/.venv/bin/activate
   ```

   This short file is sourced **before the editor starts**, so extensions inherit
   the compute-node internet proxy and Python environment. It does not submit jobs
   or hide Slurm commands. Keep the module line consistent with the environment
   creation command.

2. Open [Great Lakes Open OnDemand](https://greatlakes.arc-ts.umich.edu), sign in,
   and choose **Interactive Apps → Visual Studio Code**. Request your own Slurm
   account, `standard` partition, **12 hours**, **2 cores**, and **8 GB total memory**.
   Select code-server **4.112.0** if available (the pilot version). Set **Source this
   setup file** to `/home/YOUR_UNIQNAME/numerator-ood-setup.sh`. Launch the job.
3. Under **My Interactive Sessions**, wait for **Running**, then **Connect to VS Code**.
   Open your cluster repository folder. In **Terminal → New Terminal**, run:

   ```sh
   hostname
   echo "$SLURM_JOB_ID"
   .venv/bin/python --version
   NUMERATOR_ROOT=tests/data/fake_numerator .venv/bin/python -m pytest
   NUMERATOR_ROOT=tests/data/fake_numerator .venv/bin/python -m numerator_onboarding.catalog
   ```

   Match the hostname and job ID to the portal session. Stop if you are on a login
   node. The fixture counts should be 4, 4, and 6 rows (see the fixture table below).
4. Open **Extensions**, search for **Codex**, and install **Codex – OpenAI's coding
   agent**, publisher **openai**, identifier **openai.chatgpt**. Open its sidebar.
   Choose ChatGPT sign-in using a **device code**. Open the displayed authentication
   link in your laptop browser and enter the code. If asked, enable device-code
   sign-in in your ChatGPT account's Security settings yourself, then retry.
   Keep authentication codes and credential files out of this repository.
5. Ask Codex to verify the installation using the prompt below. Keep execution in
   this workspace, rather than delegating the task to a cloud environment:

   > Read AGENTS.md. Check hostname and SLURM_JOB_ID and confirm this is an allocated
   > compute node. Use .venv/bin/python with NUMERATOR_ROOT=tests/data/fake_numerator
   > to run pytest and python -m numerator_onboarding.catalog. Do not access real
   > data or modify source files. Report the node, job, Python version, test result,
   > and synthetic table counts. If something fails, diagnose that layer first.

Reopen the running session through **My Interactive Sessions** after closing the
browser. Closing the browser does not release the allocation. When finished,
stop/delete that specific session in the portal to release its resources. When
its time limit expires, launch a new session; the old compute-node URL is temporary.
The checkout lives in your home directory, so it survives allocation expiry.

**Validation:** code-server 4.112.0, the official Codex extension, and Python 3.12
were exercised on a Great Lakes compute node. Codex ran tests and the synthetic
catalog; browser reload preserved sign-in and the completed chat. A separate
checkout and new environment created with `python/3.12.1` also passed the tests,
catalog, and DuckDB example. A second 12-hour allocation on a different compute
node retained the Codex installation and sign-in; Codex ran all 10 tests there.
A one-file real Parquet footer check also succeeded without reading observations.
Extension versions may change through auto-update.

## First real-data check: one Parquet footer

Only when you decide to inspect real metadata, use one known Parquet file in
the allocated shell. Obtain its relative path on Great Lakes from your data
manager or by browsing there; do not paste filenames containing identifiers
into an AI chat. Replace the sample relative path below. This reads one footer,
without recursively discovering files, reading column statistics, or scanning
observations:

```sh
NUMERATOR_ROOT=/nfs/turbo/bus-kbaldata/Numerator python - 'people_table/REPLACE_WITH_RELATIVE_FILE.parquet' <<'PY'
import json
import sys
import pyarrow.parquet as pq
from numerator_onboarding.config import data_root

try:
    with pq.ParquetFile(data_root() / sys.argv[1]) as parquet:
        result = {
            "files_inspected": 1,
            "rows_in_this_file": parquet.metadata.num_rows,
            "columns": [
                {"name": field.name, "type": str(field.type), "nullable": field.nullable}
                for field in parquet.schema_arrow
            ],
        }
except Exception:
    raise SystemExit("Metadata check failed: check the path, access, and Parquet format on Great Lakes.") from None
print(json.dumps(result, indent=2))
PY
```

The result describes that file only, not table-wide row counts or schema
consistency. The full catalog visits every matching file, so run it later in a
compute allocation after the one-file check succeeds. A one-file footer check
has been exercised on an allocated Great Lakes compute node. It does not validate a full-tree catalog or an observation scan.

## Local practice with synthetic data

From the repository root:

```sh
python3 --version  # Must be 3.10 or newer
python3 -m venv .venv
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

This teaching example rejects a `NUMERATOR_ROOT` other than the repository's
synthetic fixture, before opening DuckDB. DuckDB recognizes Hive directory partitions.
Unlike the catalog, this query scans
selected column data. A small result or a `LIMIT` does not guarantee a small scan.
Before adapting it to real data, inspect the actual schema and add appropriate
partition filters. The illustrative `channel` and `spend` fields are not promised
to exist in the real tables.

## Working with real data

Real data stays on Great Lakes. Start with the one-file exercise above. Later,
inside a compute allocation with dependencies available, the full catalog supports:

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

## Debugging

Check failures one layer at a time:

| Symptom | First check |
| --- | --- |
| SSH fails | Account access, network/VPN requirements, and password/MFA; Python is not involved yet. |
| Slurm rejects the request | Allocation account and partition eligibility; ask the allocation owner if unknown. |
| Job remains pending | `squeue -u "$USER"` shows its state/reason; wait for resources. |
| Python import fails | `which python`, `python --version`, and `python -m pip show numerator-onboarding pyarrow duckdb`; activate the cluster `.venv`. |
| Metadata check fails | Verify the selected file and read permissions on Great Lakes; first rerun the synthetic catalog to separate environment problems from input problems. |
| Catalog prints `[]` | It found no Parquet files under immediate child directories; verify the root and directory layout. |

Catalog errors deliberately omit backend details because those can contain
identifiers in paths or partition values. Reproduce with synthetic inputs before
sharing an error. There is no automatic cluster detection in the Python code;
the researcher must check the allocation and hostname before real-data work.

For browser-editor problems, separate the layers:

| Symptom | First check |
| --- | --- |
| Portal will not open | U-M access/network/VPN and login; the repository is not involved yet. |
| Extensions cannot download or Codex cannot connect | Ensure the proxy is sourced by the setup file **before** launching VS Code. Setting it only in a terminal does not update an already-running extension. Relaunch the editor allocation with the setup file. |
| Browser redirects to localhost during sign-in | Use Codex's device-code login instead. |
| Device login is refused | Enable device-code sign-in in ChatGPT Security settings and request a fresh code. |
| Editor URL stops working | Check whether the allocation expired; reconnect or launch a new session from the portal. |
| Python works over SSH but not in browser VS Code | Verify the setup file activates the same environment before editor launch; check the ITS environment compatibility guidance below. |
| Codex cannot run a command | Read its exact error. Do not automatically disable sandboxing or grant full access; first distinguish environment, proxy, authentication, and command-permission failures. |

For Codex troubleshooting, share the failed command and sanitized error, the
hostname/job state, interpreter version, and synthetic test result. Never share
authentication files, raw observations, or identifiers. Ask Codex to reproduce
problems against the fixture before escalating to the project owner.

Official references:

- [Great Lakes interactive allocations](https://documentation.its.umich.edu/node/4983)
- [Great Lakes defaults and limits](https://documentation.its.umich.edu/arc-hpc/greatlakes/user-guide/defaults-limits)
- [ITS VS Code, Open OnDemand, and proxy guidance](https://documentation.its.umich.edu/arc-hpc/open-ondemand/vs-code)
- [OpenAI Codex IDE extension](https://developers.openai.com/codex/ide)
