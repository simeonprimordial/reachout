from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

from .enrichment import enrich_company

router = APIRouter(prefix="/api/enrichment", tags=["enrichment"])


class EnrichmentRequest(BaseModel):
    url: HttpUrl


@router.post("/company")
async def enrich(request: EnrichmentRequest):
    try:
        profile = await enrich_company(str(request.url))
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Unable to read the company website.") from exc

    return profile.__dict__
