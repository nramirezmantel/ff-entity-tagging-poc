#!/usr/bin/env python3
"""
LLM tagging script: Processes TXT files with LLM to extract entities and cleans the results
"""
import json
import argparse
import asyncio
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Union

# Add the project root directory to Python path for LLM imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# Import LLM modules
try:
    from src.llm.runners.ee_openai_runner import ee_openai_runner, list_files_in_folder
    from src.llm.prompts.ic_mrc_arc import ic_mrc_arc_prompts
    from src.llm.utils.helpers import clean_json as llm_clean_json
except ImportError as e:
    print(f"Warning: Some LLM modules could not be imported: {e}")
    print("LLM entity extraction may not work properly.")


async def process_files_llm(input_folder: Union[str, Path], output_folder: Union[str, Path]) -> int:
    """Process text files and extract entities using LLM"""
    # Convert to Path objects
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    
    # Create output folder if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    list_files = list_files_in_folder(str(input_path))
    processed_count = 0
    
    for file_path in list_files:
        file_path_obj = Path(file_path)
        if file_path_obj.suffix.lower() != '.txt':
            continue
            
        base_name = file_path_obj.stem
        print(f"Processing document: {file_path}")

        try:
            # Use the ee_openai_runner to extract entities
            responses = await ee_openai_runner(file_path, ic_mrc_arc_prompts)
            
            if not isinstance(responses, dict):
                print("Responses are not an object")
                continue

            # Clean the responses using the LLM clean_json function
            cleaned_responses = llm_clean_json(responses)
            json_responses = json.dumps(cleaned_responses, indent=2)

            timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            output_file = output_path / f"response-{base_name}-{timestamp}.json"
            
            output_file.write_text(json_responses, encoding="utf-8")
            print(f"Output file: {output_file}")
            processed_count += 1
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    return processed_count


def clean_date_string(date_string: str) -> str:
    """Clean a date string by removing brackets, escaped characters, and quotes"""
    # Remove '[' and ']' characters
    cleaned = date_string.strip('[]')
    # Remove any escaped characters (e.g., \n, \t, etc.)
    cleaned = bytes(cleaned, 'utf-8').decode('unicode_escape')
    # Remove single or double quotes inside the string
    cleaned = cleaned.replace("'", "").replace('"', "")
    return cleaned


def clean_json(json_data: Dict[str, Any], keys_to_remove: List[str]) -> Dict[str, Any]:
    """Clean a JSON object by removing specified keys and cleaning string values"""
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


def process_files_in_directory(
    directory: Union[str, Path], 
    keys_to_remove: List[str], 
    output_dir: Optional[Union[str, Path]] = None
) -> int:
    """Process all JSON files in a directory, cleaning them and saving the results"""
    # Convert to Path objects
    dir_path = Path(directory)
    out_path = Path(output_dir) if output_dir else dir_path
    
    if not dir_path.is_dir():
        raise ValueError(f"Directory not found: {directory}")
    
    # Create output directory if it doesn't exist
    if output_dir:
        out_path.mkdir(parents=True, exist_ok=True)
    
    processed_count = 0
    
    # Process each JSON file in the directory
    for file_path in dir_path.glob("*.json"):
        try:
            # Load the JSON data
            data = json.loads(file_path.read_text(encoding="utf-8"))

            # Clean and remove the specified keys
            cleaned_data = clean_json(data, keys_to_remove)

            # Create a new filename with the '_cleaned' postfix
            new_filename = f"{file_path.stem}_cleaned.json"
            new_file_path = out_path / new_filename

            # Write the cleaned data to the new file
            new_file_path.write_text(json.dumps(cleaned_data, indent=2), encoding="utf-8")
            print(f"Processed and saved cleaned file: {new_filename}")
            processed_count += 1

        except Exception as e:
            print(f"Failed to process {file_path.name}: {e}")
    
    return processed_count


async def main_async(args: argparse.Namespace) -> None:
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


def main() -> None:
    """Main function to run the LLM tagging script"""
    parser = argparse.ArgumentParser(description="LLM tagging: Extract entities and clean JSON files")
    
    # Input directory
    parser.add_argument("--input", required=True, 
                        help="Directory containing text files to process")
    
    # LLM arguments
    parser.add_argument("--llm", action="store_true",
                        help="Perform LLM entity extraction")
    parser.add_argument("--llm-output", default="data/processed/pre_processing/llm_entities",
                        help="Directory to save LLM entity extraction output files")
    
    # Clean arguments
    parser.add_argument("--clean", action="store_true",
                        help="Perform JSON cleaning")
    parser.add_argument("--clean-output", default="data/processed/pre_processing/cleaned_llm_entities",
                        help="Directory to save cleaned JSON files")
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
