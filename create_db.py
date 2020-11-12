#!/usr/bin/python
# Helper Functions to communicate with local database

import sqlite3
from sqlite3 import Error
import json


def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)
	return conn

def create_table_template(conn, create_table_sql):
	try:
		c = conn.cursor()
		c.execute(create_table_sql)
	except Error as e:
		print(e)

def create_guardian_table(conn):
	sql_create_guardian_table = """ CREATE TABLE IF NOT EXISTS guardian (
                                    id integer PRIMARY KEY,
                                    title text NOT NULL,
                                    url text NOT NULL,
                                    author text,
                                    publish_date text,
                                    publish_time text
                                ); """

	create_table_template(conn, sql_create_guardian_table)

def insert_into_guardian(conn,website):
	conn.execute("INSERT INTO guardian (ID,TITLE,URL,AUTHOR,PUBLISH_DATE,PUBLISH_TIME) \
      VALUES (website.id, website.title, website.url, website.author, website.publish_date, website.publish_time)");


def close_connection(conn):
	try:
		conn.close()
	except Error as e:
		print(e)