-- Copyright 2026 The Project Contributors
-- SPDX-License-Identifier: MIT
--
-- Tests that fail, ranked by how many providers they fail on.
-- Fails across many providers => test/prompt suspect; fails on one weak model => model limit.
-- No LIMIT here: the renderer caps the table and reports "...and N more".
SELECT
    testMethod,
    round(100.0 * avg(CASE WHEN outcome = 'fail' THEN 1 ELSE 0 END), 1) AS fail_pct,
    count(DISTINCT provider) FILTER (WHERE outcome = 'fail') AS providers_failed,
    string_agg(DISTINCT provider, ', ' ORDER BY provider) FILTER (WHERE outcome = 'fail') AS failed_on,
    count(*) AS samples
FROM signal_results
WHERE NOT is_no_signal
GROUP BY testMethod
HAVING count(DISTINCT provider) FILTER (WHERE outcome = 'fail') > 0
-- Rank by fail rate (the dashboard surfaces the worst offenders first); providers_failed and the
-- testMethod GROUP BY key break ties so the order — and the renderer's top-N cap — is deterministic.
ORDER BY fail_pct DESC, providers_failed DESC, testMethod ASC;
