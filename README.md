## Simple Pydantic AI Agent

This project gives you a small chat app with:

- Pydantic AI for the agent
- OpenRouter as the model provider
- `openrouter/free` as the default model
- Gradio as the frontend
- Short answers by default

I used the OpenRouter setup pattern described in `llms-full.md`, including the `OpenRouterModel(...)` approach and `OPENROUTER_API_KEY` environment variable.

## Project Files

- `main.py` starts the app
- `app/config.py` loads `.env` settings
- `app/agent.py` creates the Pydantic AI agent
- `app/ui.py` creates the Gradio chat UI
- `.env` stores your local settings

## 1. Add Your API Key

Open `.env` and set your real OpenRouter key:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=openrouter/free
APP_HOST=127.0.0.1
APP_PORT=7860
APP_TITLE=Short Answer Agent
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

## How It Works

- The app loads your key from `.env`
- It creates a Pydantic AI `Agent`
- The agent uses `OpenRouterModel("openrouter/free")`
- The system instructions tell the agent to answer briefly
- Gradio shows a simple chat interface

## Notes

- `openrouter/free` is the default model router for free inference on OpenRouter
- If you want a different model later, change `OPENROUTER_MODEL` in `.env`
- `.env` is ignored by git so your key stays local
