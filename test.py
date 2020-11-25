import sqlite3, db_access
from db_access import *
from sqlite3 import Error
def main():
	#Database declaration and connection
    database = r'database/dopplegaenger.db'
    conn_comments = create_connection(database)
    try:
        #Returns a dictionary curstor instead of tuple
        conn_comments.row_factory = sql.Row
        cur = sql_check_username_exist(conn_comments,"Wonkothesane76")
        username_exist = cur.fetchone();  
        if username_exist:
            print("User exists")
        else:
            print("No user found")
        # for user in rows_user:
        #     print("Next User ", user['username'])
        #     logging.log(logging.INFO, "Next User: ", user['username'])
        #     #Returns a dictionary curstor instead of tuple
        #     conn_comments.row_factory = sql.Row
        #     size = 1
        #     cursor = sql_select_comments_from_user(conn_comments,user['username'],size)
        #     rows = cursor.fetchall(); 
        #     for row in rows:
        #         print(row['comment_author_username'], "|" , row['comment_text'], "|" , row['article_title'], "|" , row['article_url'])
            # cur.close()
        # cur.close()
    except sqlite3.Error as error:
        # logging.log(logging.ERROR, "Fatal Error! Database Tables Not Created. Exiting!")
        print("TESTING")
main()