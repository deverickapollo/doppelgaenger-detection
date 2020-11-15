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
            link = url.css("a::attr(href)").extract_first()
            yield scrapy.Request(url=link, callback=self.parse_article, meta={'url': link})
        for url in response.css("h4.fc-sublink__title"):
           link = url.css("a::attr(href)").extract_first()
           yield scrapy.Request(url=link, callback=self.parse_article, meta={'url': link})

    def parse_article(self, response):
        yield {
            'title' : response.xpath('normalize-space(//h1/text())').get(),
            'url': response.meta.get('url'),
            'author' : response.xpath('//a[@rel="author"]/text()').get(),
            'publish_date': response.css("time.content__dateline-wpd::text").extract_first(),
            'publish_time': response.css("span.content__dateline-time::text").extract_first()
        }