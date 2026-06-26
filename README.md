# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 88.0% average pass rate · 183 total failures · 34 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.4%, llama 94.4%, deepseek 90.7%, openai 90.7%, anthropic 77.9%, gemini 74.7%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.4% | 3 | $0.4741 | 29.21M | `mistral-large-2411, mistral-small-2506` |
| `llama` | `█████████████▎` 94.4% | 26 | $0.2293 | 21.06M | `meta-llama/llama-3.3-70b-instruct` |
| `deepseek` | `████████████▊░` 90.7% | 40 | $0.0500 | 23.84M | `deepseek-chat` |
| `openai` | `████████████▊░` 90.7% | 47 | n/a | 22.13M | `gpt-4.1, gpt-4.1-mini` |
| `anthropic` | `██████████▉░░░` 77.9% | 4 | n/a | 7.16M | `claude-haiku-4-5, claude-sonnet-4-6` |
| `gemini` | `██████████▌░░░` 74.7% | 63 | n/a | 19.80M | `gemini-2.5-flash, gemini-2.5-pro` |

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
| `deepseek` | classification | 37 | 92.5 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | classification | 22 | 84.6 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 100.0 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | classification | 4 | 8.5 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `gemini` | classification | 4 | 6.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | deterministic | 3 | 11.5 | `event-based gateway()::RECEIVE (act-wait-for-response) requires messageName` |
| `deepseek` | deterministic | 3 | 7.5 | `escalation end()::TIMER (boundaryEvent) requires detail` |
| `mistral` | infra | 2 | 66.7 | `terminate end()::terminate end() timed out after 240 seconds` |
| `mistral` | deterministic | 1 | 33.3 | `event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind` |
| `llama` | infra | 1 | 3.8 | `exclusive gateway()::exclusive gateway() timed out after 240 seconds` |

</details>

## Flaky tests

> [!WARNING]
> Fails **across providers** ⇒ the test or prompt is suspect. Fails on **one provider** ⇒ a model limit.

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `error boundary event()` | `████████▉░░░` 37.0% | 5 — anthropic, deepseek, gemini, llama, openai | 81 |
| `escalation end()` | `███▎░░░░░░░░` 13.6% | 3 — deepseek, gemini, openai | 81 |
| `standard loop activity()` | `███▎░░░░░░░░` 13.6% | 3 — deepseek, gemini, openai | 81 |
| `parallel gateway()` | `███░░░░░░░░░` 12.7% | 2 — gemini, llama | 79 |
| `event-based gateway()` | `███░░░░░░░░░` 12.5% | 2 — llama, openai | 80 |
| `escalation boundary event()` | `██▉░░░░░░░░░` 12.2% | 4 — anthropic, deepseek, gemini, openai | 82 |

<details>
<summary>28 more flaky tests (≤ 11.8% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `intermediate signal throw()` | `██▉░░░░░░░░░` 11.8% | 3 — gemini, llama, openai | 76 |
| `signal end()` | `██▌░░░░░░░░░` 10.5% | 4 — deepseek, gemini, llama, openai | 76 |
| `business rule task()` | `█▉░░░░░░░░░░` 7.9% | 2 — gemini, openai | 76 |
| `data objects and stores()` | `█▉░░░░░░░░░░` 7.9% | 2 — gemini, openai | 76 |
| `manual task()` | `█▉░░░░░░░░░░` 7.9% | 2 — gemini, openai | 76 |
| `message start()` | `█▉░░░░░░░░░░` 7.9% | 2 — gemini, openai | 76 |
| `sequential multi-instance activity()` | `█▉░░░░░░░░░░` 7.9% | 2 — gemini, openai | 76 |
| `timer start()` | `█▉░░░░░░░░░░` 7.9% | 2 — gemini, openai | 76 |
| `intermediate message throw()` | `█▊░░░░░░░░░░` 7.5% | 4 — deepseek, gemini, llama, openai | 80 |
| `exclusive gateway()` | `█▏░░░░░░░░░░` 4.9% | 3 — gemini, llama, openai | 81 |
| `intermediate escalation throw()` | `▉░░░░░░░░░░░` 3.8% | 3 — deepseek, llama, openai | 80 |
| `message end()` | `▉░░░░░░░░░░░` 3.8% | 2 — gemini, openai | 80 |
| `receive task()` | `▉░░░░░░░░░░░` 3.8% | 2 — gemini, openai | 80 |
| `signal start()` | `▉░░░░░░░░░░░` 3.8% | 2 — gemini, openai | 80 |
| `terminate end()` | `▉░░░░░░░░░░░` 3.8% | 2 — mistral, openai | 80 |
| `parallel multi-instance activity()` | `▉░░░░░░░░░░░` 3.7% | 3 — deepseek, gemini, openai | 82 |
| `script task()` | `▉░░░░░░░░░░░` 3.7% | 2 — gemini, openai | 81 |
| `call activity()` | `▊░░░░░░░░░░░` 2.9% | 2 — gemini, openai | 70 |
| `event subprocess()` | `▋░░░░░░░░░░░` 2.5% | 2 — gemini, mistral | 79 |
| `timer boundary event()` | `▋░░░░░░░░░░░` 2.5% | 2 — gemini, mistral | 79 |
| `embedded subprocess()` | `▋░░░░░░░░░░░` 2.4% | 2 — gemini, openai | 82 |
| `exclusive gateway with default branch()` | `▋░░░░░░░░░░░` 2.4% | 2 — gemini, openai | 82 |
| `send task()` | `▋░░░░░░░░░░░` 2.4% | 2 — gemini, openai | 82 |
| `error end()` | `▎░░░░░░░░░░░` 1.3% | 1 — gemini | 79 |
| `inclusive gateway()` | `▎░░░░░░░░░░░` 1.3% | 1 — openai | 80 |
| `pools and lanes from distinct actors()` | `▎░░░░░░░░░░░` 1.3% | 1 — gemini | 79 |
| `service task()` | `▎░░░░░░░░░░░` 1.3% | 1 — openai | 80 |
| `user task()` | `▎░░░░░░░░░░░` 1.3% | 1 — openai | 80 |

</details>

## LLM efficiency

> [!IMPORTANT]
> `mistral` is the outlier — median 5 calls/test but a P95 of 23 and a max of **69**, suggesting retry or tool-loop storms. Every other provider sits at a median of 5.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/llm-efficiency-dark.svg">
  <img alt="LLM calls per test by provider — mistral spread is far wider than the rest" src="assets/smoke-health/llm-efficiency-light.svg" width="760">
</picture>

---

<sub>📖 How this repo works — ingest, querying & setup → [`ABOUT.md`](ABOUT.md) · Regenerated every run by `render_dashboard.py`. Machine-managed — do not edit by hand.</sub>
