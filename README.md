# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 91.0% average pass rate · 166 total failures · 34 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.3%, openai 98.1%, llama 94%, deepseek 91.9%, anthropic 81.5%, gemini 80.9%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.3% | 2 | $0.4716 | 19.29M | `mistral-large-2411, mistral-small-2506` |
| `openai` | `█████████████▊` 98.1% | 6 | $0.5015 | 15.03M | `gpt-4.1, gpt-4.1-mini` |
| `llama` | `█████████████▏` 94.0% | 18 | $0.2253 | 13.78M | `meta-llama/llama-3.3-70b-instruct` |
| `deepseek` | `████████████▉░` 91.9% | 21 | $0.0510 | 14.50M | `deepseek-chat` |
| `anthropic` | `███████████▍░░` 81.5% | 61 | n/a | 7.16M | `claude-haiku-4-5, claude-sonnet-4-6` |
| `gemini` | `███████████▍░░` 80.9% | 58 | n/a | 13.11M | `gemini-2.5-flash, gemini-2.5-pro` |

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
  <img alt="Failure categories by provider — anthropic has the most failures (61)" src="assets/smoke-health/failure-split-light.svg" width="760">
</picture>

<details>
<summary><b>Failure detail</b> — counts, share & sample signatures</summary>

| Provider | Category | Failures | % of fails | Sample signature |
|---|---|--:|--:|---|
| `gemini` | deterministic | 58 | 100.0 | `business rule task()::429 - [{` |
| `anthropic` | deterministic | 57 | 93.4 | `business rule task()::400 - {"type":"error","error":{"type":"invalid_request_er…` |
| `deepseek` | classification | 18 | 85.7 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | classification | 15 | 83.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | classification | 4 | 66.7 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 6.6 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `deepseek` | deterministic | 3 | 14.3 | `escalation end()::TIMER (boundaryEvent) requires detail` |
| `openai` | deterministic | 2 | 33.3 | `event-based gateway()::RECEIVE (act-await-response) requires messageName` |
| `llama` | deterministic | 2 | 11.1 | `event-based gateway()::RECEIVE (act-wait-for-response) requires messageName` |
| `mistral` | deterministic | 1 | 50.0 | `event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind` |
| `mistral` | infra | 1 | 50.0 | `timer boundary event()::timer boundary event() timed out after 240 seconds` |
| `llama` | infra | 1 | 5.6 | `exclusive gateway()::exclusive gateway() timed out after 240 seconds` |

</details>

## Flaky tests

> [!WARNING]
> Fails **across providers** ⇒ the test or prompt is suspect. Fails on **one provider** ⇒ a model limit.

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `error boundary event()` | `████████▉░░░` 37.0% | 5 — anthropic, deepseek, gemini, llama, openai | 54 |
| `escalation end()` | `████░░░░░░░░` 16.7% | 3 — anthropic, deepseek, gemini | 54 |
| `parallel gateway()` | `████░░░░░░░░` 16.7% | 3 — anthropic, gemini, llama | 54 |
| `event-based gateway()` | `███▉░░░░░░░░` 16.4% | 3 — anthropic, llama, openai | 55 |
| `signal end()` | `███▎░░░░░░░░` 13.7% | 4 — anthropic, deepseek, gemini, llama | 51 |
| `intermediate signal throw()` | `███▎░░░░░░░░` 13.7% | 3 — anthropic, gemini, llama | 51 |

<details>
<summary>28 more flaky tests (≤ 13.0% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `escalation boundary event()` | `███▏░░░░░░░░` 13.0% | 3 — anthropic, deepseek, gemini | 54 |
| `standard loop activity()` | `██▋░░░░░░░░░` 11.1% | 3 — anthropic, deepseek, gemini | 54 |
| `business rule task()` | `██▍░░░░░░░░░` 9.8% | 2 — anthropic, gemini | 51 |
| `data objects and stores()` | `██▍░░░░░░░░░` 9.8% | 2 — anthropic, gemini | 51 |
| `manual task()` | `██▍░░░░░░░░░` 9.8% | 2 — anthropic, gemini | 51 |
| `message start()` | `██▍░░░░░░░░░` 9.8% | 2 — anthropic, gemini | 51 |
| `sequential multi-instance activity()` | `██▍░░░░░░░░░` 9.8% | 2 — anthropic, gemini | 51 |
| `timer start()` | `██▍░░░░░░░░░` 9.8% | 2 — anthropic, gemini | 51 |
| `event subprocess()` | `██▎░░░░░░░░░` 9.3% | 3 — anthropic, gemini, mistral | 54 |
| `exclusive gateway()` | `██▎░░░░░░░░░` 9.3% | 3 — anthropic, gemini, llama | 54 |
| `timer boundary event()` | `██▎░░░░░░░░░` 9.3% | 3 — anthropic, gemini, mistral | 54 |
| `intermediate message throw()` | `██▏░░░░░░░░░` 9.1% | 3 — anthropic, gemini, llama | 55 |
| `error end()` | `█▊░░░░░░░░░░` 7.4% | 2 — anthropic, gemini | 54 |
| `pools and lanes from distinct actors()` | `█▊░░░░░░░░░░` 7.4% | 2 — anthropic, gemini | 54 |
| `script task()` | `█▊░░░░░░░░░░` 7.4% | 2 — anthropic, gemini | 54 |
| `message end()` | `█▊░░░░░░░░░░` 7.3% | 2 — anthropic, gemini | 55 |
| `receive task()` | `█▊░░░░░░░░░░` 7.3% | 2 — anthropic, gemini | 55 |
| `signal start()` | `█▊░░░░░░░░░░` 7.3% | 2 — anthropic, gemini | 55 |
| `parallel multi-instance activity()` | `█▍░░░░░░░░░░` 5.6% | 3 — anthropic, deepseek, gemini | 54 |
| `call activity()` | `█▏░░░░░░░░░░` 4.8% | 2 — anthropic, gemini | 42 |
| `embedded subprocess()` | `▉░░░░░░░░░░░` 3.7% | 2 — anthropic, gemini | 54 |
| `exclusive gateway with default branch()` | `▉░░░░░░░░░░░` 3.7% | 2 — anthropic, gemini | 54 |
| `send task()` | `▉░░░░░░░░░░░` 3.7% | 2 — anthropic, gemini | 54 |
| `intermediate escalation throw()` | `▉░░░░░░░░░░░` 3.6% | 2 — anthropic, deepseek | 55 |
| `terminate end()` | `▉░░░░░░░░░░░` 3.6% | 2 — anthropic, openai | 55 |
| `inclusive gateway()` | `▍░░░░░░░░░░░` 1.8% | 1 — anthropic | 55 |
| `service task()` | `▍░░░░░░░░░░░` 1.8% | 1 — anthropic | 55 |
| `user task()` | `▍░░░░░░░░░░░` 1.8% | 1 — anthropic | 55 |

</details>

## LLM efficiency

> [!IMPORTANT]
> `mistral` is the outlier — median 7 calls/test but a P95 of 23 and a max of **69**, suggesting retry or tool-loop storms. Every other provider sits at a median of 5.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/llm-efficiency-dark.svg">
  <img alt="LLM calls per test by provider — mistral spread is far wider than the rest" src="assets/smoke-health/llm-efficiency-light.svg" width="760">
</picture>

---

<sub>📖 How this repo works — ingest, querying & setup → [`ABOUT.md`](ABOUT.md) · Regenerated every run by `render_dashboard.py`. Machine-managed — do not edit by hand.</sub>
