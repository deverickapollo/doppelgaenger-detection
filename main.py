#!/usr/bin/python
# Main File for the Dopplegaenger Detection Program
# Execute: pyhon3 main.py
from create_db import *
from scrape_guardian import *

def main():
	database = r'database/dopplegaenger.db'
	conn = create_connection(database)


	if conn is not None:
		create_guardian_table(conn)
		runSpider()
		close_connection(conn)
	else:
		print("Error! Database Tables Not Created.")

if __name__ == '__main__':
	main()