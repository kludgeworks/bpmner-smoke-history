# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 84.8% average pass rate · 355 total failures · 34 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.3%, llama 94.4%, deepseek 90.2%, openai 90.1%, gemini 79.8%, anthropic 54.8%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.3% | 3 | $0.4728 | 27.67M | `mistral-large-2411, mistral-small-2506` |
| `llama` | `█████████████▎` 94.4% | 25 | $0.2310 | 20.43M | `meta-llama/llama-3.3-70b-instruct` |
| `deepseek` | `████████████▋░` 90.2% | 40 | $0.0502 | 22.69M | `deepseek-chat` |
| `openai` | `████████████▋░` 90.1% | 47 | n/a | 20.70M | `gpt-4.1, gpt-4.1-mini` |
| `gemini` | `███████████▏░░` 79.8% | 63 | n/a | 19.80M | `gemini-2.5-flash, gemini-2.5-pro` |
| `anthropic` | `███████▋░░░░░░` 54.8% | 177 | n/a | 7.16M | `claude-haiku-4-5, claude-sonnet-4-6` |

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
| `llama` | classification | 21 | 84.0 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | classification | 4 | 8.5 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `gemini` | classification | 4 | 6.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 2.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | deterministic | 3 | 12.0 | `event-based gateway()::RECEIVE (act-wait-for-response) requires messageName` |
| `deepseek` | deterministic | 3 | 7.5 | `escalation end()::TIMER (boundaryEvent) requires detail` |
| `mistral` | infra | 2 | 66.7 | `terminate end()::terminate end() timed out after 240 seconds` |
| `mistral` | deterministic | 1 | 33.3 | `event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind` |
| `llama` | infra | 1 | 4.0 | `exclusive gateway()::exclusive gateway() timed out after 240 seconds` |

</details>

## Flaky tests

> [!WARNING]
> Fails **across providers** ⇒ the test or prompt is suspect. Fails on **one provider** ⇒ a model limit.

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `error boundary event()` | `██████████▎░` 42.5% | 5 — anthropic, deepseek, gemini, llama, openai | 80 |
| `event-based gateway()` | `████▉░░░░░░░` 20.5% | 3 — anthropic, llama, openai | 83 |
| `escalation end()` | `████▌░░░░░░░` 18.8% | 4 — anthropic, deepseek, gemini, openai | 80 |
| `standard loop activity()` | `████▌░░░░░░░` 18.8% | 4 — anthropic, deepseek, gemini, openai | 80 |
| `intermediate signal throw()` | `████▍░░░░░░░` 18.2% | 4 — anthropic, gemini, llama, openai | 77 |
| `parallel gateway()` | `████▎░░░░░░░` 17.5% | 3 — anthropic, gemini, llama | 80 |

<details>
<summary>28 more flaky tests (≤ 16.9% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `signal end()` | `████░░░░░░░░` 16.9% | 5 — anthropic, deepseek, gemini, llama, openai | 77 |
| `escalation boundary event()` | `███▉░░░░░░░░` 16.0% | 4 — anthropic, deepseek, gemini, openai | 81 |
| `intermediate message throw()` | `███▉░░░░░░░░` 15.9% | 5 — anthropic, deepseek, gemini, llama, openai | 82 |
| `business rule task()` | `███▍░░░░░░░░` 14.3% | 3 — anthropic, gemini, openai | 77 |
| `data objects and stores()` | `███▍░░░░░░░░` 14.3% | 3 — anthropic, gemini, openai | 77 |
| `manual task()` | `███▍░░░░░░░░` 14.3% | 3 — anthropic, gemini, openai | 77 |
| `message start()` | `███▍░░░░░░░░` 14.3% | 3 — anthropic, gemini, openai | 77 |
| `sequential multi-instance activity()` | `███▍░░░░░░░░` 14.3% | 3 — anthropic, gemini, openai | 77 |
| `timer start()` | `███▍░░░░░░░░` 14.3% | 3 — anthropic, gemini, openai | 77 |
| `message end()` | `██▉░░░░░░░░░` 12.2% | 3 — anthropic, gemini, openai | 82 |
| `receive task()` | `██▉░░░░░░░░░` 12.2% | 3 — anthropic, gemini, openai | 82 |
| `signal start()` | `██▉░░░░░░░░░` 12.2% | 3 — anthropic, gemini, openai | 82 |
| `intermediate escalation throw()` | `██▉░░░░░░░░░` 12.0% | 4 — anthropic, deepseek, llama, openai | 83 |
| `terminate end()` | `██▉░░░░░░░░░` 12.0% | 3 — anthropic, mistral, openai | 83 |
| `exclusive gateway()` | `██▍░░░░░░░░░` 10.0% | 4 — anthropic, gemini, llama, openai | 80 |
| `inclusive gateway()` | `██▎░░░░░░░░░` 9.6% | 2 — anthropic, openai | 83 |
| `service task()` | `██▎░░░░░░░░░` 9.6% | 2 — anthropic, openai | 83 |
| `user task()` | `██▎░░░░░░░░░` 9.6% | 2 — anthropic, openai | 83 |
| `event subprocess()` | `██▏░░░░░░░░░` 8.8% | 3 — anthropic, gemini, mistral | 80 |
| `script task()` | `██▏░░░░░░░░░` 8.8% | 3 — anthropic, gemini, openai | 80 |
| `timer boundary event()` | `██▏░░░░░░░░░` 8.8% | 3 — anthropic, gemini, mistral | 80 |
| `error end()` | `█▊░░░░░░░░░░` 7.5% | 2 — anthropic, gemini | 80 |
| `pools and lanes from distinct actors()` | `█▊░░░░░░░░░░` 7.5% | 2 — anthropic, gemini | 80 |
| `parallel multi-instance activity()` | `█▊░░░░░░░░░░` 7.4% | 4 — anthropic, deepseek, gemini, openai | 81 |
| `call activity()` | `█▊░░░░░░░░░░` 7.2% | 3 — anthropic, gemini, openai | 69 |
| `embedded subprocess()` | `█▌░░░░░░░░░░` 6.2% | 3 — anthropic, gemini, openai | 81 |
| `exclusive gateway with default branch()` | `█▌░░░░░░░░░░` 6.2% | 3 — anthropic, gemini, openai | 81 |
| `send task()` | `█▌░░░░░░░░░░` 6.2% | 3 — anthropic, gemini, openai | 81 |

</details>

## LLM efficiency

> [!IMPORTANT]
> `mistral` is the outlier — median 5 calls/test but a P95 of 21 and a max of **69**, suggesting retry or tool-loop storms. Every other provider sits at a median of 5.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/llm-efficiency-dark.svg">
  <img alt="LLM calls per test by provider — mistral spread is far wider than the rest" src="assets/smoke-health/llm-efficiency-light.svg" width="760">
</picture>

---

<sub>📖 How this repo works — ingest, querying & setup → [`ABOUT.md`](ABOUT.md) · Regenerated every run by `render_dashboard.py`. Machine-managed — do not edit by hand.</sub>
