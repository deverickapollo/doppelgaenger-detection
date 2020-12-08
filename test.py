import sqlite3, database.db_access as db, features.feature_generation as feat, logging, pytest, features.leetalpha as alpha
from database.db_access import *
from fractions import Fraction
#Debug Log
logging.basicConfig(level=logging.DEBUG, format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
mylogger = logging.getLogger()
# mylogger.log(logging.DEBUG, "Leet is %s", leet)

raw_comment = "1. Here is sample /\\pple I3urger  23424, comment of language used to test 0 functions found in our feature generation file. L33t bcuz Le3t. 2. This is purely for test purposes  .  Test, Repeat. 1, 2 3 ,434, 4 "
sensitive_comment = u'/\pple is all i need'

def test_py():
      x=5
      y=6
      assert x+1 == y,"test failed"

def test_insert_and_verify_user():
    #Database declaration and connection
    database = r'database/dopplegaenger.db'
    conn = db.create_connection(database)
    #Returns a dictionary cursor instead of tuple
    conn.row_factory = db.sql.Row
    thisdict = {
    "comment_author_id": 999999999,
    "comment_author_username": "monero"
    }
    mylogger.log(logging.DEBUG, "User ID: %s and  Username: %s", str(thisdict["comment_author_id"]), str(thisdict["comment_author_username"]))
    db.insert_into_user(conn,thisdict)
    conn.commit()
    cur = db.sql_check_username_exist(conn,"monero")
    username_exist = cur.fetchone()
    mylogger.log(logging.DEBUG, "user exist %s", username_exist)
    assert username_exist,"test failed"
    db.sql_delete_username(conn,"monero")
    conn.commit()
    db.close_db_connection(conn)

# def test_letter_frequency():
#     freq = feat.character_frequency_letters(raw_comment)
#     freq_compare = {'H': 1, 'e': 18, 'r': 7, 'i': 7, 's': 11, 'a': 6, 'm': 3, 'p': 5, 'l': 4, 'c': 2, 'o': 9, 'n': 8, 't': 11, 'f': 6, 'g': 3, 'u': 8, 'd': 2, 'T': 2, 'h': 1, 'y': 1, 'R': 1}
#     mylogger.log(logging.DEBUG, "Char frequency is %s", freq)
#     assert freq == freq_compare, "test failed"  

# def test_letter_frequency_fail():
#     freq = feat.character_frequency_letters(raw_comment)
#     freq_compare = {'H': 1, 'e': 190, 'r': 7, 'i': 7, 's': 11, 'a': 7, 'm': 3, 'p': 5, 'l': 4, 'c': 2, 'o': 9, 'n': 8, 't': 11, 'f': 6, 'g': 3, 'u': 8, 'd': 2, 'T': 2, 'h': 1, 'y': 1, 'R': 1}
#     assert freq != freq_compare, "test failed"  

# def test_digit_frequency():
#     freq = feat.character_frequency_digits(raw_comment)
#     freq_compare = {'1': 2, '2': 4, '3': 3, '4': 5, '0': 1}
#     assert freq == freq_compare, "test failed"

# #VERIFY
# def test_individual_char_frequency():
#     freq = feat.character_frequency(raw_comment)
#     freq_compare = {1: 16, 4: 8, 2: 5, 6: 3, 5: 2, 7: 2, 8: 2, 9: 1, 3: 2, 10: 1}
#     mylogger.log(logging.DEBUG, "Char frequency is %s", freq)
#     assert freq == freq_compare, "test failed"  

# def test_individual_char_frequency():
#     freq = feat.word_length_distribution(raw_comment)
#     freq_compare = {'H': 1, 'e': 190, 'r': 7, 'i': 7, 's': 11, 'a': 7, 'm': 3, 'p': 5, 'l': 4, 'c': 2, 'o': 9, 'n': 8, 't': 11, 'f': 6, 'g': 3, 'u': 8, 'd': 2, 'T': 2, 'h': 1, 'y': 1, 'R': 1}
#     mylogger.log(logging.DEBUG, "Word Distribution is %s", freq)
#     assert freq != freq_compare, "test failed" 

# def test_leet_string_sentence():
#     leet = feat.leetspeak_sentence(raw_comment)
#     leet_compare = {'H': 1, 'e': 190, 'r': 7, 'i': 7, 's': 11, 'a': 7, 'm': 3, 'p': 5, 'l': 4, 'c': 2, 'o': 9, 'n': 8, 't': 11, 'f': 6, 'g': 3, 'u': 8, 'd': 2, 'T': 2, 'h': 1, 'y': 1, 'R': 1}
#     assert leet != leet, "test failed"

def test_leetScan():
    leet = feat.dictionary_values_as_keys(alpha.leet_alphabet)
    assert feat.leetScan(raw_comment,leet) == Fraction(1, 24)

def test_check():
    assert feat.leetCheck("/\\pple") == True, "test failed"

def test_reverse():
    reverse = {'4': ['a'], '/\\': ['a'], '@': ['a'], '/-\\': ['a', 'h'], '^': ['a', 'n'], 'aye': ['a'], '(L': ['a'], 'Д': ['a'], 'I3': ['b'], '8': ['b'], '13': ['b'], '|3': ['b'], 'ß': ['b'], '!3': ['b'], '(3': ['b'], '/3': ['b'], ')3': ['b'], '|-]': ['b'], 'j3': ['b'], '6': ['b', 'g'], '[': ['c'], '¢': ['c'], '{': ['c'], '<': ['c'], '(': ['c'], '©': ['c'], ')': ['d'], '|)': ['d'], '(|': ['d'], '[)': ['d'], 'I>': ['d'], '|>': ['d', 'p'], '?': ['d', 'p', 'x'], 'T)': ['d', 'd'], 'I7': ['d'], 'cl': ['d'], '|}': ['d'], '>': ['d'], '|]': ['d'], '3': ['e'], '&': ['e', 'g', 'q'], '£': ['e', 'l'], '€': ['e'], 'ë': ['e'], '[-': ['e'], '|=-': ['e'], '|=': ['f'], 'ƒ': ['f'], '|#': ['f'], 'ph': ['f'], '/=': ['f'], 'v': ['f', 'u'], '(_+': ['g'], '9': ['g', 'p', 'q'], 'C-': ['g'], 'gee': ['g'], '(?,': ['g'], '[,': ['g'], '{,': ['g'], '<-': ['g'], '(.': ['g'], '#': ['h'], '/-/': ['h'], '[-]': ['h'], ']-[': ['h'], ')-(': ['h'], '(-)': ['h'], ':-:': ['h'], '|~|': ['h'], '|-|': ['h'], ']~[': ['h'], '}{': ['h', 'x'], '!-!': ['h'], '1-1': ['h'], '\\-/': ['h'], 'I+I': ['h'], '1': ['i', 'j', 'l'], '[]': ['i', 'o'], '|': ['i', 'l'], '!': ['i'], 'eye': ['i'], '3y3': ['i'], '][': ['i', 'x'], ',_|': ['j'], '_|': ['j'], '._|': ['j'], '._]': ['j'], '_]': ['j'], ',_]': ['j'], ']': ['j'], ';': ['j'], '>|': ['k'], '|<': ['k'], '/<': ['k'], '1<': ['k'], '|c': ['k'], '|(': ['k'], '|{': ['k'], '7': ['l', 't', 'y'], '|_': ['l'], '/\\/\\': ['m'], '/\\V\\': ['m'], 'JVI': ['m'], '[V]': ['m'], '[]V[]': ['m'], '|\\/|': ['m'], '^^': ['m'], '<\\/>': ['m'], '\\{V\\}': ['m'], '(v)': ['m'], '(V)': ['m'], '|V|': ['m'], 'nn': ['m'], 'IVI': ['m'], '|\\|\\': ['m'], ']\\/[': ['m'], '1^1': ['m'], 'ITI': ['m'], 'JTI': ['m'], '^/': ['n'], '|\\|': ['n'], '/\\/': ['n'], '[\\]': ['n'], '<\\>': ['n'], '{\\}': ['n'], '|V': ['n'], '/V': ['n'], 'И': ['n'], 'ท': ['n'], '0': ['o'], 'Q': ['o'], '()': ['o'], 'oh': ['o'], 'p': ['o'], '<>': ['o'], 'Ø': ['o'], '|*': ['p'], '|o': ['p'], '|º': ['p'], '|^': ['p', 'r'], '|"': ['p'], '[]D': ['p'], '|°': ['p'], '|7': ['p'], '(_,)': ['q'], '()_': ['q'], '2': ['q', 'r', 's', 'z'], '0_': ['q'], '<|': ['q'], 'I2': ['r'], '|`': ['r'], '|~': ['r'], '|?': ['r'], '/2': ['r'], 'lz': ['r'], '|9': ['r'], '12': ['r'], '®': ['r'], '[z': ['r'], 'Я': ['r'], '.-': ['r'], '|2': ['r'], '|-': ['r'], '5': ['s'], '$': ['s'], 'z': ['s'], '§': ['s'], 'ehs': ['s'], 'es': ['s'], '+': ['t'], '-|-': ['t'], "']['": ['t'], '†': ['t'], '"|"': ['t'], '~|~': ['t'], '(_)': ['u'], '|_|': ['u'], 'L|': ['u'], 'µ': ['u'], 'บ': ['u'], '\\/': ['v'], '|/': ['v'], '\\|': ['v'], '\\/\\/': ['w'], 'VV': ['w'], '\\N': ['w'], "'//": ['w'], "\\\\'": ['w'], '\\^/': ['w'], '(n)': ['w'], '\\V/': ['w'], '\\X/': ['w'], '\\|/': ['w', 'y'], '\\_|_/': ['w'], '\\_:_/': ['w'], 'Ш': ['w'], 'Щ': ['w'], 'uu': ['w'], '2u': ['w'], '\\\\//\\\\//': ['w'], 'พ': ['w'], 'v²': ['w'], '><': ['x'], 'Ж': ['x'], 'ecks': ['x'], '×': ['x'], ')(': ['x'], 'j': ['y'], '`/': ['y'], 'Ч': ['y'], '¥': ['y'], '\\//': ['y'], '7_': ['z'], '-/_': ['z'], '%': ['z'], '>_': ['z'], 's': ['z'], '~/_': ['z'], '-\\_': ['z'], '-|_': ['z']}
    leet = feat.dictionary_values_as_keys(alpha.leet_alphabet)
    assert leet == reverse

def test_upperCase():
    mylogger.log(logging.DEBUG, "Word: Strong")
    assert feat.uppercase_words("Strong")[0] == 1, "test failed"
def test_ALLCAPS():    
    mylogger.log(logging.DEBUG, "Word: STRONG is THE KEY")
    assert feat.all_capital_words("STRONG is THE KEY")[0] == 3, "test failed"

def test_grammar():
    assert feat.grammarCheck(u'A sentence with a error in the Hitchhiker’s Guide tot he Galaxy')[1] == 2, "test failed"