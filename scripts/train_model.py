"""
Actually trains the spaCy model
"""
import pickle
import spacy
import argparse
import os
import subprocess
from spacy.tokens import DocBin


def load_data(file_path):
    """
    Load data from a pickle file
    
    Args:
        file_path (str): Path to the pickle file
        
    Returns:
        list: The loaded data
    """
    with open(file_path, "rb") as f:
        return pickle.load(f)


def convert_to_spacy_format(data, output_path, model_name="en_core_web_sm", verbose=False):
    """
    Convert data to spaCy binary format
    
    Args:
        data (list): List of (text, annotations) tuples
        output_path (str): Path to save the spaCy binary file
        model_name (str): Name of the spaCy model to use
        verbose (bool): Whether to print verbose output
        
    Returns:
        None
    """
    db = DocBin()
    nlp = spacy.load(model_name)
    
    for text, annotations in data:
        entity_annotations = annotations['entities']
        doc = nlp(text)
        ents = []
        
        for annotation in entity_annotations:
            start, end, label = annotation
            span = doc.char_span(start, end, label=label)
            if span is not None:  # Check if span is valid
                ents.append(span)
        
        if ents:  # Only add if there are valid entities
            doc.ents = ents
            if verbose:
                print(f"text: {text}, ents: {ents}")
            db.add(doc)
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    db.to_disk(output_path)
    print(f"Saved spaCy binary file to {output_path}")


def train_model(config_path, train_path, valid_path, output_dir):
    """
    Train a spaCy model using the provided config and data
    
    Args:
        config_path (str): Path to the spaCy config file
        train_path (str): Path to the training data in spaCy binary format
        valid_path (str): Path to the validation data in spaCy binary format
        output_dir (str): Directory to save the trained model
        
    Returns:
        int: Return code from the training process
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Build the command
    cmd = [
        "python", "-m", "spacy", "train", 
        config_path,
        "--output", output_dir,
        "--paths.train", train_path,
        "--paths.dev", valid_path
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    
    # Run the command
    process = subprocess.run(cmd)
    
    return process.returncode


def main():
    """Main function to run the script"""
    parser = argparse.ArgumentParser(description="Train a spaCy NER model")
    parser.add_argument("--train", default="TRAIN-ic-mrc-arc-large-batch.pkl", 
                        help="Path to the training data pickle file")
    parser.add_argument("--test", default="TEST-ic-mrc-arc-large-batch.pkl", 
                        help="Path to the test data pickle file")
    parser.add_argument("--config", default="config.cfg", 
                        help="Path to the spaCy config file")
    parser.add_argument("--output", default="./output", 
                        help="Directory to save the trained model")
    parser.add_argument("--model", default="en_core_web_sm", 
                        help="spaCy model to use for preprocessing")
    parser.add_argument("--verbose", action="store_true", 
                        help="Print verbose output")
    
    args = parser.parse_args()
    
    # Load data
    train_data = load_data(args.train)
    test_data = load_data(args.test)
    
    # Convert to spaCy format
    train_spacy_path = "./train.spacy"
    valid_spacy_path = "./valid.spacy"
    
    print("Converting training data to spaCy format...")
    convert_to_spacy_format(train_data, train_spacy_path, args.model, args.verbose)
    
    print("Converting test data to spaCy format...")
    convert_to_spacy_format(test_data, valid_spacy_path, args.model, args.verbose)
    
    # Train the model
    print("\nTraining the model...")
    return_code = train_model(args.config, train_spacy_path, valid_spacy_path, args.output)
    
    if return_code == 0:
        print(f"\nTraining completed successfully. Model saved to {args.output}")
    else:
        print(f"\nTraining failed with return code {return_code}")


if __name__ == "__main__":
    main()
