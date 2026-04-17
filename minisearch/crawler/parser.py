# crawler/parser.py
# Extracts links and clean text from raw HTML using BeautifulSoup.

from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def parse(html: str, base_url: str) -> dict:
    """
    Parse raw HTML and extract:
    - title: page title
    - text: clean visible text
    - links: absolute URLs found on the page
    """
    soup = BeautifulSoup(html, "lxml")

    title = _extract_title(soup)
    text = _extract_text(soup)
    links = _extract_links(soup, base_url)

    return {
        "title": title,
        "text": text,
        "links": links,
    }


def _extract_title(soup: BeautifulSoup) -> str:
    tag = soup.find("title")
    return tag.get_text(strip=True) if tag else "No title"


def _extract_text(soup: BeautifulSoup) -> str:
    # Remove tags that don't contain readable content
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    return " ".join(soup.get_text().split())  # Collapse whitespace


def _extract_links(soup: BeautifulSoup, base_url: str) -> list[str]:
    links = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]

        # Convert relative URLs to absolute (e.g. /about → https://example.com/about)
        absolute = urljoin(base_url, href)

        # Only keep http/https links, drop mailto:, javascript:, etc.
        if urlparse(absolute).scheme in ("http", "https"):
            links.append(absolute)

    return list(set(links))  # Deduplicate


# --- Quick test ---
if __name__ == "__main__":
    from fetcher import fetch

    url = "https://example.com"
    html = fetch(url)
    result = parse(html, url)

    print(f"Title:  {result['title']}")
    print(f"Text:   {result['text'][:200]}")
    print(f"Links:  {result['links']}")