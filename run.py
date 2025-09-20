#!/usr/bin/env python3
"""
Simple launcher for TechCheck FDV Thesis Validator
"""

import os
import sys
from pathlib import Path

def main():
    """Main startup function"""
    print("Starting TechCheck FDV Thesis Validator")
    print("="*50)
    
    # Check basic requirements
    try:
        import fastapi
        import uvicorn
        import PyPDF2
        import openai
        print("* All required packages are installed")
    except ImportError as e:
        print(f"ERROR: Missing required package: {e}")
        print("Please install: pip install fastapi uvicorn PyPDF2 openai python-dotenv")
        sys.exit(1)
    
    # Check environment
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: No API key found in environment")
        print("Please set DEEPSEEK_API_KEY or OPENAI_API_KEY in .env file")
        sys.exit(1)
    
    print("* Environment configured")
    
    # Create directories
    Path("uploads").mkdir(exist_ok=True)
    Path("output").mkdir(exist_ok=True)
    print("* Created necessary directories")
    
    print("\nTARGET: Starting FastAPI server...")
    print("API will be available at: http://localhost:8000")
    print("API docs at: http://localhost:8000/docs")
    print("Health check: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop the server")
    print("="*50)
    
    # Start the server
    try:
        import uvicorn
        uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\nServer stopped")
    except Exception as e:
        print(f"ERROR: Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()