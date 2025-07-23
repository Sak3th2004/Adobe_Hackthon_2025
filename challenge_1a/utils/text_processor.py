from typing import List, Optional
import re

class TextProcessor:
    """Universal text processor with minimal assumptions"""
    
    def is_likely_heading(self, text: str, context: dict = None) -> bool:
        """Universal heading detection"""
        
        if not text or len(text.strip()) < 3:
            return False
        
        text = text.strip()
        
        
        if len(text) > 120:
            return False
        
        
        letters = len(re.findall(r'[a-zA-Z]', text))
        if letters < 2:
            return False
        
        
        quality_indicators = [
            
            re.match(r'^\d+\.?\s+[A-Z]', text),
            
            
            re.match(r'^(Chapter|Section|Part|Appendix)', text, re.IGNORECASE),
            
            
            text.istitle() and len(text) > 5,
            text.isupper() and 5 <= len(text) <= 50,
            
            
            text.endswith('?') and len(text) > 8,
            text.endswith(':') and 8 <= len(text) <= 60,
        ]
        
        return any(quality_indicators)
    
    def normalize_heading_text(self, text: str) -> str:
        """Universal text normalization"""
        
        if not text:
            return ""
        
       
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        
        
        text = re.sub(r'[:;,]+$', '', text)
        
        return text.strip()
    
    def clean_text(self, text: str) -> str:
        """Universal text cleaning"""
        return self.normalize_heading_text(text)