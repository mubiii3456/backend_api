import os
import requests
from pathlib import Path

# Base Configuration
CACHE_DIR = Path(__file__).resolve().parent.parent / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "FlyRankInternship-A9/1.0 (+https://github.com/mubiii3456/backend_api)"
}

def fetch_page(url: str, cache_filename: str) -> str:
    cache_path = CACHE_DIR / cache_filename
    
    # Check if cached version exists
    if cache_path.exists():
        print(f"CACHE HIT: Loading from {cache_filename}")
        html_content = cache_path.read_text(encoding="utf-8")
        print(f"Response size: {len(html_content)} characters")
        return html_content

    # Fetch from live web if not cached
    print(f"FETCH: Requesting {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        
        if response.status_code != 200:
            raise Exception(f"Failed to fetch page. Status code: {response.status_code}")

        html_content = response.text
        
        # Save to local cache
        cache_path.write_text(html_content, encoding="utf-8")
        print(f"Response size: {len(html_content)} characters")
        return html_content

    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        raise

if __name__ == "__main__":
    target_url = "https://books.toscrape.com/catalogue/page-1.html"
    fetch_page(target_url, "catalogue-page-1.html")