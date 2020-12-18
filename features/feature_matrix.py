import configparser, json, features.preprocessing as process, string, time, multiprocessing 
from features.feature_generation import *

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
        
# generate the feature vector based on the config file
# returns a dict
def feature_vector(string):
    dict ={}
    language = get_language(string)
    string_remove_stop_words = process.remove_stop_words(string)
    string_lemmatize = process.lemmatize(string, language)
    string_remove_stop_words_lemmatize = process.lemmatize(string_remove_stop_words, language)
    strings = [string, string_remove_stop_words, string_lemmatize, string_remove_stop_words_lemmatize]
    config = configparser.ConfigParser()
    #config.readfp(open(r'features/feature_generation_config.cfg'))
    config.read_file(open(r'features/feature_generation_config.cfg'))
    # Character Frequency
    cfg = json.loads(config.get("Character Frequency", "character_frequency_letters"))
    if cfg[0] == 1:
        dict["character_frequency_letters"] = character_frequency_letters(strings[select_string(cfg)])
    cfg = json.loads(config.get("Character Frequency", "character_frequency_digits"))
    if cfg[0] == 1:
        dict["character_frequency_digits"] = character_frequency_digits(strings[select_string(cfg)])
    cfg = json.loads(config.get("Character Frequency", "character_frequency_special_characters"))
    if cfg[0] == 1:
        dict["character_frequency_special_characters"] = character_frequency_special_characters(strings[select_string(cfg)])
    cfg = json.loads(config.get("Character Frequency", "character_frequency"))
    if cfg[0] == 1:
        dict["character_frequency"] = character_frequency(strings[select_string(cfg)])
    cfg = json.loads(config.get("Character Frequency", "word_length_distribution"))
    if cfg[0] == 1:
        dict["word_length_distribution"] = word_length_distribution(strings[select_string(cfg)])

    # Vocabulary Richness
    cfg = json.loads(config.get("Vocabulary Richness", "word_frequency"))
    if cfg[0] == 1:
        dict["word_frequency"] = word_frequency(strings[select_string(cfg)])
    cfg = json.loads(config.get("Vocabulary Richness", "number_big_words"))
    if cfg[0] == 1:
        dict["number_big_words"] = number_big_words(strings[select_string(cfg)])
    cfg = json.loads(config.get("Vocabulary Richness", "hapax_legomena"))
    if cfg[0] == 1:
        dict["hapax_legomena"] = number_words_appearing_i_times(strings[select_string(cfg)])
    cfg = json.loads(config.get("Vocabulary Richness", "hapax_dislegomena"))
    if cfg[0] == 1:
        dict["hapax_dislegomena"] = number_words_appearing_i_times(strings[select_string(cfg)], 2)
    cfg = json.loads(config.get("Vocabulary Richness", "yules_k"))
    if cfg[0] == 1:
        dict["yules_k"] = yules_k(strings[select_string(cfg)])
    cfg = json.loads(config.get("Vocabulary Richness", "brunets_w"))
    if cfg[0] == 1:
        dict["brunets_w"] = brunets_w(strings[select_string(cfg)])
    cfg = json.loads(config.get("Vocabulary Richness", "honores_r"))
    if cfg[0] == 1:
        dict["honores_r"] = honores_r(strings[select_string(cfg)])

    # Sentence Level
    cfg = json.loads(config.get("Sentence Level", "average_number_characters_sentence"))
    if cfg[0] == 1:
        dict["average_number_characters_sentence"] = average_number_characters_sentence(strings[select_string(cfg)])
    cfg = json.loads(config.get("Sentence Level", "average_number_lowercase_letters_sentence"))
    if cfg[0] == 1:
        dict["average_number_lowercase_letters_sentence"] = average_number_lowercase_letters_sentence(strings[select_string(cfg)])
    cfg = json.loads(config.get("Sentence Level", "average_number_uppercase_letters_sentence"))
    if cfg[0] == 1:
        dict["average_number_uppercase_letters_sentence"] = average_number_uppercase_letters_sentence(strings[select_string(cfg)])
    cfg = json.loads(config.get("Sentence Level", "average_number_digits_sentence"))
    if cfg[0] == 1:
        dict["average_number_digits_sentence"] = average_number_digits_sentence(strings[select_string(cfg)])
    cfg = json.loads(config.get("Sentence Level", "average_number_words_sentence"))
    if cfg[0] == 1:
        dict["average_number_words_sentence"] = average_number_words_sentence(strings[select_string(cfg)])
    cfg = json.loads(config.get("Sentence Level", "total_number_words_sentence"))
    if cfg[0] == 1:
        dict["total_number_words_sentence"] = total_number_words_sentence(strings[select_string(cfg)])

    # Punctuation
    cfg = json.loads(config.get("Punctuation", "punctuation_frequency"))
    if cfg[0] == 1:
        dict["punctuation_frequency"] = punctuation_frequency(strings[select_string(cfg)])
    cfg = json.loads(config.get("Punctuation", "punctuation_frequency_sentence"))
    if cfg[0] == 1:
        dict["punctuation_frequency_sentence"] = punctuation_frequency_sentence(strings[select_string(cfg)])

    # Whitespaces
    cfg = json.loads(config.get("Whitespaces", "repeated_whitespace"))
    if cfg[0] == 1:
        dict["repeated_whitespace"] = repeated_whitespace(strings[select_string(cfg)])
    cfg = json.loads(config.get("Whitespaces", "repeated_whitespace_sentence"))
    if cfg[0] == 1:
        dict["repeated_whitespace_sentence"] = repeated_whitespace_sentence(strings[select_string(cfg)])

    # Idiosyncrasy
    cfg = json.loads(config.get("Idiosyncrasy", "uppercase_words"))
    if cfg[0] == 1:
        dict["uppercase_words"] = uppercase_words(strings[select_string(cfg)])
    cfg = json.loads(config.get("Idiosyncrasy", "uppercase_words_sentence"))
    if cfg[0] == 1:
        dict["uppercase_words_sentence"] = uppercase_words_sentence(strings[select_string(cfg)])
    cfg = json.loads(config.get("Idiosyncrasy", "grammarCheck"))
    if cfg[0] == 1:
        dict["grammarCheck"] = grammarCheck(strings[select_string(cfg)], language)
    cfg = json.loads(config.get("Idiosyncrasy", "grammarCheck_sentence"))
    if cfg[0] == 1:
        dict["grammarCheck_sentence"] = grammarCheck_sentence(strings[select_string(cfg)], language)

    # Sentiment Analysis
    cfg = json.loads(config.get("Sentiment Analysis", "sentiment_analysis_word_average"))
    if cfg[0] == 1:
        dict["sentiment_analysis_word_average"] = sentiment_analysis_word_average(strings[select_string(cfg)], language)
    cfg = json.loads(config.get("Sentiment Analysis", "sentiment_analysis_sentence_average"))
    if cfg[0] == 1:
        dict["sentiment_analysis_sentence_average"] = sentiment_analysis_sentence_average(strings[select_string(cfg)], language)

    # Leetspeak
    #cfg = json.loads(config.get("Leetspeak", "leetspeak"))
    #if cfg[0] == 1:
    #    dict["leetspeak"] = leetspeak(strings[select_string(cfg)])

    # Additional Features
    cfg = json.loads(config.get("Additional Features", "emoji_frequency_word"))
    if cfg[0] == 1:
        dict["emoji_frequency_word"] = emoji_frequency_word(strings[select_string(cfg)])
    cfg = json.loads(config.get("Additional Features", "emoji_frequency_sentence"))
    if cfg[0] == 1:
        dict["emoji_frequency_sentence"] = emoji_frequency_sentence(strings[select_string(cfg)])
    cfg = json.loads(config.get("Additional Features", "get_language"))
    if cfg[0] == 1:
        dict["get_language"] = get_language(strings[select_string(cfg)])
    cfg = json.loads(config.get("Additional Features", "all_capital_words"))
    if cfg[0] == 1:
        dict["all_capital_words"] = all_capital_words(strings[select_string(cfg)])
    cfg = json.loads(config.get("Additional Features", "all_capital_words_sentence"))
    if cfg[0] == 1:
        dict["all_capital_words_sentence"] = all_capital_words_sentence(strings[select_string(cfg)])
    cfg = json.loads(config.get("Additional Features", "type_token_ratio"))
    if cfg[0] == 1:
        dict["type_token_ratio"] = type_token_ratio(strings[select_string(cfg)])
    cfg = json.loads(config.get("Additional Features", "mean_word_frequency"))
    if cfg[0] == 1:
        dict["mean_word_frequency"] = mean_word_frequency(strings[select_string(cfg)])
    cfg = json.loads(config.get("Additional Features", "sichels_s"))
    if cfg[0] == 1:
        dict["sichels_s"] = sichels_s(strings[select_string(cfg)])

    return dict

if __name__ == '__main__':
    print("RUNNING")