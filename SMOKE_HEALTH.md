# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 24 | 94.2 | 8 | n/a* | 3657283 |
| deepseek | `deepseek-chat` | 16 | 87.7 | 10 | $0.0444 | 4371571 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 24 | 100.0 | 0 | $0.4465 | 6785504 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 24 | 92.8 | 10 | $0.2367 | 6437332 |
| mistral | `mistral-large-2411,mistral-small-2506` | 24 | 98.4 | 2 | $0.4492 | 9258193 |
| openai | `gpt-4.1-mini,gpt-4.1` | 24 | 97.1 | 4 | $0.5117 | 6630312 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `error boundary event()` | 43.5 | 4 (anthropic, deepseek, llama, openai) | 23 |
| `event-based gateway()` | 21.7 | 2 (llama, openai) | 23 |
| `escalation end()` | 17.4 | 2 (anthropic, deepseek) | 23 |
| `standard loop activity()` | 13.0 | 2 (anthropic, deepseek) | 23 |
| `intermediate signal throw()` | 9.1 | 1 (llama) | 22 |
| `parallel gateway()` | 8.7 | 1 (llama) | 23 |
| `signal end()` | 4.5 | 1 (llama) | 22 |
| `event subprocess()` | 4.3 | 1 (mistral) | 23 |
| `exclusive gateway()` | 4.3 | 1 (anthropic) | 23 |
| `intermediate escalation throw()` | 4.3 | 1 (deepseek) | 23 |
| `intermediate message throw()` | 4.3 | 1 (llama) | 23 |
| `script task()` | 4.3 | 1 (anthropic) | 23 |
| `terminate end()` | 4.3 | 1 (openai) | 23 |
| `timer boundary event()` | 4.3 | 1 (mistral) | 23 |

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
| openai | classification | 2 | 50.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| openai | deterministic | 2 | 50.0 | event-based gateway()::RECEIVE (act-await-response) requires messageName |

## Stage breakdown

_Per-pipeline-stage model and token usage (readiness vs extraction)._

| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |
|---|---|---|---:|---:|---:|---:|
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 1130631 | 935094 | 429 | 139 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 1159780 | 252030 | 268 | 139 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 673911 | 487890 | 294 | 81 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 2885594 | 135236 | 182 | 81 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 1048623 | 771882 | 426 | 131 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 4477954 | 259966 | 268 | 131 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 966105 | 399063 | 432 | 139 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 4776012 | 167920 | 314 | 139 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 3043116 | 1556328 | 1308 | 126 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 4240144 | 250122 | 268 | 126 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 1051815 | 631557 | 474 | 140 |
| openai | ValidatedProcessContract | `gpt-4.1` | 4589430 | 191814 | 300 | 140 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 0 | 5.3 | 5 | 8 | 14 | 1.7 | 139 |
| deepseek | 5 | 6.5 | 5 | 11 | 20 | 3.0 | 81 |
| gemini | 5 | 5.7 | 5 | 8 | 20 | 2.0 | 131 |
| llama | 5 | 5.7 | 5 | 8 | 15 | 1.6 | 139 |
| mistral | 5 | 12.9 | 8 | 36 | 69 | 11.0 | 126 |
| openai | 5 | 5.9 | 5 | 10 | 23 | 2.3 | 140 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
