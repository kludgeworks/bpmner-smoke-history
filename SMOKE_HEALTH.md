# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 16 | 97.8 | 2 | $0.5905 | 2549473 |
| deepseek | `deepseek-chat` | 8 | 87.5 | 5 | $0.0421 | 2085227 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 16 | 100.0 | 0 | $0.4208 | 4215744 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 16 | 91.1 | 8 | $0.2274 | 4114879 |
| mistral | `mistral-large-2411,mistral-small-2506` | 16 | 98.8 | 1 | $0.4515 | 6689492 |
| openai | `gpt-4.1-mini,gpt-4.1` | 16 | 97.8 | 2 | $0.5025 | 4340313 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `error boundary event()` | 26.7 | 2 (anthropic, deepseek) | 15 |
| `event-based gateway()` | 20.0 | 2 (llama, openai) | 15 |
| `intermediate signal throw()` | 14.3 | 1 (llama) | 14 |
| `parallel gateway()` | 13.3 | 1 (llama) | 15 |
| `signal end()` | 7.1 | 1 (llama) | 14 |
| `escalation end()` | 6.7 | 1 (deepseek) | 15 |
| `intermediate escalation throw()` | 6.7 | 1 (deepseek) | 15 |
| `intermediate message throw()` | 6.7 | 1 (llama) | 15 |
| `standard loop activity()` | 6.7 | 1 (deepseek) | 15 |
| `terminate end()` | 6.7 | 1 (openai) | 15 |
| `timer boundary event()` | 6.7 | 1 (mistral) | 15 |

## Failure categories

_`deterministic` = harness/config failure (e.g. context load); `classification` = the model produced a wrong answer. Separates 'the harness broke' from 'the model struggled'._

| Provider | Category | Failures | % of provider fails | Sample signature |
|---|---|---:|---:|---|
| anthropic | classification | 2 | 100.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | classification | 4 | 80.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | deterministic | 1 | 20.0 | escalation end()::TIMER (boundaryEvent) requires detail |
| llama | classification | 6 | 75.0 | event-based gateway()::Expected decision gateway of kind EVENT_BASED, but fou… |
| llama | deterministic | 2 | 25.0 | event-based gateway()::RECEIVE (act-wait-for-response) requires messageName |
| mistral | infra | 1 | 100.0 | timer boundary event()::timer boundary event() timed out after 240 seconds |
| openai | classification | 1 | 50.0 | terminate end()::Expected end state of type Terminate in contract, but found:… |
| openai | deterministic | 1 | 50.0 | event-based gateway()::RECEIVE (act-await-response) requires messageName |

## Stage breakdown

_Per-pipeline-stage model and token usage (readiness vs extraction)._

| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |
|---|---|---|---:|---:|---:|---:|
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 861303 | 716868 | 327 | 93 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 797220 | 174082 | 186 | 93 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 350403 | 252960 | 153 | 40 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 1413572 | 68292 | 90 | 40 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 663888 | 496854 | 270 | 86 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 2886734 | 168268 | 174 | 86 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 690507 | 294702 | 309 | 90 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 3020734 | 108936 | 200 | 90 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 2440731 | 1284903 | 1050 | 84 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 2797296 | 166562 | 178 | 84 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 758598 | 448125 | 342 | 91 |
| openai | ValidatedProcessContract | `gpt-4.1` | 3008304 | 125286 | 198 | 91 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 5 | 5.5 | 5 | 8 | 14 | 1.4 | 93 |
| deepseek | 5 | 6.1 | 5 | 8 | 18 | 2.6 | 40 |
| gemini | 5 | 5.2 | 5 | 6 | 8 | 0.7 | 86 |
| llama | 5 | 5.7 | 5 | 8 | 11 | 1.4 | 90 |
| mistral | 5 | 14.6 | 11 | 43 | 69 | 12.2 | 84 |
| openai | 5 | 5.9 | 5 | 9 | 23 | 2.4 | 91 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
