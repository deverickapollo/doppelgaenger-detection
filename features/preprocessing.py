from nltk.corpus import stopwords
import nltk, spacy
from nltk.tokenize.treebank import TreebankWordDetokenizer

stop_words_dict = dict(EN=set(stopwords.words('english')),
                       ES=set(stopwords.words('spanish')),
                       DE=set(stopwords.words('german')),
                       FR=set(stopwords.words('french')))
spacy_models_dict = dict(EN="en_core_web_sm",
                         ES="es_core_news_sm",
                         DE="de_core_news_sm",
                         FR="fr_core_news_sm")

# detokenize a list of word tokens and return a string
def detokenize(words):
    return TreebankWordDetokenizer().detokenize(words)

# remove stop words from a string
def remove_stop_words(string, language = "EN"):
    word_tokens = nltk.word_tokenize(string)
    return detokenize([word for word in word_tokens if not word in stop_words_dict.get(language.upper())])

# lemmatize string
def lemmatize(string, language = "EN"):
    nlp = spacy.load(spacy_models_dict.get(language.upper()))
    s = nlp(string)
    return detokenize([word.lemma_ for word in s])
