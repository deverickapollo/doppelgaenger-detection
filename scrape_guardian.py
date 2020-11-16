#!/usr/bin/python
# Helper functions to crawl Guardian News Website
import scrapy
import requests
from scrapy import *
from datetime import datetime
from datetime import timezone
import logging

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
        date = response.xpath('//*[@class="css-1kkxezg"]//text()').extract_first()
        title = response.xpath('normalize-space(//h1//text())').get()
        author = response.xpath('//*[@rel="author"]//text()').extract_first()
        if not date:
            date = response.css("time.content__dateline-wpd::text").extract_first() + response.css(
                "span.content__dateline-time::text").extract_first()
        if not title:
            title = response.css('h1 span::text').get()
        if not author:
            author = ''.join(response.xpath('//*[@class="css-1rv9jci"]//text()').extract())
        date_stripped = date.replace("\n", "")
        time_in_datetime = datetime.strptime(date_stripped, "%a %d %b %Y %H.%M %Z")
        timestamp = time_in_datetime.replace(tzinfo=timezone.utc).timestamp()
        yield {
            'title': title,
            'url': response.meta.get('url'),
            'author': author,
            'publish_date': timestamp
        }
