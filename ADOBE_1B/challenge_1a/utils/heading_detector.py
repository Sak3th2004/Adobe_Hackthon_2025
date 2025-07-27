from typing import List, Dict, Any
import re

class HeadingDetector:
    """Universal heading detector that adapts to any document"""
    
    def detect_headings_universal(self, page, page_num: int) -> List[Dict[str, Any]]:
        """Detect headings using universal methods"""
        
        headings = []
        
        try:
            
            font_headings = self._detect_by_adaptive_font(page, page_num)
            headings.extend(font_headings)
            
            
            pattern_headings = self._detect_by_universal_patterns(page, page_num)
            headings.extend(pattern_headings)
            
        except Exception:
            pass
        
        return headings
    
    def _detect_by_adaptive_font(self, page, page_num: int) -> List[Dict[str, Any]]:
        """Adaptive font detection that works for any document"""
        
        headings = []
        chars = page.chars
        
        if not chars:
            return headings
        
        try:
            
            font_sizes = [c.get('size', 12) for c in chars if c.get('size', 0) > 0]
            
            if len(font_sizes) < 20:  
                return headings
            
            
            font_sizes.sort()
            median_font = font_sizes[len(font_sizes) // 2]
            p75_font = font_sizes[int(len(font_sizes) * 0.75)]
            
            
            heading_threshold = max(median_font * 1.1, median_font + 1)
            
            
            lines = self._group_chars_by_position(chars)
            
            for line_chars in lines:
                if not line_chars:
                    continue
                
                
                line_text = ''.join(c.get('text', '') for c in line_chars).strip()
                line_fonts = [c.get('size', 12) for c in line_chars if c.get('size', 0) > 0]
                
                if not line_text or not line_fonts:
                    continue
                
                avg_line_font = sum(line_fonts) / len(line_fonts)
                
                
                if (avg_line_font >= heading_threshold and 
                    self._is_reasonable_heading_text(line_text)):
                    
                    level = self._determine_level_adaptive(avg_line_font, median_font, p75_font)
                    
                    headings.append({
                        'level': level,
                        'text': line_text,
                        'page': page_num
                    })
        
        except Exception:
            pass
        
        return headings
    
    def _detect_by_universal_patterns(self, page, page_num: int) -> List[Dict[str, Any]]:
        """Detect using universal structural patterns"""
        
        headings = []
        
        try:
            text = page.extract_text()
            if not text:
                return headings
            
            lines = text.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                
                if self._matches_universal_pattern(line):
                    level = self._get_pattern_level(line)
                    
                    headings.append({
                        'level': level,
                        'text': line,
                        'page': page_num
                    })
        
        except Exception:
            pass
        
        return headings
    
    def _group_chars_by_position(self, chars: List[Dict]) -> List[List[Dict]]:
        """Group characters into lines by position"""
        
        if not chars:
            return []
        
        try:
           
            sorted_chars = sorted(chars, key=lambda c: (c.get('top', 0), c.get('x0', 0)))
            
            lines = []
            current_line = []
            current_y = None
            tolerance = 3
            
            for char in sorted_chars:
                char_y = char.get('top', 0)
                
                if current_y is None or abs(char_y - current_y) <= tolerance:
                    current_line.append(char)
                    current_y = char_y
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = [char]
                    current_y = char_y
            
            if current_line:
                lines.append(current_line)
            
            return lines
        
        except Exception:
            return []
    
    def _is_reasonable_heading_text(self, text: str) -> bool:
        """Check if text could reasonably be a heading (universal)"""
        
        if len(text) < 3 or len(text) > 100:
            return False
        
        
        if not re.search(r'[a-zA-Z]', text):
            return False
        
        
        letter_ratio = len(re.findall(r'[a-zA-Z]', text)) / len(text)
        if letter_ratio < 0.3:  
            return False
        
        return True
    
    def _determine_level_adaptive(self, font_size: float, median: float, p75: float) -> str:
        """Determine level based on font size relative to document"""
        
        if font_size >= p75 * 1.2:
            return "H1"
        elif font_size >= median * 1.3:
            return "H2"
        else:
            return "H3"
    
    def _matches_universal_pattern(self, text: str) -> bool:
        """Check for universal structural patterns"""
        
        # Universal patterns that appear in many document types
        universal_patterns = [
            r'^\d+\.?\s+[A-Z]',  
            r'^\d+\.\d+\s+[A-Z]', 
            r'^(Chapter|Section|Part|Appendix)\s+\d+',  
            r'^[A-Z][A-Z\s]{4,30}$', 
            r'^[A-Z][a-z]+(\s+[A-Z][a-z]+){1,4}$',  
        ]
        
        for pattern in universal_patterns:
            if re.match(pattern, text):
                return True
        
        return False
    
    def _get_pattern_level(self, text: str) -> str:
        """Get heading level based on pattern"""
        
        if re.match(r'^\d+\.\s+', text):
            return "H1"
        elif re.match(r'^\d+\.\d+\s+', text):
            return "H2"
        elif re.match(r'^(Chapter|CHAPTER)', text):
            return "H1"
        elif re.match(r'^(Section|SECTION)', text):
            return "H2"
        elif text.isupper() and len(text) > 10:
            return "H1"
        elif text.istitle():
            return "H2"
        else:
            return "H3"