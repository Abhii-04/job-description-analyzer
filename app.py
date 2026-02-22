from flask import Flask, render_template, request
from utils import (
    calculate_inclusivity_score,
    calculate_readability_score,
    calculate_skills_coverage_score,
    calculate_overall_score,
    get_gemini_insights
)

app = Flask(__name__)


@app.route('/')
def index():
    """
    Home page - displays the job description input form
    """
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze the job description and return scores
    Accepts POST data with job_description and skills
    """
    # Get form data
    job_description = request.form.get('job_description', '')
    required_skills = request.form.get('skills', '')
    
    # Validate input
    if not job_description.strip():
        error = "Please provide a job description to analyze."
        return render_template('index.html', error=error)
    
    # Calculate all scores
    inclusivity_score, biased_words_count = calculate_inclusivity_score(job_description)
    readability_score = calculate_readability_score(job_description)
    skills_score, matched_skills = calculate_skills_coverage_score(job_description, required_skills)
    
    # Calculate overall weighted score
    overall_score = calculate_overall_score(inclusivity_score, readability_score, skills_score)
    
    # Get AI-powered insights from Gemini
    ai_insights = get_gemini_insights(
        job_description, 
        inclusivity_score, 
        readability_score, 
        skills_score, 
        matched_skills
    )
    
    # Prepare data for template
    results = {
        'overall_score': overall_score,
        'inclusivity_score': inclusivity_score,
        'biased_words_count': biased_words_count,
        'readability_score': readability_score,
        'skills_score': skills_score,
        'matched_skills': matched_skills,
        'total_skills': len([s.strip() for s in required_skills.split(',') if s.strip()]) if required_skills else 0,
        'ai_insights': ai_insights
    }
    
    return render_template('result.html', **results)


import os

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get("PORT", 5000))
    )