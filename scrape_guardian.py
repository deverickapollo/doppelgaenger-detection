#!/usr/bin/python
# Helper functions to crawl Guardian News Website
from urllib.request import Request

from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
import logging
from scrapy.utils.log import configure_logging
from scrapy.settings import Settings
import os
from db_access import *



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

def runSpider():
    # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    configure_logging(install_root_handler = False) 
    logging.basicConfig ( 
    filename = 'logging.txt', 
    format = '%(levelname)s: %(message)s', 
    level = logging.DEBUG 
    )
    settings = Settings()
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'settings'
    settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
    settings.setmodule(settings_module_path, priority='default')
    runner = CrawlerRunner(settings)
    database = r'database/dopplegaenger.db'
    conn = create_connection(database)
    
    if conn is not None:
        create_guardian_table(conn)
        
        d = runner.crawl(guardianSpider,connection=conn)
        d.addBoth(lambda _: reactor.stop())
        reactor.run()  # the script will block here until the crawling is finished
    else:
        logging.log(logging.ERROR, "Error! Database Tables Not Created.")

    close_connection(conn)

runSpider()