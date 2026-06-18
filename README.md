# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 91.5% average pass rate · 140 total failures · 34 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.3%, openai 97.9%, llama 94.5%, deepseek 90.7%, anthropic 87.3%, gemini 79.4%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.3% | 2 | $0.4593 | 17.44M | `mistral-large-2411, mistral-small-2506` |
| `openai` | `█████████████▊` 97.9% | 6 | $0.5085 | 13.87M | `gpt-4.1, gpt-4.1-mini` |
| `llama` | `█████████████▎` 94.5% | 15 | $0.2267 | 12.59M | `meta-llama/llama-3.3-70b-instruct` |
| `deepseek` | `████████████▊░` 90.7% | 21 | $0.0488 | 12.33M | `deepseek-chat` |
| `anthropic` | `████████████▎░` 87.3% | 39 | n/a | 7.16M | `claude-haiku-4-5, claude-sonnet-4-6` |
| `gemini` | `███████████▏░░` 79.4% | 57 | n/a | 11.63M | `gemini-2.5-flash, gemini-2.5-pro` |

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
| `anthropic` | deterministic | 35 | 89.7 | `business rule task()::400 - {"type":"error","error":{"type":"invalid_request_er…` |
| `deepseek` | classification | 18 | 85.7 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | classification | 12 | 80.0 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | classification | 4 | 66.7 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 10.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `deepseek` | deterministic | 3 | 14.3 | `escalation end()::TIMER (boundaryEvent) requires detail` |
| `openai` | deterministic | 2 | 33.3 | `event-based gateway()::RECEIVE (act-await-response) requires messageName` |
| `llama` | deterministic | 2 | 13.3 | `event-based gateway()::RECEIVE (act-wait-for-response) requires messageName` |
| `mistral` | deterministic | 1 | 50.0 | `event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind` |
| `mistral` | infra | 1 | 50.0 | `timer boundary event()::timer boundary event() timed out after 240 seconds` |
| `llama` | infra | 1 | 6.7 | `exclusive gateway()::exclusive gateway() timed out after 240 seconds` |

</details>

## Flaky tests

> [!WARNING]
> Fails **across providers** ⇒ the test or prompt is suspect. Fails on **one provider** ⇒ a model limit.

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `error boundary event()` | `█████████▊░░` 40.8% | 5 — anthropic, deepseek, gemini, llama, openai | 49 |
| `escalation end()` | `███▉░░░░░░░░` 16.3% | 3 — anthropic, deepseek, gemini | 49 |
| `event-based gateway()` | `███▉░░░░░░░░` 16.0% | 3 — anthropic, llama, openai | 50 |
| `signal end()` | `███▋░░░░░░░░` 15.2% | 4 — anthropic, deepseek, gemini, llama | 46 |
| `intermediate signal throw()` | `███▋░░░░░░░░` 15.2% | 3 — anthropic, gemini, llama | 46 |
| `escalation boundary event()` | `███▍░░░░░░░░` 14.3% | 3 — anthropic, deepseek, gemini | 49 |

<details>
<summary>28 more flaky tests (≤ 12.2% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `standard loop activity()` | `██▉░░░░░░░░░` 12.2% | 3 — anthropic, deepseek, gemini | 49 |
| `business rule task()` | `██▋░░░░░░░░░` 10.9% | 2 — anthropic, gemini | 46 |
| `data objects and stores()` | `██▋░░░░░░░░░` 10.9% | 2 — anthropic, gemini | 46 |
| `manual task()` | `██▋░░░░░░░░░` 10.9% | 2 — anthropic, gemini | 46 |
| `message start()` | `██▋░░░░░░░░░` 10.9% | 2 — anthropic, gemini | 46 |
| `sequential multi-instance activity()` | `██▋░░░░░░░░░` 10.9% | 2 — anthropic, gemini | 46 |
| `timer start()` | `██▋░░░░░░░░░` 10.9% | 2 — anthropic, gemini | 46 |
| `exclusive gateway()` | `██▌░░░░░░░░░` 10.2% | 3 — anthropic, gemini, llama | 49 |
| `parallel gateway()` | `██▌░░░░░░░░░` 10.2% | 3 — anthropic, gemini, llama | 49 |
| `script task()` | `██░░░░░░░░░░` 8.2% | 2 — anthropic, gemini | 49 |
| `event subprocess()` | `█▌░░░░░░░░░░` 6.1% | 3 — anthropic, gemini, mistral | 49 |
| `parallel multi-instance activity()` | `█▌░░░░░░░░░░` 6.1% | 3 — anthropic, deepseek, gemini | 49 |
| `timer boundary event()` | `█▌░░░░░░░░░░` 6.1% | 3 — anthropic, gemini, mistral | 49 |
| `call activity()` | `█▎░░░░░░░░░░` 5.4% | 2 — anthropic, gemini | 37 |
| `embedded subprocess()` | `█░░░░░░░░░░░` 4.1% | 2 — anthropic, gemini | 49 |
| `error end()` | `█░░░░░░░░░░░` 4.1% | 2 — anthropic, gemini | 49 |
| `exclusive gateway with default branch()` | `█░░░░░░░░░░░` 4.1% | 2 — anthropic, gemini | 49 |
| `pools and lanes from distinct actors()` | `█░░░░░░░░░░░` 4.1% | 2 — anthropic, gemini | 49 |
| `send task()` | `█░░░░░░░░░░░` 4.1% | 2 — anthropic, gemini | 49 |
| `intermediate escalation throw()` | `█░░░░░░░░░░░` 4.0% | 2 — anthropic, deepseek | 50 |
| `intermediate message throw()` | `█░░░░░░░░░░░` 4.0% | 2 — gemini, llama | 50 |
| `terminate end()` | `█░░░░░░░░░░░` 4.0% | 2 — anthropic, openai | 50 |
| `inclusive gateway()` | `▌░░░░░░░░░░░` 2.0% | 1 — anthropic | 50 |
| `message end()` | `▌░░░░░░░░░░░` 2.0% | 1 — gemini | 50 |
| `receive task()` | `▌░░░░░░░░░░░` 2.0% | 1 — gemini | 50 |
| `service task()` | `▌░░░░░░░░░░░` 2.0% | 1 — anthropic | 50 |
| `signal start()` | `▌░░░░░░░░░░░` 2.0% | 1 — gemini | 50 |
| `user task()` | `▌░░░░░░░░░░░` 2.0% | 1 — anthropic | 50 |

</details>

## LLM efficiency

> [!IMPORTANT]
> `mistral` is the outlier — median 8 calls/test but a P95 of 23 and a max of **69**, suggesting retry or tool-loop storms. Every other provider sits at a median of 5.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/llm-efficiency-dark.svg">
  <img alt="LLM calls per test by provider — mistral spread is far wider than the rest" src="assets/smoke-health/llm-efficiency-light.svg" width="760">
</picture>

---

<sub>📖 How this repo works — ingest, querying & setup → [`ABOUT.md`](ABOUT.md) · Regenerated every run by `render_dashboard.py`. Machine-managed — do not edit by hand.</sub>
