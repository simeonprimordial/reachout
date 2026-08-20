from pydantic import BaseModel, Field


class CompanySearchResult(BaseModel):
    name: str
    website: str
    title: str
    description: str
    source_url: str


class CompanySearchResponse(BaseModel):
    query: str
    provider: str
    results: list[CompanySearchResult] = Field(default_factory=list)
