# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 13 | 98.7 | 1 | $0.6062 | 2127386 |
| deepseek | `deepseek-chat` | 5 | 83.3 | 4 | $0.0373 | 1144251 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 13 | 100.0 | 0 | $0.4206 | 3436391 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 13 | 90.5 | 7 | $0.2272 | 3340720 |
| mistral | `mistral-small-2506,mistral-large-2411` | 13 | 100.0 | 0 | $0.4474 | 5344666 |
| openai | `gpt-4.1-mini,gpt-4.1` | 13 | 98.6 | 1 | $0.4810 | 3354761 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `error boundary event()` | 25.0 | 2 (anthropic, deepseek) | 12 |
| `event-based gateway()` | 25.0 | 2 (llama, openai) | 12 |
| `intermediate signal throw()` | 18.2 | 1 (llama) | 11 |
| `signal end()` | 9.1 | 1 (llama) | 11 |
| `escalation end()` | 8.3 | 1 (deepseek) | 12 |
| `intermediate message throw()` | 8.3 | 1 (llama) | 12 |
| `parallel gateway()` | 8.3 | 1 (llama) | 12 |
| `standard loop activity()` | 8.3 | 1 (deepseek) | 12 |

## Failure categories

_`deterministic` = harness/config failure (e.g. context load); `classification` = the model produced a wrong answer. Separates 'the harness broke' from 'the model struggled'._

| Provider | Category | Failures | % of provider fails | Sample signature |
|---|---|---:|---:|---|
| anthropic | classification | 1 | 100.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | classification | 3 | 75.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | deterministic | 1 | 25.0 | escalation end()::TIMER (boundaryEvent) requires detail |
| llama | classification | 5 | 71.4 | event-based gateway()::Expected decision gateway of kind EVENT_BASED, but fou… |
| llama | deterministic | 2 | 28.6 | event-based gateway()::RECEIVE (act-wait-for-response) requires messageName |
| openai | deterministic | 1 | 100.0 | event-based gateway()::RECEIVE (act-await-response) requires messageName |

## Stage breakdown

_Per-pipeline-stage model and token usage (readiness vs extraction)._

| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |
|---|---|---|---:|---:|---:|---:|
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 727062 | 607374 | 276 | 76 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 648112 | 144838 | 152 | 76 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 205872 | 148299 | 90 | 24 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 750688 | 39392 | 48 | 24 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 545874 | 407211 | 222 | 70 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 2348228 | 135078 | 142 | 70 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 576120 | 240510 | 258 | 74 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 2438860 | 85230 | 162 | 74 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 1938576 | 1014738 | 834 | 67 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 2257460 | 133892 | 144 | 67 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 565512 | 331635 | 255 | 72 |
| openai | ValidatedProcessContract | `gpt-4.1` | 2360752 | 96862 | 156 | 72 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 5 | 5.6 | 5 | 8 | 14 | 1.6 | 76 |
| deepseek | 5 | 5.8 | 5 | 8 | 8 | 1.3 | 24 |
| gemini | 5 | 5.2 | 5 | 7 | 8 | 0.7 | 70 |
| llama | 5 | 5.7 | 5 | 8 | 11 | 1.4 | 74 |
| mistral | 5 | 14.6 | 11 | 43 | 53 | 11.4 | 67 |
| openai | 5 | 5.7 | 5 | 8 | 13 | 1.6 | 72 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
