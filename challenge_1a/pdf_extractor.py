import pdfplumber
from pathlib import Path
from typing import Dict, List, Any
import json
import re
from utils.heading_detector import HeadingDetector
from utils.text_processor import TextProcessor

class PDFExtractor:
    """Truly universal PDF extraction for any document type"""
    
    def __init__(self):
        self.heading_detector = HeadingDetector()
        self.text_processor = TextProcessor()
        self.max_pages = 50
        self.max_headings_total = 100  # Reasonable limit for any document
    
    def extract_structure(self, pdf_path: Path) -> Dict[str, Any]:
        """Extract structure from any PDF universally"""
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = min(len(pdf.pages), self.max_pages)
                print(f"Processing {total_pages} pages...")
                
                # Extract title
                title = self._extract_universal_title(pdf)
                
                # Extract headings universally
                headings = self._extract_universal_headings(pdf, total_pages)
                
                return {
                    "title": title,
                    "outline": headings
                }
                
        except Exception as e:
            print(f"Error extracting structure from {pdf_path}: {e}")
            return {
                "title": "",
                "outline": []
            }
    
    def _extract_universal_title(self, pdf) -> str:
        """Universal title extraction that works for any PDF"""
        
        # Method 1: PDF metadata (most reliable when available)
        if pdf.metadata and pdf.metadata.get('Title'):
            title = pdf.metadata['Title'].strip()
            if self._is_reasonable_title(title):
                return self._clean_any_title(title)
        
        # Method 2: Largest font on first page
        if len(pdf.pages) > 0:
            first_page = pdf.pages[0]
            title = self._find_title_by_largest_font(first_page)
            if title:
                return self._clean_any_title(title)
        
        return ""
    
    def _is_reasonable_title(self, text: str) -> bool:
        """Check if text could reasonably be a title (universal)"""
        
        if not text or len(text) < 3 or len(text) > 200:
            return False
        
        # Skip obvious non-titles (universal patterns only)
        if text.lower() in ['untitled', 'document', 'pdf', 'file']:
            return False
        
        # Must have some alphabetic content
        if not re.search(r'[a-zA-Z]', text):
            return False
        
        return True
    
    def _find_title_by_largest_font(self, page) -> str:
        """Find title by looking for largest font in upper area"""
        
        chars = page.chars
        if not chars:
            return ""
        
        try:
            # Look only in upper 30% of page
            page_height = max(char.get('bottom', 0) for char in chars)
            upper_limit = page_height * 0.3
            
            # Group characters by font size and line
            font_lines = {}
            
            for char in chars:
                if char.get('top', 0) <= upper_limit:
                    font_size = char.get('size', 12)
                    y_pos = round(char.get('top', 0))
                    
                    key = (font_size, y_pos)
                    if key not in font_lines:
                        font_lines[key] = []
                    font_lines[key].append(char.get('text', ''))
            
            # Find the line with largest font
            if font_lines:
                max_font = max(key[0] for key in font_lines.keys())
                
                for (font_size, y_pos), texts in font_lines.items():
                    if font_size == max_font:
                        candidate = ''.join(texts).strip()
                        if self._is_reasonable_title(candidate):
                            return candidate
        
        except Exception:
            pass
        
        return ""
    
    def _clean_any_title(self, title: str) -> str:
        """Clean title without making assumptions about content"""
        
        # Basic cleaning only
        title = re.sub(r'\s+', ' ', title).strip()
        
        # Remove obvious file artifacts (universal)
        title = re.sub(r'\.(pdf|doc|docx|txt)$', '', title, flags=re.IGNORECASE)
        title = re.sub(r'^Microsoft Word - ', '', title, flags=re.IGNORECASE)
        
        # Reasonable length limit
        if len(title) > 150:
            title = title[:150] + "..."
        
        return title.strip()
    
    def _extract_universal_headings(self, pdf, total_pages: int) -> List[Dict[str, Any]]:
        """Extract headings that work for any document type"""
        
        all_headings = []
        
        # Process each page
        for page_num in range(total_pages):
            try:
                page = pdf.pages[page_num]
                page_headings = self.heading_detector.detect_headings_universal(page, page_num + 1)
                all_headings.extend(page_headings)
                
                # Progress for large documents
                if (page_num + 1) % 10 == 0:
                    print(f"Processed {page_num + 1}/{total_pages} pages...")
                
            except Exception:
                continue
        
        print(f"Found {len(all_headings)} potential headings...")
        
        # Universal processing (no content assumptions)
        filtered = self._universal_filter(all_headings)
        deduplicated = self._universal_deduplicate(filtered)
        final = self._limit_reasonable_count(deduplicated)
        
        # Sort by page then by text
        final.sort(key=lambda x: (x.get('page', 0), x.get('text', '')))
        
        print(f"Final universal output: {len(final)} headings")
        return final
    
    def _universal_filter(self, headings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Universal filtering without content assumptions"""
        
        filtered = []
        
        for heading in headings:
            if not all(k in heading for k in ['level', 'text', 'page']):
                continue
            
            text = heading['text'].strip()
            
            # Only universal quality checks
            if self._is_universal_quality(text):
                filtered.append({
                    'level': heading['level'],
                    'text': self._clean_universal_text(text),
                    'page': heading['page']
                })
        
        return filtered
    
    def _is_universal_quality(self, text: str) -> bool:
        """Universal quality check that works for any content"""
        
        if not text or len(text) < 3:
            return False
        
        # Universal length limits
        if len(text) > 120:
            return False
        
        # Must have some letters
        letter_count = len(re.findall(r'[a-zA-Z]', text))
        if letter_count < 2:
            return False
        
        # Universal bad patterns (very minimal)
        universal_bad = [
            r'^\s*$',  # Empty
            r'^©',     # Copyright symbol
            r'^www\.',  # URL
            r'^http',   # URL
        ]
        
        for pattern in universal_bad:
            if re.match(pattern, text):
                return False
        
        return True
    
    def _clean_universal_text(self, text: str) -> str:
        """Universal text cleaning"""
        
        # Basic cleaning only
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        
        return text
    
    def _universal_deduplicate(self, headings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Universal deduplication"""
        
        seen_texts = set()
        unique = []
        
        for heading in headings:
            # Simple normalization for comparison
            normalized = re.sub(r'[^\w\s]', '', heading['text']).lower().strip()
            
            if normalized and normalized not in seen_texts:
                seen_texts.add(normalized)
                unique.append(heading)
        
        return unique
    
    def _limit_reasonable_count(self, headings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Limit to reasonable count for any document"""
        
        if len(headings) <= self.max_headings_total:
            return headings
        
        # If too many, select best ones by simple criteria
        def simple_score(h):
            text = h.get('text', '')
            score = 0
            
            # Prefer numbered sections (universal structure)
            if re.match(r'^\d+\.', text):
                score += 3
            
            # Prefer reasonable length
            if 5 <= len(text) <= 50:
                score += 1
            
            
            if text.istitle():
                score += 1
            
            return score
        
        headings.sort(key=simple_score, reverse=True)
        return headings[:self.max_headings_total]