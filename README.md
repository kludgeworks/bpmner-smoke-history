# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 87.0% average pass rate · 297 total failures · 34 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.2%, llama 94.5%, deepseek 90.2%, openai 88.9%, gemini 83.3%, anthropic 66%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.2% | 3 | $0.4774 | 23.25M | `mistral-large-2411, mistral-small-2506` |
| `llama` | `█████████████▎` 94.5% | 20 | $0.2283 | 16.55M | `meta-llama/llama-3.3-70b-instruct` |
| `deepseek` | `████████████▋░` 90.2% | 32 | $0.0509 | 18.27M | `deepseek-chat` |
| `openai` | `████████████▌░` 88.9% | 43 | n/a | 16.82M | `gpt-4.1, gpt-4.1-mini` |
| `gemini` | `███████████▋░░` 83.3% | 61 | n/a | 16.72M | `gemini-2.5-flash, gemini-2.5-pro` |
| `anthropic` | `█████████▎░░░░` 66.0% | 138 | n/a | 7.16M | `claude-haiku-4-5, claude-sonnet-4-6` |

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
  <img alt="Failure categories by provider — anthropic has the most failures (138)" src="assets/smoke-health/failure-split-light.svg" width="760">
</picture>

<details>
<summary><b>Failure detail</b> — counts, share & sample signatures</summary>

| Provider | Category | Failures | % of fails | Sample signature |
|---|---|--:|--:|---|
| `anthropic` | deterministic | 134 | 97.1 | `business rule task()::400 - {"type":"error","error":{"type":"invalid_request_er…` |
| `gemini` | deterministic | 59 | 96.7 | `business rule task()::429 - [{` |
| `openai` | deterministic | 39 | 90.7 | `business rule task()::429 - {` |
| `deepseek` | classification | 29 | 90.6 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | classification | 17 | 85.0 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | classification | 4 | 9.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 2.9 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `deepseek` | deterministic | 3 | 9.4 | `escalation end()::TIMER (boundaryEvent) requires detail` |
| `mistral` | infra | 2 | 66.7 | `terminate end()::terminate end() timed out after 240 seconds` |
| `llama` | deterministic | 2 | 10.0 | `event-based gateway()::RECEIVE (act-wait-for-response) requires messageName` |
| `gemini` | classification | 2 | 3.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `mistral` | deterministic | 1 | 33.3 | `event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind` |
| `llama` | infra | 1 | 5.0 | `exclusive gateway()::exclusive gateway() timed out after 240 seconds` |

</details>

## Flaky tests

> [!WARNING]
> Fails **across providers** ⇒ the test or prompt is suspect. Fails on **one provider** ⇒ a model limit.

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `error boundary event()` | `██████████▊░` 44.6% | 5 — anthropic, deepseek, gemini, llama, openai | 65 |
| `event-based gateway()` | `█████░░░░░░░` 20.6% | 3 — anthropic, llama, openai | 68 |
| `escalation end()` | `████▊░░░░░░░` 20.0% | 4 — anthropic, deepseek, gemini, openai | 65 |
| `standard loop activity()` | `████▊░░░░░░░` 20.0% | 4 — anthropic, deepseek, gemini, openai | 65 |
| `signal end()` | `████▌░░░░░░░` 19.0% | 5 — anthropic, deepseek, gemini, llama, openai | 63 |
| `intermediate signal throw()` | `████▌░░░░░░░` 19.0% | 4 — anthropic, gemini, llama, openai | 63 |

<details>
<summary>28 more flaky tests (≤ 18.2% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `parallel gateway()` | `████▍░░░░░░░` 18.2% | 3 — anthropic, gemini, llama | 66 |
| `escalation boundary event()` | `████░░░░░░░░` 16.7% | 4 — anthropic, deepseek, gemini, openai | 66 |
| `business rule task()` | `███▉░░░░░░░░` 15.9% | 3 — anthropic, gemini, openai | 63 |
| `data objects and stores()` | `███▉░░░░░░░░` 15.9% | 3 — anthropic, gemini, openai | 63 |
| `manual task()` | `███▉░░░░░░░░` 15.9% | 3 — anthropic, gemini, openai | 63 |
| `message start()` | `███▉░░░░░░░░` 15.9% | 3 — anthropic, gemini, openai | 63 |
| `sequential multi-instance activity()` | `███▉░░░░░░░░` 15.9% | 3 — anthropic, gemini, openai | 63 |
| `timer start()` | `███▉░░░░░░░░` 15.9% | 3 — anthropic, gemini, openai | 63 |
| `intermediate message throw()` | `███▎░░░░░░░░` 13.4% | 5 — anthropic, deepseek, gemini, llama, openai | 67 |
| `exclusive gateway()` | `███░░░░░░░░░` 12.3% | 4 — anthropic, gemini, llama, openai | 65 |
| `terminate end()` | `██▉░░░░░░░░░` 11.8% | 3 — anthropic, mistral, openai | 68 |
| `script task()` | `██▋░░░░░░░░░` 10.8% | 3 — anthropic, gemini, openai | 65 |
| `message end()` | `██▌░░░░░░░░░` 10.4% | 3 — anthropic, gemini, openai | 67 |
| `receive task()` | `██▌░░░░░░░░░` 10.4% | 3 — anthropic, gemini, openai | 67 |
| `signal start()` | `██▌░░░░░░░░░` 10.4% | 3 — anthropic, gemini, openai | 67 |
| `intermediate escalation throw()` | `██▌░░░░░░░░░` 10.3% | 3 — anthropic, deepseek, openai | 68 |
| `event subprocess()` | `██▏░░░░░░░░░` 9.1% | 3 — anthropic, gemini, mistral | 66 |
| `timer boundary event()` | `██▏░░░░░░░░░` 9.1% | 3 — anthropic, gemini, mistral | 66 |
| `inclusive gateway()` | `██▏░░░░░░░░░` 8.8% | 2 — anthropic, openai | 68 |
| `service task()` | `██▏░░░░░░░░░` 8.8% | 2 — anthropic, openai | 68 |
| `user task()` | `██▏░░░░░░░░░` 8.8% | 2 — anthropic, openai | 68 |
| `parallel multi-instance activity()` | `█▉░░░░░░░░░░` 7.6% | 4 — anthropic, deepseek, gemini, openai | 66 |
| `error end()` | `█▉░░░░░░░░░░` 7.6% | 2 — anthropic, gemini | 66 |
| `pools and lanes from distinct actors()` | `█▉░░░░░░░░░░` 7.6% | 2 — anthropic, gemini | 66 |
| `call activity()` | `█▊░░░░░░░░░░` 7.4% | 3 — anthropic, gemini, openai | 54 |
| `embedded subprocess()` | `█▌░░░░░░░░░░` 6.1% | 3 — anthropic, gemini, openai | 66 |
| `exclusive gateway with default branch()` | `█▌░░░░░░░░░░` 6.1% | 3 — anthropic, gemini, openai | 66 |
| `send task()` | `█▌░░░░░░░░░░` 6.1% | 3 — anthropic, gemini, openai | 66 |

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
