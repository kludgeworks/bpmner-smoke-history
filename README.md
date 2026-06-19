# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 91.4% average pass rate · 146 total failures · 34 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.3%, openai 97.9%, llama 94.3%, deepseek 91%, anthropic 85.9%, gemini 79.9%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.3% | 2 | $0.4581 | 17.72M | `mistral-large-2411, mistral-small-2506` |
| `openai` | `█████████████▊` 97.9% | 6 | $0.5048 | 14.04M | `gpt-4.1, gpt-4.1-mini` |
| `llama` | `█████████████▎` 94.3% | 16 | $0.2271 | 12.87M | `meta-llama/llama-3.3-70b-instruct` |
| `deepseek` | `████████████▊░` 91.0% | 21 | $0.0493 | 12.78M | `deepseek-chat` |
| `anthropic` | `████████████░░` 85.9% | 44 | n/a | 7.16M | `claude-haiku-4-5, claude-sonnet-4-6` |
| `gemini` | `███████████▏░░` 79.9% | 57 | n/a | 11.93M | `gemini-2.5-flash, gemini-2.5-pro` |

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
| `anthropic` | deterministic | 40 | 90.9 | `business rule task()::400 - {"type":"error","error":{"type":"invalid_request_er…` |
| `deepseek` | classification | 18 | 85.7 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | classification | 13 | 81.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | classification | 4 | 66.7 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 9.1 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `deepseek` | deterministic | 3 | 14.3 | `escalation end()::TIMER (boundaryEvent) requires detail` |
| `openai` | deterministic | 2 | 33.3 | `event-based gateway()::RECEIVE (act-await-response) requires messageName` |
| `llama` | deterministic | 2 | 12.5 | `event-based gateway()::RECEIVE (act-wait-for-response) requires messageName` |
| `mistral` | deterministic | 1 | 50.0 | `event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind` |
| `mistral` | infra | 1 | 50.0 | `timer boundary event()::timer boundary event() timed out after 240 seconds` |
| `llama` | infra | 1 | 6.3 | `exclusive gateway()::exclusive gateway() timed out after 240 seconds` |

</details>

## Flaky tests

> [!WARNING]
> Fails **across providers** ⇒ the test or prompt is suspect. Fails on **one provider** ⇒ a model limit.

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `error boundary event()` | `█████████▋░░` 40.0% | 5 — anthropic, deepseek, gemini, llama, openai | 50 |
| `event-based gateway()` | `████▎░░░░░░░` 17.6% | 3 — anthropic, llama, openai | 51 |
| `escalation end()` | `███▉░░░░░░░░` 16.0% | 3 — anthropic, deepseek, gemini | 50 |
| `signal end()` | `███▋░░░░░░░░` 14.9% | 4 — anthropic, deepseek, gemini, llama | 47 |
| `intermediate signal throw()` | `███▋░░░░░░░░` 14.9% | 3 — anthropic, gemini, llama | 47 |
| `escalation boundary event()` | `███▍░░░░░░░░` 14.0% | 3 — anthropic, deepseek, gemini | 50 |

<details>
<summary>28 more flaky tests (≤ 12.0% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `parallel gateway()` | `██▉░░░░░░░░░` 12.0% | 3 — anthropic, gemini, llama | 50 |
| `standard loop activity()` | `██▉░░░░░░░░░` 12.0% | 3 — anthropic, deepseek, gemini | 50 |
| `business rule task()` | `██▌░░░░░░░░░` 10.6% | 2 — anthropic, gemini | 47 |
| `data objects and stores()` | `██▌░░░░░░░░░` 10.6% | 2 — anthropic, gemini | 47 |
| `manual task()` | `██▌░░░░░░░░░` 10.6% | 2 — anthropic, gemini | 47 |
| `message start()` | `██▌░░░░░░░░░` 10.6% | 2 — anthropic, gemini | 47 |
| `sequential multi-instance activity()` | `██▌░░░░░░░░░` 10.6% | 2 — anthropic, gemini | 47 |
| `timer start()` | `██▌░░░░░░░░░` 10.6% | 2 — anthropic, gemini | 47 |
| `exclusive gateway()` | `██▍░░░░░░░░░` 10.0% | 3 — anthropic, gemini, llama | 50 |
| `event subprocess()` | `█▉░░░░░░░░░░` 8.0% | 3 — anthropic, gemini, mistral | 50 |
| `timer boundary event()` | `█▉░░░░░░░░░░` 8.0% | 3 — anthropic, gemini, mistral | 50 |
| `script task()` | `█▉░░░░░░░░░░` 8.0% | 2 — anthropic, gemini | 50 |
| `parallel multi-instance activity()` | `█▌░░░░░░░░░░` 6.0% | 3 — anthropic, deepseek, gemini | 50 |
| `error end()` | `█▌░░░░░░░░░░` 6.0% | 2 — anthropic, gemini | 50 |
| `pools and lanes from distinct actors()` | `█▌░░░░░░░░░░` 6.0% | 2 — anthropic, gemini | 50 |
| `call activity()` | `█▎░░░░░░░░░░` 5.3% | 2 — anthropic, gemini | 38 |
| `embedded subprocess()` | `█░░░░░░░░░░░` 4.0% | 2 — anthropic, gemini | 50 |
| `exclusive gateway with default branch()` | `█░░░░░░░░░░░` 4.0% | 2 — anthropic, gemini | 50 |
| `send task()` | `█░░░░░░░░░░░` 4.0% | 2 — anthropic, gemini | 50 |
| `intermediate escalation throw()` | `▉░░░░░░░░░░░` 3.9% | 2 — anthropic, deepseek | 51 |
| `intermediate message throw()` | `▉░░░░░░░░░░░` 3.9% | 2 — gemini, llama | 51 |
| `terminate end()` | `▉░░░░░░░░░░░` 3.9% | 2 — anthropic, openai | 51 |
| `inclusive gateway()` | `▌░░░░░░░░░░░` 2.0% | 1 — anthropic | 51 |
| `message end()` | `▌░░░░░░░░░░░` 2.0% | 1 — gemini | 51 |
| `receive task()` | `▌░░░░░░░░░░░` 2.0% | 1 — gemini | 51 |
| `service task()` | `▌░░░░░░░░░░░` 2.0% | 1 — anthropic | 51 |
| `signal start()` | `▌░░░░░░░░░░░` 2.0% | 1 — gemini | 51 |
| `user task()` | `▌░░░░░░░░░░░` 2.0% | 1 — anthropic | 51 |

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
