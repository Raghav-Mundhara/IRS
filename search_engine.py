import os
import glob
import math
from collections import defaultdict, Counter
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import PyPDF2
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')  # Optional: to get additional languages

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Initialize the stemmer
stemmer = PorterStemmer()

# Function to read documents from the specified directory (including the root folder)
def read_documents_from_folder(folder_path=''):
    documents = {}
    
    # If no folder path is provided, assume the current working directory (root folder)
    if folder_path == '':
        folder_path = os.getcwd()  # Get the current working directory
    
    # Read all text files in the folder
    # for filepath in glob.glob(os.path.join(folder_path, "*.txt")):
    #     with open(filepath, 'r', encoding='utf-8') as file:
    #         content = file.read()
    #         tokens = word_tokenize(content)  # Tokenize using NLTK
    #         print(tokens)
    #         stemmed_tokens = [stemmer.stem(token.lower()) for token in tokens if token.isalpha()]  # Stem and filter out non-alphabetic tokens
    #         print(stemmed_tokens)
    #         documents[os.path.basename(filepath)] = stemmed_tokens
    # Read all PDF files in the folder
    for filepath in glob.glob(os.path.join(folder_path, "*.pdf")):
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            content = ''
            for page in reader.pages:
                content += page.extract_text() or ''  # Extract text from each page
            tokens = word_tokenize(content)
            lemmatized_tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens if token.isalpha()]
            print(lemmatized_tokens)  # Print lemmatized tokens for verification
            documents[os.path.basename(filepath)] = lemmatized_tokens
    # print(documents)
    return documents

# Function to build an inverted index for document searching
def build_inverted_index(documents):
    inverted_index = defaultdict(list)
    for doc_id, tokens in documents.items():
        for token in tokens:
            inverted_index[token].append(doc_id)
    return inverted_index

# Function to compute term frequency (TF) for a document
def compute_tf(document):
    tf = Counter(document)
    total_terms = len(document)
    for term in tf:
        tf[term] = tf[term] / total_terms
    return tf

# Function to compute inverse document frequency (IDF) for all documents
def compute_idf(documents):
    idf = {}
    total_docs = len(documents)
    for document in documents.values():
        for term in set(document):
            if term not in idf:
                idf[term] = 0
            idf[term] += 1
    for term in idf:
        idf[term] = math.log(total_docs / idf[term])
    return idf

# Function to compute TF-IDF for all documents
def compute_tfidf(documents):
    idf = compute_idf(documents)
    tfidf_documents = defaultdict(dict)
    for doc_id, document in documents.items():
        tf = compute_tf(document)
        for term in tf:
            tfidf_documents[term][doc_id] = tf[term] * idf[term]  # Store by term and doc_id
    return tfidf_documents

# Search for relevant documents based on the query tokens and TF-IDF values
def search_documents(query_tokens, tfidf_documents):
    relevant_docs = defaultdict(float)
    for token in query_tokens:
        if token in tfidf_documents:
            for doc_id, tfidf_score in tfidf_documents[token].items():
                relevant_docs[doc_id] += tfidf_score
    sorted_docs = sorted(relevant_docs.items(), key=lambda x: x[1], reverse=True)
    return sorted_docs


