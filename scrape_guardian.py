#!/usr/bin/python
# Helper functions to crawl Guardian News Website
import scrapy
import requests
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
        date = response.css("time.content__dateline-wpd::text").extract_first() + response.css("span.content__dateline-time::text").extract_first()
        if not date:
            date = response.xpath('//*[@class="css-1kkxezg"]//text()').extract_first()
        author = response.xpath('//*[@rel="author"]//text()').extract_first()
        title = response.xpath('normalize-space(//h1//text())').get()
        if not title:
            title = response.css('h1 span::text')
        #if not author:
         #   author = response.xpath('//*[@class="css-1rv9jci"]//text()').extract()

        yield {
            'title' : title,
            'url': response.meta.get('url'),
            'author' : author,
            'publish_date': date
        }