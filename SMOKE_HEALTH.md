# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 35 | 95.6 | 9 | n/a* | 5309731 |
| deepseek | `deepseek-chat` | 27 | 91.6 | 12 | $0.0479 | 7964108 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 35 | 77.0 | 45 | n/a* | 7845891 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 35 | 93.4 | 13 | $0.2288 | 9072462 |
| mistral | `mistral-large-2411,mistral-small-2506` | 35 | 98.9 | 2 | $0.4649 | 12746167 |
| openai | `gpt-4.1-mini,gpt-4.1` | 35 | 97.5 | 5 | $0.5221 | 9800660 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `error boundary event()` | 44.1 | 5 (anthropic, deepseek, gemini, llama, openai) | 34 |
| `escalation end()` | 20.6 | 3 (anthropic, deepseek, gemini) | 34 |
| `standard loop activity()` | 14.7 | 3 (anthropic, deepseek, gemini) | 34 |
| `exclusive gateway()` | 11.8 | 3 (anthropic, gemini, llama) | 34 |
| `intermediate signal throw()` | 15.2 | 2 (gemini, llama) | 33 |
| `event-based gateway()` | 14.7 | 2 (llama, openai) | 34 |
| `signal end()` | 12.1 | 2 (gemini, llama) | 33 |
| `parallel gateway()` | 11.8 | 2 (gemini, llama) | 34 |
| `script task()` | 8.8 | 2 (anthropic, gemini) | 34 |
| `escalation boundary event()` | 6.1 | 2 (anthropic, gemini) | 33 |
| `event subprocess()` | 5.9 | 2 (gemini, mistral) | 34 |
| `timer boundary event()` | 5.9 | 2 (gemini, mistral) | 34 |
| `business rule task()` | 9.1 | 1 (gemini) | 33 |
| `data objects and stores()` | 9.1 | 1 (gemini) | 33 |
| `manual task()` | 9.1 | 1 (gemini) | 33 |
| `message start()` | 9.1 | 1 (gemini) | 33 |
| `sequential multi-instance activity()` | 9.1 | 1 (gemini) | 33 |
| `timer start()` | 9.1 | 1 (gemini) | 33 |
| `call activity()` | 4.8 | 1 (gemini) | 21 |
| `embedded subprocess()` | 3.0 | 1 (gemini) | 33 |
| `exclusive gateway with default branch()` | 3.0 | 1 (gemini) | 33 |
| `parallel multi-instance activity()` | 3.0 | 1 (gemini) | 33 |
| `send task()` | 3.0 | 1 (gemini) | 33 |
| `error end()` | 2.9 | 1 (gemini) | 34 |
| `intermediate escalation throw()` | 2.9 | 1 (deepseek) | 34 |

_…and 3 more flaky tests._

## Failure categories

_`deterministic` = harness/config failure (e.g. context load); `classification` = the model produced a wrong answer. Separates 'the harness broke' from 'the model struggled'._

| Provider | Category | Failures | % of provider fails | Sample signature |
|---|---|---:|---:|---|
| anthropic | deterministic | 5 | 55.6 | error boundary event()::400 - {"type":"error","error":{"type":"invalid_reques… |
| anthropic | classification | 4 | 44.4 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | classification | 10 | 83.3 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | deterministic | 2 | 16.7 | escalation end()::TIMER (boundaryEvent) requires detail |
| gemini | deterministic | 45 | 100.0 | business rule task()::429 - [{ |
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
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 1130631 | 935094 | 429 | 205 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 1743768 | 369880 | 400 | 205 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 673911 | 487890 | 294 | 143 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 5252000 | 240246 | 330 | 143 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 1048623 | 771882 | 426 | 196 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 5155058 | 301354 | 308 | 196 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 966105 | 399063 | 432 | 196 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 6717686 | 235876 | 440 | 196 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 3043116 | 1556328 | 1308 | 188 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 6515124 | 376630 | 410 | 188 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 1051815 | 631557 | 474 | 202 |
| openai | ValidatedProcessContract | `gpt-4.1` | 6879832 | 286234 | 448 | 202 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 0 | 5.2 | 5 | 8 | 14 | 1.4 | 205 |
| deepseek | 5 | 6.7 | 5 | 14 | 23 | 3.4 | 143 |
| gemini | 0 | 4.4 | 5 | 8 | 20 | 3.0 | 196 |
| llama | 5 | 5.7 | 5 | 9 | 15 | 1.6 | 196 |
| mistral | 5 | 11.0 | 8 | 30 | 69 | 9.7 | 188 |
| openai | 5 | 5.9 | 5 | 10 | 23 | 2.4 | 202 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
