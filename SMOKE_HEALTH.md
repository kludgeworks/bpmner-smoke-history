# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 28 | 95.2 | 8 | n/a* | 4341175 |
| deepseek | `deepseek-chat` | 20 | 88.2 | 12 | $0.0458 | 5615007 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 28 | 100.0 | 0 | $0.4426 | 7845891 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 28 | 93.3 | 11 | $0.2388 | 7573403 |
| mistral | `mistral-large-2411,mistral-small-2506` | 28 | 98.6 | 2 | $0.4405 | 10250500 |
| openai | `gpt-4.1-mini,gpt-4.1` | 28 | 97.6 | 4 | $0.5345 | 8042968 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `error boundary event()` | 40.7 | 4 (anthropic, deepseek, llama, openai) | 27 |
| `escalation end()` | 18.5 | 2 (anthropic, deepseek) | 27 |
| `event-based gateway()` | 18.5 | 2 (llama, openai) | 27 |
| `standard loop activity()` | 11.1 | 2 (anthropic, deepseek) | 27 |
| `exclusive gateway()` | 7.4 | 2 (anthropic, llama) | 27 |
| `intermediate signal throw()` | 7.7 | 1 (llama) | 26 |
| `parallel gateway()` | 7.4 | 1 (llama) | 27 |
| `signal end()` | 3.8 | 1 (llama) | 26 |
| `event subprocess()` | 3.7 | 1 (mistral) | 27 |
| `intermediate escalation throw()` | 3.7 | 1 (deepseek) | 27 |
| `intermediate message throw()` | 3.7 | 1 (llama) | 27 |
| `script task()` | 3.7 | 1 (anthropic) | 27 |
| `terminate end()` | 3.7 | 1 (openai) | 27 |
| `timer boundary event()` | 3.7 | 1 (mistral) | 27 |

## Failure categories

_`deterministic` = harness/config failure (e.g. context load); `classification` = the model produced a wrong answer. Separates 'the harness broke' from 'the model struggled'._

| Provider | Category | Failures | % of provider fails | Sample signature |
|---|---|---:|---:|---|
| anthropic | deterministic | 5 | 62.5 | error boundary event()::400 - {"type":"error","error":{"type":"invalid_reques… |
| anthropic | classification | 3 | 37.5 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | classification | 10 | 83.3 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | deterministic | 2 | 16.7 | escalation end()::TIMER (boundaryEvent) requires detail |
| llama | classification | 8 | 72.7 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| llama | deterministic | 2 | 18.2 | event-based gateway()::RECEIVE (act-wait-for-response) requires messageName |
| llama | infra | 1 | 9.1 | exclusive gateway()::exclusive gateway() timed out after 240 seconds |
| mistral | deterministic | 1 | 50.0 | event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind |
| mistral | infra | 1 | 50.0 | timer boundary event()::timer boundary event() timed out after 240 seconds |
| openai | classification | 2 | 50.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| openai | deterministic | 2 | 50.0 | event-based gateway()::RECEIVE (act-await-response) requires messageName |

## Stage breakdown

_Per-pipeline-stage model and token usage (readiness vs extraction)._

| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |
|---|---|---|---:|---:|---:|---:|
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 1130631 | 935094 | 429 | 166 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 1398200 | 300392 | 322 | 166 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 673911 | 487890 | 294 | 102 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 3622246 | 169892 | 228 | 102 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 1048623 | 771882 | 426 | 151 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 5155058 | 301354 | 308 | 151 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 966105 | 399063 | 432 | 163 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 5608570 | 197506 | 368 | 163 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 3043116 | 1556328 | 1308 | 145 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 4882034 | 286346 | 308 | 145 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 1051815 | 631557 | 474 | 165 |
| openai | ValidatedProcessContract | `gpt-4.1` | 5609470 | 235602 | 366 | 165 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 0 | 5.3 | 5 | 8 | 14 | 1.5 | 166 |
| deepseek | 5 | 6.8 | 5 | 14 | 20 | 3.3 | 102 |
| gemini | 5 | 5.8 | 5 | 8 | 20 | 2.0 | 151 |
| llama | 5 | 5.7 | 5 | 9 | 15 | 1.6 | 163 |
| mistral | 5 | 12.1 | 8 | 32 | 69 | 10.5 | 145 |
| openai | 5 | 6.0 | 5 | 10 | 23 | 2.6 | 165 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
