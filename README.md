# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 92.0% average pass rate · 100 total failures · 31 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99%, openai 97.7%, anthropic 96.1%, llama 93.4%, deepseek 92%, gemini 74%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.0% | 2 | $0.4668 | 13.99M | `mistral-large-2411, mistral-small-2506` |
| `openai` | `█████████████▋` 97.7% | 5 | $0.5138 | 10.72M | `gpt-4.1, gpt-4.1-mini` |
| `anthropic` | `█████████████▌` 96.1% | 9 | n/a | 5.95M | `claude-haiku-4-5, claude-sonnet-4-6` |
| `llama` | `█████████████▏` 93.4% | 14 | $0.2274 | 9.79M | `meta-llama/llama-3.3-70b-instruct` |
| `deepseek` | `████████████▉░` 92.0% | 13 | $0.0487 | 9.00M | `deepseek-chat` |
| `gemini` | `██████████▍░░░` 74.0% | 57 | n/a | 8.39M | `gemini-2.5-flash, gemini-2.5-pro` |

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
| `deepseek` | classification | 11 | 84.6 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | classification | 11 | 78.6 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | deterministic | 5 | 55.6 | `error boundary event()::400 - {"type":"error","error":{"type":"invalid_request_…` |
| `anthropic` | classification | 4 | 44.4 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | classification | 3 | 60.0 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | deterministic | 2 | 40.0 | `event-based gateway()::RECEIVE (act-await-response) requires messageName` |
| `deepseek` | deterministic | 2 | 15.4 | `escalation end()::TIMER (boundaryEvent) requires detail` |
| `llama` | deterministic | 2 | 14.3 | `event-based gateway()::RECEIVE (act-wait-for-response) requires messageName` |
| `mistral` | deterministic | 1 | 50.0 | `event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind` |
| `mistral` | infra | 1 | 50.0 | `timer boundary event()::timer boundary event() timed out after 240 seconds` |
| `llama` | infra | 1 | 7.1 | `exclusive gateway()::exclusive gateway() timed out after 240 seconds` |

</details>

## Flaky tests

> [!WARNING]
> Fails **across providers** ⇒ the test or prompt is suspect. Fails on **one provider** ⇒ a model limit.

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `error boundary event()` | `█████████▊░░` 40.5% | 5 — anthropic, deepseek, gemini, llama, openai | 37 |
| `escalation end()` | `████▌░░░░░░░` 18.9% | 3 — anthropic, deepseek, gemini | 37 |
| `intermediate signal throw()` | `████░░░░░░░░` 16.7% | 2 — gemini, llama | 36 |
| `event-based gateway()` | `███▊░░░░░░░░` 15.8% | 2 — llama, openai | 38 |
| `signal end()` | `███▍░░░░░░░░` 13.9% | 2 — gemini, llama | 36 |
| `standard loop activity()` | `███▎░░░░░░░░` 13.5% | 3 — anthropic, deepseek, gemini | 37 |

<details>
<summary>25 more flaky tests (≤ 11.1% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `business rule task()` | `██▋░░░░░░░░░` 11.1% | 1 — gemini | 36 |
| `data objects and stores()` | `██▋░░░░░░░░░` 11.1% | 1 — gemini | 36 |
| `manual task()` | `██▋░░░░░░░░░` 11.1% | 1 — gemini | 36 |
| `message start()` | `██▋░░░░░░░░░` 11.1% | 1 — gemini | 36 |
| `sequential multi-instance activity()` | `██▋░░░░░░░░░` 11.1% | 1 — gemini | 36 |
| `timer start()` | `██▋░░░░░░░░░` 11.1% | 1 — gemini | 36 |
| `exclusive gateway()` | `██▋░░░░░░░░░` 10.8% | 3 — anthropic, gemini, llama | 37 |
| `parallel gateway()` | `██▌░░░░░░░░░` 10.5% | 2 — gemini, llama | 38 |
| `escalation boundary event()` | `██░░░░░░░░░░` 8.1% | 3 — anthropic, deepseek, gemini | 37 |
| `script task()` | `██░░░░░░░░░░` 8.1% | 2 — anthropic, gemini | 37 |
| `event subprocess()` | `█▎░░░░░░░░░░` 5.3% | 2 — gemini, mistral | 38 |
| `intermediate message throw()` | `█▎░░░░░░░░░░` 5.3% | 2 — gemini, llama | 38 |
| `timer boundary event()` | `█▎░░░░░░░░░░` 5.3% | 2 — gemini, mistral | 38 |
| `call activity()` | `█░░░░░░░░░░░` 4.0% | 1 — gemini | 25 |
| `embedded subprocess()` | `▋░░░░░░░░░░░` 2.7% | 1 — gemini | 37 |
| `exclusive gateway with default branch()` | `▋░░░░░░░░░░░` 2.7% | 1 — gemini | 37 |
| `parallel multi-instance activity()` | `▋░░░░░░░░░░░` 2.7% | 1 — gemini | 37 |
| `send task()` | `▋░░░░░░░░░░░` 2.7% | 1 — gemini | 37 |
| `error end()` | `▋░░░░░░░░░░░` 2.6% | 1 — gemini | 38 |
| `intermediate escalation throw()` | `▋░░░░░░░░░░░` 2.6% | 1 — deepseek | 38 |
| `message end()` | `▋░░░░░░░░░░░` 2.6% | 1 — gemini | 38 |
| `pools and lanes from distinct actors()` | `▋░░░░░░░░░░░` 2.6% | 1 — gemini | 38 |
| `receive task()` | `▋░░░░░░░░░░░` 2.6% | 1 — gemini | 38 |
| `signal start()` | `▋░░░░░░░░░░░` 2.6% | 1 — gemini | 38 |
| `terminate end()` | `▋░░░░░░░░░░░` 2.6% | 1 — openai | 38 |

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
