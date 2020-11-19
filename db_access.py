#!/usr/bin/python
# Helper Functions to communicate with local database
import logging, flask
import sqlite3 as sql
from flask import g, Flask
from sqlite3 import Error
import logging, flask
from itemadapter import ItemAdapter, is_item

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

def execute_sql(conn, f):
	try:
		c = conn.cursor()
		c.execute(f)
	except Error as e:
		logging.log(logging.ERROR, '%s raised an error on query %s', e, f)

def execute_sql_cursor_expect(conn, f):
	c = None
	try:
		c = conn.cursor()
		c.execute(f)
		return c
	except Error as e:
		logging.log(logging.ERROR, '%s raised an error on query %s', e, f)
	return c	

def create_article_table(conn):
	sql_create_article_table = """ CREATE TABLE IF NOT EXISTS article (
                                    url text PRIMARY KEY,
                                    title text NOT NULL,
                                    author text,
                                    publish_date integer,
                                    comment_count integer
                                ); """
	execute_sql(conn, sql_create_article_table)

def create_user_table(conn):
	sql_create_user_table = """ CREATE TABLE IF NOT EXISTS user (
                                    user_id integer PRIMARY KEY AUTOINCREMENT,
                                    username text NOT NULL UNIQUE
                                ); """
	execute_sql(conn, sql_create_user_table)

def create_comment_table(conn):
	sql_create_comment_table = """ CREATE TABLE IF NOT EXISTS comment (
                                    message_date integer NOT NULL,
                                    article_title text,
                                    message_title text,
									comment text NOT NULL,
									user_id integer NOT NULL,
									FOREIGN KEY (user_id) REFERENCES user (user_id)
                                ); """
	execute_sql(conn, sql_create_comment_table)

def insert_into_article(conn,item):
	adapter = ItemAdapter(item)
	sql_insert_article_table = f'INSERT INTO article (url, author, title, publish_date, comment_count) VALUES ("{adapter["url"]}", "{adapter["author"]}", "{adapter["title"]}", "{adapter["publish_date"]}", "{adapter["comment_count"]}")'
	execute_sql(conn, sql_insert_article_table)

def purge_db(conn):
	sql_purge_article_table = 'DROP TABLE IF EXISTS article;'
	execute_sql(conn, sql_purge_article_table)

def sql_full_report(conn):
	sql_full_report_query = "select url, title, author, datetime(publish_date, 'unixepoch') as date from article"
	return execute_sql_cursor_expect(conn, sql_full_report_query)

def sql_return_row_from_url(conn, url):
	sql_return_url_query = 'SELECT * FROM article WHERE url="{url}"'
	return execute_sql_cursor_expect(conn, sql_return_url_query)

def sql_return_comment_from_id(conn, id):
	sql_return_url_query = 'SELECT * FROM article WHERE id="{id}"'
	return execute_sql_cursor_expect(conn, sql_return_url_query)

def insert_into_comment(conn,item):
	adapter = ItemAdapter(item)
	sql_insert_comment_table = f'INSERT INTO comment (url, author, title, publish_date) VALUES ("{adapter["url"]}", "{adapter["author"]}", "{adapter["title"]}", "{adapter["publish_date"]}")'
	execute_sql(conn, sql_insert_comment_table)

def drop_all(conn):	
	execute_sql(conn, 'DROP TABLE comment')
	execute_sql(conn, 'DROP TABLE user')
	execute_sql(conn, 'DROP TABLE article')
	conn.commit()

def close_db_connection(conn):
	try:
		conn.close()
	except Error as e:
		logging.error('%s close raised an error', e)