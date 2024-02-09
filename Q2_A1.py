import os
import pickle
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import nltk

nltk.download('stopwords')
nltk.download('punkt')
# Function to preprocess text
def preprocess_text(text):
    # Lowercase the text
    text = text.lower()

    # Remove HTML tags using BeautifulSoup
    text = BeautifulSoup(text, "html.parser").get_text()

    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]

    # Remove punctuations
    tokens = [word for word in tokens if word not in string.punctuation]

    # Remove blank space tokens
    tokens = [word for word in tokens if word.strip()]

    return tokens


# Function to execute query operations
def execute_query(queries, inverted_index):
    results = []
    for query in queries:
        query_terms = preprocess_text(query[0])
        operations = query[1].split(', ')
        result_set = set()

        for term in query_terms:
            if term in inverted_index:
                if len(result_set) == 0:
                    result_set.update(inverted_index[term])
                else:
                    if 'AND' in operations:
                        result_set.intersection_update(inverted_index[term])
                    elif 'OR' in operations:
                        result_set.update(inverted_index[term])
                    elif 'NOT' in operations:
                        result_set.difference_update(inverted_index[term])
        
        results.append((query[0], len(result_set), list(result_set)))
    
    return results

# Function to load inverted index using pickle
def load_index(input_path):
    with open(input_path, 'rb') as file:
        inverted_index = pickle.load(file)
    return inverted_index

# Sample Test Case
queries = [
    ("Car bag in a canister", "OR, AND NOT"),
    ("Coffee brewing techniques in cookbook", "AND, OR NOT, OR")
]

dataset_path = './data/text_files'
output_path = './temp'

# Create inverted index
# inverted_index = create_inverted_index(dataset_path)
inverted_index = {}

for filename in os.listdir(dataset_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(dataset_path, filename)
        with open(file_path, 'r') as file:
            text = file.read()
            tokens = preprocess_text(text)
            for token in tokens:
                if token in inverted_index:
                    if filename not in inverted_index[token]:
                        inverted_index[token].append(filename)
                else:
                    inverted_index[token] = [filename]
# Save inverted index
                    
with open(output_path, 'wb') as file:
    pickle.dump(inverted_index, file)


# Load inverted index
inverted_index = load_index(output_path)

# Execute queries
results = execute_query(queries, inverted_index)

# Output results
for i, result in enumerate(results):
    query, count, documents = result
    print(f"Query {i+1}: {query}")
    print(f"Number of documents retrieved for query {i+1}: {count}")
    print(f"Names of the documents retrieved for query {i+1}: {' '.join(documents)}\n")