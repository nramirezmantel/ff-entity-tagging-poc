"""
Script for running inference with a trained spaCy model
"""
import spacy
import argparse
import json
import os


def load_model(model_path):
    """
    Load a trained spaCy model
    
    Args:
        model_path (str): Path to the trained model
        
    Returns:
        spacy.language.Language: The loaded spaCy model
    """
    try:
        nlp = spacy.load(model_path)
        print(f"Model loaded from {model_path}")
        return nlp
    except Exception as e:
        print(f"Error loading model: {e}")
        raise


def process_text(nlp, text):
    """
    Process text with a spaCy model
    
    Args:
        nlp (spacy.language.Language): The spaCy model
        text (str): The text to process
        
    Returns:
        dict: Dictionary containing the processed results
    """
    doc = nlp(text)
    
    # Extract entities
    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "start": ent.start_char,
            "end": ent.end_char,
            "label": ent.label_
        })
    
    return {
        "text": text,
        "entities": entities
    }


def process_file(nlp, input_path, output_path=None):
    """
    Process a text file with a spaCy model
    
    Args:
        nlp (spacy.language.Language): The spaCy model
        input_path (str): Path to the input text file
        output_path (str, optional): Path to save the results
        
    Returns:
        dict: Dictionary containing the processed results
    """
    # Read the input file
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Process the text
    results = process_text(nlp, text)
    
    # Save the results if output path is provided
    if output_path:
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {output_path}")
    
    return results


def main():
    """Main function to run the script"""
    parser = argparse.ArgumentParser(description="Run inference with a trained spaCy model")
    parser.add_argument("--model", default="output/model-best", 
                        help="Path to the trained model (default: output/model-best)")
    parser.add_argument("--input", required=True, 
                        help="Path to the input text file or text to process")
    parser.add_argument("--output", 
                        help="Path to save the results (optional)")
    parser.add_argument("--is-file", action="store_true", 
                        help="Treat input as a file path (default: False)")
    
    args = parser.parse_args()
    
    # Load the model
    nlp = load_model(args.model)
    
    # Process the input
    if args.is_file:
        results = process_file(nlp, args.input, args.output)
    else:
        results = process_text(nlp, args.input)
        
        # Save the results if output path is provided
        if args.output:
            os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)
            print(f"Results saved to {args.output}")
    
    # Print the results
    if not args.output:
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
