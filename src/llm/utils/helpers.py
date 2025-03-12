import os
from openai import AzureOpenAI
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

def get_azure_openai_client():
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_GPT_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_GPT_MODEL"),
        api_version=os.getenv("AZURE_GPT_API_VERSION"),
        api_key=os.getenv("AZURE_GPT_API_KEY")
    )
    return {"client": client}

def clean_text(text: str) -> str:
    return (
        text.replace("\r\n", ' ')  # Replace Windows-style line endings with a space
            .replace("\n", ' ')      # Replace Unix-style line endings with a space
            .replace("\r", ' ')      # Replace Mac-style carriage returns with a space
            .replace("\\s+", ' ')     # Replace multiple spaces (or whitespace) with a single space
            .strip()                 # Remove leading and trailing spaces
    )

def chunk_text(text: str, encoding, max_tokens_per_chunk: int) -> list:
    tokens = encoding.encode(text)
    chunks = []
    decoder = encoding.decode

    # Split tokens into chunks
    for i in range(0, len(tokens), max_tokens_per_chunk):
        token_chunk = tokens[i:i + max_tokens_per_chunk]
        chunk_text = decoder(token_chunk)
        chunks.append(chunk_text)

    return chunks

def clean_string(input: str) -> str:
    # Split into array and remove quotes
    items = [item.replace('"', '') for item in input.split(',')]
    
    # Filter out null entries
    filtered_items = [item for item in items if item != 'null']
    
    # Join back into string
    return ','.join(filtered_items)

def clean_json(input: dict) -> dict:
    cleaned_object = {}

    for key, value in input.items():
        cleaned_value = []
        cleaned_string = value.strip().replace('"', "")
        
        if key != "registered_addresses":
            # Replace `","` with `,` and trim spaces in lists
            cleaned_value = cleaned_string.replace('","', ', ').replace(r'\s*,\s*', ', ').split(", ")

        # Handle cases where `|` is used as a separator (e.g., addresses)
        if key == "registered_addresses":
            cleaned_value = cleaned_string.replace('|', ' | ').split(' | ')

        # Store cleaned value
        cleaned_object[key] = cleaned_value

    return cleaned_object

