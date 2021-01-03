#!/usr/bin/python
# Helper Functions to communicate with local database
import logging, flask
import sqlite3 as sql
from flask import g, Flask
from sqlite3 import Error
import logging, flask
from itemadapter import ItemAdapter

app = Flask(__name__)

#Used for webserver. Provided by Flask. Investigate g and determine if we can replace with create_connection
def get_db(database):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect(database,detect_types=sql.PARSE_DECLTYPES)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def create_connection(db_file):
	conn = None
	try:
		conn = sql.connect(db_file,detect_types=sql.PARSE_DECLTYPES)
		return conn
	except Error as e:
		logging.error('%s raised an error', e)
	return conn

def close_db_connection(conn):
	try:
		conn.close()
	except Error as e:
		logging.error('%s close raised an error', e)

def execute_sql(conn, f):
	c = None
	try:
		c = conn.cursor()
		c.execute(f)
	except Error as e:
		logging.log(logging.ERROR, '%s raised an error on query %s', e, f)
	return c

def execute_sql_param(conn, f,param):
	c = None
	try:
		c = conn.cursor()
		c.execute(f,param)
	except Error as e:
		logging.log(logging.ERROR, '%s raised an error on query %s', e, f)
	return c

def create_article_table(conn):
	sql_create_article_table = """ CREATE TABLE IF NOT EXISTS article (
                                    url text PRIMARY KEY,
                                    title text NOT NULL,
                                    author text,
                                    publish_date text,
                                    comment_count integer
                                ); """
	execute_sql(conn, sql_create_article_table)

def create_user_table(conn):
	sql_create_user_table = """ CREATE TABLE IF NOT EXISTS user (
                                    user_id integer PRIMARY KEY,
                                    username text NOT NULL UNIQUE
                                ); """
	execute_sql(conn, sql_create_user_table)

def create_comment_table(conn):
	sql_create_comment_table = """ CREATE TABLE IF NOT EXISTS comment (
									comment_id integer PRIMARY KEY,
									comment_text text,
									comment_date text,
									comment_author_id integer,
									comment_author_username text,
									article_url text,
									article_title text,
									FOREIGN KEY (comment_author_id) REFERENCES user (user_id)
                                ); """
	execute_sql(conn, sql_create_comment_table)

# def create_stats_table(conn):
# 	sql_create_stats_table = """ CREATE TABLE IF NOT EXISTS stats (
# 									stat_id integer PRIMARY KEY,
# 									character_frequency_letters integer,
# 									character_frequency_digits integer,
# 									character_frequency_special_characters integer,
# 									character_frequency integer,
# 									word_length_distribution integer,
# 									word_frequency integer,
# 									number_big_words integer,
# 									hapax_legomena integer,
# 									hapax_dislegomena integer,
# 									yules_k integer,
# 									brunets_w integer,
# 									honores_r integer,
# 									average_number_characters_sentence integer,
# 									average_number_lowercase_letters_sentence integer,
# 									average_number_uppercase_letters_sentence integer,
# 									average_number_digits_sentence integer,
# 									average_number_words_sentence integer,
# 									total_number_words_sentence integer,
# 									punctuation_frequency integer,
# 									punctuation_frequency_sentence integer,
# 									repeated_whitespace integer,
# 									repeated_whitespace_sentence integer,
# 									uppercase_words integer,
# 									uppercase_words_sentence integer,
# 									grammarCheck integer,
# 									grammarCheck_sentence integer,
# 									sentiment_analysis_word_average integer,
# 									sentiment_analysis_sentence_average integer,
# 									emoji_frequency_word integer,
# 									emoji_frequency_sentence integer,
# 									get_language integer,
# 									all_capital_words integer,
# 									all_capital_words_sentence integer,
# 									type_token_ratio integer,
# 									mean_word_frequency integer,
# 									sichels_s integer,
# 									FOREIGN KEY (stat_id) REFERENCES comment (comment_id)
#                                 ); """
# 	execute_sql(conn, sql_create_stats_table)

def create_stats_table(conn):
	sql_create_stats_table = """ CREATE TABLE IF NOT EXISTS stats (
									stat_id integer PRIMARY KEY,
									jsondump text,
									FOREIGN KEY (stat_id) REFERENCES comment (comment_id)
                                ); """
	execute_sql(conn, sql_create_stats_table)

