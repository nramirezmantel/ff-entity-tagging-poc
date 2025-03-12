import asyncio
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

import aiofiles
import glob
import os
import json
import tiktoken
from datetime import datetime
from pathlib import Path
from llm.utils.helpers import chunk_text, clean_json, clean_string
from llm.completions.openai import openai_completion
from llm.prompts.foundational import foundational_prompts
from llm.prompts.ic_mrc_arc import ic_mrc_arc_prompts
from llm.config import EXPLORATORY_MODEL, STATIC_MODEL, LIMITS

async def read_txt_file(file_path: str) -> str:
    try:
        async with aiofiles.open(file_path, mode="r", encoding="utf-8") as file:
            content = await file.read()
        return content
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""

def list_files_in_folder(root_folder: str):
    file_list = glob.glob(os.path.join(root_folder, "**", "*"), recursive=True)
    return [f for f in file_list if os.path.isfile(f)]  # Filter out directories

async def ee_openai_runner(file_path: str, prompts: dict) -> dict:


    #prebuiltLayoutRunner removed for now, reading text files instead
    context = await read_txt_file(file_path)
    responses = {}

    model = STATIC_MODEL
    if len(context) > LIMITS[STATIC_MODEL]["max_tokens_no_chunk"]:
        model = EXPLORATORY_MODEL
        if len(context) > LIMITS[model]["max_tokens_no_chunk"]:
            chunks = chunk_text(context, tiktoken.encoding_for_model(model), LIMITS[model]["max_tokens_per_chunk"])
            for prompt_name, prompt in prompts.items():
                response = openai_completion(prompt, model, chunks=chunks)
                responses[prompt_name] = response
            return responses

    for prompt_name, prompt in prompts.items():
        response = openai_completion(prompt, model, context=context)
        responses[prompt_name] = response

    return responses

def main():

    list_files = list_files_in_folder("data/processed/pre_processing/ocr_output")

    for file_path in list_files:
        base_name = Path(file_path).stem
        print(f"processing document: {file_path}")

        responses = asyncio.run(ee_openai_runner(file_path, ic_mrc_arc_prompts))
        print(responses)

        if not isinstance(responses, dict):
            print("Responses are not an object")
            return

        cleaned_responses = clean_json(responses)
        json_responses = json.dumps(cleaned_responses, indent=2)

        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        output_dir = Path("data/processed/pre_processing/llm_entities/")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"response-{base_name}-{timestamp}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(json_responses)

        print(f"Output file: {output_file}")

if __name__ == "__main__":
    main()
