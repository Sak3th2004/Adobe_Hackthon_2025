# Challenge 1A: PDF Document Structure Extractor

## Overview
This solution extracts structured information (title and headings H1, H2, H3) from PDF documents and outputs them in the specified JSON format for Challenge 1A.

## Approach
- **Multi-Strategy Title Detection**: Uses PDF metadata, font analysis, and position-based detection
- **Comprehensive Heading Detection**: Combines font size analysis, text patterns, and positional heuristics
- **Robust Validation**: Filters false positives like page numbers and figure captions
- **Hierarchical Classification**: Automatically determines H1, H2, H3 levels based on multiple criteria

## Libraries Used
- **PyPDF2** (3.0.1): PDF metadata extraction (~2MB)
- **pdfplumber** (0.10.3): Text extraction and character-level analysis (~3MB)
- **regex** (2023.12.25): Enhanced pattern matching (~1MB)
- **Total size**: <10MB (well within 200MB constraint)

## Architecture
├── process_pdfs.py # Main entry point
├── pdf_extractor.py # Core PDF processing logic
└── utils/
├── heading_detector.py # Heading detection algorithms
└── text_processor.py # Text processing utilities



## Building and Running

### Build Docker Image
docker build --platform linux/amd64 -t challenge1a:latest .

text

### Run Solution (Official Format)
docker run --rm
-v $(pwd)/input:/app/input
-v $(pwd)/output:/app/output
--network none
challenge1a:latest

text

## Features
- ✅ **AMD64 Compatible**: Optimized for linux/amd64 architecture
- ✅ **High Performance**: Processes 50-page PDFs in <10 seconds
- ✅ **Offline Operation**: No internet access required
- ✅ **Memory Efficient**: Works within 16GB RAM constraint
- ✅ **Multilingual Support**: Handles Japanese text patterns (bonus feature)
- ✅ **Exact Format Compliance**: Outputs JSON exactly as specified

## Output Format
{
"title": "Document Title",
"outline": [
{ "level": "H1", "text": "Introduction", "page": 1 },
{ "level": "H2", "text": "Background", "page": 2 },
{ "level": "H3", "text": "Methodology", "page": 3 }
]
}



## Performance
- **Execution Time**: <10 seconds for 50-page PDFs
- **Memory Usage**: <1GB typical, scales with document size
- **Model Size**: No ML models used, library dependencies <10MB
- **CPU Only**: No GPU dependencies

## Heading Detection Strategy
1. **Font Analysis**: Compares font sizes against page averages
2. **Pattern Recognition**: Detects numbered sections, academic formats
3. **Position Analysis**: Considers spacing and alignment
4. **Content Validation**: Filters out false positives
5. **Hierarchy Refinement**: Ensures consistent H1/H2/H3 levels

This solution is designed specifically for Challenge 1A requirements and will serve as the foundation for subsequent rounds.