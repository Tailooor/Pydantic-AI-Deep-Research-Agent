## Deep Research Agent

This project gives you a small deep research app with:

- Pydantic AI for research planning and report writing
- OpenRouter as the model provider
- `openrouter/free` as the default model
- DuckDuckGo for web research
- Gradio as the frontend
- Structured research plans and detailed reports

I used the OpenRouter setup pattern described in `llms-full.md`, including the `OpenRouterModel(...)` approach and `OPENROUTER_API_KEY` environment variable.

## Project Files

- `main.py` starts the app
- `app/config.py` loads `.env` settings
- `app/agent.py` creates the Pydantic AI planner and writer agents
- `app/duckduckgo.py` runs DuckDuckGo web searches
- `app/research.py` orchestrates multi-step research
- `app/schemas.py` defines structured outputs
- `app/ui.py` creates the Gradio research UI
- `.env` stores your local settings

## 1. Add Your API Key

Open `.env` and set your real OpenRouter key:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=openrouter/free
APP_HOST=127.0.0.1
APP_PORT=7860
APP_TITLE=Deep Research Agent
DISCOVERY_RESULT_COUNT=5
ANGLE_RESULT_COUNT=4
```

## 2. Install Dependencies

If you want to use `uv`:

```bash
uv sync
```

If you want to use `pip` in a virtual environment:

```bash
pip install -e .
```

## 3. Start The App

With `uv`:

```bash
uv run python main.py
```

Or with your virtual environment:

```bash
python main.py
```

## 4. Open The UI

Open this in your browser:

```text
http://127.0.0.1:7860
```

## What The Agent Does

1. It detects whether your input is likely a stock ticker or a general research query.
2. It runs one DuckDuckGo discovery search.
3. It uses those results to generate 3 to 4 non-overlapping research angles.
4. It runs more DuckDuckGo searches for each angle.
5. It writes a structured report with:

- executive summary
- subject profile
- angle-by-angle findings
- opportunities
- risks
- final take
- source list

## Example Inputs

- `NVDA`
- `MSFT`
- `AI infrastructure demand outlook`
- `Open-source coding agents competitive landscape`

## Notes

- `openrouter/free` is the default model router for free inference on OpenRouter
- If you want a different model later, change `OPENROUTER_MODEL` in `.env`
- `.env` is ignored by git so your key stays local
