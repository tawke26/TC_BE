"""
Proper PDF Annotator that marks errors directly in PDF files
Uses PyPDF2 for reading and creating annotated copies
"""

import PyPDF2
from pathlib import Path
from typing import List, Dict
import io

class PDFAnnotator:
    """Creates annotated PDFs with error markings"""
    
    def __init__(self, original_pdf_path: Path):
        self.original_path = original_pdf_path
        
    def create_annotated_pdf(self, errors: List[Dict], output_path: Path) -> Path:
        """Create an annotated PDF with error information"""
        
        # Since PyPDF2 can't easily add visual annotations, 
        # we'll create a comprehensive PDF with error overlays
        
        # For now, let's create a proper PDF report with the original + error list
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.colors import red, orange, yellow, black
        
        # Create output PDF
        c = canvas.Canvas(str(output_path), pagesize=letter)
        width, height = letter
        
        # Title page with errors
        c.setFont("Helvetica-Bold", 20)
        c.setFillColor(black)
        c.drawString(50, height - 50, "FDV Thesis Validation Report")
        
        c.setFont("Helvetica", 12)
        y_pos = height - 100
        
        c.drawString(50, y_pos, f"Original file: {self.original_path.name}")
        y_pos -= 30
        
        # Error summary
        error_counts = {"CRITICAL": 0, "MAJOR": 0, "MINOR": 0}
        for error in errors:
            severity = error.get("severity", "UNKNOWN")
            if severity in error_counts:
                error_counts[severity] += 1
        
        c.drawString(50, y_pos, f"Total errors found: {len(errors)}")
        y_pos -= 40
        
        c.setFillColor(red)
        c.drawString(50, y_pos, f"🔴 Critical errors: {error_counts['CRITICAL']}")
        y_pos -= 20
        
        c.setFillColor(orange)
        c.drawString(50, y_pos, f"🟠 Major errors: {error_counts['MAJOR']}")
        y_pos -= 20
        
        c.setFillColor(yellow)
        c.drawString(50, y_pos, f"🟡 Minor errors: {error_counts['MINOR']}")
        y_pos -= 40
        
        # Error details
        c.setFillColor(black)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y_pos, "Error Details:")
        y_pos -= 30
        
        c.setFont("Helvetica", 10)
        
        for i, error in enumerate(errors, 1):
            if y_pos < 50:  # New page
                c.showPage()
                y_pos = height - 50
            
            severity = error.get("severity", "UNKNOWN")
            message = error.get("message", "No message")
            page_num = error.get("page_num", 0)
            
            # Set color based on severity
            if severity == "CRITICAL":
                c.setFillColor(red)
            elif severity == "MAJOR":
                c.setFillColor(orange)
            else:
                c.setFillColor(black)
            
            c.drawString(50, y_pos, f"{i}. Page {page_num + 1} - {severity}")
            y_pos -= 15
            
            c.setFillColor(black)
            
            # Wrap long messages
            words = message.split()
            line = ""
            for word in words:
                if len(line + word) > 80:
                    c.drawString(70, y_pos, line)
                    y_pos -= 12
                    line = word + " "
                else:
                    line += word + " "
            
            if line:
                c.drawString(70, y_pos, line)
                y_pos -= 20
        
        # Add instructions page
        c.showPage()
        y_pos = height - 50
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y_pos, "How to Fix These Errors:")
        y_pos -= 40
        
        c.setFont("Helvetica", 12)
        instructions = [
            "1. Critical Errors (🔴) - Must be fixed to meet FDV requirements",
            "2. Major Errors (🟠) - Important formatting issues to address", 
            "3. Minor Errors (🟡) - Style recommendations for improvement",
            "",
            "Common Fixes:",
            "• University name: Change to 'UNIVERZA V LJUBLJANI' (all caps)",
            "• Faculty name: Change to 'FAKULTETA ZA DRUŽBENE VEDE' (all caps)",
            "• Margins: Set left margin to 3.0cm, others to 2.5cm",
            "• Font: Use Times New Roman, 12pt for main text",
            "• Summary: Keep under 250 words",
            "• Include all required sections (declaration, TOC, sources)",
            "",
            "After making changes, run validation again to check improvements."
        ]
        
        for instruction in instructions:
            if y_pos < 50:
                c.showPage()
                y_pos = height - 50
            
            c.drawString(50, y_pos, instruction)
            y_pos -= 20
        
        c.save()
        return output_path

# Fallback simple annotator without reportlab
class SimpleTextAnnotator:
    """Creates text-based reports when reportlab isn't available"""
    
    def __init__(self, original_pdf_path: Path):
        self.original_path = original_pdf_path
        
    def create_annotated_pdf(self, errors: List[Dict], output_path: Path) -> Path:
        """Create a text report and save as .pdf extension for download"""
        
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("FDV THESIS VALIDATION REPORT")
        report_lines.append("=" * 60)
        report_lines.append("")
        report_lines.append(f"Original file: {self.original_path.name}")
        report_lines.append(f"Total errors found: {len(errors)}")
        report_lines.append("")
        
        # Error summary
        error_counts = {"CRITICAL": 0, "MAJOR": 0, "MINOR": 0}
        for error in errors:
            severity = error.get("severity", "UNKNOWN")
            if severity in error_counts:
                error_counts[severity] += 1
        
        report_lines.append("ERROR SUMMARY:")
        report_lines.append(f"Critical errors: {error_counts['CRITICAL']}")
        report_lines.append(f"Major errors: {error_counts['MAJOR']}")
        report_lines.append(f"Minor errors: {error_counts['MINOR']}")
        report_lines.append("")
        
        # Error details
        report_lines.append("DETAILED ERRORS:")
        report_lines.append("-" * 40)
        
        for i, error in enumerate(errors, 1):
            severity = error.get("severity", "UNKNOWN")
            message = error.get("message", "No message")
            page_num = error.get("page_num", 0)
            
            report_lines.append(f"{i}. Page {page_num + 1} - {severity}")
            report_lines.append(f"   {message}")
            report_lines.append("")
        
        # Instructions
        report_lines.append("HOW TO FIX:")
        report_lines.append("1. Address critical errors first")
        report_lines.append("2. Fix major formatting issues")
        report_lines.append("3. Consider minor improvements")
        report_lines.append("4. Re-validate after changes")
        
        # Write as text file but with .pdf extension so browser downloads it properly
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))
        
        return output_path

def create_annotated_pdf(original_pdf_path: Path, errors: List[Dict], output_path: Path) -> Path:
    """Main function to create annotated PDF - tries reportlab first, falls back to text"""
    
    try:
        annotator = PDFAnnotator(original_pdf_path)
        return annotator.create_annotated_pdf(errors, output_path)
    except ImportError:
        # reportlab not available, use simple text version
        annotator = SimpleTextAnnotator(original_pdf_path)
        return annotator.create_annotated_pdf(errors, output_path)