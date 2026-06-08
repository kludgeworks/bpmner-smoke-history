-- Copyright 2026 The Project Contributors
-- SPDX-License-Identifier: MIT
--
-- Per-provider LLM latency over time.
-- Each row is one (runId, provider) combination for charting latency trends.
SELECT
    runId,
    provider,
    min(ts) AS run_ts,
    round(avg(llmTimeMs), 0) AS avg_llm_time_ms,
    round(percentile_cont(0.95) WITHIN GROUP (ORDER BY llmTimeMs), 0) AS p95_llm_time_ms,
    count(*) AS samples
FROM results
GROUP BY runId, provider
ORDER BY run_ts, provider;