def insert_into_article(conn,item):
	adapter = ItemAdapter(item)
	sqlite_insert_with_param = """INSERT INTO article
							(url, author, title, publish_date, comment_count) 
							VALUES (?, ?, ?, ?, ? );"""
	data_tuple = (adapter["url"], adapter["author"], adapter["title"], adapter["publish_date"], adapter["comment_count"])
	execute_sql_param(conn, sqlite_insert_with_param, data_tuple)

def insert_into_comment(conn,item):
	adapter = ItemAdapter(item)
	sqlite_insert_with_param = """INSERT OR REPLACE INTO comment
							(comment_id, comment_text, comment_date, comment_author_id, comment_author_username,article_url,article_title) 
							VALUES (?, ?, ?, ?, ?, ?, ?);"""
	data_tuple = (adapter["comment_id"], adapter["comment_text"], adapter["comment_date"], adapter["comment_author_id"], adapter["comment_author_username"],adapter["article_url"],adapter["article_title"])
	execute_sql_param(conn, sqlite_insert_with_param, data_tuple)

def insert_into_user(conn,item):
	adapter = ItemAdapter(item)
	sqlite_insert_with_param = """INSERT INTO user
							(user_id, username) 
							VALUES (?, ?);"""
	data_tuple = (adapter["comment_author_id"], adapter["comment_author_username"])
	logging.log(logging.INFO, 'Inserting user %s with user_id %s into user table', adapter["comment_author_username"], adapter["comment_author_id"])
	execute_sql_param(conn, sqlite_insert_with_param, data_tuple)

def insert_into_stats(conn, comment_id, statistics):
	adapter = ItemAdapter(statistics)
	sqlite_insert_with_param = """INSERT OR REPLACE INTO stats
							(stat_id, character_frequency_letters, character_frequency_digits, character_frequency_special_characters, character_frequency,word_length_distribution,word_frequency,number_big_words,\
							hapax_legomena,hapax_dislegomena,yules_k,brunets_w,honores_r,average_number_characters_sentence, average_number_lowercase_letters_sentence,average_number_uppercase_letters_sentence,\
							average_number_digits_sentence,average_number_words_sentence,total_number_words_sentence,punctuation_frequency,punctuation_frequency_sentence,repeated_whitespace,repeated_whitespace_sentence,\
							uppercase_words,uppercase_words_sentence,grammarCheck,grammarCheck_sentence,sentiment_analysis_word_average,sentiment_analysis_sentence_average,emoji_frequency_word,emoji_frequency_sentence,\
							get_language, all_capital_words,all_capital_words_sentence, type_token_ratio, mean_word_frequency, sichels_s) 
							VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );"""

	data_tuple =(comment_id, adapter["character_frequency_letters"], adapter["character_frequency_digits"], adapter["character_frequency_special_characters"], adapter["character_frequency"],adapter["word_length_distribution"],adapter["word_frequency"],\
				adapter["number_big_words"], adapter["hapax_legomena"], adapter["hapax_dislegomena"], adapter["yules_k"], adapter["brunets_w"],adapter["honores_r"],adapter["average_number_characters_sentence"],\
				adapter["average_number_lowercase_letters_sentence"], adapter["average_number_uppercase_letters_sentence"], adapter["average_number_digits_sentence"], adapter["average_number_words_sentence"], adapter["total_number_words_sentence"],adapter["punctuation_frequency"],adapter["punctuation_frequency_sentence"],\
				adapter["repeated_whitespace"], adapter["repeated_whitespace_sentence"], adapter["uppercase_words"], adapter["uppercase_words_sentence"], adapter["grammarCheck"],adapter["grammarCheck_sentence"],adapter["sentiment_analysis_word_average"],\
				adapter["sentiment_analysis_sentence_average"], adapter["emoji_frequency_word"], adapter["emoji_frequency_sentence"], adapter["get_language"], adapter["all_capital_words"],adapter["all_capital_words_sentence"],adapter["type_token_ratio"],\
				adapter["mean_word_frequency"], adapter["sichels_s"])
	execute_sql_param(conn, sqlite_insert_with_param, data_tuple)

def insert_stat_horrorshow(conn, comment_id, statistics):
	sqlite_insert_with_param = """INSERT OR REPLACE INTO stats
							(stat_id, jsondump) 
							VALUES (?,?);"""
	data_tuple =(comment_id, str(statistics))
	execute_sql_param(conn, sqlite_insert_with_param, data_tuple)

