import configparser, json, features.preprocessing as process, string, time, multiprocessing as mp, sys, os, logging
from pprint import pprint

from features.feature_generation import *
from multiprocessing import Process
from multiprocessing import Pool

cpu_count = mp.cpu_count()

config = configparser.ConfigParser()
config.read_file(open(r'features/feature_generation_config.cfg'))

# Debug Log
# logging.basicConfig(level=logging.DEBUG, format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
# mylogger = logging.getLogger()

# Character Frequency
cfg1 = json.loads(config.get("Character Frequency", "character_frequency_letters"))
cfg2 = json.loads(config.get("Character Frequency", "character_frequency_digits"))
cfg3 = json.loads(config.get("Character Frequency", "character_frequency_special_characters"))
cfg4 = json.loads(config.get("Character Frequency", "character_frequency"))
cfg5 = json.loads(config.get("Character Frequency", "word_length_distribution"))
cfg6 = json.loads(config.get("Vocabulary Richness", "word_frequency"))
cfg7 = json.loads(config.get("Vocabulary Richness", "number_big_words"))
cfg8 = json.loads(config.get("Vocabulary Richness", "hapax_legomena"))
cfg9 = json.loads(config.get("Vocabulary Richness", "hapax_dislegomena"))
cfg10 = json.loads(config.get("Vocabulary Richness", "yules_k"))
cfg11 = json.loads(config.get("Vocabulary Richness", "brunets_w"))
cfg12 = json.loads(config.get("Vocabulary Richness", "honores_r"))
cfg13 = json.loads(config.get("Sentence Level", "average_number_characters_sentence"))
cfg14 = json.loads(config.get("Sentence Level", "average_number_lowercase_letters_sentence"))
cfg15 = json.loads(config.get("Sentence Level", "average_number_uppercase_letters_sentence"))
cfg16 = json.loads(config.get("Sentence Level", "average_number_digits_sentence"))
cfg17 = json.loads(config.get("Sentence Level", "average_number_words_sentence"))
cfg18 = json.loads(config.get("Sentence Level", "total_number_words_sentence"))
cfg19 = json.loads(config.get("Punctuation", "punctuation_frequency"))
cfg20 = json.loads(config.get("Punctuation", "punctuation_frequency_sentence"))
cfg21 = json.loads(config.get("Whitespaces", "repeated_whitespace"))
cfg22 = json.loads(config.get("Whitespaces", "repeated_whitespace_sentence"))
cfg23 = json.loads(config.get("Idiosyncrasy", "uppercase_words"))
cfg24 = json.loads(config.get("Idiosyncrasy", "uppercase_words_sentence"))
cfg25 = json.loads(config.get("Idiosyncrasy", "grammarCheck"))
cfg26 = json.loads(config.get("Idiosyncrasy", "grammarCheck_sentence"))
cfg27 = json.loads(config.get("Sentiment Analysis", "sentiment_analysis_word_average"))
cfg28 = json.loads(config.get("Sentiment Analysis", "sentiment_analysis_sentence_average"))
cfg29 = json.loads(config.get("Additional Features", "emoji_frequency_word"))
cfg30 = json.loads(config.get("Additional Features", "emoji_frequency_sentence"))
cfg31 = json.loads(config.get("Additional Features", "get_language"))
cfg32 = json.loads(config.get("Additional Features", "all_capital_words"))
cfg33 = json.loads(config.get("Additional Features", "all_capital_words_sentence"))
cfg34 = json.loads(config.get("Additional Features", "type_token_ratio"))
cfg35 = json.loads(config.get("Additional Features", "mean_word_frequency"))
cfg36 = json.loads(config.get("Additional Features", "sichels_s"))

###################################
### FEATURE VECTOR GENERATION #####
###################################

# select which string is passed to the feature generation functions based on the config file
def select_string(cfg):
    if cfg[1] == 0 and cfg[2] == 0:
        return 0
    elif cfg[1] == 1 and cfg[2] == 0:
        return 1
    elif cfg[1] == 0 and cfg[2] == 1:
        return 2
    else:
        return 3


def func1(strings, matrix, matrix_dict):
    if select_string(cfg1):
        matrix.reset_string(strings[select_string(cfg1)])
    matrix_dict["character_frequency_letters"] = matrix.character_frequency_letters()


def func2(strings, matrix, matrix_dict):
    if select_string(cfg2):
        matrix.reset_string(strings[select_string(cfg2)])
    matrix_dict["character_frequency_digits"] = matrix.character_frequency_digits()


def func3(strings, matrix, matrix_dict):
    if select_string(cfg3):
        matrix.reset_string(strings[select_string(cfg3)])
    matrix_dict["character_frequency_special_characters"] = matrix.character_frequency_special_characters()


def func5(strings, matrix, matrix_dict):
    if select_string(cfg5):
        matrix.reset_string(strings[select_string(cfg5)])
    matrix_dict["word_length_distribution"] = matrix.word_length_distribution()


