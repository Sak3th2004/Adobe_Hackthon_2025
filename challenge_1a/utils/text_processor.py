import re
from typing import List, Optional

class TextProcessor:
    """Utility class for text processing operations"""
    
    def __init__(self):
        pass
    
    def clean_text(self, text: str) -> str:
        """Clean extracted text"""
        
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that might cause issues
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        
        return text.strip()
    
    def is_likely_heading(self, text: str, context: dict = None) -> bool:
        """Determine if text is likely a heading"""
        
        if not text or len(text.strip()) < 2:
            return False
        
        text = text.strip()
        
        # Too long to be a heading
        if len(text) > 200:
            return False
        
        # Common heading indicators
        heading_indicators = [
            text.isupper(),
            text.istitle(),
            re.match(r'^\d+\.', text),
            re.match(r'^(Chapter|Section|Part)', text, re.IGNORECASE),
            text.endswith(':') and len(text) < 50
        ]
        
        return any(heading_indicators)
    
    def normalize_heading_text(self, text: str) -> str:
        """Normalize heading text for consistency"""
        
        if not text:
            return ""
        
        # Clean the text first
        text = self.clean_text(text)
        
        # Remove trailing colons
        text = re.sub(r':+$', '', text)
        
        # Normalize multiple spaces
        text = re.sub(r'\s{2,}', ' ', text)
        
        return text.strip()