def insert_available_into_stats(conn, comment_id, statistics):
	adapter = ItemAdapter(statistics)
	sqlite_insert_with_param = """INSERT OR REPLACE INTO stats
							(stat_id, character_frequency_letters, character_frequency_digits, character_frequency_special_characters, character_frequency,word_length_distribution,word_frequency,number_big_words,\
							hapax_legomena,hapax_dislegomena,yules_k,brunets_w,honores_r,average_number_characters_sentence, average_number_lowercase_letters_sentence,average_number_uppercase_letters_sentence,\
							average_number_digits_sentence,average_number_words_sentence,total_number_words_sentence,punctuation_frequency,punctuation_frequency_sentence,repeated_whitespace,repeated_whitespace_sentence,\
							uppercase_words,uppercase_words_sentence,grammarCheck,grammarCheck_sentence,sentiment_analysis_word_average,sentiment_analysis_sentence_average,emoji_frequency_word,emoji_frequency_sentence,\
							get_language, all_capital_words,all_capital_words_sentence, type_token_ratio, mean_word_frequency, sichels_s) 
							VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? );"""

	data_tuple =(comment_id, adapter["character_frequency_letters"], adapter["character_frequency_digits"], adapter["character_frequency_special_characters"], adapter["character_frequency"],adapter["word_length_distribution"],adapter["word_frequency"],\
				adapter["number_big_words"], adapter["hapax_legomena"], adapter["hapax_dislegomena"], adapter["yules_k"], adapter["brunets_w"],adapter["honores_r"],adapter["average_number_characters_sentence"],\
				adapter["average_number_lowercase_letters_sentence"], adapter["average_number_uppercase_letters_sentence"], adapter["average_number_digits_sentence"], adapter["average_number_words_sentence"], adapter["total_number_words_sentence"],adapter["punctuation_frequency"],adapter["punctuation_frequency_sentence"],\
				adapter["repeated_whitespace"], adapter["repeated_whitespace_sentence"], adapter["uppercase_words"], adapter["uppercase_words_sentence"], adapter["grammarCheck"],adapter["grammarCheck_sentence"],adapter["sentiment_analysis_word_average"],\
				adapter["sentiment_analysis_sentence_average"], adapter["emoji_frequency_word"], adapter["emoji_frequency_sentence"], adapter["get_language"], adapter["all_capital_words"],adapter["all_capital_words_sentence"],adapter["type_token_ratio"],\
				adapter["mean_word_frequency"], adapter["sichels_s"])
	execute_sql_param(conn, sqlite_insert_with_param, data_tuple)

def sql_full_report(conn):
	sql_full_report_query = """SELECT url, title, author, publish_date AS date, comment_count FROM article;"""
	return execute_sql(conn, sql_full_report_query)

def sql_return_row_from_url(conn, url):
	sql_return_comment_query = """SELECT * FROM article WHERE url=?;"""
	data_tuple = (url,)
	return execute_sql_param(conn, sql_return_comment_query,data_tuple)

def sql_check_userid_exist(conn, id):
	sql_return_comment_query = """SELECT * FROM user WHERE user_id=?;"""
	data_tuple = (id,)
	return execute_sql_param(conn, sql_return_comment_query,data_tuple)

def sql_check_username_exist(conn, username):
	sql_return_username_query = """SELECT * FROM user WHERE username= ?;"""
	data_tuple = (username,)
	return execute_sql_param(conn, sql_return_username_query,data_tuple)

def sql_check_comment_exist(conn, comment_id):
	sql_return_comment_query = """SELECT * FROM comment WHERE comment_id= ?;"""
	data_tuple = (comment_id,)
	return execute_sql_param(conn, sql_return_comment_query,data_tuple)

def sql_check_stat_exist(conn, stat_id):
	sql_return_comment_query = """SELECT * FROM stats WHERE stat_id= ?;"""
	data_tuple = (stat_id,)
	return execute_sql_param(conn, sql_return_comment_query,data_tuple)

def sql_return_comment_from_id(conn, id):
	sql_return_comment_query = """SELECT * FROM comment WHERE comment_id=?;"""
	data_tuple = (id,)
	return execute_sql_param(conn, sql_return_comment_query,data_tuple)

def sql_return_comments_from_title(conn, title):
	sql_return_comment_query = """SELECT * FROM comment WHERE article_title=?;"""
	data_tuple = (title,)
	return execute_sql_param(conn, sql_return_comment_query,data_tuple)

