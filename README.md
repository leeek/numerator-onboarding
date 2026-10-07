# Numerator onboarding on Great Lakes

A small metadata-first Python exercise for University of Michigan faculty and
researchers. Local development uses invented data only; no real Numerator data
is included or needed. Requires Python 3.10 or newer.

**New here?** Follow the setup instructions below, starting with prerequisites.
**Already set up?** Jump to the [daily browser VS Code workflow](#great-lakes-browser-vs-code-daily-workflow)
or [choosing resources and batch jobs](#choosing-resources-and-batch-jobs).

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
  If you do not have an account, create one first.

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
> Use browser VS Code through Open OnDemand with 18 hours, 2 cores, and 8 GB.
> Help me create a private copy using the GitHub template and clone my copy onto
> Great Lakes. Use ~/numerator-onboarding as the checkout folder for this setup.
> Help configure Git authentication if needed without requesting my credentials.
> Keep Python work on an allocated compute node and use synthetic data only during
> setup. Do not
> access real Numerator data, overwrite existing work, or change account-security
> settings automatically. Let me handle authentication and required approvals.
> Finish by checking the node/job, Python environment, tests, synthetic catalog,
> and Codex command execution. Show me how to reconnect and stop the allocation.

If Computer Use is unavailable, follow the manual instructions below and ask your
assistant to explain one step or error at a time.

See OpenAI's [Computer Use setup](https://learn.chatgpt.com/docs/computer-use) and
[desktop/browser task guide](https://learn.chatgpt.com/use-cases/use-your-computer-with-codex).

## Create your own project

This is a public GitHub template. **Sign in to GitHub first** (create a free
GitHub account if you do not have one), then return to
[this repository](https://github.com/leeek/numerator-onboarding). To start your own
research project, click **Use this template → Create a new repository**, give your
project a name, and choose **Private**. Copy your new repository's **Code → HTTPS**
URL for the clone command below. This gives you an independent project; later
starter updates are not applied automatically.

The commands below put your project in `~/numerator-onboarding` on Great Lakes,
regardless of its GitHub name. If you use a different folder, update the paths
throughout the guide, including the editor setup file. Keep research data outside
Git, even in a private repository.

## Manual setup: overview

If using the assistant above, let it work through these steps with you; this is
also the reference for doing setup yourself. Complete **One-time cluster checkout and Python environment**
below, then use **Great Lakes browser VS Code** for everyday work. Local practice
is optional. The initial SSH setup creates files and an environment; daily work
uses the browser and does not require configuring Remote-SSH.

## One-time cluster checkout and Python environment

Replace `YOUR_UNIQNAME` and `YOUR_SLURM_ACCOUNT` below with your own values. The
Slurm account is an allocation/billing account, not necessarily your uniqname.

On your laptop, in a terminal:

```sh
ssh YOUR_UNIQNAME@greatlakes.arc-ts.umich.edu
```

Complete password/MFA authentication yourself. On the Great Lakes login node,
clone your private repository once. GitHub authentication is separate from your
U-M login; GitHub account passwords do not work for Git HTTPS authentication.
Use an existing authenticated Git setup or ask Codex to help configure it without
sharing tokens.

Replace `YOUR_REPOSITORY_HTTPS_URL` with the URL you copied from **your private
repository**, and run these commands from your home directory. If
`~/numerator-onboarding` already exists, use that checkout if it is your project;
ask Codex to inspect it before proceeding if you are unsure.

```sh
cd ~
git clone YOUR_REPOSITORY_HTTPS_URL numerator-onboarding
cd numerator-onboarding
git log -1 --oneline
```

Request an 18-hour interactive allocation:

```sh
salloc --account=YOUR_SLURM_ACCOUNT --partition=standard --nodes=1 --ntasks=1 --cpus-per-task=2 --mem=8G --time=18:00:00
hostname
echo "$SLURM_JOB_ID"
squeue -u "$USER"
```

Wait for the allocation to start. Great Lakes' `salloc` normally places the shell
on a compute node. Confirm the hostname matches your job's node, not `gl-login*`.
If the shell remains on a login node after allocation, use `srun --pty bash -l`
and check again. The resources above are a starting point for development and
metadata work, not a recommendation for full data scans. Keep the session open;
18 hours is the allocation limit, not a guarantee against connection loss or
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

Use `python/3.12.1` consistently when creating the environment and in the editor
setup file below. Specifying the version avoids depending on a changing cluster
default. Loading a different module does not upgrade an existing `.venv`.

## Great Lakes browser VS Code: daily workflow

The recommended editor is **Visual Studio Code through Great Lakes Open OnDemand**,
with the official Codex extension running in the same compute allocation. Your
browser is the interface; Python and Codex's commands run on Great Lakes. Local
work remains synthetic-only. First create the cluster checkout and environment
using the explicit one-time commands above. For later sessions, reuse the setup
file and installed extensions; start at step 2. If a session is still running,
reconnect through **My Interactive Sessions** instead of launching another job.

1. **First session only:** create `~/numerator-ood-setup.sh` on Great Lakes using
   a text editor. Its contents should be the following (replace the environment path and use the same Python
   module that created your environment):

   ```sh
   source /etc/profile.d/http_proxy.sh
   module load python/3.12.1
   source /home/YOUR_UNIQNAME/numerator-onboarding/.venv/bin/activate
   ```

   This short file is sourced **before the editor starts**, so extensions inherit
   the compute-node internet proxy and Python environment.

2. Open [Great Lakes Open OnDemand](https://greatlakes.arc-ts.umich.edu), sign in,
   and choose **Interactive Apps → Visual Studio Code**. Request your own Slurm
   account, `standard` partition, **18 hours**, **2 cores**, and **8 GB total memory**.
   Select code-server **4.112.0** if available. Set **Source this
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
4. **First session only:** open **Extensions**, search for **Codex**, and install **Codex – OpenAI's coding
   agent**, publisher **openai**, identifier **openai.chatgpt**. Open its sidebar.
   Choose ChatGPT sign-in using a **device code**. Open the displayed authentication
   link in your laptop browser and enter the code. If asked, enable device-code
   sign-in in your ChatGPT account's Security settings yourself, then retry.
   Keep authentication codes and credential files out of this repository.
   Installation normally persists in your Great Lakes home directory, so you do
   not need to reinstall for each allocation or compute node. On later sessions,
   open the Codex sidebar directly; sign in again only if prompted. Each researcher
   installs under their own Great Lakes account.
5. **First session or troubleshooting:** ask Codex to verify the installation
   using the prompt below. Keep execution in this workspace, rather than delegating
   the task to a cloud environment:

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

## Choosing resources and batch jobs

Browser VS Code already runs inside a Slurm compute allocation. It is suitable
for writing code, debugging, inspecting metadata, and exploring a small, explicitly
filtered part of the data. You can request more resources for interactive work,
but a long, repeatable cleaning run is usually better as a separate batch job.

### What can I change when launching VS Code?

Set these fields in the Open OnDemand launch form before starting a new session:

| Setting | Starter default | When to change it |
| --- | --- | --- |
| Slurm account | Your authorized account | Use the allocation that supports your project. |
| Partition | `standard` | Keep this for ordinary Python/Parquet work; special partitions require a specific need and appropriate access. |
| Number of hours | **18** | Request enough time for your session. This is a maximum duration, not a promise of immediate availability. |
| Number of cores | **2** | Increase when your query or code actually uses parallel workers/threads. Extra cores do not automatically speed up a serial Python loop. |
| Memory (GB) | **8 GB total** | Increase when a measured pilot needs more memory, especially for joins, sorts, and large intermediate results. |
| Source this setup file | Your `numerator-ood-setup.sh` | Change when switching project environments; keep its Python module and environment path consistent. |

Choose larger resource requests based on a small trial run of your workload.
Larger requests can wait longer in the queue and reserve more shared resources.
Save your work
and launch a new allocation to change the resource request; changing a Python
setting does not enlarge the current Slurm allocation. Stop sessions when finished.

### Interactive or batch?

| Task | Suggested approach |
| --- | --- |
| Develop a cleaning rule and inspect aggregate checks | Browser VS Code on one explicitly selected partition or other bounded input. |
| Debug a join that needs more memory while inspecting intermediate results | A larger interactive session, sized from a pilot. |
| Clean many months, rebuild a large derived dataset, or run unattended | A Python script submitted as a Slurm batch job. |
| Repeat the same independent operation across many partitions | Start with one batch job; consider a job array after validating the operation. |

For batch work, continue editing in VS Code, but submit a separate job with
`sbatch`. Its CPU, memory, and time requests are independent of the editor's
allocation. Slurm runs it on allocated compute resources and writes its logs;
it does not depend on keeping the editor session alive. Keep the account, paths,
and resource requests visible in an ordinary `.sbatch` file. Do not run a large
cleaning script directly on a login node. Store real-data outputs and potentially
sensitive logs outside this repository; see [where to store cleaned tables](#where-to-store-cleaned-tables).

Before scaling up, select only needed partitions and columns, measure elapsed time
and peak memory, and leave headroom. Compressed Parquet file size is not the memory
requirement. Configure DuckDB/Arrow workers to respect allocated cores and leave
memory for Python and the editor. A `LIMIT` alone does not guarantee a small scan.
The exact resources and batching strategy belong in each research project's code
and notes, rather than being fixed for everyone in this starter.

A useful request to Codex once your small pilot works:

> Read AGENTS.md and inspect my cleaning script. Help me turn it into a Slurm batch
> job with explicit account, input/output paths, CPU, memory, and time requests.
> First propose a bounded pilot and explain how to measure its resource use. Use
> those measurements to recommend a full-run request; do not submit the full scan
> yet. Keep real-data outputs and logs outside Git and do not print observations
> or identifiers. Show the commands to submit, monitor, and cancel the job.

References: [Slurm batch submission](https://slurm.schedmd.com/sbatch.html),
[job accounting and memory statistics](https://slurm.schedmd.com/sacct.html), and
[Great Lakes limits](https://documentation.its.umich.edu/arc-hpc/greatlakes/user-guide/defaults-limits).

## Where to store cleaned tables

For cleaned or derived tables you intend to keep, use **approved project storage
accessible from Great Lakes**, usually your research group's **Turbo allocation**.
Before starting a substantial cleaning run, confirm the output location, available
space, and collaborator permissions with your project owner or Ross Research Computing. Access to the shared Numerator source does not
automatically provide a project output allocation.

| Location | What belongs there |
| --- | --- |
| Home directory | Code checkout, Python environment, and small configuration files. |
| Scratch | Temporary intermediates and spill files that can be regenerated. |
| Approved project storage (typically Turbo) | Retained cleaned tables and other derived research datasets. |
| Your GitHub repository | Code and documentation needed to reproduce the work, not Numerator data or derived tables. |

Keep outputs separate from `/nfs/turbo/bus-kbaldata/Numerator`; treat that shared
source as read-only for your workflow. Configure an explicit output path outside
the Git checkout. Do not use scratch as the only copy of important results:
Great Lakes documents an 80 GB home quota and scratch deletion after 60 days
without access. Confirm your project storage's retention and data-protection
arrangements rather than assuming every volume has the same configuration.

See [Great Lakes storage guidance](https://documentation.its.umich.edu/arc-hpc/greatlakes/user-guide/defaults-limits)
and the [Turbo storage guide](https://documentation.its.umich.edu/arc-storage/turbo).

## First real-data check: one Parquet footer

Once your Numerator access is approved and the synthetic checks pass, paste this
prompt into **Codex inside Great Lakes browser VS Code**:

> Read AGENTS.md. Confirm that the hostname and Slurm job match an active compute
> allocation. Use this Great Lakes workspace and .venv/bin/python, with
> NUMERATOR_ROOT=/nfs/turbo/bus-kbaldata/Numerator. Find one Parquet file under
> people_table using incremental directory traversal that stops at the first
> match; do not build a full file listing or run the full catalog. Use PyArrow to
> read only that file's footer. Report its row count and column names/types, without
> printing its path, column statistics, identifiers, or observation values. Do not
> read data rows, modify the source data, or save data or metadata in Git. If access
> fails, explain the failing step and what I need to resolve. Explain what the
> successful check tells me and suggest a small next step without running a scan.

This checks access and the structure of one file. It does not establish table-wide
row counts or schema consistency. The full catalog visits every matching file;
use it later in a compute allocation when you are ready for that metadata crawl.

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

With `NUMERATOR_ROOT` unset, this checkout defaults to the same synthetic fixture.

## Exercise 1: inspect before querying

Run `numerator-catalog` (equivalently `python -m numerator_onboarding.catalog`).
Its JSON output reports table names, Parquet file counts, row counts, compressed
file sizes, and column names and types. It treats each directory directly under
the data root as a table and finds Parquet files in its subdirectories. Directories
without Parquet files are skipped.

Row counts come from Parquet footers without reading observations. File sizes
describe disk storage, not the memory needed for analysis. Every file is inspected,
so cataloging a large dataset can still take time. An unreadable or invalid file
stops the catalog rather than producing an incomplete result.

If column definitions differ between files, the catalog reports each version.
Check these differences before writing queries. Partition labels stored only in
directory names, such as `year` or `month`, are not included as columns. The catalog
prints column definitions, never observation values or file paths.

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
Unlike the catalog, this query scans selected column data. A small result or a `LIMIT` does not guarantee a small scan.
Before adapting it to real data, inspect the actual schema and add appropriate
partition filters. The illustrative `channel` and `spend` fields are not promised
to exist in the real tables.

## Working with real data

After the [one-file metadata check](#first-real-data-check-one-parquet-footer)
succeeds, continue in Codex inside Great Lakes browser VS Code:

1. **Describe your research task.** Tell Codex the population, time period, and
   output you want—for example, a household-by-month table of spending in a
   particular category. Explain any definitions you already have and ask it to
   flag unresolved choices.
2. **Understand the relevant tables.** Consult the documentation in
   `0-Data_Description_and_Schemas` and inspect metadata for the tables you need.
   Confirm what each row represents, which variables define your sample, and how
   tables join. Do not assume the synthetic example's columns exist in real data.
3. **Build a small pilot.** Select explicit files or partitions and only the
   columns needed. Check missingness, duplicates, and row counts before and after
   joins using aggregate summaries. A small result or `LIMIT` alone does not make
   a query a small scan. Measure runtime and memory before expanding the input.
4. **Save and scale.** Store derived tables in
   [project storage](#where-to-store-cleaned-tables), with code and documentation
   committed and pushed to your private GitHub repository. For larger or repeatable
   runs, follow [the batch-job guidance](#choosing-resources-and-batch-jobs).

To start, replace the bracketed text and paste this into the remote Codex sidebar:

> Read AGENTS.md. My research task is [describe the population, time period, and
> desired output]. Confirm this workspace is on an active Great Lakes compute
> allocation. Use .venv/bin/python and set
> NUMERATOR_ROOT=/nfs/turbo/bus-kbaldata/Numerator for real-data work. Consult the
> data documentation and relevant Parquet metadata to identify candidate tables,
> variables, and join keys. Explain what each row represents and flag definitions
> that need my input. Propose a small pilot with explicit input files or partitions,
> columns, aggregate validation checks, and a project-storage output path. Ask me
> about missing research definitions or storage access. Show me the pilot plan
> before reading observations; do not run a full scan. Keep observations and
> identifiers out of logs and chat, and keep data outside the Git repository.

**Optional: catalog the full dataset.** You do not need a full inventory before
working with a few relevant tables. If you need one, this command reads the footer
of every Parquet file under the table directories, which can take time. Run it
from your repository folder inside a compute allocation:

```sh
NUMERATOR_ROOT=/nfs/turbo/bus-kbaldata/Numerator .venv/bin/python -m numerator_onboarding.catalog
```

Real data stays on Great Lakes. Throughout your work:

- **Never commit Numerator data. Never copy raw Numerator observations into this repo.**
- Develop against synthetic data locally. Do not mount, download, or access real
  Numerator data during local development.
- Do not print household/person identifiers in logs, notebooks, or error reports.
  Do not save row-level extracts here. Review aggregates before sharing them.
- Run large real-data scans on allocated Great Lakes compute nodes, **not login
  nodes**. For a large metadata crawl, use a compute allocation as well.
- `.gitignore` blocks common data formats but cannot enforce these rules. Its
  fixture exception is for generated synthetic data only. Review staged files.

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
