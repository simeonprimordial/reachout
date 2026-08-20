import re
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup


@dataclass
class PersonCandidate:
    name: str
    role: str
    source_url: str
    confidence: int


ROLE_PATTERNS = (
    "founder",
    "co-founder",
    "chief executive officer",
    "ceo",
    "chief technology officer",
    "cto",
    "chief information officer",
    "cio",
    "vp engineering",
    "vice president of engineering",
    "head of engineering",
)


def _is_leadership_role(text: str) -> bool:
    normalized = re.sub(r"\s+", " ", text.lower()).strip()
    return any(role in normalized for role in ROLE_PATTERNS)


def _clean_name(text: str) -> str | None:
    value = re.sub(r"\s+", " ", text).strip()
    if not value or len(value) < 3 or len(value) > 100:
        return None
    if any(char.isdigit() for char in value):
        return None
    return value


async def discover_people(company_url: str) -> list[PersonCandidate]:
    parsed = urlparse(company_url)
    website = f"{parsed.scheme}://{parsed.netloc}"

    async with httpx.AsyncClient(
        timeout=15.0,
        follow_redirects=True,
        headers={"User-Agent": "ReachOut/0.1 (+company-discovery)"},
    ) as client:
        response = await client.get(website)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    candidates: list[PersonCandidate] = []

    links = [
        urljoin(website, link["href"])
        for link in soup.find_all("a", href=True)
        if any(token in link.get_text(" ", strip=True).lower() for token in ("team", "leadership", "about"))
    ]

    for page_url in dict.fromkeys(links)[:5]:
        try:
            async with httpx.AsyncClient(
                timeout=15.0,
                follow_redirects=True,
                headers={"User-Agent": "ReachOut/0.1 (+company-discovery)"},
            ) as client:
                page = await client.get(page_url)
                page.raise_for_status()
        except httpx.HTTPError:
            continue

        page_soup = BeautifulSoup(page.text, "html.parser")
        for element in page_soup.find_all(["article", "section", "li", "div"]):
            text = element.get_text(" ", strip=True)
            if not _is_leadership_role(text) or len(text) > 500:
                continue

            role_match = next((role for role in ROLE_PATTERNS if role in text.lower()), None)
            if not role_match:
                continue

            headings = element.find_all(["h1", "h2", "h3", "h4", "strong"])
            name = next((_clean_name(node.get_text(" ", strip=True)) for node in headings), None)
            if name:
                candidates.append(PersonCandidate(name, role_match.title(), str(page.url), 80))

    unique: dict[tuple[str, str], PersonCandidate] = {}
    for candidate in candidates:
        unique[(candidate.name.lower(), candidate.role.lower())] = candidate
    return list(unique.values())
