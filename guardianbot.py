#!/usr/bin/python
# Main for Dopplegaenger Detection Program
import pickle
from datetime import datetime

import database.db_access as db
from pprint import pprint

from scrape_guardian import *
from database.db_access import *
import logging, os, argparse, features.feature_generation as feat
import features.principal_component_analysis as pca, features.train_classifiers as trainer

from logging import FileHandler
from logging import Formatter

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.settings import Settings

import numpy as np
import time

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
all_args.add_argument("-e", "--experiments", help="Run the experiments from the fourth tash sheet", action="store_true")


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
	#TODO Use ForEach logic to execute multiple modes in succession.
	if mode:
		mode_execute(mode)
	if args.features:
		logging.log(logging.INFO, "Now computing statistics")
		cur_comments_and_id = db.sql_return_comments_users_hundred(conn_article)
		datad = cur_comments_and_id.fetchall()
		comment_id_bulk = [d[0] for d in datad]
		comment_article_id_bulk = [d[5] for d in datad]
		comment_user_id_bulk = [d[3] for d in datad]
		comment_text_bulk = [d[1] for d in datad]

		# comment first four lines of this block if feature matrix should be loaded from file
		# comment last two lines of this block if feature matrix should be computed new
		#statistics = fmatrix.feature_matrix(comment_text_bulk[:100],comment_user_id_bulk[:100],comment_id_bulk[:100],comment_article_id_bulk[:100])
		#f = open("data.pkl", "wb")
		#pickle.dump(statistics, f)
		#f.close()
		f = open("data.pkl", "rb")
		statistics = pickle.load(f)
		pc = pca.execute_pca(statistics)
		pc = trainer.get_matrix_experiment_one(pc, users=4, text_length=500)

		pc = trainer.split_user_accounts(pc)
		pcs =  trainer.k_fold_cross_validation(pc, 3)

		yes = set(['yes','y', 'ye', ''])
		no = set(['no','n'])
		choice = input('Would you like to execute the dopplegaenger analysis as well?: ').lower()
		if choice in yes:
			#EndlessLoop until value submitted	
			mode = input('Which mode would you like to use; average, multiplication, squaredaverage: ').lower()
			#Return list of authors with possible dopplegaenger identities
			modelist = set(['average', 'multiplication', 'squaredaverage'])
			results= []
			if mode in modelist:
				for p in pcs:
					r = trainer.dopplegeanger_detection(p, mode)
					#r = trainer.dopplegaenger_detection_euclid(pc, 1)
					results.append(r)
					for row in r:
						print(row)
			else:
				logging.log(logging.INFO, "Please select either: average, multiplication, squaredaverage")
		elif choice in no:
			pass
		else:
			logging.log(logging.INFO, "Please respond with 'yes' or 'no'")
        	#TODO Pass dictionaries and symbol tables into Matrix
	if args.experiments:
		f = open("data.pkl", "rb")
		statistics = pickle.load(f)
		pc = pca.execute_pca(statistics)

		mode = input('Which mode would you like to use to compute the pairwise probability; average, multiplication, squaredaverage: ').lower()
		model = input('Which machine learning model would you like to use; svc, randomforest, knearestneighbors: ').lower()
		split_mode = input('Which split mode would you like to use; i, ii, iii, iv: ').lower()

		users = 5

		## Task 2 a) Experiment 1
		print("\n===== Executing Task 2 a) Experiment 1 =====")
		experiment_matrix = trainer.get_matrix_experiment_one(pc, users, text_length=250)
		experiment_matrix_split = trainer.split_user_accounts(experiment_matrix, split_mode)
		experiment_matrix_split_kfold = trainer.k_fold_cross_validation(experiment_matrix_split, 3)
		results = []

		for emsk in experiment_matrix_split_kfold:
			r = trainer.dopplegeanger_detection(emsk, mode, model)
			results.append(r)
		results = np.concatenate(results, axis=0)
		tfpn = trainer.get_number_true_false_positive_negative(results)
		print("Total numbers true/false positives/negatives: ")
		print(tfpn)
		cm = [[tfpn["true_positive"],tfpn["false_positive"]],[tfpn["false_negative"],tfpn["true_negative"]]]
		trainer.plot_heatmap(cm,"Task 2a ex1")
		f = open("2a_experiment_1.pkl", "wb")
		pickle.dump([results, tfpn], f)
		f.close()
	
		## Task 2 a) Experiment 2
		print("\n===== Executing Task 2 a) Experiment 2 =====")
		experiment_matrix = trainer.get_matrix_experiment_one(pc, users, text_length=500)
		experiment_matrix_split = trainer.split_user_accounts(experiment_matrix, split_mode)
		experiment_matrix_split_kfold = trainer.k_fold_cross_validation(experiment_matrix_split, 3)
		results = []
		for emsk in experiment_matrix_split_kfold:
			r = trainer.dopplegeanger_detection(emsk, mode, model)
			results.append(r)
		results = np.concatenate(results, axis=0)
		tfpn = trainer.get_number_true_false_positive_negative(results)
		print("Total numbers true/false positives/negatives: ")
		print(tfpn)
		cm = [[tfpn["true_positive"],tfpn["false_positive"]],[tfpn["false_negative"],tfpn["true_negative"]]]
		trainer.plot_heatmap(cm,"Task 2 ex 2")
		f = open("2a_experiment_2.pkl", "wb")
		pickle.dump([results, tfpn], f)
		f.close()

		## Task 2 a) Experiment 3
		print("\n===== Executing Task 2 a) Experiment 3 =====")
		experiment_matrix = trainer.get_matrix_experiment_one(pc, users, text_length=750)
		experiment_matrix_split = trainer.split_user_accounts(experiment_matrix, split_mode)
		experiment_matrix_split_kfold = trainer.k_fold_cross_validation(experiment_matrix_split, 3)
		results = []
		for emsk in experiment_matrix_split_kfold:
			r = trainer.dopplegeanger_detection(emsk, mode, model)
			results.append(r)
		results = np.concatenate(results, axis=0)
		tfpn = trainer.get_number_true_false_positive_negative(results)
		print("Total numbers true/false positives/negatives: ")
		print(tfpn)
		cm = [[tfpn["true_positive"],tfpn["false_positive"]],[tfpn["false_negative"],tfpn["true_negative"]]]
		trainer.plot_heatmap(cm,"Task 2a ex 3")		
		f = open("2a_experiment_3.pkl", "wb")
		pickle.dump([results, tfpn], f)
		f.close()

		## Task 2 b) Experiment 1-3
		experiment_matrices = trainer.get_matrix_experiment_two(pc)
		i = 1
		for exm in experiment_matrices:
			print("\n===== Executing Task 2 b) Experiment " + str(i) + " =====")
			exm_split = trainer.split_user_accounts(exm, split_mode)
			exm_split_kfold = trainer.k_fold_cross_validation(exm_split, 3)
			results = []
			for emsk in exm_split_kfold:
				r = trainer.dopplegeanger_detection(emsk, mode, model)
				results.append(r)
			results = np.concatenate(results, axis=0)
			tfpn = trainer.get_number_true_false_positive_negative(results)
			print("Total numbers true/false positives/negatives: ")
			print(tfpn)
			cm = [[tfpn["true_positive"],tfpn["false_positive"]],[tfpn["false_negative"],tfpn["true_negative"]]]
			title = "Task 2b ex " + str(i)
			trainer.plot_heatmap(cm,title)			
			f = open("2b_experiment_" + str(i) + ".pkl", "wb")
			pickle.dump([results, tfpn], f)
			f.close()
			i += 1


		## Task 3 a)
		print("\n===== Executing Task 3 a) =====")
		threshold_euclid = input('Select threshold for Euclid: ')
		expirment_matrix = trainer.get_matrix_experiment_one(pc, users, text_length=750)
		expirment_matrix_split = trainer.split_user_accounts(expirment_matrix, split_mode)
		r = trainer.dopplegaenger_detection_euclid(expirment_matrix_split, threshold=float(threshold_euclid))
		tfpn = trainer.get_number_true_false_positive_negative(r)
		print("Total numbers true/false positives/negatives: ")
		print(tfpn)
		print(len(r))
		cm = [[tfpn["true_positive"],tfpn["false_positive"]],[tfpn["false_negative"],tfpn["true_negative"]]]
		trainer.plot_heatmap(cm,"Task 3a")	
		f = open("3a_experiment.pkl", "wb")
		pickle.dump([r, tfpn], f)
		f.close()

		## Task 3 b)
		print("\n===== Executing Task 3 b)====")
		expirment_matrix = trainer.get_matrix_experiment_one(pc, users, text_length=750)
		expirment_matrix_split = trainer.split_user_accounts(expirment_matrix, split_mode)
		expirment_matrix_split_kfold = trainer.k_fold_cross_validation(expirment_matrix_split, 3)
		results = []
		for emsk in expirment_matrix_split_kfold:
			print("==== Executing Three Fold Cross Valication")
			threshold = trainer.get_optimal_distance_euclid(emsk[0])
			r = trainer.dopplegaenger_detection_euclid(emsk[1], threshold)
			results.append(r)
		results = np.concatenate(results, axis=0)
		tfpn = trainer.get_number_true_false_positive_negative(results)
		print("Total numbers true/false positives/negatives: ")
		print(tfpn)
		cm = [[tfpn["true_positive"],tfpn["false_positive"]],[tfpn["false_negative"],tfpn["true_negative"]]]
		trainer.plot_heatmap(cm,"Task 3b")	
		f = open("3b_experiment.pkl", "wb")
		pickle.dump([results, tfpn], f)
		f.close()
		#Close writing to PDF after calling plot_heatmap
		trainer.closepdf()
	# TODO Pass dictionaries and symbol tables into Matrix
	close_db_connection(conn_article)
	close_db_connection(conn_comments)
	close_db_connection(conn_user)

def is_number(n):
    is_number = True
    try:
        num = float(n)
        # check for "nan" floats
        is_number = num == num  
    except ValueError:
        is_number = False
    return is_number

def isnumerical():
	threshold = input('What is your expected threshold percentage?: ').lower()
	if is_number(threshold) is not True:
		logging.log(logging.INFO, "Please only use decimal values(0-1)")
		isnumerical()
	return threshold

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
