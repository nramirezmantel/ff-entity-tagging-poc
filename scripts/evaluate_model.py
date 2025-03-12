"""
Evaluates a trained spaCy model on training and test data
"""
import pickle
import spacy
import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple, Optional
from spacy.training.example import Example
from spacy.language import Language


def load_data(file_path: str) -> List[Tuple[str, Dict[str, Any]]]:
    """Load data from a pickle file"""
    with open(file_path, "rb") as f:
        return pickle.load(f)


def create_examples(model: Language, data: List[Tuple[str, Dict[str, Any]]]) -> List[Example]:
    """Create spaCy examples from data"""
    return [Example.from_dict(model.make_doc(text), annots) for text, annots in data]


def evaluate_model(
    model_path: str, 
    train_data_path: str, 
    test_data_path: str, 
    output_path: Optional[str] = None
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Evaluate a trained spaCy model on train and test data"""
    # Load the model
    trained_model = spacy.load(model_path)
    
    # Load data
    train_data = load_data(train_data_path)
    test_data = load_data(test_data_path)
    
    # Create examples
    train_examples = create_examples(trained_model, train_data)
    test_examples = create_examples(trained_model, test_data)
    
    # Evaluate
    train_performance_dict = trained_model.evaluate(train_examples)
    test_performance_dict = trained_model.evaluate(test_examples)
    
    # Print results
    print("\nTraining data evaluation:")
    print(f"Precision: {train_performance_dict['ents_p']:.4f}")
    print(f"Recall: {train_performance_dict['ents_r']:.4f}")
    print(f"F-score: {train_performance_dict['ents_f']:.4f}")
    
    print("\nTest data evaluation:")
    print(f"Precision: {test_performance_dict['ents_p']:.4f}")
    print(f"Recall: {test_performance_dict['ents_r']:.4f}")
    print(f"F-score: {test_performance_dict['ents_f']:.4f}")
    
    # Save results if output path is provided
    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump({
                'train': train_performance_dict,
                'test': test_performance_dict
            }, f, indent=2)
        print(f"\nEvaluation results saved to {output_path}")
    
    return train_performance_dict, test_performance_dict


def main() -> None:
    """Main function to run the script"""
    parser = argparse.ArgumentParser(description="Evaluate a trained spaCy model")
    parser.add_argument("--model", default="output/model-best", 
                        help="Path to the trained model (default: output/model-best)")
    parser.add_argument("--train", default="TRAIN-ic-mrc-arc-large-batch.pkl", 
                        help="Path to the training data pickle file")
    parser.add_argument("--test", default="TEST-ic-mrc-arc-large-batch.pkl", 
                        help="Path to the test data pickle file")
    parser.add_argument("--output", help="Path to save evaluation results (optional)")
    
    args = parser.parse_args()
    evaluate_model(args.model, args.train, args.test, args.output)


if __name__ == "__main__":
    main()
