# Resume Analysis Application

A powerful Flask-based web application that analyzes resumes against job descriptions using AI to provide matching scores, keyword analysis, and personalized suggestions.

## Features

- Resume parsing support for PDF and Word documents
- Job description matching analysis
- AI-powered resume analysis using Google's Gemini AI
- Detailed skill analysis and job compatibility scoring
- Personalized improvement suggestions
- Modern and responsive user interface

## Technology Stack

- **Backend Framework**: Flask
- **AI/ML Libraries**:
  - Google Generative AI (Gemini)
  - NLTK
  - Spacy
  - Transformers
- **Document Processing**:
  - PyMuPDF
  - python-docx
- **Frontend**:
  - HTML/CSS
  - JavaScript

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd resumeAI2
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\activate
   
   # Linux/MacOS
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the project root
   - Add your Google Gemini API key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```

## Usage

1. Start the Flask application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Upload a resume (PDF or DOCX format) and enter the job description

4. Click "Analyze" to get detailed insights

## Project Structure

```
├── app.py                 # Main Flask application
├── resume_parser.py       # Resume text extraction logic
├── job_matching.py        # Job description matching analysis
├── ai_analysis.py         # Gemini AI integration
├── static/               # Static assets (CSS, images)
├── templates/            # HTML templates
├── uploads/              # Temporary resume storage
└── requirements.txt      # Python dependencies
```

## API Endpoints

### POST /
- Main endpoint for resume upload and analysis
- Accepts multipart form data with resume file and job description
- Returns rendered result page with analysis

### POST /analyze
- Alternative API endpoint for programmatic access
- Accepts resume file and job description
- Returns JSON with analysis results

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.