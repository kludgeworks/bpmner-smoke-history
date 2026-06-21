# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 89.9% average pass rate · 199 total failures · 34 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.4%, openai 98.2%, llama 94.3%, deepseek 90.6%, gemini 81.7%, anthropic 75.1%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.4% | 2 | $0.4686 | 20.14M | `mistral-large-2411, mistral-small-2506` |
| `openai` | `█████████████▊` 98.2% | 6 | $0.5021 | 16.10M | `gpt-4.1, gpt-4.1-mini` |
| `llama` | `█████████████▎` 94.3% | 18 | $0.2284 | 14.49M | `meta-llama/llama-3.3-70b-instruct` |
| `deepseek` | `████████████▋░` 90.6% | 26 | $0.0509 | 15.40M | `deepseek-chat` |
| `gemini` | `███████████▌░░` 81.7% | 58 | n/a | 13.83M | `gemini-2.5-flash, gemini-2.5-pro` |
| `anthropic` | `██████████▌░░░` 75.1% | 89 | n/a | 7.16M | `claude-haiku-4-5, claude-sonnet-4-6` |

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
  <img alt="Failure categories by provider — anthropic has the most failures (89)" src="assets/smoke-health/failure-split-light.svg" width="760">
</picture>

<details>
<summary><b>Failure detail</b> — counts, share & sample signatures</summary>

| Provider | Category | Failures | % of fails | Sample signature |
|---|---|--:|--:|---|
| `anthropic` | deterministic | 85 | 95.5 | `business rule task()::400 - {"type":"error","error":{"type":"invalid_request_er…` |
| `gemini` | deterministic | 58 | 100.0 | `business rule task()::429 - [{` |
| `deepseek` | classification | 23 | 88.5 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | classification | 15 | 83.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | classification | 4 | 66.7 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 4.5 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `deepseek` | deterministic | 3 | 11.5 | `escalation end()::TIMER (boundaryEvent) requires detail` |
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
| `error boundary event()` | `█████████▍░░` 39.3% | 5 — anthropic, deepseek, gemini, llama, openai | 56 |
| `event-based gateway()` | `████▌░░░░░░░` 18.6% | 3 — anthropic, llama, openai | 59 |
| `signal end()` | `███▉░░░░░░░░` 16.4% | 4 — anthropic, deepseek, gemini, llama | 55 |
| `intermediate signal throw()` | `███▉░░░░░░░░` 16.4% | 3 — anthropic, gemini, llama | 55 |
| `escalation end()` | `███▉░░░░░░░░` 16.1% | 3 — anthropic, deepseek, gemini | 56 |
| `parallel gateway()` | `███▊░░░░░░░░` 15.8% | 3 — anthropic, gemini, llama | 57 |

<details>
<summary>28 more flaky tests (≤ 14.3% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `standard loop activity()` | `███▍░░░░░░░░` 14.3% | 3 — anthropic, deepseek, gemini | 56 |
| `escalation boundary event()` | `███▍░░░░░░░░` 14.0% | 3 — anthropic, deepseek, gemini | 57 |
| `business rule task()` | `███░░░░░░░░░` 12.7% | 2 — anthropic, gemini | 55 |
| `data objects and stores()` | `███░░░░░░░░░` 12.7% | 2 — anthropic, gemini | 55 |
| `manual task()` | `███░░░░░░░░░` 12.7% | 2 — anthropic, gemini | 55 |
| `message start()` | `███░░░░░░░░░` 12.7% | 2 — anthropic, gemini | 55 |
| `sequential multi-instance activity()` | `███░░░░░░░░░` 12.7% | 2 — anthropic, gemini | 55 |
| `timer start()` | `███░░░░░░░░░` 12.7% | 2 — anthropic, gemini | 55 |
| `exclusive gateway()` | `██▏░░░░░░░░░` 8.9% | 3 — anthropic, gemini, llama | 56 |
| `event subprocess()` | `██▏░░░░░░░░░` 8.8% | 3 — anthropic, gemini, mistral | 57 |
| `timer boundary event()` | `██▏░░░░░░░░░` 8.8% | 3 — anthropic, gemini, mistral | 57 |
| `intermediate message throw()` | `██▏░░░░░░░░░` 8.6% | 3 — anthropic, gemini, llama | 58 |
| `script task()` | `█▊░░░░░░░░░░` 7.1% | 2 — anthropic, gemini | 56 |
| `error end()` | `█▋░░░░░░░░░░` 7.0% | 2 — anthropic, gemini | 57 |
| `pools and lanes from distinct actors()` | `█▋░░░░░░░░░░` 7.0% | 2 — anthropic, gemini | 57 |
| `message end()` | `█▋░░░░░░░░░░` 6.9% | 2 — anthropic, gemini | 58 |
| `receive task()` | `█▋░░░░░░░░░░` 6.9% | 2 — anthropic, gemini | 58 |
| `signal start()` | `█▋░░░░░░░░░░` 6.9% | 2 — anthropic, gemini | 58 |
| `intermediate escalation throw()` | `█▋░░░░░░░░░░` 6.8% | 2 — anthropic, deepseek | 59 |
| `terminate end()` | `█▋░░░░░░░░░░` 6.8% | 2 — anthropic, openai | 59 |
| `parallel multi-instance activity()` | `█▎░░░░░░░░░░` 5.3% | 3 — anthropic, deepseek, gemini | 57 |
| `inclusive gateway()` | `█▎░░░░░░░░░░` 5.1% | 1 — anthropic | 59 |
| `service task()` | `█▎░░░░░░░░░░` 5.1% | 1 — anthropic | 59 |
| `user task()` | `█▎░░░░░░░░░░` 5.1% | 1 — anthropic | 59 |
| `call activity()` | `█░░░░░░░░░░░` 4.4% | 2 — anthropic, gemini | 45 |
| `embedded subprocess()` | `▉░░░░░░░░░░░` 3.5% | 2 — anthropic, gemini | 57 |
| `exclusive gateway with default branch()` | `▉░░░░░░░░░░░` 3.5% | 2 — anthropic, gemini | 57 |
| `send task()` | `▉░░░░░░░░░░░` 3.5% | 2 — anthropic, gemini | 57 |

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
