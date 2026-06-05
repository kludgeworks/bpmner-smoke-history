# bpmner-smoke-history

Append-only history of [bpmner](https://github.com/kludgeworks/bpmner) live-LLM **smoke-test** results.

Each run of bpmner's `smoke-tests` workflow appends one consolidated file:

```
data/year=YYYY/month=MM/run-<run_id>.jsonl
```

with one row per *(provider, test-method)* — outcome, per-test cost/tokens, `attempts`, and
change-detection fingerprints. Written by bpmner's `publish-smoke-history` job via a GitHub App
(Contents: write). **Do not edit by hand** — it is machine-managed, append-only.

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

The rendered provider scorecard + flaky-test ranking live in bpmner's pinned **"Smoke Health"**
issue. The render / query / consolidation scripts are in
[`bpmner:tools/smoke-history/`](https://github.com/kludgeworks/bpmner/tree/main/tools/smoke-history).
