# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 11 | 98.4 | 1 | $0.6035 | 1799573 |
| deepseek | `deepseek-chat` | 3 | 100.0 | 0 | $0.0355 | 654504 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 11 | 100.0 | 0 | $0.4446 | 3058456 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 11 | 91.4 | 5 | $0.2098 | 2609361 |
| mistral | `mistral-small-2506,mistral-large-2411` | 11 | 100.0 | 0 | $0.4516 | 4315348 |
| openai | `gpt-4.1-mini,gpt-4.1` | 11 | 98.4 | 1 | $0.4930 | 2907483 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `event-based gateway()` | 30.0 | 2 (openai, llama) | 10 |
| `intermediate signal throw()` | 11.1 | 1 (llama) | 9 |
| `error boundary event()` | 10.0 | 1 (anthropic) | 10 |
| `intermediate message throw()` | 10.0 | 1 (llama) | 10 |
| `parallel gateway()` | 10.0 | 1 (llama) | 10 |
