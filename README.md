# 🔬 Smoke Health

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/summary-dark.svg">
  <img alt="6 providers · 90.1% average pass rate · 191 total failures · 34 flaky tests" src="assets/smoke-health/summary-light.svg" width="760">
</picture>

> [!NOTE]
> **Report-only · all recorded runs.** _Provider_ = the model family under test. Pass/fail reflects the authoritative post-retry outcome joined from `test.xml`.

## Provider scorecard

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/smoke-health/scorecard-dark.svg">
  <img alt="Pass rate by provider — mistral 99.4%, openai 98.2%, llama 94.2%, deepseek 91.1%, gemini 81.5%, anthropic 76.4%" src="assets/smoke-health/scorecard-light.svg" width="760">
</picture>

<details>
<summary><b>Full table</b> — pass-rate bars, fails, cost & tokens per run</summary>

| Provider | Pass rate | Fails | $/run | Tokens | Model family |
|---|:--|--:|--:|--:|---|
| `mistral` | `█████████████▉` 99.4% | 2 | $0.4687 | 19.85M | `mistral-large-2411, mistral-small-2506` |
| `openai` | `█████████████▊` 98.2% | 6 | $0.5035 | 15.89M | `gpt-4.1, gpt-4.1-mini` |
| `llama` | `█████████████▎` 94.2% | 18 | $0.2267 | 14.12M | `meta-llama/llama-3.3-70b-instruct` |
| `deepseek` | `████████████▊░` 91.1% | 24 | $0.0511 | 15.16M | `deepseek-chat` |
| `gemini` | `███████████▍░░` 81.5% | 58 | n/a | 13.62M | `gemini-2.5-flash, gemini-2.5-pro` |
| `anthropic` | `██████████▊░░░` 76.4% | 83 | n/a | 7.16M | `claude-haiku-4-5, claude-sonnet-4-6` |

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
  <img alt="Failure categories by provider — anthropic has the most failures (83)" src="assets/smoke-health/failure-split-light.svg" width="760">
</picture>

<details>
<summary><b>Failure detail</b> — counts, share & sample signatures</summary>

| Provider | Category | Failures | % of fails | Sample signature |
|---|---|--:|--:|---|
| `anthropic` | deterministic | 79 | 95.2 | `business rule task()::400 - {"type":"error","error":{"type":"invalid_request_er…` |
| `gemini` | deterministic | 58 | 100.0 | `business rule task()::429 - [{` |
| `deepseek` | classification | 21 | 87.5 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `llama` | classification | 15 | 83.3 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `openai` | classification | 4 | 66.7 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `anthropic` | classification | 4 | 4.8 | `error boundary event()::Expected an activity carrying a ERROR boundary event, b…` |
| `deepseek` | deterministic | 3 | 12.5 | `escalation end()::TIMER (boundaryEvent) requires detail` |
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
| `error boundary event()` | `█████████▏░░` 38.2% | 5 — anthropic, deepseek, gemini, llama, openai | 55 |
| `event-based gateway()` | `████▏░░░░░░░` 17.2% | 3 — anthropic, llama, openai | 58 |
| `signal end()` | `████░░░░░░░░` 16.7% | 4 — anthropic, deepseek, gemini, llama | 54 |
| `intermediate signal throw()` | `████░░░░░░░░` 16.7% | 3 — anthropic, gemini, llama | 54 |
| `escalation end()` | `███▉░░░░░░░░` 16.4% | 3 — anthropic, deepseek, gemini | 55 |
| `parallel gateway()` | `███▉░░░░░░░░` 16.1% | 3 — anthropic, gemini, llama | 56 |

<details>
<summary>28 more flaky tests (≤ 14.3% fail rate)</summary>

| Test | Fail rate | Providers failed | Samples |
|---|:--|---|--:|
| `escalation boundary event()` | `███▍░░░░░░░░` 14.3% | 3 — anthropic, deepseek, gemini | 56 |
| `business rule task()` | `███▏░░░░░░░░` 13.0% | 2 — anthropic, gemini | 54 |
| `data objects and stores()` | `███▏░░░░░░░░` 13.0% | 2 — anthropic, gemini | 54 |
| `manual task()` | `███▏░░░░░░░░` 13.0% | 2 — anthropic, gemini | 54 |
| `message start()` | `███▏░░░░░░░░` 13.0% | 2 — anthropic, gemini | 54 |
| `sequential multi-instance activity()` | `███▏░░░░░░░░` 13.0% | 2 — anthropic, gemini | 54 |
| `timer start()` | `███▏░░░░░░░░` 13.0% | 2 — anthropic, gemini | 54 |
| `standard loop activity()` | `███░░░░░░░░░` 12.7% | 3 — anthropic, deepseek, gemini | 55 |
| `exclusive gateway()` | `██▏░░░░░░░░░` 9.1% | 3 — anthropic, gemini, llama | 55 |
| `event subprocess()` | `██▏░░░░░░░░░` 8.9% | 3 — anthropic, gemini, mistral | 56 |
| `timer boundary event()` | `██▏░░░░░░░░░` 8.9% | 3 — anthropic, gemini, mistral | 56 |
| `intermediate message throw()` | `██▏░░░░░░░░░` 8.8% | 3 — anthropic, gemini, llama | 57 |
| `script task()` | `█▊░░░░░░░░░░` 7.3% | 2 — anthropic, gemini | 55 |
| `error end()` | `█▊░░░░░░░░░░` 7.1% | 2 — anthropic, gemini | 56 |
| `pools and lanes from distinct actors()` | `█▊░░░░░░░░░░` 7.1% | 2 — anthropic, gemini | 56 |
| `message end()` | `█▋░░░░░░░░░░` 7.0% | 2 — anthropic, gemini | 57 |
| `receive task()` | `█▋░░░░░░░░░░` 7.0% | 2 — anthropic, gemini | 57 |
| `signal start()` | `█▋░░░░░░░░░░` 7.0% | 2 — anthropic, gemini | 57 |
| `parallel multi-instance activity()` | `█▎░░░░░░░░░░` 5.4% | 3 — anthropic, deepseek, gemini | 56 |
| `intermediate escalation throw()` | `█▎░░░░░░░░░░` 5.2% | 2 — anthropic, deepseek | 58 |
| `terminate end()` | `█▎░░░░░░░░░░` 5.2% | 2 — anthropic, openai | 58 |
| `call activity()` | `█▏░░░░░░░░░░` 4.5% | 2 — anthropic, gemini | 44 |
| `embedded subprocess()` | `▉░░░░░░░░░░░` 3.6% | 2 — anthropic, gemini | 56 |
| `exclusive gateway with default branch()` | `▉░░░░░░░░░░░` 3.6% | 2 — anthropic, gemini | 56 |
| `send task()` | `▉░░░░░░░░░░░` 3.6% | 2 — anthropic, gemini | 56 |
| `inclusive gateway()` | `▉░░░░░░░░░░░` 3.4% | 1 — anthropic | 58 |
| `service task()` | `▉░░░░░░░░░░░` 3.4% | 1 — anthropic | 58 |
| `user task()` | `▉░░░░░░░░░░░` 3.4% | 1 — anthropic | 58 |

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
