import PyPDF2
from docx import Document
import os
import re
from typing import Dict, List
import mimetypes

def extract_resume_text(file_path):
    if not os.path.exists(file_path):
        raise ValueError("File does not exist")

    file_extension = os.path.splitext(file_path)[1].lower()
    mime_type, _ = mimetypes.guess_type(file_path)
    
    # Validate file type using both extension and MIME type
    if file_extension == '.pdf' and mime_type == 'application/pdf':
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ''
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            raise ValueError(f"Error reading PDF file: {str(e)}")
            
    elif file_extension in ['.doc', '.docx'] and mime_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        try:
            doc = Document(file_path)
            text = ''
            for paragraph in doc.paragraphs:
                text += paragraph.text + '\n'
            return text
        except Exception as e:
            raise ValueError(f"Error reading Word document: {str(e)}")
        
    else:
        raise ValueError("Unsupported file format. Please upload a valid PDF or Word document.")

def extract_resume_sections(input_data) -> Dict[str, List[str]]:
    # Handle both file path and text input
    if isinstance(input_data, str):
        if os.path.exists(input_data):
            full_text = extract_resume_text(input_data)
        else:
            full_text = input_data
    else:
        raise ValueError("Input must be either a file path or text content")
    
    # Initialize sections dictionary
    sections = {
        'education': [],
        'experience': [],
        'skills': [],
        'projects': [],
        'certifications': []
    }
    
    # Split text into lines and remove empty lines
    lines = [line.strip() for line in full_text.split('\n') if line.strip()]
    
    current_section = None
    section_content = []
    
    # Common section headers
    section_headers = {
        'education': ['education', 'academic background', 'academic qualification'],
        'experience': ['experience', 'work experience', 'employment history', 'work history'],
        'skills': ['skills', 'technical skills', 'core competencies', 'expertise'],
        'projects': ['projects', 'project experience', 'key projects'],
        'certifications': ['certifications', 'certificates', 'professional certifications']
    }
    
    for line in lines:
        # Check if line is a section header
        for section, headers in section_headers.items():
            if any(header.lower() in line.lower() for header in headers):
                # Save previous section content if exists
                if current_section and section_content:
                    sections[current_section].extend(section_content)
                    section_content = []
                current_section = section
                break
        else:
            if current_section:
                section_content.append(line)
    
    # Add last section content
    if current_section and section_content:
        sections[current_section].extend(section_content)
    
    # Clean up sections
    for section in sections:
        sections[section] = [item for item in sections[section] if len(item) > 3]
    
    return sections
