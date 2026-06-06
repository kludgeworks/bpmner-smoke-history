# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 3 | 100.0 | 0 | $0.5750 | 478698 |
| deepseek | `?` | 3 | 0.0 | 16 | n/a* | 0 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 3 | 100.0 | 0 | $0.4680 | 886141 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 3 | 92.9 | 1 | $0.1846 | 624558 |
| mistral | `mistral-small-2506,mistral-large-2411` | 3 | 100.0 | 0 | $0.5957 | 1253913 |
| openai | `gpt-4.1-mini,gpt-4.1` | 3 | 100.0 | 0 | $0.4718 | 743020 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `parallel gateway()` | 66.7 | 2 (llama, deepseek) | 3 |
| `embedded subprocess()` | 33.3 | 1 (deepseek) | 3 |
| `error end()` | 33.3 | 1 (deepseek) | 3 |
| `escalation boundary event()` | 33.3 | 1 (deepseek) | 3 |
| `event subprocess()` | 33.3 | 1 (deepseek) | 3 |
| `event-based gateway()` | 33.3 | 1 (deepseek) | 3 |
| `exclusive gateway with default branch()` | 33.3 | 1 (deepseek) | 3 |
| `inclusive gateway()` | 33.3 | 1 (deepseek) | 3 |
| `intermediate escalation throw()` | 33.3 | 1 (deepseek) | 3 |
| `parallel multi-instance activity()` | 33.3 | 1 (deepseek) | 3 |
| `pools and lanes from distinct actors()` | 33.3 | 1 (deepseek) | 3 |
| `send task()` | 33.3 | 1 (deepseek) | 3 |
| `service task()` | 33.3 | 1 (deepseek) | 3 |
| `terminate end()` | 33.3 | 1 (deepseek) | 3 |
| `timer boundary event()` | 33.3 | 1 (deepseek) | 3 |
| `user task()` | 33.3 | 1 (deepseek) | 3 |
