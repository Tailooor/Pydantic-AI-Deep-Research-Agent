from __future__ import annotations

from pydantic_ai import Agent
from pydantic_ai.models.openrouter import OpenRouterModel
from pydantic_ai.providers.openrouter import OpenRouterProvider

from app.config import Settings
from app.schemas import DeepResearchReport, ResearchPlan


PLANNER_INSTRUCTIONS = """
You are planning a multi-step web research workflow.
Classify whether the user input is a stock ticker or a general query.

Rules:
- If the input looks like a stock ticker, set intent to ticker.
- For a ticker, resolve the company name and brief business context from the discovery results.
- Create exactly 3 or 4 non-overlapping research angles.
- Angles must be practical, specific, and diverse.
- For stock research, prefer angles such as business overview, financial performance, competitive position, and recent developments or guidance.
- Keep search keywords concise and web-search friendly.
""".strip()


REPORT_WRITER_INSTRUCTIONS = """
You are a senior research analyst writing a structured deep research report.
Use only the provided research material and do not invent facts.
Be detailed, specific, and balanced.
Prefer crisp bullet-style observations in the structured fields.
When the topic is a stock, include business context, performance drivers, competition, opportunities, and risks.
""".strip()


def build_model(settings: Settings) -> OpenRouterModel:
    return OpenRouterModel(
        settings.openrouter_model,
        provider=OpenRouterProvider(api_key=settings.openrouter_api_key),
    )


def build_planner_agent(settings: Settings) -> Agent:
    return Agent(
        model=build_model(settings),
        instructions=PLANNER_INSTRUCTIONS,
        output_type=ResearchPlan,
        name="deep_research_planner",
    )


def build_report_agent(settings: Settings) -> Agent:
    return Agent(
        model=build_model(settings),
        instructions=REPORT_WRITER_INSTRUCTIONS,
        output_type=DeepResearchReport,
        name="deep_research_writer",
    )
