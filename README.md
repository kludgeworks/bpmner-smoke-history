# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 86.5% average pass rate · 322 total failures · 34 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.2%, llama 94.3%, deepseek 90.1%, openai 88.3%, gemini 83.9%, anthropic 63.4%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.2% | 3 | $0.4759 | 24.13M | `mistral-large-2411, mistral-small-2506` |
| `llama` | `█████████████▎` 94.3% | 22 | $0.2309 | 17.53M | `meta-llama/llama-3.3-70b-instruct` |
| `deepseek` | `████████████▋░` 90.1% | 34 | $0.0510 | 19.24M | `deepseek-chat` |
| `openai` | `████████████▍░` 88.3% | 47 | n/a | 17.26M | `gpt-4.1, gpt-4.1-mini` |
| `gemini` | `███████████▊░░` 83.9% | 61 | n/a | 17.54M | `gemini-2.5-flash, gemini-2.5-pro` |
| `anthropic` | `████████▉░░░░░` 63.4% | 155 | n/a | 7.16M | `claude-haiku-4-5, claude-sonnet-4-6` |

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
  <img alt="Failure categories by provider — anthropic has the most failures (155)" src="assets/smoke-health/failure-split-light.svg" width="760">
</picture>

<details>
<summary><b>Failure detail</b> — counts, share & sample signatures</summary>

| Provider | Category | Failures | % of fails | Sample signature |
|---|---|--:|--:|---|
| `anthropic` | deterministic | 151 | 97.4 | `business rule task()::400 - {"type":"error","error":{"type":"invalid_request_er…` |
| `gemini` | deterministic | 59 | 96.7 | `business rule task()::429 - [{` |
| `openai` | deterministic | 43 | 91.5 | `business rule task()::429 - {` |
| `deepseek` | classification | 31 | 91.2 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | classification | 18 | 81.8 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | classification | 4 | 8.5 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 2.6 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | deterministic | 3 | 13.6 | `event-based gateway()::RECEIVE (act-wait-for-response) requires messageName` |
| `deepseek` | deterministic | 3 | 8.8 | `escalation end()::TIMER (boundaryEvent) requires detail` |
| `mistral` | infra | 2 | 66.7 | `terminate end()::terminate end() timed out after 240 seconds` |
| `gemini` | classification | 2 | 3.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `mistral` | deterministic | 1 | 33.3 | `event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind` |
| `llama` | infra | 1 | 4.5 | `exclusive gateway()::exclusive gateway() timed out after 240 seconds` |

</details>

## Flaky tests

> [!WARNING]
> Fails **across providers** ⇒ the test or prompt is suspect. Fails on **one provider** ⇒ a model limit.

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `error boundary event()` | `███████████░` 45.6% | 5 — anthropic, deepseek, gemini, llama, openai | 68 |
| `event-based gateway()` | `█████▍░░░░░░` 22.5% | 3 — anthropic, llama, openai | 71 |
| `intermediate signal throw()` | `████▊░░░░░░░` 19.7% | 4 — anthropic, gemini, llama, openai | 66 |
| `escalation end()` | `████▋░░░░░░░` 19.1% | 4 — anthropic, deepseek, gemini, openai | 68 |
| `standard loop activity()` | `████▋░░░░░░░` 19.1% | 4 — anthropic, deepseek, gemini, openai | 68 |
| `parallel gateway()` | `████▌░░░░░░░` 18.8% | 3 — anthropic, gemini, llama | 69 |

<details>
<summary>28 more flaky tests (≤ 18.2% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `signal end()` | `████▍░░░░░░░` 18.2% | 5 — anthropic, deepseek, gemini, llama, openai | 66 |
| `escalation boundary event()` | `███▉░░░░░░░░` 15.9% | 4 — anthropic, deepseek, gemini, openai | 69 |
| `business rule task()` | `███▋░░░░░░░░` 15.2% | 3 — anthropic, gemini, openai | 66 |
| `data objects and stores()` | `███▋░░░░░░░░` 15.2% | 3 — anthropic, gemini, openai | 66 |
| `manual task()` | `███▋░░░░░░░░` 15.2% | 3 — anthropic, gemini, openai | 66 |
| `message start()` | `███▋░░░░░░░░` 15.2% | 3 — anthropic, gemini, openai | 66 |
| `sequential multi-instance activity()` | `███▋░░░░░░░░` 15.2% | 3 — anthropic, gemini, openai | 66 |
| `timer start()` | `███▋░░░░░░░░` 15.2% | 3 — anthropic, gemini, openai | 66 |
| `intermediate message throw()` | `███▍░░░░░░░░` 14.3% | 5 — anthropic, deepseek, gemini, llama, openai | 70 |
| `intermediate escalation throw()` | `███▍░░░░░░░░` 14.1% | 4 — anthropic, deepseek, llama, openai | 71 |
| `terminate end()` | `███▍░░░░░░░░` 14.1% | 3 — anthropic, mistral, openai | 71 |
| `exclusive gateway()` | `██▉░░░░░░░░░` 11.8% | 4 — anthropic, gemini, llama, openai | 68 |
| `message end()` | `██▊░░░░░░░░░` 11.4% | 3 — anthropic, gemini, openai | 70 |
| `receive task()` | `██▊░░░░░░░░░` 11.4% | 3 — anthropic, gemini, openai | 70 |
| `signal start()` | `██▊░░░░░░░░░` 11.4% | 3 — anthropic, gemini, openai | 70 |
| `inclusive gateway()` | `██▊░░░░░░░░░` 11.3% | 2 — anthropic, openai | 71 |
| `service task()` | `██▊░░░░░░░░░` 11.3% | 2 — anthropic, openai | 71 |
| `user task()` | `██▊░░░░░░░░░` 11.3% | 2 — anthropic, openai | 71 |
| `script task()` | `██▌░░░░░░░░░` 10.3% | 3 — anthropic, gemini, openai | 68 |
| `event subprocess()` | `██▍░░░░░░░░░` 10.1% | 3 — anthropic, gemini, mistral | 69 |
| `timer boundary event()` | `██▍░░░░░░░░░` 10.1% | 3 — anthropic, gemini, mistral | 69 |
| `error end()` | `██▏░░░░░░░░░` 8.7% | 2 — anthropic, gemini | 69 |
| `pools and lanes from distinct actors()` | `██▏░░░░░░░░░` 8.7% | 2 — anthropic, gemini | 69 |
| `parallel multi-instance activity()` | `█▊░░░░░░░░░░` 7.2% | 4 — anthropic, deepseek, gemini, openai | 69 |
| `call activity()` | `█▋░░░░░░░░░░` 7.0% | 3 — anthropic, gemini, openai | 57 |
| `embedded subprocess()` | `█▍░░░░░░░░░░` 5.8% | 3 — anthropic, gemini, openai | 69 |
| `exclusive gateway with default branch()` | `█▍░░░░░░░░░░` 5.8% | 3 — anthropic, gemini, openai | 69 |
| `send task()` | `█▍░░░░░░░░░░` 5.8% | 3 — anthropic, gemini, openai | 69 |

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
