"""
FDV Faculty formatting requirements for theses validation
Based on official FDV guidelines for academic papers
"""

FDV_REQUIREMENTS = {
    "front_page": {
        "university_name": {
            "text": "UNIVERZA V LJUBLJANI",
            "format": "uppercase",
            "required": True,
            "severity": "CRITICAL"
        },
        "faculty_name": {
            "text": "FAKULTETA ZA DRUŽBENE VEDE", 
            "format": "uppercase",
            "required": True,
            "severity": "CRITICAL"
        },
        "title_format": {
            "font": "Times New Roman",
            "size": 16,
            "bold": True,
            "severity": "MAJOR"
        },
        "required_elements": [
            "university_name",
            "faculty_name", 
            "title_slovenian",
            "title_english",
            "author_name",
            "location_year"
        ]
    },
    
    "margins": {
        "left": {"value": 3.0, "unit": "cm", "severity": "CRITICAL"},
        "right": {"value": 2.5, "unit": "cm", "severity": "MAJOR"},
        "top": {"value": 2.5, "unit": "cm", "severity": "MAJOR"},
        "bottom": {"value": 2.5, "unit": "cm", "severity": "MAJOR"}
    },
    
    "main_text": {
        "font": {
            "family": "Times New Roman",
            "size": 12,
            "severity": "MAJOR"
        },
        "line_spacing": {
            "value": 1.5,
            "severity": "MAJOR"
        },
        "paragraph_spacing": {
            "before": 10,
            "after": 10,
            "unit": "pt",
            "severity": "MINOR"
        },
        "alignment": {
            "type": "justified",
            "severity": "MINOR"
        }
    },
    
    "summary": {
        "max_words": {
            "value": 250,
            "severity": "MAJOR"
        },
        "min_keywords": {
            "value": 3,
            "severity": "MAJOR"
        },
        "line_spacing": {
            "value": 1.0,
            "severity": "MINOR"
        }
    },
    
    "citations": {
        "format": "APA",
        "severity": "MAJOR",
        "quotations": {
            "long_quote_lines": 5,
            "indent": {"value": 1.5, "unit": "cm"},
            "font_size": 11,
            "line_spacing": 1.0
        }
    },
    
    "tables_figures": {
        "numbering": "chapter.number",
        "title_position": {
            "tables": "above",
            "figures": "below"
        },
        "severity": "MAJOR"
    },
    
    "page_numbering": {
        "start_visible": "table_of_contents",
        "format": "arabic",
        "position": "bottom_center",
        "severity": "MAJOR"
    },
    
    "required_sections": {
        "front_page": {"required": True, "severity": "CRITICAL"},
        "title_page": {"required": True, "severity": "CRITICAL"},
        "authors_declaration": {"required": True, "severity": "CRITICAL"},
        "summary_keywords": {"required": True, "severity": "CRITICAL"},
        "table_of_contents": {"required": True, "severity": "CRITICAL"},
        "introduction": {"required": True, "severity": "CRITICAL"},
        "conclusion": {"required": True, "severity": "CRITICAL"},
        "sources": {"required": True, "severity": "CRITICAL"}
    }
}

ERROR_MESSAGES = {
    "en": {
        "university_name": "University name must be in full uppercase: UNIVERZA V LJUBLJANI",
        "faculty_name": "Faculty name must be in full uppercase: FAKULTETA ZA DRUŽBENE VEDE",
        "margin_left": "Left margin must be 3.0cm for binding (found {found}cm)",
        "margin_other": "{side} margin must be 2.5cm (found {found}cm)",
        "font_family": "Main text must use Times New Roman font (found {found})",
        "font_size": "Main text must be 12pt (found {found}pt)",
        "line_spacing": "Text must use 1.5 line spacing (found {found})",
        "summary_words": "Summary exceeds 250 words (found {found} words)",
        "summary_keywords": "Minimum 3 keywords required (found {found})",
        "title_format": "Title must be Times New Roman, 16pt, bold",
        "missing_section": "Required section '{section}' is missing"
    },
    "sl": {
        "university_name": "Ime univerze mora biti v velikih črkah: UNIVERZA V LJUBLJANI", 
        "faculty_name": "Ime fakultete mora biti v velikih črkah: FAKULTETA ZA DRUŽBENE VEDE",
        "margin_left": "Levi rob mora biti 3,0 cm za vezavo (najdeno {found} cm)",
        "margin_other": "{side} rob mora biti 2,5 cm (najdeno {found} cm)",
        "font_family": "Glavno besedilo mora uporabljati Times New Roman (najdeno {found})",
        "font_size": "Glavno besedilo mora biti 12pt (najdeno {found}pt)",
        "line_spacing": "Besedilo mora imeti 1,5 razmak med vrsticami (najdeno {found})",
        "summary_words": "Povzetek presega 250 besed (najdeno {found} besed)",
        "summary_keywords": "Potrebne so najmanj 3 ključne besede (najdeno {found})",
        "title_format": "Naslov mora biti Times New Roman, 16pt, krepko",
        "missing_section": "Obvezen razdelek '{section}' manjka"
    }
}