import spacy
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter

nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    doc = nlp(text)
    keywords = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]
    return Counter(keywords)

def compare_resume_with_job(resume_text, job_description):
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description)

    matched_keywords = set(resume_keywords.keys()) & set(job_keywords.keys())
    match_score = len(matched_keywords) / len(job_keywords) * 100

    return match_score, matched_keywords
