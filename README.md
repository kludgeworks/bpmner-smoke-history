# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 87.0% average pass rate · 186 total failures · 34 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.4%, llama 94.4%, openai 91%, deepseek 90.6%, anthropic 74.4%, gemini 72.2%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.4% | 3 | $0.4774 | 30.35M | `mistral-large-2411, mistral-small-2506` |
| `llama` | `█████████████▎` 94.4% | 27 | $0.2290 | 21.80M | `meta-llama/llama-3.3-70b-instruct` |
| `openai` | `████████████▊░` 91.0% | 47 | n/a | 22.86M | `gpt-4.1, gpt-4.1-mini` |
| `deepseek` | `████████████▋░` 90.6% | 42 | $0.0498 | 24.64M | `deepseek-chat` |
| `anthropic` | `██████████▍░░░` 74.4% | 4 | n/a | 7.16M | `claude-haiku-4-5, claude-sonnet-4-6` |
| `gemini` | `██████████▏░░░` 72.2% | 63 | n/a | 19.80M | `gemini-2.5-flash, gemini-2.5-pro` |

_\* `openai`, `anthropic`, `gemini` cost is `n/a` — provider has no configured pricing._

</details>

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/latency-trend-dark.svg">
  <img alt="Average LLM latency by provider over runs — llama highest, deepseek lowest" src="assets/smoke-health/latency-trend-light.svg" width="760">
</picture>

## Cost per test

> [!CAUTION]
> Cost is normalised **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable. Unpriced or no-signal points are excluded.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/cost-trend-dark.svg">
  <img alt="Cost per test by provider over runs — anthropic highest, deepseek lowest" src="assets/smoke-health/cost-trend-light.svg" width="760">
</picture>

## Token split — readiness vs extraction

_Tokens spent in the cheap readiness gatekeeper (`ProcessInputAssessment`) vs the expensive extraction stage (`ValidatedProcessContract`), per provider._

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/token-split-dark.svg">
  <img alt="Token split by provider — extraction dominates for 6 of 6 providers (readiness vs extraction tokens)" src="assets/smoke-health/token-split-light.svg" width="760">
</picture>

## Failure categories

> [!TIP]
> `deterministic` = harness/config failure (e.g. context load) · `classification` = the model produced a wrong answer · `infra` = timeout/transport. This separates _"the harness broke"_ from _"the model struggled."_

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/failure-split-dark.svg">
  <img alt="Failure categories by provider — gemini has the most failures (63)" src="assets/smoke-health/failure-split-light.svg" width="760">
</picture>

<details>
<summary><b>Failure detail</b> — counts, share & sample signatures</summary>

| Provider | Category | Failures | % of fails | Sample signature |
|---|---|--:|--:|---|
| `gemini` | deterministic | 59 | 93.7 | `business rule task()::429 - [{` |
| `openai` | deterministic | 43 | 91.5 | `business rule task()::429 - {` |
| `deepseek` | classification | 39 | 92.9 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | classification | 23 | 85.2 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 100.0 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | classification | 4 | 8.5 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `gemini` | classification | 4 | 6.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | deterministic | 3 | 11.1 | `event-based gateway()::RECEIVE (act-wait-for-response) requires messageName` |
| `deepseek` | deterministic | 3 | 7.1 | `escalation end()::TIMER (boundaryEvent) requires detail` |
| `mistral` | infra | 2 | 66.7 | `terminate end()::terminate end() timed out after 240 seconds` |
| `mistral` | deterministic | 1 | 33.3 | `event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind` |
| `llama` | infra | 1 | 3.7 | `exclusive gateway()::exclusive gateway() timed out after 240 seconds` |

</details>

## Flaky tests

> [!WARNING]
> Fails **across providers** ⇒ the test or prompt is suspect. Fails on **one provider** ⇒ a model limit.

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `error boundary event()` | `████████▉░░░` 36.9% | 5 — anthropic, deepseek, gemini, llama, openai | 84 |
| `standard loop activity()` | `███▍░░░░░░░░` 14.3% | 3 — deepseek, gemini, openai | 84 |
| `parallel gateway()` | `███▎░░░░░░░░` 13.4% | 2 — gemini, llama | 82 |
| `escalation end()` | `███▏░░░░░░░░` 13.1% | 3 — deepseek, gemini, openai | 84 |
| `event-based gateway()` | `██▉░░░░░░░░░` 12.0% | 2 — llama, openai | 83 |
| `escalation boundary event()` | `██▉░░░░░░░░░` 11.8% | 4 — anthropic, deepseek, gemini, openai | 85 |

