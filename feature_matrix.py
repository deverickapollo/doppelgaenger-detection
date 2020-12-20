import configparser, json, features.preprocessing as process, string, time, multiprocessing as mp, sys
from features.feature_generation import *
from multiprocessing import Process
from os import getpid, getppid
from multiprocessing import Pool

cpu_count = mp.cpu_count()

config = configparser.ConfigParser()
config.read_file(open(r'features/feature_generation_config.cfg'))

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


def func1(strings):
    matrix_dict["character_frequency_letters"] = character_frequency_letters(strings[select_string(cfg1)])
def func2(strings):
    matrix_dict["character_frequency_digits"] = character_frequency_digits(strings[select_string(cfg2)])
def func3(strings):
    matrix_dict["character_frequency_special_characters"] = character_frequency_special_characters(strings[select_string(cfg3)])
def func4(strings):
    matrix_dict["character_frequency"] = character_frequency(strings[select_string(cfg4)])
def func5(strings):
    matrix_dict["word_length_distribution"] = word_length_distribution(strings[select_string(cfg5)])
def func6(strings):
    matrix_dict["word_frequency"] = word_frequency(strings[select_string(cfg6)])
def func7(strings):
    matrix_dict["number_big_words"] = number_big_words(strings[select_string(cfg7)])
def func8(strings):
    matrix_dict["hapax_legomena"] = number_words_appearing_i_times(strings[select_string(cfg8)])
def func9(strings):
    matrix_dict["hapax_dislegomena"] = number_words_appearing_i_times(strings[select_string(cfg9)], 2)
def func10(strings):
    matrix_dict["yules_k"] = yules_k(strings[select_string(cfg10)])
def func11(strings):
    matrix_dict["brunets_w"] = brunets_w(strings[select_string(cfg11)])
def func12(strings):
    matrix_dict["honores_r"] = honores_r(strings[select_string(cfg12)])
def func13(strings):
    matrix_dict["average_number_characters_sentence"] = average_number_characters_sentence(strings[select_string(cfg13)])
def func14(strings):
    matrix_dict["average_number_lowercase_letters_sentence"] = average_number_lowercase_letters_sentence(strings[select_string(cfg14)])
def func15(strings):
    matrix_dict["average_number_uppercase_letters_sentence"] = average_number_uppercase_letters_sentence(strings[select_string(cfg15)])
def func16(strings):
    matrix_dict["average_number_digits_sentence"] = average_number_digits_sentence(strings[select_string(cfg16)])
def func17(strings):
    matrix_dict["average_number_words_sentence"] = average_number_words_sentence(strings[select_string(cfg17)])
def func18(strings):
    matrix_dict["total_number_words_sentence"] = total_number_words_sentence(strings[select_string(cfg18)])
def func19(strings):
    matrix_dict["punctuation_frequency"] = punctuation_frequency(strings[select_string(cfg19)])
def func20(strings):
    matrix_dict["punctuation_frequency_sentence"] = punctuation_frequency_sentence(strings[select_string(cfg20)])
def func21(strings):
    matrix_dict["repeated_whitespace"] = repeated_whitespace(strings[select_string(cfg21)])
def func22(strings):
    matrix_dict["repeated_whitespace_sentence"] = repeated_whitespace_sentence(strings[select_string(cfg22)])
def func23(strings):
    matrix_dict["uppercase_words"] = uppercase_words(strings[select_string(cfg23)])
def func24(strings):
    matrix_dict["uppercase_words_sentence"] = uppercase_words_sentence(strings[select_string(cfg24)])
def func25(strings, language):
    matrix_dict["grammarCheck"] = grammarCheck(strings[select_string(cfg25)], language)
def func26(strings, language):
    matrix_dict["grammarCheck_sentence"] = grammarCheck_sentence(strings[select_string(cfg26)], language)
def func27(strings, language):
    matrix_dict["sentiment_analysis_word_average"] = sentiment_analysis_word_average(strings[select_string(cfg27)], language)
def func28(strings, language):
    matrix_dict["sentiment_analysis_sentence_average"] = sentiment_analysis_sentence_average(strings[select_string(cfg28)], language)
def func29(strings):
    matrix_dict["emoji_frequency_word"] = emoji_frequency_word(strings[select_string(cfg29)])
def func30(strings):
    matrix_dict["emoji_frequency_sentence"] = emoji_frequency_sentence(strings[select_string(cfg30)])
def func31(strings):
    matrix_dict["get_language"] = get_language(strings[select_string(cfg31)])
def func32(strings):
    matrix_dict["all_capital_words"] = all_capital_words(strings[select_string(cfg32)])
def func33(strings):
    matrix_dict["all_capital_words_sentence"] = all_capital_words_sentence(strings[select_string(cfg33)])
def func34(strings):
    matrix_dict["type_token_ratio"] = type_token_ratio(strings[select_string(cfg34)])
def func35(strings):
    matrix_dict["mean_word_frequency"] = mean_word_frequency(strings[select_string(cfg35)])
def func36(strings):
    matrix_dict["sichels_s"] = sichels_s(strings[select_string(cfg36)])


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

def add_to_db_if_exist(comment,statvalues):
    pass

def returnDict():
    return matrix_dict

# generate the feature vector based on the config file
# returns a dict
if __name__ == '__main__':
    starttime = time.time()
    string = str(sys.argv[1])
    matrix_dict = {}
    language = get_language(string)
    string_remove_stop_words = process.remove_stop_words(string)
    string_lemmatize = process.lemmatize(string, language)
    string_remove_stop_words_lemmatize = process.lemmatize(string_remove_stop_words, language)
    strings = [string, string_remove_stop_words, string_lemmatize, string_remove_stop_words_lemmatize]

    flist=[func1,func2,func3,func4,func5,func6,func7,\
          func8,func9,func10,func11,func12,func13,func14,\
          func15,func16,func17,func18,func19,func20,func21,\
          func22,func23,func24,\
          func29,func30,func31,func32,func33,func34,func35,func36]
    flist2=[func25,func26,func27,func28]
    with mp.Pool(processes=cpu_count) as pool:
        for i in flist:
            pool.apply_async(i(strings))  
        for j in flist2:
            pool.apply_async(j(strings,language))

    pool.close()
    pool.join()

    # print(matrix_dict)
    # print("=========================================")    
    # print('Time taken = {} seconds'.format(time.time() - starttime))
    # print("=========================================")  

    