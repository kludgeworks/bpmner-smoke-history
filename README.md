# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 86.4% average pass rate · 341 total failures · 34 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.3%, llama 94.1%, deepseek 90.6%, openai 88.8%, gemini 84.7%, anthropic 60.8%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.3% | 3 | $0.4737 | 24.70M | `mistral-large-2411, mistral-small-2506` |
| `llama` | `█████████████▏` 94.1% | 23 | $0.2294 | 17.94M | `meta-llama/llama-3.3-70b-instruct` |
| `deepseek` | `████████████▋░` 90.6% | 34 | $0.0510 | 20.23M | `deepseek-chat` |
| `openai` | `████████████▍░` 88.8% | 47 | n/a | 18.04M | `gpt-4.1, gpt-4.1-mini` |
| `gemini` | `███████████▉░░` 84.7% | 61 | n/a | 18.56M | `gemini-2.5-flash, gemini-2.5-pro` |
| `anthropic` | `████████▌░░░░░` 60.8% | 173 | n/a | 7.16M | `claude-haiku-4-5, claude-sonnet-4-6` |

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
  <img alt="Failure categories by provider — anthropic has the most failures (173)" src="assets/smoke-health/failure-split-light.svg" width="760">
</picture>

<details>
<summary><b>Failure detail</b> — counts, share & sample signatures</summary>

| Provider | Category | Failures | % of fails | Sample signature |
|---|---|--:|--:|---|
| `anthropic` | deterministic | 169 | 97.7 | `business rule task()::400 - {"type":"error","error":{"type":"invalid_request_er…` |
| `gemini` | deterministic | 59 | 96.7 | `business rule task()::429 - [{` |
| `openai` | deterministic | 43 | 91.5 | `business rule task()::429 - {` |
| `deepseek` | classification | 31 | 91.2 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | classification | 19 | 82.6 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | classification | 4 | 8.5 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 2.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | deterministic | 3 | 13.0 | `event-based gateway()::RECEIVE (act-wait-for-response) requires messageName` |
| `deepseek` | deterministic | 3 | 8.8 | `escalation end()::TIMER (boundaryEvent) requires detail` |
| `mistral` | infra | 2 | 66.7 | `terminate end()::terminate end() timed out after 240 seconds` |
| `gemini` | classification | 2 | 3.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `mistral` | deterministic | 1 | 33.3 | `event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind` |
| `llama` | infra | 1 | 4.3 | `exclusive gateway()::exclusive gateway() timed out after 240 seconds` |

</details>

## Flaky tests

> [!WARNING]
> Fails **across providers** ⇒ the test or prompt is suspect. Fails on **one provider** ⇒ a model limit.

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `error boundary event()` | `██████████▌░` 43.7% | 5 — anthropic, deepseek, gemini, llama, openai | 71 |
| `event-based gateway()` | `█████▏░░░░░░` 21.6% | 3 — anthropic, llama, openai | 74 |
| `intermediate signal throw()` | `█████░░░░░░░` 20.6% | 4 — anthropic, gemini, llama, openai | 68 |
| `signal end()` | `████▋░░░░░░░` 19.1% | 5 — anthropic, deepseek, gemini, llama, openai | 68 |
| `escalation end()` | `████▍░░░░░░░` 18.3% | 4 — anthropic, deepseek, gemini, openai | 71 |
| `standard loop activity()` | `████▍░░░░░░░` 18.3% | 4 — anthropic, deepseek, gemini, openai | 71 |

<details>
<summary>28 more flaky tests (≤ 18.3% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `parallel gateway()` | `████▍░░░░░░░` 18.3% | 3 — anthropic, gemini, llama | 71 |
| `escalation boundary event()` | `████░░░░░░░░` 16.7% | 4 — anthropic, deepseek, gemini, openai | 72 |
| `intermediate message throw()` | `███▉░░░░░░░░` 16.4% | 5 — anthropic, deepseek, gemini, llama, openai | 73 |
| `business rule task()` | `███▉░░░░░░░░` 16.2% | 3 — anthropic, gemini, openai | 68 |
| `data objects and stores()` | `███▉░░░░░░░░` 16.2% | 3 — anthropic, gemini, openai | 68 |
| `manual task()` | `███▉░░░░░░░░` 16.2% | 3 — anthropic, gemini, openai | 68 |
| `message start()` | `███▉░░░░░░░░` 16.2% | 3 — anthropic, gemini, openai | 68 |
| `sequential multi-instance activity()` | `███▉░░░░░░░░` 16.2% | 3 — anthropic, gemini, openai | 68 |
| `timer start()` | `███▉░░░░░░░░` 16.2% | 3 — anthropic, gemini, openai | 68 |
| `intermediate escalation throw()` | `███▎░░░░░░░░` 13.5% | 4 — anthropic, deepseek, llama, openai | 74 |
| `terminate end()` | `███▎░░░░░░░░` 13.5% | 3 — anthropic, mistral, openai | 74 |
| `message end()` | `███░░░░░░░░░` 12.3% | 3 — anthropic, gemini, openai | 73 |
| `receive task()` | `███░░░░░░░░░` 12.3% | 3 — anthropic, gemini, openai | 73 |
| `signal start()` | `███░░░░░░░░░` 12.3% | 3 — anthropic, gemini, openai | 73 |
| `exclusive gateway()` | `██▊░░░░░░░░░` 11.3% | 4 — anthropic, gemini, llama, openai | 71 |
| `inclusive gateway()` | `██▋░░░░░░░░░` 10.8% | 2 — anthropic, openai | 74 |
| `service task()` | `██▋░░░░░░░░░` 10.8% | 2 — anthropic, openai | 74 |
| `user task()` | `██▋░░░░░░░░░` 10.8% | 2 — anthropic, openai | 74 |
| `event subprocess()` | `██▍░░░░░░░░░` 9.9% | 3 — anthropic, gemini, mistral | 71 |
| `script task()` | `██▍░░░░░░░░░` 9.9% | 3 — anthropic, gemini, openai | 71 |
| `timer boundary event()` | `██▍░░░░░░░░░` 9.9% | 3 — anthropic, gemini, mistral | 71 |
| `error end()` | `██░░░░░░░░░░` 8.5% | 2 — anthropic, gemini | 71 |
| `pools and lanes from distinct actors()` | `██░░░░░░░░░░` 8.5% | 2 — anthropic, gemini | 71 |
| `parallel multi-instance activity()` | `██░░░░░░░░░░` 8.3% | 4 — anthropic, deepseek, gemini, openai | 72 |
| `call activity()` | `██░░░░░░░░░░` 8.3% | 3 — anthropic, gemini, openai | 60 |
| `embedded subprocess()` | `█▋░░░░░░░░░░` 6.9% | 3 — anthropic, gemini, openai | 72 |
| `exclusive gateway with default branch()` | `█▋░░░░░░░░░░` 6.9% | 3 — anthropic, gemini, openai | 72 |
| `send task()` | `█▋░░░░░░░░░░` 6.9% | 3 — anthropic, gemini, openai | 72 |

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
