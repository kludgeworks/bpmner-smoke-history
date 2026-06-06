# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 2 | 100.0 | 0 | $0.6310 | 354840 |
| deepseek | `?` | 2 | 0.0 | 11 | n/a* | 0 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 2 | 100.0 | 0 | $0.3844 | 477444 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 2 | 90.0 | 1 | $0.2055 | 462534 |
| mistral | `mistral-small-2506,mistral-large-2411` | 2 | 100.0 | 0 | $0.5038 | 782179 |
| openai | `gpt-4.1-mini,gpt-4.1` | 2 | 100.0 | 0 | $0.4409 | 462729 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `embedded subprocess()` | 50.0 | 1 (deepseek) | 2 |
| `escalation boundary event()` | 50.0 | 1 (deepseek) | 2 |
| `event-based gateway()` | 50.0 | 1 (deepseek) | 2 |
| `exclusive gateway with default branch()` | 50.0 | 1 (deepseek) | 2 |
| `inclusive gateway()` | 50.0 | 1 (deepseek) | 2 |
| `intermediate escalation throw()` | 50.0 | 1 (deepseek) | 2 |
| `parallel gateway()` | 50.0 | 1 (llama) | 2 |
| `parallel multi-instance activity()` | 50.0 | 1 (deepseek) | 2 |
| `send task()` | 50.0 | 1 (deepseek) | 2 |
| `service task()` | 50.0 | 1 (deepseek) | 2 |
| `terminate end()` | 50.0 | 1 (deepseek) | 2 |
| `user task()` | 50.0 | 1 (deepseek) | 2 |
