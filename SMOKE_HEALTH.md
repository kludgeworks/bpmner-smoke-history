# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 6 | 100.0 | 0 | $0.6398 | 1048085 |
| deepseek | `?` | 6 | 0.0 | 34 | n/a* | 0 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 6 | 100.0 | 0 | $0.4154 | 1568213 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 6 | 90.9 | 3 | $0.2206 | 1500116 |
| mistral | `mistral-small-2506,mistral-large-2411` | 6 | 100.0 | 0 | $0.4769 | 2046109 |
| openai | `gpt-4.1-mini,gpt-4.1` | 6 | 100.0 | 0 | $0.4374 | 1392986 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `event-based gateway()` | 33.3 | 2 (deepseek, llama) | 6 |
| `intermediate signal throw()` | 33.3 | 2 (llama, deepseek) | 6 |
| `parallel gateway()` | 33.3 | 2 (llama, deepseek) | 6 |
| `embedded subprocess()` | 33.3 | 1 (deepseek) | 6 |
| `escalation boundary event()` | 33.3 | 1 (deepseek) | 6 |
| `exclusive gateway with default branch()` | 33.3 | 1 (deepseek) | 6 |
| `parallel multi-instance activity()` | 33.3 | 1 (deepseek) | 6 |
| `send task()` | 33.3 | 1 (deepseek) | 6 |
| `business rule task()` | 16.7 | 1 (deepseek) | 6 |
| `data objects and stores()` | 16.7 | 1 (deepseek) | 6 |
| `error boundary event()` | 16.7 | 1 (deepseek) | 6 |
| `error end()` | 16.7 | 1 (deepseek) | 6 |
| `escalation end()` | 16.7 | 1 (deepseek) | 6 |
| `event subprocess()` | 16.7 | 1 (deepseek) | 6 |
| `exclusive gateway()` | 16.7 | 1 (deepseek) | 6 |
| `inclusive gateway()` | 16.7 | 1 (deepseek) | 6 |
| `intermediate escalation throw()` | 16.7 | 1 (deepseek) | 6 |
| `manual task()` | 16.7 | 1 (deepseek) | 6 |
| `message start()` | 16.7 | 1 (deepseek) | 6 |
| `pools and lanes from distinct actors()` | 16.7 | 1 (deepseek) | 6 |
| `script task()` | 16.7 | 1 (deepseek) | 6 |
| `sequential multi-instance activity()` | 16.7 | 1 (deepseek) | 6 |
| `service task()` | 16.7 | 1 (deepseek) | 6 |
| `signal end()` | 16.7 | 1 (deepseek) | 6 |
| `standard loop activity()` | 16.7 | 1 (deepseek) | 6 |

_…and 4 more flaky tests._
