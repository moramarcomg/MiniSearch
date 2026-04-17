# MiniSearch — Build a Search Engine from Scratch


## Project Philosophy

Google-like systems actually work under the hood — not just theoretically, but through.

---

## Final Project Structure

```
minisearch/
├── crawler/
│   ├── __init__.py
│   ├── crawler.py          # Web crawler (BFS-based)
│   ├── parser.py           # HTML parsing with BeautifulSoup
│   └── robots.py           # robots.txt respect
│
├── indexer/
│   ├── __init__.py
│   ├── index.py            # Inverted index builder
│   ├── tokenizer.py        # Text cleaning & tokenization
│   └── storage.py          # Persist index to disk (JSON)
│
├── ranker/
│   ├── __init__.py
│   ├── pagerank.py         # PageRank algorithm
│   └── scorer.py           # TF-IDF + PageRank combined score
│
├── api/
│   ├── __init__.py
│   ├── app.py              # Flask app entry point
│   └── routes.py           # Search API endpoints
│
├── frontend/
│   ├── templates/
│   │   ├── index.html      # Search home page
│   │   └── results.html    # Results page
│   └── static/
│       └── style.css
│
├── data/
│   ├── crawled_pages.json  # Raw crawled data
│   ├── index.json          # Inverted index
│   └── pagerank.json       # PageRank scores
│
├── tests/
│   ├── test_crawler.py
│   ├── test_indexer.py
│   └── test_ranker.py
│
├── requirements.txt
├── config.py               # Global config (seed URLs, limits, etc.)
└── README.md
```

---

## Roadmap — Phases & Commits

The project is divided into **5 phases**, each with several small commits. Each commit = one working, testable piece.

---

### Phase 0 — Project Setup
**Goal:** Repo structure, dependencies, config file. Nothing runs yet, but everything is organized.

| Commit | What you do |
|--------|-------------|
| `init: project scaffold` | Create folder structure and empty `__init__.py` files |
| `init: add requirements.txt` | Pin dependencies: Flask, BeautifulSoup4, requests, nltk |
| `init: config.py with seed URLs and limits` | Central config so nothing is hardcoded |

**What you learn:** Good project organization from day one.

**Key config values:**
```python
# config.py
SEED_URLS = ["https://example.com"]
MAX_PAGES = 50
MAX_DEPTH = 3
REQUEST_DELAY = 1.0  # Be polite to servers
```

---

### Phase 1 — Web Crawler
**Goal:** Crawl a set of seed URLs, follow links, and save raw HTML + metadata.

| Commit | What you do |
|--------|-------------|
| `crawler: basic HTTP fetcher with requests` | Fetch a single URL, handle errors and timeouts |
| `crawler: HTML parser extracts links and text` | Use BeautifulSoup to get `<a href>` links and body text |
| `crawler: BFS crawl loop with visited set` | Expand from seed URLs level by level, avoid revisiting |
| `crawler: respect robots.txt` | Parse and honor crawl rules before fetching |
| `crawler: save crawled pages to JSON` | Persist `{url, title, text, links, timestamp}` per page |

**What you learn:** How crawlers navigate the web, why BFS matters, HTTP basics, politeness rules.

**Core data structure per crawled page:**
```json
{
  "url": "https://example.com/page",
  "title": "Page Title",
  "text": "cleaned body text...",
  "outbound_links": ["https://example.com/other"],
  "depth": 1,
  "crawled_at": "2025-01-01T00:00:00"
}
```

---

### Phase 2 — Inverted Index
**Goal:** Turn raw crawled text into a searchable inverted index.

| Commit | What you do |
|--------|-------------|
| `indexer: tokenizer with stopword removal` | Lowercase, remove punctuation, drop common words |
| `indexer: build term frequency map per document` | Count how many times each token appears in each page |
| `indexer: build inverted index structure` | Map: `token → [{url, tf, positions}]` |
| `indexer: compute TF-IDF weights` | Weight terms by rarity across the corpus |
| `indexer: save and load index from disk` | Serialize to `data/index.json` and reload on startup |

**What you learn:** How search engines find relevant documents in milliseconds, what TF-IDF actually means.

**Core data structure:**
```json
{
  "python": [
    {"url": "https://example.com/a", "tf": 0.12, "tfidf": 0.34},
    {"url": "https://example.com/b", "tf": 0.05, "tfidf": 0.18}
  ]
}
```

**TF-IDF formula:**
```
TF(t, d)  = (count of t in d) / (total tokens in d)
IDF(t)    = log(total docs / docs containing t)
TF-IDF    = TF × IDF
```

---

### Phase 3 — PageRank Ranking
**Goal:** Use the link graph to score pages by importance, just like Google's original algorithm.

