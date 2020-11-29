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


# get character frequency for individual digits in a string
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
    char_freq_letters = character_frequency_letters(string)
    char_freq_digits = character_frequency_digits(string)
    char_freq_special = character_frequency_special_characters(string)
    char_freq_letters.update(char_freq_digits)
    char_freq_letters.update(char_freq_special)
    return char_freq_letters
