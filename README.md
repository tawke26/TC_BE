# TechCheck Backend - FDV Thesis Validator

An AI-powered system that validates academic theses against FDV (Faculty of Social Sciences, University of Ljubljana) formatting requirements and produces annotated PDFs with marked errors.

## Features

- 🤖 **AI Agent Validation** - Smart analysis using OpenAI with specialized tools
- 📄 **PDF Annotation** - Visual error marking with colored boxes and comments
- 🔧 **Comprehensive Checks** - Validates margins, fonts, structure, citations, and more
- 🌐 **REST API** - Easy integration with web frontends
- ⚡ **Background Processing** - Async validation for better performance

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment
Create a `.env` file with your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 3. Start the Server
```bash
python start.py
```

The API will be available at `http://localhost:8000`

## API Usage

### Upload Thesis for Validation
```bash
curl -X POST "http://localhost:8000/validate" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@thesis.pdf"
```

Response:
```json
{
  "job_id": "uuid-here",
  "status": "processing",
  "message": "Validation started. Use /status/{job_id} to check progress."
}
```

### Check Validation Status
```bash
curl "http://localhost:8000/status/{job_id}"
```

### Download Annotated PDF
```bash
curl "http://localhost:8000/download-pdf/{job_id}" -o validated_thesis.pdf
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/health` | Detailed health status |
| POST | `/validate` | Upload thesis for validation |
| GET | `/status/{job_id}` | Check validation progress |
| GET | `/result/{job_id}` | Get detailed validation results |
| GET | `/download-pdf/{job_id}` | Download annotated PDF |

## Interactive API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## FDV Requirements Validated

The system checks for:

### Front Matter
- ✅ University name format (UNIVERZA V LJUBLJANI)
- ✅ Faculty name format (FAKULTETA ZA DRUŽBENE VEDE)
- ✅ Title formatting (Times New Roman, 16pt, bold)
- ✅ Required sections (declaration, summary, TOC)

### Document Formatting
- ✅ Page margins (3cm left, 2.5cm others)
- ✅ Font requirements (Times New Roman 12pt)
- ✅ Line spacing (1.5 for main text)
- ✅ Text alignment (justified)

### Content Structure
- ✅ Summary word count (max 250 words)
- ✅ Keywords (minimum 3)
- ✅ Table of contents structure
- ✅ Citation format (APA style)
- ✅ Sources section formatting

### Output
- ✅ Annotated PDF with error markers
- ✅ Colored severity levels (Red=Critical, Orange=Major, Yellow=Minor)
- ✅ Detailed error descriptions
- ✅ Page-by-page validation

## Error Severity Levels

- **CRITICAL** 🔴 - Must fix (missing required sections, wrong university name)
- **MAJOR** 🟠 - Important formatting issues (wrong margins, fonts)
- **MINOR** 🟡 - Style recommendations (spacing, alignment)

## Architecture

```
User uploads PDF → FastAPI → AI Agent uses tools → PDF Processor → Annotated PDF
                                    ↓
                              [extract_text, measure_margins,
                               detect_fonts, mark_errors, etc.]
```

## Development

### Project Structure
```
TechCheck Backend/
├── app.py                 # FastAPI application
├── validation_agent.py    # AI agent with tool-calling
├── pdf_processor.py       # PDF processing tools
├── fdv_requirements.py    # FDV formatting rules
├── start.py              # Startup script
├── requirements.txt      # Dependencies
└── README.md            # This file
```

### Agent Tools
The AI agent has access to these specialized tools:
1. `extract_text_from_page()` - Extract text from specific pages
2. `detect_page_type()` - Identify page types (front, TOC, etc.)
3. `measure_margins()` - Calculate page margins
4. `get_font_properties()` - Analyze fonts and formatting
5. `find_text_position()` - Locate text coordinates
6. `count_words()` - Word counting
7. `detect_language()` - Slovenian/English detection
8. `check_text_format()` - Format validation
9. `mark_error()` - Error annotation
10. `get_page_count()` - Document length

## Requirements

- Python 3.11+
- OpenAI API key
- 2GB+ RAM for PDF processing
- Internet connection for AI agent

## License

MIT License - see LICENSE file for details.

## Support

For issues and feature requests, please open an issue on GitHub.