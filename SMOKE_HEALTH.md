# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 20 | 94.1 | 7 | n/a* | 3082873 |
| deepseek | `deepseek-chat` | 12 | 83.3 | 10 | $0.0424 | 3124567 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 20 | 100.0 | 0 | $0.4245 | 5355585 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 20 | 92.3 | 9 | $0.2359 | 5341037 |
| mistral | `mistral-large-2411,mistral-small-2506` | 20 | 98.1 | 2 | $0.4459 | 8103286 |
| openai | `gpt-4.1-mini,gpt-4.1` | 20 | 97.4 | 3 | $0.5075 | 5476496 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `error boundary event()` | 42.1 | 3 (anthropic, deepseek, llama) | 19 |
| `escalation end()` | 21.1 | 2 (anthropic, deepseek) | 19 |
| `event-based gateway()` | 21.1 | 2 (llama, openai) | 19 |
| `standard loop activity()` | 15.8 | 2 (anthropic, deepseek) | 19 |
| `intermediate signal throw()` | 11.1 | 1 (llama) | 18 |
| `parallel gateway()` | 10.5 | 1 (llama) | 19 |
| `signal end()` | 5.6 | 1 (llama) | 18 |
| `event subprocess()` | 5.3 | 1 (mistral) | 19 |
| `exclusive gateway()` | 5.3 | 1 (anthropic) | 19 |
| `intermediate escalation throw()` | 5.3 | 1 (deepseek) | 19 |
| `intermediate message throw()` | 5.3 | 1 (llama) | 19 |
| `script task()` | 5.3 | 1 (anthropic) | 19 |
| `terminate end()` | 5.3 | 1 (openai) | 19 |
| `timer boundary event()` | 5.3 | 1 (mistral) | 19 |

## Failure categories

_`deterministic` = harness/config failure (e.g. context load); `classification` = the model produced a wrong answer. Separates 'the harness broke' from 'the model struggled'._

| Provider | Category | Failures | % of provider fails | Sample signature |
|---|---|---:|---:|---|
| anthropic | deterministic | 5 | 71.4 | error boundary event()::400 - {"type":"error","error":{"type":"invalid_reques… |
| anthropic | classification | 2 | 28.6 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | classification | 8 | 80.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | deterministic | 2 | 20.0 | escalation end()::TIMER (boundaryEvent) requires detail |
| llama | classification | 7 | 77.8 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| llama | deterministic | 2 | 22.2 | event-based gateway()::RECEIVE (act-wait-for-response) requires messageName |
| mistral | infra | 1 | 50.0 | timer boundary event()::timer boundary event() timed out after 240 seconds |
| mistral | deterministic | 1 | 50.0 | event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind |
| openai | deterministic | 2 | 66.7 | event-based gateway()::RECEIVE (act-await-response) requires messageName |
| openai | classification | 1 | 33.3 | terminate end()::Expected end state of type Terminate in contract, but found:… |

## Stage breakdown

_Per-pipeline-stage model and token usage (readiness vs extraction)._

| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |
|---|---|---|---:|---:|---:|---:|
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 1035516 | 860205 | 393 | 118 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 974454 | 212698 | 226 | 118 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 563883 | 406734 | 246 | 60 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 2054400 | 99550 | 130 | 60 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 907740 | 675159 | 369 | 105 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 3565308 | 207378 | 214 | 105 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 885135 | 370992 | 396 | 117 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 3945622 | 139288 | 260 | 117 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 2924454 | 1502268 | 1257 | 105 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 3471122 | 205442 | 220 | 105 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 958515 | 574707 | 432 | 115 |
| openai | ValidatedProcessContract | `gpt-4.1` | 3783292 | 159982 | 248 | 115 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 0 | 5.2 | 5 | 8 | 14 | 1.7 | 118 |
| deepseek | 5 | 6.3 | 5 | 11 | 18 | 2.4 | 60 |
| gemini | 5 | 5.6 | 5 | 8 | 20 | 2.1 | 105 |
| llama | 5 | 5.6 | 5 | 8 | 11 | 1.3 | 117 |
| mistral | 5 | 14.1 | 11 | 40 | 69 | 11.6 | 105 |
| openai | 5 | 5.9 | 5 | 9 | 23 | 2.4 | 115 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
