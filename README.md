# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 91.8% average pass rate · 133 total failures · 31 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.2%, openai 97.9%, llama 94.3%, deepseek 91%, anthropic 89%, gemini 79.1%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.2% | 2 | $0.4591 | 17.16M | `mistral-large-2411, mistral-small-2506` |
| `openai` | `█████████████▊` 97.9% | 6 | $0.5102 | 13.65M | `gpt-4.1, gpt-4.1-mini` |
| `llama` | `█████████████▎` 94.3% | 15 | $0.2244 | 12.21M | `meta-llama/llama-3.3-70b-instruct` |
| `deepseek` | `████████████▊░` 91.0% | 20 | $0.0488 | 12.04M | `deepseek-chat` |
| `anthropic` | `████████████▌░` 89.0% | 33 | n/a | 7.16M | `claude-haiku-4-5, claude-sonnet-4-6` |
| `gemini` | `███████████▏░░` 79.1% | 57 | n/a | 11.40M | `gemini-2.5-flash, gemini-2.5-pro` |

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
| `anthropic` | deterministic | 29 | 87.9 | `business rule task()::400 - {"type":"error","error":{"type":"invalid_request_er…` |
| `deepseek` | classification | 17 | 85.0 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | classification | 12 | 80.0 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | classification | 4 | 66.7 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 12.1 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `deepseek` | deterministic | 3 | 15.0 | `escalation end()::TIMER (boundaryEvent) requires detail` |
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
| `error boundary event()` | `█████████▌░░` 39.6% | 5 — anthropic, deepseek, gemini, llama, openai | 48 |
| `escalation end()` | `████░░░░░░░░` 16.7% | 3 — anthropic, deepseek, gemini | 48 |
| `signal end()` | `███▊░░░░░░░░` 15.6% | 4 — anthropic, deepseek, gemini, llama | 45 |
| `intermediate signal throw()` | `███▊░░░░░░░░` 15.6% | 3 — anthropic, gemini, llama | 45 |
| `escalation boundary event()` | `███▌░░░░░░░░` 14.6% | 3 — anthropic, deepseek, gemini | 48 |
| `event-based gateway()` | `███▍░░░░░░░░` 14.3% | 2 — llama, openai | 49 |

<details>
<summary>25 more flaky tests (≤ 12.5% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `standard loop activity()` | `███░░░░░░░░░` 12.5% | 3 — anthropic, deepseek, gemini | 48 |
| `business rule task()` | `██▋░░░░░░░░░` 11.1% | 2 — anthropic, gemini | 45 |
| `data objects and stores()` | `██▋░░░░░░░░░` 11.1% | 2 — anthropic, gemini | 45 |
| `manual task()` | `██▋░░░░░░░░░` 11.1% | 2 — anthropic, gemini | 45 |
| `message start()` | `██▋░░░░░░░░░` 11.1% | 2 — anthropic, gemini | 45 |
| `sequential multi-instance activity()` | `██▋░░░░░░░░░` 11.1% | 2 — anthropic, gemini | 45 |
| `timer start()` | `██▋░░░░░░░░░` 11.1% | 2 — anthropic, gemini | 45 |
| `exclusive gateway()` | `██▌░░░░░░░░░` 10.4% | 3 — anthropic, gemini, llama | 48 |
| `parallel gateway()` | `██▌░░░░░░░░░` 10.4% | 3 — anthropic, gemini, llama | 48 |
| `script task()` | `██░░░░░░░░░░` 8.3% | 2 — anthropic, gemini | 48 |
| `event subprocess()` | `█▌░░░░░░░░░░` 6.3% | 3 — anthropic, gemini, mistral | 48 |
| `parallel multi-instance activity()` | `█▌░░░░░░░░░░` 6.3% | 3 — anthropic, deepseek, gemini | 48 |
| `timer boundary event()` | `█▌░░░░░░░░░░` 6.3% | 3 — anthropic, gemini, mistral | 48 |
| `call activity()` | `█▍░░░░░░░░░░` 5.6% | 2 — anthropic, gemini | 36 |
| `embedded subprocess()` | `█░░░░░░░░░░░` 4.2% | 2 — anthropic, gemini | 48 |
| `error end()` | `█░░░░░░░░░░░` 4.2% | 2 — anthropic, gemini | 48 |
| `exclusive gateway with default branch()` | `█░░░░░░░░░░░` 4.2% | 2 — anthropic, gemini | 48 |
| `pools and lanes from distinct actors()` | `█░░░░░░░░░░░` 4.2% | 2 — anthropic, gemini | 48 |
| `send task()` | `█░░░░░░░░░░░` 4.2% | 2 — anthropic, gemini | 48 |
| `intermediate message throw()` | `█░░░░░░░░░░░` 4.1% | 2 — gemini, llama | 49 |
| `intermediate escalation throw()` | `▌░░░░░░░░░░░` 2.0% | 1 — deepseek | 49 |
| `message end()` | `▌░░░░░░░░░░░` 2.0% | 1 — gemini | 49 |
| `receive task()` | `▌░░░░░░░░░░░` 2.0% | 1 — gemini | 49 |
| `signal start()` | `▌░░░░░░░░░░░` 2.0% | 1 — gemini | 49 |
| `terminate end()` | `▌░░░░░░░░░░░` 2.0% | 1 — openai | 49 |

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
