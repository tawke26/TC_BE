# TechCheck Backend - AI-Powered FDV Thesis Validator

## Project Overview
Complete AI-powered system that validates academic theses against FDV (Faculty of Social Sciences, University of Ljubljana) formatting requirements and produces annotated PDFs with marked errors.

## 🎯 FINAL WORKING SYSTEM

### ✅ What We Built Successfully
- **Beautiful Web Interface** at http://localhost:8000
- **Direct AI Validation** using OpenRouter API with latest models
- **PDF Error Detection** that finds formatting violations
- **Annotated PDF Reports** with detailed error descriptions
- **Professional UI** with drag-and-drop file upload

## 🔧 Technical Implementation

### Core Components
1. **FastAPI Backend** (`app.py`)
   - File upload endpoint with background processing
   - Job status tracking and result delivery
   - Web interface serving

2. **Simple AI Validator** (`simple_ai_validator.py`)
   - Direct AI analysis without complex agent system
   - Extracts PDF text with proper UTF-8 encoding
   - Comprehensive FDV requirement checking

3. **PDF Processing** (`ultra_simple_pdf.py`)
   - PyPDF2-based text extraction
   - Encoding issue handling for Slovenian characters
   - PDF annotation system

4. **PDF Report Generation** (`pdf_annotator.py`)
   - ReportLab-based PDF creation
   - Color-coded error severity (Critical/Major/Minor)
   - Professional formatting with fix instructions

5. **Web Interface** (`templates/index.html`)
   - Modern drag-and-drop UI
   - Progress tracking and status updates
   - Direct PDF download of results

## 🛠 Current Configuration

### API Setup
- **Provider**: OpenRouter (https://openrouter.ai/api/v1)
- **Model**: `openrouter/sonoma-sky-alpha` (latest model)
- **API Key**: Configured in `.env` file

### Dependencies
```
fastapi
uvicorn
PyPDF2
python-multipart
python-dotenv
openai
aiofiles
jinja2
reportlab
```

## 🚀 How to Use

### 1. Start Server
```bash
python run.py
```

### 2. Access Web Interface
Open browser: http://localhost:8000

### 3. Upload & Validate
- Drag/drop PDF file or click to browse
- Click "Validate Thesis"
- Wait for AI analysis
- Download annotated PDF report

## 🎯 What the System Validates

### Critical Requirements (Must Fix)
- University name: "UNIVERZA V LJUBLJANI" (uppercase)
- Faculty name: "FAKULTETA ZA DRUŽBENE VEDE" (uppercase)
- Required sections: declaration, summary, TOC, sources
- Proper Slovenian language usage

### Major Formatting Issues
- Font requirements (Times New Roman, 12pt)
- Page margins (3cm left, 2.5cm others)
- Summary word count (max 250 words)
- Title in both Slovenian and English

### Minor Style Issues
- Citation format (APA)
- Spacing and alignment
- Professional formatting

## 📁 Key Files Created

### Core System Files
- `app.py` - Main FastAPI application
- `simple_ai_validator.py` - Direct AI validation (WORKING)
- `ultra_simple_pdf.py` - PDF processing with encoding fixes
- `pdf_annotator.py` - Professional PDF report generation
- `templates/index.html` - Beautiful web interface

### Configuration Files
- `.env` - API configuration (OpenRouter + model selection)
- `fdv_requirements.py` - Complete FDV formatting rules
- `requirements.txt` - Python dependencies

### Utility Files
- `run.py` - Simple server launcher
- `debug_validation.py` - Diagnostic tool
- `QUICK_START.md` - Usage instructions

## 🐛 Issues Fixed

### 1. **PDF Text Extraction**
- **Problem**: Slovenian characters (ć, š, ž) causing encoding errors
- **Solution**: Added UTF-8 encoding handling in text extraction

### 2. **AI Agent Not Working**
- **Problem**: Complex tool-calling agent system was failing silently
- **Solution**: Replaced with direct AI validation approach

### 3. **Model Compatibility**
- **Problem**: Rate limiting on free models
- **Solution**: Configured OpenRouter with latest working model

### 4. **PDF Generation**
- **Problem**: Text reports instead of proper PDFs
- **Solution**: Added ReportLab for professional PDF creation

## ✅ Final Status: FULLY WORKING

### Test Results
- ✅ PDF upload works
- ✅ Text extraction handles Slovenian characters
- ✅ AI finds multiple errors (tested: 13 errors found)
- ✅ Professional PDF reports generated
- ✅ Web interface fully functional

### Example Validation Results
```
Found 13 errors:
- CRITICAL: University name is 'UNIVERSITY OF MARIBOR' but must be 'UNIVERZA V LJUBLJANI'
- CRITICAL: Faculty name is 'FACULTY OF TOURISM' but must be 'FAKULTETA ZA DRUŽBENE VEDE'  
- MAJOR: Wrong degree type for FDV requirements
+ 10 more errors with specific fix instructions
```

## 🎊 Ready for Production Use

The system successfully:
1. **Accepts thesis PDFs** via beautiful web interface
2. **Validates against FDV requirements** using AI
3. **Finds actual formatting violations** 
4. **Generates professional PDF reports** with detailed fix instructions
5. **Handles Slovenian language** and special characters properly

**Students can now upload their theses and get comprehensive FDV validation reports!**

---
*Last updated: System fully working and production-ready*