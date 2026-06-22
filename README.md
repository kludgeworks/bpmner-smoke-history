# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 88.4% average pass rate · 247 total failures · 34 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.4%, openai 94.5%, llama 94.1%, deepseek 90.1%, gemini 82.1%, anthropic 70.2%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.4% | 2 | $0.4770 | 22.07M | `mistral-large-2411, mistral-small-2506` |
| `openai` | `█████████████▎` 94.5% | 20 | n/a | 16.82M | `gpt-4.1, gpt-4.1-mini` |
| `llama` | `█████████████▏` 94.1% | 20 | $0.2291 | 15.57M | `meta-llama/llama-3.3-70b-instruct` |
| `deepseek` | `████████████▋░` 90.1% | 30 | $0.0510 | 17.04M | `deepseek-chat` |
| `gemini` | `███████████▌░░` 82.1% | 61 | n/a | 15.24M | `gemini-2.5-flash, gemini-2.5-pro` |
| `anthropic` | `█████████▉░░░░` 70.2% | 114 | n/a | 7.16M | `claude-haiku-4-5, claude-sonnet-4-6` |

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
  <img alt="Failure categories by provider — anthropic has the most failures (114)" src="assets/smoke-health/failure-split-light.svg" width="760">
</picture>

<details>
<summary><b>Failure detail</b> — counts, share & sample signatures</summary>

| Provider | Category | Failures | % of fails | Sample signature |
|---|---|--:|--:|---|
| `anthropic` | deterministic | 110 | 96.5 | `business rule task()::400 - {"type":"error","error":{"type":"invalid_request_er…` |
| `gemini` | deterministic | 59 | 96.7 | `business rule task()::429 - [{` |
| `deepseek` | classification | 27 | 90.0 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | classification | 17 | 85.0 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | deterministic | 16 | 80.0 | `business rule task()::429 - {` |
| `openai` | classification | 4 | 20.0 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 3.5 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
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
| `error boundary event()` | `██████████▋░` 44.3% | 5 — anthropic, deepseek, gemini, llama, openai | 61 |
| `event-based gateway()` | `████▉░░░░░░░` 20.3% | 3 — anthropic, llama, openai | 64 |
| `escalation end()` | `████▍░░░░░░░` 18.0% | 3 — anthropic, deepseek, gemini | 61 |
| `standard loop activity()` | `████▍░░░░░░░` 18.0% | 3 — anthropic, deepseek, gemini | 61 |
| `parallel gateway()` | `████▎░░░░░░░` 17.7% | 3 — anthropic, gemini, llama | 62 |
| `signal end()` | `████░░░░░░░░` 16.9% | 5 — anthropic, deepseek, gemini, llama, openai | 59 |

<details>
<summary>28 more flaky tests (≤ 16.9% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `intermediate signal throw()` | `████░░░░░░░░` 16.9% | 4 — anthropic, gemini, llama, openai | 59 |
| `escalation boundary event()` | `███▌░░░░░░░░` 14.5% | 4 — anthropic, deepseek, gemini, openai | 62 |
| `business rule task()` | `███▎░░░░░░░░` 13.6% | 3 — anthropic, gemini, openai | 59 |
| `data objects and stores()` | `███▎░░░░░░░░` 13.6% | 3 — anthropic, gemini, openai | 59 |
| `manual task()` | `███▎░░░░░░░░` 13.6% | 3 — anthropic, gemini, openai | 59 |
| `message start()` | `███▎░░░░░░░░` 13.6% | 3 — anthropic, gemini, openai | 59 |
| `sequential multi-instance activity()` | `███▎░░░░░░░░` 13.6% | 3 — anthropic, gemini, openai | 59 |
| `timer start()` | `███▎░░░░░░░░` 13.6% | 3 — anthropic, gemini, openai | 59 |
| `intermediate message throw()` | `██▋░░░░░░░░░` 11.1% | 3 — anthropic, gemini, llama | 63 |
| `exclusive gateway()` | `██▍░░░░░░░░░` 9.8% | 3 — anthropic, gemini, llama | 61 |
| `message end()` | `██▎░░░░░░░░░` 9.5% | 2 — anthropic, gemini | 63 |
| `receive task()` | `██▎░░░░░░░░░` 9.5% | 2 — anthropic, gemini | 63 |
| `signal start()` | `██▎░░░░░░░░░` 9.5% | 2 — anthropic, gemini | 63 |
| `intermediate escalation throw()` | `██▎░░░░░░░░░` 9.4% | 2 — anthropic, deepseek | 64 |
| `terminate end()` | `██▎░░░░░░░░░` 9.4% | 2 — anthropic, openai | 64 |
| `script task()` | `██░░░░░░░░░░` 8.2% | 2 — anthropic, gemini | 61 |
| `event subprocess()` | `██░░░░░░░░░░` 8.1% | 3 — anthropic, gemini, mistral | 62 |
| `timer boundary event()` | `██░░░░░░░░░░` 8.1% | 3 — anthropic, gemini, mistral | 62 |
| `inclusive gateway()` | `█▉░░░░░░░░░░` 7.8% | 1 — anthropic | 64 |
| `service task()` | `█▉░░░░░░░░░░` 7.8% | 1 — anthropic | 64 |
| `user task()` | `█▉░░░░░░░░░░` 7.8% | 1 — anthropic | 64 |
| `parallel multi-instance activity()` | `█▌░░░░░░░░░░` 6.5% | 4 — anthropic, deepseek, gemini, openai | 62 |
| `error end()` | `█▌░░░░░░░░░░` 6.5% | 2 — anthropic, gemini | 62 |
| `pools and lanes from distinct actors()` | `█▌░░░░░░░░░░` 6.5% | 2 — anthropic, gemini | 62 |
| `call activity()` | `█▌░░░░░░░░░░` 6.0% | 3 — anthropic, gemini, openai | 50 |
| `embedded subprocess()` | `█▏░░░░░░░░░░` 4.8% | 3 — anthropic, gemini, openai | 62 |
| `exclusive gateway with default branch()` | `█▏░░░░░░░░░░` 4.8% | 3 — anthropic, gemini, openai | 62 |
| `send task()` | `█▏░░░░░░░░░░` 4.8% | 3 — anthropic, gemini, openai | 62 |

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
