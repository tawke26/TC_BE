"""
Ultra Simple PDF Processing Module for FDV Thesis Validation
Uses only PyPDF2 and creates text reports instead of PDF annotations
"""

import re
import PyPDF2
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass

@dataclass
class ErrorAnnotation:
    page_num: int
    rect: Tuple[float, float, float, float]  # x0, y0, x1, y1
    severity: str
    message: str
    error_type: str

@dataclass 
class FontInfo:
    family: str
    size: float
    bold: bool
    italic: bool

@dataclass
class MarginInfo:
    left: float
    right: float
    top: float
    bottom: float
    unit: str = "cm"

class UltraSimplePDFProcessor:
    """Ultra simplified PDF processing class using only PyPDF2"""
    
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.errors = []
        
        # Load PDF
        with open(file_path, 'rb') as file:
            self.reader = PyPDF2.PdfReader(file)
            self.pages = [page for page in self.reader.pages]
        
    # ========== AGENT TOOLS ==========
    
    def extract_text_from_page(self, page_num: int) -> str:
        """Tool: Extract all text from specified page with proper encoding"""
        if page_num >= len(self.pages):
            return ""
        
        try:
            text = self.pages[page_num].extract_text()
            # Handle encoding issues by replacing problematic characters
            return text.encode("utf-8", errors="replace").decode("utf-8")
        except Exception as e:
            return f"Error extracting text: {str(e)}"
    
    def detect_page_type(self, page_num: int) -> str:
        """Tool: Detect the type of page (front_page, toc, chapter, etc.)"""
        text = self.extract_text_from_page(page_num).lower()
        
        # Front page indicators
        if any(x in text for x in ["univerza v ljubljani", "fakulteta za družbene vede"]):
            return "front_page"
        
        # Table of contents
        if any(x in text for x in ["kazalo", "table of contents", "vsebina"]):
            return "table_of_contents"
        
        # Summary page
        if any(x in text for x in ["povzetek", "summary", "ključne besede", "keywords"]):
            return "summary_page"
        
        # Declaration
        if any(x in text for x in ["izjava", "declaration", "avtorstvo"]):
            return "declaration"
        
        # Sources
        if any(x in text for x in ["viri", "literatura", "sources", "bibliography"]):
            return "sources"
        
        # Appendix
        if any(x in text for x in ["priloga", "appendix"]):
            return "appendix"
        
        # Chapter start (numbered chapters)
        if re.search(r'^\s*\d+\s+[A-ŽŠČĐĆ]', text, re.MULTILINE):
            return "chapter_start"
        
        return "content"
    
    def measure_margins(self, page_num: int) -> MarginInfo:
        """Tool: Estimate page margins (simplified version)"""
        if page_num >= len(self.pages):
            return MarginInfo(0, 0, 0, 0)
        
        # For PyPDF2, we can't get exact margins, so we estimate
        # Standard A4 page with typical margins
        return MarginInfo(
            left=2.5,   # Estimated
            right=2.5,  # Estimated
            top=2.5,    # Estimated
            bottom=2.5  # Estimated
        )
    
    def get_font_properties(self, page_num: int, text_pattern: str = None) -> List[FontInfo]:
        """Tool: Get font properties (simplified - returns estimates)"""
        # PyPDF2 has limited font detection, so we return reasonable defaults
        return [FontInfo(
            family="Times New Roman",  # Assumed
            size=12.0,                 # Assumed
            bold=False,                # Can't detect easily
            italic=False               # Can't detect easily
        )]
    
    def find_text_position(self, page_num: int, text: str) -> Optional[Tuple[float, float, float, float]]:
        """Tool: Find position of specific text on page (estimated)"""
        page_text = self.extract_text_from_page(page_num)
        
        if text.lower() in page_text.lower():
            # Return estimated position (top of page)
            return (50, 50, 300, 80)  # x0, y0, x1, y1
        
        return None
    
    def count_words(self, text: str) -> int:
        """Tool: Count words in text"""
        words = re.findall(r'\b\w+\b', text)
        return len(words)
    
    def detect_language(self, text: str) -> str:
        """Tool: Simple language detection for Slovenian/English"""
        slovenian_indicators = ['in', 'je', 'da', 'se', 'na', 'za', 'so', 'kot', 'ter', 'tudi']
        english_indicators = ['the', 'and', 'of', 'to', 'is', 'in', 'that', 'for', 'as', 'with']
        
        text_lower = text.lower()
        
        sl_count = sum(1 for word in slovenian_indicators if f' {word} ' in text_lower)
        en_count = sum(1 for word in english_indicators if f' {word} ' in text_lower)
        
        return "slovenian" if sl_count > en_count else "english"
    
    def check_text_format(self, text: str, expected_format: str) -> bool:
        """Tool: Check if text matches expected format"""
        if expected_format == "uppercase":
            return text.isupper()
        elif expected_format == "lowercase":
            return text.islower()
        elif expected_format == "title_case":
            return text.istitle()
        
        return False
    
    def measure_line_spacing(self, page_num: int) -> float:
        """Tool: Estimate line spacing (simplified)"""
        # Since PyPDF2 can't measure line spacing accurately, return default
        return 1.5
    
    def mark_error(self, page_num: int, rect: Tuple[float, float, float, float], 
                   severity: str, message: str, error_type: str = "formatting"):
        """Tool: Mark an error location for annotation"""
        error = ErrorAnnotation(
            page_num=page_num,
            rect=rect,
            severity=severity,
            message=message,
            error_type=error_type
        )
        self.errors.append(error)
    
    def get_page_count(self) -> int:
        """Tool: Get total number of pages"""
        return len(self.pages)
    
    def extract_table_of_contents(self, page_num: int) -> List[Dict]:
        """Tool: Extract table of contents structure"""
        text = self.extract_text_from_page(page_num)
        
        # Simple TOC extraction using regex
        toc_entries = []
        lines = text.split('\n')
        
        for line in lines:
            # Match patterns like "1.2 Chapter Name ........ 15"
            match = re.match(r'(\d+(?:\.\d+)*)\s+(.+?)\s*\.+\s*(\d+)', line.strip())
            if match:
                toc_entries.append({
                    "number": match.group(1),
                    "title": match.group(2).strip(),
                    "page": int(match.group(3))
                })
        
        return toc_entries
    
    # ========== ANNOTATION SYSTEM ==========
    
    def generate_annotated_pdf(self, errors: List[Dict], output_path: Path) -> Path:
        """Generate a proper annotated PDF with error markings"""
        from pdf_annotator import create_annotated_pdf
        return create_annotated_pdf(self.file_path, errors, output_path)
