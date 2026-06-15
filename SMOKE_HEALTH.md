# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 38 | 95.9 | 9 | n/a* | 5743605 |
| deepseek | `deepseek-chat` | 29 | 92.3 | 12 | $0.0487 | 8701720 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 38 | 73.4 | 57 | n/a* | 8133105 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 37 | 93.2 | 14 | $0.2285 | 9577851 |
| mistral | `mistral-large-2411,mistral-small-2506` | 38 | 99.0 | 2 | $0.4709 | 13763478 |
| openai | `gpt-4.1-mini,gpt-4.1` | 38 | 97.7 | 5 | $0.5110 | 10399679 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `error boundary event()` | 41.7 | 5 (anthropic, deepseek, gemini, llama, openai) | 36 |
| `escalation end()` | 19.4 | 3 (anthropic, deepseek, gemini) | 36 |
| `standard loop activity()` | 13.9 | 3 (anthropic, deepseek, gemini) | 36 |
| `exclusive gateway()` | 11.1 | 3 (anthropic, gemini, llama) | 36 |
| `intermediate signal throw()` | 17.1 | 2 (gemini, llama) | 35 |
| `event-based gateway()` | 16.2 | 2 (llama, openai) | 37 |
| `signal end()` | 14.3 | 2 (gemini, llama) | 35 |
| `parallel gateway()` | 10.8 | 2 (gemini, llama) | 37 |
| `script task()` | 8.3 | 2 (anthropic, gemini) | 36 |
| `escalation boundary event()` | 5.6 | 2 (anthropic, gemini) | 36 |
| `event subprocess()` | 5.4 | 2 (gemini, mistral) | 37 |
| `intermediate message throw()` | 5.4 | 2 (gemini, llama) | 37 |
| `timer boundary event()` | 5.4 | 2 (gemini, mistral) | 37 |
| `business rule task()` | 11.4 | 1 (gemini) | 35 |
| `data objects and stores()` | 11.4 | 1 (gemini) | 35 |
| `manual task()` | 11.4 | 1 (gemini) | 35 |
| `message start()` | 11.4 | 1 (gemini) | 35 |
| `sequential multi-instance activity()` | 11.4 | 1 (gemini) | 35 |
| `timer start()` | 11.4 | 1 (gemini) | 35 |
| `call activity()` | 4.2 | 1 (gemini) | 24 |
| `embedded subprocess()` | 2.8 | 1 (gemini) | 36 |
| `exclusive gateway with default branch()` | 2.8 | 1 (gemini) | 36 |
| `parallel multi-instance activity()` | 2.8 | 1 (gemini) | 36 |
| `send task()` | 2.8 | 1 (gemini) | 36 |
| `error end()` | 2.7 | 1 (gemini) | 37 |

_…and 6 more flaky tests._

## Failure categories

_`deterministic` = harness/config failure (e.g. context load); `classification` = the model produced a wrong answer. Separates 'the harness broke' from 'the model struggled'._

| Provider | Category | Failures | % of provider fails | Sample signature |
|---|---|---:|---:|---|
| anthropic | deterministic | 5 | 55.6 | error boundary event()::400 - {"type":"error","error":{"type":"invalid_reques… |
| anthropic | classification | 4 | 44.4 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | classification | 10 | 83.3 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | deterministic | 2 | 16.7 | escalation end()::TIMER (boundaryEvent) requires detail |
| gemini | deterministic | 57 | 100.0 | business rule task()::429 - [{ |
| llama | classification | 11 | 78.6 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| llama | deterministic | 2 | 14.3 | event-based gateway()::RECEIVE (act-wait-for-response) requires messageName |
| llama | infra | 1 | 7.1 | exclusive gateway()::exclusive gateway() timed out after 240 seconds |
| mistral | infra | 1 | 50.0 | timer boundary event()::timer boundary event() timed out after 240 seconds |
| mistral | deterministic | 1 | 50.0 | event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind |
| openai | classification | 3 | 60.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| openai | deterministic | 2 | 40.0 | event-based gateway()::RECEIVE (act-await-response) requires messageName |

## Stage breakdown

_Per-pipeline-stage model and token usage (readiness vs extraction)._

| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |
|---|---|---|---:|---:|---:|---:|
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 1130631 | 935094 | 429 | 222 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 1893946 | 402806 | 434 | 222 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 673911 | 487890 | 294 | 156 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 5699688 | 261442 | 358 | 156 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 1048623 | 771882 | 426 | 214 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 5358256 | 312842 | 320 | 214 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 966105 | 399063 | 432 | 206 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 7088258 | 249202 | 464 | 206 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 3043116 | 1556328 | 1308 | 205 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 7187762 | 413890 | 452 | 205 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 1051815 | 631557 | 474 | 216 |
| openai | ValidatedProcessContract | `gpt-4.1` | 7313942 | 305364 | 476 | 216 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 0 | 5.2 | 5 | 8 | 14 | 1.4 | 222 |
| deepseek | 5 | 6.8 | 5 | 14 | 23 | 3.5 | 156 |
| gemini | 0 | 4.2 | 5 | 8 | 20 | 3.0 | 214 |
| llama | 5 | 5.7 | 5 | 8 | 15 | 1.6 | 206 |
| mistral | 5 | 10.7 | 8 | 29 | 69 | 9.4 | 205 |
| openai | 5 | 5.9 | 5 | 10 | 23 | 2.3 | 216 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