| Commit | What you do |
|--------|-------------|
| `ranker: build link graph from crawled data` | `{url: [outbound_links]}` adjacency map |
| `ranker: implement PageRank iteration` | Run the power iteration algorithm until convergence |
| `ranker: handle dangling nodes and damping factor` | Pages with no outlinks, damping factor d=0.85 |
| `ranker: save PageRank scores to disk` | Persist `{url: score}` to `data/pagerank.json` |
| `ranker: combine TF-IDF + PageRank into final score` | `final = alpha * tfidf + (1-alpha) * pagerank` |

**What you learn:** Graph theory applied to the web, why links are "votes", iterative algorithms.

**PageRank formula:**
```
PR(A) = (1 - d) + d × Σ [ PR(T_i) / C(T_i) ]

where:
  d    = damping factor (0.85)
  T_i  = pages that link to A
  C(T) = number of outbound links from T
```

**PageRank iteration (pseudocode):**
```python
for each iteration:
    for each page:
        PR[page] = (1 - d) / N + d * sum(PR[linker] / out_degree[linker]
                                          for linker in pages_that_link_to(page))
    if converged: break
```

---

### Phase 4 — Flask Search API & UI
**Goal:** Expose the search engine via a clean REST API and a simple web interface.

| Commit | What you do |
|--------|-------------|
| `api: Flask app skeleton with health check` | `GET /health` returns `{"status": "ok"}` |
| `api: POST /search returns ranked results` | Accept `q` param, query the index, return JSON |
| `api: load index and pagerank on startup` | One-time load into memory when Flask starts |
| `frontend: search home page (index.html)` | Simple input + submit form |
| `frontend: results page with ranked links` | Display title, URL, snippet, score |
| `api: GET /crawl triggers crawler run` | Optional endpoint to re-crawl and re-index |

**What you learn:** REST API design, serving ML results via Flask, separating concerns.

**API contract:**
```
GET  /                    → Search UI
GET  /search?q=python     → Search results (JSON)
POST /crawl               → Trigger a crawl (JSON body: {urls: [...]})
GET  /health              → System status
GET  /stats               → Index stats (total pages, terms, etc.)
```

**Search response format:**
```json
{
  "query": "python tutorial",
  "results": [
    {
      "url": "https://example.com/python",
      "title": "Python Tutorial",
      "snippet": "...Python is a great language for...",
      "score": 0.847,
      "pagerank": 0.023
    }
  ],
  "total": 12,
  "time_ms": 4
}
```

---

### Phase 5 — Testing & Polish
**Goal:** Make it reliable and production-ready (at mini scale).

| Commit | What you do |
|--------|-------------|
| `tests: crawler unit tests with mocked HTTP` | Test fetching, parsing, BFS logic |
| `tests: indexer unit tests` | Test tokenization, TF-IDF computation |
| `tests: ranker unit tests` | Test PageRank convergence on small graphs |
| `polish: add logging throughout` | Replace print() with Python logging module |
| `polish: error handling and edge cases` | Dead links, empty queries, missing pages |
| `polish: README final update + demo GIF` | Document how to run the full pipeline |

---

## Dependencies

```txt
# requirements.txt
flask>=3.0
requests>=2.31
beautifulsoup4>=4.12
lxml>=5.0           # Faster HTML parser for BeautifulSoup
nltk>=3.8           # Stopwords and tokenization
```

Install:
```bash
pip install -r requirements.txt
python -m nltk.downloader stopwords
```

---

## How to Run (End State)

```bash
# 1. Crawl seed URLs
python -m crawler.crawler

# 2. Build the index
python -m indexer.index

# 3. Compute PageRank
python -m ranker.pagerank

# 4. Start the search API
flask --app api/app.py run

# 5. Open browser
open http://localhost:5000
```

---

## Key Concepts Quick Reference

| Concept | Where it lives | One-line explanation |
|---------|---------------|----------------------|
| BFS Crawl | `crawler/crawler.py` | Explore the web level by level from seed URLs |
| Inverted Index | `indexer/index.py` | Map of `word → [documents]` for fast lookup |
| TF-IDF | `indexer/scorer.py` | How relevant a word is to a document vs the corpus |
| PageRank | `ranker/pagerank.py` | A page's importance = sum of importance of pages linking to it |
| Combined Score | `ranker/scorer.py` | `α × relevance + (1-α) × authority` |

---

## Learning Progression

```
Phase 0   → Understand project structure
Phase 1   → Understand how the web is traversed
Phase 2   → Understand how text becomes searchable
Phase 3   → Understand how links encode authority
Phase 4   → Understand how it all becomes an API
Phase 5   → Understand how to make it reliable
```

Each phase builds directly on the last.

---

## Ethical Crawling Rules

This project respects the following:

1. **Honor `robots.txt`** — Always check before crawling
2. **Rate limit requests** — Default 1 second delay between requests
3. **Set a proper User-Agent** — `MiniSearch/1.0 (educational project)`
4. **Stay within scope** — Only crawl domains in your seed list
5. **Small scale only** — `MAX_PAGES = 50` by default

---
