# W5 - The Polite Scraper (Python Lane)

A polite, resilient web scraping pipeline built in Python using **Requests**, **BeautifulSoup4**, and **Pydantic**. It extracts book catalogue data, validates schema compliance, safely caches HTML responses to prevent hammering the source server, and produces run telemetry reports.

---

## 🎯 Target Classification & Rules
* **Target Site:** Books to Scrape (`https://books.toscrape.com/`)
* **Purpose:** Educational exercise practicing web scraping pipelines on an open sandbox.
* **Scope:** First 3 catalogue pages (60 total book items).
* **Data Collected:** Book Title, Canonical Product URL, Raw Price, Clean Price (GBP), Availability, Rating, Description, Source Page, Fetch Timestamp.
* **Robots.txt Check:** `https://books.toscrape.com/robots.txt` returned no restrictive disallow rules for catalogue items.

> I will not reuse this code on another site without checking its rules and terms first.

---

## 🛠️ Politeness & Reliability Protocols
1. **Custom User-Agent:** `FlyRankInternship-A9/1.0 (+https://github.com/mubiii3456/backend_api)`
2. **Rate Limiting:** Built-in `0.5s` delay before outbound live network requests.
3. **Timeout Guard:** Requests abort after `10s` if server response hangs.
4. **Local Caching:** HTML responses are persisted to `cache/` during initial execution, allowing offline idempotency on subsequent runs.
5. **Browser Cost Comparison:** Pure HTTP requests were chosen over Playwright/Selenium because the target HTML contains static server-side rendered data. Bypassing headless browser execution saves ~100x CPU/memory overhead and runs in seconds.

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
2. Execute Scraper Pipeline
Bash
python src/main.py
📋 Data Record Schema (Pydantic)
Python
class BookRecord(BaseModel):
    title: str
    product_url: HttpUrl
    price_text: str
    price_gbp: float
    availability_text: str
    rating_text: str
    description: Optional[str] = None
    source_page: HttpUrl
    fetched_at: str
📊 Sample Run Telemetry (output/run-report.json)
JSON
{
  "timestamp": "2026-08-18T14:20:00Z",
  "duration_seconds": 1.12,
  "total_discovered": 60,
  "valid_records": 60,
  "failed_records": 0,
  "cache_hits": 63,
  "network_fetches": 0
}
⚖️ Ethics & Responsible Scraping
Always prefer official APIs when available.

Respect site terms, robots.txt, and rate limits.

Never scrape behind logins, paywalls, or sensitive personal data.