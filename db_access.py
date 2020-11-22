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

def insert_into_article(conn,item):
	adapter = ItemAdapter(item)
	sqlite_insert_with_param = """INSERT INTO article
							(url, author, title, publish_date, comment_count) 
							VALUES (?, ?, ?, ?,?);"""
	data_tuple = (adapter["url"], adapter["author"], adapter["title"], adapter["publish_date"], adapter["comment_count"])
	execute_sql_param(conn, sqlite_insert_with_param, data_tuple)

def insert_into_comment(conn,item):
	adapter = ItemAdapter(item)
	sqlite_insert_with_param = """INSERT INTO comment
							(comment_id, comment_text, comment_date, comment_author_id, comment_author_username,article_url,article_title) 
							VALUES (?, ?, ?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE comment_text = ?;"""
	data_tuple = (adapter["comment_id"], adapter["comment_text"], adapter["comment_date"], adapter["comment_author_id"], adapter["comment_author_username"],adapter["article_url"],adapter["article_title"], adapter["comment_text"])
	execute_sql_param(conn, sqlite_insert_with_param, data_tuple)

def insert_into_user(conn,item):
	adapter = ItemAdapter(item)
	sqlite_insert_with_param = """INSERT INTO user
							(user_id, username) 
							VALUES (?, ?);"""
	data_tuple = (adapter["comment_author_id"], adapter["comment_author_username"])
	logging.log(logging.INFO, 'Inserting user %s with user_id %s into user table', adapter["comment_author_id"], adapter["comment_author_username"])
	execute_sql_param(conn, sqlite_insert_with_param, data_tuple)

def sql_full_report(conn):
	sql_full_report_query = """SELECT url, title, author, publish_date AS date FROM article;"""
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
	sql_return_comment_query = """SELECT * FROM user WHERE username= ?;"""
	data_tuple = (username,)
	return execute_sql_param(conn, sql_return_comment_query,data_tuple)

def sql_return_comment_from_id(conn, id):
	sql_return_comment_query = """SELECT * FROM comment WHERE comment_id=?;"""
	data_tuple = (id,)
	return execute_sql_param(conn, sql_return_comment_query,data_tuple)

def sql_select_comments_from_user(conn, user,row_count):
	sql_return_comment_query = """SELECT comment_author_username, comment_text, article_title, article_url FROM comment WHERE comment_author_username= ? ORDER BY comment_author_username LIMIT ? ;"""
	data_tuple = (user,row_count,)
	return execute_sql_param(conn, sql_return_comment_query,data_tuple)

def sql_select_all_users(conn):
	sql_select_all_users_query = """SELECT username FROM user;"""
	return execute_sql(conn, sql_select_all_users_query)

def drop_all(conn):	
	execute_sql(conn, 'DROP TABLE IF EXISTS comment')
	execute_sql(conn, 'DROP TABLE IF EXISTS user')
	execute_sql(conn, 'DROP TABLE IF EXISTS article')
	conn.commit()

