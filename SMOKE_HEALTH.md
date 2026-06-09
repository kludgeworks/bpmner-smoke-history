# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 19 | 93.8 | 7 | n/a* | 2934974 |
| deepseek | `deepseek-chat` | 11 | 85.5 | 8 | $0.0422 | 2860852 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 19 | 100.0 | 0 | $0.4270 | 5089928 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 19 | 91.7 | 9 | $0.2311 | 4969411 |
| mistral | `mistral-large-2411,mistral-small-2506` | 19 | 98.0 | 2 | $0.4441 | 7739182 |
| openai | `gpt-4.1-mini,gpt-4.1` | 19 | 97.3 | 3 | $0.5120 | 5250273 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `error boundary event()` | 38.9 | 3 (anthropic, deepseek, llama) | 18 |
| `event-based gateway()` | 22.2 | 2 (llama, openai) | 18 |
| `escalation end()` | 16.7 | 2 (anthropic, deepseek) | 18 |
| `standard loop activity()` | 16.7 | 2 (anthropic, deepseek) | 18 |
| `intermediate signal throw()` | 11.8 | 1 (llama) | 17 |
| `parallel gateway()` | 11.1 | 1 (llama) | 18 |
| `signal end()` | 5.9 | 1 (llama) | 17 |
| `event subprocess()` | 5.6 | 1 (mistral) | 18 |
| `exclusive gateway()` | 5.6 | 1 (anthropic) | 18 |
| `intermediate escalation throw()` | 5.6 | 1 (deepseek) | 18 |
| `intermediate message throw()` | 5.6 | 1 (llama) | 18 |
| `script task()` | 5.6 | 1 (anthropic) | 18 |
| `terminate end()` | 5.6 | 1 (openai) | 18 |
| `timer boundary event()` | 5.6 | 1 (mistral) | 18 |

## Failure categories

_`deterministic` = harness/config failure (e.g. context load); `classification` = the model produced a wrong answer. Separates 'the harness broke' from 'the model struggled'._

| Provider | Category | Failures | % of provider fails | Sample signature |
|---|---|---:|---:|---|
| anthropic | deterministic | 5 | 71.4 | error boundary event()::400 - {"type":"error","error":{"type":"invalid_reques… |
| anthropic | classification | 2 | 28.6 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | classification | 7 | 87.5 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | deterministic | 1 | 12.5 | escalation end()::TIMER (boundaryEvent) requires detail |
| llama | classification | 7 | 77.8 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| llama | deterministic | 2 | 22.2 | event-based gateway()::RECEIVE (act-wait-for-response) requires messageName |
| mistral | deterministic | 1 | 50.0 | event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind |
| mistral | infra | 1 | 50.0 | timer boundary event()::timer boundary event() timed out after 240 seconds |
| openai | deterministic | 2 | 66.7 | event-based gateway()::RECEIVE (act-await-response) requires messageName |
| openai | classification | 1 | 33.3 | terminate end()::Expected end state of type Terminate in contract, but found:… |

## Stage breakdown

_Per-pipeline-stage model and token usage (readiness vs extraction)._

| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |
|---|---|---|---:|---:|---:|---:|
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 987963 | 824523 | 375 | 112 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 921444 | 201044 | 214 | 112 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 508779 | 366105 | 222 | 55 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 1894280 | 91688 | 120 | 55 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 833913 | 624495 | 339 | 101 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 3430186 | 201334 | 206 | 101 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 824835 | 345612 | 369 | 109 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 3668278 | 130686 | 242 | 109 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 2819175 | 1447311 | 1212 | 99 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 3278422 | 194274 | 208 | 99 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 918405 | 550824 | 414 | 110 |
| openai | ValidatedProcessContract | `gpt-4.1` | 3628220 | 152824 | 238 | 110 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 0 | 5.3 | 5 | 8 | 14 | 1.8 | 112 |
| deepseek | 5 | 6.2 | 5 | 11 | 18 | 2.5 | 55 |
| gemini | 5 | 5.4 | 5 | 8 | 20 | 1.7 | 101 |
| llama | 5 | 5.6 | 5 | 8 | 11 | 1.3 | 109 |
| mistral | 5 | 14.3 | 11 | 41 | 69 | 11.8 | 99 |
| openai | 5 | 5.9 | 5 | 9 | 23 | 2.4 | 110 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
