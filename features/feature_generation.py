import math, re, nltk, features.leetalpha as alpha, string, spacy, features.preprocessing as process
from spacy_hunspell import spaCyHunSpell
from string import punctuation
from fractions import Fraction
from collections import defaultdict



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
        if word in punctuation:
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
    return count_words(string) / len(sentences)


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
        if char in punctuation:
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
            if char in punctuation:
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
            dict[len(w)] += 1
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
######## IDIOSYNCRASY #############
###################################

# get the number of uppercase words for a string
# returns a tuple: (total, average)
def uppercase_words(string):
    words = nltk.word_tokenize(string)
    counter_uppercase = 0
    for word in words:
        if word.isupper():
            counter_uppercase += 1
    return (counter_uppercase, counter_uppercase / count_words(string))


# get the number of uppercase words per sentence for a string
# returns a dict with a tuple per sentence: (total, average)
def uppercase_words_sentence(string):
    dict = {}
    sentences = nltk.sent_tokenize(string)
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        counter_uppercase = 0
        for word in words:
            if word.isupper():
                counter_uppercase += 1
        dict[sentence] = (counter_uppercase, counter_uppercase / count_words(sentence))
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
    with open("../misc/sentiment_analysis/de/SentiWS_v2.0_Negative.txt") as f:
        lines = f.read().splitlines()
    for line in lines:
        line = re.split("\|.{0,6}\\t|\\t|,", line)
        for word in line[:1] + line[2:]:
            dict[word] = line[1]
    with open("../misc/sentiment_analysis/de/SentiWS_v2.0_Positive.txt") as f:
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
    with open("../misc/sentiment_analysis/en/vader_lexicon.txt") as f:
        lines = f.read().splitlines()
    for line in lines:
        line = re.split("\t", line)
        dict[line[0]] = float(line[1]) / 4
    return dict


# loads the french sentiment lexicon from a text file, does some preprocessing and returns a dict
#
# We use the spanish version of the AFINN wordlist:
#
# * Finn Årup Nielsen, "A new ANEW: evaluation of a word list for sentiment analysis in microblogs", Proceedings
# of the ESWC2011 Workshop on 'Making Sense of Microposts': Big things come in small packages. Volume 718 in CEUR
# Workshop Proceedings: 93-98. 2011 May. Matthew Rowe, Milan Stankovic, Aba-Sah Dadzie, Mariann Hardey (editors)
def load_sentiment_lexicon_spanish():
    dict = {}
    with open("../misc/sentiment_analysis/es/AFINN-es-111.txt") as f:
        lines = f.read()
    lines = re.split(',', lines)
    for line in lines:
        line = re.split(':', line)
        dict[line[0].replace('"', '')] = float(line[1]) / 5
    return dict


# loads the french sentiment lexicon from a text file, does some preprocessing and returns a dict
#
# We use the french version of the AFINN wordlist:
#
# * Finn Årup Nielsen, "A new ANEW: evaluation of a word list for sentiment analysis in microblogs", Proceedings
# of the ESWC2011 Workshop on 'Making Sense of Microposts': Big things come in small packages. Volume 718 in CEUR
# Workshop Proceedings: 93-98. 2011 May. Matthew Rowe, Milan Stankovic, Aba-Sah Dadzie, Mariann Hardey (editors)
def load_sentiment_lexicon_french():
    dict = {}
    with open("../misc/sentiment_analysis/fr/AFINN-fr-165.txt") as f:
        lines = f.read().splitlines()
    for line in lines:
        line = re.split("\t", line)
        dict[line[0]] = float(line[1]) / 5
    return dict


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
####### LEEETSPEAK ################
###################################

def leetspeak(string):
    # total per sentence
    tots_per_sentence = total_number_words_sentence(string)
    punkt_st = nltk.tokenize.PunktSentenceTokenizer()
    sentence_list = punkt_st.tokenize(string)
    # Sentence Level Check
    sentence_level_leet = leetcheck(sentence_list)
    # Full Text Level Search
    # text_level_leet = leetcheck(string)
    return sentence_level_leet


def find_key(input_dict, value):
    return {k for k, v in input_dict.items() if v == value}


def leetcheck(string, language="EN"):
    leet = []
    nlp = spacy.load(process.spacy_models_dict.get(language.upper()))
    hunspell = spaCyHunSpell(nlp, ('/Library/Spelling/en_US.dic', '/Library/Spelling/en_US.aff'))
    # Need to consider other languages here
    nlp.add_pipe(hunspell)
    for sentence in string:
        tokens = nltk.word_tokenize(sentence)
        for token in tokens:
            # Check for misspelling
            check = nlp(token)[0]
            if check._.hunspell_spell == False:
                # See if word contains leet
                for a in alpha.leet_alphabet.values():
                    for j in a:
                        if j in token:
                            z = find_key(alpha.leet_alphabet, j)
                            # Add to possible candidate list

                            # Test candidate list
                            leet.append(token + " " + j + " " + str(z[0]))

    return leet


