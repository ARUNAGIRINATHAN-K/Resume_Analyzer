import os
import logging
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
import fitz  # PyMuPDF
from nlp_processor import NLPProcessor
from scoring_engine import ScoringEngine

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize NLP processor and scoring engine
nlp_processor = NLPProcessor()
scoring_engine = ScoringEngine()

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file_path):
    """Extract text from PDF using PyMuPDF."""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.strip()
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {str(e)}")
        return None

@app.route('/')
def index():
    """Render the main upload form."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Process the resume and job description, then show results."""
    try:
        # Check if file is uploaded
        if 'resume' not in request.files:
            flash('No resume file uploaded', 'error')
            return redirect(url_for('index'))
        
        file = request.files['resume']
        job_description = request.form.get('job_description', '').strip()
        
        # Validate inputs
        if file.filename == '':
            flash('No resume file selected', 'error')
            return redirect(url_for('index'))
        
        if not job_description:
            flash('Job description is required', 'error')
            return redirect(url_for('index'))
        
        if not allowed_file(file.filename):
            flash('Only PDF files are allowed', 'error')
            return redirect(url_for('index'))
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Extract text from resume
        resume_text = extract_text_from_pdf(file_path)
        if not resume_text:
            flash('Could not extract text from the PDF. Please ensure it\'s not a scanned document.', 'error')
            os.remove(file_path)  # Clean up
            return redirect(url_for('index'))
        
        # Clean up uploaded file
        os.remove(file_path)
        
        # Process with NLP
        logging.debug("Processing resume and job description with NLP...")
        resume_analysis = nlp_processor.analyze_text(resume_text, text_type='resume')
        jd_analysis = nlp_processor.analyze_text(job_description, text_type='job_description')
        
        # Calculate scores and comparisons
        logging.debug("Calculating job fit score...")
        score_data = scoring_engine.calculate_job_fit_score(resume_analysis, jd_analysis)
        
        # Generate improvement suggestions
        suggestions = scoring_engine.generate_suggestions(resume_analysis, jd_analysis, score_data)
        
        # Prepare results data
        results_data = {
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
        
        return render_template('results.html', results=results_data)
        
    except Exception as e:
        logging.error(f"Error during analysis: {str(e)}")
        flash('An error occurred during analysis. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/sample-jd')
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

@app.route('/export-pdf')
def export_pdf():
    """Export results as PDF (simple print-friendly version)."""
    # For now, just redirect to print; in production, use a library like ReportLab
    return render_template('results.html', results=request.args.to_dict(), print_mode=True)
