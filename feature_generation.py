import math
import re
import string

import nltk

sentiment_analysis_word_dict = dict(EN="misc/sentiment_analysis/en/vader_lexicon.txt",
                                    ES="",
                                    DE=["misc/sentiment_analysis/de/SentiWS_v2.0_Negative.txt",
                                        "misc/sentiment_analysis/de/SentiWS_v2.0_Positive.txt"],
                                    FR="")


###################################
####### HELPER FUNCTIONS ##########
###################################

# count words of a string excluding all punctuation but including emojis
def count_words(s):
    with open("misc/emojis/emoji_list", "r") as f:
        lines = f.read().splitlines()
    counter_include = 0
    for l in lines:
        counter_include += s.count(l)
    words = nltk.word_tokenize(s)
    counter_exclude = 0
    for word in words:
        if word in string.punctuation:
            counter_exclude += 1
    return len(words) - counter_exclude + counter_include


###################################
####### CHARACTER LEVEL ###########
###################################

# get character frequency for individual letters in a string
def character_frequency_letters(string):
    char_freq_letters = {}
    for char in string:
        if char.isalpha():
            if char in char_freq_letters:
                char_freq_letters[char] += 1
            else:
                char_freq_letters[char] = 1
    for char in char_freq_letters:
        char_freq_letters[char] = (char_freq_letters[char], char_freq_letters[char] / len(string))
    return char_freq_letters


# get character frequency for individual digits in a string
def character_frequency_digits(string):
    char_freq_digits = {}
    for char in string:
        if char.isnumeric():
            if char in char_freq_digits:
                char_freq_digits[char] += 1
            else:
                char_freq_digits[char] = 1
    for char in char_freq_digits:
        char_freq_digits[char] = (char_freq_digits[char], char_freq_digits[char] / len(string))
    return char_freq_digits


# get character frequency for individual special characters in a string
def character_frequency_special_characters(string):
    char_freq_special = {}
    for char in string:
        if not char.isalnum():
            if char in char_freq_special:
                char_freq_special[char] += 1
            else:
                char_freq_special[char] = 1
    for char in char_freq_special:
        char_freq_special[char] = (char_freq_special[char], char_freq_special[char] / len(string))
    return char_freq_special


# get character frequency for all individual characters in a string
def character_frequency(string):
    char_freq = {}
    for char in string:
        if char in char_freq:
            char_freq[char] += 1
        else:
            char_freq[char] = 1
    for char in char_freq:
        char_freq[char] = (char_freq[char], char_freq[char] / len(string))
    return char_freq


# get word length distribution for all words with up to 20 characters in a string
def word_length_distribution(string):
    word_length_distr = {}
    word_tokens = nltk.word_tokenize(string)
    for word in word_tokens:
        if len(word) <= 20:
            if len(word) in word_length_distr:
                word_length_distr[len(word)] += 1
            else:
                word_length_distr[len(word)] = 1
    return word_length_distr


###################################
##### VOCABULARY RICHNESS #########
###################################

# get word frequency for a string
def word_frequency(string):
    word_freq = {}
    word_tokens = nltk.word_tokenize(string)
    for word in word_tokens:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1
    return word_freq


# get number of words with a length larger then l
# returns a tuple: (total, weighted)
# TODO: is 10 a good standard value?
def number_big_words(string, l=10):
    number = 0
    word_tokens = nltk.word_tokenize(string)
    n = len(word_tokens)
    for word in word_tokens:
        if len(word) > l:
            number += 1
    return (number, number / n)


# get number of words appearing i times in a string
# for hapax legomena: i = 1
# for hapax dislegomena: i = 2
# returns a tuple: (total, weighted)
def number_words_appearing_i_times(string, i=1):
    number = 0
    word_freq = word_frequency(string)
    n = len(nltk.word_tokenize(string))
    for word in word_freq:
        if word_freq[word] == i:
            number += 1
    return (number, number / n)


def yules_k(string):
    return 0


def brunets_w(string):
    return 0


# get honores r measure for a string
# TODO: Research: What to do if hapax_legomena_weighted is 1? -> division by 0
def honores_r(string):
    word_tokens = nltk.word_tokenize(string)
    n = len(word_tokens)
    hapax_legomena_weighted = number_words_appearing_i_times(string)[1]
    if hapax_legomena_weighted == 1:
        return 0
    else:
        return 100 * (math.log(n) / (1 - hapax_legomena_weighted))


###################################
####### SENTENCE LEVEL ############
###################################

# get the average number of characters per sentence for a string
def average_number_characters_sentence(string):
    exclude = set([".", "?", "!"])
    counter_exclude = 0
    for char in string:
        if char in exclude or char.isspace():
            counter_exclude += 1
    sentences = nltk.sent_tokenize(string)
    return (len(string) - counter_exclude) / len(sentences)