###################################
##### ADDITIONAL FEATURES #########
###################################

# get the emoji frequency for a string
# returns a dict with tuples per emoji: tuple (total, average)
def emoji_frequency_word(string):
    with open("../misc/emojis/emoji_list", "r") as f:
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
    with open("../misc/emojis/emoji_list", "r") as f:
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



###################################
####### LEETSPEAK ################
###################################

def leetspeak(string):
    valDict = dictionary_values_as_keys(alpha.leet_alphabet)

    #total per sentence
    tots_per_sentence = total_number_words_sentence(string)
    punkt_st = nltk.tokenize.PunktSentenceTokenizer()
    sentence_list = punkt_st.tokenize(string)
    #Sentence Level Check
    sentence_level_leet=leetScan(sentence_list, valDict)
    #Full Text Level Search
    # text_level_leet = leetScan(string)
    return sentence_level_leet

# Builds a dictionary with values from input dictionary mapped as keys.
# input: Dictionary
# output: Dictionary
def dictionary_values_as_keys(dict):
    keysDict = {}
    for key,values in dict.items():
        for v in values:
            if v not in keysDict:
                keysDict[v] = [key]
            elif v in keysDict:
                keysDict[v].append(key)
    return keysDict

# Prints a dictionary that contains a list as values.
# input: Dictionary
# output: Dictionary
def print_ldict(dict):
    for k in dict:
        print("key: " + k)
        for x in dict[k]:
            print(x)    

# Checks input strign for possible leet characters
# input: String
# output: True/False
def leetCheck(token):
    status = False
    for lValues in alpha.leet_alphabet.values():
        for leet in lValues:
            if leet in token:
                status = True
                return status
    return status

#Lets play a game.
# input: String
# output: True/False
def swapValid(token):
    status = False
    for lValues in alpha.leet_alphabet.values():
        for leet in lValues:
            if leet in token:
                print("hello")
    return status

# Checks what percentage of words are potential leetwords
# input: String, language = "EN"
# output: fraction

def leetScan(string, valDict, language = "EN", ):
    leetcandidates = []
    count = 0
    nlp = spacy.load(process.spacy_models_dict.get(language.upper()))
    
    hunspell = spaCyHunSpell(nlp, ('/Library/Spelling/en_US.dic', '/Library/Spelling/en_US.aff'))
    #Need to consider other languages here
    nlp.add_pipe(hunspell)
    tokens = nltk.word_tokenize(string)
    #Calculate Total Words in string
    total_words = len(tokens)
    for token in tokens:
        #Check for misspelling
        check = nlp(token)[0]
        if check._.hunspell_spell == False:
            #See if word contains leet
            if leetCheck(token):
                #Add to possible candidate list
                leetcandidates.append(token)
    #Test candidate list for word validity using swapping
    for candidate in leetcandidates:
        if swapValid(candidate):
            count = count + 1
    fraction = count//total_words
    #Lazy solution
    fraction = len(leetcandidates)//total_words
    return fraction

# load word lists from text files
def load_most_common_words():
    with open("../misc/most_common_words/de.txt", "r") as f:
        german = f.read().splitlines()
    with open("../misc/most_common_words/en.txt", "r") as f:
        english = f.read().splitlines()
    with open("../misc/most_common_words/es.txt", "r") as f:
        spanish = f.read().splitlines()
    with open("../misc/most_common_words/fr.txt", "r") as f:
        french = f.read().splitlines()
    return dict(DE=german, EN=english, ES=spanish, FR=french)


# determine if the language of a string is most likely to be en, de, fr or es based on a word list approach
# each word list contains the 10000 most common words of the language
#
# word lists are taken from https://github.com/oprogramador/most-common-words-by-language
#
# returns the language
def get_language(string):
    words = nltk.word_tokenize(string)
    counter = dict(DE=0, EN=0, ES=0, FR=0)
    most_common_words = load_most_common_words()
    for word in words:
        if word in most_common_words['DE']:
            counter['DE'] += 1
        if word in most_common_words['EN']:
            counter['EN'] += 1
        if word in most_common_words['ES']:
            counter['ES'] += 1
        if word in most_common_words['FR']:
            counter['FR'] += 1
    return max(counter, key=counter.get)
