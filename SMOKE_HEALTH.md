# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 8 | 100.0 | 0 | $0.6112 | 1328074 |
| deepseek | `?` | 8 | 0.0 | 46 | n/a* | 0 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 8 | 100.0 | 0 | $0.4200 | 2101657 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 8 | 90.9 | 4 | $0.2208 | 1999700 |
| mistral | `mistral-small-2506,mistral-large-2411` | 8 | 100.0 | 0 | $0.4623 | 2917925 |
| openai | `gpt-4.1-mini,gpt-4.1` | 8 | 100.0 | 0 | $0.4507 | 1932828 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `event-based gateway()` | 37.5 | 2 (deepseek, llama) | 8 |
| `intermediate signal throw()` | 37.5 | 2 (llama, deepseek) | 8 |
| `parallel gateway()` | 25.0 | 2 (llama, deepseek) | 8 |
| `business rule task()` | 25.0 | 1 (deepseek) | 8 |
| `data objects and stores()` | 25.0 | 1 (deepseek) | 8 |
| `embedded subprocess()` | 25.0 | 1 (deepseek) | 8 |
| `escalation boundary event()` | 25.0 | 1 (deepseek) | 8 |
| `exclusive gateway with default branch()` | 25.0 | 1 (deepseek) | 8 |
| `manual task()` | 25.0 | 1 (deepseek) | 8 |
| `message start()` | 25.0 | 1 (deepseek) | 8 |
| `parallel multi-instance activity()` | 25.0 | 1 (deepseek) | 8 |
| `send task()` | 25.0 | 1 (deepseek) | 8 |
| `sequential multi-instance activity()` | 25.0 | 1 (deepseek) | 8 |
| `signal end()` | 25.0 | 1 (deepseek) | 8 |
| `timer start()` | 25.0 | 1 (deepseek) | 8 |
| `error boundary event()` | 12.5 | 1 (deepseek) | 8 |
| `error end()` | 12.5 | 1 (deepseek) | 8 |
| `escalation end()` | 12.5 | 1 (deepseek) | 8 |
| `event subprocess()` | 12.5 | 1 (deepseek) | 8 |
| `exclusive gateway()` | 12.5 | 1 (deepseek) | 8 |
| `inclusive gateway()` | 12.5 | 1 (deepseek) | 8 |
| `intermediate escalation throw()` | 12.5 | 1 (deepseek) | 8 |
| `intermediate message throw()` | 12.5 | 1 (deepseek) | 8 |
| `message end()` | 12.5 | 1 (deepseek) | 8 |
| `pools and lanes from distinct actors()` | 12.5 | 1 (deepseek) | 8 |

_…and 8 more flaky tests._