def sql_select_comments_from_user(conn, user,row_count):
	sql_return_comment_query = """SELECT comment_author_username, comment_text, article_title, article_url FROM comment WHERE comment_author_username= ? ORDER BY comment_author_username LIMIT ? ;"""
	data_tuple = (user,row_count,)
	return execute_sql_param(conn, sql_return_comment_query,data_tuple)

def sql_select_all_comments_from_user(conn, user):
	sql_return_comment_query = """SELECT comment_author_username, comment_text, article_title, article_url, comment_date FROM comment WHERE comment_author_username= ? ORDER BY comment_author_username ;"""
	data_tuple = (user,)
	return execute_sql_param(conn, sql_return_comment_query,data_tuple)
	
def sql_select_all_comments(conn):
	sql_return_comment_query = """SELECT comment_text FROM comment;"""
	return execute_sql(conn,sql_return_comment_query)

def sql_select_all_users(conn):
	sql_select_all_users_query = """SELECT username FROM user;"""
	return execute_sql(conn, sql_select_all_users_query)

def select_all_stats(conn):
	sql_select_all_stats = """SELECT * FROM stats;"""
	return execute_sql(conn, sql_select_all_stats)
	
def sql_count_articles(conn):
	sql_count_articles_query = """SELECT COUNT(*) FROM article;"""
	return execute_sql(conn, sql_count_articles_query)

def sql_count_users(conn):
	sql_count_users_query = """SELECT COUNT(*) FROM user;"""
	return execute_sql(conn, sql_count_users_query)

def sql_count_comments(conn):
	sql_count_comments_query = """SELECT COUNT(*) FROM comment;"""
	return execute_sql(conn, sql_count_comments_query)

def sql_count_stats(conn):
	sql_count_stats_query = """SELECT COUNT(*) FROM stats;"""
	return execute_sql(conn, sql_count_stats_query)

def sql_delete_username(conn, username):
	sql_return_comment_query = """DELETE FROM user WHERE username= ?;"""
	data_tuple = (username,)
	return execute_sql_param(conn, sql_return_comment_query,data_tuple)

def sql_delete_userid(conn, user_id):
	sql_return_comment_query = """DELETE FROM user WHERE user_id= ?;"""
	data_tuple = (user_id,)
	return execute_sql_param(conn, sql_return_comment_query,data_tuple)

def sql_delete_stat_by_id(conn, stat_id):
	sql_return_stats_query = """DELETE FROM stats WHERE stat_id= ?;"""
	data_tuple = (stat_id,)
	return execute_sql_param(conn, sql_return_stats_query,data_tuple)

def sql_delete_comments_by_comment_id(conn, comment_id):
	sql_return_comments_query = """DELETE FROM comment WHERE comment_id= ?;"""
	data_tuple = (comment_id,)
	return execute_sql_param(conn, sql_return_comments_query,data_tuple)

def sql_delete_comments_by_comment_author_id(conn, comment_author_id):
	sql_return_comments_query = """DELETE FROM comment WHERE comment_author_id= ?;"""
	data_tuple = (stat_id,)
	return execute_sql_param(conn, sql_return_comments_query,data_tuple)

def sql_delete_comments_by_comment_author_username(conn, comment_author_username):
	sql_return_comments_query = """DELETE FROM comment WHERE comment_author_username= ?;"""
	data_tuple = (comment_author_username,)
	return execute_sql_param(conn, sql_return_comments_query,data_tuple)

# return all comments by users which have at least 100 comments
def sql_return_comments_users_hundred(conn):
	sql_return_comments_users_hundred_query = """SELECT * FROM comment c JOIN ( SELECT comment_author_id FROM comment GROUP BY comment_author_id HAVING COUNT(*) > 99 ) b on c.comment_author_id = b.comment_author_id ORDER BY comment_author_id;"""
	return execute_sql(conn, sql_return_comments_users_hundred_query)

def drop_all(conn):	
	execute_sql(conn, 'DROP TABLE IF EXISTS comment')
	execute_sql(conn, 'DROP TABLE IF EXISTS user')
	execute_sql(conn, 'DROP TABLE IF EXISTS article')
	execute_sql(conn, 'DROP TABLE IF EXISTS stats')
	

def check_table(conn,table):
	sql_verify = """SELECT name FROM sqlite_master WHERE type='table' AND name=?;"""
	data_tuple = (table,)
	return execute_sql_param(conn,sql_verify,data_tuple)