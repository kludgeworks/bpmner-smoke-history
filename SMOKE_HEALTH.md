# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 36 | 95.7 | 9 | n/a* | 5459166 |
| deepseek | `deepseek-chat` | 28 | 91.9 | 12 | $0.0478 | 8237222 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 36 | 74.0 | 53 | n/a* | 7845891 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 36 | 93.5 | 13 | $0.2266 | 9239685 |
| mistral | `mistral-large-2411,mistral-small-2506` | 36 | 99.0 | 2 | $0.4732 | 13167741 |
| openai | `gpt-4.1-mini,gpt-4.1` | 36 | 97.6 | 5 | $0.5189 | 10014357 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `error boundary event()` | 42.9 | 5 (anthropic, deepseek, gemini, llama, openai) | 35 |
| `escalation end()` | 20.0 | 3 (anthropic, deepseek, gemini) | 35 |
| `standard loop activity()` | 14.3 | 3 (anthropic, deepseek, gemini) | 35 |
| `exclusive gateway()` | 11.4 | 3 (anthropic, gemini, llama) | 35 |
| `intermediate signal throw()` | 17.6 | 2 (gemini, llama) | 34 |
| `signal end()` | 14.7 | 2 (gemini, llama) | 34 |
| `event-based gateway()` | 14.3 | 2 (llama, openai) | 35 |
| `parallel gateway()` | 11.4 | 2 (gemini, llama) | 35 |
| `script task()` | 8.6 | 2 (anthropic, gemini) | 35 |
| `escalation boundary event()` | 5.9 | 2 (anthropic, gemini) | 34 |
| `event subprocess()` | 5.7 | 2 (gemini, mistral) | 35 |
| `timer boundary event()` | 5.7 | 2 (gemini, mistral) | 35 |
| `business rule task()` | 11.8 | 1 (gemini) | 34 |
| `data objects and stores()` | 11.8 | 1 (gemini) | 34 |
| `manual task()` | 11.8 | 1 (gemini) | 34 |
| `message start()` | 11.8 | 1 (gemini) | 34 |
| `sequential multi-instance activity()` | 11.8 | 1 (gemini) | 34 |
| `timer start()` | 11.8 | 1 (gemini) | 34 |
| `call activity()` | 4.5 | 1 (gemini) | 22 |
| `embedded subprocess()` | 2.9 | 1 (gemini) | 34 |
| `error end()` | 2.9 | 1 (gemini) | 35 |
| `exclusive gateway with default branch()` | 2.9 | 1 (gemini) | 34 |
| `intermediate escalation throw()` | 2.9 | 1 (deepseek) | 35 |
| `intermediate message throw()` | 2.9 | 1 (llama) | 35 |
| `parallel multi-instance activity()` | 2.9 | 1 (gemini) | 34 |

_…and 3 more flaky tests._

## Failure categories

_`deterministic` = harness/config failure (e.g. context load); `classification` = the model produced a wrong answer. Separates 'the harness broke' from 'the model struggled'._

| Provider | Category | Failures | % of provider fails | Sample signature |
|---|---|---:|---:|---|
| anthropic | deterministic | 5 | 55.6 | error boundary event()::400 - {"type":"error","error":{"type":"invalid_reques… |
| anthropic | classification | 4 | 44.4 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | classification | 10 | 83.3 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | deterministic | 2 | 16.7 | escalation end()::TIMER (boundaryEvent) requires detail |
| gemini | deterministic | 53 | 100.0 | business rule task()::429 - [{ |
| llama | classification | 10 | 76.9 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| llama | deterministic | 2 | 15.4 | event-based gateway()::RECEIVE (act-wait-for-response) requires messageName |
| llama | infra | 1 | 7.7 | exclusive gateway()::exclusive gateway() timed out after 240 seconds |
| mistral | deterministic | 1 | 50.0 | event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind |
| mistral | infra | 1 | 50.0 | timer boundary event()::timer boundary event() timed out after 240 seconds |
| openai | classification | 3 | 60.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| openai | deterministic | 2 | 40.0 | event-based gateway()::RECEIVE (act-await-response) requires messageName |

## Stage breakdown

_Per-pipeline-stage model and token usage (readiness vs extraction)._

| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |
|---|---|---|---:|---:|---:|---:|
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 1130631 | 935094 | 429 | 211 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 1796946 | 381594 | 412 | 211 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 673911 | 487890 | 294 | 148 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 5412212 | 248574 | 340 | 148 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 1048623 | 771882 | 426 | 204 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 5155058 | 301354 | 308 | 204 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 966105 | 399063 | 432 | 200 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 6841162 | 239786 | 448 | 200 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 3043116 | 1556328 | 1308 | 194 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 6834836 | 394744 | 430 | 194 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 1051815 | 631557 | 474 | 207 |
| openai | ValidatedProcessContract | `gpt-4.1` | 7034778 | 292986 | 458 | 207 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 0 | 5.2 | 5 | 8 | 14 | 1.4 | 211 |
| deepseek | 5 | 6.7 | 5 | 14 | 23 | 3.4 | 148 |
| gemini | 0 | 4.3 | 5 | 8 | 20 | 3.1 | 204 |
| llama | 5 | 5.7 | 5 | 9 | 15 | 1.5 | 200 |
| mistral | 5 | 10.9 | 8 | 30 | 69 | 9.5 | 194 |
| openai | 5 | 5.9 | 5 | 10 | 23 | 2.4 | 207 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
