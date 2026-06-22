# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 88.2% average pass rate · 256 total failures · 34 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.4%, llama 94.2%, openai 93.5%, deepseek 90.3%, gemini 82.4%, anthropic 69.3%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.4% | 2 | $0.4757 | 22.34M | `mistral-large-2411, mistral-small-2506` |
| `llama` | `█████████████▎` 94.2% | 20 | $0.2304 | 15.92M | `meta-llama/llama-3.3-70b-instruct` |
| `openai` | `█████████████▏` 93.5% | 24 | n/a | 16.82M | `gpt-4.1, gpt-4.1-mini` |
| `deepseek` | `████████████▋░` 90.3% | 30 | $0.0514 | 17.50M | `deepseek-chat` |
| `gemini` | `███████████▌░░` 82.4% | 61 | n/a | 15.57M | `gemini-2.5-flash, gemini-2.5-pro` |
| `anthropic` | `█████████▊░░░░` 69.3% | 119 | n/a | 7.16M | `claude-haiku-4-5, claude-sonnet-4-6` |

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
  <img alt="Failure categories by provider — anthropic has the most failures (119)" src="assets/smoke-health/failure-split-light.svg" width="760">
</picture>

<details>
<summary><b>Failure detail</b> — counts, share & sample signatures</summary>

| Provider | Category | Failures | % of fails | Sample signature |
|---|---|--:|--:|---|
| `anthropic` | deterministic | 115 | 96.6 | `business rule task()::400 - {"type":"error","error":{"type":"invalid_request_er…` |
| `gemini` | deterministic | 59 | 96.7 | `business rule task()::429 - [{` |
| `deepseek` | classification | 27 | 90.0 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | deterministic | 20 | 83.3 | `business rule task()::429 - {` |
| `llama` | classification | 17 | 85.0 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | classification | 4 | 16.7 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 3.4 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `deepseek` | deterministic | 3 | 10.0 | `escalation end()::TIMER (boundaryEvent) requires detail` |
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
| `error boundary event()` | `██████████▌░` 43.5% | 5 — anthropic, deepseek, gemini, llama, openai | 62 |
| `event-based gateway()` | `████▊░░░░░░░` 20.0% | 3 — anthropic, llama, openai | 65 |
| `parallel gateway()` | `████▌░░░░░░░` 19.0% | 3 — anthropic, gemini, llama | 63 |
| `escalation end()` | `████▎░░░░░░░` 17.7% | 3 — anthropic, deepseek, gemini | 62 |
| `standard loop activity()` | `████▎░░░░░░░` 17.7% | 3 — anthropic, deepseek, gemini | 62 |
| `signal end()` | `████░░░░░░░░` 16.7% | 5 — anthropic, deepseek, gemini, llama, openai | 60 |

<details>
<summary>28 more flaky tests (≤ 16.7% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `intermediate signal throw()` | `████░░░░░░░░` 16.7% | 4 — anthropic, gemini, llama, openai | 60 |
| `escalation boundary event()` | `███▍░░░░░░░░` 14.3% | 4 — anthropic, deepseek, gemini, openai | 63 |
| `business rule task()` | `███▎░░░░░░░░` 13.3% | 3 — anthropic, gemini, openai | 60 |
| `data objects and stores()` | `███▎░░░░░░░░` 13.3% | 3 — anthropic, gemini, openai | 60 |
| `manual task()` | `███▎░░░░░░░░` 13.3% | 3 — anthropic, gemini, openai | 60 |
| `message start()` | `███▎░░░░░░░░` 13.3% | 3 — anthropic, gemini, openai | 60 |
| `sequential multi-instance activity()` | `███▎░░░░░░░░` 13.3% | 3 — anthropic, gemini, openai | 60 |
| `timer start()` | `███▎░░░░░░░░` 13.3% | 3 — anthropic, gemini, openai | 60 |
| `intermediate message throw()` | `███░░░░░░░░░` 12.5% | 4 — anthropic, gemini, llama, openai | 64 |
| `message end()` | `██▋░░░░░░░░░` 10.9% | 3 — anthropic, gemini, openai | 64 |
| `receive task()` | `██▋░░░░░░░░░` 10.9% | 3 — anthropic, gemini, openai | 64 |
| `signal start()` | `██▋░░░░░░░░░` 10.9% | 3 — anthropic, gemini, openai | 64 |
| `exclusive gateway()` | `██▍░░░░░░░░░` 9.7% | 3 — anthropic, gemini, llama | 62 |
| `event subprocess()` | `██▎░░░░░░░░░` 9.5% | 3 — anthropic, gemini, mistral | 63 |
| `timer boundary event()` | `██▎░░░░░░░░░` 9.5% | 3 — anthropic, gemini, mistral | 63 |
| `intermediate escalation throw()` | `██▎░░░░░░░░░` 9.2% | 2 — anthropic, deepseek | 65 |
| `terminate end()` | `██▎░░░░░░░░░` 9.2% | 2 — anthropic, openai | 65 |
| `script task()` | `██░░░░░░░░░░` 8.1% | 2 — anthropic, gemini | 62 |
| `error end()` | `█▉░░░░░░░░░░` 7.9% | 2 — anthropic, gemini | 63 |
| `pools and lanes from distinct actors()` | `█▉░░░░░░░░░░` 7.9% | 2 — anthropic, gemini | 63 |
| `inclusive gateway()` | `█▉░░░░░░░░░░` 7.7% | 1 — anthropic | 65 |
| `service task()` | `█▉░░░░░░░░░░` 7.7% | 1 — anthropic | 65 |
| `user task()` | `█▉░░░░░░░░░░` 7.7% | 1 — anthropic | 65 |
| `parallel multi-instance activity()` | `█▌░░░░░░░░░░` 6.3% | 4 — anthropic, deepseek, gemini, openai | 63 |
| `call activity()` | `█▍░░░░░░░░░░` 5.9% | 3 — anthropic, gemini, openai | 51 |
| `embedded subprocess()` | `█▏░░░░░░░░░░` 4.8% | 3 — anthropic, gemini, openai | 63 |
| `exclusive gateway with default branch()` | `█▏░░░░░░░░░░` 4.8% | 3 — anthropic, gemini, openai | 63 |
| `send task()` | `█▏░░░░░░░░░░` 4.8% | 3 — anthropic, gemini, openai | 63 |

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
