-- Copyright 2026 The Project Contributors
-- SPDX-License-Identifier: MIT
--
-- Failure category breakdown per provider.
-- Shows what kinds of failures dominate each provider and a sample signature for debugging.
SELECT
    provider,
    failureCategory,
    count(*) AS failures,
    round(
        100.0 * count(*)
        / nullif(sum(count(*)) OVER (PARTITION BY provider), 0),
        1
    ) AS pct_of_provider_failures,
    -- min() (not any_value) so the representative signature is deterministic across renders.
    min(failureSignature) AS sample_signature
FROM results
WHERE outcome = 'fail'
GROUP BY provider, failureCategory
ORDER BY provider ASC, failures DESC;
