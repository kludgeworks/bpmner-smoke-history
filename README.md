# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 89.4% average pass rate · 214 total failures · 34 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.4%, openai 98.3%, llama 94.1%, deepseek 90.2%, gemini 81.6%, anthropic 73%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.4% | 2 | $0.4760 | 21.04M | `mistral-large-2411, mistral-small-2506` |
| `openai` | `█████████████▊` 98.3% | 6 | $0.5006 | 16.58M | `gpt-4.1, gpt-4.1-mini` |
| `llama` | `█████████████▏` 94.1% | 19 | $0.2283 | 14.74M | `meta-llama/llama-3.3-70b-instruct` |
| `deepseek` | `████████████▋░` 90.2% | 28 | $0.0512 | 16.17M | `deepseek-chat` |
| `gemini` | `███████████▍░░` 81.6% | 60 | n/a | 14.44M | `gemini-2.5-flash, gemini-2.5-pro` |
| `anthropic` | `██████████▎░░░` 73.0% | 99 | n/a | 7.16M | `claude-haiku-4-5, claude-sonnet-4-6` |

_\* `gemini`, `anthropic` cost is `n/a` — provider has no configured pricing._

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
  <img alt="Failure categories by provider — anthropic has the most failures (99)" src="assets/smoke-health/failure-split-light.svg" width="760">
</picture>

<details>
<summary><b>Failure detail</b> — counts, share & sample signatures</summary>

| Provider | Category | Failures | % of fails | Sample signature |
|---|---|--:|--:|---|
| `anthropic` | deterministic | 95 | 96.0 | `business rule task()::400 - {"type":"error","error":{"type":"invalid_request_er…` |
| `gemini` | deterministic | 59 | 98.3 | `business rule task()::429 - [{` |
| `deepseek` | classification | 25 | 89.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | classification | 16 | 84.2 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | classification | 4 | 66.7 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 4.0 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `deepseek` | deterministic | 3 | 10.7 | `escalation end()::TIMER (boundaryEvent) requires detail` |
| `openai` | deterministic | 2 | 33.3 | `event-based gateway()::RECEIVE (act-await-response) requires messageName` |
| `llama` | deterministic | 2 | 10.5 | `event-based gateway()::RECEIVE (act-wait-for-response) requires messageName` |
| `mistral` | deterministic | 1 | 50.0 | `event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind` |
| `mistral` | infra | 1 | 50.0 | `timer boundary event()::timer boundary event() timed out after 240 seconds` |
| `llama` | infra | 1 | 5.3 | `exclusive gateway()::exclusive gateway() timed out after 240 seconds` |
| `gemini` | classification | 1 | 1.7 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |

</details>

## Flaky tests

> [!WARNING]
> Fails **across providers** ⇒ the test or prompt is suspect. Fails on **one provider** ⇒ a model limit.

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `error boundary event()` | `█████████▉░░` 41.4% | 5 — anthropic, deepseek, gemini, llama, openai | 58 |
| `event-based gateway()` | `████▊░░░░░░░` 19.7% | 3 — anthropic, llama, openai | 61 |
| `escalation end()` | `████▏░░░░░░░` 17.2% | 3 — anthropic, deepseek, gemini | 58 |
| `parallel gateway()` | `████░░░░░░░░` 16.9% | 3 — anthropic, gemini, llama | 59 |
| `signal end()` | `███▉░░░░░░░░` 16.1% | 4 — anthropic, deepseek, gemini, llama | 56 |
| `intermediate signal throw()` | `███▉░░░░░░░░` 16.1% | 3 — anthropic, gemini, llama | 56 |

<details>
<summary>28 more flaky tests (≤ 15.5% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `standard loop activity()` | `███▊░░░░░░░░` 15.5% | 3 — anthropic, deepseek, gemini | 58 |
| `escalation boundary event()` | `███▎░░░░░░░░` 13.6% | 3 — anthropic, deepseek, gemini | 59 |
| `business rule task()` | `███░░░░░░░░░` 12.5% | 2 — anthropic, gemini | 56 |
| `data objects and stores()` | `███░░░░░░░░░` 12.5% | 2 — anthropic, gemini | 56 |
| `manual task()` | `███░░░░░░░░░` 12.5% | 2 — anthropic, gemini | 56 |
| `message start()` | `███░░░░░░░░░` 12.5% | 2 — anthropic, gemini | 56 |
| `sequential multi-instance activity()` | `███░░░░░░░░░` 12.5% | 2 — anthropic, gemini | 56 |
| `timer start()` | `███░░░░░░░░░` 12.5% | 2 — anthropic, gemini | 56 |
| `intermediate message throw()` | `██▍░░░░░░░░░` 10.0% | 3 — anthropic, gemini, llama | 60 |
| `exclusive gateway()` | `██▏░░░░░░░░░` 8.6% | 3 — anthropic, gemini, llama | 58 |
| `event subprocess()` | `██░░░░░░░░░░` 8.5% | 3 — anthropic, gemini, mistral | 59 |
| `timer boundary event()` | `██░░░░░░░░░░` 8.5% | 3 — anthropic, gemini, mistral | 59 |
| `message end()` | `██░░░░░░░░░░` 8.3% | 2 — anthropic, gemini | 60 |
| `receive task()` | `██░░░░░░░░░░` 8.3% | 2 — anthropic, gemini | 60 |
| `signal start()` | `██░░░░░░░░░░` 8.3% | 2 — anthropic, gemini | 60 |
| `intermediate escalation throw()` | `██░░░░░░░░░░` 8.2% | 2 — anthropic, deepseek | 61 |
| `terminate end()` | `██░░░░░░░░░░` 8.2% | 2 — anthropic, openai | 61 |
| `script task()` | `█▋░░░░░░░░░░` 6.9% | 2 — anthropic, gemini | 58 |
| `error end()` | `█▋░░░░░░░░░░` 6.8% | 2 — anthropic, gemini | 59 |
| `pools and lanes from distinct actors()` | `█▋░░░░░░░░░░` 6.8% | 2 — anthropic, gemini | 59 |
| `inclusive gateway()` | `█▋░░░░░░░░░░` 6.6% | 1 — anthropic | 61 |
| `service task()` | `█▋░░░░░░░░░░` 6.6% | 1 — anthropic | 61 |
| `user task()` | `█▋░░░░░░░░░░` 6.6% | 1 — anthropic | 61 |
| `parallel multi-instance activity()` | `█▎░░░░░░░░░░` 5.1% | 3 — anthropic, deepseek, gemini | 59 |
| `call activity()` | `█░░░░░░░░░░░` 4.3% | 2 — anthropic, gemini | 47 |
| `embedded subprocess()` | `▉░░░░░░░░░░░` 3.4% | 2 — anthropic, gemini | 59 |
| `exclusive gateway with default branch()` | `▉░░░░░░░░░░░` 3.4% | 2 — anthropic, gemini | 59 |
| `send task()` | `▉░░░░░░░░░░░` 3.4% | 2 — anthropic, gemini | 59 |

</details>

## LLM efficiency

> [!IMPORTANT]
> `mistral` is the outlier — median 7 calls/test but a P95 of 23 and a max of **69**, suggesting retry or tool-loop storms. Every other provider sits at a median of 5.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/llm-efficiency-dark.svg">
  <img alt="LLM calls per test by provider — mistral spread is far wider than the rest" src="assets/smoke-health/llm-efficiency-light.svg" width="760">
</picture>

---

<sub>📖 How this repo works — ingest, querying & setup → [`ABOUT.md`](ABOUT.md) · Regenerated every run by `render_dashboard.py`. Machine-managed — do not edit by hand.</sub>
