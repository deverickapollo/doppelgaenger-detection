#!/usr/bin/python
# Main File for the Dopplegaenger Detection Program
# Execute: python3 guardianbot.py
from scrape_guardian import *
from db_access import *
import logging, scrapy, os, asyncio

from logging import FileHandler
from logging import Formatter

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.settings import Settings

from importlib import import_module

def main():
	#Report Log 
	# LOG_FORMAT = (
    # "%(asctime)s [%(levelname)s]: %(message)s in %(pathname)s:%(lineno)d")
	LOG_FORMAT = (
		"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s"
	)
	LOG_LEVEL = logging.INFO
	# messaging logger
	MESSAGING_LOG_FILE = os.getcwd() + "/logs/report.log"
	messaging_logger = logging.getLogger("doppelgaenger_detection.guardianbot")
	messaging_logger.setLevel(LOG_LEVEL)
	messaging_logger_file_handler = FileHandler(MESSAGING_LOG_FILE)
	messaging_logger_file_handler.setLevel(LOG_LEVEL)
	messaging_logger_file_handler.setFormatter(Formatter(LOG_FORMAT))
	messaging_logger.addHandler(messaging_logger_file_handler)


	#Debug Log
	configure_logging(install_root_handler = False)
	logging.basicConfig(filename='logs/webapp.log', level=logging.DEBUG, format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
	settings = Settings()
	os.environ['SCRAPY_SETTINGS_MODULE'] = 'settings'
	settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
	settings.setmodule(settings_module_path, priority='default')


	#Database declaration and connection
	database = r'database/dopplegaenger.db'
	conn = create_connection(database)
	conn2 = create_connection(database)
	if conn is not None:
		create_article_table(conn)
		create_user_table(conn)
		create_comment_table(conn)
		runner = CrawlerRunner(settings)
		runner.crawl(guardianSpider,connection=conn)
		runner.crawl(commentSpider,connection=conn2)
		d = runner.join() 
		d.addBoth(lambda _: reactor.stop())
		reactor.run()  # the script will block here until the crawling is finished
	else:
	    logging.log(logging.ERROR, "Error! Database Tables Not Created.")
	close_db_connection(conn)


main()
