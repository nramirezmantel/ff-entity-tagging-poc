# functions to read raw docs and entities with
NUM_CHUNKS = 6

def read_raw_docs(root_folder, extensions=['.txt']):
    """
    Reads files recursively from a root folder.
    
    :param root_folder: The root folder to start searching.
    :param extensions: Optional list of file extensions to filter (e.g., ['.txt', '.md']).
    """
    corpus = ''
    for dirpath, _, filenames in os.walk(root_folder):
        print(dirpath)
        for filename in filenames:
            print(filename)
            if extensions is None or any(filename.endswith(ext) for ext in extensions):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        print(f"Reading {file_path}")
                        corpus += file.read()
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    return corpus

def read_json_docs(root_folder, extensions=[".json"]):
    """
    Reads JSON files recursively from a root folder and merges their contents into a single dictionary,
    extending list values for shared keys.
    
    :param root_folder: The root folder to start searching.
    :param extensions: Optional list of file extensions to filter (default: ['.json']).
    :return: A dictionary containing the merged content of all JSON files.
    """
    if extensions is None:
        raise ValueError(f"no file extension provided. Can't read.")

    merged_dict = {}
    for dirpath, _, filenames in os.walk(root_folder):
        print(dirpath)
        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        if "_cleaned.json" in file_path:
                            print(f"Reading {file_path}")
                            file_content = json.load(file)
                            if not isinstance(file_content, dict) or not all(isinstance(v, list) for v in file_content.values()):
                                raise ValueError(f"Expected a dictionary with list values in {file_path}.")
                            for key, new_value in file_content.items():
                                if key in merged_dict:
                                    print(f"extending {key} with {new_value}")
                                    merged_dict[key].extend(new_value)  # Extend the list
                                    print(f"merged_dict[key] new: {merged_dict[key]}")
                                    pass
                                else:
                                    print(f"initialising: {key}")
                                    merged_dict[key] = new_value  # Add new key-value pair if it doesn't exist
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    return merged_dict

# Usage
docs = read_raw_docs(RAW_TEXT_DIR)
entities = read_json_docs(ENTITIES_DIR)

print(docs[:100])
docs = docs.replace("\n", " ")

# print number of characters in corpus - spacy has to work with <1mil characters
print(f"number of characters in our corpus: {len(docs)}")

# establish a dictionary of entity categories - for training spaCy custom NER later (per doc)
ent_patterns_list = [] # global scope
for ent_category, ent_list in entities.items():
    for ent in ent_list:
        # gets rid of empty entities
        if ent != '':
            ent_patterns_list.append(
                # {"label": ent_category, "pattern": [{"lower": ent}]}
                {"label": ent_category, "pattern": ent}
            )
print(ent_patterns_list[:10])

# spacy can only work with chunks <1mil characters at a time. chunk the corpus below
def divide_string_into_n_chunks(input_string, num_chunks):
    """
    Divides a string into `num_chunks` chunks and stores them in a dictionary.

    :param input_string: The string to be divided.
    :param num_chunks: The number of chunks.
    :return: A dictionary where the keys are indices, and the values are string chunks.
    """
    # Calculate the chunk size (integer division)
    chunk_size = len(input_string) // num_chunks
    remainder = len(input_string) % num_chunks
    
    # Dictionary to store chunks
    chunks_dict = {}
    start_index = 0

    for i in range(num_chunks):
        # Calculate the end index for the current chunk
        end_index = start_index + chunk_size + (1 if i < remainder else 0)  # Distribute remainder evenly
        chunks_dict[i] = input_string[start_index:end_index]
        start_index = end_index  # Update start index for next chunk
    
    return chunks_dict

# Example usage:
doc_chunk_dict = divide_string_into_n_chunks(docs, NUM_CHUNKS)

print(f"number of items in our full train-test dataset: {len(TRAIN_TEST_DATASET)}")

# Original data
import random

# Create a shuffled copy
shuffled_data = random.sample(TRAIN_TEST_DATASET, len(TRAIN_TEST_DATASET))

# Split into 80% for training and 20% for testing
split_index = int(0.8 * len(shuffled_data))
TRAIN_DATA = shuffled_data[:split_index]
TEST_DATA = shuffled_data[split_index:]

print("Original data unchanged:", TRAIN_TEST_DATASET)
print("Shuffled data:", shuffled_data)

# entity categories in train and test data

def count_entity_categories(data):
    result_dict = {}
    for sent, annotations in data:
        # print(annotations)
        for annot in annotations['entities']:
            ent_category = annot[2]
            if ent_category not in result_dict:
                result_dict[ent_category] = 1
            else:
                # print(f"ent category: {ent_category} has count: {result_dict[ent_category]}")
                result_dict[ent_category] += 1
    return result_dict
    
# print out # of senteces in train and test sets
print(f"# of elements in train data: {len(TRAIN_DATA)}")
print(f"# of elements in test data: {len(TEST_DATA)}")

print(f"Training dataset (number of entities):")
train_analysis = count_entity_categories(TRAIN_DATA)
print(train_analysis)
print(f"Testing dataset (number of entities):")
test_analysis = count_entity_categories(TEST_DATA)
print(test_analysis)

# saving train and test data to pickle files
import pickle

with open('TRAIN-ic-mrc-arc-large-batch.pkl', 'wb') as train_file:
    pickle.dump(TRAIN_DATA, train_file)

with open('TEST-ic-mrc-arc-large-batch.pkl', 'wb') as test_file:
    pickle.dump(TEST_DATA, test_file)