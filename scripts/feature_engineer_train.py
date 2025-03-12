"""
Feature engineering for training data: Processes raw text and entity data to create datasets
"""
import json
import random
import pickle
import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional, Union

# Type aliases for better readability
EntityPattern = Dict[str, str]
TrainingExample = Tuple[str, Dict[str, List[Tuple[int, int, str]]]]


def read_raw_docs(
    root_folder: Union[str, Path], 
    extensions: List[str] = ['.txt'], 
    verbose: bool = False
) -> str:
    """Reads files recursively from a root folder and combines their content"""
    root_path = Path(root_folder)
    corpus = ''
    
    for file_path in root_path.rglob('*'):
        if not file_path.is_file():
            continue
            
        if extensions is None or any(file_path.suffix.lower() == ext.lower() for ext in extensions):
            if verbose:
                print(f"Reading {file_path}")
                
            try:
                corpus += file_path.read_text(encoding='utf-8')
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                
    return corpus


def read_json_docs(
    root_folder: Union[str, Path], 
    extensions: List[str] = [".json"], 
    verbose: bool = False
) -> Dict[str, List[Any]]:
    """Reads JSON files recursively and merges their contents into a single dictionary"""
    if extensions is None:
        raise ValueError("No file extension provided. Can't read.")

    root_path = Path(root_folder)
    merged_dict: Dict[str, List[Any]] = {}
    
    for file_path in root_path.rglob('*'):
        if not file_path.is_file():
            continue
            
        if any(file_path.suffix.lower() == ext.lower() for ext in extensions):
            if "_cleaned.json" not in str(file_path):
                continue
                
            try:
                if verbose:
                    print(f"Reading {file_path}")
                    
                file_content = json.loads(file_path.read_text(encoding='utf-8'))
                
                if not isinstance(file_content, dict) or not all(isinstance(v, list) for v in file_content.values()):
                    raise ValueError(f"Expected a dictionary with list values in {file_path}.")
                    
                for key, new_value in file_content.items():
                    if key in merged_dict:
                        if verbose:
                            print(f"extending {key} with {new_value}")
                        merged_dict[key].extend(new_value)
                        if verbose:
                            print(f"merged_dict[key] new: {merged_dict[key]}")
                    else:
                        if verbose:
                            print(f"initialising: {key}")
                        merged_dict[key] = new_value
                        
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                
    return merged_dict


def divide_string_into_n_chunks(input_string: str, num_chunks: int) -> Dict[int, str]:
    """Divides a string into `num_chunks` chunks and stores them in a dictionary"""
    chunk_size = len(input_string) // num_chunks
    remainder = len(input_string) % num_chunks
    
    chunks_dict: Dict[int, str] = {}
    start_index = 0

    for i in range(num_chunks):
        end_index = start_index + chunk_size + (1 if i < remainder else 0)
        chunks_dict[i] = input_string[start_index:end_index]
        start_index = end_index
    
    return chunks_dict


def create_entity_patterns(entities: Dict[str, List[str]]) -> List[EntityPattern]:
    """Create entity patterns for spaCy NER training"""
    return [
        {"label": ent_category, "pattern": ent}
        for ent_category, ent_list in entities.items()
        for ent in ent_list
        if ent != ''
    ]


def count_entity_categories(data: List[TrainingExample]) -> Dict[str, int]:
    """Count entity categories in the dataset"""
    result_dict: Dict[str, int] = {}
    for _, annotations in data:
        for annot in annotations['entities']:
            ent_category = annot[2]
            result_dict[ent_category] = result_dict.get(ent_category, 0) + 1
    return result_dict


def create_training_data(
    doc_chunks: Dict[int, str], 
    entity_patterns: List[EntityPattern], 
    verbose: bool = False
) -> List[TrainingExample]:
    """Create training data from document chunks and entity patterns"""
    training_data = []
    
    for chunk_id, chunk_text in doc_chunks.items():
        chunk_entities = []
        
        for pattern in entity_patterns:
            entity_text = pattern["pattern"]
            entity_label = pattern["label"]
            
            # Find all occurrences of the entity in the chunk
            for match in re.finditer(re.escape(entity_text), chunk_text, re.IGNORECASE):
                start, end = match.span()
                chunk_entities.append((start, end, entity_label))
        
        # Only add chunks that contain entities
        if chunk_entities:
            # Sort entities by start position
            chunk_entities.sort(key=lambda x: x[0])
            
            # Add to training data
            training_data.append((chunk_text, {"entities": chunk_entities}))
            
            if verbose and len(training_data) % 100 == 0:
                print(f"Created {len(training_data)} training examples")
    
    return training_data


def process_data(
    raw_text_dir: Union[str, Path], 
    entities_dir: Union[str, Path], 
    train_output: Union[str, Path], 
    test_output: Union[str, Path], 
    num_chunks: int = 6, 
    verbose: bool = False
) -> Tuple[List[TrainingExample], List[TrainingExample]]:
    """Process raw text and entity data to create training and test datasets"""
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
    
    # Create training data from chunks and entity patterns
    train_test_dataset = create_training_data(doc_chunk_dict, ent_patterns_list, verbose)
    
    # If there's no data, return empty lists
    if not train_test_dataset:
        print("Warning: No training data was created.")
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
    Path(train_output).parent.mkdir(parents=True, exist_ok=True)
    Path(test_output).parent.mkdir(parents=True, exist_ok=True)
    
    # Save train and test data to pickle files
    with open(train_output, 'wb') as train_file:
        pickle.dump(train_data, train_file)
    
    with open(test_output, 'wb') as test_file:
        pickle.dump(test_data, test_file)
    
    print(f"Training data saved to {train_output}")
    print(f"Test data saved to {test_output}")
    
    return train_data, test_data


def main() -> None:
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
