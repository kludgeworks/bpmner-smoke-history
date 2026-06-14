# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 31 | 95.7 | 8 | n/a* | 4787531 |
| deepseek | `deepseek-chat` | 23 | 89.9 | 12 | $0.0465 | 6542974 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 31 | 89.3 | 18 | n/a* | 7845891 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 31 | 93.2 | 12 | $0.2333 | 8194241 |
| mistral | `mistral-large-2411,mistral-small-2506` | 31 | 98.8 | 2 | $0.4459 | 11229786 |
| openai | `gpt-4.1-mini,gpt-4.1` | 31 | 97.8 | 4 | $0.5350 | 8887828 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `error boundary event()` | 43.3 | 5 (anthropic, deepseek, gemini, llama, openai) | 30 |
| `escalation end()` | 20.0 | 3 (anthropic, deepseek, gemini) | 30 |
| `standard loop activity()` | 13.3 | 3 (anthropic, deepseek, gemini) | 30 |
| `exclusive gateway()` | 10.0 | 3 (anthropic, gemini, llama) | 30 |
| `event-based gateway()` | 16.7 | 2 (llama, openai) | 30 |
| `intermediate signal throw()` | 10.3 | 2 (gemini, llama) | 29 |
| `parallel gateway()` | 10.0 | 2 (gemini, llama) | 30 |
| `signal end()` | 6.9 | 2 (gemini, llama) | 29 |
| `event subprocess()` | 6.7 | 2 (gemini, mistral) | 30 |
| `script task()` | 6.7 | 2 (anthropic, gemini) | 30 |
| `timer boundary event()` | 6.7 | 2 (gemini, mistral) | 30 |
| `business rule task()` | 3.4 | 1 (gemini) | 29 |
| `data objects and stores()` | 3.4 | 1 (gemini) | 29 |
| `manual task()` | 3.4 | 1 (gemini) | 29 |
| `message start()` | 3.4 | 1 (gemini) | 29 |
| `sequential multi-instance activity()` | 3.4 | 1 (gemini) | 29 |
| `timer start()` | 3.4 | 1 (gemini) | 29 |
| `error end()` | 3.3 | 1 (gemini) | 30 |
| `intermediate escalation throw()` | 3.3 | 1 (deepseek) | 30 |
| `intermediate message throw()` | 3.3 | 1 (llama) | 30 |
| `pools and lanes from distinct actors()` | 3.3 | 1 (gemini) | 30 |
| `terminate end()` | 3.3 | 1 (openai) | 30 |

## Failure categories

_`deterministic` = harness/config failure (e.g. context load); `classification` = the model produced a wrong answer. Separates 'the harness broke' from 'the model struggled'._

| Provider | Category | Failures | % of provider fails | Sample signature |
|---|---|---:|---:|---|
| anthropic | deterministic | 5 | 62.5 | error boundary event()::400 - {"type":"error","error":{"type":"invalid_reques… |
| anthropic | classification | 3 | 37.5 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | classification | 10 | 83.3 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | deterministic | 2 | 16.7 | escalation end()::TIMER (boundaryEvent) requires detail |
| gemini | deterministic | 18 | 100.0 | business rule task()::429 - [{ |
| llama | classification | 9 | 75.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| llama | deterministic | 2 | 16.7 | event-based gateway()::RECEIVE (act-wait-for-response) requires messageName |
| llama | infra | 1 | 8.3 | exclusive gateway()::exclusive gateway() timed out after 240 seconds |
| mistral | deterministic | 1 | 50.0 | event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind |
| mistral | infra | 1 | 50.0 | timer boundary event()::timer boundary event() timed out after 240 seconds |
| openai | deterministic | 2 | 50.0 | event-based gateway()::RECEIVE (act-await-response) requires messageName |
| openai | classification | 2 | 50.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |

## Stage breakdown

_Per-pipeline-stage model and token usage (readiness vs extraction)._

| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |
|---|---|---|---:|---:|---:|---:|
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 1130631 | 935094 | 429 | 184 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 1557512 | 331530 | 358 | 184 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 673911 | 487890 | 294 | 119 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 4198356 | 195982 | 264 | 119 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 1048623 | 771882 | 426 | 169 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 5155058 | 301354 | 308 | 169 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 966105 | 399063 | 432 | 177 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 6070840 | 214636 | 398 | 177 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 3043116 | 1556328 | 1308 | 163 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 5491312 | 321710 | 346 | 163 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 1051815 | 631557 | 474 | 182 |
| openai | ValidatedProcessContract | `gpt-4.1` | 6228710 | 262394 | 406 | 182 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 0 | 5.2 | 5 | 8 | 14 | 1.5 | 184 |
| deepseek | 5 | 6.8 | 5 | 14 | 23 | 3.5 | 119 |
| gemini | 0 | 5.1 | 5 | 8 | 20 | 2.6 | 169 |
| llama | 5 | 5.7 | 5 | 9 | 15 | 1.6 | 177 |
| mistral | 5 | 11.6 | 8 | 32 | 69 | 10.1 | 163 |
| openai | 5 | 6.0 | 5 | 10 | 23 | 2.5 | 182 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
