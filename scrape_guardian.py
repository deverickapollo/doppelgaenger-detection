#!/usr/bin/python
# Helper functions to crawl Guardian News Website
from urllib.request import Request

from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging


class guardianSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = [
        'https://www.theguardian.com/international',
    ]


    def parse(self, response):
        for url in response.css("h3.fc-item__title"):
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


    def runSpider(self):
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        runner = CrawlerRunner()

        d = runner.crawl(guardianSpider)
        d.addBoth(lambda _: reactor.stop())
        reactor.run()  # the script will block here until the crawling is finished


