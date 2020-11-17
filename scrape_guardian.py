#!/usr/bin/python
# Helper functions to crawl Guardian News Website
import logging, re, pytz, requests, scrapy
from scrapy import *
from datetime import datetime, timezone as ttime
import pytz
from pytz import timezone

bst = pytz.timezone('Europe/London')

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
        date_xa0 = date_stripped.replace(u'\xa0', u' ')
        #HANDLE BST TIMESTAMPS
        if (date_xa0.find('BST') != -1):
            scrubbed = date_xa0[:-4]
            naive = datetime.strptime(scrubbed, "%a %d %b %Y %H.%M")
            local_dt = bst.localize(naive, is_dst=None)
            timestamp = local_dt.astimezone(pytz.utc).timestamp()
        else:
            time_in_datetime = datetime.strptime(date_xa0, "%a %d %b %Y %H.%M %Z")
            timestamp = time_in_datetime.replace(tzinfo=ttime.utc).timestamp()
        yield {
            'title': title, #string
            'url': response.meta.get('url'), #string
            'author': author, #string
            'publish_date': timestamp #datetime object stored as a timestamp from epoch 
        }

class commentSpider(scrapy.Spider):
    name = "toscrape-comment-css"

    def __init__(self, *args, **kwargs):
        super(commentSpider, self).__init__(*args, **kwargs)
        conn = kwargs.get('connection')
        if not conn:
            raise ValueError('No connection argument available')
        self.start_urls = ['https://www.theguardian.com/international']

    def parse(self, response):
        link = url.css("a::attr(href)").extract_first()
        yield scrapy.Request(url=link, callback=self.parse_article, meta={'url': link})

    def parse_article(self, response):
        date = response.xpath('//*[@class="css-1kkxezg"]//text()').extract_first()