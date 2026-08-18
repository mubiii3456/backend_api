import os
import time
import requests
from urllib.parse import urljoin
from pathlib import Path
from bs4 import BeautifulSoup

# Base Configuration
CACHE_DIR = Path(__file__).resolve().parent.parent / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "FlyRankInternship-A9/1.0 (+https://github.com/mubiii3456/backend_api)"
}

def fetch_page(url: str, cache_filename: str) -> str:
    cache_path = CACHE_DIR / cache_filename
    
    if cache_path.exists():
        print(f"CACHE HIT: Loading from {cache_filename}")
        html_content = cache_path.read_text(encoding="utf-8")
        return html_content

    # Polite delay before real network request
    time.sleep(0.5)
    print(f"FETCH: Requesting {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch page. Status code: {response.status_code}")

        html_content = response.text
        cache_path.write_text(html_content, encoding="utf-8")
        return html_content
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        raise

def discover_book_urls(start_url: str, max_pages: int = 3):
    current_url = start_url
    page_count = 0
    all_book_urls = []

    while current_url and page_count < max_pages:
        page_count += 1
        cache_file = f"catalogue-page-{page_count}.html"
        html = fetch_page(current_url, cache_file)
        soup = BeautifulSoup(html, "html.parser")

        # Extract all book links on current page
        article_nodes = soup.select("article.product_pod h3 a")
        for a_tag in article_nodes:
            relative_href = a_tag.get("href")
            absolute_url = urljoin(current_url, relative_href)
            all_book_urls.append(absolute_url)

        # Find 'next' page link
        next_a = soup.select_one("li.next a")
        if next_a:
            next_href = next_a.get("href")
            current_url = urljoin(current_url, next_href)
        else:
            current_url = None

    # Remove duplicates preserving order
    unique_book_urls = list(dict.fromkeys(all_book_urls))

    print(f"\ncatalogue_pages={page_count}, discovered={len(all_book_urls)}, unique_urls={len(unique_book_urls)}")
    return unique_book_urls

if __name__ == "__main__":
    start_catalogue_url = "https://books.toscrape.com/catalogue/page-1.html"
    discovered_urls = discover_book_urls(start_catalogue_url, max_pages=3)