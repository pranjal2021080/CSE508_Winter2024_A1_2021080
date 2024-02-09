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
def execute_query(queries, positional_index):
    results = []
    for query in queries:
        query_terms = preprocess_text(query)
        result_set = set()
        for term in query_terms:
            if term in positional_index:
                if len(result_set) == 0:
                    result_set.update(positional_index[term].keys())
                else:
                    result_set.intersection_update(positional_index[term].keys())

        # Filter documents by phrase queries
        phrase_results = []
        for doc in result_set:
            positions = [positional_index[term][doc] for term in query_terms if doc in positional_index[term]]
            for pos in positions[0]:
                if all(pos + i in positions[j] for j, i in enumerate(range(1, len(positions)))):
                    phrase_results.append(doc)

        results.append((len(phrase_results), phrase_results))

    return results


# Function to load positional index using pickle
def load_index(input_path):
    with open(input_path, 'rb') as file:
        positional_index = pickle.load(file)
    return positional_index


# Sample Test Case
queries = [
    "Car bag in a canister",
    "Coffee brewing techniques in cookbook"
]

dataset_path = './data/text_files/'
output_path = 'temp'


positional_index = {}

for filename in os.listdir(dataset_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(dataset_path, filename)
        with open(file_path, 'r') as file:
            text = file.read()
            tokens = preprocess_text(text)
            position = 0
            for token in tokens:
                position += 1
                if token in positional_index:
                    if filename in positional_index[token]:
                        positional_index[token][filename].append(position)
                    else:
                        positional_index[token][filename] = [position]
                else:
                    positional_index[token] = {filename: [position]}
# Save positional index
with open(output_path, 'wb') as file:
    pickle.dump(positional_index, file)

# Load positional index
positional_index = load_index(output_path)

# Execute queries
results = execute_query(queries, positional_index)

# Output results
for i, result in enumerate(results):
    count, documents = result
    print(f"Number of documents retrieved for query {i + 1} using positional index: {count}")
    print(f"Names of documents retrieved for query {i + 1} using positional index: {', '.join(documents)}\n")