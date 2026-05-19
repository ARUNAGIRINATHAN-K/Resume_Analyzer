import os
import logging
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from werkzeug.utils import secure_filename
from app.nlp_processor import NLPProcessor
from app.scoring_engine import ScoringEngine
from app.utils import allowed_file, extract_text_from_pdf

bp = Blueprint('main', __name__)

# Initialize NLP processor and scoring engine
nlp_processor = NLPProcessor()
scoring_engine = ScoringEngine()

def perform_analysis(resume_text, job_description):
    """Run NLP analysis, scoring, and suggestions generation."""
    logging.debug("Processing resume and job description with NLP...")
    resume_analysis = nlp_processor.analyze_text(resume_text, text_type='resume')
    jd_analysis = nlp_processor.analyze_text(job_description, text_type='job_description')
    
    # Calculate scores and comparisons
    logging.debug("Calculating job fit score...")
    score_data = scoring_engine.calculate_job_fit_score(resume_analysis, jd_analysis)
    
    # Generate improvement suggestions
    suggestions = scoring_engine.generate_suggestions(resume_analysis, jd_analysis, score_data)
    
    return {
        'overall_score': score_data['overall_score'],
        'skill_score': score_data['skill_score'],
        'role_score': score_data['role_score'],
        'experience_score': score_data['experience_score'],
        'matched_keywords': score_data['matched_keywords'],
        'missing_keywords': score_data['missing_keywords'],
        'suggestions': suggestions,
        'resume_keywords': resume_analysis['keywords'],
        'jd_keywords': jd_analysis['keywords']
    }

@bp.route('/')
def index():
    """Render the main upload form."""
    return render_template('index.html')

@bp.route('/analyze', methods=['POST'])
def analyze():
    """Process the resume and job description, then show results."""
    try:
        # Check if file is uploaded
        if 'resume' not in request.files:
            flash('No resume file uploaded', 'error')
            return redirect(url_for('main.index'))
        
        file = request.files['resume']
        job_description = request.form.get('job_description', '').strip()
        
        # Validate inputs
        if file.filename == '':
            flash('No resume file selected', 'error')
            return redirect(url_for('main.index'))
        
        if not job_description:
            flash('Job description is required', 'error')
            return redirect(url_for('main.index'))
        
        if not allowed_file(file.filename):
            flash('Only PDF files are allowed', 'error')
            return redirect(url_for('main.index'))
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Extract text from resume
        resume_text = extract_text_from_pdf(file_path)
        if not resume_text:
            flash('Could not extract text from the PDF. Please ensure it\'s not a scanned document.', 'error')
            os.remove(file_path)  # Clean up
            return redirect(url_for('main.index'))
        
        # Clean up uploaded file
        os.remove(file_path)
        
        # Process with NLP and calculate scores
        results_data = perform_analysis(resume_text, job_description)
        results_data['resume_text'] = resume_text
        results_data['job_description'] = job_description
        
        return render_template('results.html', results=results_data)
        
    except Exception as e:
        logging.error(f"Error during analysis: {str(e)}")
        flash('An error occurred during analysis. Please try again.', 'error')
        return redirect(url_for('main.index'))

@bp.route('/api/analyze-text', methods=['POST'])
def analyze_text_api():
    """API endpoint to re-analyze resume text and job description."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request data'}), 400
            
        resume_text = data.get('resume_text', '').strip()
        job_description = data.get('job_description', '').strip()
        
        if not resume_text:
            return jsonify({'error': 'Resume text is required'}), 400
        if not job_description:
            return jsonify({'error': 'Job description is required'}), 400
            
        results_data = perform_analysis(resume_text, job_description)
        results_data['resume_text'] = resume_text
        results_data['job_description'] = job_description
        
        return jsonify(results_data)
    except Exception as e:
        logging.error(f"Error during API analysis: {str(e)}")
        return jsonify({'error': 'An error occurred during analysis.'}), 500

@bp.route('/sample-jd')
def sample_jd():
    """Return a sample job description."""
    sample = {
        'job_description': """We are looking for a skilled Python Developer to join our team. The ideal candidate will have experience with web development using Flask or Django, and proficiency in Python programming.

Requirements:
- 3+ years of experience in Python development
- Strong knowledge of web frameworks (Flask, Django)
- Experience with databases (PostgreSQL, MySQL)
- Familiarity with version control (Git)
- Knowledge of REST APIs and microservices
- Experience with testing frameworks (pytest, unittest)

Responsibilities:
- Develop and maintain web applications using Python
- Collaborate with cross-functional teams
- Write clean, maintainable code
- Participate in code reviews
- Troubleshoot and debug applications

Nice to have:
- Experience with cloud platforms (AWS, Azure)
- Knowledge of containerization (Docker)
- Familiarity with CI/CD pipelines"""
    }
    return jsonify(sample)

@bp.route('/export-pdf')
def export_pdf():
    """Export results as PDF (simple print-friendly version)."""
    return render_template('results.html', results=request.args.to_dict(), print_mode=True)
