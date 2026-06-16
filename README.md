# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 92.2% average pass rate · 102 total failures · 31 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.1%, openai 97.9%, anthropic 96.3%, llama 93.5%, deepseek 91.3%, gemini 75%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.1% | 2 | $0.4632 | 14.50M | `mistral-large-2411, mistral-small-2506` |
| `openai` | `█████████████▊` 97.9% | 5 | $0.5164 | 11.31M | `gpt-4.1, gpt-4.1-mini` |
| `anthropic` | `█████████████▌` 96.3% | 9 | n/a | 6.31M | `claude-haiku-4-5, claude-sonnet-4-6` |
| `llama` | `█████████████▏` 93.5% | 14 | $0.2269 | 10.03M | `meta-llama/llama-3.3-70b-instruct` |
| `deepseek` | `████████████▊░` 91.3% | 15 | $0.0486 | 9.57M | `deepseek-chat` |
| `gemini` | `██████████▌░░░` 75.0% | 57 | n/a | 8.87M | `gemini-2.5-flash, gemini-2.5-pro` |

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
| `deepseek` | classification | 13 | 86.7 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | classification | 11 | 78.6 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | deterministic | 5 | 55.6 | `error boundary event()::400 - {"type":"error","error":{"type":"invalid_request_…` |
| `anthropic` | classification | 4 | 44.4 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | classification | 3 | 60.0 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | deterministic | 2 | 40.0 | `event-based gateway()::RECEIVE (act-await-response) requires messageName` |
| `llama` | deterministic | 2 | 14.3 | `event-based gateway()::RECEIVE (act-wait-for-response) requires messageName` |
| `deepseek` | deterministic | 2 | 13.3 | `escalation end()::TIMER (boundaryEvent) requires detail` |
| `mistral` | deterministic | 1 | 50.0 | `event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind` |
| `mistral` | infra | 1 | 50.0 | `timer boundary event()::timer boundary event() timed out after 240 seconds` |
| `llama` | infra | 1 | 7.1 | `exclusive gateway()::exclusive gateway() timed out after 240 seconds` |

</details>

## Flaky tests

> [!WARNING]
> Fails **across providers** ⇒ the test or prompt is suspect. Fails on **one provider** ⇒ a model limit.

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `error boundary event()` | `█████████▉░░` 41.0% | 5 — anthropic, deepseek, gemini, llama, openai | 39 |
| `escalation end()` | `████▎░░░░░░░` 17.9% | 3 — anthropic, deepseek, gemini | 39 |
| `intermediate signal throw()` | `███▉░░░░░░░░` 16.2% | 2 — gemini, llama | 37 |
| `event-based gateway()` | `███▋░░░░░░░░` 15.0% | 2 — llama, openai | 40 |
| `signal end()` | `███▎░░░░░░░░` 13.5% | 2 — gemini, llama | 37 |
| `standard loop activity()` | `███▏░░░░░░░░` 12.8% | 3 — anthropic, deepseek, gemini | 39 |

<details>
<summary>25 more flaky tests (≤ 10.8% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `business rule task()` | `██▋░░░░░░░░░` 10.8% | 1 — gemini | 37 |
| `data objects and stores()` | `██▋░░░░░░░░░` 10.8% | 1 — gemini | 37 |
| `manual task()` | `██▋░░░░░░░░░` 10.8% | 1 — gemini | 37 |
| `message start()` | `██▋░░░░░░░░░` 10.8% | 1 — gemini | 37 |
| `sequential multi-instance activity()` | `██▋░░░░░░░░░` 10.8% | 1 — gemini | 37 |
| `timer start()` | `██▋░░░░░░░░░` 10.8% | 1 — gemini | 37 |
| `exclusive gateway()` | `██▌░░░░░░░░░` 10.3% | 3 — anthropic, gemini, llama | 39 |
| `parallel gateway()` | `██▍░░░░░░░░░` 10.0% | 2 — gemini, llama | 40 |
| `escalation boundary event()` | `█▉░░░░░░░░░░` 7.7% | 3 — anthropic, deepseek, gemini | 39 |
| `script task()` | `█▉░░░░░░░░░░` 7.7% | 2 — anthropic, gemini | 39 |
| `parallel multi-instance activity()` | `█▎░░░░░░░░░░` 5.1% | 2 — deepseek, gemini | 39 |
| `event subprocess()` | `█▎░░░░░░░░░░` 5.0% | 2 — gemini, mistral | 40 |
| `intermediate message throw()` | `█▎░░░░░░░░░░` 5.0% | 2 — gemini, llama | 40 |
| `timer boundary event()` | `█▎░░░░░░░░░░` 5.0% | 2 — gemini, mistral | 40 |
| `call activity()` | `▉░░░░░░░░░░░` 3.7% | 1 — gemini | 27 |
| `embedded subprocess()` | `▋░░░░░░░░░░░` 2.6% | 1 — gemini | 39 |
| `exclusive gateway with default branch()` | `▋░░░░░░░░░░░` 2.6% | 1 — gemini | 39 |
| `send task()` | `▋░░░░░░░░░░░` 2.6% | 1 — gemini | 39 |
| `error end()` | `▋░░░░░░░░░░░` 2.5% | 1 — gemini | 40 |
| `intermediate escalation throw()` | `▋░░░░░░░░░░░` 2.5% | 1 — deepseek | 40 |
| `message end()` | `▋░░░░░░░░░░░` 2.5% | 1 — gemini | 40 |
| `pools and lanes from distinct actors()` | `▋░░░░░░░░░░░` 2.5% | 1 — gemini | 40 |
| `receive task()` | `▋░░░░░░░░░░░` 2.5% | 1 — gemini | 40 |
| `signal start()` | `▋░░░░░░░░░░░` 2.5% | 1 — gemini | 40 |
| `terminate end()` | `▋░░░░░░░░░░░` 2.5% | 1 — openai | 40 |

</details>

## LLM efficiency

> [!IMPORTANT]
> `mistral` is the outlier — median 8 calls/test but a P95 of 29 and a max of **69**, suggesting retry or tool-loop storms. Every other provider sits at a median of 5.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/llm-efficiency-dark.svg">
  <img alt="LLM calls per test by provider — mistral spread is far wider than the rest" src="assets/smoke-health/llm-efficiency-light.svg" width="760">
</picture>

---

<sub>📖 How this repo works — ingest, querying & setup → [`ABOUT.md`](ABOUT.md) · Regenerated every run by `render_dashboard.py`. Machine-managed — do not edit by hand.</sub>
