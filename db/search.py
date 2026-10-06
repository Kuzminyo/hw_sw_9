"""Interactive quote search.

Run from the project root:  python -m db.search
Results of `name:` and `tag:` are cached in Redis.
"""
import json
import re
import sys

import redis

from config import CACHE_TTL, REDIS_HOST, REDIS_PORT, connect_db
from db.models import Author, Quote

HELP = """Commands:
    name: Steve Martin   quotes by author (a prefix is enough: name:st)
    tag:life             quotes with the tag (a prefix is enough: tag:li)
    tags:life,live       quotes having any of the tags
    exit                 quit"""


def get_cache() -> redis.Redis | None:
    client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    try:
        client.ping()
        return client
    except redis.RedisError:
        print("Redis is unavailable, caching disabled.")
        return None


def prefix_regex(value: str) -> str:
    return "^" + re.escape(value)


def format_quote(q: Quote) -> str:
    return f"{q.quote}\n    — {q.author.fullname}  [{', '.join(q.tags)}]"


def find_by_name(value: str) -> list[str]:
    authors = Author.objects(fullname__iregex=prefix_regex(value))
    return [format_quote(q) for q in Quote.objects(author__in=authors)]


def find_by_tag(value: str) -> list[str]:
    return [format_quote(q) for q in Quote.objects(tags__iregex=prefix_regex(value))]


def find_by_tags(value: str) -> list[str]:
    tags = [t.strip() for t in value.split(",") if t.strip()]
    return [format_quote(q) for q in Quote.objects(tags__in=tags)]


HANDLERS = {"name": find_by_name, "tag": find_by_tag, "tags": find_by_tags}
CACHED_COMMANDS = {"name", "tag"}


def run_command(command: str, value: str, cache: redis.Redis | None) -> tuple[list[str], bool]:
    """Return (results, from_cache)."""
    use_cache = cache is not None and command in CACHED_COMMANDS
    key = f"quotes:{command}:{value.lower()}"
    if use_cache:
        cached = cache.get(key)
        if cached is not None:
            return json.loads(cached), True

    results = HANDLERS[command](value)
    if use_cache:
        cache.set(key, json.dumps(results, ensure_ascii=False), ex=CACHE_TTL)
    return results, False


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stdin.reconfigure(encoding="utf-8")
    connect_db()
    cache = get_cache()
    print(HELP)

    while True:
        try:
            line = input("\n>>> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not line:
            continue
        if line.lower() == "exit":
            break

        command, sep, value = line.partition(":")
        command, value = command.strip().lower(), value.strip()
        if not sep or command not in HANDLERS or not value:
            print("Unknown command. Use name:<author>, tag:<tag>, tags:<tag1>,<tag2> or exit.")
            continue

        results, from_cache = run_command(command, value, cache)
        if not results:
            print("Nothing found.")
            continue
        if from_cache:
            print("(from cache)")
        for item in results:
            print(item)

    print("Bye!")


if __name__ == "__main__":
    main()
