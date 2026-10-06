"""Scrape quotes.toscrape.com into data/quotes.json and data/authors.json,
then load both files into MongoDB with the HW #8 loader.

Run from the project root:
    python main.py            # scrape + load into the database
    python main.py --no-seed  # scrape only
"""
import argparse

from scrapy.crawler import CrawlerProcess

from config import AUTHORS_FILE, QUOTES_FILE
from scraper.items import AuthorItem, QuoteItem
from scraper.spider import QuotesSpider


def feed(item_class) -> dict:
    return {
        "format": "json",
        "encoding": "utf8",
        "indent": 2,
        "overwrite": True,
        "item_classes": [item_class],
    }


SETTINGS = {
    "FEEDS": {
        QUOTES_FILE.as_uri(): feed(QuoteItem),
        AUTHORS_FILE.as_uri(): feed(AuthorItem),
    },
    "LOG_LEVEL": "INFO",
}


def crawl():
    process = CrawlerProcess(settings=SETTINGS)
    process.crawl(QuotesSpider)
    process.start()


def main():
    parser = argparse.ArgumentParser(description="Scrape quotes.toscrape.com and load the result into MongoDB.")
    parser.add_argument("--no-seed", action="store_true", help="only scrape, do not load into MongoDB")
    args = parser.parse_args()

    crawl()
    print(f"Saved {QUOTES_FILE} and {AUTHORS_FILE}")

    if not args.no_seed:
        from db.seed import main as seed

        seed()


if __name__ == "__main__":
    main()
