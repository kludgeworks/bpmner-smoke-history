# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 1 | 100.0 | 0 | $0.8790 | 243760 |
| deepseek | `?` | 1 | 0.0 | 5 | n/a* | 0 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 1 | 100.0 | 0 | $0.3955 | 241439 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 1 | 100.0 | 0 | $0.2216 | 250914 |
| mistral | `mistral-small-2506,mistral-large-2411` | 1 | 100.0 | 0 | $0.3198 | 270293 |
| openai | `gpt-4.1-mini,gpt-4.1` | 1 | 100.0 | 0 | $0.4822 | 253104 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `embedded subprocess()` | 100.0 | 1 (deepseek) | 1 |
| `escalation boundary event()` | 100.0 | 1 (deepseek) | 1 |
| `exclusive gateway with default branch()` | 100.0 | 1 (deepseek) | 1 |
| `parallel multi-instance activity()` | 100.0 | 1 (deepseek) | 1 |
| `send task()` | 100.0 | 1 (deepseek) | 1 |
