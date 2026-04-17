# crawler/crawler.py
# BFS-based web crawler. Starts from seed URLs and follows links.

import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config
from fetcher import fetch
from parser import parse

from collections import deque


def crawl(seed_urls: list[str]) -> list[dict]:
    """
    BFS crawl starting from seed_urls.
    Returns a list of page dicts with url, title, text, links.
    """
    visited = set()
    queue = deque()
    pages = []

    # Seed the queue — each item is (url, depth)
    for url in seed_urls:
        queue.append((url, 0))
        visited.add(url)

    print(f"[CRAWL] Starting. Seed URLs: {len(seed_urls)}")

    while queue and len(pages) < config.MAX_PAGES:
        url, depth = queue.popleft()

        # Don't go deeper than MAX_DEPTH
        if depth > config.MAX_DEPTH:
            continue

        print(f"[CRAWL] ({len(pages)+1}/{config.MAX_PAGES}) depth={depth} {url}")

        html = fetch(url)
        if not html:
            continue

        parsed = parse(html, url)

        page = {
            "url": url,
            "title": parsed["title"],
            "text": parsed["text"],
            "outbound_links": parsed["links"],
            "depth": depth,
        }
        pages.append(page)

        # Add unvisited links to the queue
        for link in parsed["links"]:
            if link not in visited:
                visited.add(link)
                queue.append((link, depth + 1))

        time.sleep(config.REQUEST_DELAY)  # Be polite

    print(f"[CRAWL] Done. Crawled {len(pages)} pages.")
    return pages


# --- Quick test ---
if __name__ == "__main__":
    results = crawl(config.SEED_URLS)
    print(f"\nSample page:")
    if results:
        p = results[0]
        print(f"  URL:   {p['url']}")
        print(f"  Title: {p['title']}")
        print(f"  Text:  {p['text'][:150]}")
        print(f"  Links: {len(p['outbound_links'])} found")