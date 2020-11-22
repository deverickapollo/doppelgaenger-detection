#!/usr/bin/python
# Main File for the Dopplegaenger Detection Program
# Execute: python3 guardianbot.py
from scrape_guardian import *
from db_access import *
import logging, scrapy, os, asyncio, argparse

from logging import FileHandler
from logging import Formatter

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.settings import Settings

# Construct an argument parser
all_args = argparse.ArgumentParser()

# Add arguments to the parser
all_args.add_argument("-v", "--version", help="Show version information.", action="store_true")
all_args.add_argument("-c", "--clean", help="Purge database and logs. Program exits after.", action="store_true")
all_args.add_argument("-l", "--log", help="Outputs report.log to the logs directory. Program continues.", action="store_true")
all_args.add_argument("-s", "--size", required=False, help="Output collection of comments from all users to CLI.")
all_args.add_argument("-u", "--user", nargs="*", required=False, help="Output a specified number of comments from a specific user to CLI.")


args = all_args.parse_args()

#Report Log 
LOG_FORMAT = (
	"%(message)s "
)
LOG_LEVEL = logging.INFO
# messaging logger
MESSAGING_LOG_FILE = os.getcwd() + "/logs/report.log"
messaging_logger = logging.getLogger("doppelgaenger_detection.guardianbot")

def main(log=False,size=0):
	#Database declaration and connection
	database = r'database/dopplegaenger.db'
	conn_article = create_connection(database)
	conn_comments = create_connection(database)
	if args.size:
		size = args.size
	if args.log:
		log = args.log
	if args.clean:
		drop_all(conn_article)
		if os.path.isfile('logs/webapp.log'):
			open('logs/webapp.log', 'w').close()
		else:
			print ("Webapp log doesn't exist")
			logging.log(logging.ERROR, "Error! Webapp log doesn't exist.")
		if os.path.isfile('logs/report.log'):
			open('logs/report.log', 'w').close()
		else:
			print ("Report log doesn't exist")
			logging.log(logging.ERROR, "Error! Report log doesn't exist.")
	elif args.version:
		print("GuardianBot version 1.0")
	else:
		if log:
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

		if conn_article is not None and conn_comments is not None:
			create_article_table(conn_article)
			create_user_table(conn_article)
			create_comment_table(conn_article)
			runner = CrawlerRunner(settings)
			runner.crawl(guardianSpider,connection=conn_article)
			runner.crawl(commentSpider,connection=conn_comments)
			d = runner.join() 
			d.addBoth(lambda _: reactor.stop())
			reactor.run()  # the script will block here until the crawling is finished
		else:
			logging.log(logging.ERROR, "Fatal Error! Database Tables Not Created. Exiting!")
	if size:
		try:
			#Returns a dictionary curstor instead of tuple
			conn_comments.row_factory = sql.Row
			cursor = sql_select_all_users(conn_comments)
			rows_user = cursor.fetchall(); 
			for user in rows_user:
				print("Next User: ", user['username'])
				print("--------------------------------------------------")
				logging.log(logging.INFO, 'Next User: %s', user['username'])
				try:
					#Returns a dictionary curstor instead of tuple
					conn_comments.row_factory = sql.Row
					cur = sql_select_comments_from_user(conn_comments,user['username'],args.size)
					rows = cur.fetchall(); 
					for row in rows:
						print(" Article Title: ", row['article_title'], "\n" , "Article URL: ", row['article_url'], "\n\n" " User Comment: ", row['comment_text'] , "\n")
				except sql.Error as error:
					logging.log(logging.ERROR, "Fatal Error! Comment Table Not Accessible. Exiting!")
		except sql.Error as error:
			logging.log(logging.ERROR, "Fatal Error! Users Table Not Accessible. Exiting!")
	if args.user:
		try:
			#Returns a dictionary curstor instead of tuple
			conn_comments.row_factory = sql.Row
			print("User: ", args.user[0])
			print("--------------------------------------------------")
			# logging.log(logging.INFO, 'Next User: %s', user['username'])
			try:
				#Returns a dictionary curstor instead of tuple
				conn_comments.row_factory = sql.Row
				cur = sql_select_comments_from_user(conn_comments,args.user[0],int(args.user[1]))
				rows = cur.fetchall();
				for row in rows:
					print(" Article Title: ", row['article_title'], "\n" , "Article URL: ", row['article_url'], "\n\n" " User Comment: ", row['comment_text'] , "\n")
			except sql.Error as error:
				logging.log(logging.ERROR, "Fatal Error! Comment Table Not Accessible. Exiting!")
		except sql.Error as error:
			logging.log(logging.ERROR, "Fatal Error! Users Table Not Accessible. Exiting!")

	close_db_connection(conn_article)
	close_db_connection(conn_comments)

main()
