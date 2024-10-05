# import nltk
# from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# from nltk.stem import PorterStemmer

# nltk.download('punkt_tab')
# nltk.download('stopwords')

# ps = PorterStemmer()
# stop_words = set(stopwords.words('english'))

# def preprocess_text(text):
#     tokens = word_tokenize(text.lower())
#     filtered_tokens = [ps.stem(word) for word in tokens if word.isalpha() and word not in stop_words]
#     return filtered_tokens


import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')  # Optional: to get additional languages


from nltk.stem import WordNetLemmatizer

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    tokens = word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens if token.isalpha()]
    return lemmatized_tokens
