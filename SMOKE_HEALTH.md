# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 15 | 97.6 | 2 | $0.5788 | 2345633 |
| deepseek | `deepseek-chat` | 7 | 85.3 | 5 | $0.0406 | 1766690 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 15 | 100.0 | 0 | $0.4221 | 3970935 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 15 | 90.6 | 8 | $0.2286 | 3876742 |
| mistral | `mistral-large-2411,mistral-small-2506` | 15 | 98.8 | 1 | $0.4601 | 6407504 |
| openai | `gpt-4.1-mini,gpt-4.1` | 15 | 98.8 | 1 | $0.4895 | 3946501 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `error boundary event()` | 28.6 | 2 (anthropic, deepseek) | 14 |
| `event-based gateway()` | 21.4 | 2 (llama, openai) | 14 |
| `intermediate signal throw()` | 15.4 | 1 (llama) | 13 |
| `parallel gateway()` | 14.3 | 1 (llama) | 14 |
| `signal end()` | 7.7 | 1 (llama) | 13 |
| `escalation end()` | 7.1 | 1 (deepseek) | 14 |
| `intermediate escalation throw()` | 7.1 | 1 (deepseek) | 14 |
| `intermediate message throw()` | 7.1 | 1 (llama) | 14 |
| `standard loop activity()` | 7.1 | 1 (deepseek) | 14 |
| `timer boundary event()` | 7.1 | 1 (mistral) | 14 |

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
| openai | deterministic | 1 | 100.0 | event-based gateway()::RECEIVE (act-await-response) requires messageName |

## Stage breakdown

_Per-pipeline-stage model and token usage (readiness vs extraction)._

| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |
|---|---|---|---:|---:|---:|---:|
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 798105 | 661530 | 303 | 85 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 726206 | 159792 | 170 | 85 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 281250 | 205800 | 123 | 34 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 1221292 | 58348 | 78 | 34 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 626973 | 469416 | 255 | 81 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 2717130 | 157416 | 164 | 81 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 656934 | 282150 | 294 | 85 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 2835660 | 101998 | 188 | 85 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 2350482 | 1228278 | 1011 | 80 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 2668808 | 159936 | 170 | 80 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 672054 | 399663 | 303 | 85 |
| openai | ValidatedProcessContract | `gpt-4.1` | 2760612 | 114172 | 182 | 85 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 5 | 5.6 | 5 | 8 | 14 | 1.5 | 85 |
| deepseek | 5 | 5.9 | 5 | 8 | 18 | 2.4 | 34 |
| gemini | 5 | 5.2 | 5 | 7 | 8 | 0.7 | 81 |
| llama | 5 | 5.7 | 5 | 8 | 11 | 1.4 | 85 |
| mistral | 5 | 14.8 | 11 | 44 | 69 | 12.4 | 80 |
| openai | 5 | 5.7 | 5 | 8 | 13 | 1.6 | 85 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
