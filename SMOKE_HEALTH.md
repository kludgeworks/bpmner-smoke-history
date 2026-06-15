# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 34 | 96.0 | 8 | n/a* | 5159566 |
| deepseek | `deepseek-chat` | 26 | 91.3 | 12 | $0.0481 | 7711117 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 34 | 80.3 | 37 | n/a* | 7845891 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 34 | 93.2 | 13 | $0.2311 | 8899640 |
| mistral | `mistral-large-2411,mistral-small-2506` | 34 | 98.9 | 2 | $0.4540 | 12197698 |
| openai | `gpt-4.1-mini,gpt-4.1` | 34 | 97.5 | 5 | $0.5234 | 9545740 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `error boundary event()` | 45.5 | 5 (anthropic, deepseek, gemini, llama, openai) | 33 |
| `escalation end()` | 21.2 | 3 (anthropic, deepseek, gemini) | 33 |
| `standard loop activity()` | 15.2 | 3 (anthropic, deepseek, gemini) | 33 |
| `exclusive gateway()` | 12.1 | 3 (anthropic, gemini, llama) | 33 |
| `event-based gateway()` | 15.2 | 2 (llama, openai) | 33 |
| `intermediate signal throw()` | 12.5 | 2 (gemini, llama) | 32 |
| `parallel gateway()` | 12.1 | 2 (gemini, llama) | 33 |
| `signal end()` | 9.4 | 2 (gemini, llama) | 32 |
| `script task()` | 9.1 | 2 (anthropic, gemini) | 33 |
| `event subprocess()` | 6.1 | 2 (gemini, mistral) | 33 |
| `timer boundary event()` | 6.1 | 2 (gemini, mistral) | 33 |
| `business rule task()` | 6.3 | 1 (gemini) | 32 |
| `data objects and stores()` | 6.3 | 1 (gemini) | 32 |
| `manual task()` | 6.3 | 1 (gemini) | 32 |
| `message start()` | 6.3 | 1 (gemini) | 32 |
| `sequential multi-instance activity()` | 6.3 | 1 (gemini) | 32 |
| `timer start()` | 6.3 | 1 (gemini) | 32 |
| `call activity()` | 5.0 | 1 (gemini) | 20 |
| `embedded subprocess()` | 3.1 | 1 (gemini) | 32 |
| `escalation boundary event()` | 3.1 | 1 (gemini) | 32 |
| `exclusive gateway with default branch()` | 3.1 | 1 (gemini) | 32 |
| `parallel multi-instance activity()` | 3.1 | 1 (gemini) | 32 |
| `send task()` | 3.1 | 1 (gemini) | 32 |
| `error end()` | 3.0 | 1 (gemini) | 33 |
| `intermediate escalation throw()` | 3.0 | 1 (deepseek) | 33 |

_…and 3 more flaky tests._

## Failure categories

_`deterministic` = harness/config failure (e.g. context load); `classification` = the model produced a wrong answer. Separates 'the harness broke' from 'the model struggled'._

| Provider | Category | Failures | % of provider fails | Sample signature |
|---|---|---:|---:|---|
| anthropic | deterministic | 5 | 62.5 | error boundary event()::400 - {"type":"error","error":{"type":"invalid_reques… |
| anthropic | classification | 3 | 37.5 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | classification | 10 | 83.3 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | deterministic | 2 | 16.7 | escalation end()::TIMER (boundaryEvent) requires detail |
| gemini | deterministic | 37 | 100.0 | business rule task()::429 - [{ |
| llama | classification | 10 | 76.9 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| llama | deterministic | 2 | 15.4 | event-based gateway()::RECEIVE (act-wait-for-response) requires messageName |
| llama | infra | 1 | 7.7 | exclusive gateway()::exclusive gateway() timed out after 240 seconds |
| mistral | infra | 1 | 50.0 | timer boundary event()::timer boundary event() timed out after 240 seconds |
| mistral | deterministic | 1 | 50.0 | event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind |
| openai | classification | 3 | 60.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| openai | deterministic | 2 | 40.0 | event-based gateway()::RECEIVE (act-await-response) requires messageName |

## Stage breakdown

_Per-pipeline-stage model and token usage (readiness vs extraction)._

| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |
|---|---|---|---:|---:|---:|---:|
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 1130631 | 935094 | 429 | 199 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 1690264 | 358458 | 388 | 199 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 673911 | 487890 | 294 | 138 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 5091848 | 231104 | 320 | 138 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 1048623 | 771882 | 426 | 188 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 5155058 | 301354 | 308 | 188 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 966105 | 399063 | 432 | 192 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 6594414 | 232628 | 432 | 192 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 3043116 | 1556328 | 1308 | 182 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 6164280 | 358936 | 388 | 182 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 1051815 | 631557 | 474 | 197 |
| openai | ValidatedProcessContract | `gpt-4.1` | 6694316 | 279590 | 436 | 197 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 0 | 5.2 | 5 | 8 | 14 | 1.4 | 199 |
| deepseek | 5 | 6.7 | 5 | 14 | 23 | 3.4 | 138 |
| gemini | 0 | 4.6 | 5 | 8 | 20 | 2.9 | 188 |
| llama | 5 | 5.7 | 5 | 9 | 15 | 1.6 | 192 |
| mistral | 5 | 11.0 | 8 | 31 | 69 | 9.7 | 182 |
| openai | 5 | 5.9 | 5 | 10 | 23 | 2.4 | 197 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
