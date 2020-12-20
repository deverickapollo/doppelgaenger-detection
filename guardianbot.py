#!/usr/bin/python
# Main for Dopplegaenger Detection Program
from pprint import pprint

from scrape_guardian import *
from database.db_access import *
import logging, scrapy, os, asyncio, argparse, features.feature_generation as feat, feature_matrix as matrix,subprocess

from logging import FileHandler
from logging import Formatter
from subprocess import Popen, PIPE

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
all_args.add_argument("-f", "--features", help="Start feature generation.", action="store_true")


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
	logging.basicConfig(filename='logs/webapp.log', level=logging.DEBUG, format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
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
			print ("Webapp log doesn't exist")
			logging.log(logging.ERROR, "Error! Webapp log doesn't exist.")
		if os.path.isfile('logs/report.log'):
			open('logs/report.log', 'w').close()
		else:
			print ("Report log doesn't exist")
			logging.log(logging.ERROR, "Error! Report log doesn't exist.")
	if args.version:
		print("GuardianBot version 1.0")
	if args.run:
		if conn_article is not None and conn_comments is not None:
			create_article_table(conn_article)
			create_user_table(conn_article)
			create_comment_table(conn_article)
			create_stats_table(conn_comments)
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
		print("This program allows a user to generate features for a string or a set of strings")
		print("")
		print("Modes: ")
		print("1 - Enter a comment id from the database and genereate a feature vector")
		print("2 - Enter a username from the database and generate feature vectors for a specified number of his comments")
		print("3 - Enter a string and generate a feature vector")
		print("4 - Run full feature analysis")
		x = input("Select Mode: ")
		if x == "1":
			comment_id = input("Enter comment id: ")
			conn_comments.row_factory = sql.Row
			cur = sql_return_comment_from_id(conn_comments, comment_id)
			rows = cur.fetchall();
			for row in rows:
				pprint(matrix.feature_vector(row['comment_text']), sort_dicts=False)
				proc=subprocess.Popen(['python3', 'feature_matrix.py', row['comment_text']], shell=False, stdout=subprocess.PIPE, )
				output=proc.communicate()[0]
				print(output)
				print("\n------\n")
		if x == "2":
			username = input("Enter username: ")
			number = input("Enter number of comments: ")
			conn_comments.row_factory = sql.Row
			cur = sql_select_comments_from_user(conn_comments, username, number)
			rows = cur.fetchall();
			for row in rows:
				pprint(matrix.feature_vector(row['comment_text']), sort_dicts=False)
				print("\n------\n")
		if x == "3":
			string = input("Enter string: ")
			pprint(matrix.feature_matrix(string), sort_dicts=False)
		if x == "4":
			conn_comments.row_factory = sql.Row
			cur = sql_select_all_comments(conn_comments)
			rows = cur.fetchall()
			llist = []
			covariance = {}
			#Here we will calculate the covariance for each the full database so we have a mean for each of the features
			for row in rows:
				llist.append(matrix.feature_vector(row['comment_text']))
				pprint(row[0])
				
	close_db_connection(conn_article)
	close_db_connection(conn_comments)
	close_db_connection(conn_user)
	
if __name__== "__main__":
	main()
	time = (time.time() - start_time)
	if time >= 120:
		time = time//60
	logging.log(logging.INFO, "--- %s seconds ---" % time)
	print("--- %s seconds ---" % time)
