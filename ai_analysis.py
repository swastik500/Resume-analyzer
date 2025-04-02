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
    
    analysis_prompt = f"""
    Analyze this resume against the job description and provide structured feedback in JSON format with the following categories:
    - Strengths
    - Areas for Improvement
    - Missing Keywords
    - Technical Skills
    - Soft Skills
    
    Resume: {resume_text}
    
    Job Description: {job_description}
    """
    
    response = model.generate_content(analysis_prompt)
    
    try:
        # Structure the suggestions in a dictionary format
        suggestions = {
            "strengths": [],
            "improvements": [],
            "missing_keywords": [],
            "technical_skills": [],
            "soft_skills": []
        }
        
        # Parse the response and populate the suggestions
        current_category = None
        for line in response.text.split('\n'):
            line = line.strip()
            if line in suggestions.keys():
                current_category = line
            elif line.startswith('- ') and current_category:
                suggestions[current_category].append(line[2:])
        
        return {
            'score': score,
            'suggestions': suggestions
        }
    except Exception as e:
        print(f"Error parsing AI response: {e}")
        return {
            'score': score,
            'suggestions': {
                'General Suggestions': [
                    'Unable to generate detailed suggestions at this time.',
                    'Please try again later.'
                ]
            }
        }
