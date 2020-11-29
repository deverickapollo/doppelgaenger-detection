from nltk.corpus import stopwords, wordnet
import nltk

stop_words = set(stopwords.words('english'))
tag_dict = {"J": wordnet.ADJ,
            "R": wordnet.ADV,
            "N": wordnet.NOUN,
            "V": wordnet.VERB}

# helper function to map nltks pos tag to wordnets pos tag
def get_pos_tag_wordnet(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    return tag_dict.get(tag, wordnet.NOUN)

# remove stop words from a string and return a list of strings
def remove_stop_words(string):
    word_tokens = nltk.word_tokenize(string)
    return [word for word in word_tokens if not word in stop_words]

# lemmatize words from a  string and return a list of strings
def lemmatize_words(string):
    word_tokens = nltk.word_tokenize(string)
    word_net_lemmatizer = nltk.WordNetLemmatizer()
    return [word_net_lemmatizer.lemmatize(word, get_pos_tag_wordnet(word)) for word in word_tokens]