# get the average number of lowercase letters per sentence for a string
def average_number_lowercase_letters_sentence(string):
    counter_lowercase = 0
    for char in string:
        if char.islower():
            counter_lowercase += 1
    sentences = nltk.sent_tokenize(string)
    return (counter_lowercase) / len(sentences)


# get the average number of uppercase letters per sentence for a string
def average_number_uppercase_letters_sentence(string):
    counter_uppercase = 0
    for char in string:
        if char.isupper():
            counter_uppercase += 1
    sentences = nltk.sent_tokenize(string)
    return (counter_uppercase) / len(sentences)


# get the average number of digits per sentence for a string
def average_number_digits_sentence(string):
    counter_digits = 0
    for char in string:
        if char.isnumeric():
            counter_digits += 1
    sentences = nltk.sent_tokenize(string)
    return (counter_digits) / len(sentences)


# get the average number of words per sentence for a string
def average_number_words_sentence(string):
    sentences = nltk.sent_tokenize(string)
    return count_words(string ) / len(sentences)


# get the total number of words per sentence for a string
def total_number_words_sentence(string):
    total_words_sentence = {}
    sentences = nltk.sent_tokenize(string)
    for sentence in sentences:
        total_words_sentence[sentence] = count_words(sentence)
    return total_words_sentence


###################################
######## PUNCTUATION ##############
###################################

# get the punctuation frequency for a string
# returns a dict with tuples (total, average)
def punctuation_frequency(s):
    punc_freq = {}
    for char in s:
        if char in string.punctuation:
            if char in punc_freq:
                punc_freq[char] += 1
            else:
                punc_freq[char] = 1
    for char in punc_freq:
        punc_freq[char] = (punc_freq[char], punc_freq[char] / len(s))
    return punc_freq


# get the punctuation frequency per sentence for a string
# returns a dict per sentence with tuples (total, average)
def punctuation_frequency_sentence(s):
    punc_freq = {}
    sentences = nltk.sent_tokenize(s)
    for sentence in sentences:
        punc_freq[sentence] = {}
        for char in sentence:
            if char in string.punctuation:
                if char in punc_freq[sentence]:
                    punc_freq[sentence][char] += 1
                else:
                    punc_freq[sentence][char] = 1
        for char in punc_freq[sentence]:
            punc_freq[sentence][char] = (punc_freq[sentence][char], punc_freq[sentence][char] / len(sentence))
    return punc_freq


###################################
######## WHITESPACES ##############
###################################

# get the frequency for the repeated occurences of whitespaces for a string
# returns a dict with tuples (total, average)
def repeated_whitespace(string):
    whitespaces = re.findall("\s+", string)
    dict = {}
    for w in whitespaces:
        if len(w) in dict:
            dict[len(w)] +=1
        else:
            dict[len(w)] = 1
    for whitespace in dict:
        dict[whitespace] = (dict[whitespace], dict[whitespace] / len(string))
    return dict


# get the frequency for the repeated occurences of whitespaces per sentence for a string
# returns a dict per sentence with tuples (total, average)
def repeated_whitespace_sentence(string):
    dict = {}
    sentences = nltk.sent_tokenize(string)
    for sentence in sentences:
        dict[sentence] = {}
        whitespaces = re.findall("\s+", sentence)
        for w in whitespaces:
            if len(w) in dict:
                dict[sentence][len(w)] += 1
            else:
                dict[sentence][len(w)] = 1
        for whitespace in dict[sentence]:
            dict[sentence][whitespace] = (dict[sentence][whitespace], dict[sentence][whitespace] / len(sentence))
    return dict


###################################
##### SENTIMENT ANALYSIS ##########
###################################

# loads the german sentiment lexicon from two text files, does some preprocessing and returns a dict
#
# We use SentimentWortschatz:
#
# SentimentWortschatz, or SentiWS for short, is a publicly available German-language resource for sentiment analysis,
# opinion mining etc. It lists positive and negative polarity bearing words weighted within the interval of [-1; 1]
# plus their part of speech tag, and if applicable, their inflections. The current version of SentiWS (v2.0) contains
# around 1,650 positive and 1,800 negative words, which sum up to around 16,000 positive and around 18,000 negative
# word forms incl. their inflections, respectively. It not only contains adjectives and adverbs explicitly expressing
# a sentiment, but also nouns and verbs implicitly containing one.
#
# R. Remus, U. Quasthoff & G. Heyer: SentiWS - a Publicly Available German-language Resource for Sentiment Analysis.
# In: Proceedings of the 7th International Language Ressources and Evaluation (LREC'10), 201
def load_sentiment_lexicon_german():
    dict = {}
    with open(sentiment_analysis_word_dict.get("DE")[0]) as f:
        lines = f.read().splitlines()
    for line in lines:
        line = re.split("\|.{0,6}\\t|\\t|,", line)
        for word in line[:1] + line[2:]:
            dict[word] = line[1]
    with open(sentiment_analysis_word_dict.get("DE")[1]) as f:
        lines = f.read().splitlines()
    for line in lines:
        line = re.split("\|.{0,6}\\t|\\t|,", line)
        for word in line[:1] + line[2:]:
            dict[word] = line[1]
    return dict


