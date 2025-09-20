"""
Simple AI Validator that directly calls the AI without complex tool system
"""

import os
import PyPDF2
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from typing import List, Dict

load_dotenv()

class SimpleAIValidator:
    """Direct AI validation without complex agent system"""
    
    def __init__(self, pdf_path: Path):
        self.pdf_path = pdf_path
        self.client = OpenAI(
            base_url=os.getenv("API_BASE_URL", "https://openrouter.ai/api/v1"),
            api_key=os.getenv("DEEPSEEK_API_KEY")
        )
        self.model = os.getenv("MODEL_NAME", "openrouter/sonoma-sky-alpha")
    
    def extract_pdf_text(self) -> str:
        """Extract text from entire PDF"""
        full_text = ""
        try:
            with open(self.pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for i, page in enumerate(reader.pages):  # All pages
                    try:
                        text = page.extract_text()
                        text = text.encode("utf-8", errors="replace").decode("utf-8")
                        full_text += f"\n\n--- PAGE {i+1} ---\n{text}"
                    except Exception as e:
                        full_text += f"\n\n--- PAGE {i+1} ---\nError extracting: {e}"
        except Exception as e:
            return f"Error reading PDF: {e}"
        
        return full_text
    
    def validate_with_ai(self) -> List[Dict]:
        """Efficient single-pass AI validation"""
        
        # Extract text from key sections
        pdf_text = self.extract_pdf_text()
        
        # Create smart sample: front + middle + end
        front_text = pdf_text[:10000]  # First 10K chars (covers title, summary, TOC)
        
        if len(pdf_text) > 20000:
            # For long docs: front + sample from middle + end
            middle_sample = pdf_text[len(pdf_text)//2:len(pdf_text)//2 + 5000]  # 5K from middle
            end_text = pdf_text[-5000:]  # Last 5K chars (covers conclusion, sources)
            combined_text = f"{front_text}\n\n--- MIDDLE SAMPLE ---\n{middle_sample}\n\n--- END SECTION ---\n{end_text}"
        else:
            # For short docs: use all text up to 20K
            combined_text = pdf_text[:20000]
        
        # Single comprehensive validation
        prompt = f"""
You are validating an FDV thesis against formatting requirements. 

CRITICAL REQUIREMENTS TO CHECK:
1. University name MUST be "UNIVERZA V LJUBLJANI" (uppercase)
2. Faculty name MUST be "FAKULTETA ZA DRUŽBENE VEDE" (uppercase) 
3. Must have Author's Declaration section
4. Summary max 250 words, minimum 3 keywords
5. Required sections: front page, declaration, summary, TOC, introduction, conclusion, sources
6. Title in both Slovenian and English
7. Proper structure and formatting

VALIDATION RULES:
- Only report CLEAR violations of FDV requirements
- Focus on CRITICAL and MAJOR issues first
- Be specific about fixes needed
- Maximum 15 total errors to avoid overwhelming user
- Don't invent problems - only report real violations

THESIS TEXT TO VALIDATE:
{combined_text}

Return JSON array of the most important errors found:
[{{"page_num": 0, "severity": "CRITICAL", "message": "Specific error and fix needed", "error_type": "formatting"}}]
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2500
            )
            
            return self.parse_ai_response(response.choices[0].message.content)
            
        except Exception as e:
            return [{
                "page_num": 0,
                "severity": "CRITICAL",
                "message": f"AI validation failed: {str(e)}",
                "error_type": "system_error"
            }]
    
    def validate_section(self, text_section: str, section_type: str) -> List[Dict]:
        """Validate a specific section of the thesis"""
        
        if section_type == "front_matter":
            focus = """
            FOCUS ON FRONT MATTER:
            - University name: "UNIVERZA V LJUBLJANI" (uppercase)
            - Faculty name: "FAKULTETA ZA DRUŽBENE VEDE" (uppercase)
            - Title in Slovenian and English
            - Author declaration
            - Summary word count (max 250 words)
            - Keywords (minimum 3)
            """
        elif section_type == "content":
            focus = """
            FOCUS ON MAIN CONTENT:
            - Chapter formatting and numbering
            - Font consistency (Times New Roman, 12pt)
            - Citation format (APA style)
            - Table of contents structure
            - Proper headings and subheadings
            """
        else:  # end_matter
            focus = """
            FOCUS ON END MATTER:
            - Sources/bibliography section
            - Proper citation format
            - Appendices if present
            - Page numbering consistency
            """
        
        prompt = f"""
You are validating an FDV thesis section. {focus}

IMPORTANT VALIDATION RULES:
- Only report CLEAR violations of FDV requirements, not suggestions
- Focus on CRITICAL issues: wrong university/faculty names, missing required sections, major formatting problems
- Ignore minor style variations unless they clearly violate FDV standards
- Maximum 8 errors per section - prioritize the most important ones
- Be specific about what needs to be fixed and why it violates FDV requirements

TEXT SECTION:
{text_section}

Find the TOP 8 most important violations in this section. Return JSON array (max 8 items):
[{{"page_num": 0, "severity": "CRITICAL", "message": "Specific error description and how to fix it", "error_type": "formatting"}}]

If you find fewer than 8 real violations, only report what you actually find. Don't invent problems.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1500
            )
            
            return self.parse_ai_response(response.choices[0].message.content)
            
        except Exception as e:
            return [{
                "page_num": 0,
                "severity": "CRITICAL",
                "message": f"Section validation failed: {str(e)}",
                "error_type": "system_error"
            }]
    
    def validate_overall_structure(self, full_text: str) -> List[Dict]:
        """Check overall document structure"""
        
        prompt = f"""
Check if this FDV thesis has ALL required sections:

REQUIRED SECTIONS:
✓ Front page with university/faculty names
✓ Author's declaration (izjava o avtorstvu)
✓ Summary in Slovenian (povzetek)
✓ Summary in English
✓ Table of contents (kazalo)
✓ Introduction (uvod)
✓ Main content chapters
✓ Conclusion (zaključek)
✓ Sources/bibliography (viri/literatura)

DOCUMENT OVERVIEW (first and last 1000 chars):
START: {full_text[:1000]}
...
END: {full_text[-1000:]}

Only report MISSING sections as CRITICAL errors. Maximum 3 errors. Return JSON array:
[{{"page_num": 0, "severity": "CRITICAL", "message": "Missing required section: [section name]", "error_type": "structure"}}]
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000
            )
            
            return self.parse_ai_response(response.choices[0].message.content)
            
        except Exception as e:
            return []
    
    def parse_ai_response(self, ai_response: str) -> List[Dict]:
        """Parse AI response into error format"""
        import json
        try:
            # Extract JSON from response
            start_idx = ai_response.find('[')
            end_idx = ai_response.rfind(']') + 1
            if start_idx != -1 and end_idx != 0:
                json_str = ai_response[start_idx:end_idx]
                errors = json.loads(json_str)
                return errors
            else:
                # Fallback: parse text response
                return self.parse_text_response(ai_response)
        except:
            # Fallback: parse text response
            return self.parse_text_response(ai_response)
    
    def parse_text_response(self, response: str) -> List[Dict]:
        """Parse text response into error format"""
        errors = []
        lines = response.split('\n')
        
        current_error = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for error indicators
            if any(word in line.upper() for word in ['CRITICAL', 'MAJOR', 'MINOR', 'ERROR', 'VIOLATION', 'WRONG', 'MISSING']):
                if current_error:
                    errors.append(current_error)
                
                # Determine severity
                severity = "MINOR"
                if "CRITICAL" in line.upper() or "MUST" in line.upper():
                    severity = "CRITICAL"
                elif "MAJOR" in line.upper() or "IMPORTANT" in line.upper():
                    severity = "MAJOR"
                
                current_error = {
                    "page_num": 0,
                    "severity": severity,
                    "message": line,
                    "error_type": "formatting"
                }
        
        if current_error:
            errors.append(current_error)
        
        # If no errors parsed, create one from the whole response
        if not errors and len(response) > 50:
            errors.append({
                "page_num": 0,
                "severity": "MAJOR",
                "message": f"Validation completed. AI response: {response[:200]}...",
                "error_type": "analysis"
            })
        
        return errors

def validate_thesis_simple(pdf_path: Path) -> List[Dict]:
    """Simple validation function"""
    validator = SimpleAIValidator(pdf_path)
    return validator.validate_with_ai()