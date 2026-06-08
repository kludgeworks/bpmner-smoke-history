# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 7 | 100.0 | 0 | $0.6199 | 1184450 |
| deepseek | `?` | 7 | 0.0 | 38 | n/a* | 0 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 7 | 100.0 | 0 | $0.4225 | 1857428 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 7 | 92.1 | 3 | $0.2162 | 1713876 |
| mistral | `mistral-small-2506,mistral-large-2411` | 7 | 100.0 | 0 | $0.4685 | 2415283 |
| openai | `gpt-4.1-mini,gpt-4.1` | 7 | 100.0 | 0 | $0.4675 | 1743901 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `event-based gateway()` | 28.6 | 2 (deepseek, llama) | 7 |
| `intermediate signal throw()` | 28.6 | 2 (llama, deepseek) | 7 |
| `parallel gateway()` | 28.6 | 2 (llama, deepseek) | 7 |
| `embedded subprocess()` | 28.6 | 1 (deepseek) | 7 |
| `escalation boundary event()` | 28.6 | 1 (deepseek) | 7 |
| `exclusive gateway with default branch()` | 28.6 | 1 (deepseek) | 7 |
| `parallel multi-instance activity()` | 28.6 | 1 (deepseek) | 7 |
| `send task()` | 28.6 | 1 (deepseek) | 7 |
| `business rule task()` | 14.3 | 1 (deepseek) | 7 |
| `data objects and stores()` | 14.3 | 1 (deepseek) | 7 |
| `error boundary event()` | 14.3 | 1 (deepseek) | 7 |
| `error end()` | 14.3 | 1 (deepseek) | 7 |
| `escalation end()` | 14.3 | 1 (deepseek) | 7 |
| `event subprocess()` | 14.3 | 1 (deepseek) | 7 |
| `exclusive gateway()` | 14.3 | 1 (deepseek) | 7 |
| `inclusive gateway()` | 14.3 | 1 (deepseek) | 7 |
| `intermediate escalation throw()` | 14.3 | 1 (deepseek) | 7 |
| `intermediate message throw()` | 14.3 | 1 (deepseek) | 7 |
| `manual task()` | 14.3 | 1 (deepseek) | 7 |
| `message end()` | 14.3 | 1 (deepseek) | 7 |
| `message start()` | 14.3 | 1 (deepseek) | 7 |
| `pools and lanes from distinct actors()` | 14.3 | 1 (deepseek) | 7 |
| `receive task()` | 14.3 | 1 (deepseek) | 7 |
| `script task()` | 14.3 | 1 (deepseek) | 7 |
| `sequential multi-instance activity()` | 14.3 | 1 (deepseek) | 7 |

_…and 8 more flaky tests._
