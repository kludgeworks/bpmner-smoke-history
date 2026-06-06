-- Copyright 2026 The Project Contributors
-- SPDX-License-Identifier: MIT
--
-- Per-provider scorecard over the `results` view (created by render_dashboard._load).
-- runId (the dispatching Actions run id, stamped by consolidate) is the canonical per-run key.
-- TODO (Phase 2.3): split by served model, not just provider.
SELECT
    provider,
    any_value(servedModel) AS model,
    count(DISTINCT runId) AS runs,
    round(100.0 * avg(CASE WHEN outcome = 'pass' THEN 1 ELSE 0 END), 1) AS pass_pct,
    sum(CASE WHEN outcome = 'fail' THEN 1 ELSE 0 END) AS fails,
    round(sum(costUsd) / nullif(count(DISTINCT runId), 0), 4) AS cost_per_run,
    sum(coalesce(promptTokens, 0) + coalesce(completionTokens, 0)) AS tokens,
    bool_or(costKnown IS DISTINCT FROM 'priced') AS cost_caveat
FROM results
GROUP BY provider
ORDER BY provider;
