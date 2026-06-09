# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 14 | 98.8 | 1 | $0.5864 | 2221641 |
| deepseek | `deepseek-chat` | 6 | 83.3 | 5 | $0.0426 | 1586135 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 14 | 100.0 | 0 | $0.4179 | 3677128 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 14 | 89.9 | 8 | $0.2286 | 3619866 |
| mistral | `mistral-small-2506,mistral-large-2411` | 14 | 100.0 | 0 | $0.4610 | 5868283 |
| openai | `gpt-4.1-mini,gpt-4.1` | 14 | 98.7 | 1 | $0.4757 | 3568193 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `error boundary event()` | 23.1 | 2 (anthropic, deepseek) | 13 |
| `event-based gateway()` | 23.1 | 2 (llama, openai) | 13 |
| `intermediate signal throw()` | 16.7 | 1 (llama) | 12 |
| `parallel gateway()` | 15.4 | 1 (llama) | 13 |
| `signal end()` | 8.3 | 1 (llama) | 12 |
| `escalation end()` | 7.7 | 1 (deepseek) | 13 |
| `intermediate escalation throw()` | 7.7 | 1 (deepseek) | 13 |
| `intermediate message throw()` | 7.7 | 1 (llama) | 13 |
| `standard loop activity()` | 7.7 | 1 (deepseek) | 13 |

## Failure categories

_`deterministic` = harness/config failure (e.g. context load); `classification` = the model produced a wrong answer. Separates 'the harness broke' from 'the model struggled'._

| Provider | Category | Failures | % of provider fails | Sample signature |
|---|---|---:|---:|---|
| anthropic | classification | 1 | 100.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | classification | 4 | 80.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | deterministic | 1 | 20.0 | escalation end()::TIMER (boundaryEvent) requires detail |
| llama | classification | 6 | 75.0 | event-based gateway()::Expected decision gateway of kind EVENT_BASED, but fou… |
| llama | deterministic | 2 | 25.0 | event-based gateway()::RECEIVE (act-wait-for-response) requires messageName |
| openai | deterministic | 1 | 100.0 | event-based gateway()::RECEIVE (act-await-response) requires messageName |

## Stage breakdown

_Per-pipeline-stage model and token usage (readiness vs extraction)._

| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |
|---|---|---|---:|---:|---:|---:|
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 758610 | 630825 | 288 | 80 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 682146 | 150060 | 160 | 80 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 253872 | 184383 | 111 | 30 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 1093202 | 54678 | 70 | 30 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 582732 | 436260 | 237 | 75 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 2513830 | 144306 | 152 | 75 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 616434 | 258546 | 276 | 79 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 2650042 | 94844 | 176 | 79 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 2105577 | 1105212 | 906 | 75 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 2508178 | 149316 | 160 | 75 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 598965 | 352926 | 270 | 77 |
| openai | ValidatedProcessContract | `gpt-4.1` | 2512510 | 103792 | 166 | 77 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 5 | 5.6 | 5 | 8 | 14 | 1.5 | 80 |
| deepseek | 5 | 6.0 | 5 | 8 | 18 | 2.6 | 30 |
| gemini | 5 | 5.2 | 5 | 7 | 8 | 0.7 | 75 |
| llama | 5 | 5.7 | 5 | 8 | 11 | 1.4 | 79 |
| mistral | 5 | 14.2 | 11 | 41 | 53 | 11.0 | 75 |
| openai | 5 | 5.7 | 5 | 8 | 13 | 1.5 | 77 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
