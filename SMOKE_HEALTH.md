# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 12 | 98.6 | 1 | $0.6037 | 1962106 |
| deepseek | `deepseek-chat` | 4 | 89.5 | 2 | $0.0367 | 900800 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 12 | 100.0 | 0 | $0.4315 | 3246607 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 12 | 90.9 | 6 | $0.2201 | 2986076 |
| mistral | `mistral-small-2506,mistral-large-2411` | 12 | 100.0 | 0 | $0.4496 | 4843566 |
| openai | `gpt-4.1-mini,gpt-4.1` | 12 | 98.5 | 1 | $0.4871 | 3141770 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `event-based gateway()` | 27.3 | 2 (llama, openai) | 11 |
| `error boundary event()` | 18.2 | 2 (anthropic, deepseek) | 11 |
| `intermediate signal throw()` | 10.0 | 1 (llama) | 10 |
| `signal end()` | 10.0 | 1 (llama) | 10 |
| `intermediate message throw()` | 9.1 | 1 (llama) | 11 |
| `parallel gateway()` | 9.1 | 1 (llama) | 11 |
| `standard loop activity()` | 9.1 | 1 (deepseek) | 11 |

## Failure categories

_`deterministic` = harness/config failure (e.g. context load); `classification` = the model produced a wrong answer. Separates 'the harness broke' from 'the model struggled'._

| Provider | Category | Failures | % of provider fails | Sample signature |
|---|---|---:|---:|---|
| anthropic | classification | 1 | 100.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | classification | 2 | 100.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| llama | classification | 4 | 66.7 | event-based gateway()::Expected decision gateway of kind EVENT_BASED, but fou… |
| llama | deterministic | 2 | 33.3 | event-based gateway()::RECEIVE (act-wait-for-response) requires messageName |
| openai | deterministic | 1 | 100.0 | event-based gateway()::RECEIVE (act-await-response) requires messageName |

## Stage breakdown

_Per-pipeline-stage model and token usage (readiness vs extraction)._

| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |
|---|---|---|---:|---:|---:|---:|
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 671778 | 561966 | 255 | 70 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 596914 | 131448 | 140 | 70 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 157926 | 116622 | 69 | 19 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 594514 | 31738 | 38 | 19 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 516447 | 385122 | 210 | 66 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 2216082 | 128956 | 134 | 66 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 522555 | 219393 | 234 | 66 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 2167902 | 76226 | 144 | 66 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 1707294 | 910692 | 735 | 62 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 2100600 | 124980 | 134 | 62 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 532200 | 310602 | 240 | 67 |
| openai | ValidatedProcessContract | `gpt-4.1` | 2209340 | 89628 | 146 | 67 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 5 | 5.6 | 5 | 8 | 14 | 1.6 | 70 |
| deepseek | 5 | 5.6 | 5 | 8 | 8 | 1.3 | 19 |
| gemini | 5 | 5.2 | 5 | 7 | 8 | 0.8 | 66 |
| llama | 5 | 5.7 | 5 | 8 | 11 | 1.4 | 66 |
| mistral | 5 | 14.0 | 11 | 40 | 44 | 10.7 | 62 |
| openai | 5 | 5.8 | 5 | 8 | 13 | 1.6 | 67 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
