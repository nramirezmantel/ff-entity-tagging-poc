# Entity Tagging Scripts

This directory contains scripts for training, evaluating, and running inference with spaCy NER models.

## Overview

These scripts orchestrate end-to-end processes for entity tagging, sourcing from scripts inside `src/` at times and data inside `data/`. Each script is designed to be run independently and includes command-line arguments for flexibility.

## Scripts

### Data Preparation

- **ocr_extract.py**: Converts PDF, DOCX, and XLSX files to TXT using OCR.
  ```
  python scripts/ocr_extract.py --input <input_dir> --output <output_dir>
  ```

- **llm_tag.py**: Processes TXT files with LLM to extract entities and cleans the extracted entity JSON files.
  ```
  python scripts/llm_tag.py --input <input_dir> --all
  ```
  or for more control:
  ```
  python scripts/llm_tag.py --input <input_dir> --llm --llm-output <llm_output_dir> --clean --clean-output <clean_output_dir> --remove <keys_to_remove>
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
   # Step 1: OCR extraction
   python scripts/ocr_extract.py --input data/raw/files --output data/processed/ocr_output
   
   # Step 2: LLM entity extraction and cleaning
   python scripts/llm_tag.py --input data/processed/ocr_output --all
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
