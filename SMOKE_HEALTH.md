# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 4 | 100.0 | 0 | $0.6579 | 724898 |
| deepseek | `?` | 4 | 0.0 | 21 | n/a* | 0 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 4 | 100.0 | 0 | $0.4477 | 1124482 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 4 | 94.7 | 1 | $0.1958 | 886889 |
| mistral | `mistral-small-2506,mistral-large-2411` | 4 | 100.0 | 0 | $0.5220 | 1481837 |
| openai | `gpt-4.1-mini,gpt-4.1` | 4 | 100.0 | 0 | $0.4718 | 992409 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `parallel gateway()` | 50.0 | 2 (llama, deepseek) | 4 |
| `embedded subprocess()` | 50.0 | 1 (deepseek) | 4 |
| `escalation boundary event()` | 50.0 | 1 (deepseek) | 4 |
| `exclusive gateway with default branch()` | 50.0 | 1 (deepseek) | 4 |
| `parallel multi-instance activity()` | 50.0 | 1 (deepseek) | 4 |
| `send task()` | 50.0 | 1 (deepseek) | 4 |
| `error end()` | 25.0 | 1 (deepseek) | 4 |
| `event subprocess()` | 25.0 | 1 (deepseek) | 4 |
| `event-based gateway()` | 25.0 | 1 (deepseek) | 4 |
| `inclusive gateway()` | 25.0 | 1 (deepseek) | 4 |
| `intermediate escalation throw()` | 25.0 | 1 (deepseek) | 4 |
| `pools and lanes from distinct actors()` | 25.0 | 1 (deepseek) | 4 |
| `service task()` | 25.0 | 1 (deepseek) | 4 |
| `terminate end()` | 25.0 | 1 (deepseek) | 4 |
| `timer boundary event()` | 25.0 | 1 (deepseek) | 4 |
| `user task()` | 25.0 | 1 (deepseek) | 4 |
