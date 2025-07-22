#!/usr/bin/env python3

import os
import json
from pathlib import Path
from pdf_extractor import PDFExtractor

def main():
    """Main function to process all PDFs in input directory"""
    
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if input directory exists
    if not input_dir.exists():
        print("Input directory not found. Creating empty input directory.")
        input_dir.mkdir(parents=True, exist_ok=True)
        return
    
    # Initialize PDF extractor
    extractor = PDFExtractor()
    
    # Process all PDF files in input directory
    pdf_files = list(input_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in input directory")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s) to process")
    
    for pdf_file in pdf_files:
        try:
            print(f"Processing: {pdf_file.name}")
            
            # Extract document structure
            result = extractor.extract_structure(pdf_file)
            
            # Create output JSON file
            output_file = output_dir / f"{pdf_file.stem}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"Generated: {output_file.name}")
            print(f"  - Title: {result['title']}")
            print(f"  - Headings found: {len(result['outline'])}")
            
        except Exception as e:
            print(f"Error processing {pdf_file.name}: {e}")
            # Create error output to avoid failing completely
            error_output = {
                "title": "Error Processing Document",
                "outline": []
            }
            output_file = output_dir / f"{pdf_file.stem}.json"
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(error_output, f, indent=2)
                print(f"Generated error output: {output_file.name}")
            except Exception as write_error:
                print(f"Failed to write error output: {write_error}")
    
    print("Processing complete!")

def test_local():
    """Test function for local development"""
    
    # Use local directories for testing
    input_dir = Path("./sample_dataset/pdfs")
    output_dir = Path("./test_output")
    
    output_dir.mkdir(exist_ok=True)
    
    if not input_dir.exists():
        print(f"Test input directory not found: {input_dir}")
        return
    
    extractor = PDFExtractor()
    pdf_files = list(input_dir.glob("*.pdf"))
    
    print(f"Testing with {len(pdf_files)} PDF files")
    
    for pdf_file in pdf_files:
        try:
            print(f"Testing: {pdf_file.name}")
            result = extractor.extract_structure(pdf_file)
            
            output_file = output_dir / f"{pdf_file.stem}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"  - Title: {result['title']}")
            print(f"  - Headings: {len(result['outline'])}")
            
        except Exception as e:
            print(f"Error testing {pdf_file.name}: {e}")

if __name__ == "__main__":
    # Check if we're in a container or local development
    if Path("/app/input").exists():
        # Running in container
        main()
    else:
        # Local development - run tests
        print("Running in local test mode...")
        test_local()