def func7(strings, matrix, matrix_dict):
    if select_string(cfg7):
        matrix.reset_string(strings[select_string(cfg7)])
    matrix_dict["number_big_words"] = matrix.number_big_words()


def func8(strings, matrix, matrix_dict):
    if select_string(cfg8):
        matrix.reset_string(strings[select_string(cfg8)])
    matrix_dict["hapax_legomena"] = matrix.number_words_appearing_i_times()


def func9(strings, matrix, matrix_dict):
    if select_string(cfg9):
        matrix.reset_string(strings[select_string(cfg9)])
    matrix_dict["hapax_dislegomena"] = matrix.number_words_appearing_i_times(2)


def func10(strings, matrix, matrix_dict):
    if select_string(cfg10):
        matrix.reset_string(strings[select_string(cfg10)])
    matrix_dict["yules_k"] = matrix.yules_k()


def func11(strings, matrix, matrix_dict):
    if select_string(cfg11):
        matrix.reset_string(strings[select_string(cfg11)])
    matrix_dict["brunets_w"] = matrix.brunets_w()


def func12(strings, matrix, matrix_dict):
    if select_string(cfg12):
        matrix.reset_string(strings[select_string(cfg12)])
    matrix_dict["honores_r"] = matrix.honores_r()


def func13(strings, matrix, matrix_dict):
    if select_string(cfg13):
        matrix.reset_string(strings[select_string(cfg13)])
    matrix_dict["average_number_characters_sentence"] = matrix.average_number_characters_sentence()


def func14(strings, matrix, matrix_dict):
    if select_string(cfg14):
        matrix.reset_string(strings[select_string(cfg14)])
    matrix_dict["average_number_lowercase_letters_sentence"] = matrix.average_number_lowercase_letters_sentence()


def func15(strings, matrix, matrix_dict):
    if select_string(cfg15):
        matrix.reset_string(strings[select_string(cfg15)])
    matrix_dict["average_number_uppercase_letters_sentence"] = matrix.average_number_uppercase_letters_sentence()


def func16(strings, matrix, matrix_dict):
    if select_string(cfg16):
        matrix.reset_string(strings[select_string(cfg16)])
    matrix_dict["average_number_digits_sentence"] = matrix.average_number_digits_sentence()


def func17(strings, matrix, matrix_dict):
    if select_string(cfg17):
        matrix.reset_string(strings[select_string(cfg17)])
    matrix_dict["average_number_words_sentence"] = matrix.average_number_words_sentence()


def func19(strings, matrix, matrix_dict):
    if select_string(cfg19):
        matrix.reset_string(strings[select_string(cfg19)])
    matrix_dict["punctuation_frequency"] = matrix.punctuation_frequency()


def func20(strings, matrix, matrix_dict):
    if select_string(cfg20):
        matrix.reset_string(strings[select_string(cfg20)])
    matrix_dict["punctuation_frequency_sentence"] = matrix.punctuation_frequency_sentence()


def func21(strings, matrix, matrix_dict):
    if select_string(cfg21):
        matrix.reset_string(strings[select_string(cfg21)])
    matrix_dict["repeated_whitespace"] = matrix.repeated_whitespace()


def func22(strings, matrix, matrix_dict):
    if select_string(cfg22):
        matrix.reset_string(strings[select_string(cfg22)])
    matrix_dict["repeated_whitespace_sentence"] = matrix.repeated_whitespace_sentence()


def func23(strings, matrix, matrix_dict):
    if select_string(cfg23):
        matrix.reset_string(strings[select_string(cfg23)])
    matrix_dict["uppercase_words"] = matrix.uppercase_words()


def func24(strings, matrix, matrix_dict):
    if select_string(cfg24):
        matrix.reset_string(strings[select_string(cfg24)])
    matrix_dict["uppercase_words_sentence"] = matrix.uppercase_words_sentence()


def func25(strings, matrix, language, matrix_dict):
    if select_string(cfg25):
        matrix.reset_string(strings[select_string(cfg25)])
    matrix_dict["grammarCheck"] = matrix.grammarCheck(language)


def func26(strings, matrix, language, matrix_dict):
    if select_string(cfg26):
        matrix.reset_string(strings[select_string(cfg26)])
    matrix_dict["grammarCheck_sentence"] = matrix.grammarCheck_sentence(language)


def func27(strings, matrix, language, matrix_dict):
    if select_string(cfg27):
        matrix.reset_string(strings[select_string(cfg27)])
    matrix_dict["sentiment_analysis_word_average"] = matrix.sentiment_analysis_word_average()


def func28(strings, matrix, language, matrix_dict):
    if select_string(cfg28):
        matrix.reset_string(strings[select_string(cfg28)])
    matrix_dict["sentiment_analysis_sentence_average"] = matrix.sentiment_analysis_sentence_average()


