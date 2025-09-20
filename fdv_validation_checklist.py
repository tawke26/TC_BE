"""
Comprehensive FDV Thesis Validation Checklist
Organized by error categories and severity levels
"""

FDV_VALIDATION_CHECKLIST = {
    
    # GROUP 1: CRITICAL IDENTITY ERRORS (Must be exact)
    "CRITICAL_IDENTITY": {
        "severity": "CRITICAL",
        "description": "University and faculty identification must be exact",
        "checks": [
            {
                "id": "C001",
                "rule": "University name must be 'UNIVERZA V LJUBLJANI' (all uppercase)",
                "location": "Front page, header",
                "requirement": "Exact match required",
                "common_errors": ["University of Ljubljana", "Univerza v Ljubljani", "UL"]
            },
            {
                "id": "C002", 
                "rule": "Faculty name must be 'FAKULTETA ZA DRUŽBENE VEDE' (all uppercase)",
                "location": "Front page, below university name",
                "requirement": "Exact match required",
                "common_errors": ["Faculty of Social Sciences", "Fakulteta za družbene vede"]
            },
            {
                "id": "C003",
                "rule": "Degree type must match FDV programs",
                "location": "Front page",
                "requirement": "Must be valid FDV degree (magistrska naloga, diplomska naloga)",
                "common_errors": ["Bachelor thesis", "Master thesis", "PhD dissertation"]
            }
        ]
    },

    # GROUP 2: CRITICAL STRUCTURE ERRORS (Missing required sections)
    "CRITICAL_STRUCTURE": {
        "severity": "CRITICAL",
        "description": "Required sections that must exist in thesis",
        "checks": [
            {
                "id": "C004",
                "rule": "Must have Author's Declaration (Izjava o avtorstvu)",
                "location": "After front page, before content",
                "requirement": "Dedicated page with author's signature statement",
                "search_terms": ["izjava", "avtorstvo", "declaration", "author"]
            },
            {
                "id": "C005",
                "rule": "Must have Abstract/Summary in Slovenian (Povzetek)",
                "location": "Before table of contents",
                "requirement": "Maximum 250 words, in Slovenian language",
                "search_terms": ["povzetek", "abstract", "summary"]
            },
            {
                "id": "C006",
                "rule": "Must have Abstract/Summary in English",
                "location": "After Slovenian abstract",
                "requirement": "Maximum 250 words, in English language",
                "search_terms": ["abstract", "summary"]
            },
            {
                "id": "C007",
                "rule": "Must have Table of Contents (Kazalo vsebine)",
                "location": "After abstracts, before main content",
                "requirement": "Complete chapter listing with page numbers",
                "search_terms": ["kazalo", "vsebina", "contents", "table"]
            },
            {
                "id": "C008",
                "rule": "Must have Sources/Bibliography (Viri in literatura)",
                "location": "End of thesis, before appendices",
                "requirement": "Complete reference list in APA format",
                "search_terms": ["viri", "literatura", "sources", "bibliography", "references"]
            }
        ]
    },

    # GROUP 3: MAJOR LANGUAGE ERRORS
    "MAJOR_LANGUAGE": {
        "severity": "MAJOR",
        "description": "Language and terminology requirements",
        "checks": [
            {
                "id": "M001",
                "rule": "Title must be in both Slovenian and English",
                "location": "Front page",
                "requirement": "Both versions clearly displayed",
                "validation": "Check for both language versions present"
            },
            {
                "id": "M002",
                "rule": "Keywords must be provided (minimum 3)",
                "location": "After abstracts",
                "requirement": "3+ keywords in both Slovenian and English",
                "search_terms": ["ključne besede", "keywords"]
            },
            {
                "id": "M003",
                "rule": "Main text must be in Slovenian",
                "location": "Throughout main content",
                "requirement": "Academic Slovenian language",
                "validation": "Language detection on content chapters"
            },
            {
                "id": "M004",
                "rule": "Proper Slovenian academic terminology",
                "location": "Throughout thesis",
                "requirement": "Use of appropriate academic Slovenian terms",
                "validation": "Check for English terms where Slovenian equivalents exist"
            }
        ]
    },

    # GROUP 4: MAJOR FORMATTING ERRORS
    "MAJOR_FORMATTING": {
        "severity": "MAJOR", 
        "description": "Core formatting requirements",
        "checks": [
            {
                "id": "M005",
                "rule": "Font must be Times New Roman, 12pt",
                "location": "Main text throughout",
                "requirement": "Consistent font family and size",
                "validation": "Check font properties in main content"
            },
            {
                "id": "M006",
                "rule": "Page margins: 3cm left, 2.5cm top/right/bottom",
                "location": "All pages",
                "requirement": "Consistent margins throughout document",
                "validation": "Measure page margins"
            },
            {
                "id": "M007",
                "rule": "Line spacing 1.5 for main text",
                "location": "Main content chapters",
                "requirement": "1.5 line spacing (not single or double)",
                "validation": "Check line spacing in paragraphs"
            },
            {
                "id": "M008",
                "rule": "Page numbering must be consistent",
                "location": "All pages after front matter",
                "requirement": "Sequential Arabic numerals",
                "validation": "Check page number sequence"
            },
            {
                "id": "M009",
                "rule": "Abstract must not exceed 250 words",
                "location": "Both Slovenian and English abstracts",
                "requirement": "Word count ≤ 250 for each abstract",
                "validation": "Count words in abstract sections"
            }
        ]
    },

    # GROUP 5: MAJOR CITATION ERRORS
    "MAJOR_CITATIONS": {
        "severity": "MAJOR",
        "description": "Academic citation and reference requirements",
        "checks": [
            {
                "id": "M010",
                "rule": "Must use APA citation style",
                "location": "In-text citations and reference list",
                "requirement": "Consistent APA 7th edition format",
                "validation": "Check citation format patterns"
            },
            {
                "id": "M011",
                "rule": "In-text citations must match reference list",
                "location": "Throughout text and bibliography",
                "requirement": "Every citation has corresponding reference",
                "validation": "Cross-reference citations and bibliography"
            },
            {
                "id": "M012",
                "rule": "Reference list must be alphabetically ordered",
                "location": "Sources/Bibliography section",
                "requirement": "APA alphabetical ordering by author surname",
                "validation": "Check alphabetical order"
            },
            {
                "id": "M013",
                "rule": "All references must be complete",
                "location": "Sources/Bibliography section",
                "requirement": "Author, year, title, publisher/journal details",
                "validation": "Check completeness of reference entries"
            }
        ]
    },

    # GROUP 6: MINOR STYLE ERRORS
    "MINOR_STYLE": {
        "severity": "MINOR",
        "description": "Style and presentation refinements",
        "checks": [
            {
                "id": "m001",
                "rule": "Chapter headings should be properly formatted",
                "location": "Chapter beginnings",
                "requirement": "Consistent heading styles and numbering",
                "validation": "Check heading hierarchy and formatting"
            },
            {
                "id": "m002",
                "rule": "Table of contents should match actual headings",
                "location": "TOC vs. actual chapter headings",
                "requirement": "Exact match between TOC and headings",
                "validation": "Compare TOC entries with actual headings"
            },
            {
                "id": "m003",
                "rule": "Figures and tables should be numbered and titled",
                "location": "Throughout document",
                "requirement": "Sequential numbering with descriptive titles",
                "validation": "Check figure/table numbering consistency"
            },
            {
                "id": "m004",
                "rule": "Proper paragraph indentation and spacing",
                "location": "Main text",
                "requirement": "Consistent paragraph formatting",
                "validation": "Check paragraph structure"
            },
            {
                "id": "m005",
                "rule": "No orphaned headings at page breaks",
                "location": "Page transitions",
                "requirement": "Headings should have following content on same page",
                "validation": "Check page break positioning"
            }
        ]
    },

    # GROUP 7: CONTENT COMPLETENESS
    "CONTENT_COMPLETENESS": {
        "severity": "MAJOR",
        "description": "Required content sections and elements",
        "checks": [
            {
                "id": "M014",
                "rule": "Must have Introduction chapter (Uvod)",
                "location": "First main chapter",
                "requirement": "Dedicated introduction section",
                "search_terms": ["uvod", "introduction"]
            },
            {
                "id": "M015", 
                "rule": "Must have Conclusion chapter (Zaključek)",
                "location": "Final main chapter",
                "requirement": "Dedicated conclusion section",
                "search_terms": ["zaključek", "conclusion"]
            },
            {
                "id": "M016",
                "rule": "Must have minimum required length",
                "location": "Main content",
                "requirement": "Appropriate length for degree type",
                "validation": "Check total word/page count"
            },
            {
                "id": "M017",
                "rule": "Chapter structure should be logical",
                "location": "Chapter organization",
                "requirement": "Logical flow from introduction to conclusion",
                "validation": "Check chapter numbering and progression"
            }
        ]
    }
}

# Validation priority order
VALIDATION_PRIORITY = [
    "CRITICAL_IDENTITY",
    "CRITICAL_STRUCTURE", 
    "MAJOR_LANGUAGE",
    "MAJOR_FORMATTING",
    "MAJOR_CITATIONS",
    "CONTENT_COMPLETENESS",
    "MINOR_STYLE"
]

# Error reporting templates
ERROR_TEMPLATES = {
    "CRITICAL": "CRITICAL ERROR: {message} | Location: {location} | Fix: {fix_instruction}",
    "MAJOR": "MAJOR ERROR: {message} | Location: {location} | Fix: {fix_instruction}",
    "MINOR": "MINOR ERROR: {message} | Location: {location} | Fix: {fix_instruction}"
}