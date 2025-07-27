
from pathlib import Path
from pdf_extractor import PDFExtractor
import json

def main():
    """Main function to process all PDFs in input directory"""
    
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")
    
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    
    if not input_dir.exists():
        print(f"Input directory {input_dir} not found!")
        return
    
    
    extractor = PDFExtractor()
    
    
    pdf_files = list(input_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in input directory")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s) to process")
    
    for pdf_file in pdf_files:
        try:
            print(f"Processing: {pdf_file.name}")
            
            # Extract structure
            result = extractor.extract_structure(pdf_file)
            
            # Generate output filename
            output_file = output_dir / f"{pdf_file.stem}.json"
            
            # Save JSON output
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"Generated: {output_file.name}")
            print(f"  - Title: {result['title']}")
            print(f"  - Headings found: {len(result['outline'])}")
            
        except Exception as e:
            print(f"Error processing {pdf_file.name}: {e}")
            # Create empty output file for failed processing
            output_file = output_dir / f"{pdf_file.stem}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({"title": "", "outline": []}, f, indent=2)
    
    print("Processing complete!")

def test_local():
    """Test function for local development"""
    input_dir = Path("input")
    output_dir = Path("output")
    
    if input_dir.exists():
        
        import sys
        sys.path.insert(0, str(Path.cwd()))
        
        extractor = PDFExtractor()
        
        for pdf_file in input_dir.glob("*.pdf"):
            print(f"Local test: {pdf_file.name}")
            result = extractor.extract_structure(pdf_file)
            
            output_file = output_dir / f"{pdf_file.stem}.json"
            output_dir.mkdir(exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()