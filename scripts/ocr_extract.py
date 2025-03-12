#!/usr/bin/env python3
"""
OCR extraction script that:
1. Takes raw files (PDF, DOCX, XLSX) and converts them to TXT using OCR
"""
import os
import argparse
from pathlib import Path

# For OCR processing
try:
    import docx2txt
    import pandas as pd
    from docling.document_converter import DocumentConverter
except ImportError as e:
    print(f"Warning: OCR package not found: {e}")
    print("OCR processing may not work properly.")


def construct_output_filepath(input_folder, output_folder, filename, extension):
    """Constructs the output file path with the specified extension."""
    return os.path.join(output_folder, filename.rsplit('.', 1)[0] + extension)


def file_already_processed(output_filepath):
    """Checks if the output file already exists."""
    if os.path.exists(output_filepath):
        print(f"Skipping {os.path.basename(output_filepath)}, because the corresponding file already exists.")
        return True
    return False


def read_and_write_file(input_filepath, output_filepath, content_extractor):
    """Reads a file, extracts content, and writes it to an output file."""
    result = content_extractor(input_filepath)
    print(f"Writing {os.path.basename(output_filepath)}")
    with open(output_filepath, "w", encoding="utf-8") as f_write:
        if result:
            f_write.write(result)
        else:
            raise ValueError(f"Empty read from file: {os.path.basename(input_filepath)}")


def process_pdf(converter, input_filepath, output_filepath):
    """Process PDF files using DocumentConverter."""
    print(f"Reading PDF: {os.path.basename(input_filepath)}")
    result = converter.convert(input_filepath)
    return result.document.export_to_markdown() if result else None


def process_docx(input_filepath, output_filepath):
    """Process DOCX files using docx2txt."""
    print(f"Reading DOCX: {os.path.basename(input_filepath)}")
    try:
        result = None
        with open(input_filepath, 'rb') as file:
            result = docx2txt.process(file)
        print("DOCX loaded successfully!")
        return result if result else None
    except Exception as e:
        print(f"Failed to read as DOCX: {e}")
        return None


def process_xlsx(input_filepath, output_filepath):
    """Process XLSX files using pandas."""
    print(f"Reading XLSX: {os.path.basename(input_filepath)}")
    df = pd.read_excel(input_filepath)
    list_results = df.applymap(str).values.flatten().tolist()
    return " ".join(list_results) if list_results else None


def process_files_ocr(input_folder, output_folder):
    """
    Process all files in the input folder and convert them to text using OCR.
    
    Args:
        input_folder (str): Path to the folder containing input files
        output_folder (str): Path to the folder where output files will be saved
    """
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    converter = DocumentConverter()
    processed_count = 0
    
    for filename in os.listdir(input_folder):
        input_filepath = os.path.join(input_folder, filename)
        
        if filename.endswith('.pdf'):
            output_filepath = construct_output_filepath(input_folder, output_folder, filename, ".txt")
            if file_already_processed(output_filepath):
                continue
            try:
                read_and_write_file(input_filepath, output_filepath, lambda f: process_pdf(converter, f, output_filepath))
                processed_count += 1
            except Exception as e:
                print(f"Error processing PDF {filename}: {e}")

        elif filename.endswith('.docx'):
            output_filepath = construct_output_filepath(input_folder, output_folder, filename, ".txt")
            if file_already_processed(output_filepath):
                continue
            try:
                read_and_write_file(input_filepath, output_filepath, lambda f: process_docx(f, output_filepath))
                processed_count += 1
            except Exception as e:
                print(f"Error processing DOCX {filename}: {e}")

        elif filename.endswith('.xlsx'):
            output_filepath = construct_output_filepath(input_folder, output_folder, filename, ".txt")
            if file_already_processed(output_filepath):
                continue
            try:
                read_and_write_file(input_filepath, output_filepath, lambda f: process_xlsx(f, output_filepath))
                processed_count += 1
            except Exception as e:
                print(f"Error processing XLSX {filename}: {e}")
        
        else:
            print(f"File extension not supported: {filename}")
    
    return processed_count


def main():
    """Main function to run the OCR extraction script"""
    parser = argparse.ArgumentParser(description="OCR extraction: Convert PDF, DOCX, XLSX files to TXT")
    
    # Input directory
    parser.add_argument("--input", required=True, 
                        help="Directory containing raw files (PDF, DOCX, XLSX) to process")
    
    # OCR arguments
    parser.add_argument("--output", default="data/processed/pre_processing/ocr_output",
                        help="Directory to save OCR output files (default: data/processed/pre_processing/ocr_output)")
    
    args = parser.parse_args()
    
    print(f"Processing files in {args.input} for OCR conversion")
    ocr_count = process_files_ocr(args.input, args.output)
    print(f"Successfully processed {ocr_count} files with OCR")


if __name__ == "__main__":
    main()
