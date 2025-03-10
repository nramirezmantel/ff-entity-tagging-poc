"""
Feature engineering for training data
Processes raw text and entity data to create training and test datasets
"""
import os
import json
import random
import pickle
import argparse


def read_raw_docs(root_folder, extensions=['.txt'], verbose=False):
    """
    Reads files recursively from a root folder.
    
    Args:
        root_folder (str): The root folder to start searching.
        extensions (list): Optional list of file extensions to filter (e.g., ['.txt', '.md']).
        verbose (bool): Whether to print verbose output
        
    Returns:
        str: Combined corpus from all files
    """
    corpus = ''
    for dirpath, _, filenames in os.walk(root_folder):
        if verbose:
            print(dirpath)
        for filename in filenames:
            if verbose:
                print(filename)
            if extensions is None or any(filename.endswith(ext) for ext in extensions):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        if verbose:
                            print(f"Reading {file_path}")
                        corpus += file.read()
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    return corpus


def read_json_docs(root_folder, extensions=[".json"], verbose=False):
    """
    Reads JSON files recursively from a root folder and merges their contents into a single dictionary,
    extending list values for shared keys.
    
    Args:
        root_folder (str): The root folder to start searching.
        extensions (list): Optional list of file extensions to filter (default: ['.json']).
        verbose (bool): Whether to print verbose output
        
    Returns:
        dict: A dictionary containing the merged content of all JSON files.
    """
    if extensions is None:
        raise ValueError("No file extension provided. Can't read.")

    merged_dict = {}
    for dirpath, _, filenames in os.walk(root_folder):
        if verbose:
            print(dirpath)
        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        if "_cleaned.json" in file_path:
                            if verbose:
                                print(f"Reading {file_path}")
                            file_content = json.load(file)
                            if not isinstance(file_content, dict) or not all(isinstance(v, list) for v in file_content.values()):
                                raise ValueError(f"Expected a dictionary with list values in {file_path}.")
                            for key, new_value in file_content.items():
                                if key in merged_dict:
                                    if verbose:
                                        print(f"extending {key} with {new_value}")
                                    merged_dict[key].extend(new_value)  # Extend the list
                                    if verbose:
                                        print(f"merged_dict[key] new: {merged_dict[key]}")
                                else:
                                    if verbose:
                                        print(f"initialising: {key}")
                                    merged_dict[key] = new_value  # Add new key-value pair if it doesn't exist
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    return merged_dict


