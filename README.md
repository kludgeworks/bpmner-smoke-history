# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 84.3% average pass rate · 356 total failures · 34 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.4%, llama 94.3%, deepseek 90.5%, openai 90.3%, gemini 77.5%, anthropic 53.7%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.4% | 3 | $0.4770 | 28.72M | `mistral-large-2411, mistral-small-2506` |
| `llama` | `█████████████▎` 94.3% | 26 | $0.2296 | 20.82M | `meta-llama/llama-3.3-70b-instruct` |
| `deepseek` | `████████████▋░` 90.5% | 40 | $0.0502 | 23.30M | `deepseek-chat` |
| `openai` | `████████████▋░` 90.3% | 47 | n/a | 21.17M | `gpt-4.1, gpt-4.1-mini` |
| `gemini` | `██████████▉░░░` 77.5% | 63 | n/a | 19.80M | `gemini-2.5-flash, gemini-2.5-pro` |
| `anthropic` | `███████▌░░░░░░` 53.7% | 177 | n/a | 7.16M | `claude-haiku-4-5, claude-sonnet-4-6` |

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
| `deepseek` | classification | 37 | 92.5 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | classification | 22 | 84.6 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | classification | 4 | 8.5 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `gemini` | classification | 4 | 6.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 2.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | deterministic | 3 | 11.5 | `event-based gateway()::RECEIVE (act-wait-for-response) requires messageName` |
| `deepseek` | deterministic | 3 | 7.5 | `escalation end()::TIMER (boundaryEvent) requires detail` |
| `mistral` | infra | 2 | 66.7 | `terminate end()::terminate end() timed out after 240 seconds` |
| `mistral` | deterministic | 1 | 33.3 | `event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind` |
| `llama` | infra | 1 | 3.8 | `exclusive gateway()::exclusive gateway() timed out after 240 seconds` |

</details>

## Flaky tests

> [!WARNING]
> Fails **across providers** ⇒ the test or prompt is suspect. Fails on **one provider** ⇒ a model limit.

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `error boundary event()` | `██████████░░` 41.5% | 5 — anthropic, deepseek, gemini, llama, openai | 82 |
| `event-based gateway()` | `████▊░░░░░░░` 20.0% | 3 — anthropic, llama, openai | 85 |
| `escalation end()` | `████▍░░░░░░░` 18.3% | 4 — anthropic, deepseek, gemini, openai | 82 |
| `standard loop activity()` | `████▍░░░░░░░` 18.3% | 4 — anthropic, deepseek, gemini, openai | 82 |
| `parallel gateway()` | `████▍░░░░░░░` 18.3% | 3 — anthropic, gemini, llama | 82 |
| `intermediate signal throw()` | `████▎░░░░░░░` 17.7% | 4 — anthropic, gemini, llama, openai | 79 |

<details>
<summary>28 more flaky tests (≤ 16.5% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `signal end()` | `████░░░░░░░░` 16.5% | 5 — anthropic, deepseek, gemini, llama, openai | 79 |
| `escalation boundary event()` | `███▊░░░░░░░░` 15.7% | 4 — anthropic, deepseek, gemini, openai | 83 |
| `intermediate message throw()` | `███▊░░░░░░░░` 15.5% | 5 — anthropic, deepseek, gemini, llama, openai | 84 |
| `business rule task()` | `███▍░░░░░░░░` 13.9% | 3 — anthropic, gemini, openai | 79 |
| `data objects and stores()` | `███▍░░░░░░░░` 13.9% | 3 — anthropic, gemini, openai | 79 |
| `manual task()` | `███▍░░░░░░░░` 13.9% | 3 — anthropic, gemini, openai | 79 |
| `message start()` | `███▍░░░░░░░░` 13.9% | 3 — anthropic, gemini, openai | 79 |
| `sequential multi-instance activity()` | `███▍░░░░░░░░` 13.9% | 3 — anthropic, gemini, openai | 79 |
| `timer start()` | `███▍░░░░░░░░` 13.9% | 3 — anthropic, gemini, openai | 79 |
| `message end()` | `██▉░░░░░░░░░` 11.9% | 3 — anthropic, gemini, openai | 84 |
| `receive task()` | `██▉░░░░░░░░░` 11.9% | 3 — anthropic, gemini, openai | 84 |
| `signal start()` | `██▉░░░░░░░░░` 11.9% | 3 — anthropic, gemini, openai | 84 |
| `intermediate escalation throw()` | `██▉░░░░░░░░░` 11.8% | 4 — anthropic, deepseek, llama, openai | 85 |
| `terminate end()` | `██▉░░░░░░░░░` 11.8% | 3 — anthropic, mistral, openai | 85 |
| `exclusive gateway()` | `██▍░░░░░░░░░` 9.8% | 4 — anthropic, gemini, llama, openai | 82 |
| `inclusive gateway()` | `██▎░░░░░░░░░` 9.4% | 2 — anthropic, openai | 85 |
| `service task()` | `██▎░░░░░░░░░` 9.4% | 2 — anthropic, openai | 85 |
| `user task()` | `██▎░░░░░░░░░` 9.4% | 2 — anthropic, openai | 85 |
| `event subprocess()` | `██░░░░░░░░░░` 8.5% | 3 — anthropic, gemini, mistral | 82 |
| `script task()` | `██░░░░░░░░░░` 8.5% | 3 — anthropic, gemini, openai | 82 |
| `timer boundary event()` | `██░░░░░░░░░░` 8.5% | 3 — anthropic, gemini, mistral | 82 |
| `error end()` | `█▊░░░░░░░░░░` 7.3% | 2 — anthropic, gemini | 82 |
| `pools and lanes from distinct actors()` | `█▊░░░░░░░░░░` 7.3% | 2 — anthropic, gemini | 82 |
| `parallel multi-instance activity()` | `█▊░░░░░░░░░░` 7.2% | 4 — anthropic, deepseek, gemini, openai | 83 |
| `call activity()` | `█▋░░░░░░░░░░` 7.0% | 3 — anthropic, gemini, openai | 71 |
| `embedded subprocess()` | `█▌░░░░░░░░░░` 6.0% | 3 — anthropic, gemini, openai | 83 |
| `exclusive gateway with default branch()` | `█▌░░░░░░░░░░` 6.0% | 3 — anthropic, gemini, openai | 83 |
| `send task()` | `█▌░░░░░░░░░░` 6.0% | 3 — anthropic, gemini, openai | 83 |

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
