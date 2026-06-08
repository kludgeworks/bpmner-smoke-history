-- Copyright 2026 The Project Contributors
-- SPDX-License-Identifier: MIT
--
-- Prompt fingerprint impact analysis.
-- Each row is a distinct promptFingerprint so we can see how prompt changes
-- correlate with pass rate and cost.
--
-- DORMANT: intentionally not wired into render_dashboard.py yet. It only becomes meaningful once
-- the prompt templates actually change between runs (today every recorded run shares one
-- fingerprint). Surface a "prompt change impact" section when fingerprints start to diverge.
SELECT
    promptFingerprint,
    min(ts) AS first_seen,
    max(ts) AS last_seen,
    count(DISTINCT runId) AS runs,
    round(100.0 * avg(CASE WHEN outcome = 'pass' THEN 1 ELSE 0 END), 1) AS pass_pct,
    round(avg(costUsd), 6) AS avg_cost,
    round(avg(coalesce(promptTokens, 0) + coalesce(completionTokens, 0)), 0) AS avg_tokens,
    count(DISTINCT provider) AS providers_tested
FROM results
GROUP BY promptFingerprint
ORDER BY first_seen;
