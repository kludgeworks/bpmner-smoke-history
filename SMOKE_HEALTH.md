# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 22 | 94.5 | 7 | n/a* | 3359797 |
| deepseek | `deepseek-chat` | 14 | 86.1 | 10 | $0.0449 | 3880629 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 22 | 100.0 | 0 | $0.4333 | 6024403 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 22 | 92.2 | 10 | $0.2403 | 5990404 |
| mistral | `mistral-large-2411,mistral-small-2506` | 22 | 98.3 | 2 | $0.4407 | 8614532 |
| openai | `gpt-4.1-mini,gpt-4.1` | 22 | 97.6 | 3 | $0.5063 | 6013608 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `error boundary event()` | 38.1 | 3 (anthropic, deepseek, llama) | 21 |
| `event-based gateway()` | 23.8 | 2 (llama, openai) | 21 |
| `escalation end()` | 19.0 | 2 (anthropic, deepseek) | 21 |
| `standard loop activity()` | 14.3 | 2 (anthropic, deepseek) | 21 |
| `intermediate signal throw()` | 10.0 | 1 (llama) | 20 |
| `parallel gateway()` | 9.5 | 1 (llama) | 21 |
| `signal end()` | 5.0 | 1 (llama) | 20 |
| `event subprocess()` | 4.8 | 1 (mistral) | 21 |
| `exclusive gateway()` | 4.8 | 1 (anthropic) | 21 |
| `intermediate escalation throw()` | 4.8 | 1 (deepseek) | 21 |
| `intermediate message throw()` | 4.8 | 1 (llama) | 21 |
| `script task()` | 4.8 | 1 (anthropic) | 21 |
| `terminate end()` | 4.8 | 1 (openai) | 21 |
| `timer boundary event()` | 4.8 | 1 (mistral) | 21 |

## Failure categories

_`deterministic` = harness/config failure (e.g. context load); `classification` = the model produced a wrong answer. Separates 'the harness broke' from 'the model struggled'._

| Provider | Category | Failures | % of provider fails | Sample signature |
|---|---|---:|---:|---|
| anthropic | deterministic | 5 | 71.4 | error boundary event()::400 - {"type":"error","error":{"type":"invalid_reques… |
| anthropic | classification | 2 | 28.6 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | classification | 8 | 80.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | deterministic | 2 | 20.0 | escalation end()::TIMER (boundaryEvent) requires detail |
| llama | classification | 8 | 80.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| llama | deterministic | 2 | 20.0 | event-based gateway()::RECEIVE (act-wait-for-response) requires messageName |
| mistral | infra | 1 | 50.0 | timer boundary event()::timer boundary event() timed out after 240 seconds |
| mistral | deterministic | 1 | 50.0 | event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind |
| openai | deterministic | 2 | 66.7 | event-based gateway()::RECEIVE (act-await-response) requires messageName |
| openai | classification | 1 | 33.3 | terminate end()::Expected end state of type Terminate in contract, but found:… |

## Stage breakdown

_Per-pipeline-stage model and token usage (readiness vs extraction)._

| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |
|---|---|---|---:|---:|---:|---:|
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 1130631 | 935094 | 429 | 128 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 1062524 | 231548 | 246 | 128 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 673911 | 487890 | 294 | 72 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 2597138 | 121690 | 164 | 72 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 1048623 | 771882 | 426 | 117 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 3971472 | 232426 | 238 | 117 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 966105 | 399063 | 432 | 129 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 4467394 | 157842 | 294 | 129 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 3043116 | 1556328 | 1308 | 115 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 3791740 | 223348 | 240 | 115 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 1051815 | 631557 | 474 | 127 |
| openai | ValidatedProcessContract | `gpt-4.1` | 4155626 | 174610 | 272 | 127 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 0 | 5.3 | 5 | 8 | 14 | 1.7 | 128 |
| deepseek | 5 | 6.4 | 5 | 11 | 18 | 2.7 | 72 |
| gemini | 5 | 5.7 | 5 | 8 | 20 | 2.1 | 117 |
| llama | 5 | 5.6 | 5 | 8 | 15 | 1.5 | 129 |
| mistral | 5 | 13.5 | 11 | 38 | 69 | 11.3 | 115 |
| openai | 5 | 5.9 | 5 | 9 | 23 | 2.4 | 127 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
