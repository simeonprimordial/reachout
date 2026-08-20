from dataclasses import dataclass
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup


@dataclass
class CompanyProfile:
    name: str
    website: str
    description: str | None
    careers_url: str | None
    source_url: str


async def enrich_company(url: str) -> CompanyProfile:
    parsed = urlparse(url)
    website = f"{parsed.scheme}://{parsed.netloc}"

    async with httpx.AsyncClient(
        timeout=15.0,
        follow_redirects=True,
        headers={"User-Agent": "ReachOut/0.1 (+company-discovery)"},
    ) as client:
        response = await client.get(website)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.get_text(" ", strip=True) if soup.title else parsed.netloc

    description = None
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        description = meta["content"].strip()

    careers_url = None
    for link in soup.find_all("a", href=True):
        text = link.get_text(" ", strip=True).lower()
        href = link["href"]
        if any(keyword in text for keyword in ("careers", "jobs", "join our team", "work with us")):
            careers_url = urljoin(website, href)
            break

    return CompanyProfile(
        name=title,
        website=website,
        description=description,
        careers_url=careers_url,
        source_url=response.url.__str__(),
    )
