#!/usr/bin/env python3
"""
LLM tagging script that:
1. Processes TXT files with LLM to extract entities
2. Cleans the extracted entity JSON files
"""
import os
import sys
import json
import argparse
import asyncio
from pathlib import Path
from datetime import datetime

# Add the project root directory to Python path for LLM imports
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

# Import LLM modules
try:
    # Import the ee_openai_runner as the entry point for LLM extraction
    from src.llm.runners.ee_openai_runner import ee_openai_runner, list_files_in_folder
    from src.llm.prompts.ic_mrc_arc import ic_mrc_arc_prompts
    from src.llm.utils.helpers import clean_json as llm_clean_json
except ImportError as e:
    print(f"Warning: Some LLM modules could not be imported: {e}")
    print("LLM entity extraction may not work properly.")


async def process_files_llm(input_folder, output_folder):
    """
    Process all text files in the input folder and extract entities using LLM.
    
    Args:
        input_folder (str): Path to the folder containing text files
        output_folder (str): Path to the folder where output JSON files will be saved
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    list_files = list_files_in_folder(input_folder)
    processed_count = 0
    
    for file_path in list_files:
        if not file_path.endswith('.txt'):
            continue
            
        base_name = Path(file_path).stem
        print(f"Processing document: {file_path}")

        try:
            # Use the ee_openai_runner to extract entities
            responses = await ee_openai_runner(file_path, ic_mrc_arc_prompts)
            print(responses)

            if not isinstance(responses, dict):
                print("Responses are not an object")
                continue

            # Clean the responses using the LLM clean_json function
            cleaned_responses = llm_clean_json(responses)
            json_responses = json.dumps(cleaned_responses, indent=2)

            timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            output_file = Path(output_folder) / f"response-{base_name}-{timestamp}.json"
            
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(json_responses)

            print(f"Output file: {output_file}")
            processed_count += 1
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    return processed_count


def clean_date_string(date_string):
    """
    Clean a date string by removing brackets, escaped characters, and quotes
    
    Args:
        date_string (str): The date string to clean
        
    Returns:
        str: The cleaned date string
    """
    # Remove '[' and ']' characters
    cleaned = date_string.strip('[]')
    # Remove any escaped characters (e.g., \n, \t, etc.)
    cleaned = bytes(cleaned, 'utf-8').decode('unicode_escape')
    # Remove single or double quotes inside the string
    cleaned = cleaned.replace("'", "").replace('"', "")
    return cleaned


def clean_json(json_data, keys_to_remove):
    """
    Clean a JSON object by removing specified keys and cleaning string values
    
    Args:
        json_data (dict): The JSON data to clean
        keys_to_remove (list): List of keys to remove from the JSON
        
    Returns:
        dict: The cleaned JSON data
    """
    # Create a copy to avoid modifying the original
    cleaned_data = json_data.copy()
    
    # Remove the specified keys
    for key in keys_to_remove:
        if key in cleaned_data:
            del cleaned_data[key]

    # Clean the values of any lists found in the JSON
    for key, value in cleaned_data.items():
        # Check if the value is a list and contains strings
        if isinstance(value, list):
            cleaned_data[key] = [clean_date_string(v) if isinstance(v, str) else v for v in value]

    return cleaned_data


def process_files_in_directory(directory, keys_to_remove, output_dir=None):
    """
    Process all JSON files in a directory, cleaning them and saving the results
    
    Args:
        directory (str): The directory containing JSON files to process
        keys_to_remove (list): List of keys to remove from each JSON file
        output_dir (str, optional): Directory to save cleaned files. If None, saves in the same directory.
        
    Returns:
        int: Number of files processed successfully
    """
    if not os.path.isdir(directory):
        raise ValueError(f"Directory not found: {directory}")
    
    # If output_dir is specified, create it if it doesn't exist
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    processed_count = 0
    
    # Loop through each file in the specified directory
    for filename in os.listdir(directory):
        # Check if the file is a JSON file
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # Clean and remove the specified keys
                cleaned_data = clean_json(data, keys_to_remove)

                # Create a new filename with the '_cleaned' postfix
                new_filename = os.path.splitext(filename)[0] + '_cleaned.json'
                new_file_path = os.path.join(output_dir or directory, new_filename)

                # Write the cleaned data to the new file
                with open(new_file_path, 'w', encoding='utf-8') as f:
                    json.dump(cleaned_data, f, indent=2)
                print(f"Processed and saved cleaned file: {new_filename}")
                processed_count += 1

            except Exception as e:
                print(f"Failed to process {filename}: {e}")
    
    return processed_count


async def main_async(args):
    """Async main function to run the script"""
    # Step 1: LLM entity extraction
    if args.llm:
        print(f"Processing files in {args.input} for LLM entity extraction")
        llm_count = await process_files_llm(args.input, args.llm_output)
        print(f"Successfully processed {llm_count} files with LLM")
    
    # Step 2: Clean JSON files
    if args.clean:
        print(f"Processing files in {args.llm_output} for JSON cleaning")
        print(f"Removing keys: {args.remove}")
        clean_count = process_files_in_directory(args.llm_output, args.remove, args.clean_output)
        print(f"Successfully processed {clean_count} files for cleaning")


def main():
    """Main function to run the LLM tagging script"""
    parser = argparse.ArgumentParser(description="LLM tagging: Extract entities and clean JSON files")
    
    # Input directory
    parser.add_argument("--input", required=True, 
                        help="Directory containing text files to process")
    
    # LLM arguments
    parser.add_argument("--llm", action="store_true",
                        help="Perform LLM entity extraction")
    parser.add_argument("--llm-output", default="data/processed/pre_processing/llm_entities",
                        help="Directory to save LLM entity extraction output files (default: data/processed/pre_processing/llm_entities)")
    
    # Clean arguments
    parser.add_argument("--clean", action="store_true",
                        help="Perform JSON cleaning")
    parser.add_argument("--clean-output", default="data/processed/pre_processing/cleaned_llm_entities",
                        help="Directory to save cleaned JSON files (default: data/processed/pre_processing/cleaned_entities)")
    # below might not be needed
    parser.add_argument("--remove", nargs='+', default=['dates', 'included entities'],
                        help="Keys to remove from JSON files (default: 'dates' 'included entities')")
    
    # All steps
    parser.add_argument("--all", action="store_true",
                        help="Perform all processing steps: LLM and cleaning")
    
    args = parser.parse_args()
    
    # If --all is specified, enable all processing steps
    if args.all:
        args.llm = True
        args.clean = True
    
    # Run the async main function
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
