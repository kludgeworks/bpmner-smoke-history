# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 92.7% average pass rate · 105 total failures · 31 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.2%, openai 97.6%, anthropic 96.7%, llama 94.1%, deepseek 91.4%, gemini 77.4%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.2% | 2 | $0.4583 | 15.67M | `mistral-large-2411, mistral-small-2506` |
| `openai` | `█████████████▋` 97.6% | 6 | $0.5122 | 12.32M | `gpt-4.1, gpt-4.1-mini` |
| `anthropic` | `█████████████▌` 96.7% | 9 | n/a | 7.01M | `claude-haiku-4-5, claude-sonnet-4-6` |
| `llama` | `█████████████▏` 94.1% | 14 | $0.2236 | 10.90M | `meta-llama/llama-3.3-70b-instruct` |
| `deepseek` | `████████████▊░` 91.4% | 17 | $0.0492 | 10.92M | `deepseek-chat` |
| `gemini` | `██████████▉░░░` 77.4% | 57 | n/a | 10.26M | `gemini-2.5-flash, gemini-2.5-pro` |

_\* `anthropic`, `gemini` cost is `n/a` — provider has no configured pricing._

</details>

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/latency-trend-dark.svg">
  <img alt="Average LLM latency by provider over runs — llama highest, deepseek lowest" src="assets/smoke-health/latency-trend-light.svg" width="760">
</picture>

## Cost per test

> [!CAUTION]
> Cost is normalised **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable. `anthropic`, `gemini` are excluded (no configured pricing).

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/cost-trend-dark.svg">
  <img alt="Cost per test by provider over runs — openai highest, deepseek lowest" src="assets/smoke-health/cost-trend-light.svg" width="760">
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
  <img alt="Failure categories by provider — gemini has the most failures (57)" src="assets/smoke-health/failure-split-light.svg" width="760">
</picture>

<details>
<summary><b>Failure detail</b> — counts, share & sample signatures</summary>

| Provider | Category | Failures | % of fails | Sample signature |
|---|---|--:|--:|---|
| `gemini` | deterministic | 57 | 100.0 | `business rule task()::429 - [{` |
| `deepseek` | classification | 15 | 88.2 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | classification | 11 | 78.6 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | deterministic | 5 | 55.6 | `error boundary event()::400 - {"type":"error","error":{"type":"invalid_request_…` |
| `openai` | classification | 4 | 66.7 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 44.4 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | deterministic | 2 | 33.3 | `event-based gateway()::RECEIVE (act-await-response) requires messageName` |
| `llama` | deterministic | 2 | 14.3 | `event-based gateway()::RECEIVE (act-wait-for-response) requires messageName` |
| `deepseek` | deterministic | 2 | 11.8 | `escalation end()::TIMER (boundaryEvent) requires detail` |
| `mistral` | deterministic | 1 | 50.0 | `event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind` |
| `mistral` | infra | 1 | 50.0 | `timer boundary event()::timer boundary event() timed out after 240 seconds` |
| `llama` | infra | 1 | 7.1 | `exclusive gateway()::exclusive gateway() timed out after 240 seconds` |

</details>

## Flaky tests

> [!WARNING]
> Fails **across providers** ⇒ the test or prompt is suspect. Fails on **one provider** ⇒ a model limit.

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `error boundary event()` | `█████████▌░░` 39.5% | 5 — anthropic, deepseek, gemini, llama, openai | 43 |
| `escalation end()` | `███▉░░░░░░░░` 16.3% | 3 — anthropic, deepseek, gemini | 43 |
| `intermediate signal throw()` | `███▌░░░░░░░░` 14.6% | 2 — gemini, llama | 41 |
| `event-based gateway()` | `███▎░░░░░░░░` 13.6% | 2 — llama, openai | 44 |
| `signal end()` | `██▉░░░░░░░░░` 12.2% | 2 — gemini, llama | 41 |
| `escalation boundary event()` | `██▊░░░░░░░░░` 11.6% | 3 — anthropic, deepseek, gemini | 43 |

<details>
<summary>25 more flaky tests (≤ 11.6% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `standard loop activity()` | `██▊░░░░░░░░░` 11.6% | 3 — anthropic, deepseek, gemini | 43 |
| `business rule task()` | `██▍░░░░░░░░░` 9.8% | 1 — gemini | 41 |
| `data objects and stores()` | `██▍░░░░░░░░░` 9.8% | 1 — gemini | 41 |
| `manual task()` | `██▍░░░░░░░░░` 9.8% | 1 — gemini | 41 |
| `message start()` | `██▍░░░░░░░░░` 9.8% | 1 — gemini | 41 |
| `sequential multi-instance activity()` | `██▍░░░░░░░░░` 9.8% | 1 — gemini | 41 |
| `timer start()` | `██▍░░░░░░░░░` 9.8% | 1 — gemini | 41 |
| `exclusive gateway()` | `██▎░░░░░░░░░` 9.3% | 3 — anthropic, gemini, llama | 43 |
| `parallel gateway()` | `██▏░░░░░░░░░` 9.1% | 2 — gemini, llama | 44 |
| `script task()` | `█▋░░░░░░░░░░` 7.0% | 2 — anthropic, gemini | 43 |
| `parallel multi-instance activity()` | `█▏░░░░░░░░░░` 4.7% | 2 — deepseek, gemini | 43 |
| `event subprocess()` | `█▏░░░░░░░░░░` 4.5% | 2 — gemini, mistral | 44 |
| `intermediate message throw()` | `█▏░░░░░░░░░░` 4.5% | 2 — gemini, llama | 44 |
| `timer boundary event()` | `█▏░░░░░░░░░░` 4.5% | 2 — gemini, mistral | 44 |
| `call activity()` | `▊░░░░░░░░░░░` 3.2% | 1 — gemini | 31 |
| `embedded subprocess()` | `▌░░░░░░░░░░░` 2.3% | 1 — gemini | 43 |
| `error end()` | `▌░░░░░░░░░░░` 2.3% | 1 — gemini | 44 |
| `exclusive gateway with default branch()` | `▌░░░░░░░░░░░` 2.3% | 1 — gemini | 43 |
| `intermediate escalation throw()` | `▌░░░░░░░░░░░` 2.3% | 1 — deepseek | 44 |
| `message end()` | `▌░░░░░░░░░░░` 2.3% | 1 — gemini | 44 |
| `pools and lanes from distinct actors()` | `▌░░░░░░░░░░░` 2.3% | 1 — gemini | 44 |
| `receive task()` | `▌░░░░░░░░░░░` 2.3% | 1 — gemini | 44 |
| `send task()` | `▌░░░░░░░░░░░` 2.3% | 1 — gemini | 43 |
| `signal start()` | `▌░░░░░░░░░░░` 2.3% | 1 — gemini | 44 |
| `terminate end()` | `▌░░░░░░░░░░░` 2.3% | 1 — openai | 44 |

</details>

## LLM efficiency

> [!IMPORTANT]
> `mistral` is the outlier — median 8 calls/test but a P95 of 26 and a max of **69**, suggesting retry or tool-loop storms. Every other provider sits at a median of 5.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/llm-efficiency-dark.svg">
  <img alt="LLM calls per test by provider — mistral spread is far wider than the rest" src="assets/smoke-health/llm-efficiency-light.svg" width="760">
</picture>

---

<sub>📖 How this repo works — ingest, querying & setup → [`ABOUT.md`](ABOUT.md) · Regenerated every run by `render_dashboard.py`. Machine-managed — do not edit by hand.</sub>
