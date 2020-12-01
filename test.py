import sqlite3, db_access, feature_generation as feat, logging, pytest
from db_access import *

#Debug Log
logging.basicConfig(level=logging.DEBUG, format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
mylogger = logging.getLogger()

raw_comment = "1. Here is sample 23424, comment of language used to test 0 functions found in our feature generation file.  2. This is purely for test purposes  .  Test, Repeat. 1, 2 3 ,434, 4 "
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
    sql_delete_username(conn,"monero")
    conn.commit()
    close_db_connection(conn)

def test_letter_frequency():
    freq = feat.character_frequency_letters(raw_comment);
    freq_compare = {'H': 1, 'e': 18, 'r': 7, 'i': 7, 's': 11, 'a': 6, 'm': 3, 'p': 5, 'l': 4, 'c': 2, 'o': 9, 'n': 8, 't': 11, 'f': 6, 'g': 3, 'u': 8, 'd': 2, 'T': 2, 'h': 1, 'y': 1, 'R': 1}
    mylogger.log(logging.DEBUG, "Char frequency is %s", freq)
    assert freq == freq_compare, "test failed"  

def test_letter_frequency_fail():
    freq = feat.character_frequency_letters(raw_comment);
    freq_compare = {'H': 1, 'e': 190, 'r': 7, 'i': 7, 's': 11, 'a': 7, 'm': 3, 'p': 5, 'l': 4, 'c': 2, 'o': 9, 'n': 8, 't': 11, 'f': 6, 'g': 3, 'u': 8, 'd': 2, 'T': 2, 'h': 1, 'y': 1, 'R': 1}
    assert freq != freq_compare, "test failed"  

def test_digit_frequency():
    freq = feat.character_frequency_digits(raw_comment);
    freq_compare = {'1': 2, '2': 4, '3': 3, '4': 5, '0': 1}
    assert freq == freq_compare, "test failed"

#VERIFY
def test_individual_char_frequency():
    freq = feat.character_frequency(raw_comment);
    freq_compare = {1: 16, 4: 8, 2: 5, 6: 3, 5: 2, 7: 2, 8: 2, 9: 1, 3: 2, 10: 1}
    mylogger.log(logging.DEBUG, "Char frequency is %s", freq)
    assert freq == freq_compare, "test failed"  

def test_individual_char_frequency():
    freq = feat.word_length_distribution(raw_comment);
    freq_compare = {'H': 1, 'e': 190, 'r': 7, 'i': 7, 's': 11, 'a': 7, 'm': 3, 'p': 5, 'l': 4, 'c': 2, 'o': 9, 'n': 8, 't': 11, 'f': 6, 'g': 3, 'u': 8, 'd': 2, 'T': 2, 'h': 1, 'y': 1, 'R': 1}
    mylogger.log(logging.DEBUG, "Word Distribution is %s", freq)
    assert freq != freq_compare, "test failed" 