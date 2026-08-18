import os
import time
import json
import requests
from datetime import datetime, timezone
from urllib.parse import urljoin
from pathlib import Path
from bs4 import BeautifulSoup

CACHE_DIR = Path(__file__).resolve().parent.parent / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "FlyRankInternship-A9/1.0 (+https://github.com/mubiii3456/backend_api)"
}

def fetch_page(url: str, cache_filename: str) -> str:
    cache_path = CACHE_DIR / cache_filename
    
    if cache_path.exists():
        return cache_path.read_text(encoding="utf-8")

    time.sleep(0.5)
    print(f"FETCH: Requesting {url}")
    
    # Timeout increased to 10s for slow connections
    for attempt in range(2):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch page. Status code: {response.status_code}")

            html_content = response.text
            cache_path.write_text(html_content, encoding="utf-8")
            return html_content
        except requests.RequestException as e:
            if attempt == 1:
                print(f"Error fetching URL {url}: {e}")
                raise
            print(f"Retrying {url}...")
            time.sleep(1)

def discover_book_urls(start_url: str, max_pages: int = 3):
    current_url = start_url
    page_count = 0
    all_book_entries = []

    while current_url and page_count < max_pages:
        page_count += 1
        cache_file = f"catalogue-page-{page_count}.html"
        html = fetch_page(current_url, cache_file)
        soup = BeautifulSoup(html, "html.parser")

        article_nodes = soup.select("article.product_pod h3 a")
        for a_tag in article_nodes:
            relative_href = a_tag.get("href")
            absolute_url = urljoin(current_url, relative_href)
            all_book_entries.append({
                "url": absolute_url,
                "source_page": current_url
            })

        next_a = soup.select_one("li.next a")
        if next_a:
            next_href = next_a.get("href")
            current_url = urljoin(current_url, next_href)
        else:
            current_url = None

    seen_urls = set()
    unique_entries = []
    for entry in all_book_entries:
        if entry["url"] not in seen_urls:
            seen_urls.add(entry["url"])
            unique_entries.append(entry)

    return unique_entries

def extract_book_detail(book_entry: dict, index: int) -> dict:
    product_url = book_entry["url"]
    source_page = book_entry["source_page"]
    cache_file = f"book-detail-{index}.html"
    
    html = fetch_page(product_url, cache_file)
    soup = BeautifulSoup(html, "html.parser")

    main_node = soup.select_one(".product_main")
    
    title = main_node.select_one("h1").get_text(strip=True) if main_node and main_node.select_one("h1") else "Unknown"
    price_text = main_node.select_one("p.price_color").get_text(strip=True) if main_node and main_node.select_one("p.price_color") else ""
    availability_text = main_node.select_one("p.instock.availability").get_text(strip=True) if main_node and main_node.select_one("p.instock.availability") else ""
    
    rating_node = main_node.select_one("p.star-rating") if main_node else None
    rating_text = "None"
    if rating_node:
        classes = rating_node.get("class", [])
        for c in classes:
            if c != "star-rating":
                rating_text = c
                break

    desc_header = soup.find("div", id="product_description")
    description = None
    if desc_header:
        desc_p = desc_header.find_next_sibling("p")
        if desc_p:
            description = desc_p.get_text(strip=True)

    fetched_at = datetime.now(timezone.utc).isoformat()

    return {
        "title": title,
        "product_url": product_url,
        "price_text": price_text,
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": description,
        "source_page": source_page,
        "fetched_at": fetched_at
    }

if __name__ == "__main__":
    start_catalogue_url = "https://books.toscrape.com/catalogue/page-1.html"
    book_entries = discover_book_urls(start_catalogue_url, max_pages=3)
    
    raw_records = []
    print("\nFetching & extracting book details...")
    for idx, entry in enumerate(book_entries, start=1):
        record = extract_book_detail(entry, idx)
        raw_records.append(record)

    print(f"\ndetail_pages={len(raw_records)}")
    print("\nSample Raw Record:")
    print(json.dumps(raw_records[0], indent=2))