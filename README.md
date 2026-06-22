# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 87.7% average pass rate · 270 total failures · 34 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.4%, llama 94.3%, openai 91.5%, deepseek 90.1%, gemini 82.7%, anthropic 68.4%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.4% | 2 | $0.4744 | 22.58M | `mistral-large-2411, mistral-small-2506` |
| `llama` | `█████████████▎` 94.3% | 20 | $0.2303 | 16.18M | `meta-llama/llama-3.3-70b-instruct` |
| `openai` | `████████████▊░` 91.5% | 32 | n/a | 16.82M | `gpt-4.1, gpt-4.1-mini` |
| `deepseek` | `████████████▋░` 90.1% | 31 | $0.0511 | 17.71M | `deepseek-chat` |
| `gemini` | `███████████▋░░` 82.7% | 61 | n/a | 15.90M | `gemini-2.5-flash, gemini-2.5-pro` |
| `anthropic` | `█████████▋░░░░` 68.4% | 124 | n/a | 7.16M | `claude-haiku-4-5, claude-sonnet-4-6` |

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
  <img alt="Failure categories by provider — anthropic has the most failures (124)" src="assets/smoke-health/failure-split-light.svg" width="760">
</picture>

<details>
<summary><b>Failure detail</b> — counts, share & sample signatures</summary>

| Provider | Category | Failures | % of fails | Sample signature |
|---|---|--:|--:|---|
| `anthropic` | deterministic | 120 | 96.8 | `business rule task()::400 - {"type":"error","error":{"type":"invalid_request_er…` |
| `gemini` | deterministic | 59 | 96.7 | `business rule task()::429 - [{` |
| `deepseek` | classification | 28 | 90.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | deterministic | 28 | 87.5 | `business rule task()::429 - {` |
| `llama` | classification | 17 | 85.0 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | classification | 4 | 12.5 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 3.2 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `deepseek` | deterministic | 3 | 9.7 | `escalation end()::TIMER (boundaryEvent) requires detail` |
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
| `error boundary event()` | `██████████▋░` 44.4% | 5 — anthropic, deepseek, gemini, llama, openai | 63 |
| `event-based gateway()` | `████▊░░░░░░░` 19.7% | 3 — anthropic, llama, openai | 66 |
| `escalation end()` | `████▌░░░░░░░` 19.0% | 3 — anthropic, deepseek, gemini | 63 |
| `standard loop activity()` | `████▌░░░░░░░` 19.0% | 3 — anthropic, deepseek, gemini | 63 |
| `parallel gateway()` | `████▌░░░░░░░` 18.8% | 3 — anthropic, gemini, llama | 64 |
| `signal end()` | `████▍░░░░░░░` 18.0% | 5 — anthropic, deepseek, gemini, llama, openai | 61 |

<details>
<summary>28 more flaky tests (≤ 18.0% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `intermediate signal throw()` | `████▍░░░░░░░` 18.0% | 4 — anthropic, gemini, llama, openai | 61 |
| `business rule task()` | `███▌░░░░░░░░` 14.8% | 3 — anthropic, gemini, openai | 61 |
| `data objects and stores()` | `███▌░░░░░░░░` 14.8% | 3 — anthropic, gemini, openai | 61 |
| `manual task()` | `███▌░░░░░░░░` 14.8% | 3 — anthropic, gemini, openai | 61 |
| `message start()` | `███▌░░░░░░░░` 14.8% | 3 — anthropic, gemini, openai | 61 |
| `sequential multi-instance activity()` | `███▌░░░░░░░░` 14.8% | 3 — anthropic, gemini, openai | 61 |
| `timer start()` | `███▌░░░░░░░░` 14.8% | 3 — anthropic, gemini, openai | 61 |
| `escalation boundary event()` | `███▍░░░░░░░░` 14.1% | 4 — anthropic, deepseek, gemini, openai | 64 |
| `intermediate message throw()` | `███▎░░░░░░░░` 13.8% | 5 — anthropic, deepseek, gemini, llama, openai | 65 |
| `exclusive gateway()` | `██▋░░░░░░░░░` 11.1% | 3 — anthropic, gemini, llama | 63 |
| `message end()` | `██▋░░░░░░░░░` 10.8% | 3 — anthropic, gemini, openai | 65 |
| `receive task()` | `██▋░░░░░░░░░` 10.8% | 3 — anthropic, gemini, openai | 65 |
| `signal start()` | `██▋░░░░░░░░░` 10.8% | 3 — anthropic, gemini, openai | 65 |
| `script task()` | `██▎░░░░░░░░░` 9.5% | 2 — anthropic, gemini | 63 |
| `event subprocess()` | `██▎░░░░░░░░░` 9.4% | 3 — anthropic, gemini, mistral | 64 |
| `timer boundary event()` | `██▎░░░░░░░░░` 9.4% | 3 — anthropic, gemini, mistral | 64 |
| `intermediate escalation throw()` | `██▏░░░░░░░░░` 9.1% | 2 — anthropic, deepseek | 66 |
| `terminate end()` | `██▏░░░░░░░░░` 9.1% | 2 — anthropic, openai | 66 |
| `error end()` | `█▉░░░░░░░░░░` 7.8% | 2 — anthropic, gemini | 64 |
| `pools and lanes from distinct actors()` | `█▉░░░░░░░░░░` 7.8% | 2 — anthropic, gemini | 64 |
| `inclusive gateway()` | `█▉░░░░░░░░░░` 7.6% | 1 — anthropic | 66 |
| `service task()` | `█▉░░░░░░░░░░` 7.6% | 1 — anthropic | 66 |
| `user task()` | `█▉░░░░░░░░░░` 7.6% | 1 — anthropic | 66 |
| `parallel multi-instance activity()` | `█▌░░░░░░░░░░` 6.3% | 4 — anthropic, deepseek, gemini, openai | 64 |
| `call activity()` | `█▍░░░░░░░░░░` 5.8% | 3 — anthropic, gemini, openai | 52 |
| `embedded subprocess()` | `█▏░░░░░░░░░░` 4.7% | 3 — anthropic, gemini, openai | 64 |
| `exclusive gateway with default branch()` | `█▏░░░░░░░░░░` 4.7% | 3 — anthropic, gemini, openai | 64 |
| `send task()` | `█▏░░░░░░░░░░` 4.7% | 3 — anthropic, gemini, openai | 64 |

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
