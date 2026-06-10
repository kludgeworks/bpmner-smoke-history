# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 21 | 94.3 | 7 | n/a* | 3237494 |
| deepseek | `deepseek-chat` | 13 | 85.3 | 10 | $0.0457 | 3673310 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 21 | 100.0 | 0 | $0.4286 | 5684316 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 21 | 91.9 | 10 | $0.2412 | 5740425 |
| mistral | `mistral-large-2411,mistral-small-2506` | 21 | 98.2 | 2 | $0.4429 | 8355510 |
| openai | `gpt-4.1-mini,gpt-4.1` | 21 | 97.5 | 3 | $0.4996 | 5669605 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `error boundary event()` | 40.0 | 3 (anthropic, deepseek, llama) | 20 |
| `event-based gateway()` | 25.0 | 2 (llama, openai) | 20 |
| `escalation end()` | 20.0 | 2 (anthropic, deepseek) | 20 |
| `standard loop activity()` | 15.0 | 2 (anthropic, deepseek) | 20 |
| `intermediate signal throw()` | 10.5 | 1 (llama) | 19 |
| `parallel gateway()` | 10.0 | 1 (llama) | 20 |
| `signal end()` | 5.3 | 1 (llama) | 19 |
| `event subprocess()` | 5.0 | 1 (mistral) | 20 |
| `exclusive gateway()` | 5.0 | 1 (anthropic) | 20 |
| `intermediate escalation throw()` | 5.0 | 1 (deepseek) | 20 |
| `intermediate message throw()` | 5.0 | 1 (llama) | 20 |
| `script task()` | 5.0 | 1 (anthropic) | 20 |
| `terminate end()` | 5.0 | 1 (openai) | 20 |
| `timer boundary event()` | 5.0 | 1 (mistral) | 20 |

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
| mistral | deterministic | 1 | 50.0 | event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind |
| mistral | infra | 1 | 50.0 | timer boundary event()::timer boundary event() timed out after 240 seconds |
| openai | deterministic | 2 | 66.7 | event-based gateway()::RECEIVE (act-await-response) requires messageName |
| openai | classification | 1 | 33.3 | terminate end()::Expected end state of type Terminate in contract, but found:… |

## Stage breakdown

_Per-pipeline-stage model and token usage (readiness vs extraction)._

| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |
|---|---|---|---:|---:|---:|---:|
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 1091016 | 905226 | 414 | 123 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 1018568 | 222684 | 236 | 123 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 632688 | 455808 | 276 | 68 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 2469002 | 115812 | 156 | 68 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 974700 | 721722 | 396 | 111 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 3768566 | 219328 | 226 | 111 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 925539 | 382776 | 414 | 123 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 4281814 | 150296 | 282 | 123 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 2980278 | 1530234 | 1281 | 110 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 3631534 | 213464 | 230 | 110 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 998454 | 598779 | 450 | 119 |
| openai | ValidatedProcessContract | `gpt-4.1` | 3907498 | 164874 | 256 | 119 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 0 | 5.3 | 5 | 8 | 14 | 1.7 | 123 |
| deepseek | 5 | 6.4 | 5 | 11 | 18 | 2.7 | 68 |
| gemini | 5 | 5.6 | 5 | 8 | 20 | 2.1 | 111 |
| llama | 5 | 5.7 | 5 | 8 | 15 | 1.5 | 123 |
| mistral | 5 | 13.7 | 11 | 39 | 69 | 11.4 | 110 |
| openai | 5 | 5.9 | 5 | 9 | 23 | 2.4 | 119 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
