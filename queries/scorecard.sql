-- Copyright 2026 The Project Contributors
-- SPDX-License-Identifier: MIT
--
-- Per-provider scorecard over the `signal_results` view (created by render_dashboard._load).
-- runId (the dispatching Actions run id, stamped by consolidate) is the canonical per-run key.
SELECT
    provider,
    -- The full served-model family. servedModel is itself a comma-joined string per row, so the renderer
    -- splits and de-dupes the individual models; array_agg(DISTINCT …) keeps the per-render set stable.
    array_agg(DISTINCT servedModel) FILTER (WHERE servedModel IS NOT NULL) AS served_models,
    count(DISTINCT runId) AS runs,
    round(100.0 * avg(CASE WHEN outcome = 'pass' THEN 1 ELSE 0 END), 1) AS pass_pct,
    sum(CASE WHEN outcome = 'fail' THEN 1 ELSE 0 END) AS fails,
    round(sum(costUsd) / nullif(count(DISTINCT runId), 0), 4) AS cost_per_run,
    sum(coalesce(promptTokens, 0) + coalesce(completionTokens, 0)) AS tokens,
    bool_or(costKnown IS DISTINCT FROM 'priced') AS cost_caveat
FROM signal_results
WHERE NOT is_no_signal
GROUP BY provider
ORDER BY provider;
