# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 88.8% average pass rate · 235 total failures · 34 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.4%, openai 96.1%, llama 94.3%, deepseek 89.9%, gemini 82.1%, anthropic 70.9%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.4% | 2 | $0.4746 | 21.57M | `mistral-large-2411, mistral-small-2506` |
| `openai` | `█████████████▌` 96.1% | 14 | n/a | 16.82M | `gpt-4.1, gpt-4.1-mini` |
| `llama` | `█████████████▎` 94.3% | 19 | $0.2299 | 15.37M | `meta-llama/llama-3.3-70b-instruct` |
| `deepseek` | `████████████▋░` 89.9% | 30 | $0.0507 | 16.62M | `deepseek-chat` |
| `gemini` | `███████████▌░░` 82.1% | 60 | n/a | 14.95M | `gemini-2.5-flash, gemini-2.5-pro` |
| `anthropic` | `█████████▉░░░░` 70.9% | 110 | n/a | 7.16M | `claude-haiku-4-5, claude-sonnet-4-6` |

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
  <img alt="Failure categories by provider — anthropic has the most failures (110)" src="assets/smoke-health/failure-split-light.svg" width="760">
</picture>

<details>
<summary><b>Failure detail</b> — counts, share & sample signatures</summary>

| Provider | Category | Failures | % of fails | Sample signature |
|---|---|--:|--:|---|
| `anthropic` | deterministic | 106 | 96.4 | `business rule task()::400 - {"type":"error","error":{"type":"invalid_request_er…` |
| `gemini` | deterministic | 59 | 98.3 | `business rule task()::429 - [{` |
| `deepseek` | classification | 27 | 90.0 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | classification | 16 | 84.2 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | deterministic | 10 | 71.4 | `business rule task()::429 - {` |
| `openai` | classification | 4 | 28.6 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 3.6 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `deepseek` | deterministic | 3 | 10.0 | `escalation end()::TIMER (boundaryEvent) requires detail` |
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
| `error boundary event()` | `██████████▍░` 43.3% | 5 — anthropic, deepseek, gemini, llama, openai | 60 |
| `event-based gateway()` | `█████░░░░░░░` 20.6% | 3 — anthropic, llama, openai | 63 |
| `escalation end()` | `████▍░░░░░░░` 18.3% | 3 — anthropic, deepseek, gemini | 60 |
| `standard loop activity()` | `████▍░░░░░░░` 18.3% | 3 — anthropic, deepseek, gemini | 60 |
| `signal end()` | `████▏░░░░░░░` 17.2% | 5 — anthropic, deepseek, gemini, llama, openai | 58 |
| `intermediate signal throw()` | `████▏░░░░░░░` 17.2% | 4 — anthropic, gemini, llama, openai | 58 |

<details>
<summary>28 more flaky tests (≤ 16.4% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `parallel gateway()` | `███▉░░░░░░░░` 16.4% | 3 — anthropic, gemini, llama | 61 |
| `business rule task()` | `███▎░░░░░░░░` 13.8% | 3 — anthropic, gemini, openai | 58 |
| `data objects and stores()` | `███▎░░░░░░░░` 13.8% | 3 — anthropic, gemini, openai | 58 |
| `manual task()` | `███▎░░░░░░░░` 13.8% | 3 — anthropic, gemini, openai | 58 |
| `message start()` | `███▎░░░░░░░░` 13.8% | 3 — anthropic, gemini, openai | 58 |
| `sequential multi-instance activity()` | `███▎░░░░░░░░` 13.8% | 3 — anthropic, gemini, openai | 58 |
| `timer start()` | `███▎░░░░░░░░` 13.8% | 3 — anthropic, gemini, openai | 58 |
| `escalation boundary event()` | `███▏░░░░░░░░` 13.1% | 3 — anthropic, deepseek, gemini | 61 |
| `exclusive gateway()` | `██▍░░░░░░░░░` 10.0% | 3 — anthropic, gemini, llama | 60 |
| `intermediate message throw()` | `██▍░░░░░░░░░` 9.7% | 3 — anthropic, gemini, llama | 62 |
| `intermediate escalation throw()` | `██▎░░░░░░░░░` 9.5% | 2 — anthropic, deepseek | 63 |
| `terminate end()` | `██▎░░░░░░░░░` 9.5% | 2 — anthropic, openai | 63 |
| `script task()` | `██░░░░░░░░░░` 8.3% | 2 — anthropic, gemini | 60 |
| `event subprocess()` | `██░░░░░░░░░░` 8.2% | 3 — anthropic, gemini, mistral | 61 |
| `timer boundary event()` | `██░░░░░░░░░░` 8.2% | 3 — anthropic, gemini, mistral | 61 |
| `message end()` | `██░░░░░░░░░░` 8.1% | 2 — anthropic, gemini | 62 |
| `receive task()` | `██░░░░░░░░░░` 8.1% | 2 — anthropic, gemini | 62 |
| `signal start()` | `██░░░░░░░░░░` 8.1% | 2 — anthropic, gemini | 62 |
| `inclusive gateway()` | `█▉░░░░░░░░░░` 7.9% | 1 — anthropic | 63 |
| `service task()` | `█▉░░░░░░░░░░` 7.9% | 1 — anthropic | 63 |
| `user task()` | `█▉░░░░░░░░░░` 7.9% | 1 — anthropic | 63 |
| `error end()` | `█▋░░░░░░░░░░` 6.6% | 2 — anthropic, gemini | 61 |
| `pools and lanes from distinct actors()` | `█▋░░░░░░░░░░` 6.6% | 2 — anthropic, gemini | 61 |
| `parallel multi-instance activity()` | `█▏░░░░░░░░░░` 4.9% | 3 — anthropic, deepseek, gemini | 61 |
| `call activity()` | `█░░░░░░░░░░░` 4.1% | 2 — anthropic, gemini | 49 |
| `embedded subprocess()` | `▊░░░░░░░░░░░` 3.3% | 2 — anthropic, gemini | 61 |
| `exclusive gateway with default branch()` | `▊░░░░░░░░░░░` 3.3% | 2 — anthropic, gemini | 61 |
| `send task()` | `▊░░░░░░░░░░░` 3.3% | 2 — anthropic, gemini | 61 |

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
