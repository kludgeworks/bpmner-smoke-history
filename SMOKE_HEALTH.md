# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 26 | 94.8 | 8 | n/a* | 4017463 |
| deepseek | `deepseek-chat` | 18 | 87.0 | 12 | $0.0453 | 5017921 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 26 | 100.0 | 0 | $0.4405 | 7251544 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 26 | 93.4 | 10 | $0.2397 | 7062723 |
| mistral | `mistral-large-2411,mistral-small-2506` | 26 | 98.5 | 2 | $0.4447 | 9780479 |
| openai | `gpt-4.1-mini,gpt-4.1` | 26 | 97.4 | 4 | $0.5260 | 7368113 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `error boundary event()` | 44.0 | 4 (anthropic, deepseek, llama, openai) | 25 |
| `escalation end()` | 20.0 | 2 (anthropic, deepseek) | 25 |
| `event-based gateway()` | 20.0 | 2 (llama, openai) | 25 |
| `standard loop activity()` | 12.0 | 2 (anthropic, deepseek) | 25 |
| `intermediate signal throw()` | 8.3 | 1 (llama) | 24 |
| `parallel gateway()` | 8.0 | 1 (llama) | 25 |
| `signal end()` | 4.2 | 1 (llama) | 24 |
| `event subprocess()` | 4.0 | 1 (mistral) | 25 |
| `exclusive gateway()` | 4.0 | 1 (anthropic) | 25 |
| `intermediate escalation throw()` | 4.0 | 1 (deepseek) | 25 |
| `intermediate message throw()` | 4.0 | 1 (llama) | 25 |
| `script task()` | 4.0 | 1 (anthropic) | 25 |
| `terminate end()` | 4.0 | 1 (openai) | 25 |
| `timer boundary event()` | 4.0 | 1 (mistral) | 25 |

## Failure categories

_`deterministic` = harness/config failure (e.g. context load); `classification` = the model produced a wrong answer. Separates 'the harness broke' from 'the model struggled'._

| Provider | Category | Failures | % of provider fails | Sample signature |
|---|---|---:|---:|---|
| anthropic | deterministic | 5 | 62.5 | error boundary event()::400 - {"type":"error","error":{"type":"invalid_reques… |
| anthropic | classification | 3 | 37.5 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | classification | 10 | 83.3 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | deterministic | 2 | 16.7 | escalation end()::TIMER (boundaryEvent) requires detail |
| llama | classification | 8 | 80.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| llama | deterministic | 2 | 20.0 | event-based gateway()::RECEIVE (act-wait-for-response) requires messageName |
| mistral | infra | 1 | 50.0 | timer boundary event()::timer boundary event() timed out after 240 seconds |
| mistral | deterministic | 1 | 50.0 | event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind |
| openai | deterministic | 2 | 50.0 | event-based gateway()::RECEIVE (act-await-response) requires messageName |
| openai | classification | 2 | 50.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |

## Stage breakdown

_Per-pipeline-stage model and token usage (readiness vs extraction)._

| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |
|---|---|---|---:|---:|---:|---:|
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 1130631 | 935094 | 429 | 153 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 1283334 | 277252 | 296 | 153 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 673911 | 487890 | 294 | 92 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 3301978 | 155028 | 208 | 92 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 1048623 | 771882 | 426 | 140 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 4782866 | 277604 | 286 | 140 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 966105 | 399063 | 432 | 152 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 5237746 | 181862 | 344 | 152 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 3043116 | 1556328 | 1308 | 136 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 4561234 | 268396 | 288 | 136 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 1051815 | 631557 | 474 | 151 |
| openai | ValidatedProcessContract | `gpt-4.1` | 5114134 | 215014 | 334 | 151 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 0 | 5.3 | 5 | 8 | 14 | 1.6 | 153 |
| deepseek | 5 | 6.6 | 5 | 11 | 20 | 3.0 | 92 |
| gemini | 5 | 5.7 | 5 | 8 | 20 | 2.0 | 140 |
| llama | 5 | 5.7 | 5 | 9 | 15 | 1.6 | 152 |
| mistral | 5 | 12.5 | 8 | 33 | 69 | 10.7 | 136 |
| openai | 5 | 6.0 | 5 | 11 | 23 | 2.7 | 151 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
