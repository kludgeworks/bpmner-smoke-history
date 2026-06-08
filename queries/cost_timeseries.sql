-- Copyright 2026 The Project Contributors
-- SPDX-License-Identifier: MIT
--
-- Per-provider cost over time.
-- Each row is one (runId, provider) combination so downstream can chart cost trends.
-- The `results` view already filters to runComplete rows.
SELECT
    runId,
    provider,
    min(ts) AS run_ts,
    round(sum(costUsd), 6) AS total_cost,
    bool_and(costKnown = 'priced') AS cost_known,
    sum(coalesce(promptTokens, 0) + coalesce(completionTokens, 0)) AS run_tokens,
    round(avg(llmCallCount), 1) AS avg_llm_calls,
    count(*) AS tests_in_run
FROM results
GROUP BY runId, provider
ORDER BY run_ts, provider;
