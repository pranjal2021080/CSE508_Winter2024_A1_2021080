dataset_directory = '/content/drive/MyDrive/text_files'

#random array for storing indices
# import random
# random_array = []
# for _ in range(5):
#     random_number = random.randint(1, 999)
#     random_array.append(random_number)
# print(random_array)

# Define function for preprocessing
def preprocess_text(text):
    dataset_path = '/content/drive/MyDrive/text_files'


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

# Process each file in the dataset
dataset_path = '/text_files'
output_path = '/preprocessed_data'

# Create output directory if it doesn't exist
if not os.path.exists(output_path):
    os.makedirs(output_path)

for filename in os.listdir(dataset_path):
    if filename.endswith(".txt"):
        input_file_path = os.path.join(dataset_path, filename)
        output_file_path = os.path.join(output_path, filename)

        with open(input_file_path, 'r') as input_file:
            text = input_file.read()
            processed_text = preprocess_text(text)

            # Write processed text to new file
            with open(output_file_path, 'w') as output_file:
                output_file.write(' '.join(processed_text))
# print(len(os.listdir(dataset_path)))