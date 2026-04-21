from __future__ import annotations

from pydantic_ai import Agent
from pydantic_ai.models.openrouter import OpenRouterModel
from pydantic_ai.providers.openrouter import OpenRouterProvider

from app.config import Settings


SHORT_RESPONSE_INSTRUCTIONS = """
You are a helpful AI assistant.
Answer briefly and clearly.
Default to 1 to 3 short sentences.
If the user asks for code, keep the explanation short and give only the code they need.
""".strip()


def build_agent(settings: Settings) -> Agent:
    model = OpenRouterModel(
        settings.openrouter_model,
        provider=OpenRouterProvider(api_key=settings.openrouter_api_key),
    )
    return Agent(
        model=model,
        instructions=SHORT_RESPONSE_INSTRUCTIONS,
        output_type=str,
        name="short_answer_agent",
    )
