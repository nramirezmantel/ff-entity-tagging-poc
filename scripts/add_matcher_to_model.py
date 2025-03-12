"""
Adds a rule-based entity matcher to a trained spaCy model
"""
import spacy
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any
from spacy.language import Language


def load_patterns(patterns_file: str) -> List[Dict[str, str]]:
    """Load entity patterns from a JSON file"""
    with open(patterns_file, 'r', encoding='utf-8') as f:
        patterns = json.load(f)
    
    print(f"Loaded {len(patterns)} patterns from {patterns_file}")
    return patterns


def add_entity_ruler(nlp: Language, patterns: List[Dict[str, str]]) -> Language:
    """Add an entity ruler to a spaCy model"""
    # Check if the entity ruler already exists
    if "entity_ruler" in nlp.pipe_names:
        nlp.remove_pipe("entity_ruler")
    
    # Create and add the entity ruler
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    ruler.add_patterns(patterns)
    
    print(f"Added entity ruler with {len(patterns)} patterns")
    return nlp


def save_model(nlp: Language, output_path: str) -> None:
    """Save a spaCy model to disk"""
    Path(output_path).mkdir(parents=True, exist_ok=True)
    nlp.to_disk(output_path)
    print(f"Model saved to {output_path}")


def main() -> None:
    """Main function to run the script"""
    parser = argparse.ArgumentParser(description="Add an entity ruler to a trained spaCy model")
    parser.add_argument("--model", default="output/model-best", 
                        help="Path to the trained model (default: output/model-best)")
    parser.add_argument("--patterns", required=True, 
                        help="Path to the patterns JSON file")
    parser.add_argument("--output", required=True, 
                        help="Path to save the updated model")
    
    args = parser.parse_args()
    
    # Load the model
    print(f"Loading model from {args.model}")
    nlp = spacy.load(args.model)
    
    # Load the patterns
    patterns = load_patterns(args.patterns)
    
    # Add the entity ruler
    nlp = add_entity_ruler(nlp, patterns)
    
    # Save the updated model
    save_model(nlp, args.output)


if __name__ == "__main__":
    main()
