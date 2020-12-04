import math, nltk, features.leetalpha

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
    return char_freq_special

# get character frequency for all individual characters in a string
def character_frequency(string):
    char_freq = {}
    for char in string:
        if char in char_freq:
            char_freq[char] += 1
        else:
            char_freq[char] = 1
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
def number_big_words(string, l = 10):
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
def number_words_appearing_i_times(string, i = 1):
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
        return 100 * (math.log(n)/ (1 - hapax_legomena_weighted))

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
    exclude = set([".", "?", "!"])
    counter_words = 0
    sentences = nltk.sent_tokenize(string)
    for sentence in sentences:
        sentence = nltk.word_tokenize(sentence)
        for word in sentence:
            if word not in exclude:
                counter_words += 1
    return counter_words / len(sentences)

# get the total number of words per sentence for a string
def total_number_words_sentence(string):
    exclude = set([".", "?", "!"])
    total_words_sentence = {}
    sentences = nltk.sent_tokenize(string)
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        for word in words:
            if word not in exclude:
                if sentence in total_words_sentence:
                    total_words_sentence[sentence] += 1
                else:
                    total_words_sentence[sentence] = 1
    return total_words_sentence
