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
