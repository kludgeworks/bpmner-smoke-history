# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 87.7% average pass rate · 184 total failures · 34 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.4%, llama 94.2%, deepseek 90.8%, openai 90.8%, anthropic 77%, gemini 74%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.4% | 3 | $0.4757 | 29.64M | `mistral-large-2411, mistral-small-2506` |
| `llama` | `█████████████▎` 94.2% | 27 | $0.2292 | 21.30M | `meta-llama/llama-3.3-70b-instruct` |
| `deepseek` | `████████████▊░` 90.8% | 40 | $0.0501 | 24.16M | `deepseek-chat` |
| `openai` | `████████████▊░` 90.8% | 47 | n/a | 22.40M | `gpt-4.1, gpt-4.1-mini` |
| `anthropic` | `██████████▊░░░` 77.0% | 4 | n/a | 7.16M | `claude-haiku-4-5, claude-sonnet-4-6` |
| `gemini` | `██████████▍░░░` 74.0% | 63 | n/a | 19.80M | `gemini-2.5-flash, gemini-2.5-pro` |

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
| `llama` | classification | 23 | 85.2 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 100.0 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | classification | 4 | 8.5 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `gemini` | classification | 4 | 6.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | deterministic | 3 | 11.1 | `event-based gateway()::RECEIVE (act-wait-for-response) requires messageName` |
| `deepseek` | deterministic | 3 | 7.5 | `escalation end()::TIMER (boundaryEvent) requires detail` |
| `mistral` | infra | 2 | 66.7 | `terminate end()::terminate end() timed out after 240 seconds` |
| `mistral` | deterministic | 1 | 33.3 | `event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind` |
| `llama` | infra | 1 | 3.7 | `exclusive gateway()::exclusive gateway() timed out after 240 seconds` |

</details>

## Flaky tests

> [!WARNING]
> Fails **across providers** ⇒ the test or prompt is suspect. Fails on **one provider** ⇒ a model limit.

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `error boundary event()` | `████████▊░░░` 36.6% | 5 — anthropic, deepseek, gemini, llama, openai | 82 |
| `parallel gateway()` | `███▎░░░░░░░░` 13.8% | 2 — gemini, llama | 80 |
| `escalation end()` | `███▎░░░░░░░░` 13.4% | 3 — deepseek, gemini, openai | 82 |
| `standard loop activity()` | `███▎░░░░░░░░` 13.4% | 3 — deepseek, gemini, openai | 82 |
| `event-based gateway()` | `███░░░░░░░░░` 12.3% | 2 — llama, openai | 81 |
| `escalation boundary event()` | `██▉░░░░░░░░░` 12.0% | 4 — anthropic, deepseek, gemini, openai | 83 |

<details>
<summary>28 more flaky tests (≤ 11.7% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `intermediate signal throw()` | `██▊░░░░░░░░░` 11.7% | 3 — gemini, llama, openai | 77 |
| `signal end()` | `██▌░░░░░░░░░` 10.4% | 4 — deepseek, gemini, llama, openai | 77 |
| `business rule task()` | `█▉░░░░░░░░░░` 7.8% | 2 — gemini, openai | 77 |
| `data objects and stores()` | `█▉░░░░░░░░░░` 7.8% | 2 — gemini, openai | 77 |
| `manual task()` | `█▉░░░░░░░░░░` 7.8% | 2 — gemini, openai | 77 |
| `message start()` | `█▉░░░░░░░░░░` 7.8% | 2 — gemini, openai | 77 |
| `sequential multi-instance activity()` | `█▉░░░░░░░░░░` 7.8% | 2 — gemini, openai | 77 |
| `timer start()` | `█▉░░░░░░░░░░` 7.8% | 2 — gemini, openai | 77 |
| `intermediate message throw()` | `█▊░░░░░░░░░░` 7.4% | 4 — deepseek, gemini, llama, openai | 81 |
| `exclusive gateway()` | `█▏░░░░░░░░░░` 4.9% | 3 — gemini, llama, openai | 82 |
| `intermediate escalation throw()` | `▉░░░░░░░░░░░` 3.7% | 3 — deepseek, llama, openai | 81 |
| `message end()` | `▉░░░░░░░░░░░` 3.7% | 2 — gemini, openai | 81 |
| `receive task()` | `▉░░░░░░░░░░░` 3.7% | 2 — gemini, openai | 81 |
| `script task()` | `▉░░░░░░░░░░░` 3.7% | 2 — gemini, openai | 82 |
| `signal start()` | `▉░░░░░░░░░░░` 3.7% | 2 — gemini, openai | 81 |
| `terminate end()` | `▉░░░░░░░░░░░` 3.7% | 2 — mistral, openai | 81 |
| `parallel multi-instance activity()` | `▉░░░░░░░░░░░` 3.6% | 3 — deepseek, gemini, openai | 83 |
| `call activity()` | `▋░░░░░░░░░░░` 2.8% | 2 — gemini, openai | 71 |
| `event subprocess()` | `▋░░░░░░░░░░░` 2.5% | 2 — gemini, mistral | 80 |
| `timer boundary event()` | `▋░░░░░░░░░░░` 2.5% | 2 — gemini, mistral | 80 |
| `embedded subprocess()` | `▋░░░░░░░░░░░` 2.4% | 2 — gemini, openai | 83 |
| `exclusive gateway with default branch()` | `▋░░░░░░░░░░░` 2.4% | 2 — gemini, openai | 83 |
| `send task()` | `▋░░░░░░░░░░░` 2.4% | 2 — gemini, openai | 83 |
| `error end()` | `▎░░░░░░░░░░░` 1.3% | 1 — gemini | 80 |
| `pools and lanes from distinct actors()` | `▎░░░░░░░░░░░` 1.3% | 1 — gemini | 80 |
| `inclusive gateway()` | `▎░░░░░░░░░░░` 1.2% | 1 — openai | 81 |
| `service task()` | `▎░░░░░░░░░░░` 1.2% | 1 — openai | 81 |
| `user task()` | `▎░░░░░░░░░░░` 1.2% | 1 — openai | 81 |

</details>

## LLM efficiency

> [!IMPORTANT]
> `mistral` is the outlier — median 5 calls/test but a P95 of 22 and a max of **69**, suggesting retry or tool-loop storms. Every other provider sits at a median of 5.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/llm-efficiency-dark.svg">
  <img alt="LLM calls per test by provider — mistral spread is far wider than the rest" src="assets/smoke-health/llm-efficiency-light.svg" width="760">
</picture>

---

<sub>📖 How this repo works — ingest, querying & setup → [`ABOUT.md`](ABOUT.md) · Regenerated every run by `render_dashboard.py`. Machine-managed — do not edit by hand.</sub>
