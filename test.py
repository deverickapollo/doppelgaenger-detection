import sqlite3, db_access, feature_generation, logging, pytest
from db_access import *

#Debug Log
logging.basicConfig(level=logging.DEBUG, format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
mylogger = logging.getLogger()

def test_py():
      x=5
      y=6
      assert x+1 == y,"test failed"

def test_insert_and_verify_user():
    #Database declaration and connection
    database = r'database/dopplegaenger.db'
    conn = create_connection(database)
    #Returns a dictionary cursor instead of tuple
    conn.row_factory = sql.Row
    thisdict = {
    "comment_author_id": 999999999,
    "comment_author_username": "monero"
    }
    mylogger.log(logging.DEBUG, "User ID: %s and  Username: %s", str(thisdict["comment_author_id"]), str(thisdict["comment_author_username"]))
    insert_into_user(conn,thisdict)
    conn.commit()
    cur = sql_check_username_exist(conn,"monero")
    username_exist = cur.fetchone();  
    mylogger.log(logging.DEBUG, "user exist %s", username_exist)
    assert username_exist,"test failed"
    close_db_connection(conn)
def test_