# config.py
# Central configuration for MiniSearch.
# Change values here — never hardcode them inside modules.

# --- Crawler settings ---
SEED_URLS = [
    "https://wikipedia.org",
]

MAX_PAGES = 50      # Stop after crawling this many pages
MAX_DEPTH = 3       # How many link-hops away from seed URLs to go
REQUEST_DELAY = 1.0 # Seconds to wait between requests (be polite!)
REQUEST_TIMEOUT = 5 # Seconds before giving up on a request
USER_AGENT = "MiniSearch/1.0 (educational project)"

# --- Indexer settings ---
LANGUAGE = "english"  # Used for NLTK stopwords. Try "spanish" too.
MIN_TOKEN_LENGTH = 2  # Ignore tokens shorter than this

# --- Ranker settings ---
PAGERANK_DAMPING = 0.85    # Classic PageRank damping factor
PAGERANK_ITERATIONS = 100  # Max iterations before we stop
PAGERANK_TOLERANCE = 1e-6  # Convergence threshold

SCORE_ALPHA = 0.7  # Weight for TF-IDF vs PageRank in final score
                   # final = alpha * tfidf + (1 - alpha) * pagerank

# --- Storage ---
DATA_DIR = "data/"
CRAWLED_PAGES_FILE = DATA_DIR + "crawled_pages.json"
INDEX_FILE = DATA_DIR + "index.json"
PAGERANK_FILE = DATA_DIR + "pagerank.json"
