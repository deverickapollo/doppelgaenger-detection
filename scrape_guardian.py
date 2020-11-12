#!/usr/bin/python
# Helper functions to crawl Guardian News Website

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
        yield {
            'title': url.css("span.js-headline-text::text").extract_first(),
            'url': url.css("a::attr(href)").extract()
        }


def parse_article(self, response):
    yield {
        'author': response.css("p.byline span span::text").extract_first(),
        'publish_date': response.css("time.content__dateline-wpd::text").extract_first(),
        'publish_time': response.css("span.content__dateline-time::text").extract_first()
    }


def runSpider():
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner()

    d = runner.crawl(guardianSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished
