# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 91.0% average pass rate · 161 total failures · 34 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.3%, openai 98%, llama 93.9%, deepseek 91.7%, anthropic 82.5%, gemini 80.9%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.3% | 2 | $0.4689 | 18.88M | `mistral-large-2411, mistral-small-2506` |
| `openai` | `█████████████▊` 98.0% | 6 | $0.5017 | 14.77M | `gpt-4.1, gpt-4.1-mini` |
| `llama` | `█████████████▏` 93.9% | 18 | $0.2259 | 13.56M | `meta-llama/llama-3.3-70b-instruct` |
| `deepseek` | `████████████▉░` 91.7% | 21 | $0.0509 | 14.13M | `deepseek-chat` |
| `anthropic` | `███████████▌░░` 82.5% | 57 | n/a | 7.16M | `claude-haiku-4-5, claude-sonnet-4-6` |
| `gemini` | `███████████▍░░` 80.9% | 57 | n/a | 12.82M | `gemini-2.5-flash, gemini-2.5-pro` |

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
  <img alt="Failure categories by provider — anthropic has the most failures (57)" src="assets/smoke-health/failure-split-light.svg" width="760">
</picture>

<details>
<summary><b>Failure detail</b> — counts, share & sample signatures</summary>

| Provider | Category | Failures | % of fails | Sample signature |
|---|---|--:|--:|---|
| `gemini` | deterministic | 57 | 100.0 | `business rule task()::429 - [{` |
| `anthropic` | deterministic | 53 | 93.0 | `business rule task()::400 - {"type":"error","error":{"type":"invalid_request_er…` |
| `deepseek` | classification | 18 | 85.7 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | classification | 15 | 83.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | classification | 4 | 66.7 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 7.0 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
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
| `error boundary event()` | `█████████░░░` 37.7% | 5 — anthropic, deepseek, gemini, llama, openai | 53 |
| `parallel gateway()` | `████▏░░░░░░░` 17.0% | 3 — anthropic, gemini, llama | 53 |
| `event-based gateway()` | `████░░░░░░░░` 16.7% | 3 — anthropic, llama, openai | 54 |
| `escalation end()` | `███▋░░░░░░░░` 15.1% | 3 — anthropic, deepseek, gemini | 53 |
| `signal end()` | `███▍░░░░░░░░` 14.0% | 4 — anthropic, deepseek, gemini, llama | 50 |
| `intermediate signal throw()` | `███▍░░░░░░░░` 14.0% | 3 — anthropic, gemini, llama | 50 |

<details>
<summary>28 more flaky tests (≤ 13.2% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `escalation boundary event()` | `███▏░░░░░░░░` 13.2% | 3 — anthropic, deepseek, gemini | 53 |
| `standard loop activity()` | `██▊░░░░░░░░░` 11.3% | 3 — anthropic, deepseek, gemini | 53 |
| `business rule task()` | `██▍░░░░░░░░░` 10.0% | 2 — anthropic, gemini | 50 |
| `data objects and stores()` | `██▍░░░░░░░░░` 10.0% | 2 — anthropic, gemini | 50 |
| `manual task()` | `██▍░░░░░░░░░` 10.0% | 2 — anthropic, gemini | 50 |
| `message start()` | `██▍░░░░░░░░░` 10.0% | 2 — anthropic, gemini | 50 |
| `sequential multi-instance activity()` | `██▍░░░░░░░░░` 10.0% | 2 — anthropic, gemini | 50 |
| `timer start()` | `██▍░░░░░░░░░` 10.0% | 2 — anthropic, gemini | 50 |
| `event subprocess()` | `██▎░░░░░░░░░` 9.4% | 3 — anthropic, gemini, mistral | 53 |
| `exclusive gateway()` | `██▎░░░░░░░░░` 9.4% | 3 — anthropic, gemini, llama | 53 |
| `timer boundary event()` | `██▎░░░░░░░░░` 9.4% | 3 — anthropic, gemini, mistral | 53 |
| `error end()` | `█▊░░░░░░░░░░` 7.5% | 2 — anthropic, gemini | 53 |
| `pools and lanes from distinct actors()` | `█▊░░░░░░░░░░` 7.5% | 2 — anthropic, gemini | 53 |
| `script task()` | `█▊░░░░░░░░░░` 7.5% | 2 — anthropic, gemini | 53 |
| `intermediate message throw()` | `█▊░░░░░░░░░░` 7.4% | 3 — anthropic, gemini, llama | 54 |
| `parallel multi-instance activity()` | `█▍░░░░░░░░░░` 5.7% | 3 — anthropic, deepseek, gemini | 53 |
| `message end()` | `█▍░░░░░░░░░░` 5.6% | 2 — anthropic, gemini | 54 |
| `receive task()` | `█▍░░░░░░░░░░` 5.6% | 2 — anthropic, gemini | 54 |
| `signal start()` | `█▍░░░░░░░░░░` 5.6% | 2 — anthropic, gemini | 54 |
| `call activity()` | `█▏░░░░░░░░░░` 4.9% | 2 — anthropic, gemini | 41 |
| `embedded subprocess()` | `▉░░░░░░░░░░░` 3.8% | 2 — anthropic, gemini | 53 |
| `exclusive gateway with default branch()` | `▉░░░░░░░░░░░` 3.8% | 2 — anthropic, gemini | 53 |
| `send task()` | `▉░░░░░░░░░░░` 3.8% | 2 — anthropic, gemini | 53 |
| `intermediate escalation throw()` | `▉░░░░░░░░░░░` 3.7% | 2 — anthropic, deepseek | 54 |
| `terminate end()` | `▉░░░░░░░░░░░` 3.7% | 2 — anthropic, openai | 54 |
| `inclusive gateway()` | `▌░░░░░░░░░░░` 1.9% | 1 — anthropic | 54 |
| `service task()` | `▌░░░░░░░░░░░` 1.9% | 1 — anthropic | 54 |
| `user task()` | `▌░░░░░░░░░░░` 1.9% | 1 — anthropic | 54 |

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
