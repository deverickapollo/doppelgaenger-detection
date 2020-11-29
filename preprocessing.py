from nltk.corpus import stopwords
import nltk
import spacy

stop_words_dict = dict(EN=set(stopwords.words('english')),
                       ES=set(stopwords.words('spanish')),
                       DE=set(stopwords.words('german')),
                       FR=set(stopwords.words('french')))
spacy_models_dict = dict(EN="en_core_web_sm",
                         ES="es_core_news_sm",
                         DE="de_core_news_sm",
                         FR="fr_core_news_sm")

# remove stop words from a string and return a list of words
def remove_stop_words(string, language = "EN"):
    word_tokens = nltk.word_tokenize(string)
    return [word for word in word_tokens if not word in stop_words_dict.get(language.upper())]

# lemmatize string and return a list of words
def lemmatize(string, language = "EN"):
    nlp = spacy.load(spacy_models_dict.get(language.upper()))
    s = nlp(string)
    return [word.lemma_ for word in s]
