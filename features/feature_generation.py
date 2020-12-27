import string

import language_tool_python
import math, re, nltk, features.leetalpha as alpha
from hunspell import Hunspell
from string import punctuation
from fractions import Fraction


class Feature_Generator:
    def __init__(self, string):
        self.string = string
        self.string_lowercase           = self.string.lower()
        self.word_tokens                = nltk.word_tokenize(self.string)
        self.word_tokens_lower          = nltk.word_tokenize(self.string_lowercase)
        self.sentences                  = nltk.sent_tokenize(self.string)
        self.wordcount                  = self.count_words()
        self.language                   = self.get_language()

        with open("misc/emojis/emoji_list", "r") as f:
            self.lines = f.read().splitlines()
            
    ###################################
    ####### HELPER FUNCTIONS ##########
    ###################################

    def reset_string(self, string):
        self.string = string
        self.string_lowercase           = self.string.lower()
        self.word_tokens                = nltk.word_tokenize(self.string)
        self.word_tokens_lower          = nltk.word_tokenize(self.string_lowercase)
        self.sentences                  = nltk.sent_tokenize(self.string)
        self.wordcount                  = self.count_words()

    # count words of a string excluding all punctuation but including emojis
    #TODO EMOJI LIST
    def count_words(self):
        with open("misc/emojis/emoji_list", "r") as f:
            lines = f.read().splitlines()
        counter_include = 0
        for l in lines:
            counter_include += self.string.count(l)
        words = self.word_tokens
        counter_exclude = 0
        for word in words:
            if word in punctuation:
                counter_exclude += 1
        return len(words) - counter_exclude + counter_include

    #TODO emojilits needs to move outside of this module
    # count words of a string excluding all punctuation but including emojis
    def count_words_sentence(self, string):
        with open("misc/emojis/emoji_list", "r") as f:
            lines = f.read().splitlines()
        counter_include = 0
        for l in lines:
            counter_include += string.count(l)
        words = nltk.word_tokenize(string)
        counter_exclude = 0
        for word in words:
            if word in punctuation:
                counter_exclude += 1
        return len(words) - counter_exclude + counter_include

    ###################################
    ####### CHARACTER LEVEL ###########
    ###################################

    # get character frequency for individual letters in a string
    def character_frequency_letters(self):
        char_freq_letters = dict.fromkeys(string.ascii_letters, 0)
        for char in self.string:
            if char in string.ascii_letters:
                char_freq_letters[char] += 1
        for char in char_freq_letters:
            char_freq_letters[char] = char_freq_letters[char] / len(self.string)
        return char_freq_letters


    # get character frequency for individual digits in a string
    def character_frequency_digits(self):
        char_freq_digits = dict.fromkeys(string.digits, 0)
        for char in self.string:
            if char in string.digits:
                char_freq_digits[char] += 1
        for char in char_freq_digits:
            char_freq_digits[char] = char_freq_digits[char] / len(self.string)
        return char_freq_digits

    # get character frequency for individual special characters in a string
    def character_frequency_special_characters(self):
        char_freq_special = dict.fromkeys(string.punctuation, 0)
        for char in self.string:
            if char in string.punctuation:
                char_freq_special[char] += 1
        for char in char_freq_special:
            char_freq_special[char] = char_freq_special[char] / len(self.string)
        return char_freq_special


    # get word length distribution for all words with up to 20 characters in a string
    def word_length_distribution(self):
        word_length_distr = dict.fromkeys(range(0, 21), 0)
        word_tokens = self.word_tokens
        for word in word_tokens:
            if len(word) <= 20 and not word in string.punctuation:
                word_length_distr[len(word)] += 1
        for word_length in word_length_distr:
            word_length_distr[word_length] = (word_length_distr[word_length] / len(self.word_tokens))
        return word_length_distr


    ###################################
    ##### VOCABULARY RICHNESS #########
    ###################################
    #TODO Should we use all lowercase here to identify matches using different capitalization
    #TODO Includes frequency character frequency letters
    #TODO Difference between word_freq and char_freq algorithm? Verify with test cases
    # get word frequency for a string
    def word_frequency(self):
        word_freq = {}

        for word in self.word_tokens_lower:
            if word not in punctuation:
                if word in word_freq:
                    word_freq[word] += 1
                else:
                    word_freq[word] = 1
        return word_freq


    # get number of words with a length larger then l
    # returns a tuple: (total, weighted)
    # TODO: is 10 a good standard value?
    def number_big_words(self, l=10):
        number = 0
        for word in self.word_tokens:
            if len(word) > l:
                number += 1
        return number


    # get number of words appearing i times in a string
    # for hapax legomena: i = 1
    # for hapax dislegomena: i = 2
    # returns a tuple: (total, weighted)
    def number_words_appearing_i_times(self, i=1):
        number = 0
        word_freq = self.word_frequency()
        for word in word_freq:
            if word_freq[word] == i:
                number += 1
        return number


    # get yules k measure for a string
    def yules_k(self):
        n = self.count_words()
        m1 = sum(self.number_words_appearing_i_times(i+1)*(((i+1)/n)**2) for i in range(n))
        m2 = -(1/n)
        return (10**4) * (m2 + m1)


    # get brunets w measure for a string
    def brunets_w(self):
        n = self.count_words()
        vocab_size = self.vocabulary_size()
        a = -0.172
        return n**(vocab_size ** -a)


    # get honores r measure for a string
    def honores_r(self):
        # word_tokens = nltk.word_tokenize(string)
        n = len(self.word_tokens)
        hapax_legomena = self.number_words_appearing_i_times()
        vocab_size = self.vocabulary_size()
        div = hapax_legomena / vocab_size
        if div == 1:
            div = 0.9999999
        return 100 * (math.log(n) / (1 - div))


    ###################################
    ####### SENTENCE LEVEL ############
    ###################################

    # get the average number of characters per sentence for a string
    def average_number_characters_sentence(self):
        exclude = set([".", "?", "!"])
        counter_exclude = 0
        for char in self.string:
            if char in exclude or char.isspace():
                counter_exclude += 1
        return (len(self.string) - counter_exclude) / len(self.sentences)

    # get the average number of lowercase letters per sentence for a string
    def average_number_lowercase_letters_sentence(self):
        counter_lowercase = 0
        for char in self.string:
            if char.islower():
                counter_lowercase += 1
        return (counter_lowercase) / len(self.sentences)


    # get the average number of uppercase letters per sentence for a string
    def average_number_uppercase_letters_sentence(self):
        counter_uppercase = 0
        for char in self.string:
            if char.isupper():
                counter_uppercase += 1
        return (counter_uppercase) / len(self.sentences)


    # get the average number of digits per sentence for a string
    def average_number_digits_sentence(self):
        counter_digits = 0
        for char in self.string:
            if char.isnumeric():
                counter_digits += 1
        return (counter_digits) / len(self.sentences)


    # get the average number of words per sentence for a string
    def average_number_words_sentence(self):
        return self.count_words() / len(self.sentences)


    # get the total number of words per sentence for a string
    def total_number_words_sentence(self):
        total_words_sentence = {}
        sentences = nltk.sent_tokenize(self.string)
        for sentence in sentences:
            total_words_sentence[sentence] = self.count_words_sentence(sentence)
        return total_words_sentence


    ###################################
    ######## PUNCTUATION ##############
    ###################################

    # get the punctuation frequency for a string
    # returns a dict with tuples (total, average)
    def punctuation_frequency(self):
        punc_freq = dict.fromkeys(punctuation, 0)
        for char in self.string:
            if char in punctuation:
                punc_freq[char] += 1
        for char in punc_freq:
            punc_freq[char] = punc_freq[char] / len(self.string)
        return punc_freq


    # get the punctuation frequency per sentence for a string
    # returns a dict per sentence with tuples (total, average)
    def punctuation_frequency_sentence(self):
        punc_freq = dict.fromkeys(punctuation, 0)
        for char in self.string:
            if char in punctuation:
                punc_freq[char] += 1
        for char in punc_freq:
            punc_freq[char] = punc_freq[char] / len(self.sentences)
        return punc_freq


    ###################################
    ######## WHITESPACES ##############
    ###################################

    # get the frequency for the repeated occurrences of whitespaces for a string
    # returns a dict with tuples (total, average)
    def repeated_whitespace(self):
        d = dict.fromkeys(range(0,21), 0)
        whitespaces = re.findall(r"\s+", self.string)
        for w in whitespaces:
            if len(w) > 1 and len(w) < 21:
                d[len(w)] += 1
        for key in d:
            d[key] = d[key] / len(self.string)
        return d


    # get the frequency for the repeated occurrences of whitespaces per sentence for a string
    # returns a dict per sentence with tuples (total, average)
    def repeated_whitespace_sentence(self):
        d = dict.fromkeys(range(0, 21), 0)
        whitespaces = re.findall(r"\s+", self.string)
        for w in whitespaces:
            if len(w) > 1 and len(w) < 21:
                d[len(w)] += 1
        for key in d:
            d[key] = d[key] / len(self.sentences)
        return d


    ###################################
    ######## IDIOSYNCRASY #############
    ###################################

    # get the number of uppercase words for a string
    # returns a tuple: (total, average)
    def uppercase_words(self):
        # words = nltk.word_tokenize(string)
        counter_uppercase = 0
        for word in self.word_tokens:
            if word.istitle():
                counter_uppercase += 1
        return counter_uppercase / self.count_words()


    # get the number of uppercase words per sentence for a string
    # returns a dict with a tuple per sentence: (total, average)
    def uppercase_words_sentence(self):
        counter_uppercase = 0
        for word in self.word_tokens:
            if word.istitle():
                counter_uppercase += 1
        return counter_uppercase / len(self.sentences)


    # get the number of grammar mistakes within a string
    # returns a tuple: (errors, len(matches))
    def grammarCheck(self, language = "en-US"):
        tool = language_tool_python.LanguageTool(language)
        errors = tool.check(self.string)
        return (errors, len(errors))


    # get the number of grammar mistakes within a string
    # returns a tuple: (errors, len(matches))
    def grammarCheck_sentence(self, language = "en-US"):
        dict = {}
        # sentences = nltk.sent_tokenize(string)
        tool = language_tool_python.LanguageTool(language)
        for sentence in self.sentences:
            errors = tool.check(sentence)
            dict[sentence] = (errors, len(errors))
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
    def load_sentiment_lexicon_german(self):
        dict = {}
        with open("misc/sentiment_analysis/de/SentiWS_v2.0_Negative.txt") as f:
            lines = f.read().splitlines()
        for line in lines:
            #TODO check added escape character valid
            line = re.split("\\|.{0,6}\\t|\\t|,", line)
            for word in line[:1] + line[2:]:
                dict[word] = line[1]
        with open("misc/sentiment_analysis/de/SentiWS_v2.0_Positive.txt") as f:
            lines = f.read().splitlines()
        for line in lines:
            line = re.split("\\|.{0,6}\\t|\\t|,", line)
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
    def load_sentiment_lexicon_english(self):
        dict = {}
        with open("misc/sentiment_analysis/en/vader_lexicon.txt") as f:
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
    def load_sentiment_lexicon_spanish(self):
        dict = {}
        with open("misc/sentiment_analysis/es/AFINN-es-111.txt") as f:
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
    def load_sentiment_lexicon_french(self):
        dict = {}
        with open("misc/sentiment_analysis/fr/AFINN-fr-165.txt") as f:
            lines = f.read().splitlines()
        for line in lines:
            line = re.split("\t", line)
            dict[line[0]] = float(line[1]) / 5
        return dict


    # helper function to load the sentiment lexicon
    def load_sentiment_lexicon(self, language):
        if language.upper() == "DE":
            return self.load_sentiment_lexicon_german()
        elif language.upper() == "EN":
            return self.load_sentiment_lexicon_english()
        elif language.upper() == "ES":
            return self.load_sentiment_lexicon_spanish()
        elif language.upper() == "FR":
            return self.load_sentiment_lexicon_french()


    # perform sentiment analysis based on a lexicon approach for a string
    # result is a value between -1 and +1 where +1 is positive and -1 is negative
    # returns the average per word
    def sentiment_analysis_word_average(self):
        sentiment_lexicon = self.load_sentiment_lexicon(self.language)
        # words = nltk.word_tokenize(self.string.lower)
        words = self.word_tokens_lower
        result = 0.0
        for word in words:
            if word in sentiment_lexicon:
                result += float(sentiment_lexicon[word])
        return result / self.count_words()


    # perform sentiment analysis based on a lexicon approach for a string
    # result is a value between -1 and +1 where +1 is positive, 0 is neutral and -1 is negative
    # returns the average per sentence
    # def sentiment_analysis_sentence_average(self, language="EN"):
    #     sentiment_lexicon = self.load_sentiment_lexicon(language)
    #     sentences = nltk.sent_tokenize(self.string_lowercase)
    #     dict = {}
    #     for sentence in sentences:
    #         result = 0.0
    #         words = nltk.word_tokenize(sentence)
    #         for word in words:
    #             if word in sentiment_lexicon:
    #                 result += float(sentiment_lexicon[word])
    #         #TODO Count_word for sentences
    #         dict[sentence] = result / self.count_words_sentence(sentence)
    #     return dict

    def sentiment_analysis_sentence_average(self):
        sentiment_lexicon = self.load_sentiment_lexicon(self.language)
        # words = nltk.word_tokenize(self.string.lower)
        words = self.word_tokens_lower
        result = 0.0
        for word in words:
            if word in sentiment_lexicon:
                result += float(sentiment_lexicon[word])
        return result / len(self.sentences)

    # def sentiment_analysis_sentence_average2(self, string, language="EN"):
    #     sentiment_lexicon = self.load_sentiment_lexicon(language)
    #     sentences = nltk.sent_tokenize(string.lower())
    #     dict = {}
    #     for sentence in sentences:
    #         result = 0.0
    #         words = nltk.word_tokenize(sentence)
    #         for word in words:
    #             if word in sentiment_lexicon:
    #                 result += float(sentiment_lexicon[word])
    #         dict[sentence] = result / self.count_words_sentence(sentence)
    #     return dict

    ###################################
    ##### ADDITIONAL FEATURES #########
    ###################################

    # get the emoji frequency for a string
    # returns a dict with tuples per emoji: tuple (total, average)
    def emoji_frequency_word(self):
        d = dict.fromkeys(self.lines, 0)
        for l in self.lines:
            emojis_counter = self.string.count(l)
            if emojis_counter > 0:
                d[l] = emojis_counter
        for emoji in d:
            d[emoji] = d[emoji] / self.count_words()
        return d


    # get the emoji frequency for a string
    # returns a dict with tuples per sentence and emoji: tuple (total, average)
    def emoji_frequency_sentence(self):
        # with open("misc/emojis/emoji_list", "r") as f:
        #     lines = f.read().splitlines()
        d = dict.fromkeys(self.lines, 0)
        for l in self.lines:
            emojis_counter = self.string.count(l)
            if emojis_counter > 0:
                d[l] = emojis_counter
        for emoji in d:
            d[emoji] = d[emoji] / len(self.sentences)
        return d

    ###################################
    ####### LEETSPEAK ################
    ###################################

    # def leetspeak_sentence(string):
    #     valDict = dictionary_values_as_keys(alpha.leet_alphabet)

    #     # total per sentence
    #     tots_per_sentence = total_number_words_sentence(string)
    #     punkt_st = nltk.tokenize.PunktSentenceTokenizer()
    #     sentence_list = punkt_st.tokenize(string)
    #     # Sentence Level Check
    #     sentence_level_leet = leetScan(sentence_list, valDict)
    #     # Full Text Level Search
    #     # text_level_leet = leetScan(string)
    #     return sentence_level_leet


    # Builds a dictionary with values from input dictionary mapped as keys.
    # input: Dictionary
    # output: Dictionary
    def dictionary_values_as_keys(self, dict):
        keysDict = {}
        for key, values in dict.items():
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

    # Checks leet alphabet dictionary values for token
    # input: String
    # output: True/False
    def leetCheck(self):
        status = False
        for lValues in alpha.leet_alphabet.values():
            for leet in lValues:
                if leet in self.string:
                    status = True
                    return status
        return status

    # Lets play a game.
    # input: String
    # output: True/False
    def swapValid(token, valDict,h):
        status = False
        for lValues in alpha.leet_alphabet.values():
            for leet in lValues:
                if leet in token:
                    #Logic
                    for l in valDict[leet]:
                        otherStr = copyToken.replace(leet , str(valDict[leet][0]))
                        #If spelled correctly, we test, otherwise try again. Perfect recursion case.
                        #Check for misspelling
                        if h.spell(otherStr) == True:
                            status = True
                            print(otherStr)
                            return status    
        return status


    # Checks what percentage of words are potential leetwords
    # input: String, language = "EN"
    # output: Fraction(1, 24) object

    def leetScan(string, valDict, language="EN" ):
        leetcandidates = []
        count = 0
        h = Hunspell('en_US', hunspell_data_dir='/Library/Spelling')
        tokens = nltk.word_tokenize(string)
        # Calculate Total Words in string
        total_words = len(tokens)
        for token in tokens:
            # Check for misspelling
            if h.spell(token)== False:
                # See if word contains leet
                if leetCheck(token):
                    # Add to possible candidate list
                    leetcandidates.append(token)
        # Test candidate list for word validity using swapping
        for candidate in leetcandidates:
            if swapValid(candidate, valDict,h):
                count = count + 1
        fraction = Fraction(count,total_words)
        return fraction

    # load word lists from text files
    def load_most_common_words(self):
        with open("misc/most_common_words/de.txt", "r") as f:
            german = f.read().splitlines()
        with open("misc/most_common_words/en.txt", "r") as f:
            english = f.read().splitlines()
        with open("misc/most_common_words/es.txt", "r") as f:
            spanish = f.read().splitlines()
        with open("misc/most_common_words/fr.txt", "r") as f:
            french = f.read().splitlines()
        return dict(DE=german, EN=english, ES=spanish, FR=french)


    # determine if the language of a string is most likely to be en, de, fr or es based on a word list approach
    # each word list contains the 10000 most common words of the language
    #
    # word lists are taken from https://github.com/oprogramador/most-common-words-by-language
    #
    # returns the language
    def get_language(self):
        words = self.word_tokens_lower
        counter = dict(DE=0, EN=0, ES=0, FR=0)
        most_common_words = self.load_most_common_words()
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

    # get the number of all capital words for a string
    # returns a tuple: (total, average)
    def all_capital_words(self):
        # words = nltk.word_tokenize(string)
        counter_all_capital = 0
        for word in self.word_tokens:
            if word.isupper():
                counter_all_capital += 1
        return counter_all_capital


    # get the number of all capital words per sentence for a string
    # returns a dict with a tuple per sentence: (total, average)
    def all_capital_words_sentence(self):
        dict = {}
        # sentences = nltk.sent_tokenize(string)
        for sentence in self.sentences:
            words = nltk.word_tokenize(sentence)
            counter_all_capital = 0
            for word in words:
                if word.isupper():
                    counter_all_capital += 1
            dict[sentence] = counter_all_capital
        return dict


    # get the vocabulary size for a string
    def vocabulary_size(self):
        # string = string.lower()
        vocab = set()
        # words = nltk.word_tokenize(string)
        words = self.word_tokens_lower
        for word in words:
            if not word in punctuation:
                vocab.add(word)
        return len(vocab)


    # get the mean word frequency
    def mean_word_frequency(self):
        return self.count_words() / self.vocabulary_size()


    # get the type token ratio
    def type_token_ratio(self):
        return self.vocabulary_size() / self.count_words()


    # get sichels s measure
    #
    # Sichel (1975) observed that the ratio of dis legomena, V (2, N ) to the vocabulary
    # size is roughly constant across a wide range of sample sizes
    def sichels_s(self):
        hapax_dislegomena = self.number_words_appearing_i_times(2)
        vocab_size = self.vocabulary_size()
        return hapax_dislegomena / vocab_size