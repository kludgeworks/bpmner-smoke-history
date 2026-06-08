-- Copyright 2026 The Project Contributors
-- SPDX-License-Identifier: MIT
--
-- Per-provider stage-level token breakdown.
-- DuckDB infers stageBreakdown as a STRUCT (not MAP) from the JSON, so we unpivot the known
-- stage keys explicitly. This handles the two current stages: readiness and extraction.
-- If new stages are added, add them here.
SELECT
    provider,
    stage,
    min(stage_model) AS model,  -- deterministic; the model is constant within a (provider, stage)
    sum(prompt_tokens) AS total_prompt_tokens,
    sum(completion_tokens) AS total_completion_tokens,
    sum(llm_calls) AS total_llm_calls,
    count(*) AS samples
FROM (
    SELECT
        res.provider,
        'ProcessInputAssessment' AS stage,
        res.stageBreakdown."goal-ProcessInputAssessment".model AS stage_model,
        res.stageBreakdown."goal-ProcessInputAssessment".promptTokens AS prompt_tokens,
        res.stageBreakdown."goal-ProcessInputAssessment".completionTokens AS completion_tokens,
        res.stageBreakdown."goal-ProcessInputAssessment".llmCalls AS llm_calls
    FROM results AS res
    WHERE res.stageBreakdown IS NOT NULL
    UNION ALL
    SELECT
        res.provider,
        'ValidatedProcessContract' AS stage,
        res.stageBreakdown."goal-ValidatedProcessContract".model AS stage_model,
        res.stageBreakdown."goal-ValidatedProcessContract".promptTokens AS prompt_tokens,
        res.stageBreakdown."goal-ValidatedProcessContract".completionTokens AS completion_tokens,
        res.stageBreakdown."goal-ValidatedProcessContract".llmCalls AS llm_calls
    FROM results AS res
    WHERE res.stageBreakdown IS NOT NULL
) AS stages
GROUP BY provider, stage
ORDER BY provider, stage;