# loads the english sentiment lexicon from a text file, does some preprocessing and returns a dict
#
# We use VADERs lexicon:
#
# VADER (Valence Aware Dictionary and sEntiment Reasoner) is a lexicon and rule-based sentiment analysis tool that is
# specifically attuned to sentiments expressed in social media. It is fully open-sourced under the [MIT License]
#
# Sentiment ratings from 10 independent human raters (all pre-screened, trained, and quality checked for optimal
# inter-rater reliability). Over 9,000 token features were rated on a scale from "[–4] Extremely Negative"
# to "[4] Extremely Positive", with allowance for "[0] Neutral (or Neither, N/A)". We kept every lexical feature
# that had a non-zero mean rating, and whose standard deviation was less than 2.5 as determined by the aggregate of
# those ten independent raters. This left us with just over 7,500 lexical features with validated valence scores that
# indicated both the sentiment polarity (positive/negative), and the sentiment intensity on a scale from –4 to +4. For
# example, the word "okay" has a positive valence of 0.9, "good" is 1.9, and "great" is 3.1, whereas "horrible" is –2.5,
# the frowning emoticon :( is –2.2, and "sucks" and it's slang derivative "sux" are both –1.5.
#
# Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media
# Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
def load_sentiment_lexicon_english():
    dict = {}
    with open(sentiment_analysis_word_dict.get("EN")) as f:
        lines = f.read().splitlines()
    for line in lines:
        line = re.split("\t",line)
        dict[line[0]] = float(line[1]) / 4
    return dict


def load_sentiment_lexicon_spanish():
    return 0


def load_sentiment_lexicon_french():
    return 0


# helper function to load the sentiment lexicon
def load_sentiment_lexicon(language):
    if language.upper() == "DE":
        return load_sentiment_lexicon_german()
    elif language.upper() == "EN":
        return load_sentiment_lexicon_english()
    elif language.upper() == "ES":
        return load_sentiment_lexicon_spanish()
    elif language.upper() == "FR":
        return load_sentiment_lexicon_french()


# perform sentiment analysis based on a lexicon approach for a string
# result is a value between -1 and +1 where +1 is positive and -1 is negative
# returns the average per word
def sentiment_analysis_word_average(string, language="EN"):
    sentiment_lexicon = load_sentiment_lexicon(language)
    words = nltk.word_tokenize(string)
    result = 0.0
    for word in words:
        if word in sentiment_lexicon:
            result += float(sentiment_lexicon[word])
    return result / count_words(string)


# perform sentiment analysis based on a lexicon approach for a string
# result is a value between -1 and +1 where +1 is positive, 0 is neutral and -1 is negative
# returns the average per sentence
def sentiment_analysis_sentence_average(string, language="EN"):
    sentiment_lexicon = load_sentiment_lexicon(language)
    sentences = nltk.sent_tokenize(string)
    dict = {}
    for sentence in sentences:
        result = 0.0
        words = nltk.word_tokenize(sentence)
        for word in words:
            if word in sentiment_lexicon:
                result += float(sentiment_lexicon[word])
        dict[sentence] = result / count_words(sentence)
    return dict


###################################
##### ADDITIONAL FEATURES #########
###################################

# get the emoji frequency for a string
# returns a dict with tuples per emoji: tuple (total, average)
def emoji_frequency_word(string):
    with open("misc/emojis/emoji_list", "r") as f:
        lines = f.read().splitlines()
    dict = {}
    for l in lines:
        for l in lines:
            emojis_counter = string.count(l)
            if emojis_counter > 0:
                dict[l] = emojis_counter
    for emoji in dict:
        dict[emoji] = (dict[emoji], dict[emoji] / count_words(string))
    return dict


# get the emoji frequency for a string
# returns a dict with tuples per sentence and emoji: tuple (total, average)
def emoji_frequency_sentence(string):
    with open("misc/emojis/emoji_list", "r") as f:
        lines = f.read().splitlines()
    sentences = nltk.sent_tokenize(string)
    dict = {}
    for sentence in sentences:
        dict[sentence] = {}
        for l in lines:
            emojis_sentence_counter = sentence.count(l)
            if emojis_sentence_counter > 0:
                dict[sentence][l] = emojis_sentence_counter
        for emoji in dict[sentence]:
            dict[sentence][emoji] = (dict[sentence][emoji], dict[sentence][emoji] / count_words(sentence))
    return dict
