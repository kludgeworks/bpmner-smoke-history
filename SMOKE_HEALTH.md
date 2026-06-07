# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 5 | 100.0 | 0 | $0.6418 | 876021 |
| deepseek | `?` | 5 | 0.0 | 26 | n/a* | 0 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 5 | 100.0 | 0 | $0.4165 | 1315223 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 5 | 92.6 | 2 | $0.2228 | 1260916 |
| mistral | `mistral-small-2506,mistral-large-2411` | 5 | 100.0 | 0 | $0.4959 | 1780097 |
| openai | `gpt-4.1-mini,gpt-4.1` | 5 | 100.0 | 0 | $0.4600 | 1213527 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `parallel gateway()` | 40.0 | 2 (deepseek, llama) | 5 |
| `embedded subprocess()` | 40.0 | 1 (deepseek) | 5 |
| `escalation boundary event()` | 40.0 | 1 (deepseek) | 5 |
| `exclusive gateway with default branch()` | 40.0 | 1 (deepseek) | 5 |
| `parallel multi-instance activity()` | 40.0 | 1 (deepseek) | 5 |
| `send task()` | 40.0 | 1 (deepseek) | 5 |
| `error boundary event()` | 20.0 | 1 (deepseek) | 5 |
| `error end()` | 20.0 | 1 (deepseek) | 5 |
| `escalation end()` | 20.0 | 1 (deepseek) | 5 |
| `event subprocess()` | 20.0 | 1 (deepseek) | 5 |
| `event-based gateway()` | 20.0 | 1 (deepseek) | 5 |
| `exclusive gateway()` | 20.0 | 1 (deepseek) | 5 |
| `inclusive gateway()` | 20.0 | 1 (deepseek) | 5 |
| `intermediate escalation throw()` | 20.0 | 1 (deepseek) | 5 |
| `intermediate signal throw()` | 20.0 | 1 (llama) | 5 |
| `pools and lanes from distinct actors()` | 20.0 | 1 (deepseek) | 5 |
| `script task()` | 20.0 | 1 (deepseek) | 5 |
| `service task()` | 20.0 | 1 (deepseek) | 5 |
| `standard loop activity()` | 20.0 | 1 (deepseek) | 5 |
| `terminate end()` | 20.0 | 1 (deepseek) | 5 |
| `timer boundary event()` | 20.0 | 1 (deepseek) | 5 |
| `user task()` | 20.0 | 1 (deepseek) | 5 |
