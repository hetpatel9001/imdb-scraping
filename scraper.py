#!/usr/bin/env python3
"""IMDb scraping starter: search titles and print rating / plot.

Uses requests + BeautifulSoup. IMDb may rate-limit or block automated
requests; keep the volume low and respect robots.txt / the Terms of Use.
"""
import argparse
import json
import sys
import time

import requests
from bs4 import BeautifulSoup

BASE = "https://www.imdb.com"
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}


def get(url):
    last = None
    for attempt in range(3):
        try:
            r = requests.get(url, headers=HEADERS, timeout=20)
            r.raise_for_status()
            return BeautifulSoup(r.text, "html.parser")
        except requests.RequestException as e:
            last = e
            time.sleep(1 * (attempt + 1))
    raise last


def search(query, limit=5):
    soup = get(BASE + "/find?q=" + query)
    out = []
    for a in soup.select("a.ipc-metadata-list-summary-item__t")[:limit]:
        out.append((a.get_text(strip=True), a.get("href", "")))
    return out


def title_details(path):
    soup = get(BASE + path)
    title = soup.select_one("h1")
    rating = soup.select_one('[data-testid="hero-rating-bar__aggregate-rating__score"] span')
    summary = soup.select_one('[data-testid="plot-xs_to_m"] span')
    return {
        "title": title.get_text(strip=True) if title else "?",
        "rating": rating.get_text(strip=True) if rating else "?",
        "plot": summary.get_text(strip=True) if summary else "?",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("query")
    p.add_argument("--open", action="store_true", help="Fetch details for the first result")
    p.add_argument("--json", action="store_true", help="Print results as JSON")
    p.add_argument("--limit", type=int, default=5, help="How many results to show")
    args = p.parse_args()
    results = search(args.query, args.limit)
    if not results:
        print("No results for:", args.query, file=sys.stderr)
        sys.exit(1)
    if args.json:
        print(json.dumps([{"title": t, "href": h} for t, h in results], indent=2))
        return
    for i, (title, href) in enumerate(results, 1):
        print("%d. %s (%s)" % (i, title, href))
    if args.open:
        d = title_details(results[0][1])
        print("\n%s | rating %s\n%s" % (d["title"], d["rating"], d["plot"]))


if __name__ == "__main__":
    main()
