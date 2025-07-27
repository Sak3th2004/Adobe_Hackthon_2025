# Challenge 1B: PDF Element Classifier & Semantic Extractor


## Overview

This solution builds upon Challenge 1A and focuses on identifying and classifying fine-grained elements in PDF documents such as paragraphs, tables, lists, and figures. It structures the extracted information into a semantic representation useful for downstream applications.

## Approach

- **Semantic Classification**: Identifies and labels different types of content (e.g., paragraph, table, list, figure)
- **Layout-Aware Analysis**: Uses bounding box coordinates and page layout features
- **Textual Feature Extraction**: Leverages font styles, indentation, and pattern heuristics
- **Scalable Design**: Supports large-scale PDF document processing within system constraints

## Libraries Used

- **pdfplumber** (`0.10.3`): PDF parsing and layout detection (`~3MB`)  
- **PyMuPDF (fitz)** (`1.23.6`): Fine-grained element rendering and bounding box analysis (`~6MB`)  
- **regex** (`2023.12.25`): Structure and pattern matching (`~1MB`)  
- **json**: Output formatting (`builtin`)  

**Total size**: `~10MB` (well within `200MB` constraint)


## Architecture

The project is structured to handle end-to-end PDF processing and challenge logic execution:

```

├── ADOBE_1B/
│   ├── Collection1/              # Challenge-specific PDF collections
│   ├── Collection2/
│   ├── Collection3/
│   ├── input/                    # Input files for execution
│   ├── main.py                   # Main execution script
│   ├── requirements.txt          # Python dependencies
│   ├── execution_instructions.txt# Steps to run the project
│   └── README.md                 # Project documentation

folder for challenge 1A outside ADOBE_1B
```

- `main.py`: Handles PDF parsing using `pdfplumber`, layout detection, and applies regex for structured extraction.
- `input/`: Contains input files (e.g., PDF paths or challenge input) required for running `main.py`.
- `CollectionX/`: Contains challenge-specific sets of PDFs.
- `requirements.txt`: Lists all required Python packages.



## Building and Running

### Build Docker Image

```bash
docker build --platform linux/amd64 -t challenge1b:latest .
```

### Run Solution (Official Format)

```bash
docker run --rm \
  -v $(pwd)/input:/app/input:ro \
  -v $(pwd)/output:/app/output \
  --network none \
  challenge1b:latest
```

## Directory Structure

```

├── ADOBE_1B/
│   ├── input/                    # Contains all the PDF collections (Collection1, Collection2, Collection3)
│   │   ├── Collection1/
│   │   ├── Collection2/
│   │   └── Collection3/
│   ├── main.py                   # Main script to execute the challenge
│   ├── requirements.txt          # List of required Python packages
│   ├── execution_instructions.txt# Execution and usage guide
│   └── README.md                 # Project documentation

folder for Challenge 1A (outside ADOBE_1B)
```


## Features

- ✅ **PDF Element Detection**: Classifies elements into paragraph, table, list, figure  
- ✅ **Hierarchical Output**: Maintains logical reading order and element relationships  
- ✅ **Layout-Aware**: Considers visual alignment and positions  
- ✅ **Pattern-Driven**: Uses regex and font features for robust detection  
- ✅ **Offline Execution**: Fully runs offline within a Docker container  
- ✅ **Performance Compliant**: Operates under 200MB image and 16GB RAM limit  



## Output Format

```json
[
  {
    "type": "paragraph",
    "text": "This is a paragraph of text extracted from the PDF.",
    "page": 1,
    "bbox": [72, 120, 540, 160]
  },
  {
    "type": "table",
    "text": "Table content goes here...",
    "page": 2,
    "bbox": [70, 200, 550, 400]
  },
  {
    "type": "list",
    "text": "- Item 1\n- Item 2\n- Item 3",
    "page": 3,
    "bbox": [60, 180, 540, 300]
  },
  {
    "type": "figure",
    "caption": "Figure 1: Sample image",
    "page": 4,
    "bbox": [100, 220, 500, 380]
  }
]

```

## Performance

- ✅ **Execution Time**: <10 seconds for 50-page PDFs  
- ✅ **Memory Usage**: <1GB typical, scales with document size  
- ✅ **Model Size**: No ML models used, library dependencies <10MB  
- ✅ **CPU Only**: No GPU dependencies  

## Heading Detection Strategy

1. **Font Analysis**: Compares font sizes against page averages  
2. **Pattern Recognition**: Detects numbered sections, academic formats  
3. **Position Analysis**: Considers spacing and alignment  
4. **Content Validation**: Filters out false positives  
5. **Hierarchy Refinement**: Ensures consistent H1/H2/H3 levels  

## Usage Instructions

1. 📂 **Place PDFs**: Copy your PDF files into the `ADOBE_1B/input/` directory  
2. 🛠️ **Build**: Run the Docker build command provided above  
3. 🚀 **Execute**: Run the Docker run command provided above  
4. 📄 **Results**: Check the `ADOBE_1B/output/` directory for JSON output  

💡 This solution is designed specifically for **Challenge 1B**, focusing on precise heading detection and hierarchical structuring. It will serve as the basis for subsequent challenge phases.
