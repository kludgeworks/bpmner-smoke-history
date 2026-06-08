# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 10 | 98.2 | 1 | $0.5901 | 1603435 |
| deepseek | `deepseek-chat` | 2 | 100.0 | 0 | $0.0349 | 428109 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 10 | 100.0 | 0 | $0.4492 | 2816997 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 10 | 90.6 | 5 | $0.2107 | 2384390 |
| mistral | `mistral-small-2506,mistral-large-2411` | 10 | 100.0 | 0 | $0.4623 | 3904389 |
| openai | `gpt-4.1-mini,gpt-4.1` | 10 | 100.0 | 0 | $0.4664 | 2520196 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `event-based gateway()` | 22.2 | 1 (llama) | 9 |
| `intermediate signal throw()` | 12.5 | 1 (llama) | 8 |
| `error boundary event()` | 11.1 | 1 (anthropic) | 9 |
| `intermediate message throw()` | 11.1 | 1 (llama) | 9 |
| `parallel gateway()` | 11.1 | 1 (llama) | 9 |
