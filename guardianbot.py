#!/usr/bin/python
# Main for Dopplegaenger Detection Program
import database.db_access as db
from pprint import pprint

from scrape_guardian import *
from database.db_access import *
import logging, os, argparse, features.feature_generation as feat
import feature_matrix as fmatrix
import features.principal_component_analysis as pca, features.train_classifiers as trainer

from logging import FileHandler
from logging import Formatter

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.settings import Settings

import time
from datetime import datetime

start_time = time.time()

# Construct an argument parser
all_args = argparse.ArgumentParser()

# Add arguments to the parser
all_args.add_argument("-r", "--run", help="Run the Crawler", action="store_true")
all_args.add_argument("-i", "--info", help="Show information about the data collection ", action="store_true")
all_args.add_argument("-v", "--version", help="Show version information.", action="store_true")
all_args.add_argument("-c", "--clean", help="Purge database and logs. Program exits after.", action="store_true")
all_args.add_argument("-l", "--log", help="Outputs report.log to the logs directory. Program continues.", action="store_true")
all_args.add_argument("-s", "--size", required=False, help="Output a specified number of comments for every user to CLI.")
all_args.add_argument("-u", "--user", nargs=2, required=False, help="Requires username as first argument and max row count as second. Output a specified number of comments from a specific user to CLI.")
all_args.add_argument("-m", "--mode", nargs="*", required=False, help="Starts Crawler with the specified pre-processing feature.")
all_args.add_argument("-f", "--features", help="Start PCA task and optional dopplegaenger analysis", action="store_true")

args = all_args.parse_args()

#Report Log 
LOG_FORMAT = (
	"%(message)s "
)
LOG_LEVEL = logging.INFO

# messaging logger
MESSAGING_LOG_FILE = os.getcwd() + "/logs/report.log"
messaging_logger = logging.getLogger("doppelgaenger_detection.guardianbot")

# Input: String
# Output: Dictionary
# Comment: Used to generate comments using available feature
def mode_execute(mode):
	text = None
	switcher ={
		'char': lambda text: feat.character_frequency_letters(text),
		'vocab': lambda text: feat.character_frequency_letters(text),
		'sentence': lambda text: feat.character_frequency_letters(text),
		'leet': lambda text: feat.character_frequency_letters(text),
		'white': lambda text: feat.character_frequency_letters(text),
		'content': lambda text: feat.character_frequency_letters(text),
		'idio': lambda text: feat.character_frequency_letters(text),
	}
	#Returns a dictionary
	return switcher.get(mode)(text)

