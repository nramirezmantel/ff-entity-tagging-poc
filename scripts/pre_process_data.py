"""
Will do both ocr extraction
and LLM entity extraction later
combining scripts inside src/llm 
and src/ocr folders

then cleaning of that eventual output
"""

# clean entity labels
def clean_date_string(date_string):
    # Remove '[' and ']' characters
    cleaned = date_string.strip('[]')
    # Remove any escaped characters (e.g., \n, \t, etc.)
    cleaned = bytes(cleaned, 'utf-8').decode('unicode_escape')
    # Remove single or double quotes inside the string
    cleaned = cleaned.replace("'", "").replace('"', "")
    return cleaned

def clean_json(json_data, keys_to_remove):
    # Remove the specified keys
    for key in keys_to_remove:
        if key in json_data:
            del json_data[key]

    # Clean the values of any lists found in the JSON
    for key, value in json_data.items():
        # Check if the value is a list and contains strings
        if isinstance(value, list):
            json_data[key] = [clean_date_string(v) if isinstance(v, str) else v for v in value]

    return json_data

def process_files_in_directory(directory, keys_to_remove):
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
                new_file_path = os.path.join(directory, new_filename)

                # Write the cleaned data to the new file
                with open(new_file_path, 'w', encoding='utf-8') as f:
                    json.dump(cleaned_data, f, indent=2)
                print(f"Processed and saved cleaned file: {new_filename}")

            except Exception as e:
                print(f"Failed to process {filename}: {e}")
                
keys_to_remove = ['dates', 'included entities']  # List of keys to remove
process_files_in_directory(ENTITIES_DIR, keys_to_remove)
