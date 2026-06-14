# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 29 | 95.3 | 8 | n/a* | 4437713 |
| deepseek | `deepseek-chat` | 21 | 88.9 | 12 | $0.0463 | 5955206 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 29 | 96.8 | 5 | n/a* | 7845891 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 29 | 93.5 | 11 | $0.2368 | 7780360 |
| mistral | `mistral-large-2411,mistral-small-2506` | 29 | 98.7 | 2 | $0.4472 | 10713506 |
| openai | `gpt-4.1-mini,gpt-4.1` | 29 | 97.7 | 4 | $0.5334 | 8311587 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `error boundary event()` | 42.9 | 5 (anthropic, deepseek, gemini, llama, openai) | 28 |
| `escalation end()` | 21.4 | 3 (anthropic, deepseek, gemini) | 28 |
| `standard loop activity()` | 14.3 | 3 (anthropic, deepseek, gemini) | 28 |
| `exclusive gateway()` | 10.7 | 3 (anthropic, gemini, llama) | 28 |
| `event-based gateway()` | 17.9 | 2 (llama, openai) | 28 |
| `script task()` | 7.1 | 2 (anthropic, gemini) | 28 |
| `intermediate signal throw()` | 7.4 | 1 (llama) | 27 |
| `parallel gateway()` | 7.1 | 1 (llama) | 28 |
| `signal end()` | 3.7 | 1 (llama) | 27 |
| `event subprocess()` | 3.6 | 1 (mistral) | 28 |
| `intermediate escalation throw()` | 3.6 | 1 (deepseek) | 28 |
| `intermediate message throw()` | 3.6 | 1 (llama) | 28 |
| `terminate end()` | 3.6 | 1 (openai) | 28 |
| `timer boundary event()` | 3.6 | 1 (mistral) | 28 |

## Failure categories

_`deterministic` = harness/config failure (e.g. context load); `classification` = the model produced a wrong answer. Separates 'the harness broke' from 'the model struggled'._

| Provider | Category | Failures | % of provider fails | Sample signature |
|---|---|---:|---:|---|
| anthropic | deterministic | 5 | 62.5 | error boundary event()::400 - {"type":"error","error":{"type":"invalid_reques… |
| anthropic | classification | 3 | 37.5 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | classification | 10 | 83.3 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | deterministic | 2 | 16.7 | escalation end()::TIMER (boundaryEvent) requires detail |
| gemini | deterministic | 5 | 100.0 | error boundary event()::429 - [{ |
| llama | classification | 8 | 72.7 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| llama | deterministic | 2 | 18.2 | event-based gateway()::RECEIVE (act-wait-for-response) requires messageName |
| llama | infra | 1 | 9.1 | exclusive gateway()::exclusive gateway() timed out after 240 seconds |
| mistral | infra | 1 | 50.0 | timer boundary event()::timer boundary event() timed out after 240 seconds |
| mistral | deterministic | 1 | 50.0 | event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind |
| openai | deterministic | 2 | 50.0 | event-based gateway()::RECEIVE (act-await-response) requires messageName |
| openai | classification | 2 | 50.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |

## Stage breakdown

_Per-pipeline-stage model and token usage (readiness vs extraction)._

| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |
|---|---|---|---:|---:|---:|---:|
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 1130631 | 935094 | 429 | 170 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 1433468 | 305880 | 330 | 170 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 673911 | 487890 | 294 | 108 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 3845812 | 179578 | 242 | 108 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 1048623 | 771882 | 426 | 156 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 5155058 | 301354 | 308 | 156 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 966105 | 399063 | 432 | 168 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 5762932 | 204684 | 378 | 168 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 3043116 | 1556328 | 1308 | 153 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 5138716 | 301378 | 324 | 153 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 1051815 | 631557 | 474 | 171 |
| openai | ValidatedProcessContract | `gpt-4.1` | 5795920 | 244256 | 378 | 171 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 0 | 5.3 | 5 | 8 | 14 | 1.5 | 170 |
| deepseek | 5 | 6.8 | 5 | 14 | 20 | 3.3 | 108 |
| gemini | 0 | 5.6 | 5 | 8 | 20 | 2.2 | 156 |
| llama | 5 | 5.7 | 5 | 9 | 15 | 1.6 | 168 |
| mistral | 5 | 11.9 | 8 | 32 | 69 | 10.3 | 153 |
| openai | 5 | 6.0 | 5 | 10 | 23 | 2.5 | 171 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
