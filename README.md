# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 87.3% average pass rate · 285 total failures · 34 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.5%, llama 94.4%, openai 90.1%, deepseek 90%, gemini 83%, anthropic 67%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.5% | 2 | $0.4719 | 22.78M | `mistral-large-2411, mistral-small-2506` |
| `llama` | `█████████████▎` 94.4% | 20 | $0.2296 | 16.39M | `meta-llama/llama-3.3-70b-instruct` |
| `openai` | `████████████▋░` 90.1% | 38 | n/a | 16.82M | `gpt-4.1, gpt-4.1-mini` |
| `deepseek` | `████████████▋░` 90.0% | 32 | $0.0511 | 18.01M | `deepseek-chat` |
| `gemini` | `███████████▋░░` 83.0% | 61 | n/a | 16.21M | `gemini-2.5-flash, gemini-2.5-pro` |
| `anthropic` | `█████████▍░░░░` 67.0% | 132 | n/a | 7.16M | `claude-haiku-4-5, claude-sonnet-4-6` |

_\* `openai`, `gemini`, `anthropic` cost is `n/a` — provider has no configured pricing._

</details>

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/latency-trend-dark.svg">
  <img alt="Average LLM latency by provider over runs — llama highest, deepseek lowest" src="assets/smoke-health/latency-trend-light.svg" width="760">
</picture>

## Cost per test

> [!CAUTION]
> Cost is normalised **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable. `anthropic`, `gemini`, `openai` are excluded (no configured pricing).

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/cost-trend-dark.svg">
  <img alt="Cost per test by provider over runs — mistral highest, deepseek lowest" src="assets/smoke-health/cost-trend-light.svg" width="760">
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
  <img alt="Failure categories by provider — anthropic has the most failures (132)" src="assets/smoke-health/failure-split-light.svg" width="760">
</picture>

<details>
<summary><b>Failure detail</b> — counts, share & sample signatures</summary>

| Provider | Category | Failures | % of fails | Sample signature |
|---|---|--:|--:|---|
| `anthropic` | deterministic | 128 | 97.0 | `business rule task()::400 - {"type":"error","error":{"type":"invalid_request_er…` |
| `gemini` | deterministic | 59 | 96.7 | `business rule task()::429 - [{` |
| `openai` | deterministic | 34 | 89.5 | `business rule task()::429 - {` |
| `deepseek` | classification | 29 | 90.6 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | classification | 17 | 85.0 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | classification | 4 | 10.5 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 3.0 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `deepseek` | deterministic | 3 | 9.4 | `escalation end()::TIMER (boundaryEvent) requires detail` |
| `llama` | deterministic | 2 | 10.0 | `event-based gateway()::RECEIVE (act-wait-for-response) requires messageName` |
| `gemini` | classification | 2 | 3.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `mistral` | deterministic | 1 | 50.0 | `event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind` |
| `mistral` | infra | 1 | 50.0 | `timer boundary event()::timer boundary event() timed out after 240 seconds` |
| `llama` | infra | 1 | 5.0 | `exclusive gateway()::exclusive gateway() timed out after 240 seconds` |

</details>

## Flaky tests

> [!WARNING]
> Fails **across providers** ⇒ the test or prompt is suspect. Fails on **one provider** ⇒ a model limit.

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `error boundary event()` | `██████████▌░` 43.8% | 5 — anthropic, deepseek, gemini, llama, openai | 64 |
| `event-based gateway()` | `█████░░░░░░░` 20.9% | 3 — anthropic, llama, openai | 67 |
| `signal end()` | `████▋░░░░░░░` 19.4% | 5 — anthropic, deepseek, gemini, llama, openai | 62 |
| `intermediate signal throw()` | `████▋░░░░░░░` 19.4% | 4 — anthropic, gemini, llama, openai | 62 |
| `escalation end()` | `████▌░░░░░░░` 18.8% | 3 — anthropic, deepseek, gemini | 64 |
| `standard loop activity()` | `████▌░░░░░░░` 18.8% | 3 — anthropic, deepseek, gemini | 64 |

<details>
<summary>28 more flaky tests (≤ 18.5% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `parallel gateway()` | `████▌░░░░░░░` 18.5% | 3 — anthropic, gemini, llama | 65 |
| `business rule task()` | `███▉░░░░░░░░` 16.1% | 3 — anthropic, gemini, openai | 62 |
| `data objects and stores()` | `███▉░░░░░░░░` 16.1% | 3 — anthropic, gemini, openai | 62 |
| `manual task()` | `███▉░░░░░░░░` 16.1% | 3 — anthropic, gemini, openai | 62 |
| `message start()` | `███▉░░░░░░░░` 16.1% | 3 — anthropic, gemini, openai | 62 |
| `sequential multi-instance activity()` | `███▉░░░░░░░░` 16.1% | 3 — anthropic, gemini, openai | 62 |
| `timer start()` | `███▉░░░░░░░░` 16.1% | 3 — anthropic, gemini, openai | 62 |
| `escalation boundary event()` | `███▊░░░░░░░░` 15.4% | 4 — anthropic, deepseek, gemini, openai | 65 |
| `intermediate message throw()` | `███▎░░░░░░░░` 13.6% | 5 — anthropic, deepseek, gemini, llama, openai | 66 |
| `exclusive gateway()` | `██▋░░░░░░░░░` 10.9% | 3 — anthropic, gemini, llama | 64 |
| `message end()` | `██▌░░░░░░░░░` 10.6% | 3 — anthropic, gemini, openai | 66 |
| `receive task()` | `██▌░░░░░░░░░` 10.6% | 3 — anthropic, gemini, openai | 66 |
| `signal start()` | `██▌░░░░░░░░░` 10.6% | 3 — anthropic, gemini, openai | 66 |
| `intermediate escalation throw()` | `██▌░░░░░░░░░` 10.4% | 3 — anthropic, deepseek, openai | 67 |
| `terminate end()` | `██▌░░░░░░░░░` 10.4% | 2 — anthropic, openai | 67 |
| `script task()` | `██▎░░░░░░░░░` 9.4% | 2 — anthropic, gemini | 64 |
| `event subprocess()` | `██▎░░░░░░░░░` 9.2% | 3 — anthropic, gemini, mistral | 65 |
| `timer boundary event()` | `██▎░░░░░░░░░` 9.2% | 3 — anthropic, gemini, mistral | 65 |
| `inclusive gateway()` | `██▏░░░░░░░░░` 9.0% | 2 — anthropic, openai | 67 |
| `service task()` | `██▏░░░░░░░░░` 9.0% | 2 — anthropic, openai | 67 |
| `user task()` | `██▏░░░░░░░░░` 9.0% | 2 — anthropic, openai | 67 |
| `error end()` | `█▉░░░░░░░░░░` 7.7% | 2 — anthropic, gemini | 65 |
| `pools and lanes from distinct actors()` | `█▉░░░░░░░░░░` 7.7% | 2 — anthropic, gemini | 65 |
| `parallel multi-instance activity()` | `█▌░░░░░░░░░░` 6.2% | 4 — anthropic, deepseek, gemini, openai | 65 |
| `call activity()` | `█▍░░░░░░░░░░` 5.7% | 3 — anthropic, gemini, openai | 53 |
| `embedded subprocess()` | `█▏░░░░░░░░░░` 4.6% | 3 — anthropic, gemini, openai | 65 |
| `exclusive gateway with default branch()` | `█▏░░░░░░░░░░` 4.6% | 3 — anthropic, gemini, openai | 65 |
| `send task()` | `█▏░░░░░░░░░░` 4.6% | 3 — anthropic, gemini, openai | 65 |

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