<details>
<summary>28 more flaky tests (≤ 11.4% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `intermediate signal throw()` | `██▊░░░░░░░░░` 11.4% | 3 — gemini, llama, openai | 79 |
| `signal end()` | `██▍░░░░░░░░░` 10.1% | 4 — deepseek, gemini, llama, openai | 79 |
| `business rule task()` | `█▉░░░░░░░░░░` 7.6% | 2 — gemini, openai | 79 |
| `data objects and stores()` | `█▉░░░░░░░░░░` 7.6% | 2 — gemini, openai | 79 |
| `manual task()` | `█▉░░░░░░░░░░` 7.6% | 2 — gemini, openai | 79 |
| `message start()` | `█▉░░░░░░░░░░` 7.6% | 2 — gemini, openai | 79 |
| `sequential multi-instance activity()` | `█▉░░░░░░░░░░` 7.6% | 2 — gemini, openai | 79 |
| `timer start()` | `█▉░░░░░░░░░░` 7.6% | 2 — gemini, openai | 79 |
| `intermediate message throw()` | `█▊░░░░░░░░░░` 7.2% | 4 — deepseek, gemini, llama, openai | 83 |
| `exclusive gateway()` | `█▏░░░░░░░░░░` 4.8% | 3 — gemini, llama, openai | 84 |
| `intermediate escalation throw()` | `▉░░░░░░░░░░░` 3.6% | 3 — deepseek, llama, openai | 83 |
| `message end()` | `▉░░░░░░░░░░░` 3.6% | 2 — gemini, openai | 83 |
| `receive task()` | `▉░░░░░░░░░░░` 3.6% | 2 — gemini, openai | 83 |
| `script task()` | `▉░░░░░░░░░░░` 3.6% | 2 — gemini, openai | 84 |
| `signal start()` | `▉░░░░░░░░░░░` 3.6% | 2 — gemini, openai | 83 |
| `terminate end()` | `▉░░░░░░░░░░░` 3.6% | 2 — mistral, openai | 83 |
| `parallel multi-instance activity()` | `▉░░░░░░░░░░░` 3.5% | 3 — deepseek, gemini, openai | 85 |
| `call activity()` | `▋░░░░░░░░░░░` 2.7% | 2 — gemini, openai | 73 |
| `embedded subprocess()` | `▋░░░░░░░░░░░` 2.4% | 2 — gemini, openai | 85 |
| `event subprocess()` | `▋░░░░░░░░░░░` 2.4% | 2 — gemini, mistral | 82 |
| `exclusive gateway with default branch()` | `▋░░░░░░░░░░░` 2.4% | 2 — gemini, openai | 85 |
| `send task()` | `▋░░░░░░░░░░░` 2.4% | 2 — gemini, openai | 85 |
| `timer boundary event()` | `▋░░░░░░░░░░░` 2.4% | 2 — gemini, mistral | 82 |
| `error end()` | `▎░░░░░░░░░░░` 1.2% | 1 — gemini | 82 |
| `inclusive gateway()` | `▎░░░░░░░░░░░` 1.2% | 1 — openai | 83 |
| `pools and lanes from distinct actors()` | `▎░░░░░░░░░░░` 1.2% | 1 — gemini | 82 |
| `service task()` | `▎░░░░░░░░░░░` 1.2% | 1 — openai | 83 |
| `user task()` | `▎░░░░░░░░░░░` 1.2% | 1 — openai | 83 |

</details>

## LLM efficiency

> [!IMPORTANT]
> `mistral` is the outlier — median 5 calls/test but a P95 of 21 and a max of **69**, suggesting retry or tool-loop storms. Every other provider sits at a median of 5.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/llm-efficiency-dark.svg">
  <img alt="LLM calls per test by provider — mistral spread is far wider than the rest" src="assets/smoke-health/llm-efficiency-light.svg" width="760">
</picture>

---

<sub>📖 How this repo works — ingest, querying & setup → [`ABOUT.md`](ABOUT.md) · Regenerated every run by `render_dashboard.py`. Machine-managed — do not edit by hand.</sub>
