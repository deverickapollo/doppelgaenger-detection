#!/usr/bin/python
# Helper Functions to communicate with local database
import sqlite3
from sqlite3 import Error
import logging

def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
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
		logging.error('%s raised an error', e)

def create_guardian_table(conn):
	sql_create_guardian_table = """ CREATE TABLE IF NOT EXISTS guardian (
                                    url text PRIMARY KEY,
                                    title text NOT NULL,
                                    author text,
                                    publish_date text,
                                    publish_time text
                                ); """
	sql_set_unique_index = """ CREATE UNIQUE INDEX url_idx ON guardian (url); """
	execute_sql(conn, sql_create_guardian_table)
	execute_sql(conn, sql_set_unique_index)

def insert_into_guardian(conn,item):

	sql_insert_guardian_table = """INSERT INTO guardian (url, author, title, publish_date, publish_time) VALUES (?, ?, ?, ?, ?)", (item[url],item[author],item[title],item[publish_date], item[publish_time])"""

	execute_sql(conn, sql_insert_guardian_table)

def purge_db(conn):
	sql_purge_guardian_table = """ DROP TABLE IF EXISTS guardian;"""
	execute_sql(conn, sql_purge_guardian_table)

def select_url(conn):
	sql_select_url = """ SELECT * FROM guardian;"""
	execute_sql(conn, sql_select_url)

def close_connection(conn):
	try:
		conn.close()
	except Error as e:
		logging.error('%s raised an error', e)