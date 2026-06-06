# bpmner-smoke-history

Append-only history of [bpmner](https://github.com/kludgeworks/bpmner) live-LLM **smoke-test** results,
plus the tooling that ingests and renders it. The rolling dashboard is **[SMOKE_HEALTH.md](SMOKE_HEALTH.md)**.

## Data

Each bpmner smoke run appends one consolidated file:

```
data/year=YYYY/month=MM/run-<run_id>.jsonl
```

one row per *(provider, test-method)* — outcome, per-test cost/tokens, and change-detection
fingerprints. **Machine-managed, append-only — do not edit by hand.**

## How it works

bpmner's CI *produces* the data; this repo *owns* ingest + rendering. The trigger is one-way —
bpmner dispatches ingest but cannot write here directly:

1. Each bpmner smoke job uploads a `smoke-<provider>` artifact (`smoke-results.jsonl` + Bazel `test.xml`).
2. bpmner's `dispatch-smoke-history` job mints an **Actions: write** GitHub-App token and calls
   `gh workflow run ingest.yml` here with the source run id.
3. This repo's [`ingest`](.github/workflows/ingest.yml) workflow guards the (untrusted) inputs, pulls
   those artifacts (`download-artifact@v8`, **Actions: read** on bpmner), runs `consolidate.py` — joining
   `test.xml` for the authoritative post-retry outcome — renders the dashboard, and commits the new data
   file + `SMOKE_HEALTH.md` **as the App** (Contents: write), which bypasses the branch ruleset.

## Querying

Zero-server, with [DuckDB](https://duckdb.org):

```sql
SELECT provider,
       count(*) FILTER (WHERE outcome = 'fail') AS fails,
       count(*)                                AS rows
FROM read_json_auto('data/**/*.jsonl', format = 'newline_delimited', union_by_name := true)
WHERE runComplete
GROUP BY provider
ORDER BY fails DESC;
```

The queries the dashboard itself uses live in [`queries/`](queries/).

## Development

Tooling is managed by [mise](https://mise.jdx.dev) + [uv](https://docs.astral.sh/uv/):

```bash
mise install   # python, uv, duckdb, hk, …
uv sync        # python deps: duckdb (runtime) + pytest (dev); ruff/sqlfluff/shellcheck/shfmt are mise tools

uv run pytest                                          # tests
hk check --all                                         # ruff + sqlfluff + addlicense + actionlint
uv run python -m smoke_history.render_dashboard data   # render the dashboard from local data/
```

## Setup — the cross-repo GitHub App

The dispatch/ingest loop needs **one** GitHub App (org `kludgeworks`): **Actions: Read & write** +
**Contents: Read & write** + **Metadata: Read**, installed on **both** `bpmner` and `bpmner-smoke-history`.
Add its credentials:

- **this repo** (Settings → Secrets and variables → Actions): variable `APP_ID`, secret `APP_PRIVATE_KEY`
- **bpmner** (1Password): `op://bpmner/smoke-history-app/app-id` + `.../private-key`
