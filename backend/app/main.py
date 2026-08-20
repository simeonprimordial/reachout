from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .schemas import CompanySearchResponse, CompanySearchResult
from .search import get_search_provider

app = FastAPI(
    title="ReachOut API",
    description="Global company discovery and outreach intelligence platform.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "reachout-api"}


@app.get("/api/companies", response_model=CompanySearchResponse)
async def search_companies(
    q: str = Query(..., min_length=2, max_length=200),
    count: int = Query(10, ge=1, le=20),
) -> CompanySearchResponse:
    if not settings.brave_search_api_key:
        raise HTTPException(
            status_code=503,
            detail="Web search is not configured. Add BRAVE_SEARCH_API_KEY to the backend environment.",
        )

    provider = get_search_provider()
    try:
        results = await provider.search(q, count)
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Search provider request failed.") from exc

    companies = []
    for result in results:
        parsed = urlparse(result.url)
        website = f"{parsed.scheme}://{parsed.netloc}" if parsed.netloc else result.url
        companies.append(
            CompanySearchResult(
                name=parsed.netloc.removeprefix("www.") or result.title,
                website=website,
                title=result.title,
                description=result.description,
                source_url=result.url,
            )
        )

    return CompanySearchResponse(
        query=q,
        provider=settings.search_provider,
        results=companies,
    )
