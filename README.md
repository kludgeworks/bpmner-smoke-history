# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 85.5% average pass rate · 353 total failures · 34 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.3%, llama 94.4%, deepseek 90%, openai 89.7%, gemini 82.9%, anthropic 56.9%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.3% | 3 | $0.4760 | 26.90M | `mistral-large-2411, mistral-small-2506` |
| `llama` | `█████████████▎` 94.4% | 24 | $0.2298 | 19.53M | `meta-llama/llama-3.3-70b-instruct` |
| `deepseek` | `████████████▋░` 90.0% | 39 | $0.0504 | 21.84M | `deepseek-chat` |
| `openai` | `████████████▌░` 89.7% | 47 | n/a | 19.81M | `gpt-4.1, gpt-4.1-mini` |
| `gemini` | `███████████▋░░` 82.9% | 63 | n/a | 19.80M | `gemini-2.5-flash, gemini-2.5-pro` |
| `anthropic` | `████████░░░░░░` 56.9% | 177 | n/a | 7.16M | `claude-haiku-4-5, claude-sonnet-4-6` |

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
  <img alt="Failure categories by provider — anthropic has the most failures (177)" src="assets/smoke-health/failure-split-light.svg" width="760">
</picture>

<details>
<summary><b>Failure detail</b> — counts, share & sample signatures</summary>

| Provider | Category | Failures | % of fails | Sample signature |
|---|---|--:|--:|---|
| `anthropic` | deterministic | 173 | 97.7 | `business rule task()::400 - {"type":"error","error":{"type":"invalid_request_er…` |
| `gemini` | deterministic | 59 | 93.7 | `business rule task()::429 - [{` |
| `openai` | deterministic | 43 | 91.5 | `business rule task()::429 - {` |
| `deepseek` | classification | 36 | 92.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | classification | 20 | 83.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | classification | 4 | 8.5 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `gemini` | classification | 4 | 6.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 2.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | deterministic | 3 | 12.5 | `event-based gateway()::RECEIVE (act-wait-for-response) requires messageName` |
| `deepseek` | deterministic | 3 | 7.7 | `escalation end()::TIMER (boundaryEvent) requires detail` |
| `mistral` | infra | 2 | 66.7 | `terminate end()::terminate end() timed out after 240 seconds` |
| `mistral` | deterministic | 1 | 33.3 | `event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind` |
| `llama` | infra | 1 | 4.2 | `exclusive gateway()::exclusive gateway() timed out after 240 seconds` |

</details>

## Flaky tests

> [!WARNING]
> Fails **across providers** ⇒ the test or prompt is suspect. Fails on **one provider** ⇒ a model limit.

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `error boundary event()` | `██████████▋░` 44.2% | 5 — anthropic, deepseek, gemini, llama, openai | 77 |
| `event-based gateway()` | `████▊░░░░░░░` 20.0% | 3 — anthropic, llama, openai | 80 |
| `escalation end()` | `████▋░░░░░░░` 19.5% | 4 — anthropic, deepseek, gemini, openai | 77 |
| `standard loop activity()` | `████▋░░░░░░░` 19.5% | 4 — anthropic, deepseek, gemini, openai | 77 |
| `intermediate signal throw()` | `████▌░░░░░░░` 18.9% | 4 — anthropic, gemini, llama, openai | 74 |
| `parallel gateway()` | `████▍░░░░░░░` 18.2% | 3 — anthropic, gemini, llama | 77 |

<details>
<summary>28 more flaky tests (≤ 17.6% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `signal end()` | `████▎░░░░░░░` 17.6% | 5 — anthropic, deepseek, gemini, llama, openai | 74 |
| `intermediate message throw()` | `████░░░░░░░░` 16.5% | 5 — anthropic, deepseek, gemini, llama, openai | 79 |
| `escalation boundary event()` | `███▊░░░░░░░░` 15.4% | 4 — anthropic, deepseek, gemini, openai | 78 |
| `business rule task()` | `███▋░░░░░░░░` 14.9% | 3 — anthropic, gemini, openai | 74 |
| `data objects and stores()` | `███▋░░░░░░░░` 14.9% | 3 — anthropic, gemini, openai | 74 |
| `manual task()` | `███▋░░░░░░░░` 14.9% | 3 — anthropic, gemini, openai | 74 |
| `message start()` | `███▋░░░░░░░░` 14.9% | 3 — anthropic, gemini, openai | 74 |
| `sequential multi-instance activity()` | `███▋░░░░░░░░` 14.9% | 3 — anthropic, gemini, openai | 74 |
| `timer start()` | `███▋░░░░░░░░` 14.9% | 3 — anthropic, gemini, openai | 74 |
| `message end()` | `███░░░░░░░░░` 12.7% | 3 — anthropic, gemini, openai | 79 |
| `receive task()` | `███░░░░░░░░░` 12.7% | 3 — anthropic, gemini, openai | 79 |
| `signal start()` | `███░░░░░░░░░` 12.7% | 3 — anthropic, gemini, openai | 79 |
| `intermediate escalation throw()` | `███░░░░░░░░░` 12.5% | 4 — anthropic, deepseek, llama, openai | 80 |
| `terminate end()` | `███░░░░░░░░░` 12.5% | 3 — anthropic, mistral, openai | 80 |
| `exclusive gateway()` | `██▌░░░░░░░░░` 10.4% | 4 — anthropic, gemini, llama, openai | 77 |
| `inclusive gateway()` | `██▍░░░░░░░░░` 10.0% | 2 — anthropic, openai | 80 |
| `service task()` | `██▍░░░░░░░░░` 10.0% | 2 — anthropic, openai | 80 |
| `user task()` | `██▍░░░░░░░░░` 10.0% | 2 — anthropic, openai | 80 |
| `event subprocess()` | `██▏░░░░░░░░░` 9.1% | 3 — anthropic, gemini, mistral | 77 |
| `script task()` | `██▏░░░░░░░░░` 9.1% | 3 — anthropic, gemini, openai | 77 |
| `timer boundary event()` | `██▏░░░░░░░░░` 9.1% | 3 — anthropic, gemini, mistral | 77 |
| `error end()` | `█▉░░░░░░░░░░` 7.8% | 2 — anthropic, gemini | 77 |
| `pools and lanes from distinct actors()` | `█▉░░░░░░░░░░` 7.8% | 2 — anthropic, gemini | 77 |
| `parallel multi-instance activity()` | `█▉░░░░░░░░░░` 7.7% | 4 — anthropic, deepseek, gemini, openai | 78 |
| `call activity()` | `█▉░░░░░░░░░░` 7.6% | 3 — anthropic, gemini, openai | 66 |
| `embedded subprocess()` | `█▌░░░░░░░░░░` 6.4% | 3 — anthropic, gemini, openai | 78 |
| `exclusive gateway with default branch()` | `█▌░░░░░░░░░░` 6.4% | 3 — anthropic, gemini, openai | 78 |
| `send task()` | `█▌░░░░░░░░░░` 6.4% | 3 — anthropic, gemini, openai | 78 |

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
