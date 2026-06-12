# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 25 | 94.6 | 8 | n/a* | 3868239 |
| deepseek | `deepseek-chat` | 17 | 88.5 | 10 | $0.0448 | 4682349 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 25 | 100.0 | 0 | $0.4447 | 7029788 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 25 | 93.1 | 10 | $0.2360 | 6685083 |
| mistral | `mistral-large-2411,mistral-small-2506` | 25 | 98.5 | 2 | $0.4436 | 9490194 |
| openai | `gpt-4.1-mini,gpt-4.1` | 25 | 97.3 | 4 | $0.5287 | 7108068 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `error boundary event()` | 41.7 | 4 (anthropic, deepseek, llama, openai) | 24 |
| `event-based gateway()` | 20.8 | 2 (llama, openai) | 24 |
| `escalation end()` | 16.7 | 2 (anthropic, deepseek) | 24 |
| `standard loop activity()` | 12.5 | 2 (anthropic, deepseek) | 24 |
| `intermediate signal throw()` | 8.7 | 1 (llama) | 23 |
| `parallel gateway()` | 8.3 | 1 (llama) | 24 |
| `signal end()` | 4.3 | 1 (llama) | 23 |
| `event subprocess()` | 4.2 | 1 (mistral) | 24 |
| `exclusive gateway()` | 4.2 | 1 (anthropic) | 24 |
| `intermediate escalation throw()` | 4.2 | 1 (deepseek) | 24 |
| `intermediate message throw()` | 4.2 | 1 (llama) | 24 |
| `script task()` | 4.2 | 1 (anthropic) | 24 |
| `terminate end()` | 4.2 | 1 (openai) | 24 |
| `timer boundary event()` | 4.2 | 1 (mistral) | 24 |

## Failure categories

_`deterministic` = harness/config failure (e.g. context load); `classification` = the model produced a wrong answer. Separates 'the harness broke' from 'the model struggled'._

| Provider | Category | Failures | % of provider fails | Sample signature |
|---|---|---:|---:|---|
| anthropic | deterministic | 5 | 62.5 | error boundary event()::400 - {"type":"error","error":{"type":"invalid_reques… |
| anthropic | classification | 3 | 37.5 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | classification | 8 | 80.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | deterministic | 2 | 20.0 | escalation end()::TIMER (boundaryEvent) requires detail |
| llama | classification | 8 | 80.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| llama | deterministic | 2 | 20.0 | event-based gateway()::RECEIVE (act-wait-for-response) requires messageName |
| mistral | deterministic | 1 | 50.0 | event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind |
| mistral | infra | 1 | 50.0 | timer boundary event()::timer boundary event() timed out after 240 seconds |
| openai | deterministic | 2 | 50.0 | event-based gateway()::RECEIVE (act-await-response) requires messageName |
| openai | classification | 2 | 50.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |

## Stage breakdown

_Per-pipeline-stage model and token usage (readiness vs extraction)._

| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |
|---|---|---|---:|---:|---:|---:|
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 1130631 | 935094 | 429 | 147 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 1230518 | 265870 | 284 | 147 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 673911 | 487890 | 294 | 87 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 3078152 | 145372 | 194 | 87 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 1048623 | 771882 | 426 | 136 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 4647176 | 271158 | 278 | 136 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 966105 | 399063 | 432 | 144 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 4960494 | 173322 | 326 | 144 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 3043116 | 1556328 | 1308 | 130 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 4368428 | 255988 | 276 | 130 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 1051815 | 631557 | 474 | 146 |
| openai | ValidatedProcessContract | `gpt-4.1` | 4959076 | 206906 | 324 | 146 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 0 | 5.3 | 5 | 8 | 14 | 1.6 | 147 |
| deepseek | 5 | 6.5 | 5 | 11 | 20 | 2.9 | 87 |
| gemini | 5 | 5.7 | 5 | 8 | 20 | 2.0 | 136 |
| llama | 5 | 5.7 | 5 | 8 | 15 | 1.6 | 144 |
| mistral | 5 | 12.8 | 8 | 35 | 69 | 10.8 | 130 |
| openai | 5 | 6.0 | 5 | 10 | 23 | 2.6 | 146 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
