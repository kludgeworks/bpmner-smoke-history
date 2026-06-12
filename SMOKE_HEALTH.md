# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 23 | 94.8 | 7 | n/a* | 3509427 |
| deepseek | `deepseek-chat` | 15 | 87.0 | 10 | $0.0454 | 4190795 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 23 | 100.0 | 0 | $0.4415 | 6430953 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 23 | 92.5 | 10 | $0.2360 | 6151078 |
| mistral | `mistral-large-2411,mistral-small-2506` | 23 | 98.3 | 2 | $0.4517 | 9016268 |
| openai | `gpt-4.1-mini,gpt-4.1` | 23 | 97.0 | 4 | $0.5051 | 6268318 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `error boundary event()` | 40.9 | 4 (anthropic, deepseek, llama, openai) | 22 |
| `event-based gateway()` | 22.7 | 2 (llama, openai) | 22 |
| `escalation end()` | 18.2 | 2 (anthropic, deepseek) | 22 |
| `standard loop activity()` | 13.6 | 2 (anthropic, deepseek) | 22 |
| `intermediate signal throw()` | 9.5 | 1 (llama) | 21 |
| `parallel gateway()` | 9.1 | 1 (llama) | 22 |
| `signal end()` | 4.8 | 1 (llama) | 21 |
| `event subprocess()` | 4.5 | 1 (mistral) | 22 |
| `exclusive gateway()` | 4.5 | 1 (anthropic) | 22 |
| `intermediate escalation throw()` | 4.5 | 1 (deepseek) | 22 |
| `intermediate message throw()` | 4.5 | 1 (llama) | 22 |
| `script task()` | 4.5 | 1 (anthropic) | 22 |
| `terminate end()` | 4.5 | 1 (openai) | 22 |
| `timer boundary event()` | 4.5 | 1 (mistral) | 22 |

## Failure categories

_`deterministic` = harness/config failure (e.g. context load); `classification` = the model produced a wrong answer. Separates 'the harness broke' from 'the model struggled'._

| Provider | Category | Failures | % of provider fails | Sample signature |
|---|---|---:|---:|---|
| anthropic | deterministic | 5 | 71.4 | error boundary event()::400 - {"type":"error","error":{"type":"invalid_reques… |
| anthropic | classification | 2 | 28.6 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | classification | 8 | 80.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | deterministic | 2 | 20.0 | escalation end()::TIMER (boundaryEvent) requires detail |
| llama | classification | 8 | 80.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| llama | deterministic | 2 | 20.0 | event-based gateway()::RECEIVE (act-wait-for-response) requires messageName |
| mistral | infra | 1 | 50.0 | timer boundary event()::timer boundary event() timed out after 240 seconds |
| mistral | deterministic | 1 | 50.0 | event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind |
| openai | classification | 2 | 50.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| openai | deterministic | 2 | 50.0 | event-based gateway()::RECEIVE (act-await-response) requires messageName |

## Stage breakdown

_Per-pipeline-stage model and token usage (readiness vs extraction)._

| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |
|---|---|---|---:|---:|---:|---:|
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 1130631 | 935094 | 429 | 134 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 1115824 | 243386 | 258 | 134 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 673911 | 487890 | 294 | 77 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 2757558 | 130400 | 174 | 77 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 1048623 | 771882 | 426 | 125 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 4241818 | 246680 | 254 | 125 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 966105 | 399063 | 432 | 133 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 4590574 | 161016 | 302 | 133 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 3043116 | 1556328 | 1308 | 121 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 4079832 | 240170 | 258 | 121 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 1051815 | 631557 | 474 | 132 |
| openai | ValidatedProcessContract | `gpt-4.1` | 4341112 | 181434 | 284 | 132 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 0 | 5.3 | 5 | 8 | 14 | 1.7 | 134 |
| deepseek | 5 | 6.5 | 5 | 11 | 20 | 3.0 | 77 |
| gemini | 5 | 5.7 | 5 | 8 | 20 | 2.0 | 125 |
| llama | 5 | 5.6 | 5 | 8 | 15 | 1.5 | 133 |
| mistral | 5 | 13.2 | 8 | 38 | 69 | 11.1 | 121 |
| openai | 5 | 5.9 | 5 | 9 | 23 | 2.3 | 132 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
