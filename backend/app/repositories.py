from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Company
from .search import SearchResult


def upsert_search_result(db: Session, result: SearchResult) -> Company:
    company = db.scalar(
        select(Company).where(Company.canonical_url == result.url)
    )

    if company is None:
        company = Company(
            name=result.title,
            website=result.url,
            canonical_url=result.url,
            description=result.description or None,
            discovered_from=result.url,
        )
        db.add(company)
    else:
        company.name = result.title or company.name
        company.description = result.description or company.description
        company.last_seen_at = company.last_seen_at

    return company
