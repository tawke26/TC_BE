#!/usr/bin/env python3
"""
Debug script to test PDF text extraction and AI validation
"""

import os
import PyPDF2
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def test_pdf_extraction(pdf_path):
    """Test what text we can extract from the PDF"""
    print(f"Testing PDF extraction from: {pdf_path}")
    print("=" * 50)
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            print(f"Total pages: {len(reader.pages)}")
            
            # Extract first few pages
            for i in range(min(3, len(reader.pages))):
                print(f"\n--- PAGE {i+1} TEXT ---")
                text = reader.pages[i].extract_text()
                print(f"Length: {len(text)} characters")
                print("First 500 characters:")
                print(text[:500])
                print("...")
                
                # Check for FDV indicators
                text_lower = text.lower()
                if "univerza" in text_lower:
                    print("✓ Found 'univerza' in text")
                if "fakulteta" in text_lower:
                    print("✓ Found 'fakulteta' in text")
                if "ljubljana" in text_lower:
                    print("✓ Found 'ljubljana' in text")
                    
    except Exception as e:
        print(f"ERROR extracting PDF: {e}")

def test_ai_validation(text_sample):
    """Test AI validation with a sample text"""
    print("\nTesting AI validation...")
    print("=" * 50)
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("DEEPSEEK_API_KEY")
    )
    
    model = os.getenv("MODEL_NAME", "openrouter/sonoma-sky-alpha")
    print(f"Using model: {model}")
    
    simple_prompt = f"""
You are validating a thesis against FDV requirements.

Check this text for these specific errors:
1. University name should be "UNIVERZA V LJUBLJANI" (all uppercase)
2. Faculty name should be "FAKULTETA ZA DRUŽBENE VEDE" (all uppercase)

TEXT TO CHECK:
{text_sample}

Find ANY formatting violations and respond with:
CRITICAL: [list any critical errors found]
MAJOR: [list any major errors found]  
MINOR: [list any minor errors found]

If you find no errors, explain why.
"""

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": simple_prompt}],
            max_tokens=1000
        )
        
        print("AI Response:")
        print(response.choices[0].message.content)
        
    except Exception as e:
        print(f"ERROR with AI validation: {e}")

def main():
    print("FDV Thesis Validation Debugger")
    print("=" * 50)
    
    # Check if there are any recent uploads
    upload_dir = Path("uploads")
    if upload_dir.exists():
        pdf_files = list(upload_dir.glob("*.pdf"))
        if pdf_files:
            latest_pdf = max(pdf_files, key=lambda p: p.stat().st_mtime)
            print(f"Found recent PDF: {latest_pdf}")
            
            # Test extraction
            test_pdf_extraction(latest_pdf)
            
            # Get sample text for AI test
            with open(latest_pdf, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                if len(reader.pages) > 0:
                    sample_text = reader.pages[0].extract_text()[:1000]
                    test_ai_validation(sample_text)
        else:
            print("No PDF files found in uploads directory")
    else:
        print("Uploads directory not found")

if __name__ == "__main__":
    main()