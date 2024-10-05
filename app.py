from flask import Flask, jsonify, request, render_template
from search_engine import read_documents_from_folder, compute_tfidf, search_documents
from text_preprocessing import preprocess_text
app = Flask(__name__)

# Load and process documents when the app starts
documents = read_documents_from_folder()  # Load documents
tfidf_documents = compute_tfidf(documents)  # Compute TF-IDF for loaded documents

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()  # Get JSON data from the request body
    query = data.get('query')  # Extract 'query' from the JSON payload
    
    if not query:
        return jsonify({"error": "Query not provided"}), 400

    query_tokens = preprocess_text(query)  # Preprocess the query
    results = search_documents(query_tokens, tfidf_documents)  # Search using TF-IDF
    
    # Return the search results in JSON format
    return jsonify({"query": query, "results": results}), 200

if __name__ == '__main__':
    app.run(debug=True)
