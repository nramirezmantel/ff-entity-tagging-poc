"""
Will do both ocr extraction
and LLM entity extraction later
combining scripts inside src/llm 
and src/ocr folders

then cleaning of that eventual output
"""
import os
import json
import argparse


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


def main():
    """Main function to run the script"""
    parser = argparse.ArgumentParser(description="Process and clean JSON files")
    parser.add_argument("--input", required=True, 
                        help="Directory containing JSON files to process")
    parser.add_argument("--output", 
                        help="Directory to save cleaned files (default: same as input)")
    parser.add_argument("--remove", nargs='+', default=['dates', 'included entities'],
                        help="Keys to remove from JSON files (default: 'dates' 'included entities')")
    
    args = parser.parse_args()
    
    print(f"Processing files in {args.input}")
    print(f"Removing keys: {args.remove}")
    
    count = process_files_in_directory(args.input, args.remove, args.output)
    
    print(f"Successfully processed {count} files")


if __name__ == "__main__":
    main()