def main(spider="guardianSpider", log=False, size=0):
	#Database declaration and connection
	size = None
	log = None
	mode = None
	database = r'database/dopplegaenger.db'
	conn_article = create_connection(database)
	conn_comments = create_connection(database)
	conn_user = create_connection(database)
	messaging_logger.setLevel(LOG_LEVEL)
	messaging_logger_file_handler = FileHandler(MESSAGING_LOG_FILE)
	messaging_logger_file_handler.setLevel(LOG_LEVEL)
	messaging_logger_file_handler.setFormatter(Formatter(LOG_FORMAT))
	messaging_logger.addHandler(messaging_logger_file_handler)
	#Debug Log
	configure_logging(install_root_handler = False)
	# logging.basicConfig(filename='logs/webapp.log', level=logging.DEBUG, format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
	settings = Settings()
	os.environ['SCRAPY_SETTINGS_MODULE'] = 'settings'
	settings_module_path = os.environ['SCRAPY_SETTINGS_MODULE']
	settings.setmodule(settings_module_path, priority='default')

	if args.size:
		size = args.size
	if args.log:
		log = args.log
	if args.mode:
		mode = args.mode
	if args.clean:
		drop_all(conn_article)
		if os.path.isfile('logs/webapp.log'):
			open('logs/webapp.log', 'w').close()
		else:
			logging.log(logging.WARNING, "WARNING! Webapp log doesn't exist.")
		if os.path.isfile('logs/report.log'):
			open('logs/report.log', 'w').close()
		else:
			logging.log(logging.WARNING, "WARNING! Report log doesn't exist.")
	if args.version:
		print("GuardianBot version 1.0")
	if args.run:
		if conn_article is not None and conn_comments is not None:
			create_article_table(conn_article)
			create_user_table(conn_article)
			create_comment_table(conn_article)
			create_stats_table(conn_article)
			runner = CrawlerRunner(settings)
			runner.crawl(guardianSpider,connection=conn_article)
			runner.crawl(commentSpider,connection=conn_comments)
			d = runner.join() 
			d.addBoth(lambda _: reactor.stop())
			reactor.run()  # the script will block here until the crawling is finished
		else:
			logging.log(logging.ERROR, "Fatal Error! Database Tables Not Created. Exiting!")
	elif args.info:
		# datetime object containing current date and time
		now = datetime.now()
		# dd/mm/YY H:M:S
		dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
		messaging_logger.info("================ Executed at " + dt_string + " ================")
		try:
			cur = sql_count_articles(conn_article)
			number_articles = cur.fetchall()[0][0]
			print("Articles: " + str(number_articles))
			messaging_logger.info("Articles: " + str(number_articles))
		except sql.Error as error:
			logging.log(logging.ERROR, "Fatal Error! Articles Table Not Accessible. Exiting!")
		try:
			cur = sql_count_comments(conn_comments)
			number_comments = cur.fetchall()[0][0]
			print("Comments: " + str(number_comments))
			messaging_logger.info("Comments: " + str(number_comments))
		except sql.Error as error:
			logging.log(logging.ERROR, "Fatal Error! Comments Table Not Accessible. Exiting!")
		try:
			cur = sql_count_users(conn_user)
			number_users = cur.fetchall()[0][0]
			print("Users: " + str(number_users))
			messaging_logger.info("Users: " + str(number_users))
		except sql.Error as error:
			logging.log(logging.ERROR, "Fatal Error! Users Table Not Accessible. Exiting!")
		print("Average Comments per User: " + str(number_comments / number_users))
		messaging_logger.info("Average Comments per User: " + str(number_comments / number_users) + "\n")
	elif size:
		try:
			#Returns a dictionary cursor instead of tuple
			conn_comments.row_factory = sql.Row
			cursor = sql_select_all_users(conn_comments)
			rows_user = cursor.fetchall(); 
			for user in rows_user:
				print("Next User: ", user['username'])
				print("--------------------------------------------------")
				logging.log(logging.INFO, 'Next User: %s', user['username'])
				try:
					#Returns a dictionary cursor instead of tuple
					conn_comments.row_factory = sql.Row
					cur = sql_select_comments_from_user(conn_comments,user['username'],args.size)
					rows = cur.fetchall();
					for row in rows:
						print(" Article Title: ", row['article_title'], "\n" , "Article URL: ", row['article_url'], "\n\n" " User Comment: ", row['comment_text'] , "\n")
				except sql.Error as error:
					logging.log(logging.ERROR, "Fatal Error! Comment Table Not Accessible. Exiting!")
		except sql.Error as error:
			logging.log(logging.ERROR, "Fatal Error! Users Table Not Accessible. Exiting!")
	elif args.user:
		try:
			#Returns a dictionary cursor instead of tuple
			conn_comments.row_factory = sql.Row
			print("User: ", args.user[0])
			print("--------------------------------------------------")
			try:
				#Returns a dictionary cursor instead of tuple
				conn_comments.row_factory = sql.Row
				cur = sql_select_comments_from_user(conn_comments,args.user[0],int(args.user[1]))
				rows = cur.fetchall();
				for row in rows:
					print(" Article Title: ", row['article_title'], "\n" , "Article URL: ", row['article_url'], "\n\n" " User Comment: ", row['comment_text'] , "\n")
			except sql.Error as error:
				logging.log(logging.ERROR, "Fatal Error! Comment Table Not Accessible. Exiting!")
		except sql.Error as error:
			logging.log(logging.ERROR, "Fatal Error! Users Table Not Accessible. Exiting!")
	#Use ForEach logic to execute multiple modes in succession.
	if mode:
		mode_execute(mode)
	if args.features:
		logging.log(logging.INFO, "Now computing statistics")
		cur_comments_and_id = db.sql_return_comments_users_hundred(conn_article)
		datad = cur_comments_and_id.fetchall()    
		comment_id_bulk = [d[0] for d in datad]
		comment_text_bulk = [d[1] for d in datad]
		statistics = fmatrix.feature_matrix(comment_text_bulk[:10],comment_id_bulk[:10])
		# pc = pca.execute_pca(statistics)
		# trainer.get_classifiers(pc)
		yes = set(['yes','y', 'ye', ''])
		no = set(['no','n'])
		choice = input('Would you like to execute the dopplegaenger analysis as well?: ').lower()
		if choice in yes:
			#Return list of authors with possible dopplegaenger identities
			#EndlessLoop
			isnumerical()
		elif choice in no:
			return False
		else:
			logging.log(logging.INFO, "Please respond with 'yes' or 'no'")
        	#TODO Pass dictionaries and symbol tables into Matrix
        	# logging.log(logging.INFO, "STATISTIC GENERATION COMPLETE")
    

    
	close_db_connection(conn_article)
	close_db_connection(conn_comments)
	close_db_connection(conn_user)

def isnumerical():
	threshold = input('What is your expected threshold percentage?: ').lower()
	results = []
	if threshold.isnumeric():
		#compare threshold value to 
		pass	
	else:
		logging.log(logging.INFO, "Please only use numeric values")
		isnumerical()
	return results

if __name__== "__main__":
	main()
	time = (time.time() - start_time)
	if time >= 120:
		time = time//60
		logging.log(logging.INFO, "Program completed in --- %s minutes ---" % time)
		print("Program completed in --- %s minutes ---" % time)
	else:
		logging.log(logging.INFO, "Program completed in --- %s seconds ---" % time)
		print("Program completed in --- %s seconds ---" % time)
