# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 89.2% average pass rate · 222 total failures · 34 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.4%, openai 98.3%, llama 94.2%, deepseek 89.7%, gemini 81.8%, anthropic 71.8%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.4% | 2 | $0.4758 | 21.32M | `mistral-large-2411, mistral-small-2506` |
| `openai` | `█████████████▊` 98.3% | 6 | $0.4996 | 16.82M | `gpt-4.1, gpt-4.1-mini` |
| `llama` | `█████████████▎` 94.2% | 19 | $0.2297 | 15.09M | `meta-llama/llama-3.3-70b-instruct` |
| `deepseek` | `████████████▌░` 89.7% | 30 | $0.0510 | 16.41M | `deepseek-chat` |
| `gemini` | `███████████▌░░` 81.8% | 60 | n/a | 14.63M | `gemini-2.5-flash, gemini-2.5-pro` |
| `anthropic` | `██████████░░░░` 71.8% | 105 | n/a | 7.16M | `claude-haiku-4-5, claude-sonnet-4-6` |

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
  <img alt="Failure categories by provider — anthropic has the most failures (105)" src="assets/smoke-health/failure-split-light.svg" width="760">
</picture>

<details>
<summary><b>Failure detail</b> — counts, share & sample signatures</summary>

| Provider | Category | Failures | % of fails | Sample signature |
|---|---|--:|--:|---|
| `anthropic` | deterministic | 101 | 96.2 | `business rule task()::400 - {"type":"error","error":{"type":"invalid_request_er…` |
| `gemini` | deterministic | 59 | 98.3 | `business rule task()::429 - [{` |
| `deepseek` | classification | 27 | 90.0 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | classification | 16 | 84.2 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | classification | 4 | 66.7 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 3.8 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `deepseek` | deterministic | 3 | 10.0 | `escalation end()::TIMER (boundaryEvent) requires detail` |
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
| `error boundary event()` | `██████████▏░` 42.4% | 5 — anthropic, deepseek, gemini, llama, openai | 59 |
| `event-based gateway()` | `█████░░░░░░░` 21.0% | 3 — anthropic, llama, openai | 62 |
| `escalation end()` | `████░░░░░░░░` 16.9% | 3 — anthropic, deepseek, gemini | 59 |
| `standard loop activity()` | `████░░░░░░░░` 16.9% | 3 — anthropic, deepseek, gemini | 59 |
| `parallel gateway()` | `████░░░░░░░░` 16.7% | 3 — anthropic, gemini, llama | 60 |
| `signal end()` | `███▊░░░░░░░░` 15.8% | 4 — anthropic, deepseek, gemini, llama | 57 |

<details>
<summary>28 more flaky tests (≤ 15.8% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `intermediate signal throw()` | `███▊░░░░░░░░` 15.8% | 3 — anthropic, gemini, llama | 57 |
| `escalation boundary event()` | `███▎░░░░░░░░` 13.3% | 3 — anthropic, deepseek, gemini | 60 |
| `business rule task()` | `███░░░░░░░░░` 12.3% | 2 — anthropic, gemini | 57 |
| `data objects and stores()` | `███░░░░░░░░░` 12.3% | 2 — anthropic, gemini | 57 |
| `manual task()` | `███░░░░░░░░░` 12.3% | 2 — anthropic, gemini | 57 |
| `message start()` | `███░░░░░░░░░` 12.3% | 2 — anthropic, gemini | 57 |
| `sequential multi-instance activity()` | `███░░░░░░░░░` 12.3% | 2 — anthropic, gemini | 57 |
| `timer start()` | `███░░░░░░░░░` 12.3% | 2 — anthropic, gemini | 57 |
| `intermediate message throw()` | `██▍░░░░░░░░░` 9.8% | 3 — anthropic, gemini, llama | 61 |
| `intermediate escalation throw()` | `██▍░░░░░░░░░` 9.7% | 2 — anthropic, deepseek | 62 |
| `terminate end()` | `██▍░░░░░░░░░` 9.7% | 2 — anthropic, openai | 62 |
| `exclusive gateway()` | `██░░░░░░░░░░` 8.5% | 3 — anthropic, gemini, llama | 59 |
| `event subprocess()` | `██░░░░░░░░░░` 8.3% | 3 — anthropic, gemini, mistral | 60 |
| `timer boundary event()` | `██░░░░░░░░░░` 8.3% | 3 — anthropic, gemini, mistral | 60 |
| `message end()` | `██░░░░░░░░░░` 8.2% | 2 — anthropic, gemini | 61 |
| `receive task()` | `██░░░░░░░░░░` 8.2% | 2 — anthropic, gemini | 61 |
| `signal start()` | `██░░░░░░░░░░` 8.2% | 2 — anthropic, gemini | 61 |
| `inclusive gateway()` | `██░░░░░░░░░░` 8.1% | 1 — anthropic | 62 |
| `service task()` | `██░░░░░░░░░░` 8.1% | 1 — anthropic | 62 |
| `user task()` | `██░░░░░░░░░░` 8.1% | 1 — anthropic | 62 |
| `script task()` | `█▋░░░░░░░░░░` 6.8% | 2 — anthropic, gemini | 59 |
| `error end()` | `█▋░░░░░░░░░░` 6.7% | 2 — anthropic, gemini | 60 |
| `pools and lanes from distinct actors()` | `█▋░░░░░░░░░░` 6.7% | 2 — anthropic, gemini | 60 |
| `parallel multi-instance activity()` | `█▎░░░░░░░░░░` 5.0% | 3 — anthropic, deepseek, gemini | 60 |
| `call activity()` | `█░░░░░░░░░░░` 4.2% | 2 — anthropic, gemini | 48 |
| `embedded subprocess()` | `▊░░░░░░░░░░░` 3.3% | 2 — anthropic, gemini | 60 |
| `exclusive gateway with default branch()` | `▊░░░░░░░░░░░` 3.3% | 2 — anthropic, gemini | 60 |
| `send task()` | `▊░░░░░░░░░░░` 3.3% | 2 — anthropic, gemini | 60 |

</details>

## LLM efficiency

> [!IMPORTANT]
> `mistral` is the outlier — median 6 calls/test but a P95 of 23 and a max of **69**, suggesting retry or tool-loop storms. Every other provider sits at a median of 5.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/llm-efficiency-dark.svg">
  <img alt="LLM calls per test by provider — mistral spread is far wider than the rest" src="assets/smoke-health/llm-efficiency-light.svg" width="760">
</picture>

---

<sub>📖 How this repo works — ingest, querying & setup → [`ABOUT.md`](ABOUT.md) · Regenerated every run by `render_dashboard.py`. Machine-managed — do not edit by hand.</sub>
