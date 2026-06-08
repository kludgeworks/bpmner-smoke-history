# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 9 | 100.0 | 0 | $0.6014 | 1468014 |
| deepseek | `deepseek-chat` | 1 | 100.0 | 0 | $0.0389 | 237961 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 9 | 100.0 | 0 | $0.4450 | 2513796 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 9 | 89.6 | 5 | $0.2141 | 2180277 |
| mistral | `mistral-small-2506,mistral-large-2411` | 9 | 100.0 | 0 | $0.4683 | 3547794 |
| openai | `gpt-4.1-mini,gpt-4.1` | 9 | 100.0 | 0 | $0.4458 | 2154041 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `event-based gateway()` | 25.0 | 1 (llama) | 8 |
| `intermediate signal throw()` | 14.3 | 1 (llama) | 7 |
| `intermediate message throw()` | 12.5 | 1 (llama) | 8 |
| `parallel gateway()` | 12.5 | 1 (llama) | 8 |
