# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 8 | 100.0 | 0 | $0.6112 | 1328074 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 8 | 100.0 | 0 | $0.4200 | 2101657 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 8 | 90.9 | 4 | $0.2208 | 1999700 |
| mistral | `mistral-small-2506,mistral-large-2411` | 8 | 100.0 | 0 | $0.4623 | 2917925 |
| openai | `gpt-4.1-mini,gpt-4.1` | 8 | 100.0 | 0 | $0.4507 | 1932828 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `event-based gateway()` | 28.6 | 1 (llama) | 7 |
| `intermediate signal throw()` | 16.7 | 1 (llama) | 6 |
| `parallel gateway()` | 14.3 | 1 (llama) | 7 |
