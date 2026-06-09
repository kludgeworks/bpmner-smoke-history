# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 18 | 93.3 | 7 | n/a* | 2716463 |
| deepseek | `deepseek-chat` | 10 | 83.7 | 8 | $0.0417 | 2565504 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 18 | 100.0 | 0 | $0.4228 | 4759285 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 18 | 92.3 | 8 | $0.2304 | 4691570 |
| mistral | `mistral-large-2411,mistral-small-2506` | 18 | 97.9 | 2 | $0.4523 | 7535834 |
| openai | `gpt-4.1-mini,gpt-4.1` | 18 | 98.1 | 2 | $0.5067 | 4905181 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `error boundary event()` | 35.3 | 2 (anthropic, deepseek) | 17 |
| `escalation end()` | 17.6 | 2 (anthropic, deepseek) | 17 |
| `event-based gateway()` | 17.6 | 2 (llama, openai) | 17 |
| `standard loop activity()` | 17.6 | 2 (anthropic, deepseek) | 17 |
| `intermediate signal throw()` | 12.5 | 1 (llama) | 16 |
| `parallel gateway()` | 11.8 | 1 (llama) | 17 |
| `signal end()` | 6.3 | 1 (llama) | 16 |
| `event subprocess()` | 5.9 | 1 (mistral) | 17 |
| `exclusive gateway()` | 5.9 | 1 (anthropic) | 17 |
| `intermediate escalation throw()` | 5.9 | 1 (deepseek) | 17 |
| `intermediate message throw()` | 5.9 | 1 (llama) | 17 |
| `script task()` | 5.9 | 1 (anthropic) | 17 |
| `terminate end()` | 5.9 | 1 (openai) | 17 |
| `timer boundary event()` | 5.9 | 1 (mistral) | 17 |

## Failure categories

_`deterministic` = harness/config failure (e.g. context load); `classification` = the model produced a wrong answer. Separates 'the harness broke' from 'the model struggled'._

| Provider | Category | Failures | % of provider fails | Sample signature |
|---|---|---:|---:|---|
| anthropic | deterministic | 5 | 71.4 | error boundary event()::400 - {"type":"error","error":{"type":"invalid_reques… |
| anthropic | classification | 2 | 28.6 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | classification | 7 | 87.5 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | deterministic | 1 | 12.5 | escalation end()::TIMER (boundaryEvent) requires detail |
| llama | classification | 6 | 75.0 | event-based gateway()::Expected decision gateway of kind EVENT_BASED, but fou… |
| llama | deterministic | 2 | 25.0 | event-based gateway()::RECEIVE (act-wait-for-response) requires messageName |
| mistral | infra | 1 | 50.0 | timer boundary event()::timer boundary event() timed out after 240 seconds |
| mistral | deterministic | 1 | 50.0 | event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind |
| openai | deterministic | 1 | 50.0 | event-based gateway()::RECEIVE (act-await-response) requires messageName |
| openai | classification | 1 | 50.0 | terminate end()::Expected end state of type Terminate in contract, but found:… |

## Stage breakdown

_Per-pipeline-stage model and token usage (readiness vs extraction)._

| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |
|---|---|---|---:|---:|---:|---:|
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 916692 | 763665 | 348 | 104 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 850432 | 185674 | 198 | 104 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 453279 | 329043 | 198 | 49 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 1701762 | 81420 | 108 | 49 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 744906 | 563229 | 303 | 96 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 3260926 | 190224 | 196 | 96 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 784449 | 330423 | 351 | 104 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 3453362 | 123336 | 228 | 104 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 2770461 | 1425681 | 1191 | 95 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 3150356 | 189336 | 200 | 95 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 845103 | 504678 | 381 | 104 |
| openai | ValidatedProcessContract | `gpt-4.1` | 3411408 | 143992 | 224 | 104 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 0 | 5.3 | 5 | 8 | 14 | 1.8 | 104 |
| deepseek | 5 | 6.2 | 5 | 11 | 18 | 2.6 | 49 |
| gemini | 5 | 5.2 | 5 | 7 | 8 | 0.7 | 96 |
| llama | 5 | 5.6 | 5 | 8 | 11 | 1.3 | 104 |
| mistral | 5 | 14.6 | 11 | 41 | 69 | 12.0 | 95 |
| openai | 5 | 5.8 | 5 | 8 | 23 | 2.3 | 104 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
