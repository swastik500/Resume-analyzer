import google.generativeai as genai
from job_matching import compare_resume_with_job
from resume_parser import extract_resume_sections

genai.configure(api_key="AIzaSyBTifvSxk2-drcNIbrC2AqrfhjzD3DldPU")

def calculate_resume_score(resume_text, job_description):
    # Calculate match score with job description (30% weight)
    match_score, _ = compare_resume_with_job(resume_text, job_description)
    weighted_match_score = match_score * 0.3
    
    # Analyze resume sections completeness (40% weight)
    sections = extract_resume_sections(resume_text)  # Now passing text directly
    completeness_score = 0
    essential_sections = ['education', 'experience', 'skills']
    for section in essential_sections:
        if section in sections and sections[section]:
            completeness_score += 33.33
    weighted_completeness_score = completeness_score * 0.4
    
    # Use Gemini for qualitative analysis (30% weight)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Analyze this resume's quality (formatting, clarity, relevance) on a scale of 0-100:\n{resume_text}"
    response = model.generate_content(prompt)
    try:
        quality_score = float(''.join(filter(str.isdigit, response.text[:10])))
    except:
        quality_score = 70  # Default score if parsing fails
    weighted_quality_score = quality_score * 0.3
    
    # Calculate final score
    final_score = round(weighted_match_score + weighted_completeness_score + weighted_quality_score)
    return min(100, max(0, final_score))  # Ensure score is between 0 and 100

def analyze_resume_with_gemini(resume_text, job_description):
    model = genai.GenerativeModel("gemini-1.5-flash")
    score = calculate_resume_score(resume_text, job_description)
    
    # Create a structured prompt for better formatting
    analysis_prompt = f"""
Analyze the resume against the job description and provide structured feedback in the following format:

**Strengths:**
- List key strengths and matches

**Areas for Improvement:**
- List specific improvement suggestions

**Missing Keywords:**
- List important keywords from job description missing in resume

Resume: {resume_text}

Job Description: {job_description}
"""
    
    response = model.generate_content(analysis_prompt)
    formatted_response = response.text.strip()
    
    return str(score), formatted_response
