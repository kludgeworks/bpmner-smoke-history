# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 17 | 98.0 | 2 | $0.5924 | 2716463 |
| deepseek | `deepseek-chat` | 9 | 82.2 | 8 | $0.0423 | 2348727 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 17 | 100.0 | 0 | $0.4193 | 4466311 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 17 | 91.8 | 8 | $0.2312 | 4445275 |
| mistral | `mistral-large-2411,mistral-small-2506` | 17 | 98.9 | 1 | $0.4548 | 7208350 |
| openai | `gpt-4.1-mini,gpt-4.1` | 17 | 97.9 | 2 | $0.4983 | 4561514 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `error boundary event()` | 31.3 | 2 (anthropic, deepseek) | 16 |
| `event-based gateway()` | 18.8 | 2 (llama, openai) | 16 |
| `intermediate signal throw()` | 13.3 | 1 (llama) | 15 |
| `escalation end()` | 12.5 | 1 (deepseek) | 16 |
| `parallel gateway()` | 12.5 | 1 (llama) | 16 |
| `standard loop activity()` | 12.5 | 1 (deepseek) | 16 |
| `signal end()` | 6.7 | 1 (llama) | 15 |
| `intermediate escalation throw()` | 6.3 | 1 (deepseek) | 16 |
| `intermediate message throw()` | 6.3 | 1 (llama) | 16 |
| `terminate end()` | 6.3 | 1 (openai) | 16 |
| `timer boundary event()` | 6.3 | 1 (mistral) | 16 |

## Failure categories

_`deterministic` = harness/config failure (e.g. context load); `classification` = the model produced a wrong answer. Separates 'the harness broke' from 'the model struggled'._

| Provider | Category | Failures | % of provider fails | Sample signature |
|---|---|---:|---:|---|
| anthropic | classification | 2 | 100.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | classification | 7 | 87.5 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | deterministic | 1 | 12.5 | escalation end()::TIMER (boundaryEvent) requires detail |
| llama | classification | 6 | 75.0 | event-based gateway()::Expected decision gateway of kind EVENT_BASED, but fou… |
| llama | deterministic | 2 | 25.0 | event-based gateway()::RECEIVE (act-wait-for-response) requires messageName |
| mistral | infra | 1 | 100.0 | timer boundary event()::timer boundary event() timed out after 240 seconds |
| openai | classification | 1 | 50.0 | terminate end()::Expected end state of type Terminate in contract, but found:… |
| openai | deterministic | 1 | 50.0 | event-based gateway()::RECEIVE (act-await-response) requires messageName |

## Stage breakdown

_Per-pipeline-stage model and token usage (readiness vs extraction)._

| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |
|---|---|---|---:|---:|---:|---:|
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 916692 | 763665 | 348 | 99 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 850432 | 185674 | 198 | 99 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 405375 | 292998 | 177 | 45 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 1573708 | 76646 | 100 | 45 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 700665 | 530754 | 285 | 90 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 3057954 | 176938 | 184 | 90 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 744015 | 316896 | 333 | 98 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 3267764 | 116600 | 216 | 98 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 2658606 | 1381092 | 1143 | 90 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 2990032 | 178620 | 190 | 90 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 791910 | 472242 | 357 | 96 |
| openai | ValidatedProcessContract | `gpt-4.1` | 3163488 | 133874 | 208 | 96 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 5 | 5.5 | 5 | 8 | 14 | 1.4 | 99 |
| deepseek | 5 | 6.2 | 5 | 10 | 18 | 2.6 | 45 |
| gemini | 5 | 5.2 | 5 | 7 | 8 | 0.7 | 90 |
| llama | 5 | 5.6 | 5 | 8 | 11 | 1.3 | 98 |
| mistral | 5 | 14.8 | 11 | 42 | 69 | 12.1 | 90 |
| openai | 5 | 5.9 | 5 | 9 | 23 | 2.4 | 96 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
