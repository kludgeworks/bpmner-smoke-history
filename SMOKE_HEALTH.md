# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 33 | 95.9 | 8 | n/a* | 5033385 |
| deepseek | `deepseek-chat` | 25 | 90.8 | 12 | $0.0472 | 7256174 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 33 | 83.0 | 31 | n/a* | 7845891 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 33 | 93.0 | 13 | $0.2292 | 8567611 |
| mistral | `mistral-large-2411,mistral-small-2506` | 33 | 98.9 | 2 | $0.4559 | 11941897 |
| openai | `gpt-4.1-mini,gpt-4.1` | 33 | 97.4 | 5 | $0.5295 | 9365545 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `error boundary event()` | 46.9 | 5 (anthropic, deepseek, gemini, llama, openai) | 32 |
| `escalation end()` | 21.9 | 3 (anthropic, deepseek, gemini) | 32 |
| `standard loop activity()` | 15.6 | 3 (anthropic, deepseek, gemini) | 32 |
| `exclusive gateway()` | 12.5 | 3 (anthropic, gemini, llama) | 32 |
| `event-based gateway()` | 15.6 | 2 (llama, openai) | 32 |
| `intermediate signal throw()` | 12.9 | 2 (gemini, llama) | 31 |
| `parallel gateway()` | 12.5 | 2 (gemini, llama) | 32 |
| `signal end()` | 9.7 | 2 (gemini, llama) | 31 |
| `script task()` | 9.4 | 2 (anthropic, gemini) | 32 |
| `event subprocess()` | 6.3 | 2 (gemini, mistral) | 32 |
| `timer boundary event()` | 6.3 | 2 (gemini, mistral) | 32 |
| `business rule task()` | 6.5 | 1 (gemini) | 31 |
| `data objects and stores()` | 6.5 | 1 (gemini) | 31 |
| `manual task()` | 6.5 | 1 (gemini) | 31 |
| `message start()` | 6.5 | 1 (gemini) | 31 |
| `sequential multi-instance activity()` | 6.5 | 1 (gemini) | 31 |
| `timer start()` | 6.5 | 1 (gemini) | 31 |
| `error end()` | 3.1 | 1 (gemini) | 32 |
| `intermediate escalation throw()` | 3.1 | 1 (deepseek) | 32 |
| `intermediate message throw()` | 3.1 | 1 (llama) | 32 |
| `pools and lanes from distinct actors()` | 3.1 | 1 (gemini) | 32 |
| `terminate end()` | 3.1 | 1 (openai) | 32 |

## Failure categories

_`deterministic` = harness/config failure (e.g. context load); `classification` = the model produced a wrong answer. Separates 'the harness broke' from 'the model struggled'._

| Provider | Category | Failures | % of provider fails | Sample signature |
|---|---|---:|---:|---|
| anthropic | deterministic | 5 | 62.5 | error boundary event()::400 - {"type":"error","error":{"type":"invalid_reques… |
| anthropic | classification | 3 | 37.5 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | classification | 10 | 83.3 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| deepseek | deterministic | 2 | 16.7 | escalation end()::TIMER (boundaryEvent) requires detail |
| gemini | deterministic | 31 | 100.0 | business rule task()::429 - [{ |
| llama | classification | 10 | 76.9 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| llama | deterministic | 2 | 15.4 | event-based gateway()::RECEIVE (act-wait-for-response) requires messageName |
| llama | infra | 1 | 7.7 | exclusive gateway()::exclusive gateway() timed out after 240 seconds |
| mistral | infra | 1 | 50.0 | timer boundary event()::timer boundary event() timed out after 240 seconds |
| mistral | deterministic | 1 | 50.0 | event subprocess()::EVENT_GATEWAY (br-no-cancel) requires triggerKind |
| openai | classification | 3 | 60.0 | error boundary event()::Expected an activity carrying a ERROR boundary event,… |
| openai | deterministic | 2 | 40.0 | event-based gateway()::RECEIVE (act-await-response) requires messageName |

## Stage breakdown

_Per-pipeline-stage model and token usage (readiness vs extraction)._

| Provider | Stage | Model | Prompt tokens | Completion tokens | LLM calls | Samples |
|---|---|---|---:|---:|---:|---:|
| anthropic | ProcessInputAssessment | `claude-haiku-4-5` | 1130631 | 935094 | 429 | 194 |
| anthropic | ValidatedProcessContract | `claude-sonnet-4-6` | 1646116 | 347912 | 378 | 194 |
| deepseek | ProcessInputAssessment | `deepseek-chat` | 673911 | 487890 | 294 | 130 |
| deepseek | ValidatedProcessContract | `deepseek-chat` | 4740986 | 217008 | 298 | 130 |
| gemini | ProcessInputAssessment | `gemini-2.5-flash` | 1048623 | 771882 | 426 | 182 |
| gemini | ValidatedProcessContract | `gemini-2.5-pro` | 5155058 | 301354 | 308 | 182 |
| llama | ProcessInputAssessment | `meta-llama/llama-3.3-70b-instruct` | 966105 | 399063 | 432 | 186 |
| llama | ValidatedProcessContract | `meta-llama/llama-3.3-70b-instruct` | 6348596 | 224714 | 416 | 186 |
| mistral | ProcessInputAssessment | `mistral-small-2506` | 3043116 | 1556328 | 1308 | 177 |
| mistral | ValidatedProcessContract | `mistral-large-2411` | 6003966 | 350038 | 378 | 177 |
| openai | ProcessInputAssessment | `gpt-4.1-mini` | 1051815 | 631557 | 474 | 193 |
| openai | ValidatedProcessContract | `gpt-4.1` | 6570362 | 275366 | 428 | 193 |

## LLM efficiency

_Distribution of LLM API calls per test — more calls may indicate retries or tool loops._

| Provider | Min | Avg | Median | P95 | Max | σ | Samples |
|---|---:|---:|---:|---:|---:|---:|---:|
| anthropic | 0 | 5.2 | 5 | 8 | 14 | 1.4 | 194 |
| deepseek | 5 | 6.8 | 5 | 14 | 23 | 3.5 | 130 |
| gemini | 0 | 4.8 | 5 | 8 | 20 | 2.8 | 182 |
| llama | 5 | 5.6 | 5 | 8 | 15 | 1.5 | 186 |
| mistral | 5 | 11.1 | 8 | 32 | 69 | 9.8 | 177 |
| openai | 5 | 5.9 | 5 | 10 | 23 | 2.4 | 193 |

## Latency

_Average LLM response time per provider over runs (seconds, wall-clock)._

![Avg LLM latency by provider over runs](assets/smoke-health/latency-trend.svg)

## Cost trends

_Cost **per test** — shard sizes vary run-to-run, so raw per-run totals aren't comparable._

![Cost per test by provider over runs](assets/smoke-health/cost-trend.svg)

## Token split (readiness vs extraction)

_Tokens spent in the cheap readiness gatekeeper vs the expensive extraction stage, per provider._

![Token split by provider](assets/smoke-health/token-split.svg)
