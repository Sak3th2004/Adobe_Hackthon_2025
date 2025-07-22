import re
from typing import List, Dict, Any

class HeadingDetector:
    """Detects headings in PDF pages using multiple strategies"""
    
    def __init__(self):
        # Common heading patterns
        self.heading_patterns = [
            r'^(\d+\.?\s+[A-Z][^.]*)',  # 1. Introduction, 2. Background
            r'^([A-Z][A-Z\s]+)$',       # ALL CAPS headings
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*$',  # Title Case headings
            r'^(Chapter\s+\d+[:\-\s]*.+)',  # Chapter headings
            r'^(Section\s+\d+[:\-\s]*.+)',  # Section headings
        ]
    
    def detect_headings(self, page, page_num: int) -> List[Dict[str, Any]]:
        """Detect headings on a single page"""
        
        headings = []
        
        try:
            # Method 1: Use character-level font analysis
            chars_headings = self._detect_by_font_analysis(page, page_num)
            headings.extend(chars_headings)
            
            # Method 2: Use text pattern matching as fallback
            if len(headings) == 0:
                pattern_headings = self._detect_by_patterns(page, page_num)
                headings.extend(pattern_headings)
                
        except Exception as e:
            print(f"Error detecting headings on page {page_num}: {e}")
        
        return headings
    
    def _detect_by_font_analysis(self, page, page_num: int) -> List[Dict[str, Any]]:
        """Detect headings using font size and style analysis"""
        
        headings = []
        chars = page.chars
        
        if not chars:
            return headings
        
        # Calculate average font size for the page
        font_sizes = [char.get('size', 12) for char in chars if char.get('size')]
        if not font_sizes:
            return headings
            
        avg_font_size = sum(font_sizes) / len(font_sizes)
        
        # Group text by lines based on y-position
        lines = self._group_chars_into_lines(chars)
        
        for line_chars in lines:
            line_text = ''.join([char['text'] for char in line_chars]).strip()
            
            if len(line_text) < 3 or len(line_text) > 200:
                continue
            
            # Calculate line statistics
            line_font_sizes = [char.get('size', 12) for char in line_chars]
            avg_line_font = sum(line_font_sizes) / len(line_font_sizes)
            
            # Check if this line could be a heading
            is_heading = False
            heading_level = "H3"
            
            # Font size based detection
            if avg_line_font > avg_font_size * 1.2:
                is_heading = True
                if avg_line_font > avg_font_size * 1.5:
                    heading_level = "H1"
                elif avg_line_font > avg_font_size * 1.3:
                    heading_level = "H2"
                else:
                    heading_level = "H3"
            
            # Pattern-based detection
            elif self._matches_heading_pattern(line_text):
                is_heading = True
                heading_level = self._determine_level_from_pattern(line_text)
            
            if is_heading:
                headings.append({
                    "level": heading_level,
                    "text": line_text,
                    "page": page_num
                })
        
        return headings
    
    def _group_chars_into_lines(self, chars: List[Dict]) -> List[List[Dict]]:
        """Group characters into lines based on y-position"""
        
        if not chars:
            return []
        
        # Sort characters by y-position, then x-position
        sorted_chars = sorted(chars, key=lambda c: (c.get('top', 0), c.get('x0', 0)))
        
        lines = []
        current_line = []
        current_y = None
        y_tolerance = 2  # Pixels tolerance for same line
        
        for char in sorted_chars:
            char_y = char.get('top', 0)
            
            if current_y is None or abs(char_y - current_y) <= y_tolerance:
                # Same line
                current_line.append(char)
                current_y = char_y
            else:
                # New line
                if current_line:
                    lines.append(current_line)
                current_line = [char]
                current_y = char_y
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def _detect_by_patterns(self, page, page_num: int) -> List[Dict[str, Any]]:
        """Detect headings using text pattern matching"""
        
        headings = []
        text = page.extract_text()
        
        if not text:
            return headings
        
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if self._matches_heading_pattern(line):
                level = self._determine_level_from_pattern(line)
                headings.append({
                    "level": level,
                    "text": line,
                    "page": page_num
                })
        
        return headings
    
    def _matches_heading_pattern(self, text: str) -> bool:
        """Check if text matches common heading patterns"""
        
        for pattern in self.heading_patterns:
            if re.match(pattern, text):
                return True
        
        # Additional heuristics
        if (len(text) > 5 and len(text) < 100 and 
            (text.isupper() or text.istitle()) and 
            not text.endswith('.')):
            return True
        
        return False
    
    def _determine_level_from_pattern(self, text: str) -> str:
        """Determine heading level based on text pattern"""
        
        # Number-based hierarchy
        if re.match(r'^\d+\.\s+', text):
            return "H1"
        elif re.match(r'^\d+\.\d+\s+', text):
            return "H2"
        elif re.match(r'^\d+\.\d+\.\d+\s+', text):
            return "H3"
        
        # Chapter/Section patterns
        if re.match(r'^(Chapter|CHAPTER)', text):
            return "H1"
        elif re.match(r'^(Section|SECTION)', text):
            return "H2"
        
        # Default based on text characteristics
        if text.isupper() and len(text) < 50:
            return "H1"
        elif text.istitle():
            return "H2"
        else:
            return "H3"
