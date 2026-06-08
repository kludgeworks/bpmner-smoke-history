-- Copyright 2026 The Project Contributors
-- SPDX-License-Identifier: MIT
--
-- Per-provider distribution of LLM call counts.
-- Gives min/avg/median/p95/max/stddev so we can spot outlier runs.
SELECT
    provider,
    min(llmCallCount) AS min_calls,
    round(avg(llmCallCount), 1) AS avg_calls,
    percentile_cont(0.50) WITHIN GROUP (ORDER BY llmCallCount) AS median_calls,
    max(llmCallCount) AS max_calls,
    percentile_cont(0.95) WITHIN GROUP (ORDER BY llmCallCount) AS p95_calls,
    round(stddev(llmCallCount), 1) AS stddev_calls,
    count(*) AS samples
FROM results
GROUP BY provider
ORDER BY provider;
