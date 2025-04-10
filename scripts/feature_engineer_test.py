"""
Script for spaCy inference - processes test data for model inference
"""
import os
import pickle
from pathlib import Path
from typing import Any, List, Optional
import argparse
import spacy


def load_data(file_path: str) -> Any:
    """Load data from a pickle file"""
    with open(file_path, "rb") as f:
        return pickle.load(f)


def save_data(data: Any, file_path: str) -> None:
    """Save data to a pickle file"""
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)
    print(f"Data saved to {file_path}")


def process_test_data(input_path: str, output_path: str, model_path: Optional[str] = None) -> Any:
    """
    Process test data using a spaCy model
    
    Args:
        input_path: Path to the input pickle file
        output_path: Path to save the processed data
        model_path: Path to the spaCy model (optional)
        
    Returns:
        The processed data
    """
    # Load the test data
    test_data = load_data(input_path)
    print(f"Loaded test data from {input_path}")
    
    # If a model path is provided, load the model and process the data
    if model_path:
        nlp = spacy.load(model_path)
        print(f"Loaded model from {model_path}")
        
        # Process the data (this is a placeholder - implement your processing logic here)
        processed_data = test_data  # Replace with actual processing
        
        # Save the processed data
        save_data(processed_data, output_path)
        return processed_data
    
    # If no model is provided, just save the data as is
    save_data(test_data, output_path)
    return test_data


def main() -> None:
    """Main function to run the script"""
    parser = argparse.ArgumentParser(description="Process test data for spaCy inference")
    parser.add_argument("--input", required=True, 
                        help="Path to the input pickle file")
    parser.add_argument("--output", required=True, 
                        help="Path to save the processed data")
    parser.add_argument("--model", 
                        help="Path to the spaCy model (optional)")
    
    args = parser.parse_args()
    process_test_data(args.input, args.output, args.model)


if __name__ == "__main__":
    main()
