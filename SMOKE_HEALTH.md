# 🔬 Smoke Health

_Report-only · all recorded runs · provider = model family under test._

## Provider scorecard

| Provider | Model | Runs | Pass % | Fails | $/run | Tokens |
|---|---|---:|---:|---:|---:|---:|
| anthropic | `claude-haiku-4-5,claude-sonnet-4-6` | 12 | 98.6 | 1 | $0.6037 | 1962106 |
| deepseek | `deepseek-chat` | 4 | 89.5 | 2 | $0.0367 | 900800 |
| gemini | `gemini-2.5-flash,gemini-2.5-pro` | 12 | 100.0 | 0 | $0.4315 | 3246607 |
| llama | `meta-llama/llama-3.3-70b-instruct` | 12 | 90.9 | 6 | $0.2201 | 2986076 |
| mistral | `mistral-small-2506,mistral-large-2411` | 12 | 100.0 | 0 | $0.4496 | 4843566 |
| openai | `gpt-4.1-mini,gpt-4.1` | 12 | 98.5 | 1 | $0.4871 | 3141770 |

_\* cost unknown — provider has no configured pricing._

## Flaky tests (fail across providers ⇒ test/prompt suspect; one provider ⇒ model limit)

| Test | Fail % | Providers failed | Samples |
|---|---:|---|---:|
| `event-based gateway()` | 27.3 | 2 (llama, openai) | 11 |
| `error boundary event()` | 18.2 | 2 (anthropic, deepseek) | 11 |
| `intermediate signal throw()` | 10.0 | 1 (llama) | 10 |
| `signal end()` | 10.0 | 1 (llama) | 10 |
| `intermediate message throw()` | 9.1 | 1 (llama) | 11 |
| `parallel gateway()` | 9.1 | 1 (llama) | 11 |
| `standard loop activity()` | 9.1 | 1 (deepseek) | 11 |
