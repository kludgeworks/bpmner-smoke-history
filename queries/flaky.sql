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
    string_agg(DISTINCT provider, ', ') FILTER (WHERE outcome = 'fail') AS failed_on,
    count(*) AS samples
FROM results
GROUP BY testMethod
HAVING count(DISTINCT provider) FILTER (WHERE outcome = 'fail') > 0
ORDER BY providers_failed DESC, fail_pct DESC;
