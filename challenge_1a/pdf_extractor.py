import re
import pdfplumber
from pathlib import Path
from typing import Dict, List, Any
from utils.heading_detector import HeadingDetector
from utils.text_processor import TextProcessor

class PDFExtractor:
    """Main PDF extraction class that handles document structure analysis"""
    
    def __init__(self):
        self.heading_detector = HeadingDetector()
        self.text_processor = TextProcessor()
    
    def extract_structure(self, pdf_path: Path) -> Dict[str, Any]:
        """Extract document structure from PDF"""
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                # Extract title from first page
                title = self._extract_title(pdf)
                
                # Extract headings from all pages
                outline = self._extract_headings(pdf)
                
                return {
                    "title": title,
                    "outline": outline
                }
                
        except Exception as e:
            print(f"Error extracting structure from {pdf_path}: {e}")
            return {
                "title": "Document",
                "outline": []
            }
    
    def _extract_title(self, pdf) -> str:
        """Extract document title from first page or metadata"""
        
        # Try to get title from PDF metadata
        if pdf.metadata and pdf.metadata.get('Title'):
            title = pdf.metadata['Title'].strip()
            if title and len(title) > 0:
                return self.text_processor.clean_text(title)
        
        # Try to extract from first page content
        if len(pdf.pages) > 0:
            first_page = pdf.pages[0]
            
            # Get text objects with font information
            chars = first_page.chars
            if chars:
                # Find the largest font size text (likely title)
                title_candidate = self._find_title_from_chars(chars)
                if title_candidate:
                    return self.text_processor.clean_text(title_candidate)
        
        return "Document"
    
    def _find_title_from_chars(self, chars: List[Dict]) -> str:
        """Find title from character objects based on font size and position"""
        
        if not chars:
            return "Document"
        
        # Group characters by font size and y-position
        font_groups = {}
        
        for char in chars:
            font_size = char.get('size', 12)
            y_pos = char.get('top', 0)
            
            key = (font_size, round(y_pos, 1))
            
            if key not in font_groups:
                font_groups[key] = []
            
            font_groups[key].append(char['text'])
        
        # Find the largest font size in the upper part of the page
        max_font_size = 0
        title_text = ""
        
        for (font_size, y_pos), text_chars in font_groups.items():
            # Focus on text in upper portion of page (y < 200 typically)
            if y_pos < 200 and font_size > max_font_size:
                line_text = ''.join(text_chars).strip()
                if len(line_text) > 5 and len(line_text) < 200:  # Reasonable title length
                    max_font_size = font_size
                    title_text = line_text
        
        return title_text if title_text else "Document"
    
    def _extract_headings(self, pdf) -> List[Dict[str, Any]]:
        """Extract headings from all pages"""
        
        headings = []
        
        for page_num, page in enumerate(pdf.pages, 1):
            try:
                page_headings = self.heading_detector.detect_headings(page, page_num)
                # Clean and normalize heading text
                for heading in page_headings:
                    heading['text'] = self.text_processor.normalize_heading_text(heading['text'])
                headings.extend(page_headings)
            except Exception as e:
                print(f"Error processing page {page_num}: {e}")
                continue
        
        # Remove duplicates and sort by page number
        headings = self._deduplicate_headings(headings)
        headings.sort(key=lambda x: (x['page'], x['text']))
        
        return headings
    
    def _deduplicate_headings(self, headings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate headings"""
        
        seen = set()
        unique_headings = []
        
        for heading in headings:
            # Create a key based on text and page
            key = (heading['text'].lower().strip(), heading['page'])
            
            if key not in seen:
                seen.add(key)
                unique_headings.append(heading)
        
        return unique_headings
