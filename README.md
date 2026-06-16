# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 91.9% average pass rate · 99 total failures · 31 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99%, openai 97.7%, anthropic 95.9%, llama 93.2%, deepseek 92.3%, gemini 73.4%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.0% | 2 | $0.4709 | 13.76M | `mistral-large-2411, mistral-small-2506` |
| `openai` | `█████████████▋` 97.7% | 5 | $0.5110 | 10.40M | `gpt-4.1, gpt-4.1-mini` |
| `anthropic` | `█████████████▍` 95.9% | 9 | n/a | 5.74M | `claude-haiku-4-5, claude-sonnet-4-6` |
| `llama` | `█████████████░` 93.2% | 14 | $0.2285 | 9.58M | `meta-llama/llama-3.3-70b-instruct` |
| `deepseek` | `████████████▉░` 92.3% | 12 | $0.0487 | 8.70M | `deepseek-chat` |
| `gemini` | `██████████▎░░░` 73.4% | 57 | n/a | 8.13M | `gemini-2.5-flash, gemini-2.5-pro` |

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
| `anthropic` | deterministic | 5 | 55.6 | `error boundary event()::400 - {"type":"error","error":{"type":"invalid_request_…` |
| `anthropic` | classification | 4 | 44.4 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `deepseek` | classification | 10 | 83.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `deepseek` | deterministic | 2 | 16.7 | `escalation end()::TIMER (boundaryEvent) requires detail` |
| `gemini` | deterministic | 57 | 100.0 | `business rule task()::429 - [{` |
| `llama` | classification | 11 | 78.6 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | deterministic | 2 | 14.3 | `event-based gateway()::RECEIVE (act-wait-for-response) requires messageName` |
| `llama` | infra | 1 | 7.1 | `exclusive gateway()::exclusive gateway() timed out after 240 seconds` |
| `mistral` | infra | 1 | 50.0 | `timer boundary event()::timer boundary event() timed out after 240 seconds` |
| `mistral` | deterministic | 1 | 50.0 | `event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind` |
| `openai` | classification | 3 | 60.0 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | deterministic | 2 | 40.0 | `event-based gateway()::RECEIVE (act-await-response) requires messageName` |

</details>

## Flaky tests

> [!WARNING]
> Fails **across providers** ⇒ the test or prompt is suspect. Fails on **one provider** ⇒ a model limit.

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `error boundary event()` | `██████████░░` 41.7% | 5 — anthropic, deepseek, gemini, llama, openai | 36 |
| `escalation end()` | `████▋░░░░░░░` 19.4% | 3 — anthropic, deepseek, gemini | 36 |
| `intermediate signal throw()` | `████▏░░░░░░░` 17.1% | 2 — gemini, llama | 35 |
| `event-based gateway()` | `███▉░░░░░░░░` 16.2% | 2 — llama, openai | 37 |
| `signal end()` | `███▍░░░░░░░░` 14.3% | 2 — gemini, llama | 35 |
| `standard loop activity()` | `███▍░░░░░░░░` 13.9% | 3 — anthropic, deepseek, gemini | 36 |

<details>
<summary>25 more flaky tests (≤ 11.4% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `business rule task()` | `██▊░░░░░░░░░` 11.4% | 1 — gemini | 35 |
| `data objects and stores()` | `██▊░░░░░░░░░` 11.4% | 1 — gemini | 35 |
| `manual task()` | `██▊░░░░░░░░░` 11.4% | 1 — gemini | 35 |
| `message start()` | `██▊░░░░░░░░░` 11.4% | 1 — gemini | 35 |
| `sequential multi-instance activity()` | `██▊░░░░░░░░░` 11.4% | 1 — gemini | 35 |
| `timer start()` | `██▊░░░░░░░░░` 11.4% | 1 — gemini | 35 |
| `exclusive gateway()` | `██▋░░░░░░░░░` 11.1% | 3 — anthropic, gemini, llama | 36 |
| `parallel gateway()` | `██▋░░░░░░░░░` 10.8% | 2 — gemini, llama | 37 |
| `script task()` | `██░░░░░░░░░░` 8.3% | 2 — anthropic, gemini | 36 |
| `escalation boundary event()` | `█▍░░░░░░░░░░` 5.6% | 2 — anthropic, gemini | 36 |
| `event subprocess()` | `█▎░░░░░░░░░░` 5.4% | 2 — gemini, mistral | 37 |
| `intermediate message throw()` | `█▎░░░░░░░░░░` 5.4% | 2 — gemini, llama | 37 |
| `timer boundary event()` | `█▎░░░░░░░░░░` 5.4% | 2 — gemini, mistral | 37 |
| `call activity()` | `█░░░░░░░░░░░` 4.2% | 1 — gemini | 24 |
| `embedded subprocess()` | `▋░░░░░░░░░░░` 2.8% | 1 — gemini | 36 |
| `exclusive gateway with default branch()` | `▋░░░░░░░░░░░` 2.8% | 1 — gemini | 36 |
| `parallel multi-instance activity()` | `▋░░░░░░░░░░░` 2.8% | 1 — gemini | 36 |
| `send task()` | `▋░░░░░░░░░░░` 2.8% | 1 — gemini | 36 |
| `error end()` | `▋░░░░░░░░░░░` 2.7% | 1 — gemini | 37 |
| `intermediate escalation throw()` | `▋░░░░░░░░░░░` 2.7% | 1 — deepseek | 37 |
| `message end()` | `▋░░░░░░░░░░░` 2.7% | 1 — gemini | 37 |
| `pools and lanes from distinct actors()` | `▋░░░░░░░░░░░` 2.7% | 1 — gemini | 37 |
| `receive task()` | `▋░░░░░░░░░░░` 2.7% | 1 — gemini | 37 |
| `signal start()` | `▋░░░░░░░░░░░` 2.7% | 1 — gemini | 37 |
| `terminate end()` | `▋░░░░░░░░░░░` 2.7% | 1 — openai | 37 |

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
