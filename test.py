import logging, database.db_access as db, features.feature_generation as feat, features.leetalpha as alpha, json
import feature_matrix as matrix, features.preprocessing as process
from database.db_access import *
from fractions import Fraction

# Debug Log
logging.basicConfig(level=logging.DEBUG, format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
mylogger = logging.getLogger()

raw_comment = "1. Here is sample /\\pple I3urger  23424, comment of language used to test 0 functions found in our feature generation file. L33t bcuz Le3t. 2. This is purely for test purposes  .  Test, Repeat. 1, 2 3 ,434, 4 "

generator = feat.Feature_Generator(raw_comment)


def test_py():
    x = 5
    y = 6
    assert x + 1 == y, "test failed"


def test_insert_and_verify_user():
    # Database declaration and connection
    database = r'database/dopplegaenger.db'
    conn = db.create_connection(database)
    create_article_table(conn)
    create_user_table(conn)
    create_comment_table(conn)
    create_stats_table(conn)
    # Returns a dictionary cursor instead of tuple
    conn.row_factory = db.sql.Row
    thisdict = {
        "comment_author_id": 999999999,
        "comment_author_username": "monero"
    }
    mylogger.log(logging.DEBUG, "User ID: %s and  Username: %s", str(thisdict["comment_author_id"]),
                 str(thisdict["comment_author_username"]))
    db.insert_into_user(conn, thisdict)
    conn.commit()
    cur = db.sql_check_username_exist(conn, "monero")
    username_exist = cur.fetchone()
    mylogger.log(logging.DEBUG, "user exist %s", username_exist[0])
    assert username_exist, "test failed"
    db.close_db_connection(conn)

    # Test Inserting Comment


def test_comment():
    database = r'database/dopplegaenger.db'
    conn = db.create_connection(database)
    thiscomment = {
        "comment_id": 999999999,
        "comment_text": "monero on the rise",
        "comment_date": 999999999,
        "comment_author_id": 999999999,
        "comment_author_username": "monero",
        "article_url": "someurl.com",
        "article_title": "Some new title"
    }
    db.insert_into_comment(conn, thiscomment)
    conn.commit()
    # Pass comment_id to check for comment in database
    cur = db.sql_check_comment_exist(conn, 999999999)
    comment_exist = cur.fetchone()
    mylogger.log(logging.DEBUG, "Comment exist %s", comment_exist)
    assert comment_exist, "test failed"
    db.close_db_connection(conn)


def test_insert_stat_for_comment():
    database = r'database/dopplegaenger.db'
    conn = db.create_connection(database)
    thisstat = {
        "character_frequency_letters": 999999999,
        "character_frequency_digits": 999999999,
        "character_frequency_special_characters": 999999999,
        "character_frequency": 999999999,
        "word_length_distribution": 999999999,
        "word_frequency": 999999999,
        "number_big_words": 999999999,
        "hapax_legomena": 999999999,
        "hapax_dislegomena": 999999999,
        "yules_k": 999999999,
        "brunets_w": 999999999,
        "honores_r": 999999999,
        "average_number_characters_sentence": 999999999,
        "average_number_lowercase_letters_sentence": 999999999,
        "average_number_uppercase_letters_sentence": 999999999,
        "average_number_digits_sentence": 999999999,
        "average_number_words_sentence": 999999999,
        "total_number_words_sentence": 999999999,
        "punctuation_frequency": 999999999,
        "punctuation_frequency_sentence": 999999999,
        "repeated_whitespace": 999999999,
        "repeated_whitespace_sentence": 999999999,
        "uppercase_words": 999999999,
        "uppercase_words_sentence": 999999999,
        "grammarCheck": 999999999,
        "grammarCheck_sentence": 999999999,
        "sentiment_analysis_word_average": 999999999,
        "sentiment_analysis_sentence_average": 999999999,
        "emoji_frequency_word": 999999999,
        "emoji_frequency_sentence": 999999999,
        "get_language": 999999999,
        "all_capital_words": 999999999,
        "all_capital_words_sentence": 999999999,
        "type_token_ratio": 999999999,
        "mean_word_frequency": 999999999,
        "sichels_s": 999999999
    }
    comment_id = 999999999
    db.insert_into_stats(conn, comment_id, thisstat)
    conn.commit()
    # Pass comment_id to check for comment in database
    cur = db.sql_check_stat_exist(conn, 999999999)
    stat_exist = cur.fetchone()
    mylogger.log(logging.DEBUG, "Stat exist %s", stat_exist)
    assert stat_exist, "test failed"
    db.close_db_connection(conn)


def test_delete():
    database = r'database/dopplegaenger.db'
    conn = db.create_connection(database)
    # We need to delete all stats
    username = "monero"
    db.sql_delete_stat_by_id(conn, 999999999)
    db.sql_delete_comments_by_comment_author_username(conn, username)
    db.sql_delete_userid(conn, 999999999)
    conn.commit()

    cur = db.sql_check_username_exist(conn, username)
    username_exist = cur.fetchone()
    mylogger.log(logging.DEBUG, "User %s has been removed ", username)
    assert username_exist == None, "test failed"
    db.close_db_connection(conn)


def test_check():
    testgenerator = feat.Feature_Generator("/\\pple")
    assert testgenerator.leetCheck() == True, "test failed"


def test_reverse():
    reverse = {'4': ['a'], '/\\': ['a'], '@': ['a'], '/-\\': ['a', 'h'], '^': ['a', 'n'], 'aye': ['a'], '(L': ['a'],
               'Д': ['a'], 'I3': ['b'], '8': ['b'], '13': ['b'], '|3': ['b'], 'ß': ['b'], '!3': ['b'], '(3': ['b'],
               '/3': ['b'], ')3': ['b'], '|-]': ['b'], 'j3': ['b'], '6': ['b', 'g'], '[': ['c'], '¢': ['c'], '{': ['c'],
               '<': ['c'], '(': ['c'], '©': ['c'], ')': ['d'], '|)': ['d'], '(|': ['d'], '[)': ['d'], 'I>': ['d'],
               '|>': ['d', 'p'], '?': ['d', 'p', 'x'], 'T)': ['d', 'd'], 'I7': ['d'], 'cl': ['d'], '|}': ['d'],
               '>': ['d'], '|]': ['d'], '3': ['e'], '&': ['e', 'g', 'q'], '£': ['e', 'l'], '€': ['e'], 'ë': ['e'],
               '[-': ['e'], '|=-': ['e'], '|=': ['f'], 'ƒ': ['f'], '|#': ['f'], 'ph': ['f'], '/=': ['f'],
               'v': ['f', 'u'], '(_+': ['g'], '9': ['g', 'p', 'q'], 'C-': ['g'], 'gee': ['g'], '(?,': ['g'],
               '[,': ['g'], '{,': ['g'], '<-': ['g'], '(.': ['g'], '#': ['h'], '/-/': ['h'], '[-]': ['h'], ']-[': ['h'],
               ')-(': ['h'], '(-)': ['h'], ':-:': ['h'], '|~|': ['h'], '|-|': ['h'], ']~[': ['h'], '}{': ['h', 'x'],
               '!-!': ['h'], '1-1': ['h'], '\\-/': ['h'], 'I+I': ['h'], '1': ['i', 'j', 'l'], '[]': ['i', 'o'],
               '|': ['i', 'l'], '!': ['i'], 'eye': ['i'], '3y3': ['i'], '][': ['i', 'x'], ',_|': ['j'], '_|': ['j'],
               '._|': ['j'], '._]': ['j'], '_]': ['j'], ',_]': ['j'], ']': ['j'], ';': ['j'], '>|': ['k'], '|<': ['k'],
               '/<': ['k'], '1<': ['k'], '|c': ['k'], '|(': ['k'], '|{': ['k'], '7': ['l', 't', 'y'], '|_': ['l'],
               '/\\/\\': ['m'], '/\\V\\': ['m'], 'JVI': ['m'], '[V]': ['m'], '[]V[]': ['m'], '|\\/|': ['m'],
               '^^': ['m'], '<\\/>': ['m'], '\\{V\\}': ['m'], '(v)': ['m'], '(V)': ['m'], '|V|': ['m'], 'nn': ['m'],
               'IVI': ['m'], '|\\|\\': ['m'], ']\\/[': ['m'], '1^1': ['m'], 'ITI': ['m'], 'JTI': ['m'], '^/': ['n'],
               '|\\|': ['n'], '/\\/': ['n'], '[\\]': ['n'], '<\\>': ['n'], '{\\}': ['n'], '|V': ['n'], '/V': ['n'],
               'И': ['n'], 'ท': ['n'], '0': ['o'], 'Q': ['o'], '()': ['o'], 'oh': ['o'], 'p': ['o'], '<>': ['o'],
               'Ø': ['o'], '|*': ['p'], '|o': ['p'], '|º': ['p'], '|^': ['p', 'r'], '|"': ['p'], '[]D': ['p'],
               '|°': ['p'], '|7': ['p'], '(_,)': ['q'], '()_': ['q'], '2': ['q', 'r', 's', 'z'], '0_': ['q'],
               '<|': ['q'], 'I2': ['r'], '|`': ['r'], '|~': ['r'], '|?': ['r'], '/2': ['r'], 'lz': ['r'], '|9': ['r'],
               '12': ['r'], '®': ['r'], '[z': ['r'], 'Я': ['r'], '.-': ['r'], '|2': ['r'], '|-': ['r'], '5': ['s'],
               '$': ['s'], 'z': ['s'], '§': ['s'], 'ehs': ['s'], 'es': ['s'], '+': ['t'], '-|-': ['t'], "']['": ['t'],
               '†': ['t'], '"|"': ['t'], '~|~': ['t'], '(_)': ['u'], '|_|': ['u'], 'L|': ['u'], 'µ': ['u'], 'บ': ['u'],
               '\\/': ['v'], '|/': ['v'], '\\|': ['v'], '\\/\\/': ['w'], 'VV': ['w'], '\\N': ['w'], "'//": ['w'],
               "\\\\'": ['w'], '\\^/': ['w'], '(n)': ['w'], '\\V/': ['w'], '\\X/': ['w'], '\\|/': ['w', 'y'],
               '\\_|_/': ['w'], '\\_:_/': ['w'], 'Ш': ['w'], 'Щ': ['w'], 'uu': ['w'], '2u': ['w'],
               '\\\\//\\\\//': ['w'], 'พ': ['w'], 'v²': ['w'], '><': ['x'], 'Ж': ['x'], 'ecks': ['x'], '×': ['x'],
               ')(': ['x'], 'j': ['y'], '`/': ['y'], 'Ч': ['y'], '¥': ['y'], '\\//': ['y'], '7_': ['z'], '-/_': ['z'],
               '%': ['z'], '>_': ['z'], 's': ['z'], '~/_': ['z'], '-\\_': ['z'], '-|_': ['z']}
    leet = generator.dictionary_values_as_keys(alpha.leet_alphabet)
    assert leet == reverse


# def test_grammar():
#     assert feat.grammarCheck(u'A sentence with a error in the Hitchhiker’s Guide tot he Galaxy')[1] == 2, "test failed"

def test_count_words_sentence():
    mylogger.log(logging.DEBUG, "Input: Check the lock. Cache is full. Lets test again.")
    testgenerator = feat.Feature_Generator("Check. Check")
    assert testgenerator.count_words_sentence("Check the lock. Cache is full. Lets test again. :)") == 10, "test failed"


def test_count_words():
    mylogger.log(logging.DEBUG, "Input: These are four words.")
    testgenerator = feat.Feature_Generator("These are four words.")
    assert testgenerator.count_words() == 4, "test failed"


def test_count_words2():
    mylogger.log(logging.DEBUG, "Input: These are. four words..")
    testgenerator = feat.Feature_Generator("These are. four words.")
    assert testgenerator.count_words() == 4, "test failed"


def test_count_words3():
    mylogger.log(logging.DEBUG, "Input: Counting characters makes Jack a dull boy.")
    testgenerator = feat.Feature_Generator("Counting characters makes Jack a dull boy.")
    assert testgenerator.count_words() == 7, "test failed"


def test_count_words4():
    mylogger.log(logging.DEBUG, "Input: ")
    testgenerator = feat.Feature_Generator("")
    assert testgenerator.count_words() == 0, "test failed"


def test_count_words5():
    mylogger.log(logging.DEBUG, "Input: ")
    testgenerator = feat.Feature_Generator("Counting characters makes Jack a dull boy. :)")
    assert testgenerator.count_words() == 8, "test failed"


def test_character_frequency_letters():
    mylogger.log(logging.DEBUG, "Input: Freq123.,!")
    dict = {'a': 0.0, 'b': 0.0, 'c': 0.0, 'd': 0.0, 'e': 0.1, 'f': 0.0, 'g': 0.0, 'h': 0.0, 'i': 0.0, 'j': 0.0,
            'k': 0.0, 'l': 0.0, 'm': 0.0, 'n': 0.0, 'o': 0.0, 'p': 0.0, 'q': 0.1, 'r': 0.1, 's': 0.0, 't': 0.0,
            'u': 0.0, 'v': 0.0, 'w': 0.0, 'x': 0.0, 'y': 0.0, 'z': 0.0, 'A': 0.0, 'B': 0.0, 'C': 0.0, 'D': 0.0,
            'E': 0.0, 'F': 0.1, 'G': 0.0, 'H': 0.0, 'I': 0.0, 'J': 0.0, 'K': 0.0, 'L': 0.0, 'M': 0.0, 'N': 0.0,
            'O': 0.0, 'P': 0.0, 'Q': 0.0, 'R': 0.0, 'S': 0.0, 'T': 0.0, 'U': 0.0, 'V': 0.0, 'W': 0.0, 'X': 0.0,
            'Y': 0.0, 'Z': 0.0}
    testgenerator = feat.Feature_Generator("Freq123.,!")
    assert testgenerator.character_frequency_letters() == dict, "test failed"


def test_character_frequency_digits():
    mylogger.log(logging.DEBUG, "Input: Freq123.,!")
    dict = {'0': 0.0,
            '1': 0.1,
            '2': 0.1,
            '3': 0.1,
            '4': 0.0,
            '5': 0.0,
            '6': 0.0,
            '7': 0.0,
            '8': 0.0,
            '9': 0.0}
    testgenerator = feat.Feature_Generator("Freq123.,!")
    assert testgenerator.character_frequency_digits() == dict, "test failed"


def test_character_frequency_special_characters():
    mylogger.log(logging.DEBUG, "Input: Freq123.,!")
    dict = {'!': 0.1,
            '"': 0.0,
            '#': 0.0,
            '$': 0.0,
            '%': 0.0,
            '&': 0.0,
            "'": 0.0,
            '(': 0.0,
            ')': 0.0,
            '*': 0.0,
            '+': 0.0,
            ',': 0.1,
            '-': 0.0,
            '.': 0.1,
            '/': 0.0,
            ':': 0.0,
            ';': 0.0,
            '<': 0.0,
            '=': 0.0,
            '>': 0.0,
            '?': 0.0,
            '@': 0.0,
            '[': 0.0,
            '\\': 0.0,
            ']': 0.0,
            '^': 0.0,
            '_': 0.0,
            '`': 0.0,
            '{': 0.0,
            '|': 0.0,
            '}': 0.0,
            '~': 0.0}
    testgenerator = feat.Feature_Generator("Freq123.,!")
    assert testgenerator.character_frequency_special_characters() == dict, "test failed"


def test_word_length_distribution():
    mylogger.log(logging.DEBUG, "Input: This is a test string.")
    dict = {0: 0.0,
            1: 0.16666666666666666,
            2: 0.16666666666666666,
            3: 0.0,
            4: 0.3333333333333333,
            5: 0.0,
            6: 0.16666666666666666,
            7: 0.0,
            8: 0.0,
            9: 0.0,
            10: 0.0,
            11: 0.0,
            12: 0.0,
            13: 0.0,
            14: 0.0,
            15: 0.0,
            16: 0.0,
            17: 0.0,
            18: 0.0,
            19: 0.0,
            20: 0.0}
    testgenerator = feat.Feature_Generator("This is a test string.")
    assert testgenerator.word_length_distribution() == dict, "test failed"


def test_number_big_words():
    mylogger.log(logging.DEBUG, "Input: Only one big woooooooooooord.")
    testgenerator = feat.Feature_Generator("Only one big woooooooooooord.")
    assert testgenerator.number_big_words() == 0.25, "test failed"


def test_hapax_legomena():
    mylogger.log(logging.DEBUG, "Input: This is a test string.")
    testgenerator = feat.Feature_Generator("This is a test string.")
    assert testgenerator.number_words_appearing_i_times() == 5, "test failed"


def test_hapax_dislegomena():
    mylogger.log(logging.DEBUG, "Input: This is a test string.")
    testgenerator = feat.Feature_Generator("This is a test string string.")
    assert testgenerator.number_words_appearing_i_times(2) == 1, "test failed"


def test_average_number_characters_sentence():
    mylogger.log(logging.DEBUG, "Input: This is. A test.")
    testgenerator = feat.Feature_Generator("This is. A test.")
    assert testgenerator.average_number_characters_sentence() == 5.5, "test failed"


def test_average_number_lowercase_letters_sentence():
    mylogger.log(logging.DEBUG, "Input: This is. A test.")
    testgenerator = feat.Feature_Generator("This is. A test.")
    assert testgenerator.average_number_lowercase_letters_sentence() == 4.5, "test failed"


def test_average_number_uppercase_letters_sentence():
    mylogger.log(logging.DEBUG, "Input: This is. A test.")
    testgenerator = feat.Feature_Generator("This is. A test.")
    assert testgenerator.average_number_uppercase_letters_sentence() == 1, "test failed"


def test_average_number_digits_sentence():
    mylogger.log(logging.DEBUG, "Input: Th1s 1s. A t3st.")
    testgenerator = feat.Feature_Generator("Th1s 1s. A t3st.")
    assert testgenerator.average_number_digits_sentence() == 1.5, "test failed"


def test_average_number_words_sentence():
    mylogger.log(logging.DEBUG, "Input: This is. A test test.")
    testgenerator = feat.Feature_Generator("This is. A test test.")
    assert testgenerator.average_number_words_sentence() == 2.5, "test failed"


def test_total_number_words_sentence():
    mylogger.log(logging.DEBUG, "Input: This is. A test.")
    testgenerator = feat.Feature_Generator("This is. A test.")
    assert testgenerator.total_number_words_sentence() == {'This is.': 2, 'A test.': 2}, "test failed"


def test_punctuation_frequency():
    dict = {'!': 0.0,
            '"': 0.0,
            '#': 0.0,
            '$': 0.0,
            '%': 0.0,
            '&': 0.0,
            "'": 0.0,
            '(': 0.0,
            ')': 0.0,
            '*': 0.0,
            '+': 0.0,
            ',': 0.0,
            '-': 0.0,
            '.': 0.125,
            '/': 0.0,
            ':': 0.0,
            ';': 0.0,
            '<': 0.0,
            '=': 0.0,
            '>': 0.0,
            '?': 0.0,
            '@': 0.0,
            '[': 0.0,
            '\\': 0.0,
            ']': 0.0,
            '^': 0.0,
            '_': 0.0,
            '`': 0.0,
            '{': 0.0,
            '|': 0.0,
            '}': 0.0,
            '~': 0.0}
    mylogger.log(logging.DEBUG, "Input: This is. A test.")
    testgenerator = feat.Feature_Generator("This is. A test.")
    assert testgenerator.punctuation_frequency() == dict, "test failed"


def test_punctuation_frequency_sentence():
    dict = {'!': 0.0,
            '"': 0.0,
            '#': 0.0,
            '$': 0.0,
            '%': 0.0,
            '&': 0.0,
            "'": 0.0,
            '(': 0.0,
            ')': 0.0,
            '*': 0.0,
            '+': 0.0,
            ',': 0.0,
            '-': 0.0,
            '.': 1.0,
            '/': 0.0,
            ':': 0.0,
            ';': 0.0,
            '<': 0.0,
            '=': 0.0,
            '>': 0.0,
            '?': 0.0,
            '@': 0.0,
            '[': 0.0,
            '\\': 0.0,
            ']': 0.0,
            '^': 0.0,
            '_': 0.0,
            '`': 0.0,
            '{': 0.0,
            '|': 0.0,
            '}': 0.0,
            '~': 0.0}
    mylogger.log(logging.DEBUG, "Input: This is. A test.")
    testgenerator = feat.Feature_Generator("This is. A test.")
    assert testgenerator.punctuation_frequency_sentence() == dict, "test failed"


def test_repeated_whitespace():
    dict = {0: 0.0,
            1: 0.0,
            2: 0.041666666666666664,
            3: 0.041666666666666664,
            4: 0.0,
            5: 0.0,
            6: 0.0,
            7: 0.0,
            8: 0.0,
            9: 0.0,
            10: 0.0,
            11: 0.0,
            12: 0.0,
            13: 0.0,
            14: 0.0,
            15: 0.0,
            16: 0.0,
            17: 0.0,
            18: 0.0,
            19: 0.0,
            20: 0.0}
    mylogger.log(logging.DEBUG, "Input: Test   Test. Test  Test.")
    testgenerator = feat.Feature_Generator("Test   Test. Test  Test.")
    assert testgenerator.repeated_whitespace() == dict, "test failed"


def test_repeated_whitespace_sentence():
    dict = {0: 0.0,
            1: 0.0,
            2: 0.5,
            3: 0.5,
            4: 0.0,
            5: 0.0,
            6: 0.0,
            7: 0.0,
            8: 0.0,
            9: 0.0,
            10: 0.0,
            11: 0.0,
            12: 0.0,
            13: 0.0,
            14: 0.0,
            15: 0.0,
            16: 0.0,
            17: 0.0,
            18: 0.0,
            19: 0.0,
            20: 0.0}
    mylogger.log(logging.DEBUG, "Input: Test   Test. Test  Test.")
    testgenerator = feat.Feature_Generator("Test   Test. Test  Test.")
    assert testgenerator.repeated_whitespace_sentence() == dict, "test failed"


def test_uppercase_words():
    mylogger.log(logging.DEBUG, "Input: Upper lower. Upper Upper.")
    testgenerator = feat.Feature_Generator("Upper lower. Upper Upper.")
    assert testgenerator.uppercase_words() == 0.75, "test failed"


def test_uppercase_words_sentence():
    mylogger.log(logging.DEBUG, "Input: Upper lower. Upper Upper.")
    testgenerator = feat.Feature_Generator("Upper lower. Upper Upper.")
    assert testgenerator.uppercase_words_sentence() == 1.5, "test failed"


def test_sentiment_analysis_word_average():
    mylogger.log(logging.DEBUG, "Input: Happy sentence. Sad sentence.")
    testgenerator = feat.Feature_Generator("Happy sentence. Sad sentence.")
    assert testgenerator.sentiment_analysis_word_average() == 0.075, "test failed"


def test_sentiment_analysis_sentence_average():
    mylogger.log(logging.DEBUG, "Input: Happy sentence. Sad sentence.")
    testgenerator = feat.Feature_Generator("Happy sentence. Sad sentence.")
    assert testgenerator.sentiment_analysis_sentence_average() == 0.15, "test failed"


def test_emoji_frequency_word():
    dict = {'$:': 0.0,
                          '%)': 0.0,
                          '%-)': 0.0,
                          '&-:': 0.0,
                          '&:': 0.0,
                          "( '}{' )": 0.0,
                          '(%': 0.0,
                          "('-:": 0.0,
                          "(':": 0.0,
                          '((-:': 0.0,
                          '(*': 0.0,
                          '(-%': 0.0,
                          '(-*': 0.0,
                          '(-:': 0.0,
                          '(-:0': 0.0,
                          '(-:<': 0.0,
                          '(-:o': 0.0,
                          '(-:O': 0.0,
                          '(-:{': 0.0,
                          '(-:|>*': 0.0,
                          '(-;': 0.0,
                          '(-;|': 0.0,
                          '(8': 0.0,
                          '(:': 0.0,
                          '(:0': 0.0,
                          '(:<': 0.0,
                          '(:o': 0.0,
                          '(:O': 0.0,
                          '(;': 0.0,
                          '(;<': 0.0,
                          '(=': 0.0,
                          '(?:': 0.0,
                          '(^:': 0.0,
                          '(^;': 0.0,
                          '(^;0': 0.0,
                          '(^;o': 0.0,
                          '(o:': 0.0,
                          ")':": 0.0,
                          ")-':": 0.0,
                          ')-:': 0.0,
                          ')-:<': 0.0,
                          ')-:{': 0.0,
                          '):': 0.0,
                          '):<': 0.0,
                          '):{': 0.0,
                          ');<': 0.0,
                          '*)': 0.0,
                          '*-)': 0.0,
                          '*-:': 0.0,
                          '*-;': 0.0,
                          '*:': 0.0,
                          '*<|:-)': 0.0,
                          '*\\0/*': 0.0,
                          '*^:': 0.0,
                          ',-:': 0.0,
                          "---'-;-{@": 0.0,
                          '--<--<@': 0.0,
                          '.-:': 0.0,
                          '..###-:': 0.0,
                          '..###:': 0.0,
                          '/-:': 0.0,
                          '/:': 0.0,
                          '/:<': 0.0,
                          '/=': 0.0,
                          '/^:': 0.0,
                          '/o:': 0.0,
                          '0-8': 0.0,
                          '0-|': 0.0,
                          '0:)': 0.0,
                          '0:-)': 0.0,
                          '0:-3': 0.0,
                          '0:03': 0.0,
                          '0;^)': 0.0,
                          '0_o': 0.0,
                          '10q': 0.0,
                          '1337': 0.0,
                          '143': 0.0,
                          '1432': 0.0,
                          '14aa41': 0.0,
                          '182': 0.0,
                          '187': 0.0,
                          '2g2b4g': 0.0,
                          '2g2bt': 0.0,
                          '2qt': 0.0,
                          '3:(': 0.0,
                          '3:)': 0.0,
                          '3:-(': 0.0,
                          '3:-)': 0.0,
                          '4col': 0.0,
                          '4q': 0.0,
                          '5fs': 0.0,
                          '8)': 0.0,
                          '8-d': 0.0,
                          '8-o': 0.0,
                          '86': 0.0,
                          '8d': 0.0,
                          ':###..': 0.0,
                          ':$': 0.0,
                          ':&': 0.0,
                          ":'(": 0.0,
                          ":')": 0.0,
                          ":'-(": 0.0,
                          ":'-)": 0.0,
                          ':(': 0.16666666666666666,
                          ':)': 0.0,
                          ':*': 0.0,
                          ':-###..': 0.0,
                          ':-&': 0.0,
                          ':-(': 0.0,
                          ':-)': 0.16666666666666666,
                          ':-))': 0.0,
                          ':-*': 0.0,
                          ':-,': 0.0,
                          ':-.': 0.0,
                          ':-/': 0.0,
                          ':-<': 0.0,
                          ':-d': 0.0,
                          ':-D': 0.0,
                          ':-o': 0.0,
                          ':-p': 0.0,
                          ':-[': 0.0,
                          ':-\\': 0.0,
                          ':-c': 0.0,
                          ':-|': 0.0,
                          ':-||': 0.0,
                          ':-Þ': 0.0,
                          ':/': 0.0,
                          ':3': 0.0,
                          ':<': 0.0,
                          ':>': 0.0,
                          ':?)': 0.0,
                          ':?c': 0.0,
                          ':@': 0.0,
                          ':d': 0.0,
                          ':D': 0.0,
                          ':l': 0.0,
                          ':o': 0.0,
                          ':p': 0.0,
                          ':s': 0.0,
                          ':[': 0.0,
                          ':\\': 0.0,
                          ':]': 0.0,
                          ':^)': 0.0,
                          ':^*': 0.0,
                          ':^/': 0.0,
                          ':^\\': 0.0,
                          ':^|': 0.0,
                          ':c': 0.0,
                          ':c)': 0.0,
                          ':o)': 0.0,
                          ':o/': 0.0,
                          ':o\\': 0.0,
                          ':o|': 0.0,
                          ':P': 0.0,
                          ':{': 0.0,
                          ':|': 0.0,
                          ':}': 0.0,
                          ':Þ': 0.0,
                          ';)': 0.0,
                          ';-)': 0.0,
                          ';-*': 0.0,
                          ';-]': 0.0,
                          ';d': 0.0,
                          ';D': 0.0,
                          ';]': 0.0,
                          ';^)': 0.0,
                          '</3': 0.0,
                          '<3': 0.0,
                          '<:': 0.0,
                          '<:-|': 0.0,
                          '=)': 0.0,
                          '=-3': 0.0,
                          '=-d': 0.0,
                          '=-D': 0.0,
                          '=/': 0.0,
                          '=3': 0.0,
                          '=d': 0.0,
                          '=D': 0.0,
                          '=l': 0.0,
                          '=\\': 0.0,
                          '=]': 0.0,
                          '=p': 0.0,
                          '=|': 0.0,
                          '>-:': 0.0,
                          '>.<': 0.0,
                          '>:': 0.0,
                          '>:(': 0.0,
                          '>:)': 0.0,
                          '>:-(': 0.0,
                          '>:-)': 0.0,
                          '>:/': 0.0,
                          '>:o': 0.0,
                          '>:p': 0.0,
                          '>:[': 0.0,
                          '>:\\': 0.0,
                          '>;(': 0.0,
                          '>;)': 0.0,
                          '>_>^': 0.0,
                          '@:': 0.0,
                          '@>-->--': 0.0,
                          "@}-;-'---": 0.0}
    mylogger.log(logging.DEBUG, "Input: This is :-). This is :(.")
    testgenerator = feat.Feature_Generator("This is :-). This is :(.")
    assert testgenerator.emoji_frequency_word() == dict, "test failed"


def test_emoji_frequency_sentence():
    dict = {'$:': 0.0,
                              '%)': 0.0,
                              '%-)': 0.0,
                              '&-:': 0.0,
                              '&:': 0.0,
                              "( '}{' )": 0.0,
                              '(%': 0.0,
                              "('-:": 0.0,
                              "(':": 0.0,
                              '((-:': 0.0,
                              '(*': 0.0,
                              '(-%': 0.0,
                              '(-*': 0.0,
                              '(-:': 0.0,
                              '(-:0': 0.0,
                              '(-:<': 0.0,
                              '(-:o': 0.0,
                              '(-:O': 0.0,
                              '(-:{': 0.0,
                              '(-:|>*': 0.0,
                              '(-;': 0.0,
                              '(-;|': 0.0,
                              '(8': 0.0,
                              '(:': 0.0,
                              '(:0': 0.0,
                              '(:<': 0.0,
                              '(:o': 0.0,
                              '(:O': 0.0,
                              '(;': 0.0,
                              '(;<': 0.0,
                              '(=': 0.0,
                              '(?:': 0.0,
                              '(^:': 0.0,
                              '(^;': 0.0,
                              '(^;0': 0.0,
                              '(^;o': 0.0,
                              '(o:': 0.0,
                              ")':": 0.0,
                              ")-':": 0.0,
                              ')-:': 0.0,
                              ')-:<': 0.0,
                              ')-:{': 0.0,
                              '):': 0.0,
                              '):<': 0.0,
                              '):{': 0.0,
                              ');<': 0.0,
                              '*)': 0.0,
                              '*-)': 0.0,
                              '*-:': 0.0,
                              '*-;': 0.0,
                              '*:': 0.0,
                              '*<|:-)': 0.0,
                              '*\\0/*': 0.0,
                              '*^:': 0.0,
                              ',-:': 0.0,
                              "---'-;-{@": 0.0,
                              '--<--<@': 0.0,
                              '.-:': 0.0,
                              '..###-:': 0.0,
                              '..###:': 0.0,
                              '/-:': 0.0,
                              '/:': 0.0,
                              '/:<': 0.0,
                              '/=': 0.0,
                              '/^:': 0.0,
                              '/o:': 0.0,
                              '0-8': 0.0,
                              '0-|': 0.0,
                              '0:)': 0.0,
                              '0:-)': 0.0,
                              '0:-3': 0.0,
                              '0:03': 0.0,
                              '0;^)': 0.0,
                              '0_o': 0.0,
                              '10q': 0.0,
                              '1337': 0.0,
                              '143': 0.0,
                              '1432': 0.0,
                              '14aa41': 0.0,
                              '182': 0.0,
                              '187': 0.0,
                              '2g2b4g': 0.0,
                              '2g2bt': 0.0,
                              '2qt': 0.0,
                              '3:(': 0.0,
                              '3:)': 0.0,
                              '3:-(': 0.0,
                              '3:-)': 0.0,
                              '4col': 0.0,
                              '4q': 0.0,
                              '5fs': 0.0,
                              '8)': 0.0,
                              '8-d': 0.0,
                              '8-o': 0.0,
                              '86': 0.0,
                              '8d': 0.0,
                              ':###..': 0.0,
                              ':$': 0.0,
                              ':&': 0.0,
                              ":'(": 0.0,
                              ":')": 0.0,
                              ":'-(": 0.0,
                              ":'-)": 0.0,
                              ':(': 0.5,
                              ':)': 0.0,
                              ':*': 0.0,
                              ':-###..': 0.0,
                              ':-&': 0.0,
                              ':-(': 0.0,
                              ':-)': 0.5,
                              ':-))': 0.0,
                              ':-*': 0.0,
                              ':-,': 0.0,
                              ':-.': 0.0,
                              ':-/': 0.0,
                              ':-<': 0.0,
                              ':-d': 0.0,
                              ':-D': 0.0,
                              ':-o': 0.0,
                              ':-p': 0.0,
                              ':-[': 0.0,
                              ':-\\': 0.0,
                              ':-c': 0.0,
                              ':-|': 0.0,
                              ':-||': 0.0,
                              ':-Þ': 0.0,
                              ':/': 0.0,
                              ':3': 0.0,
                              ':<': 0.0,
                              ':>': 0.0,
                              ':?)': 0.0,
                              ':?c': 0.0,
                              ':@': 0.0,
                              ':d': 0.0,
                              ':D': 0.0,
                              ':l': 0.0,
                              ':o': 0.0,
                              ':p': 0.0,
                              ':s': 0.0,
                              ':[': 0.0,
                              ':\\': 0.0,
                              ':]': 0.0,
                              ':^)': 0.0,
                              ':^*': 0.0,
                              ':^/': 0.0,
                              ':^\\': 0.0,
                              ':^|': 0.0,
                              ':c': 0.0,
                              ':c)': 0.0,
                              ':o)': 0.0,
                              ':o/': 0.0,
                              ':o\\': 0.0,
                              ':o|': 0.0,
                              ':P': 0.0,
                              ':{': 0.0,
                              ':|': 0.0,
                              ':}': 0.0,
                              ':Þ': 0.0,
                              ';)': 0.0,
                              ';-)': 0.0,
                              ';-*': 0.0,
                              ';-]': 0.0,
                              ';d': 0.0,
                              ';D': 0.0,
                              ';]': 0.0,
                              ';^)': 0.0,
                              '</3': 0.0,
                              '<3': 0.0,
                              '<:': 0.0,
                              '<:-|': 0.0,
                              '=)': 0.0,
                              '=-3': 0.0,
                              '=-d': 0.0,
                              '=-D': 0.0,
                              '=/': 0.0,
                              '=3': 0.0,
                              '=d': 0.0,
                              '=D': 0.0,
                              '=l': 0.0,
                              '=\\': 0.0,
                              '=]': 0.0,
                              '=p': 0.0,
                              '=|': 0.0,
                              '>-:': 0.0,
                              '>.<': 0.0,
                              '>:': 0.0,
                              '>:(': 0.0,
                              '>:)': 0.0,
                              '>:-(': 0.0,
                              '>:-)': 0.0,
                              '>:/': 0.0,
                              '>:o': 0.0,
                              '>:p': 0.0,
                              '>:[': 0.0,
                              '>:\\': 0.0,
                              '>;(': 0.0,
                              '>;)': 0.0,
                              '>_>^': 0.0,
                              '@:': 0.0,
                              '@>-->--': 0.0,
                              "@}-;-'---": 0.0}
    mylogger.log(logging.DEBUG, "Input: This is :-). This is :(.")
    testgenerator = feat.Feature_Generator("This is :-). This is :(.")
    assert testgenerator.emoji_frequency_sentence() == dict, "test failed"


def test_get_language_de():
    mylogger.log(logging.DEBUG, "Input: Das ist ein deutscher Satz.")
    testgenerator = feat.Feature_Generator("Das ist ein deutscher Satz")
    assert testgenerator.get_language() == "DE", "test failed"


def test_get_language_en():
    mylogger.log(logging.DEBUG, "Input: This is an english sentence.")
    testgenerator = feat.Feature_Generator("This is an english sentence.")
    assert testgenerator.get_language() == "EN", "test failed"


def test_all_capital_words():
    mylogger.log(logging.DEBUG, "Input: STRONG is THE KEY")
    testgenerator = feat.Feature_Generator("STRONG is THE KEY")
    assert testgenerator.all_capital_words() == 0.75, "test failed"


def test_all_capital_words_sentence():
    mylogger.log(logging.DEBUG, "Input: STRONG is THE KEY. KEY.")
    testgenerator = feat.Feature_Generator("STRONG is THE KEY. KEY.")
    assert testgenerator.all_capital_words_sentence() == 2, "test failed"


# def test_leetScan():
#    leet = generator.dictionary_values_as_keys(alpha.leet_alphabet)
#    assert generator.leetScan(raw_comment,leet) == Fraction(1, 24)

def test_feature_matrix():
    mylogger.log(logging.DEBUG, "Feature Matrix Testing")
    mylogger.log(logging.DEBUG, "Input: STRONG is THE KEY")
    ddict = matrix.feature_matrix("STRONG is THE KEY")
    json_dump = json.dumps(ddict, sort_keys=False, indent=4)
    ##Pretty print nested dictionary
    # mylogger.log(logging.DEBUG, "Feature Matrix: %s",  json_dump)
    assert ddict == {'character_frequency_letters': {'a': 0.0,
                                 'b': 0.0,
                                 'c': 0.0,
                                 'd': 0.0,
                                 'e': 0.0,
                                 'f': 0.0,
                                 'g': 0.0,
                                 'h': 0.0,
                                 'i': 0.058823529411764705,
                                 'j': 0.0,
                                 'k': 0.0,
                                 'l': 0.0,
                                 'm': 0.0,
                                 'n': 0.0,
                                 'o': 0.0,
                                 'p': 0.0,
                                 'q': 0.0,
                                 'r': 0.0,
                                 's': 0.058823529411764705,
                                 't': 0.0,
                                 'u': 0.0,
                                 'v': 0.0,
                                 'w': 0.0,
                                 'x': 0.0,
                                 'y': 0.0,
                                 'z': 0.0,
                                 'A': 0.0,
                                 'B': 0.0,
                                 'C': 0.0,
                                 'D': 0.0,
                                 'E': 0.11764705882352941,
                                 'F': 0.0,
                                 'G': 0.058823529411764705,
                                 'H': 0.058823529411764705,
                                 'I': 0.0,
                                 'J': 0.0,
                                 'K': 0.058823529411764705,
                                 'L': 0.0,
                                 'M': 0.0,
                                 'N': 0.058823529411764705,
                                 'O': 0.058823529411764705,
                                 'P': 0.0,
                                 'Q': 0.0,
                                 'R': 0.058823529411764705,
                                 'S': 0.058823529411764705,
                                 'T': 0.11764705882352941,
                                 'U': 0.0,
                                 'V': 0.0,
                                 'W': 0.0,
                                 'X': 0.0,
                                 'Y': 0.058823529411764705,
                                 'Z': 0.0},
 'character_frequency_digits': {'0': 0.0,
                                '1': 0.0,
                                '2': 0.0,
                                '3': 0.0,
                                '4': 0.0,
                                '5': 0.0,
                                '6': 0.0,
                                '7': 0.0,
                                '8': 0.0,
                                '9': 0.0},
 'character_frequency_special_characters': {'!': 0.0,
                                            '"': 0.0,
                                            '#': 0.0,
                                            '$': 0.0,
                                            '%': 0.0,
                                            '&': 0.0,
                                            "'": 0.0,
                                            '(': 0.0,
                                            ')': 0.0,
                                            '*': 0.0,
                                            '+': 0.0,
                                            ',': 0.0,
                                            '-': 0.0,
                                            '.': 0.0,
                                            '/': 0.0,
                                            ':': 0.0,
                                            ';': 0.0,
                                            '<': 0.0,
                                            '=': 0.0,
                                            '>': 0.0,
                                            '?': 0.0,
                                            '@': 0.0,
                                            '[': 0.0,
                                            '\\': 0.0,
                                            ']': 0.0,
                                            '^': 0.0,
                                            '_': 0.0,
                                            '`': 0.0,
                                            '{': 0.0,
                                            '|': 0.0,
                                            '}': 0.0,
                                            '~': 0.0},
 'word_length_distribution': {0: 0.0,
                              1: 0.0,
                              2: 0.25,
                              3: 0.5,
                              4: 0.0,
                              5: 0.0,
                              6: 0.25,
                              7: 0.0,
                              8: 0.0,
                              9: 0.0,
                              10: 0.0,
                              11: 0.0,
                              12: 0.0,
                              13: 0.0,
                              14: 0.0,
                              15: 0.0,
                              16: 0.0,
                              17: 0.0,
                              18: 0.0,
                              19: 0.0,
                              20: 0.0},
 'number_big_words': 0.0,
 'hapax_legomena': 4,
 'hapax_dislegomena': 0,
 'yules_k': 0.0,
 'brunets_w': 5.8100145317524445,
 'honores_r': 1386294361.8495748,
 'average_number_characters_sentence': 14.0,
 'average_number_lowercase_letters_sentence': 2.0,
 'average_number_uppercase_letters_sentence': 12.0,
 'average_number_digits_sentence': 0.0,
 'average_number_words_sentence': 4.0,
 'punctuation_frequency': {'!': 0.0,
                           '"': 0.0,
                           '#': 0.0,
                           '$': 0.0,
                           '%': 0.0,
                           '&': 0.0,
                           "'": 0.0,
                           '(': 0.0,
                           ')': 0.0,
                           '*': 0.0,
                           '+': 0.0,
                           ',': 0.0,
                           '-': 0.0,
                           '.': 0.0,
                           '/': 0.0,
                           ':': 0.0,
                           ';': 0.0,
                           '<': 0.0,
                           '=': 0.0,
                           '>': 0.0,
                           '?': 0.0,
                           '@': 0.0,
                           '[': 0.0,
                           '\\': 0.0,
                           ']': 0.0,
                           '^': 0.0,
                           '_': 0.0,
                           '`': 0.0,
                           '{': 0.0,
                           '|': 0.0,
                           '}': 0.0,
                           '~': 0.0},
 'punctuation_frequency_sentence': {'!': 0.0,
                                    '"': 0.0,
                                    '#': 0.0,
                                    '$': 0.0,
                                    '%': 0.0,
                                    '&': 0.0,
                                    "'": 0.0,
                                    '(': 0.0,
                                    ')': 0.0,
                                    '*': 0.0,
                                    '+': 0.0,
                                    ',': 0.0,
                                    '-': 0.0,
                                    '.': 0.0,
                                    '/': 0.0,
                                    ':': 0.0,
                                    ';': 0.0,
                                    '<': 0.0,
                                    '=': 0.0,
                                    '>': 0.0,
                                    '?': 0.0,
                                    '@': 0.0,
                                    '[': 0.0,
                                    '\\': 0.0,
                                    ']': 0.0,
                                    '^': 0.0,
                                    '_': 0.0,
                                    '`': 0.0,
                                    '{': 0.0,
                                    '|': 0.0,
                                    '}': 0.0,
                                    '~': 0.0},
 'repeated_whitespace': {0: 0.0,
                         1: 0.0,
                         2: 0.0,
                         3: 0.0,
                         4: 0.0,
                         5: 0.0,
                         6: 0.0,
                         7: 0.0,
                         8: 0.0,
                         9: 0.0,
                         10: 0.0,
                         11: 0.0,
                         12: 0.0,
                         13: 0.0,
                         14: 0.0,
                         15: 0.0,
                         16: 0.0,
                         17: 0.0,
                         18: 0.0,
                         19: 0.0,
                         20: 0.0},
 'repeated_whitespace_sentence': {0: 0.0,
                                  1: 0.0,
                                  2: 0.0,
                                  3: 0.0,
                                  4: 0.0,
                                  5: 0.0,
                                  6: 0.0,
                                  7: 0.0,
                                  8: 0.0,
                                  9: 0.0,
                                  10: 0.0,
                                  11: 0.0,
                                  12: 0.0,
                                  13: 0.0,
                                  14: 0.0,
                                  15: 0.0,
                                  16: 0.0,
                                  17: 0.0,
                                  18: 0.0,
                                  19: 0.0,
                                  20: 0.0},
 'uppercase_words': 0.0,
 'uppercase_words_sentence': 0.0,
 'emoji_frequency_word': {'$:': 0.0,
                          '%)': 0.0,
                          '%-)': 0.0,
                          '&-:': 0.0,
                          '&:': 0.0,
                          "( '}{' )": 0.0,
                          '(%': 0.0,
                          "('-:": 0.0,
                          "(':": 0.0,
                          '((-:': 0.0,
                          '(*': 0.0,
                          '(-%': 0.0,
                          '(-*': 0.0,
                          '(-:': 0.0,
                          '(-:0': 0.0,
                          '(-:<': 0.0,
                          '(-:o': 0.0,
                          '(-:O': 0.0,
                          '(-:{': 0.0,
                          '(-:|>*': 0.0,
                          '(-;': 0.0,
                          '(-;|': 0.0,
                          '(8': 0.0,
                          '(:': 0.0,
                          '(:0': 0.0,
                          '(:<': 0.0,
                          '(:o': 0.0,
                          '(:O': 0.0,
                          '(;': 0.0,
                          '(;<': 0.0,
                          '(=': 0.0,
                          '(?:': 0.0,
                          '(^:': 0.0,
                          '(^;': 0.0,
                          '(^;0': 0.0,
                          '(^;o': 0.0,
                          '(o:': 0.0,
                          ")':": 0.0,
                          ")-':": 0.0,
                          ')-:': 0.0,
                          ')-:<': 0.0,
                          ')-:{': 0.0,
                          '):': 0.0,
                          '):<': 0.0,
                          '):{': 0.0,
                          ');<': 0.0,
                          '*)': 0.0,
                          '*-)': 0.0,
                          '*-:': 0.0,
                          '*-;': 0.0,
                          '*:': 0.0,
                          '*<|:-)': 0.0,
                          '*\\0/*': 0.0,
                          '*^:': 0.0,
                          ',-:': 0.0,
                          "---'-;-{@": 0.0,
                          '--<--<@': 0.0,
                          '.-:': 0.0,
                          '..###-:': 0.0,
                          '..###:': 0.0,
                          '/-:': 0.0,
                          '/:': 0.0,
                          '/:<': 0.0,
                          '/=': 0.0,
                          '/^:': 0.0,
                          '/o:': 0.0,
                          '0-8': 0.0,
                          '0-|': 0.0,
                          '0:)': 0.0,
                          '0:-)': 0.0,
                          '0:-3': 0.0,
                          '0:03': 0.0,
                          '0;^)': 0.0,
                          '0_o': 0.0,
                          '10q': 0.0,
                          '1337': 0.0,
                          '143': 0.0,
                          '1432': 0.0,
                          '14aa41': 0.0,
                          '182': 0.0,
                          '187': 0.0,
                          '2g2b4g': 0.0,
                          '2g2bt': 0.0,
                          '2qt': 0.0,
                          '3:(': 0.0,
                          '3:)': 0.0,
                          '3:-(': 0.0,
                          '3:-)': 0.0,
                          '4col': 0.0,
                          '4q': 0.0,
                          '5fs': 0.0,
                          '8)': 0.0,
                          '8-d': 0.0,
                          '8-o': 0.0,
                          '86': 0.0,
                          '8d': 0.0,
                          ':###..': 0.0,
                          ':$': 0.0,
                          ':&': 0.0,
                          ":'(": 0.0,
                          ":')": 0.0,
                          ":'-(": 0.0,
                          ":'-)": 0.0,
                          ':(': 0.0,
                          ':)': 0.0,
                          ':*': 0.0,
                          ':-###..': 0.0,
                          ':-&': 0.0,
                          ':-(': 0.0,
                          ':-)': 0.0,
                          ':-))': 0.0,
                          ':-*': 0.0,
                          ':-,': 0.0,
                          ':-.': 0.0,
                          ':-/': 0.0,
                          ':-<': 0.0,
                          ':-d': 0.0,
                          ':-D': 0.0,
                          ':-o': 0.0,
                          ':-p': 0.0,
                          ':-[': 0.0,
                          ':-\\': 0.0,
                          ':-c': 0.0,
                          ':-|': 0.0,
                          ':-||': 0.0,
                          ':-Þ': 0.0,
                          ':/': 0.0,
                          ':3': 0.0,
                          ':<': 0.0,
                          ':>': 0.0,
                          ':?)': 0.0,
                          ':?c': 0.0,
                          ':@': 0.0,
                          ':d': 0.0,
                          ':D': 0.0,
                          ':l': 0.0,
                          ':o': 0.0,
                          ':p': 0.0,
                          ':s': 0.0,
                          ':[': 0.0,
                          ':\\': 0.0,
                          ':]': 0.0,
                          ':^)': 0.0,
                          ':^*': 0.0,
                          ':^/': 0.0,
                          ':^\\': 0.0,
                          ':^|': 0.0,
                          ':c': 0.0,
                          ':c)': 0.0,
                          ':o)': 0.0,
                          ':o/': 0.0,
                          ':o\\': 0.0,
                          ':o|': 0.0,
                          ':P': 0.0,
                          ':{': 0.0,
                          ':|': 0.0,
                          ':}': 0.0,
                          ':Þ': 0.0,
                          ';)': 0.0,
                          ';-)': 0.0,
                          ';-*': 0.0,
                          ';-]': 0.0,
                          ';d': 0.0,
                          ';D': 0.0,
                          ';]': 0.0,
                          ';^)': 0.0,
                          '</3': 0.0,
                          '<3': 0.0,
                          '<:': 0.0,
                          '<:-|': 0.0,
                          '=)': 0.0,
                          '=-3': 0.0,
                          '=-d': 0.0,
                          '=-D': 0.0,
                          '=/': 0.0,
                          '=3': 0.0,
                          '=d': 0.0,
                          '=D': 0.0,
                          '=l': 0.0,
                          '=\\': 0.0,
                          '=]': 0.0,
                          '=p': 0.0,
                          '=|': 0.0,
                          '>-:': 0.0,
                          '>.<': 0.0,
                          '>:': 0.0,
                          '>:(': 0.0,
                          '>:)': 0.0,
                          '>:-(': 0.0,
                          '>:-)': 0.0,
                          '>:/': 0.0,
                          '>:o': 0.0,
                          '>:p': 0.0,
                          '>:[': 0.0,
                          '>:\\': 0.0,
                          '>;(': 0.0,
                          '>;)': 0.0,
                          '>_>^': 0.0,
                          '@:': 0.0,
                          '@>-->--': 0.0,
                          "@}-;-'---": 0.0},
 'emoji_frequency_sentence': {'$:': 0.0,
                              '%)': 0.0,
                              '%-)': 0.0,
                              '&-:': 0.0,
                              '&:': 0.0,
                              "( '}{' )": 0.0,
                              '(%': 0.0,
                              "('-:": 0.0,
                              "(':": 0.0,
                              '((-:': 0.0,
                              '(*': 0.0,
                              '(-%': 0.0,
                              '(-*': 0.0,
                              '(-:': 0.0,
                              '(-:0': 0.0,
                              '(-:<': 0.0,
                              '(-:o': 0.0,
                              '(-:O': 0.0,
                              '(-:{': 0.0,
                              '(-:|>*': 0.0,
                              '(-;': 0.0,
                              '(-;|': 0.0,
                              '(8': 0.0,
                              '(:': 0.0,
                              '(:0': 0.0,
                              '(:<': 0.0,
                              '(:o': 0.0,
                              '(:O': 0.0,
                              '(;': 0.0,
                              '(;<': 0.0,
                              '(=': 0.0,
                              '(?:': 0.0,
                              '(^:': 0.0,
                              '(^;': 0.0,
                              '(^;0': 0.0,
                              '(^;o': 0.0,
                              '(o:': 0.0,
                              ")':": 0.0,
                              ")-':": 0.0,
                              ')-:': 0.0,
                              ')-:<': 0.0,
                              ')-:{': 0.0,
                              '):': 0.0,
                              '):<': 0.0,
                              '):{': 0.0,
                              ');<': 0.0,
                              '*)': 0.0,
                              '*-)': 0.0,
                              '*-:': 0.0,
                              '*-;': 0.0,
                              '*:': 0.0,
                              '*<|:-)': 0.0,
                              '*\\0/*': 0.0,
                              '*^:': 0.0,
                              ',-:': 0.0,
                              "---'-;-{@": 0.0,
                              '--<--<@': 0.0,
                              '.-:': 0.0,
                              '..###-:': 0.0,
                              '..###:': 0.0,
                              '/-:': 0.0,
                              '/:': 0.0,
                              '/:<': 0.0,
                              '/=': 0.0,
                              '/^:': 0.0,
                              '/o:': 0.0,
                              '0-8': 0.0,
                              '0-|': 0.0,
                              '0:)': 0.0,
                              '0:-)': 0.0,
                              '0:-3': 0.0,
                              '0:03': 0.0,
                              '0;^)': 0.0,
                              '0_o': 0.0,
                              '10q': 0.0,
                              '1337': 0.0,
                              '143': 0.0,
                              '1432': 0.0,
                              '14aa41': 0.0,
                              '182': 0.0,
                              '187': 0.0,
                              '2g2b4g': 0.0,
                              '2g2bt': 0.0,
                              '2qt': 0.0,
                              '3:(': 0.0,
                              '3:)': 0.0,
                              '3:-(': 0.0,
                              '3:-)': 0.0,
                              '4col': 0.0,
                              '4q': 0.0,
                              '5fs': 0.0,
                              '8)': 0.0,
                              '8-d': 0.0,
                              '8-o': 0.0,
                              '86': 0.0,
                              '8d': 0.0,
                              ':###..': 0.0,
                              ':$': 0.0,
                              ':&': 0.0,
                              ":'(": 0.0,
                              ":')": 0.0,
                              ":'-(": 0.0,
                              ":'-)": 0.0,
                              ':(': 0.0,
                              ':)': 0.0,
                              ':*': 0.0,
                              ':-###..': 0.0,
                              ':-&': 0.0,
                              ':-(': 0.0,
                              ':-)': 0.0,
                              ':-))': 0.0,
                              ':-*': 0.0,
                              ':-,': 0.0,
                              ':-.': 0.0,
                              ':-/': 0.0,
                              ':-<': 0.0,
                              ':-d': 0.0,
                              ':-D': 0.0,
                              ':-o': 0.0,
                              ':-p': 0.0,
                              ':-[': 0.0,
                              ':-\\': 0.0,
                              ':-c': 0.0,
                              ':-|': 0.0,
                              ':-||': 0.0,
                              ':-Þ': 0.0,
                              ':/': 0.0,
                              ':3': 0.0,
                              ':<': 0.0,
                              ':>': 0.0,
                              ':?)': 0.0,
                              ':?c': 0.0,
                              ':@': 0.0,
                              ':d': 0.0,
                              ':D': 0.0,
                              ':l': 0.0,
                              ':o': 0.0,
                              ':p': 0.0,
                              ':s': 0.0,
                              ':[': 0.0,
                              ':\\': 0.0,
                              ':]': 0.0,
                              ':^)': 0.0,
                              ':^*': 0.0,
                              ':^/': 0.0,
                              ':^\\': 0.0,
                              ':^|': 0.0,
                              ':c': 0.0,
                              ':c)': 0.0,
                              ':o)': 0.0,
                              ':o/': 0.0,
                              ':o\\': 0.0,
                              ':o|': 0.0,
                              ':P': 0.0,
                              ':{': 0.0,
                              ':|': 0.0,
                              ':}': 0.0,
                              ':Þ': 0.0,
                              ';)': 0.0,
                              ';-)': 0.0,
                              ';-*': 0.0,
                              ';-]': 0.0,
                              ';d': 0.0,
                              ';D': 0.0,
                              ';]': 0.0,
                              ';^)': 0.0,
                              '</3': 0.0,
                              '<3': 0.0,
                              '<:': 0.0,
                              '<:-|': 0.0,
                              '=)': 0.0,
                              '=-3': 0.0,
                              '=-d': 0.0,
                              '=-D': 0.0,
                              '=/': 0.0,
                              '=3': 0.0,
                              '=d': 0.0,
                              '=D': 0.0,
                              '=l': 0.0,
                              '=\\': 0.0,
                              '=]': 0.0,
                              '=p': 0.0,
                              '=|': 0.0,
                              '>-:': 0.0,
                              '>.<': 0.0,
                              '>:': 0.0,
                              '>:(': 0.0,
                              '>:)': 0.0,
                              '>:-(': 0.0,
                              '>:-)': 0.0,
                              '>:/': 0.0,
                              '>:o': 0.0,
                              '>:p': 0.0,
                              '>:[': 0.0,
                              '>:\\': 0.0,
                              '>;(': 0.0,
                              '>;)': 0.0,
                              '>_>^': 0.0,
                              '@:': 0.0,
                              '@>-->--': 0.0,
                              "@}-;-'---": 0.0},
 'get_language': 'EN',
 'all_capital_words': 0.75,
 'all_capital_words_sentence': 3.0,
 'type_token_ratio': 1.0,
 'mean_word_frequency': 1.0,
 'sichels_s': 0.0,
 'sentiment_analysis_word_average': 0.14375,
 'sentiment_analysis_sentence_average': 0.575}, \
        "test failed"

##Grammar check included
# assert ddict == {'character_frequency_letters': {'S': (1, 0.058823529411764705), 'T': (2, 0.11764705882352941), 'R': (1, 0.058823529411764705), \
#                 'O': (1, 0.058823529411764705), 'N': (1, 0.058823529411764705), 'G': (1, 0.058823529411764705), 'i': (1, 0.058823529411764705), 's': \
#                 (1, 0.058823529411764705), 'H': (1, 0.058823529411764705), 'E': (2, 0.11764705882352941), 'K': (1, 0.058823529411764705), \
#                 'Y': (1, 0.058823529411764705)}, 'character_frequency_digits': {}, 'character_frequency_special_characters': {' ': (3, 0.17647058823529413)}, \
#                 'character_frequency': {'S': (1, 0.058823529411764705), 'T': (2, 0.11764705882352941), 'R': (1, 0.058823529411764705), 'O': (1, 0.058823529411764705), \
#                 'N': (1, 0.058823529411764705), 'G': (1, 0.058823529411764705), ' ': (3, 0.17647058823529413), 'i': (1, 0.058823529411764705), 's': (1, 0.058823529411764705), \
#                 'H': (1, 0.058823529411764705), 'E': (2, 0.11764705882352941), 'K': (1, 0.058823529411764705), 'Y': (1, 0.058823529411764705)}, 'word_length_distribution': {6: 1, 2: 1, 3: 2}, \
#                 'word_frequency': {'STRONG': 1, 'is': 1, 'THE': 1, 'KEY': 1}, 'number_big_words': (0, 0.0), 'hapax_legomena': (4, 1.0), 'hapax_dislegomena': (0, 0.0), 'yules_k': 0.0, 'brunets_w': 5.8100145317524445, 'honores_r': 1386294361.8495748, \
#                 'average_number_characters_sentence': 14.0, 'average_number_lowercase_letters_sentence': 2.0, 'average_number_uppercase_letters_sentence': 12.0, 'average_number_digits_sentence': 0.0, \
#                 'average_number_words_sentence': 4.0, 'total_number_words_sentence': {'STRONG is THE KEY': 4}, 'punctuation_frequency': {}, 'punctuation_frequency_sentence': {'STRONG is THE KEY': {}}, \
#                 'repeated_whitespace': {}, 'repeated_whitespace_sentence': {'STRONG is THE KEY': {}}, 'uppercase_words': (0, 0.0), 'uppercase_words_sentence': {'STRONG is THE KEY': (0, 0.0)}, 'grammarCheck': ([], 0), \
#                 'grammarCheck_sentence': {'STRONG is THE KEY': ([], 0)}, 'sentiment_analysis_word_average': 0.14375, 'sentiment_analysis_sentence_average': {'strong is the key': 0.14375}, 'emoji_frequency_word': {}, \
#                 'emoji_frequency_sentence': {'STRONG is THE KEY': {}}, 'get_language': 'EN', 'all_capital_words': (3, 0.75), 'all_capital_words_sentence': {'STRONG is THE KEY': (3, 0.75)}, 'type_token_ratio': 1.0, 'mean_word_frequency': 1.0, 'sichels_s': 0.0}, \
#                 "test failed"
