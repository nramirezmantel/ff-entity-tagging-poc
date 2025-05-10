"""
Runs evaluation on a trained model, 
Or a trained model + matcher
"""
import pickle
import spacy
import argparse
import os
import json
from spacy.training.example import Example


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


def create_examples(model, data):
    """
    Create spaCy examples from data
    
    Args:
        model: The spaCy model
        data (list): List of (text, annotations) tuples
        
    Returns:
        list: List of spaCy Example objects
    """
    examples = []
    for text, annots in data:
        doc = model.make_doc(text)
        examples.append(Example.from_dict(doc, annots))
    return examples


def evaluate_model(model_path, train_data_path, test_data_path, output_path=None):
    """
    Evaluate a trained spaCy model on train and test data
    
    Args:
        model_path (str): Path to the trained model
        train_data_path (str): Path to the training data pickle file
        test_data_path (str): Path to the test data pickle file
        output_path (str, optional): Path to save evaluation results
        
    Returns:
        tuple: (train_performance_dict, test_performance_dict)
    """
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
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump({
                'train': train_performance_dict,
                'test': test_performance_dict
            }, f, indent=2)
        print(f"\nEvaluation results saved to {output_path}")
    
    return train_performance_dict, test_performance_dict


def main():
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
