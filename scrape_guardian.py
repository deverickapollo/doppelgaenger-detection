#!/usr/bin/python
# Helper functions to crawl Guardian News Website
import scrapy
from scrapy import *

class guardianSpider(scrapy.Spider):
    name = "toscrape-css"

    def __init__(self, *args, **kwargs):
        super(guardianSpider, self).__init__(*args, **kwargs)
        conn = kwargs.get('connection')
        if not conn:
            raise ValueError('No connection argument available')
        self.start_urls = ['https://www.theguardian.com/international']

    def parse(self, response):
        for url in response.css("h3.fc-item__title"):
            title = url.css("span.js-headline-text::text").extract_first()
            link = url.css("a::attr(href)").extract_first()
            yield scrapy.Request(url=link, callback=self.parse_article, meta={'title': title, 'url': link})
        for url in response.css("h4.fc-sublink__title"):
            title = url.css("span.js-headline-text::text").extract_first()
            link = url.css("a::attr(href)").extract_first()
            yield scrapy.Request(url=link, callback=self.parse_article, meta={'title': title, 'url': link})

    def parse_article(self, response):
        yield {
            'title': response.meta.get('title'),
            'url': response.meta.get('url'),
            'author': response.css("p.byline span span::text").extract_first(),
            'publish_date': response.css("time.content__dateline-wpd::text").extract_first(),
            'publish_time': response.css("span.content__dateline-time::text").extract_first()
        }