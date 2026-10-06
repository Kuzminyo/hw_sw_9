# Домашнє завдання #9 — скрапінг quotes.toscrape.com (Scrapy)

## Підготовка

```bash
pip install -r requirements.txt
cp .env.example .env          # вписати рядок підключення до MongoDB Atlas у MONGO_URI
```

## Запуск

```bash
python main.py            # скрапінг + завантаження в MongoDB
python main.py --no-seed  # тільки скрапінг
```

`main.py` запускає краулер через `CrawlerProcess`. Павук проходить усі сторінки сайту
(посилання `Next`) і заходить на сторінку кожного автора (повторні посилання відкидає
вбудований фільтр дублікатів Scrapy). Результат записують два feed-експорти Scrapy:

- `data/quotes.json` — `tags`, `author`, `quote` (100 цитат);
- `data/authors.json` — `fullname`, `born_date`, `born_location`, `description` (50 авторів).

Структура файлів така сама, як у ДЗ #8. Потім `main.py` викликає завантажувач із ДЗ #8
(`db/seed.py`), який перезаписує колекції `authors` і `quotes`.

| Файл | Призначення |
|---|---|
| `main.py` | Єдина точка входу: краулер + завантаження в базу |
| `scraper/spider.py` | Павук `QuotesSpider` |
| `scraper/items.py` | `QuoteItem`, `AuthorItem` |
| `db/models.py`, `db/seed.py`, `db/search.py` | Моделі, завантажувач і пошук із ДЗ #8 |

## Перевірка роботи ДЗ #8 з новою базою

```bash
python -m db.search       # name:st, tag:life, tags:life,live, exit
```

Або з проєкту ДЗ #8, вказавши нову базу: `MONGO_DB=hw9 python -m part1.search`.
