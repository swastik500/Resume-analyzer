from flask import Flask, request, render_template, flash
from resume_parser import extract_resume_text
from job_matching import compare_resume_with_job
from ai_analysis import analyze_resume_with_gemini
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Add this line for flash messages

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if 'resume' not in request.files:
            flash('No file uploaded')
            return render_template("index.html")
            
        resume_file = request.files["resume"]
        if resume_file.filename == '':
            flash('No file selected')
            return render_template("index.html")
            
        if not allowed_file(resume_file.filename):
            flash('Please upload a PDF or Word document')
            return render_template("index.html")

        job_description = request.form["job_description"]
        
        # Save the file temporarily
        file_path = os.path.join(UPLOAD_FOLDER, resume_file.filename)
        resume_file.save(file_path)

        resume_text = extract_resume_text(file_path)

        match_score, matched_keywords = compare_resume_with_job(resume_text, job_description)
        ai_suggestions = analyze_resume_with_gemini(resume_text, job_description)
        
        # Mock data for skills and jobs sections
        technical_skills = "Python, JavaScript, React, Node.js, SQL, AWS"
        soft_skills = "Communication, Leadership, Problem Solving, Team Collaboration"
        job_matches = "Senior Full Stack Developer, Frontend Engineer, Backend Developer"

        return render_template("result.html", 
            score=match_score, 
            keywords=matched_keywords, 
            suggestions=ai_suggestions,
            technical_skills=technical_skills,
            soft_skills=soft_skills,
            job_matches=job_matches
        )

    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        job_description = request.form["job_description"]
        resume_file = request.files["resume"]
        resume_text = extract_resume_text(resume_file)

        match_score, matched_keywords = compare_resume_with_job(resume_text, job_description)
        ai_suggestions = analyze_resume_with_gemini(resume_text, job_description)
        
        # Mock data for skills and jobs sections
        technical_skills = "Python, JavaScript, React, Node.js, SQL, AWS"
        soft_skills = "Communication, Leadership, Problem Solving, Team Collaboration"
        job_matches = "Senior Full Stack Developer, Frontend Engineer, Backend Developer"

        return render_template("result.html", 
            score=match_score, 
            keywords=matched_keywords, 
            suggestions=ai_suggestions,
            technical_skills=technical_skills,
            soft_skills=soft_skills,
            job_matches=job_matches
        )

    except Exception as e:
        return f"Error: {str(e)}", 500


if __name__ == "__main__":
    app.run(debug=True)
