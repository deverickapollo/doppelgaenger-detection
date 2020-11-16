#!/usr/bin/python
# Main File for the Dopplegaenger Detection Program
# Execute: python3 guardianbot.py

from scrape_guardian import *
from db_access import *
import logging

import scrapy
import os

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.settings import Settings

def main():
	configure_logging(install_root_handler = False)
	logging.basicConfig (
    filename = 'logs/spider.log',
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
		create_article_table(conn)
		create_user_table(conn)
		create_comment_table(conn)
		d = runner.crawl(guardianSpider,connection=conn)
		d.addBoth(lambda _: reactor.stop())
		reactor.run()  # the script will block here until the crawling is finished
	else:
	    logging.log(logging.ERROR, "Error! Database Tables Not Created.")
	close_db_connection(conn)

if __name__ == '__main__':
	main()
