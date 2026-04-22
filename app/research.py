from __future__ import annotations

import re
from dataclasses import dataclass

from app.agent import build_planner_agent, build_report_agent
from app.config import Settings
from app.duckduckgo import duckduckgo_search
from app.schemas import DeepResearchReport, ResearchPlan, SearchResult


def _looks_like_ticker(user_input: str) -> bool:
    candidate = user_input.strip().upper()
    return bool(re.fullmatch(r"[A-Z]{1,5}(?:\.[A-Z])?", candidate))


def _render_results(results: list[SearchResult]) -> str:
    if not results:
        return "No results found."

    lines: list[str] = []
    for index, result in enumerate(results, start=1):
        lines.append(f"{index}. {result.title}")
        lines.append(f"URL: {result.url}")
        lines.append(f"Snippet: {result.snippet}")
    return "\n".join(lines)


def _discovery_query(user_input: str) -> str:
    if _looks_like_ticker(user_input):
        return f"{user_input.strip().upper()} stock company overview latest results"
    return user_input.strip()


@dataclass(slots=True)
class ResearchRun:
    plan: ResearchPlan
    report: DeepResearchReport
    discovery_results: list[SearchResult]
    angle_results: dict[str, list[SearchResult]]

    def to_markdown(self) -> str:
        lines = [
            f"# {self.report.report_title}",
            "",
            f"**Subject:** {self.report.subject_name}",
            f"**Intent:** {self.report.intent}",
            "",
            "## Executive Summary",
        ]
        lines.extend(f"- {item}" for item in self.report.executive_summary)
        lines.extend(["", "## Subject Profile"])
        lines.extend(f"- {item}" for item in self.report.subject_profile)

        for finding in self.report.angle_findings:
            lines.extend(
                [
                    "",
                    f"## {finding.angle_title}",
                    finding.evidence_summary,
                    "",
                    "Key takeaways:",
                ]
            )
            lines.extend(f"- {item}" for item in finding.key_takeaways)
            if finding.source_urls:
                lines.extend(["", "Sources:"])
                lines.extend(f"- {url}" for url in finding.source_urls)

        if self.report.opportunities:
            lines.extend(["", "## Opportunities"])
            lines.extend(f"- {item}" for item in self.report.opportunities)

        if self.report.risks:
            lines.extend(["", "## Risks"])
            lines.extend(f"- {item}" for item in self.report.risks)

        lines.extend(["", "## Final Take", self.report.final_take, "", "## Source List"])
        lines.extend(f"- {url}" for url in self.report.sources)
        return "\n".join(lines)


class DeepResearchService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.planner_agent = build_planner_agent(settings)
        self.report_agent = build_report_agent(settings)

    def run(self, user_input: str) -> ResearchRun:
        cleaned_input = user_input.strip()
        if not cleaned_input:
            raise ValueError("Enter a stock ticker or a research query.")

        discovery_query = _discovery_query(cleaned_input)
        discovery_results = duckduckgo_search(
            discovery_query,
            max_results=self.settings.discovery_result_count,
        )

        planning_prompt = "\n\n".join(
            [
                f"User input: {cleaned_input}",
                f"Ticker hint: {_looks_like_ticker(cleaned_input)}",
                f"Discovery query: {discovery_query}",
                "Discovery results:",
                _render_results(discovery_results),
            ]
        )
        plan = self.planner_agent.run_sync(planning_prompt).output

        angle_results: dict[str, list[SearchResult]] = {}
        for angle in plan.research_angles:
            angle_results[angle.title] = duckduckgo_search(
                angle.search_keywords,
                max_results=self.settings.angle_result_count,
            )

        report_prompt_parts = [
            f"Original input: {cleaned_input}",
            f"Resolved subject: {plan.subject_name}",
            f"Intent: {plan.intent}",
            f"Subject context: {plan.subject_context}",
            "",
            "Initial discovery results:",
            _render_results(discovery_results),
        ]

        for angle in plan.research_angles:
            report_prompt_parts.extend(
                [
                    "",
                    f"Research angle: {angle.title}",
                    f"Why it matters: {angle.reason}",
                    f"Search keywords used: {angle.search_keywords}",
                    "Results:",
                    _render_results(angle_results[angle.title]),
                ]
            )

        report = self.report_agent.run_sync("\n".join(report_prompt_parts)).output
        return ResearchRun(
            plan=plan,
            report=report,
            discovery_results=discovery_results,
            angle_results=angle_results,
        )
