from dataclasses import dataclass
from typing import Protocol

import httpx

from .config import settings


@dataclass
class SearchResult:
    title: str
    url: str
    description: str


class SearchProvider(Protocol):
    async def search(self, query: str, count: int = 10) -> list[SearchResult]: ...


class BraveSearchProvider:
    endpoint = "https://api.search.brave.com/res/v1/web/search"

    async def search(self, query: str, count: int = 10) -> list[SearchResult]:
        if not settings.brave_search_api_key:
            return []

        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": settings.brave_search_api_key,
        }
        params = {"q": query, "count": max(1, min(count, 20))}

        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(self.endpoint, headers=headers, params=params)
            response.raise_for_status()
            payload = response.json()

        results = payload.get("web", {}).get("results", [])
        return [
            SearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                description=item.get("description", ""),
            )
            for item in results
            if item.get("url")
        ]


def get_search_provider() -> SearchProvider:
    if settings.search_provider.lower() != "brave":
        raise ValueError(f"Unsupported search provider: {settings.search_provider}")
    return BraveSearchProvider()
