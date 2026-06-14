# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 32 | 95.7 | 8 | n/a* | 4885409 |
| deepseek | `deepseek-chat` | 24 | 90.4 | 12 | $0.0475 | 7006422 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 32 | 86.8 | 23 | n/a* | 7845891 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 32 | 92.9 | 13 | $0.2320 | 8406617 |
| mistral | `mistral-large-2411,mistral-small-2506` | 32 | 98.8 | 2 | $0.4557 | 11653630 |
| openai | `gpt-4.1-mini,gpt-4.1` | 32 | 97.9 | 4 | $0.5333 | 9144408 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `error boundary event()` | 45.2 | 5 (anthropic, deepseek, gemini, llama, openai) | 31 |
| `escalation end()` | 22.6 | 3 (anthropic, deepseek, gemini) | 31 |
| `standard loop activity()` | 16.1 | 3 (anthropic, deepseek, gemini) | 31 |
| `exclusive gateway()` | 12.9 | 3 (anthropic, gemini, llama) | 31 |
| `event-based gateway()` | 16.1 | 2 (llama, openai) | 31 |
| `parallel gateway()` | 12.9 | 2 (gemini, llama) | 31 |
| `intermediate signal throw()` | 10.0 | 2 (gemini, llama) | 30 |
| `script task()` | 9.7 | 2 (anthropic, gemini) | 31 |
| `signal end()` | 6.7 | 2 (gemini, llama) | 30 |
| `event subprocess()` | 6.5 | 2 (gemini, mistral) | 31 |
| `timer boundary event()` | 6.5 | 2 (gemini, mistral) | 31 |
| `business rule task()` | 3.3 | 1 (gemini) | 30 |
| `data objects and stores()` | 3.3 | 1 (gemini) | 30 |
| `manual task()` | 3.3 | 1 (gemini) | 30 |
| `message start()` | 3.3 | 1 (gemini) | 30 |
| `sequential multi-instance activity()` | 3.3 | 1 (gemini) | 30 |
| `timer start()` | 3.3 | 1 (gemini) | 30 |
| `error end()` | 3.2 | 1 (gemini) | 31 |
| `intermediate escalation throw()` | 3.2 | 1 (deepseek) | 31 |
| `intermediate message throw()` | 3.2 | 1 (llama) | 31 |
| `pools and lanes from distinct actors()` | 3.2 | 1 (gemini) | 31 |
| `terminate end()` | 3.2 | 1 (openai) | 31 |

## Failure categories

_`deterministic` = harness/config failure (e.g. context load); `classification` = the model produced a wrong answer. Separates 'the harness broke' from 'the model struggled'._

| Provider | Category | Failures | % of provider fails | Sample signature |
|---|---|---:|---:|---|
| anthropic | deterministic | 5 | 62.5 | error boundary event()::400 - {"type":"error","error":{"type":"invalid_reques… |
| anthropic | classification | 3 | 37.5 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | classification | 10 | 83.3 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | deterministic | 2 | 16.7 | escalation end()::TIMER (boundaryEvent) requires detail |
| gemini | deterministic | 23 | 100.0 | business rule task()::429 - [{ |
| llama | classification | 10 | 76.9 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| llama | deterministic | 2 | 15.4 | event-based gateway()::RECEIVE (act-wait-for-response) requires messageName |
| llama | infra | 1 | 7.7 | exclusive gateway()::exclusive gateway() timed out after 240 seconds |
| mistral | deterministic | 1 | 50.0 | event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind |
| mistral | infra | 1 | 50.0 | timer boundary event()::timer boundary event() timed out after 240 seconds |
| openai | classification | 2 | 50.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| openai | deterministic | 2 | 50.0 | event-based gateway()::RECEIVE (act-await-response) requires messageName |

## Stage breakdown

_Per-pipeline-stage model and token usage (readiness vs extraction)._

| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |
|---|---|---|---:|---:|---:|---:|
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 1130631 | 935094 | 429 | 188 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 1592878 | 337234 | 366 | 188 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 673911 | 487890 | 294 | 125 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 4580866 | 208352 | 288 | 125 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 1048623 | 771882 | 426 | 174 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 5155058 | 301354 | 308 | 174 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 966105 | 399063 | 432 | 182 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 6225218 | 221100 | 408 | 182 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 3043116 | 1556328 | 1308 | 171 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 5811630 | 339364 | 366 | 171 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 1051815 | 631557 | 474 | 188 |
| openai | ValidatedProcessContract | `gpt-4.1` | 6415024 | 269354 | 418 | 188 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 0 | 5.2 | 5 | 8 | 14 | 1.5 | 188 |
| deepseek | 5 | 6.8 | 5 | 14 | 23 | 3.5 | 125 |
| gemini | 0 | 5.0 | 5 | 8 | 20 | 2.7 | 174 |
| llama | 5 | 5.7 | 5 | 8 | 15 | 1.6 | 182 |
| mistral | 5 | 11.3 | 8 | 32 | 69 | 9.9 | 171 |
| openai | 5 | 5.9 | 5 | 10 | 23 | 2.5 | 188 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
