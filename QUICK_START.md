# TechCheck FDV Thesis Validator - Quick Start

## ✅ System Status: WORKING!

Your AI-powered FDV thesis validator is ready to use with OpenRouter API.

## 🚀 How to Use

### 1. Start the Server
```bash
python run.py
```

The server will start on `http://localhost:8000`

### 2. Use the API

#### Option A: Web Interface (Easiest)
Open your browser and go to:
- **API Documentation**: http://localhost:8000/docs
- **Interactive Testing**: Use the web interface to upload PDFs

#### Option B: Command Line
```bash
# Upload thesis for validation
curl -X POST "http://localhost:8000/validate" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_thesis.pdf"

# Check status (use job_id from upload response)
curl "http://localhost:8000/status/YOUR_JOB_ID"

# Get detailed results
curl "http://localhost:8000/result/YOUR_JOB_ID"

# Download validation report
curl "http://localhost:8000/download-pdf/YOUR_JOB_ID" -o validation_report.txt
```

## 🎯 What It Validates

The AI agent checks for:
- ✅ University/Faculty name format (UPPERCASE)
- ✅ Page margins and formatting
- ✅ Font requirements (Times New Roman, 12pt)
- ✅ Summary word count (max 250 words)
- ✅ Table of contents structure
- ✅ Citation format
- ✅ Required sections (declaration, sources, etc.)

## 📊 Output

You'll get a detailed text report with:
- 🔴 **Critical errors** - Must fix (violate FDV requirements)
- 🟠 **Major errors** - Important formatting issues
- 🟡 **Minor errors** - Style recommendations

## 💡 Your Configuration

- **API**: OpenRouter
- **Model**: Claude 3 Haiku (fast, accurate, cheap)
- **API Key**: Configured ✅
- **Output**: Text-based validation reports

## 🔧 Need Help?

1. **Server not starting?** Check if all dependencies are installed
2. **API errors?** Verify your OpenRouter API key in `.env` file
3. **Want different model?** Edit `MODEL_NAME` in `.env` file

## 🎉 Ready to Validate!

Your thesis validator is working and ready to help students meet FDV requirements!