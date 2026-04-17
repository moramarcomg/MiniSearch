# crawler/fetcher.py
import requests
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config

def fetch(url: str) -> str | None:
    headers = {"User-Agent": config.USER_AGENT}

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=config.REQUEST_TIMEOUT
        )
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type:
            print(f"[SKIP] Not HTML: {url} ({content_type})")
            return None

        response.encoding = response.apparent_encoding
        return response.text

    except requests.exceptions.Timeout:
        print(f"[ERROR] Timeout: {url}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Connection error: {url}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] HTTP {e.response.status_code}: {url}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error fetching {url}: {e}")
        return None


if __name__ == "__main__":
    test_url = "https://example.com"
    print(f"Fetching {test_url}...")
    html = fetch(test_url)
    if html:
        print(f"Success! Got {len(html)} characters")
        print(html[:300])
    else:
        print("Failed to fetch.")