def divide_string_into_n_chunks(input_string, num_chunks):
    """
    Divides a string into `num_chunks` chunks and stores them in a dictionary.

    Args:
        input_string (str): The string to be divided.
        num_chunks (int): The number of chunks.
        
    Returns:
        dict: A dictionary where the keys are indices, and the values are string chunks.
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


def create_entity_patterns(entities):
    """
    Create entity patterns for spaCy NER training
    
    Args:
        entities (dict): Dictionary of entity categories and their values
        
    Returns:
        list: List of entity patterns
    """
    ent_patterns_list = []
    for ent_category, ent_list in entities.items():
        for ent in ent_list:
            # gets rid of empty entities
            if ent != '':
                ent_patterns_list.append(
                    {"label": ent_category, "pattern": ent}
                )
    return ent_patterns_list


def count_entity_categories(data):
    """
    Count entity categories in the dataset
    
    Args:
        data (list): List of (text, annotations) tuples
        
    Returns:
        dict: Dictionary of entity categories and their counts
    """
    result_dict = {}
    for _, annotations in data:
        for annot in annotations['entities']:
            ent_category = annot[2]
            if ent_category not in result_dict:
                result_dict[ent_category] = 1
            else:
                result_dict[ent_category] += 1
    return result_dict


def process_data(raw_text_dir, entities_dir, train_output, test_output, num_chunks=6, verbose=False):
    """
    Process raw text and entity data to create training and test datasets
    
    Args:
        raw_text_dir (str): Directory containing raw text files
        entities_dir (str): Directory containing entity JSON files
        train_output (str): Path to save training data pickle file
        test_output (str): Path to save test data pickle file
        num_chunks (int): Number of chunks to divide the corpus into
        verbose (bool): Whether to print verbose output
        
    Returns:
        tuple: (train_data, test_data)
    """
    # Read raw docs and entities
    docs = read_raw_docs(raw_text_dir, verbose=verbose)
    entities = read_json_docs(entities_dir, verbose=verbose)
    
    if verbose:
        print(docs[:100])
    
    # Clean up docs
    docs = docs.replace("\n", " ")
    
    if verbose:
        print(f"Number of characters in our corpus: {len(docs)}")
    
    # Create entity patterns
    ent_patterns_list = create_entity_patterns(entities)
    
    if verbose:
        print("Sample entity patterns:")
        print(ent_patterns_list[:10])
    
    # Divide corpus into chunks
    doc_chunk_dict = divide_string_into_n_chunks(docs, num_chunks)
    
    # TODO: This part is incomplete in the original script
    # We need to create TRAIN_TEST_DATASET from doc_chunk_dict and ent_patterns_list
    # For now, we'll assume it's a placeholder and create a dummy dataset
    
    # This is a placeholder - in a real implementation, you would create actual training data
    # from the documents and entity patterns
    train_test_dataset = []
    
    # If there's no data, return empty lists
    if not train_test_dataset:
        print("Warning: No training data was created. This is likely because the original script was incomplete.")
        print("You'll need to implement the logic to create the training dataset from the documents and entity patterns.")
        return [], []
    
    # Create a shuffled copy
    shuffled_data = random.sample(train_test_dataset, len(train_test_dataset))
    
    # Split into 80% for training and 20% for testing
    split_index = int(0.8 * len(shuffled_data))
    train_data = shuffled_data[:split_index]
    test_data = shuffled_data[split_index:]
    
    if verbose:
        print(f"Number of items in our full train-test dataset: {len(train_test_dataset)}")
        print(f"# of elements in train data: {len(train_data)}")
        print(f"# of elements in test data: {len(test_data)}")
        
        print(f"Training dataset (number of entities):")
        train_analysis = count_entity_categories(train_data)
        print(train_analysis)
        print(f"Testing dataset (number of entities):")
        test_analysis = count_entity_categories(test_data)
        print(test_analysis)
    
    # Create output directories if they don't exist
    os.makedirs(os.path.dirname(train_output) or '.', exist_ok=True)
    os.makedirs(os.path.dirname(test_output) or '.', exist_ok=True)
    
    # Save train and test data to pickle files
    with open(train_output, 'wb') as train_file:
        pickle.dump(train_data, train_file)
    
    with open(test_output, 'wb') as test_file:
        pickle.dump(test_data, test_file)
    
    print(f"Training data saved to {train_output}")
    print(f"Test data saved to {test_output}")
    
    return train_data, test_data


def main():
    """Main function to run the script"""
    parser = argparse.ArgumentParser(description="Feature engineering for training data")
    parser.add_argument("--raw-text", required=True, 
                        help="Directory containing raw text files")
    parser.add_argument("--entities", required=True, 
                        help="Directory containing entity JSON files")
    parser.add_argument("--train-output", default="TRAIN-ic-mrc-arc-large-batch.pkl", 
                        help="Path to save training data pickle file")
    parser.add_argument("--test-output", default="TEST-ic-mrc-arc-large-batch.pkl", 
                        help="Path to save test data pickle file")
    parser.add_argument("--chunks", type=int, default=6, 
                        help="Number of chunks to divide the corpus into")
    parser.add_argument("--verbose", action="store_true", 
                        help="Print verbose output")
    
    args = parser.parse_args()
    
    process_data(
        args.raw_text, 
        args.entities, 
        args.train_output, 
        args.test_output, 
        args.chunks, 
        args.verbose
    )


if __name__ == "__main__":
    main()
