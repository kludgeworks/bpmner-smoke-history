# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 86.7% average pass rate · 314 total failures · 34 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.2%, llama 94.4%, deepseek 90.2%, openai 88.2%, gemini 83.8%, anthropic 64.3%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.2% | 3 | $0.4760 | 23.82M | `mistral-large-2411, mistral-small-2506` |
| `llama` | `█████████████▎` 94.4% | 21 | $0.2299 | 17.19M | `meta-llama/llama-3.3-70b-instruct` |
| `deepseek` | `████████████▋░` 90.2% | 33 | $0.0511 | 18.95M | `deepseek-chat` |
| `openai` | `████████████▍░` 88.2% | 47 | n/a | 17.04M | `gpt-4.1, gpt-4.1-mini` |
| `gemini` | `███████████▊░░` 83.8% | 61 | n/a | 17.32M | `gemini-2.5-flash, gemini-2.5-pro` |
| `anthropic` | `█████████░░░░░` 64.3% | 149 | n/a | 7.16M | `claude-haiku-4-5, claude-sonnet-4-6` |

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
  <img alt="Failure categories by provider — anthropic has the most failures (149)" src="assets/smoke-health/failure-split-light.svg" width="760">
</picture>

<details>
<summary><b>Failure detail</b> — counts, share & sample signatures</summary>

| Provider | Category | Failures | % of fails | Sample signature |
|---|---|--:|--:|---|
| `anthropic` | deterministic | 145 | 97.3 | `business rule task()::400 - {"type":"error","error":{"type":"invalid_request_er…` |
| `gemini` | deterministic | 59 | 96.7 | `business rule task()::429 - [{` |
| `openai` | deterministic | 43 | 91.5 | `business rule task()::429 - {` |
| `deepseek` | classification | 30 | 90.9 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | classification | 17 | 81.0 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | classification | 4 | 8.5 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 2.7 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | deterministic | 3 | 14.3 | `event-based gateway()::RECEIVE (act-wait-for-response) requires messageName` |
| `deepseek` | deterministic | 3 | 9.1 | `escalation end()::TIMER (boundaryEvent) requires detail` |
| `mistral` | infra | 2 | 66.7 | `terminate end()::terminate end() timed out after 240 seconds` |
| `gemini` | classification | 2 | 3.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `mistral` | deterministic | 1 | 33.3 | `event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind` |
| `llama` | infra | 1 | 4.8 | `exclusive gateway()::exclusive gateway() timed out after 240 seconds` |

</details>

## Flaky tests

> [!WARNING]
> Fails **across providers** ⇒ the test or prompt is suspect. Fails on **one provider** ⇒ a model limit.

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `error boundary event()` | `██████████▊░` 44.8% | 5 — anthropic, deepseek, gemini, llama, openai | 67 |
| `event-based gateway()` | `█████▏░░░░░░` 21.4% | 3 — anthropic, llama, openai | 70 |
| `escalation end()` | `████▋░░░░░░░` 19.4% | 4 — anthropic, deepseek, gemini, openai | 67 |
| `standard loop activity()` | `████▋░░░░░░░` 19.4% | 4 — anthropic, deepseek, gemini, openai | 67 |
| `parallel gateway()` | `████▋░░░░░░░` 19.1% | 3 — anthropic, gemini, llama | 68 |
| `signal end()` | `████▌░░░░░░░` 18.5% | 5 — anthropic, deepseek, gemini, llama, openai | 65 |

<details>
<summary>28 more flaky tests (≤ 18.5% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `intermediate signal throw()` | `████▌░░░░░░░` 18.5% | 4 — anthropic, gemini, llama, openai | 65 |
| `escalation boundary event()` | `███▉░░░░░░░░` 16.2% | 4 — anthropic, deepseek, gemini, openai | 68 |
| `business rule task()` | `███▊░░░░░░░░` 15.4% | 3 — anthropic, gemini, openai | 65 |
| `data objects and stores()` | `███▊░░░░░░░░` 15.4% | 3 — anthropic, gemini, openai | 65 |
| `manual task()` | `███▊░░░░░░░░` 15.4% | 3 — anthropic, gemini, openai | 65 |
| `message start()` | `███▊░░░░░░░░` 15.4% | 3 — anthropic, gemini, openai | 65 |
| `sequential multi-instance activity()` | `███▊░░░░░░░░` 15.4% | 3 — anthropic, gemini, openai | 65 |
| `timer start()` | `███▊░░░░░░░░` 15.4% | 3 — anthropic, gemini, openai | 65 |
| `intermediate message throw()` | `███▌░░░░░░░░` 14.5% | 5 — anthropic, deepseek, gemini, llama, openai | 69 |
| `intermediate escalation throw()` | `███▏░░░░░░░░` 12.9% | 4 — anthropic, deepseek, llama, openai | 70 |
| `terminate end()` | `███▏░░░░░░░░` 12.9% | 3 — anthropic, mistral, openai | 70 |
| `exclusive gateway()` | `██▉░░░░░░░░░` 11.9% | 4 — anthropic, gemini, llama, openai | 67 |
| `message end()` | `██▊░░░░░░░░░` 11.6% | 3 — anthropic, gemini, openai | 69 |
| `receive task()` | `██▊░░░░░░░░░` 11.6% | 3 — anthropic, gemini, openai | 69 |
| `signal start()` | `██▊░░░░░░░░░` 11.6% | 3 — anthropic, gemini, openai | 69 |
| `script task()` | `██▌░░░░░░░░░` 10.4% | 3 — anthropic, gemini, openai | 67 |
| `event subprocess()` | `██▌░░░░░░░░░` 10.3% | 3 — anthropic, gemini, mistral | 68 |
| `timer boundary event()` | `██▌░░░░░░░░░` 10.3% | 3 — anthropic, gemini, mistral | 68 |
| `inclusive gateway()` | `██▍░░░░░░░░░` 10.0% | 2 — anthropic, openai | 70 |
| `service task()` | `██▍░░░░░░░░░` 10.0% | 2 — anthropic, openai | 70 |
| `user task()` | `██▍░░░░░░░░░` 10.0% | 2 — anthropic, openai | 70 |
| `error end()` | `██▏░░░░░░░░░` 8.8% | 2 — anthropic, gemini | 68 |
| `pools and lanes from distinct actors()` | `██▏░░░░░░░░░` 8.8% | 2 — anthropic, gemini | 68 |
| `parallel multi-instance activity()` | `█▊░░░░░░░░░░` 7.4% | 4 — anthropic, deepseek, gemini, openai | 68 |
| `call activity()` | `█▊░░░░░░░░░░` 7.1% | 3 — anthropic, gemini, openai | 56 |
| `embedded subprocess()` | `█▍░░░░░░░░░░` 5.9% | 3 — anthropic, gemini, openai | 68 |
| `exclusive gateway with default branch()` | `█▍░░░░░░░░░░` 5.9% | 3 — anthropic, gemini, openai | 68 |
| `send task()` | `█▍░░░░░░░░░░` 5.9% | 3 — anthropic, gemini, openai | 68 |

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
