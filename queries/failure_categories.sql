-- Copyright 2026 The Project Contributors
-- SPDX-License-Identifier: MIT
--
-- Failure category breakdown per provider.
-- Shows what kinds of failures dominate each provider and a sample signature for debugging.
SELECT
    provider,
    -- Bucket an absent category as infra (the catch-all transport/timeout class) rather than dropping
    -- the failure — the design's split has exactly three categories and every fail must land in one.
    coalesce(failureCategory, 'infra') AS failureCategory,
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
GROUP BY provider, coalesce(failureCategory, 'infra')
-- Surface the biggest failure buckets first; provider/category break ties so row order is deterministic.
ORDER BY failures DESC, pct_of_provider_failures DESC, provider ASC, failureCategory ASC;
