from __future__ import annotations

from ddgs import DDGS

from app.schemas import SearchResult


def duckduckgo_search(query: str, max_results: int = 5) -> list[SearchResult]:
    """Run a simple DuckDuckGo text search and normalize the response."""
    with DDGS() as ddgs:
        raw_results = list(ddgs.text(query, max_results=max_results))

    results: list[SearchResult] = []
    for item in raw_results:
        title = (item.get("title") or "").strip()
        url = (item.get("href") or "").strip()
        snippet = (item.get("body") or "").strip()
        if not title or not url:
            continue
        results.append(SearchResult(title=title, url=url, snippet=snippet))

    return results