def func29(strings, matrix, matrix_dict):
    if select_string(cfg29):
        matrix.reset_string(strings[select_string(cfg29)])
    matrix_dict["emoji_frequency_word"] = matrix.emoji_frequency_word()


def func30(strings, matrix, matrix_dict):
    if select_string(cfg30):
        matrix.reset_string(strings[select_string(cfg30)])
    matrix_dict["emoji_frequency_sentence"] = matrix.emoji_frequency_sentence()


def func31(strings, matrix, matrix_dict):
    if select_string(cfg31):
        matrix.reset_string(strings[select_string(cfg31)])
    matrix_dict["get_language"] = matrix.get_language()


def func32(strings, matrix, matrix_dict):
    if select_string(cfg32):
        matrix.reset_string(strings[select_string(cfg32)])
    matrix_dict["all_capital_words"] = matrix.all_capital_words()


def func33(strings, matrix, matrix_dict):
    if select_string(cfg33):
        matrix.reset_string(strings[select_string(cfg33)])
    matrix_dict["all_capital_words_sentence"] = matrix.all_capital_words_sentence()


def func34(strings, matrix, matrix_dict):
    if select_string(cfg34):
        matrix.reset_string(strings[select_string(cfg34)])
    matrix_dict["type_token_ratio"] = matrix.type_token_ratio()


def func35(strings, matrix, matrix_dict):
    if select_string(cfg35):
        matrix.reset_string(strings[select_string(cfg35)])
    matrix_dict["mean_word_frequency"] = matrix.mean_word_frequency()


def func36(strings, matrix, matrix_dict):
    if select_string(cfg36):
        matrix.reset_string(strings[select_string(cfg36)])
    matrix_dict["sichels_s"] = matrix.sichels_s()

    # Leetspeak
    # cfg = json.loads(config.get("Leetspeak", "leetspeak"))
    # if cfg[0] == 1:
    #    matrix_dict["leetspeak"] = leetspeak(strings[select_string(cfg)])


def run_cpu_tasks_in_parallel(tasks):
    running_tasks = [Process(target=task) for task in tasks]
    for running_task in running_tasks:
        running_task.start()
    for running_task in running_tasks:
        running_task.join()


# generate a feature matrix for a list of strings and a list of user ids
def feature_matrix(s, u):
    vectors = []

    #func31 is getlanguage. strings not useful for pca computation
    flist = [func1, func2, func3, func5, func7, \
             func8, func9, func10, func11, func12, func13, func14, \
             func15, func16, func17, func19, func20, func21, \
             func22, func23, func24, \
             func29, func30,  func32, func33, func34, func35, func36]
    ##Grammar functions are cpu intensive. Evaluate value proposition before adding. TODO Must also be added to DB  # func25,func26,
    flist2 = [func27, func28]   
    starttime = time.time()
    with mp.Pool(processes=cpu_count) as pool:
        logging.log(logging.DEBUG, "s and u: %s %s",  s, u)
        # mylogger.log(logging.DEBUG, "s and u: %s %s",  s, u)
        for string, user_id in zip(s, u):
            matrix = Feature_Generator(string)
            string_remove_stop_words = process.remove_stop_words(string)
            string_lemmatize = process.lemmatize(string, matrix.language)
            string_remove_stop_words_lemmatize = process.lemmatize(string_remove_stop_words, matrix.language)
            strings = [string, string_remove_stop_words, string_lemmatize, string_remove_stop_words_lemmatize]
            matrix_dict = {}
       
            for i in flist:
                pool.apply_async(i(strings, matrix, matrix_dict))
            for j in flist2:
                pool.apply_async(j(strings, matrix, matrix.language, matrix_dict))



            json_dump = json.dumps(matrix_dict, sort_keys=False, indent=4)
            # # print(json_dump)

            matrix_dict["user_id"] = user_id
            vectors.append(flatten_dict(matrix_dict))
        pool.close()
        pool.join()
        print("=========================================")
        print('Time taken = {} seconds'.format(time.time() - starttime))
        print("=========================================")
        logging.log(logging.DEBUG, 'Time taken = {} seconds'.format(time.time() - starttime))
        logging.log(logging.DEBUG, merge_dicts(vectors))
        return merge_dicts(vectors)


# flatten a dictionary
def flatten_dict(init, left_key=''):
    flattened = dict()
    for right_key, value in init.items():
        key = str(left_key) + str(right_key)
        if isinstance(value, dict):
            flattened.update(flatten_dict(value, key + '_'))
        else:
            flattened[key] = value
    return flattened


# merge a list of dictionaries to a single dictionary
def merge_dicts(dicts):
    new = dict()
    for d in dicts:
        for key, value in d.items():
            new.setdefault(key, []).append(value)
    return new


# generate the feature matrix based on the config file
# returns a dict
if __name__ == '__main__':
    s = str(sys.argv[1])
    u = int(sys.argv[2])
    feature_matrix(s, u)
