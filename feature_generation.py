import nltk


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