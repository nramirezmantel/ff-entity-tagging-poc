#!/usr/bin/env python3
"""
OCR extraction script: Converts PDF, DOCX, XLSX files to TXT using OCR
"""
import argparse
from pathlib import Path
from typing import Callable, Optional, Dict, Any, List, Union

# For OCR processing
try:
    import docx2txt
    import pandas as pd
    from docling.document_converter import DocumentConverter
except ImportError as e:
    print(f"Warning: OCR package not found: {e}")
    print("OCR processing may not work properly.")


def construct_output_filepath(output_folder: Path, filename: str, extension: str) -> Path:
    """Constructs the output file path with the specified extension"""
    return output_folder / f"{Path(filename).stem}{extension}"


def file_already_processed(output_filepath: Path) -> bool:
    """Checks if the output file already exists"""
    if output_filepath.exists():
        print(f"Skipping {output_filepath.name}, because the corresponding file already exists.")
        return True
    return False


def read_and_write_file(
    input_filepath: Path, 
    output_filepath: Path, 
    content_extractor: Callable[[Path], Optional[str]]
) -> None:
    """Reads a file, extracts content, and writes it to an output file"""
    result = content_extractor(input_filepath)
    print(f"Writing {output_filepath.name}")
    
    if not result:
        raise ValueError(f"Empty read from file: {input_filepath.name}")
        
    output_filepath.write_text(result, encoding="utf-8")


def process_pdf(converter: DocumentConverter, input_filepath: Path) -> Optional[str]:
    """Process PDF files using DocumentConverter"""
    print(f"Reading PDF: {input_filepath.name}")
    result = converter.convert(str(input_filepath))
    return result.document.export_to_markdown() if result else None


def process_docx(input_filepath: Path) -> Optional[str]:
    """Process DOCX files using docx2txt"""
    print(f"Reading DOCX: {input_filepath.name}")
    try:
        with open(input_filepath, 'rb') as file:
            result = docx2txt.process(file)
        print("DOCX loaded successfully!")
        return result if result else None
    except Exception as e:
        print(f"Failed to read as DOCX: {e}")
        return None


def process_xlsx(input_filepath: Path) -> Optional[str]:
    """Process XLSX files using pandas"""
    print(f"Reading XLSX: {input_filepath.name}")
    try:
        df = pd.read_excel(input_filepath)
        list_results = df.applymap(str).values.flatten().tolist()
        return " ".join(list_results) if list_results else None
    except Exception as e:
        print(f"Failed to read as XLSX: {e}")
        return None


def process_files_ocr(input_folder: Union[str, Path], output_folder: Union[str, Path]) -> int:
    """Process all files in the input folder and convert them to text using OCR"""
    # Convert to Path objects
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    
    # Create output folder if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    converter = DocumentConverter()
    processed_count = 0
    
    # Define file processors
    processors = {
        '.pdf': lambda filepath: process_pdf(converter, filepath),
        '.docx': process_docx,
        '.xlsx': process_xlsx
    }
    
    for file_path in input_path.iterdir():
        if not file_path.is_file():
            continue
            
        file_suffix = file_path.suffix.lower()
        if file_suffix not in processors:
            print(f"File extension not supported: {file_path.name}")
            continue
            
        output_filepath = construct_output_filepath(output_path, file_path.name, ".txt")
        if file_already_processed(output_filepath):
            continue
            
        try:
            processor = processors[file_suffix]
            read_and_write_file(file_path, output_filepath, processor)
            processed_count += 1
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")
    
    return processed_count


def main() -> None:
    """Main function to run the OCR extraction script"""
    parser = argparse.ArgumentParser(description="OCR extraction: Convert PDF, DOCX, XLSX files to TXT")
    
    # Input directory
    parser.add_argument("--input", required=True, 
                        help="Directory containing raw files (PDF, DOCX, XLSX) to process")
    
    # OCR arguments
    parser.add_argument("--output", default="data/processed/pre_processing/ocr_output",
                        help="Directory to save OCR output files")
    
    args = parser.parse_args()
    
    print(f"Processing files in {args.input} for OCR conversion")
    ocr_count = process_files_ocr(args.input, args.output)
    print(f"Successfully processed {ocr_count} files with OCR")


if __name__ == "__main__":
    main()
