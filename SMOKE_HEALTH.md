# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 27 | 94.9 | 8 | n/a* | 4139910 |
| deepseek | `deepseek-chat` | 19 | 87.5 | 12 | $0.0455 | 5304686 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 27 | 100.0 | 0 | $0.4433 | 7587642 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 27 | 93.7 | 10 | $0.2398 | 7334722 |
| mistral | `mistral-large-2411,mistral-small-2506` | 27 | 98.6 | 2 | $0.4427 | 10027140 |
| openai | `gpt-4.1-mini,gpt-4.1` | 27 | 97.5 | 4 | $0.5311 | 7722923 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `error boundary event()` | 42.3 | 4 (anthropic, deepseek, llama, openai) | 26 |
| `escalation end()` | 19.2 | 2 (anthropic, deepseek) | 26 |
| `event-based gateway()` | 19.2 | 2 (llama, openai) | 26 |
| `standard loop activity()` | 11.5 | 2 (anthropic, deepseek) | 26 |
| `intermediate signal throw()` | 8.0 | 1 (llama) | 25 |
| `parallel gateway()` | 7.7 | 1 (llama) | 26 |
| `signal end()` | 4.0 | 1 (llama) | 25 |
| `event subprocess()` | 3.8 | 1 (mistral) | 26 |
| `exclusive gateway()` | 3.8 | 1 (anthropic) | 26 |
| `intermediate escalation throw()` | 3.8 | 1 (deepseek) | 26 |
| `intermediate message throw()` | 3.8 | 1 (llama) | 26 |
| `script task()` | 3.8 | 1 (anthropic) | 26 |
| `terminate end()` | 3.8 | 1 (openai) | 26 |
| `timer boundary event()` | 3.8 | 1 (mistral) | 26 |

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
| openai | classification | 2 | 50.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| openai | deterministic | 2 | 50.0 | event-based gateway()::RECEIVE (act-await-response) requires messageName |

## Stage breakdown

_Per-pipeline-stage model and token usage (readiness vs extraction)._

| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |
|---|---|---|---:|---:|---:|---:|
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 1130631 | 935094 | 429 | 158 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 1327316 | 285526 | 306 | 158 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 673911 | 487890 | 294 | 96 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 3429900 | 159596 | 216 | 96 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 1048623 | 771882 | 426 | 146 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 4985688 | 289914 | 298 | 146 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 966105 | 399063 | 432 | 158 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 5423330 | 190220 | 356 | 158 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 3043116 | 1556328 | 1308 | 141 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 4721482 | 277916 | 298 | 141 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 1051815 | 631557 | 474 | 159 |
| openai | ValidatedProcessContract | `gpt-4.1` | 5362192 | 225586 | 350 | 159 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 0 | 5.3 | 5 | 8 | 14 | 1.6 | 158 |
| deepseek | 5 | 6.8 | 5 | 14 | 20 | 3.3 | 96 |
| gemini | 5 | 5.8 | 5 | 8 | 20 | 2.0 | 146 |
| llama | 5 | 5.7 | 5 | 9 | 15 | 1.6 | 158 |
| mistral | 5 | 12.3 | 8 | 32 | 69 | 10.6 | 141 |
| openai | 5 | 6.0 | 5 | 11 | 23 | 2.6 | 159 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
