#!/usr/bin/python
# Helper Functions to communicate with local database
import sqlite3
from sqlite3 import Error
import logging

def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file,detect_types=sqlite3.PARSE_DECLTYPES)
		return conn
	except Error as e:
		logging.error('%s raised an error', e)

	return conn

def execute_sql(conn, f):
	try:
		c = conn.cursor()
		c.execute(f)
		conn.commit()
	except Error as e:
		logging.log(logging.ERROR, '%s raised an error', e)

def create_article_table(conn):
	sql_create_article_table = """ CREATE TABLE IF NOT EXISTS article (
                                    url text PRIMARY KEY,
                                    title text NOT NULL,
                                    author text,
                                    publish_date integer
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
									FOREIGN KEY (user_id)
										REFERENCES user (user_id)
                                ); """
	#add a drop tables before creating table
	#DROP TABLE suppliers;
	execute_sql(conn, sql_create_comment_table)

def insert_into_article(conn,item):
	sql_insert_article_table = """INSERT INTO article (url, author, title, publish_date) VALUES (?, ?, ?, ?)", (item[url],item[author],item[title],item[publish_date])"""

	execute_sql(conn, sql_insert_article_table)

def purge_db(conn):
	sql_purge_article_table = """ DROP TABLE IF EXISTS article;"""
	execute_sql(conn, sql_purge_article_table)

def select_article_url(conn):
	sql_article_select_url = """ SELECT * FROM article;"""
	execute_sql(conn, sql_article_select_url)

def close_db_connection(conn):
	try:
		conn.close()
	except Error as e:
		logging.error('%s raised an error', e)