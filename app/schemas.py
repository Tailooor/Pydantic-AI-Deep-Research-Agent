from __future__ import annotations

from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str


class ResearchAngle(BaseModel):
    title: str = Field(description="Short research angle title")
    reason: str = Field(description="Why this angle matters")
    search_keywords: str = Field(description="DuckDuckGo query for this angle")


class ResearchPlan(BaseModel):
    intent: str = Field(description="Either ticker or general_query")
    normalized_input: str = Field(description="Normalized version of the user input")
    subject_name: str = Field(description="Resolved company name or main research subject")
    ticker: str | None = Field(default=None, description="Ticker if detected")
    subject_context: str = Field(
        description="Short context about the subject, company, sector, or topic"
    )
    discovery_search_query: str = Field(description="Query used for the first search")
    research_angles: list[ResearchAngle] = Field(
        min_length=3,
        max_length=4,
        description="Three to four non-overlapping research angles",
    )


class ResearchAngleFindings(BaseModel):
    angle_title: str
    key_takeaways: list[str] = Field(min_length=2, max_length=5)
    evidence_summary: str
    source_urls: list[str] = Field(default_factory=list)


class DeepResearchReport(BaseModel):
    report_title: str
    subject_name: str
    intent: str
    executive_summary: list[str] = Field(min_length=3, max_length=6)
    subject_profile: list[str] = Field(min_length=3, max_length=6)
    angle_findings: list[ResearchAngleFindings] = Field(min_length=3, max_length=4)
    opportunities: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    final_take: str
    sources: list[str] = Field(min_length=4)
