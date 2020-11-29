from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words('english'))

# remove stop words from a string and return a list
def remove_stop_words(comment_text):
    word_tokens = word_tokenize(comment_text)
    comment_text_filtered = [word for word in word_tokens if not word in stop_words]
    return comment_text_filtered

