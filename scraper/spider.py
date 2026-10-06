import scrapy

from scraper.items import AuthorItem, QuoteItem


class QuotesSpider(scrapy.Spider):
    """Walks every page of quotes.toscrape.com and visits each author's page once.

    Repeated author links are dropped by Scrapy's duplicate request filter,
    so every author is yielded exactly once.
    """

    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]

    def parse(self, response):
        for block in response.css("div.quote"):
            fullname = block.css("small.author::text").get().strip()
            yield QuoteItem(
                tags=block.css("a.tag::text").getall(),
                author=fullname,
                quote=block.css("span.text::text").get().strip(),
            )
            # Pass the name from the quote so authors.json and quotes.json use the same key.
            yield response.follow(
                block.css("a[href^='/author/']::attr(href)").get(),
                callback=self.parse_author,
                cb_kwargs={"fullname": fullname},
            )

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_author(self, response, fullname):
        details = response.css("div.author-details")
        yield AuthorItem(
            fullname=fullname,
            born_date=details.css("span.author-born-date::text").get().strip(),
            born_location=details.css("span.author-born-location::text").get().strip(),
            description=details.css("div.author-description::text").get().strip(),
        )
