# Entity Tagging Scripts

This directory contains scripts for training, evaluating, and running inference with spaCy NER models.

## Overview

These scripts orchestrate end-to-end processes for entity tagging, sourcing from scripts inside `src/` and data inside `data/`. Each script is designed to be run independently and includes command-line arguments for flexibility.

## Scripts

### Data Preparation

- **pre_process_data.py**: Processes and cleans JSON files containing entity data.
  ```
  python scripts/pre_process_data.py --input <input_dir> --output <output_dir> --remove <keys_to_remove>
  ```

- **feature_engineer_train.py**: Processes raw text and entity data to create training and test datasets.
  ```
  python scripts/feature_engineer_train.py --raw-text <raw_text_dir> --entities <entities_dir> --train-output <train_output> --test-output <test_output>
  ```

- **feature_engineer_test.py**: Processes test data for spaCy inference.
  ```
  python scripts/feature_engineer_test.py --input <input_path> --output <output_path> --model <model_path>
  ```

### Model Training and Evaluation

- **train_model.py**: Trains a spaCy NER model using the provided data.
  ```
  python scripts/train_model.py --train <train_data> --test <test_data> --config <config_path> --output <output_dir>
  ```

- **evaluate_model.py**: Evaluates a trained spaCy model on train and test data.
  ```
  python scripts/evaluate_model.py --model <model_path> --train <train_data> --test <test_data> --output <output_path>
  ```

- **add_matcher_to_model.py**: Adds a rule-based entity matcher to a trained spaCy model.
  ```
  python scripts/add_matcher_to_model.py --model <model_path> --patterns <patterns_file> --output <output_path>
  ```

### Inference

- **inference_model.py**: Runs inference with a trained spaCy model.
  ```
  python scripts/inference_model.py --model <model_path> --input <input_text> --output <output_path>
  ```

### Utilities

- **utils.py**: Contains utility functions for visualizing model evaluation metrics.
  ```
  python scripts/utils.py --input <metrics_file> --output <plot_path>
  ```

## Example Workflow

1. Process raw data:
   ```
   python scripts/pre_process_data.py --input data/raw/entities --output data/processed/entities
   ```

2. Create training and test datasets:
   ```
   python scripts/feature_engineer_train.py --raw-text data/raw/text --entities data/processed/entities --train-output data/processed/train.pkl --test-output data/processed/test.pkl
   ```

3. Train the model:
   ```
   python scripts/train_model.py --train data/processed/train.pkl --test data/processed/test.pkl --config config.cfg --output models/ner
   ```

4. Evaluate the model:
   ```
   python scripts/evaluate_model.py --model models/ner/model-best --train data/processed/train.pkl --test data/processed/test.pkl --output models/ner/evaluation.json
   ```

5. Visualize the evaluation metrics:
   ```
   python scripts/utils.py --input models/ner/evaluation.json --output models/ner/evaluation.png
   ```

6. Run inference:
   ```
   python scripts/inference_model.py --model models/ner/model-best --input "Sample text to analyze" --output results.json
   ```
