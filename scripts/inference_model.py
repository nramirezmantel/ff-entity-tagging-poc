"""
Runs inference with a trained spaCy model on text or files
"""
import spacy
import argparse
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from spacy.language import Language


def load_model(model_path: str) -> Language:
    """Load a trained spaCy model"""
    try:
        nlp = spacy.load(model_path)
        print(f"Model loaded from {model_path}")
        return nlp
    except Exception as e:
        print(f"Error loading model: {e}")
        raise


def process_text(nlp: Language, text: str) -> Dict[str, Any]:
    """Process text with a spaCy model"""
    doc = nlp(text)
    
    # Extract entities
    entities = [
        {
            "text": ent.text,
            "start": ent.start_char,
            "end": ent.end_char,
            "label": ent.label_
        }
        for ent in doc.ents
    ]
    
    return {
        "text": text,
        "entities": entities
    }


def process_file(
    nlp: Language, 
    input_path: str, 
    output_path: Optional[str] = None
) -> Dict[str, Any]:
    """Process a text file with a spaCy model"""
    # Read the input file
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Process the text
    results = process_text(nlp, text)
    
    # Save the results if output path is provided
    if output_path:
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {output_path}")
    
    return results


def main() -> None:
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
            output_file = Path(args.output)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2)
            print(f"Results saved to {args.output}")
    
    # Print the results
    if not args.output:
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
