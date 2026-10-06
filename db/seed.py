"""Load authors.json and quotes.json into MongoDB (the loader from HW #8).

Run from the project root:  python -m db.seed
Re-running is safe: both collections are recreated from the files.
"""
import json
from pathlib import Path

from config import AUTHORS_FILE, QUOTES_FILE, connect_db
from db.models import Author, Quote


def read_json(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def seed_authors() -> dict[str, Author]:
    Author.drop_collection()
    authors = {}
    for item in read_json(AUTHORS_FILE):
        authors[item["fullname"]] = Author(**item).save()
    return authors


def seed_quotes(authors: dict[str, Author]) -> int:
    Quote.drop_collection()
    count = 0
    for item in read_json(QUOTES_FILE):
        author = authors.get(item["author"])
        if author is None:
            print(f"Skipped quote: unknown author {item['author']!r}")
            continue
        Quote(tags=item["tags"], author=author, quote=item["quote"]).save()
        count += 1
    return count


def main():
    connect_db()
    authors = seed_authors()
    quotes_count = seed_quotes(authors)
    print(f"Loaded {len(authors)} authors and {quotes_count} quotes.")


if __name__ == "__main__":
    main()
